import datetime
from pathlib import Path
import os
import tempfile
from typing import Sequence, Optional, List, Tuple

import pexpect

from terminhtml._exc import CommandInternalException
from terminhtml.exc import UserCommandException
from terminhtml.output import LineOutput, Output
from terminhtml.runner.commandresult import CommandResult


def run_commands_in_temp_dir(
    commands: Sequence[str],
    setup_command: Optional[str] = None,
    input: Optional[List[str]] = None,
    allow_exceptions: bool = False,
    prompt_matchers: Optional[List[str]] = None,
    command_timeout: int = 10,
) -> List[CommandResult]:
    def run(command: str, last_cwd: Path, input: Optional[str] = None) -> CommandResult:
        try:
            return _run(
                command,
                last_cwd,
                input,
                prompt_matchers=prompt_matchers,
                command_timeout=command_timeout,
            )
        except (
            pexpect.exceptions.EOF,
            pexpect.exceptions.TIMEOUT,
            CommandInternalException,
        ) as e:
            if isinstance(e, CommandInternalException):
                if allow_exceptions:
                    return CommandResult(
                        input=e.input,
                        output=e.output,
                        cwd=e.cwd,
                    )
                raise UserCommandException(
                    f"Command failed: {command} due to {e} as "
                    f"part of running {commands=} {setup_command=} {input=}",
                    output=e.output,
                    cwd=e.cwd,
                ) from e
            exc_parts = e.value.split("\n")
            output = [
                part
                for part in exc_parts
                if part.startswith("before (last 100 chars): ")
            ][0]
            output_without_prefix = output[len("before (last 100 chars): ") :]
            raise UserCommandException(
                f"Command failed: {command} as "
                f"part of running {commands=} {setup_command=} {input=}",
                output_without_prefix,
                last_cwd,
            ) from e

    input = input or []
    orig_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        last_cwd = Path(tmpdir)
        if setup_command:
            # Don't save the output of the setup command
            out_command = run(setup_command, last_cwd)
            last_cwd = out_command.cwd
        out_commands: List[CommandResult] = []
        for i, command in enumerate(commands):
            try:
                this_command_input = input[i]
            except IndexError:
                this_command_input = None
            out_command = run(command, last_cwd, input=this_command_input)
            last_cwd = out_command.cwd
            out_commands.append(out_command)
        os.chdir(orig_dir)
    return out_commands


def _get_terminal_output_with_prompt_at_end(output: str) -> str:
    lines = output.split("\r\n")

    return "\r\n".join([*lines[:-1], "# " + lines[-1] + "$ "])


def _get_real_output_and_cwd_from_output_lines(
    lines: List[LineOutput], last_cwd: Path, input_line: LineOutput
) -> Tuple[Output, Path]:
    # Find index of last real line
    i = 0
    for i, line in enumerate(reversed(lines)):
        if line:
            break
    last_real_idx = -(i + 1)
    real_output = Output(lines=lines[:last_real_idx])
    cwd = Path(lines[last_real_idx].line.strip())
    if not cwd.exists():
        raise CommandInternalException(
            f"{cwd=} does not exist.", real_output, input_line, last_cwd
        )
    return real_output, cwd


def _run(
    command: str,
    cwd: Path,
    input: Optional[str] = None,
    prompt_matchers: Optional[List[str]] = None,
    command_timeout: int = 10,
) -> CommandResult:
    use_input = input.split("\n") if input else []
    stop_for_input_chars = ["\r\n", pexpect.EOF, *(prompt_matchers or [])]
    new_line_index = 0
    eof_index = 1
    prompt_indices = [
        i
        for i in range(len(stop_for_input_chars))
        if i not in [new_line_index, eof_index]
    ]

    start_time = datetime.datetime.now()
    process = pexpect.spawn(
        f"bash -c \"cd '{cwd}' && {command} && printf '\\n' && pwd\"", encoding="utf-8"
    )
    output_lines: List[LineOutput] = []
    input_idx = 0
    while True:
        matched_idx = process.expect(stop_for_input_chars, timeout=command_timeout)
        # Process printed a new line, collect it and the time
        this_stdout = _extract_pexpect_output_and_strip_ending_newlines(process)
        output_lines.append(LineOutput(line=this_stdout, time=datetime.datetime.now()))
        if matched_idx in prompt_indices:
            # Process printed a prompt, send input
            process.sendline(use_input[input_idx])
            input_idx += 1
        elif matched_idx == eof_index:
            # Process printed EOF, break
            break

    start_line = LineOutput(line=command, time=start_time)
    real_output, new_cwd = _get_real_output_and_cwd_from_output_lines(
        output_lines, cwd, start_line
    )
    return CommandResult(input=start_line, output=real_output, cwd=new_cwd)


def _extract_pexpect_output(spawn: pexpect.spawn) -> str:
    if spawn.after == pexpect.EOF:
        return spawn.before
    return spawn.before + spawn.after


def _extract_pexpect_output_and_strip_ending_newlines(spawn: pexpect.spawn) -> str:
    output = _extract_pexpect_output(spawn)
    return output.rstrip("\r\n")

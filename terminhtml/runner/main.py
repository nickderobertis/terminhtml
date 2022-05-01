from pathlib import Path
import os
import tempfile
from typing import Sequence, Optional, List, Tuple

import pexpect

from terminhtml.runner.commandresult import CommandResult


def run_commands_in_temp_dir(
    commands: Sequence[str],
    setup_command: Optional[str] = None,
    input: Optional[List[str]] = None,
    allow_exceptions: bool = False,
) -> List[CommandResult]:
    def run(command: str, last_cwd: Path, input: Optional[str] = None) -> CommandResult:
        try:
            return _run(command, last_cwd, input)
        except (
            pexpect.exceptions.EOF,
            pexpect.exceptions.TIMEOUT,
            CommandException,
        ) as e:
            if isinstance(e, CommandException):
                if allow_exceptions:
                    return CommandResult(
                        input=command,
                        output=e.output,
                        cwd=e.cwd,
                    )
                raise CommandException(
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
            raise CommandException(
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


class CommandException(Exception):
    def __init__(self, message: str, output: str, cwd: Path) -> None:
        self.output = output
        self.cwd = cwd
        super().__init__(message)

    def __str__(self) -> str:
        return f"{super().__str__()}\n{self.cwd=} with output:\n{self.output}"


def _get_terminal_output_with_prompt_at_end(output: str) -> str:
    lines = output.split("\r\n")

    return "\r\n".join([*lines[:-1], "# " + lines[-1] + "$ "])


def _get_real_output_and_cwd_from_output(
    output: str, last_cwd: Path
) -> Tuple[str, Path]:
    lines = output.split("\r\n")
    # Find index of last real line
    i = 0
    for i, line in enumerate(reversed(lines)):
        if line:
            break
    last_real_idx = -(i + 1)
    real_output = "\r\n".join(lines[:last_real_idx])
    cwd = Path(lines[last_real_idx].strip())
    if not cwd.exists():
        raise CommandException(f"{cwd=} does not exist.", output, last_cwd)
    return real_output, cwd


def _run(command: str, cwd: Path, input: Optional[str] = None) -> CommandResult:
    use_input = input.split("\n") if input else []
    stop_for_input_chars = ["]: ", r"0m: "]

    process = pexpect.spawn(
        f"bash -c \"cd '{cwd}' && {command} && printf '\\n' && pwd\"", encoding="utf-8"
    )
    all_stdout = ""
    for inp in use_input:
        process.expect_exact(stop_for_input_chars, timeout=10)
        this_stdout = process.before + process.after
        all_stdout += this_stdout
        process.sendline(inp)
    process.expect(pexpect.EOF)
    real_output, new_cwd = _get_real_output_and_cwd_from_output(process.before, cwd)
    all_stdout += real_output
    return CommandResult(input=command, output=all_stdout, cwd=new_cwd)


def _commands_to_list(commands: Sequence[CommandResult]) -> List[str]:
    output: List[str] = []
    for command in commands:
        output.append(f"$ {command.input}")
        output.append(command.output)
    return output

import datetime
from pathlib import Path
import os
import tempfile
from typing import Sequence, Optional, List, Tuple, Dict

import pexpect
from pydantic import BaseModel

from terminhtml._exc import CommandInternalException
from terminhtml.exc import UserCommandException
from terminhtml.output import LineOutput, Output, LineEnding, PromptOutput
from terminhtml.runner.commandresult import CommandResult, RunnerContext


def run_commands(
    commands: Sequence[str],
    setup_command: Optional[str] = None,
    input: Optional[List[str]] = None,
    allow_exceptions: bool = False,
    prompt_matchers: Optional[List[str]] = None,
    command_timeout: int = 10,
    cwd: Optional[Path] = None,
    echo: bool = False,
) -> List[CommandResult]:
    def run(
        command: str, last_context: RunnerContext, input: Optional[str] = None
    ) -> CommandResult:
        try:
            return _run(
                command,
                last_context,
                input,
                prompt_matchers=prompt_matchers,
                command_timeout=command_timeout,
                echo=echo,
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
                        context=e.context,
                    )
                raise UserCommandException(
                    f"Command failed: {command} due to {e} as "
                    f"part of running {commands=} {setup_command=} {input=}",
                    output=e.output,
                    context=e.context,
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
                last_context,
            ) from e

    input = input or []
    orig_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        if cwd:
            begin_cwd = cwd
        else:
            begin_cwd = Path(tmpdir)
        last_context = RunnerContext(cwd=begin_cwd)
        if setup_command:
            # Don't save the output of the setup command
            out_command = run(setup_command, last_context)
            last_context = out_command.context
        out_commands: List[CommandResult] = []
        for i, command in enumerate(commands):
            try:
                this_command_input = input[i]
            except IndexError:
                this_command_input = None
            out_command = run(command, last_context, input=this_command_input)
            last_context = out_command.context
            out_commands.append(out_command)
        os.chdir(orig_dir)
    return out_commands


def _get_terminal_output_with_prompt_at_end(output: str) -> str:
    lines = output.split("\r\n")

    return "\r\n".join([*lines[:-1], "# " + lines[-1] + "$ "])


def _get_real_output_and_context_from_output_lines(
    lines: List[LineOutput], last_context: RunnerContext, input_line: LineOutput
) -> Tuple[Output, RunnerContext]:
    command_marker_indices = _find_persistence_command_markers(lines)
    real_output = Output(lines=lines[: (command_marker_indices.last_real_output + 1)])
    cwd = Path(lines[command_marker_indices.path].line.strip())
    if not cwd.exists():
        raise CommandInternalException(
            f"{cwd=} does not exist.", real_output, input_line, last_context
        )
    # Extract environment lines
    env: Dict[str, str] = {}
    for line in lines[
        command_marker_indices.begin_env + 1 : command_marker_indices.end_env
    ]:
        if not line.line:
            # Sometimes an extra blank line gets added, ignore them
            continue
        variable, value = line.line.split("=", 1)

        env[variable] = value
    context = RunnerContext(cwd=cwd, env=env)
    return real_output, context


class CommandMarkerIndices(BaseModel):
    begin_persistence: int
    end_persistence: int
    begin_path: int
    end_path: int
    begin_env: int
    end_env: int

    @property
    def last_real_output(self) -> int:
        return self.begin_persistence - 1

    @property
    def path(self) -> int:
        if self.begin_path != (self.end_path - 2):
            raise ValueError("More than one line printed for path")
        return self.begin_path + 1


def _find_persistence_command_markers(lines: List[LineOutput]) -> CommandMarkerIndices:
    begin_persistence = None
    end_persistence = None
    begin_path = None
    end_path = None
    begin_env = None
    end_env = None
    for i, line in enumerate(lines):
        if line.line == "::BEGIN TERMINHTML PERSISTENCE::":
            begin_persistence = i
        if line.line == "::END TERMINHTML PERSISTENCE::":
            end_persistence = i
        if line.line == "::BEGIN TERMINHTML PATH::":
            begin_path = i
        if line.line == "::END TERMINHTML PATH::":
            end_path = i
        if line.line == "::BEGIN TERMINHTML ENV::":
            begin_env = i
        if line.line == "::END TERMINHTML ENV::":
            end_env = i
    if any(
        x is None
        for x in [
            begin_persistence,
            end_persistence,
            begin_path,
            end_path,
            begin_env,
            end_env,
        ]
    ):
        raise ValueError(f"Could not find all command markers in lines: {lines}")
    return CommandMarkerIndices(
        begin_persistence=begin_persistence,
        end_persistence=end_persistence,
        begin_path=begin_path,
        end_path=end_path,
        begin_env=begin_env,
        end_env=end_env,
    )


_terminal_persistence_commands = [
    "echo '::BEGIN TERMINHTML PERSISTENCE::'",
    "echo '::BEGIN TERMINHTML PATH::'",
    "pwd",
    "echo '::END TERMINHTML PATH::'",
    "echo '::BEGIN TERMINHTML ENV::'",
    "set",
    "echo '::END TERMINHTML ENV::'",
    "echo '::END TERMINHTML PERSISTENCE::'",
]
_terminal_persistence_command = " && ".join(_terminal_persistence_commands)


def _run(
    command: str,
    context: RunnerContext,
    input: Optional[str] = None,
    prompt_matchers: Optional[List[str]] = None,
    command_timeout: int = 10,
    echo: bool = False,
) -> CommandResult:
    use_input = input.split("\n") if input else []
    line_and_output_end_chars = ["\r\n", "\r", pexpect.EOF]
    stop_for_input_chars = [*line_and_output_end_chars, *(prompt_matchers or [])]
    new_line_index = 0
    carriage_return_index = 1
    line_break_indices = [new_line_index, carriage_return_index]
    eof_index = 2
    prompt_indices = [
        i
        for i in range(len(stop_for_input_chars))
        if i not in [new_line_index, carriage_return_index, eof_index]
    ]

    if echo:
        print(f"$ {command}")

    start_time = datetime.datetime.now()
    process = pexpect.spawn(
        f"bash -c \"cd '{context.cwd}' && {command} && printf '\\n' && {_terminal_persistence_command}\"",
        encoding="utf-8",
        env=context.env,
    )
    output_lines: List[LineOutput] = []
    input_idx = 0
    skip_next_lines = 0
    processing_terminhtml_context_commands = False
    while True:
        line_matchers: List[str]
        if processing_terminhtml_context_commands:
            # We have finished the user command and are now determining the output context
            # Stop matching on prompt matchers
            line_matchers = line_and_output_end_chars
        else:
            line_matchers = stop_for_input_chars

        matched_idx = process.expect(line_matchers, timeout=command_timeout)
        # Process printed a new line
        # First check if we should skip the line due to it being user input that
        # is already tracked in PromptOutput
        if skip_next_lines > 0:
            skip_next_lines -= 1
            continue

        # Collect the line and the time
        this_stdout = _extract_pexpect_output_and_strip_ending_newlines(process)
        line_ending: LineEnding
        if matched_idx == carriage_return_index:
            line_ending = LineEnding.CR
        else:
            line_ending = LineEnding.CRLF

        if (
            matched_idx in line_break_indices
            and this_stdout == "::BEGIN TERMINHTML PERSISTENCE::"
        ):
            # We have finished the user command and are now determining the output context
            processing_terminhtml_context_commands = True

        prompt_output: Optional[PromptOutput] = None
        if matched_idx in prompt_indices:
            # Process printed a prompt, send input
            try:
                user_input = use_input[input_idx]
            except IndexError:
                raise IncorrectCommandSpecificationException(
                    f"Received prompt for input but no input was provided. "
                    f"Prompt: {this_stdout}\nInput: {use_input}"
                )
            process.sendline(user_input)
            input_idx += 1
            prompt_output = PromptOutput(prompt=this_stdout, user_input=user_input)
            # The next lines will be the input we just provided, skip them
            skip_next_lines = len(user_input.split("\n"))
            if echo:
                print(f"{this_stdout} {user_input}")
        elif echo and not processing_terminhtml_context_commands:
            if line_ending == LineEnding.CR:
                print(this_stdout, end="\r")
            else:
                print(this_stdout)

        output_lines.append(
            LineOutput(
                line=this_stdout,
                time=datetime.datetime.now(),
                line_ending=line_ending,
                prompt_output=prompt_output,
            )
        )
        if matched_idx == eof_index:
            # Process printed EOF, break
            break

    start_line = LineOutput(line=command, time=start_time, line_ending=LineEnding.CRLF)
    real_output, new_context = _get_real_output_and_context_from_output_lines(
        output_lines, context, start_line
    )
    return CommandResult(input=start_line, output=real_output, context=new_context)


def _extract_pexpect_output(spawn: pexpect.spawn) -> str:
    if spawn.after == pexpect.EOF:
        return spawn.before
    return spawn.before + spawn.after


def _extract_pexpect_output_and_strip_ending_newlines(spawn: pexpect.spawn) -> str:
    output = _extract_pexpect_output(spawn)
    return output.rstrip("\r\n")

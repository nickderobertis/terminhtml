import shlex
from enum import Enum
from typing import Sequence, Union

from click.testing import Result
from typer.testing import CliRunner

from terminhtml.cli import app
from tests.e2e import ext_click

runner = CliRunner()


class CLIRunnerException(Exception):
    pass


class ExceptionHandling(str, Enum):
    RAISE = "raise"
    IGNORE = "ignore"


def run_cli(
    command: str,
    exception_handling: ExceptionHandling = ExceptionHandling.RAISE,
) -> Result:
    split_command = shlex.split(command)
    result = runner.invoke(app, split_command)
    if exception_handling == ExceptionHandling.RAISE and result.exit_code != 0:
        output = ext_click.result_to_message(result)
        full_command = shlex.join(["terminhtml", command])
        raise CLIRunnerException(
            f"{full_command} exited with code {result.exit_code}.\n{output}"
        )
    return result

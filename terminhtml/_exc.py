from pathlib import Path

from terminhtml.base_exc import TerminHTMLException
from terminhtml.output import Output, LineOutput
from terminhtml.runner.commandresult import RunnerContext


class TerminHTMLInternalException(TerminHTMLException):
    """
    Base class for all exceptions that represent internal errors.
    """

    pass


class CommandInternalException(TerminHTMLInternalException):
    def __init__(
        self, message: str, output: Output, input: LineOutput, context: RunnerContext
    ) -> None:
        self.output = output
        self.input = input
        self.context = context
        super().__init__(message)

    def __str__(self) -> str:
        return f"{super().__str__()}\n{self.context=} with input {self.input}\noutput:\n{self.output}"

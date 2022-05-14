from pathlib import Path

from terminhtml.base_exc import TerminHTMLException
from terminhtml.output import Output
from terminhtml.runner.commandresult import RunnerContext


class TerminHTMLUserException(TerminHTMLException):
    """
    Base class for all expected exceptions in TerminHTML.
    """

    pass


class IncorrectCommandSpecificationException(TerminHTMLUserException):
    """
    Raised if the command specification is incorrect.
    """

    pass


class UserCommandException(TerminHTMLUserException):
    """
    Exception for user commands.
    """

    def __init__(self, message: str, output: Output, context: RunnerContext) -> None:
        self.output = output
        self.context = context
        super().__init__(message)

    def __str__(self) -> str:
        return f"{super().__str__()}\n{self.context=} with output:\n{self.output}"

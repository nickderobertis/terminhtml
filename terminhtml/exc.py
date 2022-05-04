from pathlib import Path

from terminhtml.base_exc import TerminHTMLException


class TerminHTMLUserException(TerminHTMLException):
    """
    Base class for all expected exceptions in TerminHTML.
    """

    pass


class UserCommandException(TerminHTMLUserException):
    """
    Exception for user commands.
    """

    def __init__(self, message: str, output: str, cwd: Path) -> None:
        self.output = output
        self.cwd = cwd
        super().__init__(message)

    def __str__(self) -> str:
        return f"{super().__str__()}\n{self.cwd=} with output:\n{self.output}"

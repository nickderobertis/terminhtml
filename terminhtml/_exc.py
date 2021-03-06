from terminhtml.base_exc import TerminHTMLException
from terminhtml.output import LineOutput, Output
from terminhtml.runner.commandresult import RunnerContext


class TerminHTMLInternalException(TerminHTMLException):
    """
    Base class for all exceptions that represent internal errors.
    """


class TerminHTMLRunnerException(TerminHTMLInternalException):
    pass


class CannotFindPersistenceLineMarkersException(TerminHTMLRunnerException):
    pass


class CommandInternalException(TerminHTMLInternalException):
    def __init__(
        self, message: str, output: Output, input: LineOutput, context: RunnerContext
    ) -> None:
        self.output = output
        self.input = input
        self.context = context
        super().__init__(message)

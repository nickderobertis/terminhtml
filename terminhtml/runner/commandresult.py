import datetime
from pathlib import Path

from pydantic import BaseModel

from terminhtml.ansi_converter import ansi_to_html
from terminhtml.output import Output, LineOutput


class LineWithDelay(LineOutput):
    delay: int

    def __str__(self) -> str:
        return _output_span_element(ansi_to_html(self.line), self.delay)


class CommandResult(BaseModel):
    input: LineOutput
    output: Output
    cwd: Path

    def __str__(self) -> str:
        delays = self.output.delays
        input_delay = int(
            (self.output.lines[0].time - self.input.time).total_seconds() * 1000
        )
        input_line = LineWithDelay(
            line=f"$ {self.input.line}", delay=input_delay, time=self.input.time
        )
        output_lines = [
            LineWithDelay(line=line.line, delay=delays[i], time=line.time)
            for i, line in enumerate(self.output.lines)
        ]
        return "\n".join([str(input_line)] + [str(line) for line in output_lines])


def _output_span_element(content: str, delay: int = 0) -> str:
    return f'<span data-ty data-ty-delay="{delay}">{content}</span>'

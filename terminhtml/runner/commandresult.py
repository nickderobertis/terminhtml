from pathlib import Path
from typing import Optional, Dict

from pydantic import BaseModel

from terminhtml.ansi_converter import ansi_to_html, strip_all_ansi
from terminhtml.output import Output, LineOutput, LineEnding


class LineWithDelay(LineOutput):
    delay: int

    def __str__(self) -> str:
        if self.prompt_output:
            line = self.prompt_output.user_input
        else:
            line = self.line
        return _output_span_element(
            ansi_to_html(line),
            self.delay,
            # TODO: enable ANSI formatting for prompts
            #  Right now we are just stripping ANSI formatting from prompts, as the prompt gets stored in
            #  a data attribute of the <span> element. terminhtmljs will need to be updated to support
            #  a way of providing an HTML structure for prompts.
            strip_all_ansi(self.prompt_output.prompt) if self.prompt_output else None,
            line_ending=self.line_ending,
        )


class RunnerContext(BaseModel):
    cwd: Path
    env: Optional[Dict[str, str]] = None


class CommandResult(BaseModel):
    input: LineOutput
    output: Output
    context: RunnerContext

    def __str__(self) -> str:
        delays = self.output.delays
        input_delay = int(
            (self.output.lines[0].time - self.input.time).total_seconds() * 1000
        )
        input_line = LineWithDelay(
            line=f"$ {self.input.line}",
            delay=input_delay,
            time=self.input.time,
            line_ending=self.input.line_ending,
            prompt_output=self.input.prompt_output,
        )
        output_lines = [
            LineWithDelay(
                line=line.line,
                delay=delays[i],
                time=line.time,
                line_ending=line.line_ending,
                prompt_output=line.prompt_output,
            )
            for i, line in enumerate(self.output.lines)
        ]
        return "\n".join([str(input_line)] + [str(line) for line in output_lines])


def _output_span_element(
    content: str,
    delay: int = 0,
    prompt: Optional[str] = None,
    line_ending: LineEnding = LineEnding.CRLF,
) -> str:
    prompt_attr = ""
    if prompt:
        prompt_attr = f'="input" data-ty-prompt="{prompt}"'
    line_ending_attr = ""
    if line_ending == LineEnding.CR:
        line_ending_attr = 'data-ty-carriageReturn="true"'
    return f'<span data-ty{prompt_attr} {line_ending_attr} data-ty-delay="{delay}">{content}</span>'

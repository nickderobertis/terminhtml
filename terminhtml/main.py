from typing import Sequence, Optional, List, Union

from pydantic import BaseModel
from lxml import html

from terminhtml.ansi_converter import ansi_to_html, ansi_styles
from terminhtml.runner.commandresult import CommandResult
from terminhtml.runner.main import run_commands_in_temp_dir

TERMINHTML_BOOTSTRAP_SCRIPT_URL = (
    "https://unpkg.com/@terminhtml/bootstrap@1.x/dist/@terminhtml-bootstrap.umd.js"
)
ANSI2HTML_CSS_URL = "https://unpkg.com/terminhtml@1.x/dist/src/ansi2html.css"


class CommandResults(BaseModel):
    results: List[CommandResult]

    def __str__(self) -> str:
        return "\n".join(str(result) for result in self.results)


class TerminHTML(BaseModel):
    command_results: CommandResults

    @classmethod
    def from_commands(
        cls,
        commands: Sequence[str],
        setup_commands: Optional[List[str]] = None,
        input: Optional[Union[List[str], str]] = None,
        allow_exceptions: bool = False,
        prompt_matchers: Optional[List[str]] = None,
        command_timeout: int = 10,
    ) -> "TerminHTML":
        """
        Create a TerminHTML object from a list of commands.

        :param commands: A list of commands to run.
        :param setup_command: A command to run before the commands, the output of these commands will not show.
        :param input: A list of strings to send to the commands. The input element will be matched with the
            command by index. If a single string is passed, it will be converted into a single-element list so
            that it will be passed to the first command.
        :param allow_exceptions: If True, exceptions will be raised.
        :param prompt_matchers: A list of regex strings to match the prompt of the command. If a prompt is matched,
            it will be provided the matched input.
        :param command_timeout: The timeout in seconds for each command. If a command times out, the process will fail.
        :return: A TerminHTML object.
        """
        setup_command = " && ".join(setup_commands or [])
        command_results = _run_commands_create_command_results(
            commands,
            setup_command,
            input,
            allow_exceptions,
            prompt_matchers=prompt_matchers,
            command_timeout=command_timeout,
        )
        return cls(command_results=CommandResults(results=command_results))

    @property
    def styles(self) -> str:
        return ansi_styles()

    @property
    def styles_link(self) -> str:
        return f"<link rel='stylesheet' href='{ANSI2HTML_CSS_URL}'>"

    def get_styles_for_inline_html(self, inline_css: bool = False) -> str:
        if inline_css:
            return f"<style>{self.styles}</style>"
        return self.styles_link

    def to_html(self, full: bool = True, inline_css: bool = False) -> str:
        """
        Convert the TerminHTML object to HTML.

        :param full: If True, the HTML will be a full standalone page. If False, the HTML will be just the terminal part.
        :param inline_css: If True, the CSS will be included inline. If False, the CSS will be linked to a stylesheet.
            Note that if full is False, this parameter is ignored.
        :return: The HTML string.
        """
        main_html = str(self.command_results)
        styles = self.get_styles_for_inline_html(inline_css=inline_css)
        if not full:
            return f"""
<pre class="terminhtml">
    {main_html}
</pre>
        """.strip()
        full_html = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <script src='{TERMINHTML_BOOTSTRAP_SCRIPT_URL}'></script>
        {styles}
        <title></title>
    </head>
    <body>
        <pre class="terminhtml">
            {main_html}
        </pre>
    </body>
</html>
        """.strip()
        return full_html

    def __str__(self) -> str:
        return self.to_html()


def _run_commands_create_command_results(
    commands: Sequence[str],
    setup_command: Optional[str] = None,
    input: Optional[Union[List[str], str]] = None,
    allow_exceptions: bool = False,
    prompt_matchers: Optional[List[str]] = None,
    command_timeout: int = 10,
) -> List[CommandResult]:
    full_setup_command = setup_command or ""
    use_input = _get_input_list(input)
    return run_commands_in_temp_dir(
        commands,
        full_setup_command,
        use_input,
        allow_exceptions,
        prompt_matchers=prompt_matchers,
        command_timeout=command_timeout,
    )


def _get_input_list(input: Optional[Union[List[str], str]]) -> List[str]:
    if input is None:
        return []
    if isinstance(input, str):
        return [input]
    return input

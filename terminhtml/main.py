from typing import Sequence, Optional, List, Union

from pydantic import BaseModel
from lxml import html

from terminhtml.ansi_converter import ansi_to_html
from terminhtml.runner.commandresult import CommandResult
from terminhtml.runner.main import run_commands_in_temp_dir

TERMINHTML_BOOTSTRAP_SCRIPT_URL = "https://unpkg.com/@terminhtml/bootstrap@1.0.0-alpha.4/dist/@terminhtml-bootstrap.umd.js"


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
        setup_command: Optional[str] = None,
        input: Optional[Union[List[str], str]] = None,
        allow_exceptions: bool = False,
    ) -> "TerminHTML":
        """
        Create a TerminHTML object from a list of commands.

        :param commands: A list of commands to run.
        :param setup_command: A command to run before the commands, the output of these commands will not show.
        :param input: A list of strings to send to the commands. The input element will be matched with the
            command by index. If a single string is passed, it will be converted into a single-element list so
            that it will be passed to the first command.
        :param allow_exceptions: If True, exceptions will be raised.
        :return: A TerminHTML object.
        """
        command_results = _run_commands_create_command_results(
            commands, setup_command, input, allow_exceptions
        )
        return cls(command_results=CommandResults(results=command_results))

    def to_html(self) -> str:
        """
        Convert the TerminHTML object to HTML.

        :return: The HTML string.
        """
        base_html = ansi_to_html(str(self.command_results))
        # Use lxml to insert the TerminHTML bootstrap script tag into the HTML head section.
        tree = html.fromstring(base_html)
        head = tree.find("head")
        script_tag = html.fragment_fromstring(
            f"<script src='{TERMINHTML_BOOTSTRAP_SCRIPT_URL}'></script>"
        )
        head.insert(0, script_tag)
        # Replace the ansi2html-content class with the terminhtml class with lxml
        for element in tree.findall(".//*[@class='ansi2html-content']"):
            element.attrib["class"] = "terminhtml"
        # Remove all classes from the body element
        body = tree.find("body")
        body.attrib.clear()
        # Add a meta tag for utf-8 encoding
        meta_tag = html.fragment_fromstring("<meta charset='utf-8'>")
        head.insert(0, meta_tag)
        final_html = html.tostring(tree, encoding="unicode")
        return final_html

    def __str__(self) -> str:
        return self.to_html()


def _run_commands_create_command_results(
    commands: Sequence[str],
    setup_command: Optional[str] = None,
    input: Optional[Union[List[str], str]] = None,
    allow_exceptions: bool = False,
) -> List[CommandResult]:
    full_setup_command = setup_command or ""
    use_input = _get_input_list(input)
    return run_commands_in_temp_dir(
        commands, full_setup_command, use_input, allow_exceptions
    )


def _get_input_list(input: Optional[Union[List[str], str]]) -> List[str]:
    if input is None:
        return []
    if isinstance(input, str):
        return [input]
    return input

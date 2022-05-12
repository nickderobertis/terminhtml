from pathlib import Path
from typing import Sequence, List, Optional, Union

import typer

from terminhtml.main import TerminHTML

app = typer.Typer()


@app.command(name="terminhtml")
def run_commands_create_html(
    commands: List[str] = typer.Argument(..., help="Commands to run"),
    setup_commands: Optional[List[str]] = typer.Option(
        None,
        "--setup",
        "-s",
        help="Setup commands that are run before the animated session: the IO from "
        "these commands are not displayed but can be used to set up the session "
        "in a particular state before the animation.",
        show_default=False,
    ),
    input: Optional[List[str]] = typer.Option(
        None,
        "--input",
        "-i",
        help="Input to be passed to the commands. Input is to be passed as a list that "
        "will be matched up to commands in order. If you need to provide multiple "
        "inputs to one command, separate them by \\n within the same input item. "
        "Note that you must use prompt matchers for input to do anything.",
        show_default=False,
    ),
    allow_exceptions: bool = typer.Option(
        False,
        "--allow-exceptions",
        "-a",
        help="Allow exceptions from passed commands, still generate html",
        show_default=False,
    ),
    prompt_matchers: Optional[List[str]] = typer.Option(
        None,
        "--prompt-matchers",
        "-m",
        help="Regex patterns to match prompts. When prompts are matched, they will "
        "be provided the passed input.",
        show_default=False,
    ),
    command_timeout: int = typer.Option(
        10, "-t", "--timeout", help="Timeout in seconds for each command."
    ),
    cwd: Optional[Path] = typer.Option(
        None,
        "--cwd",
        "-c",
        help="Working directory to run commands in. "
        "If not passed, defaults to a temporary directory.",
    ),
    out_path: Optional[Path] = typer.Option(
        None,
        "-o",
        "--out",
        help="Output path, defaults to printing to stdout",
        show_default=False,
    ),
    partial_html: bool = typer.Option(
        False,
        "-p",
        "--partial",
        help="Whether to output HTML for only the the commands themselves, "
        "defaults to full HTML including JS/CSS/full page structure",
        show_default=False,
    ),
    inline_css: bool = typer.Option(
        False,
        "-i",
        "--inline-css",
        help="Whether to inline CSS in the HTML, defaults to using a link tag "
        "to reference the stylesheet. Note that this option is ignored "
        "if --partial is set.",
        show_default=False,
    ),
    echo: bool = typer.Option(
        False,
        "--echo",
        "-e",
        help="Echo the commands to stdout",
        show_default=False,
    ),
) -> None:
    """
    Create an animated HTML/CSS terminal by running commands and recording their output.

    Examples:
    ```
    # Run two commands
    $ terminhtml "echo woo > something.txt" "cat something.txt"

    # Output results to a file
    $ terminhtml -o output.html "echo woo"

    # Run a script my-script.sh
    $ terminhtml "$(<my-script.sh)"

    # Run setup commands before the animated session
    $ terminhtml "cat woo.txt" -s "echo a > woo.txt && echo b >> woo.txt"

    # Output partial HTML
    $ terminhtml -p "echo woo"

    # Allow longer-running commands
    $ terminhtml -t 20 "sleep 15 && echo woo"

    # Animate commands that prompt for user input
    $ terminhtml -m "] " -i "woo" "read -p '[value?] ' varname && echo \$varname"

    # Run commands in a specific directory rather than a temporary directory
    $ terminhtml -c .. "ls -l"

    # Echo the commands to stdout
    $ terminhtml -e "echo foo"
    ```
    """
    # In the CLI only, support passing multiple commands separated by newlines
    all_commands: List[str] = []
    for command in commands:
        all_commands.extend(command.split("\n"))

    term = TerminHTML.from_commands(
        all_commands,
        setup_commands,
        input,
        allow_exceptions,
        prompt_matchers,
        command_timeout,
        cwd,
        echo,
    )
    html = term.to_html(full=not partial_html, inline_css=inline_css)
    if out_path is not None:
        out_path.write_text(html)
    else:
        print(html)


def main() -> None:
    typer.run(run_commands_create_html)


if __name__ == "__main__":
    # For some reason this is the required setup for docs generation to work.
    # main() is the actual CLI entrypoint. Access it through __main__.
    typer.run(app)

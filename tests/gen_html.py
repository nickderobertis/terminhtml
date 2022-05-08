from terminhtml.main import TerminHTML
from tests.config import (
    RICH_HTML,
    FXT_INIT_FROM_HTML,
    FXT_ADD_OUTPUT_HTML,
    BASIC_HTML,
    FXT_UPDATE_HTML,
    FXT_INIT_HTML, RICH_PROGRESS_BAR_HTML,
)


def create_basic_html() -> str:
    commands = [
        "echo yeah > woo.txt",
        "ls -l",
        "cat woo.txt",
    ]
    term = TerminHTML.from_commands(commands)
    return str(term)


def create_rich_html() -> str:
    commands = ["python -m rich"]
    term = TerminHTML.from_commands(commands)
    return str(term)


def create_rich_progress_bar_html() -> str:
    commands = ["python -m rich.progress_bar"]
    term = TerminHTML.from_commands(commands)
    return str(term)


def create_fxt_init_from_html() -> str:
    commands = [
        "fxt init-from -n https://github.com/nickderobertis/copier-typescript-npm-sphinx"
    ]
    term = TerminHTML.from_commands(commands)
    return str(term)


def create_fxt_init_html() -> str:
    setup_commands = [
        "git init",
        "touch woo.txt",
        "git add .",
        "git commit -m 'Initial commit'",
    ]
    commands = [
        "fxt init",
    ]
    prompt_matchers = ["]: ", r"0m: "]
    term = TerminHTML.from_commands(
        commands, setup_commands, None, prompt_matchers=prompt_matchers
    )
    return str(term)


def create_fxt_add_output_html() -> str:
    setup_commands = [
        "git init",
        "touch woo.txt",
        "git add .",
        "git commit -m 'Initial commit'",
        "fxt init",
    ]
    commands = [
        "fxt add source https://github.com/nickderobertis/copier-simple-example",
        "fxt add output copier-simple-example",
    ]
    input = [
        None,
        "my answer\n10",
    ]
    prompt_matchers = ["]: ", r"0m: "]
    term = TerminHTML.from_commands(
        commands, setup_commands, input, prompt_matchers=prompt_matchers
    )
    return str(term)


def create_fxt_update_html() -> str:
    setup_commands = [
        "git init",
        "touch woo.txt",
        "git add .",
        "git commit -m 'Initial commit'",
        "fxt init-from https://github.com/nickderobertis/copier-simple-example --no-input --version c7e1ba1bfb141e9c577e7c21ee4a5d3ae5dde04d --folder-name my-project && cd my-project && fxt config target copier-simple-example",
    ]
    commands = [
        "cat answer1.txt",
        "fxt update",
        "cat answer1.txt",
    ]
    input = [
        None,
        "\n50",
    ]
    prompt_matchers = ["]: ", r"0m: "]
    term = TerminHTML.from_commands(
        commands, setup_commands, input, prompt_matchers=prompt_matchers
    )
    return str(term)


if __name__ == "__main__":
    BASIC_HTML.write_text(create_basic_html())
    RICH_HTML.write_text(create_rich_html())
    RICH_PROGRESS_BAR_HTML.write_text(create_rich_progress_bar_html())
    FXT_INIT_FROM_HTML.write_text(create_fxt_init_from_html())
    FXT_INIT_HTML.write_text(create_fxt_init_html())
    FXT_ADD_OUTPUT_HTML.write_text(create_fxt_add_output_html())
    FXT_UPDATE_HTML.write_text(create_fxt_update_html())

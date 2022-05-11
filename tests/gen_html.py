from pathlib import Path

from terminhtml.main import TerminHTML
from tests.config import (
    RICH_HTML,
    FXT_INIT_FROM_HTML,
    FXT_ADD_OUTPUT_HTML,
    BASIC_HTML,
    FXT_UPDATE_HTML,
    FXT_INIT_HTML,
    RICH_PROGRESS_BAR_HTML,
    BASIC_INPUT_HTML,
    ENVIRONMENT_SHARING_HTML,
    BASIC_SETUP_COMMAND_HTML,
    INPUT_FILES_DIR,
    BASIC_CWD_HTML,
)


def create_basic_html() -> str:
    commands = [
        "echo yeah > woo.txt",
        "ls -l",
        "cat woo.txt",
    ]
    term = TerminHTML.from_commands(commands)
    return str(term)


def create_basic_input_html() -> str:
    commands = [
        "read -p '[value?] ' varname && echo $varname",
    ]
    prompt_matchers = ["] "]
    input = ["woo"]
    term = TerminHTML.from_commands(
        commands, input=input, prompt_matchers=prompt_matchers
    )
    return str(term)


def create_basic_setup_command_html() -> str:
    setup_commands = [
        "echo hello > woo.txt",
    ]
    commands = [
        "cat woo.txt",
    ]
    term = TerminHTML.from_commands(commands, setup_commands=setup_commands)
    return str(term)


def create_basic_cwd_html() -> str:
    commands = [
        "ls -l",
    ]
    cwd = INPUT_FILES_DIR
    term = TerminHTML.from_commands(commands, cwd=cwd)
    return str(term)


def create_environment_sharing_html() -> str:
    setup_commands = [
        "my_var=123",
        "export my_exported_var=e123",
    ]
    commands = [
        "echo $my_var should be 123",
        "echo $my_exported_var should be e123",
        "second_var=456",
        "echo $second_var should be 456",
    ]
    term = TerminHTML.from_commands(commands, setup_commands=setup_commands)
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
    BASIC_INPUT_HTML.write_text(create_basic_input_html())
    BASIC_SETUP_COMMAND_HTML.write_text(create_basic_setup_command_html())
    BASIC_CWD_HTML.write_text(create_basic_cwd_html())
    ENVIRONMENT_SHARING_HTML.write_text(create_environment_sharing_html())
    RICH_HTML.write_text(create_rich_html())
    RICH_PROGRESS_BAR_HTML.write_text(create_rich_progress_bar_html())
    FXT_INIT_FROM_HTML.write_text(create_fxt_init_from_html())
    FXT_INIT_HTML.write_text(create_fxt_init_html())
    FXT_ADD_OUTPUT_HTML.write_text(create_fxt_add_output_html())
    FXT_UPDATE_HTML.write_text(create_fxt_update_html())

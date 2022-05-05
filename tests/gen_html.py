from terminhtml.main import TerminHTML
from tests.config import RICH_HTML, FXT_INIT_FROM_HTML, FXT_ADD_OUTPUT_HTML


def create_rich_html() -> str:
    commands = ["python -m rich"]
    term = TerminHTML.from_commands(commands)
    return str(term)


def create_fxt_init_from_html() -> str:
    commands = [
        "fxt init-from -n https://github.com/nickderobertis/copier-typescript-npm-sphinx"
    ]
    term = TerminHTML.from_commands(commands)
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


if __name__ == "__main__":
    RICH_HTML.write_text(create_rich_html())
    FXT_INIT_FROM_HTML.write_text(create_fxt_init_from_html())
    FXT_ADD_OUTPUT_HTML.write_text(create_fxt_add_output_html())

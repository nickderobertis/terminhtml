from terminhtml.main import TerminHTML
from tests.config import RICH_HTML, FXT_INIT_FROM_HTML


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


if __name__ == "__main__":
    RICH_HTML.write_text(create_rich_html())
    FXT_INIT_FROM_HTML.write_text(create_fxt_init_from_html())

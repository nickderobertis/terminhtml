from terminhtml.main import TerminHTML
from tests.config import RICH_HTML


def create_rich_html() -> str:
    commands = ["python -m rich"]
    term = TerminHTML.from_commands(commands)
    return str(term)


if __name__ == "__main__":
    RICH_HTML.write_text(create_rich_html())

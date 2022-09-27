import pytest

from tests.config import INPUT_FILES_DIR
from tests.dirutils import change_directory_to
from tests.e2e.cli_stub import run_cli


@pytest.mark.parametrize(
    "flag",
    ["-d", "--cwd"],
)
def test_command_runs_in_absolute_cwd_when_passed(flag: str):
    cwd = INPUT_FILES_DIR
    result = run_cli(f"{flag} {cwd.absolute()} 'ls -l'")
    text = result.output
    assert result.exit_code == 0
    assert "rich_progress_bar.html" in text


@pytest.mark.parametrize(
    "flag",
    ["-d", "--cwd"],
)
def test_command_runs_in_current_directory_when_passed_as_dot(flag: str):
    cwd = INPUT_FILES_DIR
    with change_directory_to(cwd):
        result = run_cli(f"{flag} . 'ls -l'")
        text = result.output
        assert result.exit_code == 0
        assert "rich_progress_bar.html" in text

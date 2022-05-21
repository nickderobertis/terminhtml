import pytest
from terminhtml.exc import UserCommandException

from terminhtml.runner.main import run_commands


def test_runner_raises_user_command_exception_when_setup_command_exits_with_error_and_exceptions_not_allowed():
    with pytest.raises(UserCommandException) as excinfo:
        run_commands(
            ["echo woo"],
            setup_command=f"echo content && exit 1",
        )
    assert "Command failed" in str(excinfo.value)
    assert "echo content && exit 1" in str(excinfo.value)
    assert "echo woo" in str(excinfo.value)
    assert "input=None" in str(excinfo.value)
    assert "env=None" in str(excinfo.value)
    assert "cwd=PosixPath" in str(excinfo.value)
    assert "output:\ncontent" in str(excinfo.value)


def test_runner_does_not_raise_exception_when_command_exits_with_error_and_exceptions_allowed():
    run_commands(["echo woo", "exit 1", "echo no"], allow_exceptions=True)

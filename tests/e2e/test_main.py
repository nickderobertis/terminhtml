from tests.e2e.cli_stub import run_cli


def test_cli_creates_html():
    result = run_cli('''"echo 'Hello World'"''')
    assert result.exit_code == 0
    assert "Hello World" in result.output

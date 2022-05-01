from terminhtml.main import TerminHTML


def test_terminhtml_runs_command_creates_unstyled_html():
    commands = [
        "echo yeah > woo.txt",
        "ls -l",
        "cat woo.txt",
    ]
    term = TerminHTML.from_commands(commands)
    html = term.to_html()
    for command in commands[1:]:
        assert command in html
    # Check html encoding
    assert "echo yeah &gt; woo.txt" in html
    # Check output of ls -l
    assert "total 4" in html

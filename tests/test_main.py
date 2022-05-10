from lxml import html

from terminhtml.main import TerminHTML
from tests.gen_html import (
    create_basic_input_html,
    create_rich_progress_bar_html,
    create_basic_setup_command_html,
    create_environment_sharing_html,
)


def test_terminhtml_runs_command_creates_unstyled_html():
    commands = [
        "echo yeah > woo.txt",
        "ls -l",
        "cat woo.txt",
    ]
    term = TerminHTML.from_commands(commands)
    text = term.to_html()
    for command in commands[1:]:
        assert command in text
    # Check html encoding
    assert "echo yeah &gt; woo.txt" in text
    # Check output of ls -l
    assert "total 4" in text
    # Ensure that pwd printing to correct cwd does not make its way into the html
    assert "/tmp/" not in text
    # Check that delay attribute was added and is non-zero for commands
    tree = html.fromstring(text)
    span = tree.xpath("//pre[@class='terminhtml']/span[1]")[0]
    assert span.text == "$ echo yeah > woo.txt"
    assert int(span.attrib["data-ty-delay"]) > 0


def test_terminhtml_creates_input_html():
    text = create_basic_input_html()
    assert "$ read -p '[value?] ' varname &amp;&amp; echo $varname" in text
    # Find second span element inside the pre tag with class "terminhtml" using lxml
    tree = html.fromstring(text)
    span = tree.xpath("//pre[@class='terminhtml']/span[2]")[0]
    assert span.text == "woo"
    # Check thst the span element has the data-ty-prompt attribute
    assert span.attrib["data-ty-prompt"] == "[value?] "


def test_terminhtml_creates_carriage_return_html():
    text = create_rich_progress_bar_html()
    assert "$ python -m rich.progress_bar" in text
    # Find second span element inside the pre tag with class "terminhtml" using lxml
    tree = html.fromstring(text)
    span = tree.xpath("//pre[@class='terminhtml']/span[2]")[0]
    # Check that the span element has both carriage return and delay attributes
    assert span.attrib["data-ty-delay"] == "50"
    assert span.attrib["data-ty-carriagereturn"] == "true"
    # Check that styling is applied to children of the span element
    for child in span.iterchildren():
        # For some reason, it seems that different shells may have different coloring of output
        # When I run this through pycharm's test runner, it applies classes ansi90 and ansi91,
        # but when I run it directly in the terminal it applies ansi38-204 and ansi38-237. The color
        # is slightly visually different, with ansi38-204 and ansi38-237 being the more accurate colors.
        # Until I can figure out why, just check for any of these classes.
        assert child.attrib["class"] in ["ansi38-204", "ansi38-237", "ansi90", "ansi91"]


def test_terminhtml_setup_commands_affect_runtime():
    text = create_basic_setup_command_html()
    assert "$ cat woo.txt" in text
    assert "hello" in text


def test_terminhtml_persists_environment_between_commands():
    text = create_environment_sharing_html()
    assert "$ echo $my_var should be 123" in text
    assert "123 should be 123" in text
    assert "$ echo $my_exported_var should be e123" in text
    assert "e123 should be e123" in text
    assert "$ second_var=456" in text
    assert "456 should be 456" in text

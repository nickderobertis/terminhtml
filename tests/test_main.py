from lxml import html

from terminhtml.main import TerminHTML
from tests.config import INPUT_FILES_DIR, PROJECT_DIR
from tests.gen_html import (
    create_basic_cwd_html,
    create_basic_input_html,
    create_basic_setup_command_html,
    create_demo_output_html,
    create_environment_sharing_html,
    create_rich_progress_bar_html,
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
    assert int(span.attrib["data-ty-delay"]) in [49, 50, 51]
    assert span.attrib["data-ty-carriagereturn"] == "true"
    # Check that styling is applied to children of the span element
    for child in span.iterchildren():
        # ansi38-204 and ansi38-237 (8-bit) should always be applied because force_color=True
        assert child.attrib["class"] in ["ansi38-204", "ansi38-237"]


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


def test_terminhtml_includes_style_link_or_full_styles_in_html():
    commands = [
        "echo yeah > woo.txt",
        "ls -l",
        "cat woo.txt",
    ]
    term = TerminHTML.from_commands(commands)
    css_link_html = term.to_html()
    assert "<link" in css_link_html
    assert not "<style" in css_link_html
    inline_css_html = term.to_html(inline_css=True)
    assert not "<link" in inline_css_html
    assert "<style" in inline_css_html


def test_terminhtml_runs_in_cwd_when_passed():
    text = create_basic_cwd_html()
    # Should be ls -l output in the input_files directory
    assert "basic.html" in text
    assert "basic_input.html" in text


def test_terminhtml_runs_in_temp_dir_when_no_cwd_passed():
    term = TerminHTML.from_commands(["ls -l", "pwd"])
    text = term.to_html()
    # Directory should be empty as it is a new temp dir
    assert "total 0" in text
    # Should have /tmp/ in the path
    assert "/tmp/" in text


def test_terminhtml_renders_a_styled_prompt():
    text = create_demo_output_html()
    # Once terminhtml supports styled prompts, this test should be updated
    assert "What is your name? (John Doe): " in text


def test_terminhtml_renders_without_color_with_term_dumb_and_no_force_color():
    commands = [
        "export TERM=dumb",
        "echo $TERM",
        "python -m terminhtml.demo_output",
    ]
    prompt_matchers = ["\\): "]
    input = [None, None, "Nick DeRobertis"]
    cwd = PROJECT_DIR
    term = TerminHTML.from_commands(
        commands,
        cwd=cwd,
        prompt_matchers=prompt_matchers,
        input=input,
        force_color=False,
    )
    text = term.to_html()
    # Should not have any color
    assert "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄" in text
    assert not '<span class="ansi38-124 ansi48-88">▄</span>' in text


def test_terminhtml_renders_with_color_with_term_dumb_and_force_color():
    commands = [
        "export TERM=dumb",
        "echo $TERM",
        "python -m terminhtml.demo_output",
    ]
    prompt_matchers = ["\\[0m: "]
    input = [None, None, "Nick DeRobertis"]
    cwd = PROJECT_DIR
    term = TerminHTML.from_commands(
        commands,
        cwd=cwd,
        prompt_matchers=prompt_matchers,
        input=input,
        force_color=True,
    )
    text = term.to_html()
    # Should have 8-bit color
    assert not "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄" in text
    assert '<span class="ansi38-124 ansi48-88">▄</span>' in text


def test_terminhtml_runs_command_in_cwd_after_pipe():
    commands = [
        "echo '.' | xargs realpath",
    ]
    cwd = INPUT_FILES_DIR
    term = TerminHTML.from_commands(commands, cwd=cwd)
    text = term.to_html()
    for command in commands:
        assert command in text
    assert cwd.name in text


def test_terminhtml_runs_command_with_nested_quotes():
    commands = [
        "echo '\"woo\"'",
    ]
    term = TerminHTML.from_commands(commands)
    text = term.to_html()
    for command in commands:
        assert command in text
    # Check for double quotes in output
    assert '"woo"</span>' in text

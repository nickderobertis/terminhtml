from typing import List

from ansi2html import Ansi2HTMLConverter
from ansi2html.style import get_styles, Rule

conv = Ansi2HTMLConverter()


# TODO: Rework ansi styles to keep only the ones used. See Ansi2HTMLConverter.convert
def ansi_styles() -> str:
    """
    Returns the ansi2html stylesheet, narrowed to what this block of ansi needs.
    """
    all_styles = get_styles(conv.dark_bg, conv.line_wrap, conv.scheme)
    return "\n".join(str(s) for s in all_styles)


def ansi_to_html(ansi: str) -> str:
    """
    Converts an ansi string to html.
    """
    return conv.convert(ansi, full=False)


if __name__ == "__main__":
    # ansi = "\x1b[30mblack\x1b[37mwhite"
    ansi = """
$ fxt init-from Initialized empty Git repository in
/tmp/tmpqlnoliu3/.git/\r\n[main (root-commit) ef680a7] Initial commit\r\n
1 file changed, 0 insertions(+), 0 deletions(-)\r\n create mode 100644
woo.txt\r\n\x1b[?25l Initializing flexlate project with default add mode
local and \x1b[33muser\x1b[0m=\x1b[3;91mFalse\x1b[0m in
\r\n\x1b[35m/tmp/\x1b[0m\x1b[95mtmpqlnoliu3\x1b[0m\r\n\x1b[32m⠋\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠋\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠙\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠹\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠸\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠼\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠦\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠧\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠇\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠏\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠋\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠙\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠹\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠸\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠼\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠴\x1b[0m
Initializing...\r\x1b[2K\x1b[32m⠦\x1b[0m
Initializing...\r\n\x1b[?25h\r\x1b[1A\x1b[2K\x1b[32m✔ Finished
initializing flexlate project\x1b[0m\r\n\x1b[0m\x1b[0m Adding template
source\x1b[33m...\x1b[0m\r\n\x1b[?25l Adding template source
copier-simple-example from
\r\n\x1b[4;94mhttps://github.com/nickderobertis/copier-simple-example\x1b[0m\r\n\x1b[32m⠋\x1b[0m\r\x1b[2K\x1b[32m⠋\x1b[0m\r\x1b[2K\x1b[32m⠹\x1b[0m\r\x1b[2K\x1b[32m⠸\x1b[0m\r\x1b[2K\x1b[32m⠼\x1b[0m\r\x1b[2K\x1b[32m⠴\x1b[0m\r\x1b[2K\x1b[32m⠦\x1b[0m\r\x1b[2K\x1b[32m⠧\x1b[0m\r\x1b[2K\x1b[32m⠇\x1b[0m\r\x1b[2K\x1b[32m⠏\x1b[0m\r\x1b[2K\x1b[32m⠋\x1b[0m\r\x1b[2K\x1b[32m⠙\x1b[0m\r\x1b[2K\x1b[32m⠹\x1b[0m\r\x1b[2K\x1b[32m⠸\x1b[0m\r\x1b[2K\x1b[32m⠼\x1b[0m\r\x1b[2K\x1b[32m⠴\x1b[0m\r\x1b[2K\x1b[32m⠦\x1b[0m\r\x1b[2K\x1b[32m⠧\x1b[0m\r\x1b[2K\x1b[32m⠇\x1b[0m\r\x1b[2K\x1b[32m⠏\x1b[0m\r\x1b[2K
Sucessfully added template source
copier-simple-example\r\n\x1b[32m⠏\x1b[0m\r\x1b[2K\x1b[32m⠏\x1b[0m\r\n\x1b[?25h\r\x1b[1A\x1b[2K\x1b[0m\x1b[0m
Merging flexlate-templates-main to flexlate-templates\r\n\x1b[32m✔
Successfully merged flexlate-templates-main to
flexlate-templates\x1b[0m\r\n\x1b[32m✔ Successfully merged
flexlate-output-main to flexlate-output\x1b[0m\r\n Deleting flexlate
feature branches flexlate-templates-main and
\r\nflexlate-output-main\r\n\x1b[32m✔ Successfully deleted flexlate
feature branches\x1b[0m\r\n\x1b[0m\x1b[0m'
    """.strip()
    html = conv.convert(ansi, full=True)
    styles = ansi_styles(ansi)
    print(html)

from pathlib import Path

TESTS_DIR = Path(__file__).parent
INPUT_FILES_DIR = TESTS_DIR / "input_files"
PROJECT_DIR = TESTS_DIR.parent

BASIC_HTML = INPUT_FILES_DIR / "basic.html"
BASIC_INPUT_HTML = INPUT_FILES_DIR / "basic_input.html"
BASIC_SETUP_COMMAND_HTML = INPUT_FILES_DIR / "basic_setup_command.html"
BASIC_CWD_HTML = INPUT_FILES_DIR / "basic_cwd.html"
DEMO_OUTPUT_HTML = INPUT_FILES_DIR / "demo_output.html"
ENVIRONMENT_SHARING_HTML = INPUT_FILES_DIR / "environment_sharing.html"
RICH_HTML = INPUT_FILES_DIR / "rich.html"
RICH_PROGRESS_BAR_HTML = INPUT_FILES_DIR / "rich_progress_bar.html"
FXT_INIT_FROM_HTML = INPUT_FILES_DIR / "fxt_init_from.html"
FXT_INIT_HTML = INPUT_FILES_DIR / "fxt_init.html"
FXT_ADD_OUTPUT_HTML = INPUT_FILES_DIR / "fxt_add_output.html"
FXT_UPDATE_HTML = INPUT_FILES_DIR / "fxt_update.html"

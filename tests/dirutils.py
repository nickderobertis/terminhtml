import os
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def change_directory_to(path: Path):
    current_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(current_path)

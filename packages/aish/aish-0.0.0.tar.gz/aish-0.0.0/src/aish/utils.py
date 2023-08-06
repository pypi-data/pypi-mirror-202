from pathlib import Path
import subprocess
import tempfile
import os
import sys
import uuid
import click
import functools
from typing import List, Any, Optional, Callable
from .config import CONFIG



def open_editor():
    temp_file = Path(tempfile.gettempdir()) / str(uuid.uuid4())
    temp_file = temp_file.with_suffix(".txt")
    temp_file.touch()

    if "EDITOR" in os.environ:
        editor = os.environ["EDITOR"]
    else:
        editor = CONFIG["general"]["editor"]

    subprocess.run([editor, str(temp_file)], check=True)

    return temp_file.read_text()


class File(click.File):
    """
    Adding extra arguments to the click.File type to support file extension validation
    """
    def __init__(self, *args, exts: List[str], **kwargs):
        self.valid_ext = exts
        super().__init__(*args, **kwargs)

    def convert(self, value: Any, param: Optional["Parameter"], ctx: Optional["Context"]) -> Any:
        file = super().convert(value, param, ctx)
        if self.valid_ext:
            extention = Path(file.name).suffix 
            if extention not in self.valid_ext:
                self.fail(f"{extention} is not a supported file type for this command", param, ctx)
        return file


class Prompt(click.ParamType):
    name = "prompt"
    
    def convert(self, value: str, param, ctx) -> Any:
        file_path = Path(value)
        if file_path.exists() and file_path.is_file():
            value = file_path.read_text()

        if not sys.stdin.isatty():
            value += sys.stdin.read()

        if not value:
            value = open_editor()

        return value


def prompt_arguments(*arg_names, optional=False):
    if not arg_names:
        if not optional:
            arg_names = ["prompt"]
        else:
            arg_names = ["-p", "--prompt"]

    def decorator(function: Callable):
        @click.argument(*arg_names, type=str, default="")
        @click.option("-f", "--file", type=click.File("r"), help="Send contents of file")
        @click.option("-e", "--editor", is_flag=True, help="Opens text editor then use contents")
        @functools.wraps(function)
        def wrapper_common_options(*args, **kwargs):
            return function(*args, **kwargs)

        return wrapper_common_options
    
    return decorator
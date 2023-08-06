import openai
import click
from typing import BinaryIO
from pathlib import Path
import base64
import tempfile
import uuid
import webbrowser
import platform
import os
import functools
from . import utils
from .api_key import load_key
from .config import CONFIG



DEFAULT_NUM = int(CONFIG["image"]["num"])
DEFAULT_SIZE = CONFIG["image"]["size"]
DEFAULT_FORMAT = CONFIG["image"]["format"]

URL_CHOICES = [
    "url",
    "b64_json",
]

SIZE_CHOICES = [
    "1024x1024",
    "512x512",
    "256x256",
]


@click.group("image", help="Image Manipulation")
def image(): 
    """DOCUMENTATION"""
    pass


def image_options(function):
    @click.option("-n", "--num", type=int, default=DEFAULT_NUM, help=f"Number of images to generate. Default is {DEFAULT_NUM}")
    @click.option("-s", "--size", type=click.Choice(SIZE_CHOICES), default=DEFAULT_SIZE, help=f"Image size. Default is {DEFAULT_SIZE}")
    @click.option("-fmt", "--format", type=click.Choice(URL_CHOICES), default=DEFAULT_FORMAT, help=f"Format of returned images. Default is {DEFAULT_FORMAT}")
    @click.option("-p", "--print", "print_response", is_flag=True, help="Output response to terminal instead of opening")
    @functools.wraps(function)
    def wrapper_common_options(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper_common_options


@image.command(help="Image generation")
@click.argument("prompt", type=utils.Prompt(), default="")
@image_options
def create(
    prompt: str,
    num: int,
    size: str,
    format: str,
    print_response: bool
):
    """DOCUMENTATION"""

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=num,
            size=size,
            response_format=format,
        )
    except openai.OpenAIError as e:
        ## TODO
        # Add more informative error messages & logging
        print(f"Error: {e}")
    else:
        display_image_response(response, format, print_response)


@image.command(help="Image generation")
@click.argument("image", type=utils.File("rb", exts=[".png"]))
@click.argument("mask", type=utils.File("rb", exts=[".png"]))
@click.argument("prompt", type=utils.Prompt(), default="")
@image_options
def edit(
    image: BinaryIO,
    mask: BinaryIO,
    prompt: str,
    num: int,
    size: str,
    format: str,
    print_response: bool
):
    """DOCUMENTATION"""

    try:
        response = openai.Image.create_edit(
            image=image,
            mask=mask,
            prompt=prompt,
            n=num,
            size=size,
            response_format=format,
        )
    except openai.OpenAIError as e:
        print(f"Error: {e}")
    else:
        display_image_response(response, format, print_response)


@image.command(help="Create a variation of an image")
@click.argument("image", type=utils.File("rb", exts=[".png"]))
@image_options
def variation(
    image: BinaryIO,
    num: int,
    size: str,
    format: str,
    print_response: bool,
):
    """DOCUMENTATION"""
    input_image = image.read()

    try:
        response = openai.Image.create_variation(
            image=input_image,
            n=num,
            size=size,
            response_format=format,
        )
    except openai.OpenAIError as e:
        ## TODO
        # Add more informative error messages & logging
        print(f"Error: {e}")
    else:
        display_image_response(response, format, print_response)


def display_image_response(response, format, print_response):
    for index, generation in enumerate(response['data']):
        if format == "url":
            image = generation[format]
        elif format == "b64_json":
            b64_encoded_data = generation[format]
            decoded_image = base64.b64decode(b64_encoded_data)
            temp_file = Path(tempfile.gettempdir()) / str(uuid.uuid4())
            temp_file = temp_file.with_suffix(".png")
            temp_file.write_bytes(decoded_image)
            image = temp_file
            
        if print_response is True:
            print(f"Image {index}:")
            print(image)
        else:
            if format == "url":
                webbrowser.open(image)
            elif format == "b64_json":
                if platform.system() == 'Darwin':
                    # subprocess.call(('open', filepath))
                    raise NotImplementedError
                elif platform.system() == 'Windows':
                    os.startfile(image)
                else:
                    # subprocess.call(('xdg-open', filepath))
                    raise NotImplementedError

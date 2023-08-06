import click
import openai
import functools
from typing import BinaryIO
from . import utils
from .api_key import load_key
from .config import CONFIG



DEFAULT_AUDIO_MODEL = CONFIG["audio"]["model"]
DEFAULT_AUDIO_TEMPERATURE = int(CONFIG["audio"]["temperature"])
DEFAULT_AUDIO_RESPONSE_FORMAT = CONFIG["audio"]["format"]
DEFAULT_AUDIO_LANGUAGE = CONFIG["audio"]["language"]

RESPONSE_FORMAT_CHOICES = [
    "json",
    "text",
    "srt",
    "verbose_json",
    "vtt",
]

FILE_FORMAT_CHOICES = [
    "mp3",
    "mp4",
    "mpeg",
    "mpga",
    "m4a",
    "wav",
    "webm",
]


@click.group(help="Speech to text")
def audio(): pass


def audio_options():
    def decorator(function):
        @click.argument("audio", type=utils.File("rb", exts=[".mp3",".mp4",".mpeg",".m4a",".wav",".webm",]))
        @click.option("-p", "--prompt", type=utils.Prompt())
        @click.option("-m", "--model", type=str, default=DEFAULT_AUDIO_MODEL, help=f"Model selection. Default is '{DEFAULT_AUDIO_MODEL}'.")
        @click.option("-t", "--temp", type=float, default=DEFAULT_AUDIO_TEMPERATURE, help=f"Sampling temperature selection. Default is {DEFAULT_AUDIO_TEMPERATURE}")
        @click.option("-fmt", "--format", type=click.Choice(RESPONSE_FORMAT_CHOICES), default=DEFAULT_AUDIO_RESPONSE_FORMAT, help=f"The format of the transcript output. Default is {DEFAULT_AUDIO_RESPONSE_FORMAT}")
        @functools.wraps(function)
        def wrapper_common_options(*args, **kwargs):
            return function(*args, **kwargs)

        return wrapper_common_options
    return decorator


@audio.command(help="Transcribes audio into the input language")
@audio_options()
@click.option("-l", "--lang", type=str, default=DEFAULT_AUDIO_LANGUAGE, help=f"Language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency. Default is '{DEFAULT_AUDIO_LANGUAGE}'.")
def transcribe(
    audio: BinaryIO,
    prompt: str,
    model: str,
    temp: float,
    format: str,
    lang: str,
):
    """DOCUMENTATION"""
    
    try:
        response = openai.Audio.translate(
            model=model,
            file=audio,
            temperature=temp,
            format=format,
            prompt=prompt,
            language=lang,
        )
    except openai.OpenAIError as e:
        ## TODO
        # Add more informative error messages & logging
        print(f"{e.__class__.__name__}: {e}")
    else:
        print(response["text"])


@audio.command(help="Translate audio into English")
@audio_options()
def translate(
    audio: BinaryIO,
    prompt: str,
    model: str,
    temp: float,
    format: str,
):
    """DOCUMENTATION"""
    
    try:
        response = openai.Audio.translate(
            model=model,
            file=audio,
            temperature=temp,
            format=format,
            prompt=prompt,
        )
    except openai.OpenAIError as e:
        ## TODO
        # Add more informative error messages & logging
        print(f"{e.__class__.__name__}: {e}")
    else:
        print(response["text"])

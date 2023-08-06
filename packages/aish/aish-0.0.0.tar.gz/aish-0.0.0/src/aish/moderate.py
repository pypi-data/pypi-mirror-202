import click
import openai
from . import utils
from .api_key import load_key
from .config import CONFIG



DEFAULT_CHAT_MODEL = CONFIG["moderation"]["model"]

@click.command(help="Check if text violates OpenAI's Content Policy")
@click.argument("input", type=utils.Prompt(), default="")
@click.option("-m", "--model", type=str, default=DEFAULT_CHAT_MODEL, help=f"Model selection. Default is {DEFAULT_CHAT_MODEL}.")
def moderate(input: str, model: str):
    try:
        response = openai.Moderation.create(
            input=input,
            model=model,
        )
    except openai.OpenAIError as e:
        print(f"Error: {e}")
    else:
        print(response)

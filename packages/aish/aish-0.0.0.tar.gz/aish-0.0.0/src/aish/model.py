import openai
import click
from .api_key import load_key



@click.group("model", help="Get information about available models")
def model():
    """DOCUMENTATION"""
    pass


@model.command(help="List available models")
def list():
    """DOCUMENTATION"""
    try:
        model_list = openai.Model.list()["data"]
    except openai.OpenAIError as e:
        print(f"Error: {e}")
    else:
        print("Available Models:")
        model_names = [model["id"] for model in model_list]
        for name in sorted(model_names):
            print(f"{name}")


@model.command(help="Get information about a model")
@click.argument("model_name", type=str)
def show(model_name: str):
    """DOCUMENTATION"""
    try:
        model_list = openai.Model.list()["data"]
    except openai.OpenAIError as e:
        print(f"Error: {e}")
    else:
        model_info = {}
        for model in model_list:
            if model["id"] == model_name:
                model_info = model

        print(model_info)




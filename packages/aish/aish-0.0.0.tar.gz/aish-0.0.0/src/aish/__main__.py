import click
import openai
from .api_key import save_key, load_key
from .text import chat, edit, complete
from .config import config
from .image import image
from .model import model
from .moderate import moderate
from .file import file
from .audio import audio


@click.group(invoke_without_command=True)
@click.option("--key", "new_key", is_flag=True, help="Show prompt to save an API key")
def main(new_key: bool):
    """DOCUMENTATION"""
    
    key = load_key()
    if new_key or not key:
        key = input("Please enter your API key\nTo generate an API key, see:\nhttps://platform.openai.com/account/api-keys\n:")
        print()
        save_key(key)

    openai.api_key = key


main.add_command(chat)
main.add_command(edit)
main.add_command(complete)
main.add_command(config)
main.add_command(image)
main.add_command(model)
main.add_command(moderate)
main.add_command(file)
main.add_command(audio)


if __name__ == "__main__":
    main()
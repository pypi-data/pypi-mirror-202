# gpt_chat_cli.py
import json
import sys
from pathlib import Path

import typer
from rich.logging import RichHandler
from rich.traceback import install

from .gpt_chat_model import GPTChatSession
from .gpt_chat_to_md import gpt_chat_session_to_md

install()
app = typer.Typer()


@app.command()
def convert(
    input_json: Path = typer.Argument(..., help="Path to the input JSON file"),
    output_md: Path = typer.Argument(..., help="Path to the output Markdown file"),
):
    """Convert a GPTChatSession JSON file to a Markdown representation."""
    # Configure the Rich logging handler
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    log = logging.getLogger("rich")

    # Read input JSON file
    try:
        with input_json.open() as f:
            chat_session_json = json.load(f)
    except Exception as e:
        log.error(f"Error reading input file: {e}")
        sys.exit(1)

    # Parse JSON to GPTChatSession instance
    try:
        chat_session = GPTChatSession.parse_obj(chat_session_json)
    except Exception as e:
        log.error(f"Error parsing GPTChatSession: {e}")
        sys.exit(1)

    # Convert GPTChatSession to Markdown
    markdown_output = gpt_chat_session_to_md(chat_session)

    # Write Markdown output to file
    try:
        with output_md.open("w") as f:
            f.write(markdown_output)
        log.info(f"Converted chat session saved to: {output_md}")
    except Exception as e:
        log.error(f"Error writing output file: {e}")
        sys.exit(1)


def main():
    app()


if __name__ == "__main__":
    main()

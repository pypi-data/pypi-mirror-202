# gpt_chat_to_md.py
from datetime import datetime

from .gpt_chat_model import GPTChatSession

from datetime import datetime


def gpt_chat_session_to_md(chat_session: GPTChatSession) -> str:
    md_output = []

    nodes_to_process = sorted(
        [node for node in chat_session.mapping.values() if node.message is not None],
        key=lambda node: node.message.create_time,
    )

    previous_user_output = ""
    for node in nodes_to_process:
        message = node.message

        if message.author.role == "assistant":
            if "interrupted" in message.metadata:
                previous_user_output = ""  # Discard the previous user message
                continue  # Skip interrupted assistant message
            else:
                # Append the previous user message
                md_output.append(previous_user_output)
                previous_user_output = ""  # Reset the previous user message

                # Format timestamp
                formatted_timestamp = datetime.fromtimestamp(
                    message.create_time
                ).strftime("%Y-%m-%d %H:%M:%S")

                # Apply block quote formatting to all lines of the assistant message
                block_quoted_content = "> " + "\n> ".join(
                    message.content.parts[0].splitlines()
                )

                md_output.append(
                    f"_**{formatted_timestamp} - Assistant:**_\n\n{block_quoted_content}\n\n---\n\n"
                )

        elif message.author.role == "user":
            # Format timestamp
            formatted_timestamp = datetime.fromtimestamp(message.create_time).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            previous_user_output = (
                f"**{formatted_timestamp} - User:**\n\n{message.content.parts[0]}\n\n"
            )

    return "".join(md_output)

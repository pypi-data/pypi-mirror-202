# ChatterMark 💬📝✨

Chattermark is a CLI tool that converts GPT chat sessions to a Markdown format, making it easier for you to read, share, or archive your chat sessions. It parses JSON data extracted from a GPT chat session and generates a neat and well-formatted Markdown file.

## Installation

```bash
pip install chattermark
```

## Usage

```bash
chattermark input.json output.md
```

### Input

Your input should be a JSON file containing a chat session with a GPT model. The JSON structure should match the `GPTChatSession` Pydantic model in the code.

### Output

Chattermark will generate a Markdown file with a chronological and easy-to-read representation of the chat session. The output will show user and assistant messages, along with timestamps.

## Example

Suppose you have the following JSON data in a file called `input.json`:

```json
{
    "title": "dev(python/chattermark): convert chat GPT sessions to markdown",
    "create_time": 1681444192.748429,
    "update_time": 1681446704.0,
    "mapping": {
        ...
    }
}
```

Run Chattermark:

```bash
chattermark input.json output.md
```

The generated `output.md` will look like this:

```
**2023-04-13 15:30:52 - User:**

Please define a pydantic model for a json representation of a chat GPT session as extracted from a Chrome browser session using the developer tools.

_**2023-04-13 15:31:53 - Assistant:**_

> To create a Pydantic model for a JSON representation of a chat GPT session extracted from a Chrome browser session using the developer tools, you'll first need to identify the data structure and fields in the JSON. ...

---

...
```

## Converting Markdown to Other Formats

Chattermark generates a Markdown output, which is a versatile and widely supported format. However, you might want to convert the Markdown output to other formats like Word documents, HTML, or PDF. To do this, you can use a tool called [Pandoc](https://pandoc.org/).

1. Install Pandoc following the [official installation guide](https://pandoc.org/installing.html).
2. Run Pandoc to convert the Markdown file to your desired format. For example:

   - To convert the Markdown file to an HTML file:

     ```bash
     pandoc output.md -o output.html
     ```

   - To convert the Markdown file to a Word document:

     ```bash
     pandoc output.md -o output.docx
     ```

   - To convert the Markdown file to a PDF file:

     ```bash
     pandoc output.md -o output.pdf
     ```

Check the [Pandoc User's Guide](https://pandoc.org/MANUAL.html) for more information on available output formats and options.

## License

ChatterMark is released under the [MIT License](https://opensource.org/licenses/MIT).

## Credits

ChatterMark was created by an enthusiastic team of an AI and a developer ~~developers~~ who believe that fun and productivity can go hand in hand! We hope you enjoy using ChatterMark as much as we enjoyed creating it.

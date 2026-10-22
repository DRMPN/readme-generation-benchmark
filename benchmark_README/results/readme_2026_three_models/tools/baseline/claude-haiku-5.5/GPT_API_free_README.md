# Zotero GPT

## Overview

This repository contains a small Python demo that calls a GPT chat model through the OpenAI Python client. The included `demo.py` shows how to send a conversation to the chat completions API and print the reply, either all at once or as a stream.

The repository's image files are named `zotero-gpt.png`, `zotero7-gpt1.png`, `zotero7-gpt2.png`, and `zotero-pdf-translate.png`, which suggests the wider project is related to Zotero, a reference manager, and GPT-based features such as PDF translation. The supplied files do not include the Zotero integration code itself, so this README describes only the demo script and the other files that are present.

The repository contains:

- `demo.py`: a runnable example of non-streaming and streaming chat completion calls.
- `images/`: image assets, including a logo, screenshots, and diagrams. Their contents are not described here.
- `.github/ISSUE_TEMPLATE/`: templates for bug reports and feature requests.
- `.gitattributes` and `LICENSE`: repository metadata and the MIT license.

## Repository Structure

```
.gitattributes
.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/feature_request.md
LICENSE
demo.py
images/             # logo, screenshots, and diagrams
```

## Setup

The supplied files do not include a dependency manifest such as `requirements.txt`, `pyproject.toml`, or `setup.py`, and they do not state a required Python version.

`demo.py` imports the `OpenAI` class from the `openai` package and calls `client.chat.completions.create(...)`. This is the interface used by version 1.x and later of the `openai` package, so that package must be installed. You can install it with:

```bash
pip install openai
```

To get the code, clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

## Configuration

The client is configured at the top of `demo.py`:

```python
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="YOUR API KEY",
    base_url="https://api.chatanywhere.tech/v1"
)
```

- **API key:** The file contains the placeholder `"YOUR API KEY"`. Replace it with your own key before running the script. The comment in the code notes that the OpenAI client defaults to the `OPENAI_API_KEY` environment variable when no key is passed. Because this script passes `api_key` explicitly, the environment variable is not used unless you change that line. Avoid committing a real key to version control.
- **Base URL:** The script sends requests to `https://api.chatanywhere.tech/v1` rather than the OpenAI client's default endpoint. Change this value if you use a different OpenAI-compatible endpoint.
- **Model:** Both functions hard-code the model name `gpt-3.5-turbo`. To use another model, edit the `model` argument in `demo.py`.

## Usage

Run the demo script:

```bash
python demo.py
```

By default, the `__main__` block sends one user message and uses the streaming function:

```python
messages = [{'role': 'user','content': '鲁迅和周树人的关系'},]
# 非流式调用
# gpt_35_api(messages)
# 流式调用
gpt_35_api_stream(messages)
```

The message asks, in Chinese, about the relationship between Lu Xun and Zhou Shuren. To switch to a non-streaming call, comment out `gpt_35_api_stream(messages)` and uncomment `gpt_35_api(messages)`.

### Available functions

**`gpt_35_api(messages: list)`**
Sends the full conversation in `messages` and waits for the complete response. It prints `completion.choices[0].message.content`.

**`gpt_35_api_stream(messages: list)`**
Sends the same request with `stream=True`. It iterates over the returned chunks and prints each non-empty `delta.content` as it arrives, with no newline between chunks.

### Message format

Both functions take a list of message dictionaries using the OpenAI chat format, where each item has a `role` and a `content` key. The demo uses a single `user` message:

```python
messages = [
    {'role': 'user', 'content': 'Your question here'},
]
```

To continue a conversation, add earlier `user` and `assistant` messages to the list before calling the function.

## Development

The repository includes GitHub issue templates in `.github/ISSUE_TEMPLATE/`:

- **Bug report** (`bug_report.md`): asks for a description of the bug, steps to reproduce it, screenshots, the tools or programming language used, and any additional context. The template labels are written in both English and Chinese.
- **Feature request** (`feature_request.md`): asks for the problem the feature would solve, the desired solution, alternatives considered, and additional context. Issues created from this template are titled with the prefix `[Enhancement]`.

The supplied files do not contain contribution guidelines, a code style guide, or build tooling.

## Testing

The supplied files do not include a test suite, test configuration, or continuous integration workflow. The only executable code is `demo.py`, which makes live API calls when run. It needs a valid API key and network access to the configured endpoint, so it is best treated as a manual example rather than an automated test.

## License

This project is licensed under the MIT License. The copyright notice in `LICENSE` reads:

> Copyright (c) 2023-2024 牛爷爷信息技术（南京）有限公司

The MIT License permits use, copying, modification, merging, publication, distribution, sublicensing, and sale of the software, provided the copyright and permission notice are included in copies or substantial portions of the software. The software is provided "as is," without warranty of any kind.

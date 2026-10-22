# Zotero GPT

This repository contains a small Python example for calling an OpenAI-compatible chat-completions API, along with image assets whose filenames reference Zotero GPT and PDF translation. The supplied files do not include a Zotero extension’s source code, installation package, or configuration documentation, so this README describes only the example and materials present here.

## Overview

[`demo.py`](demo.py) demonstrates two ways to send chat messages to a model:

- **Non-streaming:** waits for the response and prints its message content.
- **Streaming:** prints response text as it arrives.

The example uses the `OpenAI` Python client, the `gpt-3.5-turbo` model name, and the base URL `https://api.chatanywhere.tech/v1`. Its sample prompt, written in Chinese, asks about the relationship between Lu Xun and Zhou Shuren.

The repository also contains image files named for Zotero-related topics and interfaces, including `zotero-gpt`, `zotero-pdf-translate`, and `zotero7-gpt`. These are image assets; the supplied files do not explain or implement the features those names may refer to.

## Repository contents

- [`demo.py`](demo.py) — Python chat-completions example.
- `images/` — image assets, including `logo.png`, `chatbox.png`, `sidebar.png`, `zotero-gpt.png`, and other Zotero- or service-named files.
- `.github/ISSUE_TEMPLATE/` — templates for bug reports and feature requests.
- [`LICENSE`](LICENSE) — MIT License.

There is no dependency manifest, application source tree, or test suite among the supplied files.

## Requirements

- Python installed in your environment. The repository does not specify a minimum Python version.
- The `openai` Python package, imported by `demo.py`.
- An API key accepted by the configured API endpoint.

The example is an API client demonstration; the supplied files do not establish that it installs or runs as a Zotero plugin.

## Setup

1. Clone or download the repository.
2. (Optional) Create and activate a Python virtual environment using your preferred workflow.
3. Install the client library:

   ```bash
   python -m pip install openai
   ```

4. Configure the API key in `demo.py` before running the example. The file currently contains the literal placeholder `"YOUR API KEY"`:

   ```python
   client = OpenAI(
       api_key="YOUR API KEY",
       base_url="https://api.chatanywhere.tech/v1"
   )
   ```

   Replace the placeholder with a key valid for the configured endpoint. The code comments that the client defaults to `OPENAI_API_KEY` when no key is supplied, but the example explicitly supplies a value. To use the environment-variable default, remove the `api_key` argument or change the code accordingly.

Do not commit real API keys to a shared repository.

## Usage

Run the example from the repository directory:

```bash
python demo.py
```

The `__main__` block creates a one-message conversation and calls the streaming function. To use a non-streaming response instead, edit the bottom of `demo.py` to enable `gpt_35_api(messages)` and disable `gpt_35_api_stream(messages)`. The two calls are commented in the file for this purpose.

The non-streaming function submits the supplied messages and prints the first choice’s message content:

```python
gpt_35_api(messages)
```

The streaming function submits the same kind of message list with streaming enabled, then prints each non-empty content fragment as it arrives:

```python
gpt_35_api_stream(messages)
```

Both functions accept a list of chat messages. The included example uses this format:

```python
messages = [
    {"role": "user", "content": "鲁迅和周树人的关系"}
]
```

Change the prompt or provide a longer conversation by editing the `messages` list. The example uses the model name `gpt-3.5-turbo`; whether that model and endpoint are available depends on the API service and account you use.

## Configuration

The client is configured near the top of `demo.py`:

- **`api_key`** — credentials for the API. The checked-in value is a placeholder and must be replaced or removed.
- **`base_url`** — the API base URL. The example sets it to `https://api.chatanywhere.tech/v1`.
- **`model`** — set in each function as `gpt-3.5-turbo`.
- **`messages`** — the conversation supplied to the completion request.

The repository provides no separate configuration file, command-line options, or documented settings for other components. If using a different OpenAI-compatible service, update the base URL and use a model name supported by that service.

## Development

The example is a single Python file and can be modified directly. Its two API functions illustrate the request patterns used in this repository: a standard completion request and a request with `stream=True`. The code prints results to the terminal and does not define a reusable command-line interface or application package.

No formatter, linter, build tool, dependency lockfile, or contribution guide is included in the supplied files. The issue templates provide a format for reporting problems and proposing enhancements. When reporting an API issue, include the tool or programming language used, steps to reproduce it, and relevant context; avoid sharing API keys or other secrets.

## Testing

No automated tests or test command are provided. A basic manual check is to install `openai`, configure a valid key and endpoint, and run `python demo.py`. A successful run should print response text; failures may result from credentials, service availability, model support, connectivity, or client setup. The repository does not specify expected output or provide a mock service for offline testing.

## License

This project is distributed under the MIT License. Copyright (c) 2023–2024 牛爷爷信息技术（南京）有限公司. See [`LICENSE`](LICENSE) for the complete terms.

# GPT_API_free-923qohmf

A small Python demo for calling an OpenAI-compatible chat completions endpoint, with both non-streaming and streaming response handling.

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project is a small Python demo that shows how to call an OpenAI-compatible chat completions endpoint. It sends a chat message and prints the reply, with both non-streaming and streaming response handling. It is aimed at developers who want a minimal reference for calling a chat API from Python. The repository provides a command-line entry point for running the streaming example and helper functions for both response modes. For runnable steps, see Getting Started.

---

## Core Features

- **Chat completions with a single response:** Sends a list of chat messages to the `gpt-3.5-turbo` model and prints the complete reply once it is generated. This gives developers a simple way to get one answer per request.
- **Streaming responses:** Sends the same kind of request with streaming enabled and prints each content fragment as it arrives. This lets developers show partial output while the model is still generating.
- **OpenAI SDK with a custom base URL:** Uses the official `openai` Python client pointed at a custom OpenAI-compatible endpoint. This lets developers reuse familiar SDK calls with a compatible provider.

---

## Installation

Install GPT_API_free-923qohmf from the current local checkout:

1. Open the repository root:
```sh
cd path/to/GPT_API_free-923qohmf
```
2. Install the `openai` Python SDK. The repository has no requirements file, pyproject, or lockfile, so install the dependency manually:
```sh
pip install openai
```

---

## Getting Started

### Prerequisites

- Python 3
- The `openai` Python SDK. The repository has no requirements file, pyproject, or lockfile, so no version is pinned.
- An API key for an OpenAI-compatible endpoint. The demo uses the base URL `https://api.chatanywhere.tech/v1`.

### Steps

1. Open `demo.py` and replace the placeholder `"YOUR API KEY"` in the `OpenAI(...)` constructor with your API key. The explicit `api_key` argument takes precedence over the `OPENAI_API_KEY` environment variable mentioned in the code comment. To avoid storing the key in source code, you can instead set the `OPENAI_API_KEY` environment variable and remove the `api_key` argument from the `OpenAI(...)` constructor.
2. Run the demo script:

```bash
python demo.py
```

3. The script runs the streaming helper `gpt_35_api_stream` with the prompt `鲁迅和周树人的关系` and prints the response to the console as it streams.
4. To run the non-streaming version instead, edit the `__main__` block in `demo.py`: uncomment `gpt_35_api(messages)` and comment out `gpt_35_api_stream(messages)`.

The demo's comments, docstrings, and prompt are in Chinese.

---

## Contributing

No contributing guidelines are included in this README.

---

## License

This project is licensed under the MIT License. A `LICENSE` file was not confirmed in the repository tree reviewed for this README, so check the repository root for the full license text before reuse.

---

## Citation

No citation information is provided in this repository.
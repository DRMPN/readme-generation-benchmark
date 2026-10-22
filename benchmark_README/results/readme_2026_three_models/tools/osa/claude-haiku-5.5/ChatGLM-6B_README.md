# ChatGLM-6B-ge1l7i5g

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

ChatGLM-6B is a Python project that loads the THUDM/chatglm-6b language model through Hugging Face transformers and provides tooling for running it and adapting it. It is intended for ML researchers and developers who want to run LLM inference or fine-tune the model, and it also serves end users who interact with the model through demo interfaces. The repository offers several interaction surfaces, including a command-line interface, a web-based chat interface, and an HTTP API service, along with a P-Tuning v2 fine-tuning and evaluation workflow and vision-related variants. Observed code requires a CUDA-capable GPU; see Getting Started for prerequisites and runnable steps.

---

## Core Features

- **Interactive chat inference:** Run ChatGLM-6B from a terminal chat loop, a Gradio web interface, or a REST endpoint, so developers can test the model in whichever interface fits their workflow.
- **Streaming responses with adjustable generation settings:** The web interface streams replies and exposes controls for maximum length, Top P, and temperature, letting users tune output without editing code.
- **Multimodal demos:** Vision variants of the CLI and web demos are provided for trying image-plus-text interaction with the model.
- **P-Tuning v2 fine-tuning and evaluation:** A sequence-to-sequence training and evaluation pipeline supports adapting the model to custom datasets, with support for quantization settings and JSON-based configuration.
- **Programmatic API access:** A FastAPI service accepts prompts with optional history and generation parameters, returning the response and updated conversation history for integration into other applications.

---

## Installation

Install ChatGLM-6B-ge1l7i5g using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/ChatGLM-6B-ge1l7i5g
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

### Prerequisites

- Python with pip.
- A CUDA-capable NVIDIA GPU. The demo and API scripts call `.cuda()` or set `DEVICE = "cuda"`, so they will not run on CPU as written.
- Access to the `THUDM/chatglm-6b` model. The scripts load it by name with `transformers` (`trust_remote_code=True`), so it is fetched from Hugging Face on first use.

For full setup details, see the Installation section.

### Steps

1. Install the dependencies from the repository root:

```bash
   pip install -r requirements.txt
```

2. Start the command-line demo:

```bash
   python cli_demo.py
```

   Type a message at the `用户：` prompt. Enter `clear` to clear the conversation history, or `stop` to exit.

3. Start the Gradio web demo:

```bash
   python web_demo.py
```

   The interface includes a **Submit** button, a **Clear History** button, and sliders for **Maximum length**, **Top P**, and **Temperature**.

4. Start the HTTP API. `api.py` imports `fastapi` and `uvicorn`, which are not listed in `requirements.txt`, so install them first:

```bash
   pip install fastapi uvicorn
   python api.py
```

   The server listens on port `8000`. Send a POST request to `/` with a JSON body that includes `prompt`:

```bash
   curl -X POST http://127.0.0.1:8000 -H "Content-Type: application/json" -d "{"prompt": "你好", "history": []}"
```

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Contributing

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). ChatGLM-6B-ge1l7i5g repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{ChatGLM-6B-ge1l7i5g,

        author = {README Benchmark},

        title = {ChatGLM-6B-ge1l7i5g repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
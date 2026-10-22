# ChatGLM-6B-b8iscbty

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project provides runnable access to ChatGLM-6B, an open-weight conversational large language model, together with a vision variant (VisualGLM) and a P-tuning v2 fine-tuning toolkit. It is intended for ML researchers and developers—particularly those working on Chinese-language NLP—who want to deploy, chat with, or fine-tune the model on their own hardware. The repository offers several interaction surfaces: a command-line chat interface, browser-based chat demos (including one for the vision model), a local REST API endpoint, and trainer-based fine-tuning and evaluation flows. Multi-GPU model loading and quantization utilities are included to help run the model on limited hardware. For runnable setup and launch steps, see the Getting Started section.

---

## Core Features

- Conversational AI deployment with multiple interfaces — run ChatGLM-6B as a command-line chat, a browser-based Gradio web demo, or a FastAPI HTTP service, so you can pick the interaction style that fits your workflow.
- Streaming, multi-turn dialogue with tunable generation — responses stream in real time and you can adjust maximum length, top-p, and temperature, with conversation history maintained across turns.
- Image-grounded chat via VisualGLM — a companion web demo lets you upload an image and ask questions or request descriptions about it.
- P-tuning v2 fine-tuning toolkit — train and evaluate the model on your own prompt-response datasets with ready-to-use training/evaluation scripts and standard Chinese/English metrics (ROUGE, BLEU).
- Flexible GPU deployment — quantization support and automatic multi-GPU model sharding let you run and tune the model on modest hardware.

---

## Installation

Install ChatGLM-6B-b8iscbty from a local checkout of this repository:

1. Open the repository root:
```sh
cd path/to/ChatGLM-6B-b8iscbty
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

Run your first conversation with ChatGLM-6B via the command-line demo.

**Prerequisites**

- Python 3 with the dependencies listed in `requirements.txt` (including `transformers==4.27.1` and `torch>=1.10`).
- An NVIDIA CUDA GPU — the demo scripts load the model in half precision onto the GPU.
- Internet access on first run: the model weights (`THUDM/chatglm-6b`) are downloaded automatically from Hugging Face.

**Quickstart**

1. Install the dependencies:

```bash
   pip install -r requirements.txt
```

2. Launch the CLI demo:

```bash
   python cli_demo.py
```

3. Wait for the model to download and load, then type a message to start chatting.
4. Type `clear` to reset the conversation history, or `stop` to exit.

**Other entry points**

- `python web_demo.py` — Gradio web UI, opens in your browser.
- `python api.py` — FastAPI HTTP service; see `api.py` for launch details and the expected request format.
- `python web_demo_vision.py` — image-and-text chat using the VisualGLM weights (`THUDM/visualglm-6b`).

To fine-tune the model with P-Tuning v2, see `ptuning/README.md`.

---

## Examples

Runnable usage examples are available in the [examples](./examples) directory.

---

## Documentation

In addition to this README, the repository includes the following documentation:

- [FAQ.md](./FAQ.md) — answers to frequently asked questions.
- [PROJECT.md](./PROJECT.md) — project overview.
- [UPDATE.md](./UPDATE.md) — summary of recent updates.
- [ptuning/README.md](./ptuning/README.md) — guide to P-Tuning v2 fine-tuning and evaluation.
- [improve/README.md](./improve/README.md) — README for the `improve/` directory.
- [resources/WECHAT.md](./resources/WECHAT.md) — WeChat-related resources.

---

## Contributing

Contributions are welcome. If you find a bug or would like to propose a new feature, please open an issue using the corresponding template under [.github/ISSUE_TEMPLATE](./.github/ISSUE_TEMPLATE):

- **Bug report** — for reporting problems with the code or documentation.
- **Feature request** — for suggesting improvements or new functionality.

When filing a bug report, please include your environment details and the steps needed to reproduce the issue.

---

## License

The code of this project is licensed under Apache 2.0, while the model weights are distributed under a separate license — see [MODEL_LICENSE](./MODEL_LICENSE). For more details on the code license, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). ChatGLM-6B-b8iscbty repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{ChatGLM-6B-b8iscbty,

        author = {README Benchmark},

        title = {ChatGLM-6B-b8iscbty repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
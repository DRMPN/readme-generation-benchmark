# ChatGLM-6B-35iwa983

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This repository provides inference and P-tuning or fine-tuning workflows for ChatGLM-6B, for developers and ML practitioners working with the model. It offers command-line, browser-based, and HTTP API interfaces alongside training and evaluation workflows. See Getting Started for runnable steps.

---

## Installation

Install ChatGLM-6B-35iwa983 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/ChatGLM-6B-35iwa983
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

Prerequisites: Python, PyTorch, Transformers, and a CUDA-capable GPU for the inference demos. The demos load `THUDM/chatglm-6b` through `from_pretrained`.

1. Start with `cli_demo.py` for an interactive chat. Enter a prompt to chat; enter `clear` to clear history or `stop` to exit.
2. For a browser interface, use `web_demo.py`; it launches the Gradio demo in a browser.
3. For the HTTP interface, use `api.py`. It serves `POST /` on port `8000`; requests can include a `prompt` and optional `history`.
4. For training or evaluation, use `ptuning/main.py`. Supply the relevant `train_file`, `validation_file`, or `test_file` and select `do_train`, `do_eval`, or `do_predict`. The script accepts arguments directly or a single JSON argument file.

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

    README Benchmark (2026). ChatGLM-6B-35iwa983 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{ChatGLM-6B-35iwa983,

        author = {README Benchmark},

        title = {ChatGLM-6B-35iwa983 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
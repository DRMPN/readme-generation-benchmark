# gpt-researcher-67e1mkt1

---

[![PyPi](https://badge.fury.io/py/gpt-researcher.svg)](https://badge.fury.io/py/gpt-researcher)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![arxiv](https://img.shields.io/badge/arXiv-B31B1B.svg?style={0}&logo=arXiv&logoColor=white)
![fastapi](https://img.shields.io/badge/FastAPI-009688.svg?style={0}&logo=FastAPI&logoColor=white)
![jinja2](https://img.shields.io/badge/Jinja-B41717.svg?style={0}&logo=Jinja&logoColor=white)
![markdown](https://img.shields.io/badge/Markdown-000000.svg?style={0}&logo=Markdown&logoColor=white)
![openai](https://img.shields.io/badge/OpenAI-412991.svg?style={0}&logo=OpenAI&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style={0}&logo=Pydantic&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

GPT Researcher is an autonomous agent for conducting online research and generating research reports. It is intended for developers integrating or running the agent, as well as researchers and other users seeking automated reports. The project offers a Python library, command-line interface, and web application; see Getting Started for runnable steps.

---

## Installation

**Prerequisites:** requires Python >=3.11, <4

Install gpt-researcher-67e1mkt1 using one of the following methods:

**Using PyPi:**

```sh
pip install gpt-researcher
```

---

## Getting Started

Use Python 3.11 or newer. Project dependencies are declared in `pyproject.toml`.

---

## Architecture

The repository is organized as a modular application with a Python research package (`gpt_researcher`), a FastAPI backend (`backend`), a Next.js frontend (`frontend/nextjs`), a CLI (`cli.py`), and separate multi-agent components (`multi_agents`).

The CLI uses `GPTResearcher` to conduct research and write reports. The backend exposes a WebSocket chat endpoint. The multi-agent entry point delegates research tasks to `ChiefEditorAgent`. The available context does not establish how the frontend connects to the backend.

---

## Testing

A test suite is available in `tests/`, and pytest configuration is defined in `pyproject.toml`. No test run command is documented here.

---

## Examples

Examples of how this should work and how it should be used are available [here](./docs/docs/examples).

---

## Documentation

A detailed gpt-researcher-67e1mkt1 description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to gpt-researcher-67e1mkt1.

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this software, please cite it as it is written in the [CITATION](./citation.cff) file.

---
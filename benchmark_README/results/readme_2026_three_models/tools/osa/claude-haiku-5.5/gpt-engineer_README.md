# gpt-engineer-3zaz19r4

---

[![PyPi](https://badge.fury.io/py/gpt-engineer.svg)](https://badge.fury.io/py/gpt-engineer)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![openai](https://img.shields.io/badge/OpenAI-412991.svg?style={0}&logo=OpenAI&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB.svg?style={0}&logo=Python&logoColor=white)
![toml](https://img.shields.io/badge/TOML-9C4121.svg?style={0}&logo=TOML&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

gpt-engineer is a tool that uses large language models to generate new code projects from a natural-language prompt and to improve existing ones. Its primary interface is a command-line tool built with Typer, which is intended for developers who want to generate or modify projects with an LLM. The underlying Python modules are also importable for developers who want to integrate the generation and improvement workflow into their own code. For runnable setup and first steps, see the Getting Started section.

---

## Core Features

- **Generate projects from natural-language prompts:** Describe an application in plain language and receive generated code files, so developers can start a project without writing the initial scaffold by hand.
- **Improve existing code with prompts:** Request changes to an existing project in natural language, so developers can iterate on a codebase without manually editing each file.
- **Use from the command line:** A Typer-based CLI exposes generation and improvement workflows, so developers can run them directly from a terminal.
- **Embed in Python code:** The `gpt_engineer` package can be imported, and its agent components accept custom generation, improvement, and processing functions, so developers can integrate or adapt the workflow in their own tools.

---

## Installation

**Prerequisites:** requires Python >=3.10,<3.13

Install gpt-engineer-3zaz19r4 using one of the following methods:

**Using PyPi:**

```sh
pip install gpt-engineer
```

---

## Getting Started

### Prerequisites

- Python, with the project's dependencies installed as described in the Installation section.
- An OpenAI API key, set as the `OPENAI_API_KEY` environment variable. The CLI reads this variable at startup.

### Steps

1. Install the project by following the **Installation** section.
2. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
3. Start the CLI. The launch command is unconfirmed in the repository context reviewed here. See the **Installation** section for the verified command.
4. When prompted, describe what you want to build. The CLI asks, "What application do you want gpt-engineer to generate?" In improve mode, it asks, "How do you want to improve the application?"

The default project path is `projects/example`.

---

## Testing

The test suite lives under `tests/` and covers the CLI, core modules, benchmark configuration, and git integration. It also includes tests for AI token usage, file selection, project configuration, and an installation check.

A `tox.ini` file is present at the repository root, but the exact test run command is not confirmed in the provided context. Check `tox.ini` and `pyproject.toml` for the configured test runner before running tests.

Continuous integration workflows and pre-commit hooks are configured in the repository's `.github/workflows` directory and `.pre-commit-config.yaml`. Review these before opening a pull request to match the checks that run on changes.

---

## Examples

Examples of how this should work and how it should be used are available [here](./docs/examples).

---

## Documentation

A detailed gpt-engineer-3zaz19r4 description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./.github/CONTRIBUTING.md)**: To learn more about making a contribution to gpt-engineer-3zaz19r4.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this software, please cite it as it is written in the [CITATION](./citation.cff) file.

---
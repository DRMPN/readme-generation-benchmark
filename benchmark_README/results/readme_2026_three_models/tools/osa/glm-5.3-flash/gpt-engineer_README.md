# gpt-engineer-jg3hnycv

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
- [Architecture](#architecture)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

gpt-engineer is a Python command-line tool that uses large language models to generate new code projects from natural-language prompts and to improve existing codebases. It is aimed primarily at developers who want to produce or refine application code through an LLM, as well as AI practitioners and researchers who need a customizable generation pipeline with a built-in benchmark harness. The tool is operated via a command-line interface, and its agent behavior is composed of injectable steps, with abstractions for memory, execution environments, and configurable preprompts. See the Getting Started section for runnable steps and initial setup.

---

## Core Features

- **Generate projects from natural-language prompts**: describe an application and the tool produces a complete codebase, including a generated entrypoint, via an LLM.
- **Improve existing code**: request targeted changes to an existing project and review colored diffs of the proposed edits before they are applied.
- **Automated execution and refinement**: generated code is run in an execution environment, with entrypoint execution and self-healing steps to refine edits that fail to apply.
- **Customizable agent behavior**: swap in your own generation, improvement, and processing step functions, or supply custom preprompts to steer how the AI works.
- **Built-in benchmark harness**: evaluate code generation quality across multiple benchmark suites with configurable settings.

---

## Installation

**Prerequisites:** requires Python >=3.10,<3.13

Install gpt-engineer-jg3hnycv using one of the following methods:

**Using PyPi:**

```sh
pip install gpt-engineer
```

---

## Getting Started

## Prerequisites

- Python with [Poetry](https://python-poetry.org/) for dependency management (see `pyproject.toml` / `poetry.lock`).
- An OpenAI API key. `ANTHROPIC_API_KEY` is supported as well; both can be provided via environment variables or a `.env` file (a `.env.template` is included in the repository).

## Steps

1. **Install dependencies:**

```bash
   poetry install
```

2. **Configure your API key.** Set `OPENAI_API_KEY` in your environment, or create a `.env` file in your working directory based on the provided `.env.template`. The CLI loads the key automatically if it is not already set.

3. **Run the CLI.** The console script entry point is defined in `pyproject.toml`; launch it through Poetry, for example:

```bash
   poetry run <console-script>
```

   Replace `<console-script>` with the script name declared under the `[tool.poetry.scripts]` section of `pyproject.toml`. When run without arguments, the tool prompts you to describe the application you want generated; the default project path is `projects/example`.

4. **Improve an existing project.** Run the same CLI in improve mode to modify code in an existing project directory; the tool will ask how you want to improve the application.

For installation alternatives (including Docker), see the Installation docs. Windows-specific guidance is available in `WINDOWS_README.md`.

---

## Architecture

gpt-engineer is organized as a layered Python package built around a small set of core abstractions with pluggable implementations.

- **Core abstractions (`gpt_engineer.core`)**: Define the main interfaces — `BaseAgent`, `BaseMemory`, and `BaseExecutionEnv` — along with supporting pieces such as the `AI` model wrapper, `Prompt`, `FilesDict`, diff handling, git integration, linting, token usage tracking, and project configuration.
- **Default implementations (`gpt_engineer.core.default`)**: Provide concrete classes for the abstractions, including `DiskMemory` (file-based memory), `DiskExecutionEnv` (local code execution), `FileStore`, and `SimpleAgent`, plus step functions (e.g., `gen_code`, `improve_fn`, `execute_entrypoint`) that compose the generation and improvement workflows.
- **Agent composition**: Agent behavior is assembled from injectable step functions (such as code generation, improvement, and code processing callables) rather than hard-coded logic, allowing custom pipelines to be swapped in.
- **Preprompts (`gpt_engineer.preprompts`)**: File-based prompt templates (e.g., `generate`, `improve`, `file_format`, `philosophy`) that guide the LLM; `PrepromptsHolder` loads them, and custom preprompts can override the defaults per project.
- **CLI application (`gpt_engineer.applications.cli`)**: The user-facing entrypoint (`main.py`, `cli_agent.py`) wires together environment loading, prompt collection (including optional image inputs), file selection, learning/feedback collection, and the agent's generation or improvement lifecycle.
- **Benchmark harness (`gpt_engineer.benchmark`)**: A TOML-configured evaluation suite with loaders for benchmarks such as `apps`, `mbpp`, and `gptme`, used to measure agent performance.
- **Tools (`gpt_engineer.tools`)**: Auxiliary utilities, including custom step functions and supported-language definitions.

Data flow at a high level: the CLI loads environment configuration and a user prompt, the agent combines the prompt with preprompts and sends it to the configured LLM, the resulting code is parsed into a `FilesDict`, stored via the memory layer, and executed or refined through the execution environment and step functions. Optional Docker packaging (`docker/`) is provided for containerized use.

This is a monolithic, single-package design — not a microservice architecture — where the abstraction layer is the primary extension point.

---

## Testing

The repository ships a test suite under `tests/`, organized to mirror the package layout:

- **Unit tests** across `gpt_engineer.core` (including its default implementations), the CLI application (`gpt_engineer.applications.cli`), the benchmark package, and `gpt_engineer.tools`.
- **Improve-flow regression fixtures** in `tests/core/improve_function_test_cases/`.
- **A shared mock AI module** (`tests/mock_ai.py`).

For the exact test commands, refer to `tox.ini` and the `Makefile`; continuous integration runs the automated checks via the GitHub Actions workflow `.github/workflows/ci.yaml`. Pre-commit hooks are configured in `.pre-commit-config.yaml` and validated by the dedicated workflow `.github/workflows/pre-commit.yaml`. Run the suite and hooks locally before submitting changes.

---

## Examples

Examples of how this should work and how it should be used are available [here](./docs/examples).

---

## Documentation

A detailed gpt-engineer-jg3hnycv description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./.github/CONTRIBUTING.md)**: To learn more about making a contribution to gpt-engineer-jg3hnycv.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this software, please cite it as it is written in the [CITATION](./citation.cff) file.

---
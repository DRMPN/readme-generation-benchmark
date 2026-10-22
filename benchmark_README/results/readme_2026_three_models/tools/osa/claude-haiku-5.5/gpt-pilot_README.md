# gpt-pilot-n17pe45b

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![anthropic](https://img.shields.io/badge/Anthropic-191919.svg?style={0}&logo=Anthropic&logoColor=white)
![jinja2](https://img.shields.io/badge/Jinja-B41717.svg?style={0}&logo=Jinja&logoColor=white)
![openai](https://img.shields.io/badge/OpenAI-412991.svg?style={0}&logo=OpenAI&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style={0}&logo=Pydantic&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB.svg?style={0}&logo=Python&logoColor=white)
![sqlalchemy](https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style={0}&logo=SQLAlchemy&logoColor=white)
![tqdm](https://img.shields.io/badge/tqdm-FFC107.svg?style={0}&logo=tqdm&logoColor=black)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Pythagora Core is a Python package that uses AI agents to build complete applications from a written description of the app. It is intended for developers and end users who want AI-assisted application generation and are comfortable working with a command-line tool. The primary interface is a command-line interface for interactive use, and work sessions can be resumed from saved project state. For runnable steps, see the Getting Started section.

---

## Core Features

- **Natural-language app generation:** Describe the app you want in plain language and the agent-based CLI builds a complete application, so you can go from idea to working code without writing the initial scaffolding yourself.
- **Multiple LLM providers:** Choose from OpenAI, Anthropic, Groq, Azure, Relace, or a local LM Studio server, so you can use the model service that fits your cost, access, or privacy needs.
- **Selectable UI modes:** Run in plain terminal mode, connect to an IPC client, or use a virtual adapter, so you can integrate the generator into different interactive or automated workflows.
- **Documented telemetry behavior:** Telemetry is described in a dedicated document, so you can review what usage data is collected before running the tool.

---

## Installation

**Prerequisites:** requires Python ^3.9

Install gpt-pilot-n17pe45b using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/gpt-pilot-n17pe45b
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

### Prerequisites

- Python 3.9 or later (per `pyproject.toml`).
- An API key for at least one supported LLM provider. Supported providers are `openai`, `relace`, `anthropic`, `groq`, `lm-studio`, and `azure`.

Complete the environment setup in the [Installation](#installation) section before continuing.

### Steps

1. **Install dependencies.** Follow the [Installation](#installation) section.

2. **Configure LLM credentials.** The provider configuration accepts an `api_key` and an optional `base_url`. This repository's provided context does not document the environment variable names or config file that supply these values. See the Installation section or the configuration documentation for the supported mechanism.

3. **Start the CLI.** From the repository root, run:

```bash
python main.py
```

   `main.py` calls `run_pythagora` from `core/cli/main.py`.

4. **Create a project.** When prompted with "What do you want to build?", select the **Full stack app** option. Then describe the application you want to build.

5. **Check the logs (optional).** By default, logs are written to `data/pythagora.log`, as set in the log configuration.

---

## Testing

Contributors verify changes with the pytest suite in `tests/`.

**Test layout**
- `tests/` mirrors the `core/` package with subfolders for `agents`, `cli`, `config`, `db`, `disk`, `llm`, `proc`, `state`, `telemetry`, `templates`, and `ui`.
- `tests/integration/llm/` contains integration tests for the LLM layer.
- `tests/conftest.py` is present. Its contents are not included in the provided context.

**Test configuration (`pyproject.toml`)**
- `[tool.pytest.ini_options]` sets pytest options that include coverage for the `core` package (`--cov=core`) and a 10-second per-test timeout (`--timeout 10`).
- `pythonpath` is set to `.`.
- Coverage excludes `core/db/migrations/*` and `core/templates/tpl/*`, along with lines under `if TYPE_CHECKING:` and `raise NotImplementedError()`.

**Dev dependencies**
- Test and lint tools are declared under `[tool.poetry.group.dev.dependencies]` in `pyproject.toml`: `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-timeout`, `ruff`, and `pre-commit`.
- The command to install these dependencies is not evidenced in the provided context.
- The command to run the test suite is not documented in the provided context.

**Lint and formatting**
- Ruff is configured in `pyproject.toml` with a line length of 120, target version `py39`, and the `I` (import sorting) rule set extended.
- `.pre-commit-config.yaml` is present. Its hooks are not shown in the provided context.

**CI**
- `.github/workflows/` exists. Its contents are not provided, so CI test steps cannot be confirmed.

---

## Documentation

A detailed gpt-pilot-n17pe45b description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./.github/CONTRIBUTING.md)**: To learn more about making a contribution to gpt-pilot-n17pe45b.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). gpt-pilot-n17pe45b repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{gpt-pilot-n17pe45b,

        author = {README Benchmark},

        title = {gpt-pilot-n17pe45b repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
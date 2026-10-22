# gpt-pilot-phb3a9cx

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
- [Architecture](#architecture)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Pythagora is an AI-driven development tool that builds complete full-stack applications from a natural-language description using an agent-based workflow. It is a Python command-line application intended for developers who want AI-assisted software creation, orchestrating multiple specialized agents and LLM providers to plan, implement, and debug apps. The tool runs as an interactive CLI session and can also operate through a UI adapter layer, with configurable LLM providers and agent settings. See the Getting Started section for runnable steps.

---

## Core Features

- **AI-driven app development** — Orchestrates specialized agents that plan, specify, build, and debug full-stack applications from a natural-language description, so developers can go from idea to working code with minimal manual scaffolding.
- **Multiple project types** — Supports generating full-stack Node.js apps or frontend-only apps against an existing backend with an OpenAPI/Swagger specification, matching the tool to your starting point.
- **Multi-provider LLM support** — Works with OpenAI, Anthropic, Groq, Azure, LM Studio, and Relace, letting you choose or switch models (including per-agent model configuration) based on cost, quality, or availability.
- **Resumable, persistent sessions** — Stores project state in a database so you can pause work, continue projects or specific steps later, and roll back safely on interruptions or errors.
- **Flexible UI modes** — Runs in a plain terminal interface, via an IPC client for editor/extension integration, or in a virtual mode for automated testing and headless usage.

---

## Installation

**Prerequisites:** requires Python ^3.9

Install gpt-pilot-phb3a9cx using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/gpt-pilot-phb3a9cx
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

## Prerequisites

- Python 3.9+ (per `pyproject.toml`)
- An LLM provider API key (Pythagora supports providers such as OpenAI, Anthropic, and Groq)

## Quickstart

1. **Set up the Python environment** in the repository root:

```sh
   python -m venv venv
   venv/bin/python -m pip install -r requirements.txt
```

   On Windows, use `venv\Scripts\python` instead of `venv/bin/python`.

2. **Configure your LLM provider.** Each provider can use a default API key from its environment variable, or you can set an `api_key` explicitly in the provider configuration (see the `ProviderConfig` / `LLMConfig` settings in `core/config/__init__.py`). Consult your provider's documentation for the exact environment variable name.

3. **Run Pythagora** from the repository root:

```sh
   python main.py
```

   The CLI entry point is `main.py`, which calls `run_pythagora()` from `core.cli.main`. If dependencies are missing, the script prints the exact setup commands above to stderr and exits.

4. **Start a project.** When prompted, choose what you want to build (e.g., a full-stack Node app or a frontend for an existing backend with OpenAPI/Swagger) and describe your app. The Orchestrator agent then runs the development workflow for you.

Note: Pythagora collects anonymous telemetry by default; see `docs/TELEMETRY.md` for what is collected.

---

## Architecture

Pythagora is an asynchronous Python CLI application in which an orchestrator coordinates LLM-driven agents to plan, build, and debug full-stack applications from starter templates.

- **CLI entry point** — `main.py` invokes `run_pythagora()` in `core/cli/main.py`, which sets up the session, runs Alembic database migrations before the asyncio loop starts, and wires together state, UI, and agents.
- **Orchestrator** (`core/agents/orchestrator.py`) — the central control loop; it runs specialized agents such as TechLead, SpecWriter, Architect, Developer, CodeMonkey, BugHunter, Troubleshooter, and Frontend until a project run completes, fails, or is interrupted.
- **Prompts** (`core/prompts/`) — per-role Jinja2 templates (e.g., `tech-lead`, `code-monkey`, `bug-hunter`) plus shared `partials` define each agent's behavior.
- **LLM layer** (`core/llm/`) — provider clients for OpenAI, Anthropic, Groq, Azure, LM Studio, and Relace (see `LLMProvider` in `core/config/`), with per-agent model configuration handled by the Pydantic-based configuration system.
- **State and persistence** (`core/state/`, `core/db/`) — `StateManager` tracks project state and rolls back on interrupts or LLM/API errors; data is stored via async SQLAlchemy (SQLite through aiosqlite) with Alembic migrations under `core/db/migrations/`.
- **UI adapters** (`core/ui/`) — pluggable frontends behind a common `UIBase` interface: `plain` (terminal), `ipc-client` (backed by the IPC server in `core/ui/api_server.py`), and `virtual`.
- **Templates and support modules** — `core/templates/` provides the starter stacks the tool builds from (`react_express`, `vite_react`, `vite_react_swagger`, `node_express_mongoose`, `javascript_react`); `core/disk/` and `core/proc/` provide file and process operations, and `core/telemetry/` reports usage events.

Typical control flow: the CLI creates or resumes a project through `StateManager`, the `Orchestrator` runs agents that call LLM providers and act on the workspace, progress is streamed to the selected UI adapter, and state changes are persisted to the database, with telemetry sent on cleanup.

---

## Testing

Testing is handled primarily using `pytest`. Test cases are structured into various subdirectories within the `tests/` folder, allowing for different scopes of verification:

*   **Unit Tests:** Found across directories like `tests/cli/` and `tests/llm/`.
*   **Integration Tests:** Located in `tests/integration/`.
*   **UI Tests:** Found in `tests/ui/`.

Contributors can ensure code quality and verify changes by leveraging the project's test suite, which is supported by pre-commit hooks.

---

## Documentation

A detailed gpt-pilot-phb3a9cx description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./.github/CONTRIBUTING.md)**: To learn more about making a contribution to gpt-pilot-phb3a9cx.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). gpt-pilot-phb3a9cx repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{gpt-pilot-phb3a9cx,

        author = {README Benchmark},

        title = {gpt-pilot-phb3a9cx repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
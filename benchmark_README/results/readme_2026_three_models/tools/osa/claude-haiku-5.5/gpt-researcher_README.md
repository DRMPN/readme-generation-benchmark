# gpt-researcher-xtcoxq1u

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

GPT Researcher is an autonomous research agent that performs online research on a given query and produces a generated report. It is intended primarily for developers and researchers who want to integrate autonomous research into their own Python applications, and end users can reach the same capability through a web interface and a command-line interface. The project offers several usage surfaces: a Python library for programmatic use, a command-line interface for generating reports from the terminal, and a backend server with a web frontend for interactive use. For runnable setup and first-run steps, see the Getting Started section.

---

## Core Features

- **Autonomous online research and report generation:** Runs research on a query and produces a written report, so developers can get a complete research output from a single request.
- **Selectable report depth:** Supports basic, detailed, and deep research report types, so developers can trade off speed against thoroughness.
- **Pluggable retrieval across web and academic sources:** Supports multiple search providers, scrapers, and academic sources such as arXiv, PubMed Central, and Semantic Scholar, so developers can target or swap data sources without changing the overall workflow.
- **Multiple access points:** Available as a Python package, a command-line interface, and a WebSocket server with a web frontend, so developers can integrate it into scripts, terminals, or web applications.

---

## Installation

**Prerequisites:** requires Python >=3.11, <4

Install gpt-researcher-xtcoxq1u using one of the following methods:

**Using PyPi:**

```sh
pip install gpt-researcher
```

---

## Getting Started

### Prerequisites

- Python 3.11 or later, below 4.0 (`requires-python = ">=3.11, <4"` in `pyproject.toml`).
- A local clone of the repository.
- API keys and provider settings for the LLM and search services you plan to use. The required variable names are not confirmed in the provided context.

For dependency installation, see the Installation section. Dependencies are declared in `pyproject.toml`.

### Steps

1. **Install dependencies.** Follow the Installation section. Packaging metadata exists in both `[tool.poetry]` and `[project]` sections of `pyproject.toml`, and the exact install command is not confirmed in this section.
2. **Configure environment variables.** The entry points `main.py` and `cli.py` call `load_dotenv()` from `python-dotenv`, so settings can be read from a `.env` file in the project root. The specific variable names and a `.env` template are not confirmed in the provided context. Check the Configuration documentation before running.
3. **Choose an entry point.** The repository provides these options:
   - `cli.py`: a command-line interface for generating reports. Its usage string and flags are unverified in this section; see `cli.py` directly.
   - `main.py`: its `__main__` block starts a Uvicorn server on port 8000. It imports `backend.server.server`, which may be stale, so verify the import path before relying on it.
   - `deep_research/main.py`: a standalone example with a `__main__` block that runs a sample deep research query.
4. **Run a first execution.** Run one of the entry points above from the repository root. Output is written to the `outputs/` directory when using `cli.py`. Confirm the exact command for your setup before running.

### Other Components

The repository also includes a FastAPI backend (`backend/server/app.py`), a Next.js frontend (`frontend/nextjs`), a Docusaurus docs site (`docs/`), and Docker files (`Dockerfile`, `Dockerfile.fullstack`, `docker-compose.yml`). Run commands for these components are not confirmed in the provided context. Refer to their respective README files or the Installation section.

---

## Architecture

GPT Researcher is organized as a modular Python package with several entry points and supporting components. The exact runtime wiring is only partially visible in the provided context, so the view below is high level.

- **Core library (`gpt_researcher`)**: The `GPTResearcher` class in `gpt_researcher/agent.py` coordinates research. It initializes pluggable components for retrievers, scrapers, LLM providers, memory, and vector store, and delegates work to skill modules such as the researcher, writer, context manager, browser manager, and source curator.
- **Report types (`backend/report_type`)**: Report generation is organized by type, including `basic_report`, `detailed_report`, and `deep_research`. The `deep_research` type uses a dedicated `DeepResearchSkill`.
- **Entry points**: The CLI (`cli.py`) runs `GPTResearcher` or `DetailedReport` directly and writes Markdown output to `outputs/`. A FastAPI server (`backend/server/app.py`) exposes a root route and a `/ws` WebSocket endpoint that passes messages to `ChatAgentWithMemory`.
- **Frontend**: A Next.js application in `frontend/nextjs` provides the web UI. Its interaction with the backend is not detailed in the provided context.
- **Supporting components**: The repository also includes a Docusaurus documentation site (`docs/`), an MCP server (`mcp-server/`), multi-agent modules (`multi_agents/`), and evaluation assets (`evals/`).

Note: The root `main.py` imports `backend.server.server`, while the FastAPI app is defined in `backend/server/app.py`. The provided context does not confirm whether `backend/server/server.py` exists, so the server entry point should be verified before relying on it.

---

## Testing

The repository includes test artifacts under `tests/`, but the exact command to run the test suite is not documented in the provided context.

### Test configuration

- Pytest settings are defined in `pyproject.toml` under `[tool.pytest.ini_options]`:
  - `testpaths = ["tests"]`
  - `python_files = "test_*.py"`
  - `asyncio_mode = "strict"`
  - `asyncio_fixture_loop_scope = "function"`
  - `addopts = "-v"`

### Test files

- Script-style test files that appear to be run manually (not confirmed as automated tests):
  - `tests/test-your-llm.py`
  - `tests/test-your-retriever.py`
- Other files in `tests/` are listed in the repository tree but their contents were not reviewed, so whether they are automated tests is unverified. Examples include `tests/test_logging.py` and `tests/test_mcp.py`.

### Continuous integration

- `.github/workflows` exists, but its contents were not provided. The CI test scope is unverified.

### Contributing

- Before opening a change, check `tests/` and the workflow files in `.github/workflows` to confirm which checks apply to your change.

---

## Examples

Examples of how this should work and how it should be used are available [here](./docs/docs/examples).

---

## Documentation

A detailed gpt-researcher-xtcoxq1u description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to gpt-researcher-xtcoxq1u.

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this software, please cite it as it is written in the [CITATION](./citation.cff) file.

---
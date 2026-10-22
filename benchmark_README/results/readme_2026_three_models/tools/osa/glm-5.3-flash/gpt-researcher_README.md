# gpt-researcher

---

[![PyPi](https://badge.fury.io/py/gpt-researcher.svg)](https://badge.fury.io/py/gpt-researcher)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![arxiv](https://img.shields.io/badge/arXiv-B31B1B.svg?logo=arXiv&logoColor=white)
![fastapi](https://img.shields.io/badge/FastAPI-009688.svg?logo=FastAPI&logoColor=white)
![jinja2](https://img.shields.io/badge/Jinja-B41717.svg?logo=Jinja&logoColor=white)
![markdown](https://img.shields.io/badge/Markdown-000000.svg?logo=Markdown&logoColor=white)
![openai](https://img.shields.io/badge/OpenAI-412991.svg?logo=OpenAI&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?logo=pandas&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?logo=Pydantic&logoColor=white)

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

GPT Researcher is a Python-based autonomous agent that performs comprehensive online research on a given query and generates structured reports. It is aimed at developers embedding research automation into applications, as well as researchers and data scientists automating report generation. The project is usable as an installable Python library, a command-line interface, and a backend service exposing a WebSocket API, with support for multiple report types and pluggable retrieval sources. Newcomers can find runnable setup and usage steps in the Getting Started section.

---

## Core Features

- **Autonomous research and report generation** — Runs end-to-end research on any query and produces multiple report types (summary, detailed, deep research, subtopic), saving developers from manually orchestrating search, scraping, and synthesis.
- **Pluggable retrievers, scrapers, and LLM providers** — Choose from a range of search backends (e.g., Tavily, Bing, Exa, Semantic Scholar, PubMed, arXiv) and LLM providers (OpenAI, Ollama, and more via LiteLLM) to fit your stack and budget.
- **Multiple integration surfaces** — Use the agent as a Python library, a CLI, or through a FastAPI server with WebSocket streaming, so it can be embedded in scripts, apps, or interactive UIs.
- **Local documents and vector store support** — Combine web search with your own documents and vector stores, and restrict queries to specific domains or source URLs for controlled, cited research.
- **MCP tool integration and multi-agent orchestration** — Extend research capabilities with external Model Context Protocol servers and layered agent workflows for more complex tasks.

---

## Installation

**Prerequisites:** requires Python >=3.11, <4

Install gpt-researcher using pip:

```sh
pip install gpt-researcher
```

---

## Getting Started

**Prerequisites**

- Python 3.11 or newer (the project requires Python `>=3.11, <4`)
- API keys for your LLM provider and search retrievers — see `.env.example` for the variables to set

**Steps**

1. Install dependencies:

```shell
pip install -r requirements.txt
```

A trimmed `requirements_minimal.txt` is also provided.

2. Configure your environment:

```shell
cp .env.example .env
```

Edit `.env` and add the API keys for the providers you plan to use. Both `cli.py` and `main.py` load this file automatically via `python-dotenv`.

3. Generate your first report from the CLI:

```shell
python cli.py "Your research question" --report_type research_report
```

- `--report_type` is required. `research_report` produces a short summary (~2 min); `detailed_report` produces an in-depth report (~5 min).
- Optional flags: `--tone` (defaults to `objective`), `--encoding`, and `--query_domains` (comma-separated list of domains to restrict the search).
- The finished report is written to `outputs/<uuid>.md`.

4. Run the web backend (optional):

```shell
python main.py
```

This starts the FastAPI backend with Uvicorn on port 8000 and exposes a WebSocket endpoint at `/ws`.

5. For containerized deployment, the repository also includes `Dockerfile`, `Dockerfile.fullstack`, and `docker-compose.yml`.

---

## Architecture

The repository is a monorepo organized around a modular Python core with several deployment surfaces on top of it.

- **Core library (`gpt_researcher/`)**: The central component is the `GPTResearcher` class (`gpt_researcher/agent.py`), which composes interchangeable skills — `ResearchConductor`, `ReportGenerator`, `ContextManager`, `BrowserManager`, `SourceCurator`, and (for the `deep_research` report type) `DeepResearchSkill` — to plan queries, gather sources, build context, and produce reports. Configuration is handled via `Config` (`gpt_researcher/config/`) with environment-based settings (see `.env.example`).
- **Pluggable retrieval and scraping**: External evidence is gathered through interchangeable retrievers (`gpt_researcher/retrievers/`, including DuckDuckGo, Tavily, Serper, Bing, Google, ArXiv, PubMed Central, Semantic Scholar, SearX, Exa, SearchAPI, and an MCP-based retriever) and scrapers (`gpt_researcher/scraper/`, e.g., BeautifulSoup, PyMuPDF, browser-based, Firecrawl, Tavily extract). Retrievers are selected via `get_retrievers` from headers and config.
- **LLM and context layers**: LLM access is abstracted through `GenericLLMProvider` (`gpt_researcher/llm_provider/`), built on LangChain/LangGraph, OpenAI SDK, and LiteLLM. Context handling includes embedding-based `Memory`, a `VectorStoreWrapper` for vector-store integration, and document processing under `gpt_researcher/context/` and `gpt_researcher/document/`.
- **API backend (`backend/`)**: A FastAPI server (`backend/server/app.py`) exposes a WebSocket endpoint (`/ws`) for streaming research and chat interactions, with a `ChatAgentWithMemory` chat agent. Report type workflows (`basic_report`, `detailed_report`, `deep_research`) live under `backend/report_type/`, with utilities for PDF/markdown output in `backend/utils.py`.
- **Multi-agent orchestration (`multi_agents/`)**: A LangGraph-based layer that coordinates multiple agents for report generation, kept separate from the single-agent core.
- **MCP support**: Model Context Protocol integration spans both the core library (MCP configs and strategies on `GPTResearcher`, `gpt_researcher/mcp/`, `gpt_researcher/retrievers/mcp/`) and a standalone `mcp-server/` package.
- **Client surfaces and deployment**: Multiple entry points consume the core: a CLI (`cli.py`), the FastAPI server (`main.py` runs Uvicorn on port 8000), and web frontends — a Next.js app (`frontend/nextjs/`) and a lightweight static frontend (`frontend/index.html`). Docker artifacts (`Dockerfile`, `Dockerfile.fullstack`, `docker-compose.yml`, `Procfile`) support containerized deployment.

Additional supporting subsystems include an evaluation suite (`evals/simple_evals/`) and a Docusaurus documentation site (`docs/`). The exact details of the CI workflows (`.github/workflows/`) and frontend-to-backend communication beyond the WebSocket endpoint are not visible in the analyzed context.

---

## Testing

The project uses **pytest**, configured in `pyproject.toml` under `[tool.pytest.ini_options]`:

- Test files live in the `tests/` directory (`testpaths = ["tests"]`, `python_files = "test_*.py"`).
- Asyncio mode is `strict`, and the fixture loop scope is set to `function`.
- Verbose output is enabled by default (`addopts = "-v"`).

To run the test suite from the repository root:

```shell
pytest
```

Test scripts in `tests/` cover several areas of the agent.

---

## Examples

Examples of how this should work and how it should be used are available [here](./docs/docs/examples).

---

## Documentation

A detailed gpt-researcher description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to gpt-researcher.

---

## License

This project is protected under the MIT License. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this software, please cite it as it is written in the [CITATION](./citation.cff) file.

---
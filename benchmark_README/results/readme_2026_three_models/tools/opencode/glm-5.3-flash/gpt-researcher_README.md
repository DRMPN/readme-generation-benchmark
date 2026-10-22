# GPT Researcher

GPT Researcher is an autonomous agent designed for comprehensive online research on a variety of tasks.

<!-- 
gpt-researcher: Autonomous LLM agent for comprehensive web research. Python 3.11+, MIT license.
-->

## Overview

GPT Researcher takes a research query, conducts autonomous online research, and generates a detailed report. It is built as a Python package (`gpt_researcher`) and ships with:

- **Core agent library** — The `GPTResearcher` class in `gpt_researcher/agent.py` orchestrates research skills such as `ResearchConductor`, `ReportGenerator`, `ContextManager`, `BrowserManager`, `SourceCurator`, and `DeepResearchSkill`.
- **FastAPI backend** — The `backend/` package exposes a web server (`backend/server/server.py`) that serves the research UI and API.
- **Frontend UI** — A static HTML/JS interface (`frontend/`) and a NextJS application (`frontend/nextjs`).
- **CLI** — A command-line interface (`cli.py`) for generating reports directly from the terminal.
- **Multi-agent pipeline** — A LangGraph-based multi-agent system in `multi_agents/`.
- **MCP server** — A Model Context Protocol server in `mcp-server/` for integrating GPT Researcher with MCP clients.
- **Documentation & examples** — Guides and examples under `docs/`, and evaluation suites under `evals/`.

## Features

- **Autonomous research**: The agent plans, searches, scrapes, and synthesizes information from the web without manual intervention.
- **Multiple report types** (from `gpt_researcher/utils/enum.py`):
  - `research_report` — summary, short and fast (~2 min)
  - `detailed_report` — in-depth, longer (~5 min)
  - `resource_report`, `outline_report`, `custom_report`, `subtopic_report`
  - `deep` — deep research with configurable breadth and depth
- **Multiple report sources**: `web`, `local`, `azure`, `langchain_documents`, `langchain_vectorstore`, `static`, `hybrid`.
- **Tone control**: 16 supported tones including `objective`, `formal`, `analytical`, `persuasive`, `informative`, `explanatory`, `descriptive`, `critical`, `comparative`, `speculative`, `reflective`, `narrative`, `humorous`, `optimistic`, `pessimistic`, `simple`, and `casual`.
- **Customizable LLM providers**: Works with OpenAI, Ollama, LiteLLM, and other LangChain-compatible providers (via `llm_provider`).
- **Multiple retrievers**: Web search via DuckDuckGo, Tavily, and others (see `gpt_researcher/retrievers/`).
- **MCP (Model Context Protocol) support**: Connect to external MCP servers as additional research sources, with `fast`, `deep`, and `disabled` execution strategies.
- **Vector store integration**: Use a LangChain vector store for local/hybrid research (via `gpt_researcher/vector_store/`).
- **Streaming output**: WebSocket support for real-time progress and report streaming.
- **Multiple export formats**: Markdown, PDF, DOCX (via `md2pdf`, `htmldocx`, `python-docx`, `PyMuPDF`).

## Getting Started

### Prerequisites

- Python >= 3.11
- Node.js (v18.17.0 recommended) if using the NextJS frontend
- An OpenAI API key and a Tavily API key (see `.env.example`)

### Installation

Clone the repository:

```bash
git clone https://github.com/assafelovic/gpt-researcher.git
cd gpt-researcher
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, install the package in editable mode with its core dependencies:

```bash
pip install -e .
```

Set up environment variables by copying `.env.example` to `.env` and filling in the values:

```bash
cp .env.example .env
```

Required variables:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for the default LLM provider (OpenAI) |
| `TAVILY_API_KEY` | API key for the Tavily web search retriever |
| `DOC_PATH` | Path to local documents for `local` report source (default: `./my-docs`) |

### Usage

#### 1. Command-Line Interface (CLI)

Run a research report from the terminal:

```bash
python cli.py "<query>" --report_type <report_type> --tone <tone> --query_domains <foo.com,bar.com>
```

Available arguments:

| Argument | Description |
|----------|-------------|
| `query` (positional) | The query to conduct research on |
| `--report_type` | One of: `research_report`, `resource_report`, `outline_report`, `custom_report`, `detailed_report`, `subtopic_report`, `deep` |
| `--tone` | One of the 16 supported tones (default: `objective`) |
| `--encoding` | Encoding for the output file (default: `utf-8`) |
| `--query_domains` | Comma-separated list of domains to restrict search to |

Reports are written to the `outputs/` directory as Markdown files.

#### 2. Python Package

Use `GPTResearcher` directly in your code:

```python
import asyncio
from gpt_researcher import GPTResearcher

async def main():
    query = "What are the latest developments in AI?"
    researcher = GPTResearcher(query=query, report_type="research_report")
    await researcher.conduct_research()
    report = await researcher.write_report()
    print(report)

asyncio.run(main())
```

Key constructor parameters include:

- `query` — the research question
- `report_type` — the report type (see Features)
- `report_source` — source of information (e.g. `web`, `local`, `hybrid`)
- `source_urls` / `document_urls` — restrict research to specific URLs
- `query_domains` — restrict search to specific domains
- `documents` / `vector_store` — LangChain documents or vector store for local research
- `mcp_configs` — list of MCP server configurations
- `mcp_strategy` — `"fast"`, `"deep"`, or `"disabled"`

#### 3. FastAPI Backend

Start the backend server:

```bash
python main.py
```

This runs a Uvicorn server on `http://0.0.0.0:8000`, serving the static frontend and the research API.

#### 4. Frontend

**Static frontend (served by FastAPI):**

Start the backend as above and visit `http://localhost:8000`.

**NextJS frontend:**

```bash
cd frontend/nextjs
npm install --legacy-peer-deps
npm run dev
```

Then visit `http://localhost:3000`. The NextJS frontend requires the backend server running on `localhost:8000`.

#### 5. Docker

Start the backend and frontend together:

```bash
docker-compose up
```

This builds and starts two services:

- `gpt-researcher` — the FastAPI backend on port `8000`
- `gptr-nextjs` — the NextJS frontend on port `3000`

Volumes are mounted for `my-docs`, `outputs`, and `logs`. Additional profiles exist for `test` and `discord` services.

## Architecture

The project is organized into the following main directories:

| Directory | Description |
|-----------|-------------|
| `gpt_researcher/` | Core agent library: research skills, retrievers, scrapers, LLM providers, memory, vector stores, MCP integration |
| `backend/` | FastAPI server, chat endpoints, report-type orchestration (basic and detailed reports) |
| `frontend/` | Static frontend and NextJS application |
| `multi_agents/` | LangGraph-based multi-agent research pipeline |
| `mcp-server/` | MCP server exposing GPT Researcher as a tool |
| `docs/` | Documentation and examples, including a Discord bot |
| `evals/` | Evaluation suite for benchmarking the agent |
| `tests/` | Unit tests (`test_*.py`) |

### Core components

- **`GPTResearcher`** (`gpt_researcher/agent.py`) — the main entry point, coordinating all research skills.
- **`ResearchConductor`** (`gpt_researcher/skills/researcher.py`) — plans and executes research queries.
- **`ReportGenerator`** (`gpt_researcher/skills/writer.py`) — generates introduction, body, and conclusion sections.
- **`ContextManager`** (`gpt_researcher/skills/context_manager.py`) — manages and deduplicates research context.
- **`BrowserManager`** (`gpt_researcher/skills/browser.py`) — handles web scraping and browsing.
- **`SourceCurator`** (`gpt_researcher/skills/curator.py`) — filters and curates sources.
- **`DeepResearchSkill`** (`gpt_researcher/skills/deep_research.py`) — iterative deep research with configurable breadth, depth, and concurrency.

## Configuration

The agent is configured through environment variables and an optional configuration file passed via `config_path`. Key configuration areas include:

- **LLM provider and model** (e.g., `OPENAI_API_KEY`, provider-specific keys)
- **Retrievers** (e.g., `RETRIEVER` environment variable to override the default)
- **Embedding provider and model** for memory and vector stores
- **MCP strategy** (`MCP_STRATEGY` environment variable or `mcp_strategy` parameter)
- **Local document path** (`DOC_PATH`)

See `gpt_researcher/config/` for the full list of supported configuration options.

## Testing

Run the test suite with `pytest`:

```bash
python -m pytest tests/
```

Note that some tests require API keys and a running backend.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to the project.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Citation

If you use GPT Researcher in your work, please cite it using the metadata in [citation.cff](citation.cff).

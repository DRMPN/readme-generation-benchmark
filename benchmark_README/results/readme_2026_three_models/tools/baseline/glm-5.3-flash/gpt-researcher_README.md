# GPT Researcher 🔎

**GPT Researcher is an open deep research agent designed for both web and local research on any given task.**

The agent produces detailed, factual, and unbiased research reports with citations, and provides a full suite of customization options for building tailor-made, domain-specific research agents. Inspired by the [Plan-and-Solve](https://arxiv.org/abs/2305.04091) and [RAG](https://arxiv.org/abs/2005.11401) papers, it addresses misinformation, speed, determinism, and reliability through parallelized agent work — aggregating over 20 web sources per task, with a typical research run taking around three minutes.

- **Repository:** <https://github.com/assafelovic/gpt-researcher>
- **Documentation:** <https://docs.gptr.dev>
- **Website:** <https://gptr.dev>
- **Community:** [Discord](https://discord.gg/QgZXvJAccX)

## Features

- 📝 Generates research reports, outlines, resource reports, subtopic reports, and custom reports
- 📜 Supports long, detailed reports (2K+ words) and recursive **Deep Research**
- 🌐 Aggregates 20+ web sources per research task for objective, factual conclusions
- 🔌 Pluggable retrievers (Tavily, DuckDuckGo, Bing, Google, SearchAPI, Serper, SerpAPI, Searx, Exa, ArXiv, PubMed Central, Semantic Scholar, MCP, custom)
- 🤖 Works with OpenAI by default and other LLM providers (Ollama, Azure OpenAI, and LangChain-compatible models via LiteLLM)
- 📂 Research on local documents, specific URLs, LangChain vector stores, or hybrid web + local sources
- 🖥️ Multiple frontends: vanilla JS, NextJS, React package, npm WebSocket client, and a Discord bot
- 📄 Exports reports to PDF, DOCX, and Markdown
- 🔗 Model Context Protocol (MCP) integration for connecting external tools and data sources

## Architecture

GPT Researcher runs "planner" and "execution" agents: the planner generates an outline of research questions that together form an objective opinion on the task, and executor agents scrape and summarize relevant online resources for each question. Summarized sources are filtered and aggregated into a final research report. The core library lives in `gpt_researcher/`, a FastAPI backend in `backend/` serves the web UI and streaming API, and an optional LangGraph-based multi-agent team lives in `multi_agents/`.

## Getting Started

### Prerequisites

- Python 3.11+ (`requires-python = ">=3.11, <4"`)
- Node.js 18.17 and npm (only for the NextJS frontend)
- API keys: `OPENAI_API_KEY` and `TAVILY_API_KEY` by default (other LLM/retriever providers supported)

### 1. Clone and configure

```bash
git clone https://github.com/assafelovic/gpt-researcher.git
cd gpt-researcher
cp .env.example .env   # add your API keys
```

### 2. Install and run the server

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit <http://localhost:8000> in your browser. You can also use a virtual environment (`python -m venv`) or Poetry (`poetry install`, `poetry shell`).

### 3. Run with Docker

```bash
docker compose up --build
```

This starts the Python API server on **localhost:8000** and the NextJS frontend on **localhost:3000**. The compose file mounts `my-docs/`, `outputs/`, and `logs/` for local documents, generated reports, and logs respectively.

### 4. Or install as a PIP package

```bash
pip install gpt-researcher
```

```python
from gpt_researcher import GPTResearcher
import asyncio

async def main():
    researcher = GPTResearcher(query="What happened in the latest burning man floods?",
                               report_type="research_report")
    await researcher.conduct_research()
    report = await researcher.write_report()
    return report

asyncio.run(main())
```

## Usage

### CLI

```bash
python cli.py "<query>" --report_type research_report --tone objective --query_domains foo.com,bar.com
```

The generated report is written as a Markdown file to `outputs/<uuid>.md`. Report types include `research_report` (summary, ~2 min), `detailed_report` (in-depth, ~5 min), `resource_report`, `outline_report`, `custom_report`, `subtopic_report`, and `deep` (Deep Research). Supported tones: `objective`, `formal`, `analytical`, `persuasive`, `informative`, `explanatory`, `descriptive`, `critical`, `comparative`, `speculative`, `reflective`, `narrative`, `humorous`, `optimistic`, `pessimistic`.

### Report sources

Pass `report_source` when creating a `GPTResearcher` instance to research the **web** (`web`), **local documents** (`local`, with `DOC_PATH=./my-docs`; supports PDF, TXT, CSV, Excel, Markdown, PowerPoint, Word), **hybrid** web + local (`hybrid`), specific URLs (`source_urls`, optionally with `complement_source_urls=True`), LangChain documents/vector stores (`langchain_documents` / `langchain_vectorstore`), or Azure Blob Storage (`azure`).

### Frontends and clients

- **Vanilla JS frontend** — served directly by FastAPI at `localhost:8000`
- **NextJS frontend** (`frontend/nextjs`) — `npm install --legacy-peer-deps` then `npm run dev` on port 3000; requires the backend on `localhost:8000` (override with `NEXT_PUBLIC_GPTR_API_URL`)
- **React package** — `npm install gpt-researcher-ui` embeds the full UI in any React app
- **npm WebSocket client** — `npm install gpt-researcher` connects to the backend's `/ws` WebSocket (HTTP `POST /report/` and `GET /report/{id}` endpoints also available)
- **Embed script** — add two script tags setting `GPTR_API_URL` in localStorage
- **Discord bot** (`docs/discord-bot`) — requires `DISCORD_BOT_TOKEN` and `DISCORD_CLIENT_ID`; run with `docker compose --profile discord run --rm discord-bot`

## Configuration

Defaults live in `gpt_researcher/config/`. Key environment variables include:

| Variable | Description | Default |
|---|---|---|
| `RETRIEVER` | Search engine (`tavily`, `duckduckgo`, `bing`, `google`, `searchapi`, `serper`, `searx`, ...) | `tavily` |
| `EMBEDDING` | Embedding provider (`openai`, `ollama`, `huggingface`, `azure_openai`, `custom`) | `openai:text-embedding-3-small` |
| `FAST_LLM` | Fast operations (summaries) | `openai:gpt-4o-mini` |
| `SMART_LLM` | Report generation and reasoning | `openai:gpt-4.1` |
| `STRATEGIC_LLM` | Planning and strategy | `openai:o4-mini` |
| `SIMILARITY_THRESHOLD` | Document similarity cutoff | `0.42` |
| `LANGUAGE` | Report language | `english` |
| `CURATE_SOURCES` | LLM-based source curation | `False` |
| `DOC_PATH` | Local documents folder | — |

A custom JSON config file can be supplied via the `config_path` parameter. Deep Research parameters: `deep_research_breadth` (default 4), `deep_research_depth` (default 2), `deep_research_concurrency` (default 2), and `reasoning_effort`.

## Multi-Agent Assistant

The `multi_agents/` package uses LangGraph to orchestrate a research team (Chief Editor, GPT Researcher, Editor, Reviewer, Reviser, Writer, Publisher, and human feedback), inspired by the STORM paper. Edit `multi_agents/task.json` to set the query, model, `max_sections`, `publish_formats`, guidelines, and more, then run `python main.py`. For deployment, `pip install langgraph-cli` and `langgraph up`.

## MCP Integration

`gpt_researcher/mcp/` lets the agent connect to external MCP servers (stdio, WebSocket, or HTTP) via `mcp_configs`, using LLM-driven tool selection. A standalone MCP server exposing deep research to assistants like Claude has moved to <https://github.com/assafelovic/gptr-mcp>.

## Development

- **Core library:** `gpt_researcher/` (agent, config, context compression, retrievers, scrapers, skills, vector store)
- **Backend:** `backend/` (FastAPI server, WebSocket manager, chat agent, report types including `basic_report`, `detailed_report`, and `deep_research`)
- **Frontend:** `frontend/` (vanilla JS and NextJS)
- **Docs:** Docusaurus site in `docs/` — install Node.js + Yarn, then `pip install pydoc-markdown`, `cd docs && yarn install`, `pydoc-markdown`, `yarn start`
- **Packaging:** Poetry/uv via `pyproject.toml`, plus `setup.py` and `requirements_minimal.txt`

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow (fork, branch from `master`, test, submit a PR) and the [Code of Conduct](CODE_OF_CONDUCT.md). Bug and feature issue templates and Dependabot configuration are included.

## Testing

Pytest is configured in `pyproject.toml` (`testpaths = ["tests"]`, strict asyncio mode). The `tests/` directory covers research runs, report types, vector stores, document loaders, LLMs, retrievers, embeddings, MCP, and logging.

Run locally:

```bash
pip install pytest pytest-asyncio faiss-cpu
python -m pytest tests/report-types.py
python -m pytest tests/vector-store.py
```

Or via Docker:

```bash
docker compose --profile test run --rm gpt-researcher-tests
```

Continuous testing runs in GitHub Actions; configure a `tests` environment with `OPENAI_API_KEY` and `TAVILY_API_KEY` secrets (workflows for Docker build/push are also included).

## Evaluations

`evals/simple_evals/` contains a SimpleQA-based evaluation framework adapted from OpenAI's simple-evals, measuring short-form factuality with a configurable GPT grader. Run with:

```bash
cd evals/simple_evals
pip install -r requirements.txt
python run_eval.py --num_examples <number>
```

It reports accuracy, F1 score, cost per query, and per-query results with sources; historical runs are tracked in `evals/simple_evals/logs/`.

## Deployment

For Linux servers (recommended: 2 GB RAM, 1 vCPU, 50 GB SSD), the documentation provides a full guide covering Docker installation and an Nginx reverse proxy that routes `/` to the frontend (port 3000) and WebSocket/upload/config routes to the backend (port 8000). The root `Dockerfile` builds a multi-stage image with Chromium, ChromeDriver, Firefox ESR, and Geckodriver, running Uvicorn as a non-root user; `Dockerfile.fullstack` and a `Procfile` are also provided.

## License

This repository is distributed under the terms in the [LICENSE](LICENSE) file, which contains the Apache License 2.0 text. Note that the package metadata in `pyproject.toml` and `setup.py` currently declares MIT.

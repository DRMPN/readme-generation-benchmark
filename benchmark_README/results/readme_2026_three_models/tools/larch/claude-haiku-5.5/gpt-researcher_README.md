# GPT Researcher

> An autonomous AI research agent that plans, searches, scrapes, and synthesizes sourced reports on any topic.

`gpt-researcher-93dm5_53` is a snapshot of the GPT Researcher project. It contains the Python research engine, a FastAPI backend, a LangGraph-based multi-agent system, a Next.js and vanilla JavaScript frontend, an MCP server, a Docusaurus documentation site, evaluation scripts, and a test suite.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Report Types](#report-types)
- [Retrievers (Search Engines)](#retrievers-search-engines)
- [LLM Providers](#llm-providers)
- [Document Ingestion](#document-ingestion)
- [Deep Research Mode](#deep-research-mode)
- [Multi-Agent System](#multi-agent-system)
- [MCP Server](#mcp-server)
- [Frontend Applications](#frontend-applications)
- [Logging](#logging)
- [Evaluation (SimpleQA)](#evaluation-simpleqa)
- [Testing](#testing)
- [Documentation](#documentation)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

GPT Researcher automates the research process that a human analyst would normally perform. Given a question or topic, it:

1. Generates a set of research sub-questions.
2. Searches the web (or other configured sources) for each sub-question.
3. Scrapes and filters the most relevant content.
4. Summarizes and compresses the gathered context.
5. Writes a structured, cited report.

The project can be used as a Python library, a CLI tool, a web application with real-time streaming, a backend for other applications over REST or WebSockets, or as an MCP tool for AI assistants such as Claude Desktop.

---

## Key Features

- **Autonomous research loop**: planner and execution agents decompose a query and iterate on findings.
- **Source-backed reports**: every claim is tied to scraped sources, with a final list of references.
- **Multiple report formats**: summary reports, detailed reports, resource lists, outlines, and custom templates.
- **Pluggable search backends**: Tavily (default), DuckDuckGo, Bing, Google, Serper, SearxNG, SearchApi, SerpApi, Exa, Semantic Scholar, arXiv, PubMed Central, and custom retrievers.
- **Broad LLM support**: OpenAI, Azure OpenAI, Anthropic, Google Gemini, Ollama, and other providers through a unified interface.
- **Local and private document research**: ingest PDFs, Word, CSV, Markdown, and other files, or Azure Blob Storage content, alongside web research.
- **Domain filtering**: restrict or exclude specific domains during search.
- **Deep research**: recursive, tree-style exploration of a topic with breadth and depth controls.
- **Multi-agent workflows**: a LangGraph pipeline with orchestrator, researcher, reviewer, reviser, writer, editor, and publisher roles, with optional human-in-the-loop feedback.
- **Real-time streaming**: WebSocket updates for agent logs, sub-queries, sources, and report content.
- **Multimodal output**: image handling and report export (for example, PDF and DOCX generation).
- **MCP integration**: expose research tools to MCP-compatible clients.
- **Embeddable frontends**: Next.js components, a React package, a vanilla JS frontend, and an embed script.
- **Observability**: structured logging with optional LangSmith tracing.
- **Benchmarking**: a SimpleQA evaluation harness.

---

## How It Works

```
          ┌───────────────┐
  Query → │   Planner     │ → sub-questions
          └───────┬───────┘
                  ▼
          ┌───────────────┐      ┌────────────┐
          │ Execution     │ ───▶ │ Retrievers │ → search results
          │ agents (x N)  │      └─────┬──────┘
          └───────┬───────┘            ▼
                  │             ┌────────────┐
                  │             │  Scrapers  │ → raw pages / docs
                  │             └─────┬──────┘
                  ▼                   ▼
          ┌──────────────────────────────────┐
          │ Filter, embed, compress context  │
          └───────────────┬──────────────────┘
                          ▼
          ┌──────────────────────────────────┐
          │ Writer: draft cited report       │ → Markdown / PDF / DOCX
          └──────────────────────────────────┘
```

1. **Planning**: the LLM produces a research plan and sub-questions.
2. **Retrieval**: each sub-question is sent to one or more search backends.
3. **Scraping**: result pages are fetched with BeautifulSoup, Tavily Extract, Firecrawl, PyMuPDF, or a headless browser (Nodriver).
4. **Context management**: pages are chunked, embedded, and ranked by relevance to keep the prompt within token limits.
5. **Synthesis**: the LLM writes each section from the top-ranked context, then compiles the final report with citations.

---

## Architecture

| Layer | Technology | Purpose |
|---|---|---|
| Core library | Python (`gpt_researcher/`) | Research agent, retrievers, scrapers, LLM abstraction |
| Backend server | FastAPI + WebSockets (`backend/`) | HTTP and streaming API for the frontends |
| Multi-agent system | LangGraph (`multi_agents/`) | Team-based workflows with specialized agents |
| Web frontend | Next.js + TypeScript (`frontend/nextjs/`) | Full-featured research UI |
| Lightweight frontend | HTML/CSS/JS (`frontend/vanilla/`) | Minimal UI without a build step |
| Component library | React/TypeScript (`frontend/nextjs/...`, `package.json`) | Reusable `GPTResearcher` component |
| MCP server | Python (`mcp-server/`) | Tool exposure to AI assistants |
| Documentation | Docusaurus (`docs/`) | Public docs site |
| Evaluation | Python (`evals/`) | SimpleQA benchmark runs |

---

## Repository Structure

The project is organized as follows. Some folder names are inferred from file contents and may differ slightly in the full repository.

```
gpt-researcher/
├── gpt_researcher/              # Core Python package
│   ├── agent.py                 # Main GPTResearcher class
│   ├── config/                  # Configuration loading and defaults
│   ├── llm_provider/            # LLM adapters (OpenAI, Azure, Anthropic, Ollama, ...)
│   ├── retrievers/              # Search backends (tavily, duckduckgo, bing, google, arxiv, ...)
│   ├── scraper/                 # Scrapers (BeautifulSoup, Tavily Extract, Firecrawl, PyMuPDF, Nodriver)
│   ├── document/                # Local and online document loaders (PDF, DOCX, CSV, Azure Blob)
│   ├── memory/                  # Embeddings and vector store support
│   ├── skills/                  # Research skills: researcher, curator, deep_research, writer, browser, context_manager
│   ├── actions/                 # Query processing, web scraping, report generation, markdown processing
│   ├── prompts.py               # Prompt templates
│   ├── utils/                   # Logging, costs, validators, enums, workers
│   └── orchestrator/            # Task orchestration and agent creation
├── backend/                     # FastAPI server
│   ├── server/                  # App, routes, WebSocket manager, server utils, logging config
│   ├── report_type/            # basic_report, detailed_report, deep research endpoints
│   ├── chat/                    # Chat agent functionality
│   └── utils.py
├── multi_agents/                # LangGraph multi-agent workflow
│   ├── agents/                  # orchestrator, researcher, reviewer, reviser, writer, editor, publisher, human
│   ├── main.py                  # Entry point
│   ├── langgraph.json           # LangGraph Studio config
│   └── task.json                # Example task definition
├── mcp-server/                  # MCP server implementation
├── frontend/
│   ├── nextjs/                  # Next.js application
│   ├── vanilla/                 # Static HTML/JS frontend
│   └── gptr-webhook/            # Webhook helper (Node.js)
├── gptr-nextjs / react package  # Embeddable React component (`gpt-researcher-react`)
├── cli.py                       # Command-line interface
├── json_schema_generator.py     # Schema generation for structured output
├── docs/                        # Docusaurus documentation site
├── evals/                       # SimpleQA evaluation (run_eval.py, simpleqa_eval.py)
├── tests/                       # Pytest test suite (logging, MCP, retrievers, embeddings, loaders, LLMs)
├── examples/                    # Example scripts and notebooks
├── Dockerfile                   # Backend image
├── Dockerfile.fullstack         # Combined backend and frontend image
├── docker-compose.yml           # Multi-service local stack
├── requirements.txt             # Core Python dependencies
├── setup.py                     # Package definition (`gpt-researcher`)
├── pyproject.toml               # Build and tooling config
├── citation.cff                 # Citation metadata
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## Requirements

- **Python** 3.11 or later (recommended)
- **Node.js** 18 or later (only for the Next.js frontend, docs, or React package)
- **Docker** and Docker Compose (optional, for containerized deployment)
- **API keys** for at least one LLM provider and one search backend. The default setup uses OpenAI and Tavily.

---

## Installation

### Option 1: Install the Python package

```bash
pip install gpt-researcher
```

### Option 2: Install from source

```bash
git clone https://github.com/assafelovic/gpt-researcher.git
cd gpt-researcher
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Option 3: Docker (full stack)

```bash
git clone https://github.com/assafelovic/gpt-researcher.git
cd gpt-researcher
cp .env.example .env               # then add your API keys
docker compose up --build
```

Once running:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

---

## Configuration

Configuration is handled through environment variables, usually placed in a `.env` file at the project root.

### Minimum configuration

```bash
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

### Common variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | none | OpenAI API key |
| `TAVILY_API_KEY` | none | Tavily search API key |
| `FAST_LLM` | `openai:gpt-4o-mini` | Model for quick tasks such as summarization |
| `SMART_LLM` | `openai:gpt-4.1` | Model for report writing and reasoning |
| `STRATEGIC_LLM` | `openai:o4-mini` | Model for planning and strategy (optional) |
| `EMBEDDING` | `openai:text-embedding-3-small` | Embedding model for context ranking |
| `RETRIEVER` | `tavily` | Search backend (comma-separate for multiple) |
| `MAX_SEARCH_RESULTS_PER_QUERY` | `5` | Results fetched per sub-query |
| `TOTAL_WORDS` | `1200` | Target length of the final report |
| `REPORT_FORMAT` | `APA` | Citation style |
| `LANGUAGE` | `english` | Output language |
| `SCRAPER` | `bs` | Scraper backend |
| `DOC_PATH` | `./my-docs` | Folder for local document research |
| `VERBOSE` | `true` | Enable verbose logging |
| `LANGCHAIN_TRACING_V2` | `false` | Enable LangSmith tracing |
| `LANGCHAIN_API_KEY` | none | LangSmith API key |

> **Note:** Default model names and variable names may change between releases. Check `gpt_researcher/config/` and the official documentation for the version you are using.

### Example `.env`

```bash
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
FAST_LLM=openai:gpt-4o-mini
SMART_LLM=openai:gpt-4.1
RETRIEVER=tavily
EMBEDDING=openai:text-embedding-3-small
DOC_PATH=./my-docs
LANGUAGE=english
```

---

## Usage

### Python library

```python
import asyncio
from gpt_researcher import GPTResearcher

async def main():
    researcher = GPTResearcher(
        query="What are the latest advances in solid-state batteries?",
        report_type="research_report",
    )

    await researcher.conduct_research()    # plan, search, scrape, compress
    report = await researcher.write_report()  # generate the final Markdown report

    print(report)
    print("Sources:", researcher.get_source_urls())
    print("Costs:", researcher.get_costs())

if __name__ == "__main__":
    asyncio.run(main())
```

### Command line

```bash
python cli.py "Impact of microplastics on marine ecosystems" --report_type research_report
```

Typical options include the report type, output path, and tone. Run `python cli.py --help` to see the options for your version.

### Backend API

Start the FastAPI server:

```bash
uvicorn backend.server.server:app --reload --port 8000
```

Interactive API docs are available at http://localhost:8000/docs. The backend exposes:

- REST endpoints for starting research jobs and retrieving reports.
- A WebSocket endpoint that streams agent logs, sub-queries, sources, and report chunks as they are produced.

Example WebSocket message (illustrative):

```json
{
  "task": "Benefits of intermittent fasting",
  "report_type": "research_report",
  "report_source": "web",
  "tone": "Objective",
  "headers": {},
  "source_urls": [],
  "document_urls": [],
  "query_domains": []
}
```

### Working with local documents

```python
researcher = GPTResearcher(
    query="Summarize the key risks in our Q3 financial report",
    report_source="local",          # research only from DOC_PATH
    report_type="research_report",
)
```

Set `report_source` to `web`, `local`, or `hybrid` to control where information is gathered from.

---

## Report Types

| Report type | Description |
|---|---|
| `research_report` | Standard summary report with findings and citations (default) |
| `detailed_report` | Longer, section-by-section report with deeper coverage |
| `resource_report` | Curated list of sources and resources on the topic |
| `outline_report` | Structured outline with headings and key points |
| `custom_report` | Report shaped by a custom prompt or template |
| `subtopic_report` | Report focused on sub-topics identified during planning |
| `deep` | Deep research mode (recursive exploration) |

Pass the type through the `report_type` argument or the API payload.

---

## Retrievers (Search Engines)

Set one or more retrievers in `RETRIEVER`, separated by commas, for example `RETRIEVER=tavily,duckduckgo`. Results from all configured retrievers are merged and deduplicated.

| Retriever | Key | Notes |
|---|---|---|
| Tavily | `tavily` | Default. Requires `TAVILY_API_KEY`. |
| DuckDuckGo | `duckduckgo` | No API key required |
| Bing | `bing` | Requires `BING_API_KEY` |
| Google | `google` | Requires Google Custom Search credentials |
| Serper | `serper` | Requires `SERPER_API_KEY` |
| SerpApi | `serpapi` | Requires `SERPAPI_API_KEY` |
| SearchApi | `searchapi` | Requires `SEARCHAPI_API_KEY` |
| SearxNG | `searx` | Self-hosted metasearch; set `SEARX_URL` |
| Exa | `exa` | Requires `EXA_API_KEY` |
| Semantic Scholar | `semantic_scholar` | Academic papers |
| arXiv | `arxiv` | Preprints |
| PubMed Central | `pubmed_central` | Biomedical literature |
| Custom | `custom` | Bring your own retriever class |

### Domain filtering

Restrict or exclude domains with `query_domains`:

```python
researcher = GPTResearcher(
    query="Recent FDA guidance on AI medical devices",
    query_domains=["fda.gov", "nih.gov"],
)
```

### Custom retriever

Implement a retriever that follows the base retriever interface in `gpt_researcher/retrievers/` and register it by name in `RETRIEVER`.

---

## LLM Providers

Models are specified as `provider:model`. Supported providers include:

- **OpenAI**: `openai:gpt-4.1`, `openai:gpt-4o-mini`
- **Azure OpenAI**: requires the Azure endpoint, key, and deployment name (see `docs/.../running-with-azure.md`)
- **Anthropic**: `anthropic:claude-...`, requires `ANTHROPIC_API_KEY`
- **Google Gemini**: `google_genai:gemini-...`
- **Ollama** (local): `ollama:llama3`, requires a running Ollama server
- **Other OpenAI-compatible endpoints**: set the base URL and key

Use different models for different tasks. A common setup is a cheap model for `FAST_LLM` and a stronger model for `SMART_LLM`, which keeps costs down while preserving report quality.

---

## Document Ingestion

Local document research is supported for:

- PDF (via PyMuPDF)
- Word (`.docx`)
- CSV and Excel
- Markdown and plain text
- Online documents by URL
- Azure Blob Storage (see `azure-storage.md` in the docs)

Place files in `DOC_PATH` or pass URLs through `document_urls`. Documents are chunked and embedded alongside web results.

---

## Deep Research Mode

Deep research explores a topic as a tree. Each level generates follow-up questions, and the process continues to a configured depth and breadth.

```python
researcher = GPTResearcher(
    query="Long-term effects of remote work on urban planning",
    report_type="deep",
)
```

Relevant controls:

- **breadth**: number of parallel branches per level
- **depth**: how many levels to explore

Higher values produce more thorough reports but use more tokens, time, and API calls. Start with low values when testing.

---

## Multi-Agent System

The `multi_agents/` package implements a LangGraph workflow that splits research among specialized agents:

| Agent | Role |
|---|---|
| Orchestrator | Plans the work and assigns tasks |
| Researcher | Gathers information for each section |
| Reviewer | Checks draft sections for quality and coverage |
| Reviser | Revises sections based on review feedback |
| Writer | Produces the full draft |
| Editor | Polishes structure and consistency |
| Publisher | Exports the final output (Markdown, PDF, DOCX) |
| Human | Optional human-in-the-loop checkpoint for feedback |

Run the workflow:

```bash
cd multi_agents
pip install -r requirements.txt
python main.py
```

To use LangGraph Studio for visual debugging:

```bash
langgraph dev
```

The task definition (topic, sections, and options) is in `task.json`.

---

## MCP Server

The `mcp-server/` directory exposes GPT Researcher as tools for MCP-compatible clients, such as Claude Desktop or other AI assistants.

Typical setup:

```bash
cd mcp-server
pip install -r requirements.txt
python server.py
```

Then add the server to your client's MCP configuration. Example for Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "gpt-researcher": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-server/server.py"],
      "env": {
        "OPENAI_API_KEY": "your_key",
        "TAVILY_API_KEY": "your_key"
      }
    }
  }
}
```

MCP tests are in `tests/test_mcp.py`.

---

## Frontend Applications

### Next.js app (`frontend/nextjs/`)

The primary web interface. It includes:

- A research form with tone, report type, and source selection
- A live agent log panel
- Source cards and images
- Report viewer with export
- Research history (stored locally)
- Chat and human-feedback components

```bash
cd frontend/nextjs
npm install
npm run dev        # http://localhost:3000
```

### Vanilla JS frontend (`frontend/vanilla/`)

A static HTML, CSS, and JavaScript client that connects to the backend over WebSockets. Serve it with any static server or open `index.html` after starting the backend.

### React package

A reusable component for embedding GPT Researcher in other React applications:

```bash
npm install gpt-researcher-react
```

```jsx
import GPTResearcher from "gpt-researcher-react";

export default function App() {
  return <GPTResearcher backendUrl="http://localhost:8000" />;
}
```

### Embed script

For websites that cannot use React, the embed script (`embed.js`) mounts the research UI into any page with a single script tag.

### Webhook helper (`gptr-webhook`)

A Node.js service that forwards research results to external systems. It can be used with chat integrations such as Discord bots.

---

## Logging

Logging is configured in `gpt_researcher/utils/logging_config.py` and `backend/server/logging_config.py`.

- Logs are emitted as structured records, including agent events and tool calls.
- The WebSocket handler streams logs to the frontend in real time.
- Set `VERBOSE=true` for detailed output.
- Enable LangSmith tracing with `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY`.

Logging tests are in `tests/test_logs.py`, `tests/test_logging.py`, `tests/test_logging_output.py`, and `tests/test_researcher_logging.py`.

---

## Evaluation (SimpleQA)

The `evals/` directory benchmarks report accuracy using the SimpleQA question set.

- `Simple QA Test Set.csv`: the question and answer dataset
- `simpleqa_eval.py`: grading logic
- `run_eval.py`: runs the researcher against the dataset and produces scores

```bash
cd evals
python run_eval.py
```

Evaluation makes many LLM and search calls, so expect meaningful API costs. Start with a small subset of questions.

---

## Testing

The test suite uses pytest.

```bash
pip install -r requirements.txt
pytest tests/
```

Test coverage includes:

| Test file | Area |
|---|---|
| `test-your-llm.py`, `test-openai-llm.py` | LLM connectivity |
| `test-your-retriever.py` | Search backends |
| `test-your-embeddings.py` | Embedding providers |
| `test-loaders.py` | Document loaders |
| `vector-store.py` | Vector store operations |
| `research_test.py` | End-to-end research flow |
| `report-types.py` | Report type generation |
| `test_mcp.py` | MCP server |
| `test_logs.py`, `test_logging*.py` | Logging behavior |
| `gptr-logs-handler.py` | Log handler |

Some tests call live APIs and require valid keys. Use mocks or skip markers for offline runs.

---

## Documentation

The full documentation lives in `docs/`, built with Docusaurus.

```bash
cd docs
npm install
npm run start      # local dev server
npm run build      # production build
```

Major topics include:

- Getting started and pip package usage
- Running with Docker, Ollama, and Azure
- Choosing LLMs and search engines
- Data ingestion and local documents
- Deep research and multi-agent workflows
- Frontend integrations (Next.js, React, vanilla JS, Discord bot)
- MCP configuration
- Logs, LangSmith, and troubleshooting
- Roadmap and FAQ

---

## Deployment

### Docker Compose

```bash
docker compose up -d --build
```

### Single-container full stack

```bash
docker build -f Dockerfile.fullstack -t gpt-researcher-fullstack .
docker run -p 3000:3000 -p 8000:8000 --env-file .env gpt-researcher-fullstack
```

### Backend only

```bash
docker build -f Dockerfile -t gpt-researcher-backend .
docker run -p 8000:8000 --env-file .env gpt-researcher-backend
```

### Linux server

Systemd and reverse-proxy (Nginx) deployment guides are available in the docs under `linux-deployment.md`. Keep API keys in environment variables or a secrets manager, never in source control.

### Cloud platforms

The repository includes a `Procfile` and deployment notes for platforms that support Procfile-based process definitions.

---

## Troubleshooting

| Problem | Possible cause and fix |
|---|---|
| `AuthenticationError` from the LLM | Check the provider key in `.env` and confirm the variable name matches the provider. |
| No search results | Confirm `RETRIEVER` is set and its API key is valid. Try `duckduckgo` as a keyless fallback. |
| Empty or short reports | Increase `MAX_SEARCH_RESULTS_PER_QUERY` or `TOTAL_WORDS`, or switch to a stronger `SMART_LLM`. |
| Scraping failures | Some sites block scrapers. Try another `SCRAPER` backend, or enable the headless browser option. |
| Frontend cannot reach backend | Verify the backend is on port 8000 and that the frontend's backend URL and CORS settings match. |
| Docker containers exit immediately | Run `docker compose logs` to inspect errors, usually a missing `.env` entry. |
| High costs | Use a cheaper `FAST_LLM`, reduce deep-research breadth and depth, and limit results per query. |
| Ollama models not responding | Confirm the Ollama server is running and the model is pulled (`ollama pull <model>`). |

For more help, see the FAQ in the docs or open an issue on GitHub.

---

## Contributing

Contributions are welcome. To get started:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
2. Fork the repository and create a feature branch.
3. Install dependencies and run the test suite.
4. Submit a pull request with a clear description and tests for new behavior.

Good first contributions include adding a retriever, adding a document loader, improving docs, and extending the evaluation set.

---

## Citation

If you use GPT Researcher in academic work, please cite it using the metadata in [citation.cff](citation.cff).

---

## License

This project is distributed under the license in [LICENSE](LICENSE). Review it before using or redistributing the code.

---

## Acknowledgments

GPT Researcher builds on several open-source projects, including LangChain, LangGraph, FastAPI, Next.js, Docusaurus, and many search and scraping libraries. Thanks to all contributors.

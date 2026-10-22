# README

<div align="center">
  <img src="docs/static/gptr-logo.png" alt="GPT Researcher Logo" width="140"/>
  <h3>GPT Researcher</h3>
  <p><b>An Autonomous Agent for Comprehensive Online Research</b><br/>
  Generate detailed, factual, and unbiased research reports with citations — on any topic, in seconds.</p>
</div>

<p align="center">
  <img src="https://img.shields.io/pypi/v/gpt-researcher" alt="PyPI"/>
  <img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="Python"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License"/>
  <img src="https://img.shields.io/badge/docker-supported-blue" alt="Docker"/>
  <img src="https://img.shields.io/badge/LLM-agentic-orange" alt="LLM"/>
</p>

<p align="center">
  <img src="docs/static/banner1.jpg" alt="GPT Researcher Banner"/>
</p>

---

## Table of Contents

- [What is GPT Researcher?](#what-is-gpt-researcher)
- [Features](#features)
- [Why GPT Researcher?](#why-gpt-researcher)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Report Types](#report-types)
- [Local Documents & Vector Stores](#local-documents--vector-stores)
- [Multi-Agent Team (LangGraph)](#multi-agent-team-langgraph)
- [MCP Integration](#mcp-integration)
- [Web Frontend](#web-frontend)
- [Discord Bot](#discord-bot)
- [Logging & Observability](#logging--observability)
- [Testing & Evaluation](#testing--evaluation)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)

---

## What is GPT Researcher?

**GPT Researcher** is an open-source autonomous agent designed for comprehensive web- and local-based research on any given task. It plans, searches, scrapes, curates, and writes — producing **detailed, factual, and unbiased research reports with citations**, while offering extensive customization for both business and consumer applications.

GPT Researcher can:

- 📝 Generate research reports, summaries, and in-depth detailed reports
- 🔍 Search and scrape 20+ web sources per query in parallel
- 🧠 Work with virtually any LLM provider
- 🗂️ Research your **local documents** (PDF, DOCX, TXT, ...) and vector stores
- 💬 Chat with the results, export to PDF/DOCX/Markdown, and more

## Features

| | |
|---|---|
| 🔎 **20+ Retrievers** | Tavily, Google, Bing, DuckDuckGo, Serper, SerpAPI, SearchAPI, Searx, Exa, arXiv, Semantic Scholar, PubMed Central, and custom retrievers |
| 🧠 **Any LLM** | OpenAI, Azure OpenAI, Ollama, LiteLLM (Anthropic, Gemini, Groq, Mistral, and more) |
| 🌐 **Multiple Scrapers** | BeautifulSoup, PyMuPDF, WebBaseLoader, Firecrawl, Tavily Extract, NodeDriver (headless), custom scrapers |
| 📄 **Multiple Report Types** | Research report, detailed (in-depth) report, basic summary, and more |
| 🤝 **Multi-Agent Mode** | A LangGraph-orchestrated research "team": Researcher, Writer, Reviewer, Reviser, Editor, Publisher |
| 🖥️ **Beautiful Web UI** | Next.js frontend with live WebSocket streaming, chat, sources, images, and settings |
| 📦 **Embeddable Widget** | React + vanilla JS packages to embed the researcher into any site |
| 🔌 **MCP Support** | Connect external tools via the Model Context Protocol |
| 🤖 **Discord Bot** | Run research tasks directly from Discord |
| 📊 **Observability** | Structured logging + LangSmith / LangGraph tracing |
| 🧪 **Evaluation Harness** | SimpleQA benchmark (100 problems) for factual accuracy |
| 🚀 **Easy Deployment** | Docker, Docker Compose, Heroku (`Procfile`), Linux, Vercel |

## Why GPT Researcher?

Producing real, factual, and unbiased research reports is notoriously hard for LLMs, which suffer from three major problems when used naively:

1. **Misinformation** — relying on a single source or a fixed training snapshot
2. **Timeliness** — knowledge cutoffs make results outdated for fast-moving topics
3. **Hallucination** — one-shot generation from parametric memory leads to fabricated facts and shallow, one-sided reports

GPT Researcher was built to solve these problems. Inspired by recent work on **Plan-and-Solve** and **RAG** ("Retrieval Augmented Generation"), it adopts a **plan-and-execute** architecture: it plans an outline of research questions, then runs retrievers and scrapers **in parallel** to gather, filter, and synthesize facts from many sources — resulting in faster, cheaper, and more reliable research.

<p align="center">
  <img src="docs/static/architecture.png" alt="GPT Researcher Architecture" width="700"/>
</p>

## How It Works

At a high level, the agent runs the following pipeline:

1. **Plan** — Generate an outline and a set of research questions derived from the task.
2. **Retrieve** — Trigger the configured retrievers (Tavily, Google, Bing, etc.) concurrently for each question.
3. **Scrape** — Fetch and extract clean content from the resulting URLs using the configured scrapers.
4. **Curate** — Deduplicate (via embedding similarity), filter for relevance, and compress raw content into a research context.
5. **Iterate** — Optionally recurse for breadth/depth ("deep research" mode) until the context is sufficient.
6. **Write** — Generate the final report with citations in the requested format, tone, and length.

The core logic lives in `gpt_researcher/agent.py` (`GPTResearcher`) and the research skills (`gpt_researcher/skills/`).

## Project Structure

```text
gpt-researcher/
├── gpt_researcher/          # Core Python package (pip install gpt-researcher)
│   ├── agent.py             # GPTResearcher — the main agent class
│   ├── config/              # Defaults, validators, LLM registry
│   ├── actions/             # Query processing, retrieval, scraping, report generation
│   ├── context/             # Context management & compression
│   ├── memory/              # Embeddings
│   ├── skills/              # Research skills (deep research, browsing, writing, curation)
│   ├── retrievers/          # Search integrations (tavily, google, bing, exa, arxiv, ...)
│   ├── scraper/             # Scrapers (beautiful_soup, pymupdf, firecrawl, nodriver, ...)
│   ├── docs/                # Document loaders (local, online, Azure)
│   ├── vector_store/        # Vector store support
│   └── llm_provider/        # LLM providers & cost tracking
├── backend/                 # FastAPI server (WebSocket manager, chat, logging)
├── frontend/
│   ├── nextjs/              # Next.js web application
│   └── embed/               # Embeddable React widget
├── multi_agents/            # LangGraph multi-agent team & orchestrator
├── examples/                # Example scripts, notebooks & custom prompts
├── eval/                    # SimpleQA evaluation harness
├── discord_bot/             # Discord integration (Node.js)
├── docs/                    # Docusaurus documentation site
├── test/                    # Tests & validation scripts
├── cli.py                   # Command-line interface
├── docker-compose.yml       # Full-stack deployment
├── Dockerfile / Dockerfile.fullstack / Dockerfile.dev
└── requirements.txt
```

## Quickstart

### Prerequisites

- Python **3.11+** (or Docker)
- API keys for your LLM provider and retriever (see [Configuration](#configuration))

### Option A — Python Package (PIP)

```bash
pip install gpt-researcher
```

```python
import asyncio
from gpt_researcher import GPTResearcher

async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query=query, report_type=report_type)
    report = await researcher.conduct_research()
    return report

if __name__ == "__main__":
    query = "What are the latest breakthroughs in quantum computing?"
    report_type = "research_report"
    report = asyncio.run(get_report(query, report_type))
    print(report)
```

More examples — detailed reports, custom prompts, sources-only output, vector stores — can be found in the [`examples/`](examples/) directory (`basic_report.py`, `detailed_report.py`, `report-types.py`, `custom_prompt.py`, `vector-store.py`, ...).

### Option B — Command Line

```bash
gpt-researcher "What are the latest advancements in renewable energy?"
```

### Option C — Docker

```bash
export OPENAI_API_KEY=sk-...      # or your preferred LLM key
export TAVILY_API_KEY=tvly-...    # default retriever

docker-compose up --build
```

- Web UI: **http://localhost:3000**
- Backend API: **http://localhost:8000**

Variants: `Dockerfile` (backend), `Dockerfile.fullstack` (backend + frontend), `Dockerfile.dev` (development). A `Procfile` is included for Heroku-style deployments.

### Option D — Run from Source

**1. Start the backend (FastAPI):**

```bash
pip install -r requirements.txt
uvicorn backend.server:app --reload --port 8000
```

**2. Start the frontend (Next.js):**

```bash
cd frontend/nextjs
npm install --legacy-peer-deps
npm run dev
```

Open **http://localhost:3000** and start researching. The UI streams agent logs, sources, images, and the final report over WebSockets — see the *Querying the Backend* guide in the docs for raw API/WebSocket usage.

## Configuration

GPT Researcher is configured via **environment variables** (or a custom config file). The most important ones:

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | ✅* | — | API key for OpenAI (default LLM provider) |
| `TAVILY_API_KEY` | ✅* | — | API key for Tavily (default retriever) |
| `RETRIEVER` | ❌ | `tavily` | Retriever(s), e.g. `google`, `bing`, `duckduckgo`, `serper`, `serpapi`, `searchapi`, `searx`, `exa`, `arxiv`, `semantic_scholar`, `pubmed_central`, `custom` (comma-separated for hybrid) |
| `LLM_PROVIDER` | ❌ | `openai` | LLM provider (`openai`, `azure`, `ollama`, `litellm`, ...) |
| `FAST_LLM` | ❌ | `openai:gpt-4o-mini` | Cheap/fast LLM for summarization & browsing |
| `SMART_LLM` | ❌ | `openai:gpt-4o` | High-quality LLM for report writing |
| `STRATEGIC_LLM` | ❌ | `openai:gpt-4o` | LLM for planning & strategy |
| `EMBEDDING_PROVIDER` | ❌ | `openai` | Embeddings provider (`openai`, `ollama`, `huggingface`) |
| `SCRAPER` | ❌ | `bs` | Scraper(s): `bs`, `pymupdf`, `web_base_loader`, `firecrawl`, `tavily_extract`, `nodriver` |
| `MAX_SEARCH_RESULTS_PER_QUERY` | ❌ | `10` | Search results fetched per query |
| `SIMILARITY_THRESHOLD` | ❌ | `0.42` | Similarity threshold for content deduplication |
| `MAX_ITERATIONS` | ❌ | `3` | Max research iterations per query |
| `TOTAL_WORDS` | ❌ | `1200` | Target report word count |
| `REPORT_FORMAT` | ❌ | `APA` | Citation format |
| `LANGCHAIN_API_KEY` | ❌ | — | LangSmith API key for tracing |

\* Required when using the defaults. Any OpenAI-compatible endpoint (including fully local setups via [Ollama](docs/docs/running-with-ollama.md)) can be used instead — see *Supported LLMs* and *Running with Azure / Ollama* in the docs.

**Retriever credentials** (set only what you use):

| Retriever | Env Vars |
|---|---|
| Tavily *(default)* | `TAVILY_API_KEY` |
| Google | `GOOGLE_API_KEY`, `GOOGLE_CX` |
| Bing | `BING_API_KEY` |
| Serper / SerpAPI / SearchAPI | `SERPER_API_KEY` / `SERPAPI_API_KEY` / `SEARCHAPI_API_KEY` |
| Searx | `SEARX_URL` |
| Exa | `EXA_API_KEY` |
| Semantic Scholar | `SEMANTIC_SCHOLAR_API_KEY` |
| arXiv / PubMed Central / DuckDuckGo | — (no key required) |
| Custom | Provide your own retriever class (`custom`) |

**Sanity-check your setup** with the bundled test scripts:

```bash
python test-your-llm.py          # verify your LLM works
python test-your-embeddings.py   # verify embeddings
python test-your-retriever.py    # verify web search
```

## Report Types

Pass `report_type` to the agent to control the output style:

| Report Type | Description |
|---|---|
| `research_report` | *(Default)* Classic, short & detailed report (~2 pages) with citations |
| `detailed_report` | In-depth report (~5–10 pages) that iteratively researches subtopics |
| `basic_report` | Quick, high-level summary |
| `outline_report` | Structured outline of the topic |
| `resource_report` | Curated list of sources and resources |

Try them all with [`examples/report-types.py`](examples/report-types.py). You can also customize prompts (tone, structure, language) via `custom_prompt` and the tone selector in the UI.

## Local Documents & Vector Stores

GPT Researcher isn't limited to the web — it can research **your own documents** and hybrid combinations:

```python
researcher = GPTResearcher(query="Summarize the key findings", report_type="research_report")

# Point the agent at local files / URLs / vector stores
await researcher.conduct_research()
```

- Document loaders: `PDF`, `DOCX`, `TXT`, `Markdown`, online docs, and Azure document storage (`gpt_researcher/docs/`)
- Vector store integration (`gpt_researcher/vector_store/`)
- Ready-made scripts: [`examples/documents-report-source.py`](examples/documents-report-source.py), [`examples/vector-store.py`](examples/vector-store.py)
- Guides: *Local Docs*, *Vector Stores*, and *Filtering by Domain* in the documentation

## Multi-Agent Team (LangGraph)

The `multi_agents/` package implements a full editorial research team orchestrated with **LangGraph**:

```
Planner → Researcher → Reviewer ⇄ Reviser → Writer → Publisher
                         ↑
                     Human (in-the-loop)
```

- **Researcher** — gathers sources and drafts content
- **Reviewer** — critiques the draft
- **Reviser** — improves it based on review notes
- **Writer / Editor** — structures and polishes the report
- **Publisher** — exports the final document (PDF, DOCX, Markdown)
- **Human** — optional approval gate before publishing

Run it standalone (uses `langgraph.json` + `task.json`):

```bash
cd multi_agents
pip install -r requirements.txt
python main.py
```

Or plug it into the web UI. Outputs land in `multi_agents/outputs/`.

<p align="center">
  <img src="docs/static/multi-agent.png" alt="Multi-agent architecture" width="600"/>
</p>

## MCP Integration

GPT Researcher supports the **Model Context Protocol (MCP)**, allowing the agent to call external MCP servers as research tools. Configuration examples are in [`docs/docs/mcp-configs.mdx`](docs/docs/mcp-configs.mdx), and a working example lives in `test_mcp.py`.

## Web Frontend

The bundled Next.js application (`frontend/nextjs/`) provides a polished research experience:

- 🧭 Research form: task input, report type, tone, domain filters, MCP tool selection
- 📡 Live **agent logs** and progress streamed over WebSockets
- 📚 **Sources** panel and source cards for every claim
- 🖼️ Auto-collected **images** and albums
- 💬 **Chat** with the completed report
- 🧑‍⚖️ **Human feedback** loop and **similar topics** suggestions
- 🕘 Research **history** and report export/share
- ⚙️ Settings modal for runtime configuration

A lightweight **vanilla JS** frontend and an **embeddable React widget** (`frontend/embed/`) are also included — see *Vanilla JS Frontend*, *React Package*, and *Embed Script* in the docs.

## Discord Bot

Run research straight from Discord with the bundled Node.js bot:

```bash
cd discord_bot
npm install
node deploy-commands.js   # register slash commands
node index.js             # start the bot
```

Setup steps (app registration, permissions, OAuth2 invite URL) are documented in *Discord Bot* under the docs, with the webhook helper (`gptr-webhook.js`) for posting reports to channels.

## Logging & Observability

- Built-in **structured logging** with configurable levels (`gpt_researcher/logging_config.py`, `backend/logging_config.py`)
- **LangSmith / LangGraph tracing** support for full run visibility — set `LANGCHAIN_API_KEY` / `LANGCHAIN_TRACING_V2` (see the *LangSmith Logs* guide)
- Log-handler utilities (`gptr-logs-handler.py`) and dedicated test scripts for logging pipelines

## Testing & Evaluation

**Validation scripts** help you verify your configuration end-to-end:

```bash
python test-your-llm.py
python test-your-embeddings.py
python test-your-retriever.py
python test-loaders.py
python test_mcp.py
```

**Benchmark** — the `eval/` directory ships a **SimpleQA** harness (`run_eval.py`, `simpleqa_eval.py`, 100-problem test set) to measure the agent's factual accuracy and citation quality:

```bash
cd eval
python run_eval.py
```

## Documentation

The full documentation site (built with **Docusaurus**) lives in [`docs/`](docs/) and covers everything in depth:

- Getting started (PIP, Docker, source) & Linux deployment
- Supported LLMs, retrievers, and search engines
- Configuration reference & troubleshooting
- Deep research, tailored research, hybrid research
- Vector stores, local docs, data ingestion
- Querying the backend, WebSockets, visualizing logs
- MCP configs, CLI, npm & pip packages, automated tests

Run it locally:

```bash
cd docs
npm install
npm start
```

## Contributing

Contributions are welcome and appreciated! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) and the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) before opening issues or pull requests. Good first contributions include new retrievers, scrapers, report types, and documentation improvements.

## Citation

If you use GPT Researcher in your research or project, please cite it (see [`citation.cff`](citation.cff)):

```bibtex
@software{gpt_researcher,
  title  = {GPT Researcher: An Autonomous Agent for Comprehensive Online Research},
  author = {Elovic, Assaf and contributors},
  year   = {2023},
  url    = {https://github.com/assafelovic/gpt-researcher},
  license = {MIT}
}
```

## License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

<div align="center">
  <sub>Built with ❤️ for faster, better, and more reliable research.</sub>
</div>

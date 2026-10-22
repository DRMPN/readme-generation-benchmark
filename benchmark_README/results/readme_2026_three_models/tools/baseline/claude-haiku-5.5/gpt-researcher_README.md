# GPT Researcher

GPT Researcher is an autonomous research agent for comprehensive online research on a variety of tasks. It is an open-source project, and its Python package, backend server, CLI, frontends, and multi-agent workflow are all in this repository.

## Overview

The project packages several ways to run research:

- **Python package** (`gpt_researcher/`): The `GPTResearcher` class plans research questions, retrieves and scrapes sources, and writes a report. The package is published as `gpt-researcher` and is configured in `pyproject.toml` and `setup.py`.
- **FastAPI backend** (`main.py`, `backend/`): Serves the application on port 8000 and exposes a WebSocket endpoint at `/ws`. `backend/report_type/` contains the detailed report and deep research flows.
- **CLI** (`cli.py`): Generates a report from a query and writes it to the `outputs/` directory.
- **Frontends** (`frontend/`): A static HTML/JavaScript frontend served by FastAPI, and a Next.js frontend (`frontend/nextjs/`) that can also be published as a React component package (`gpt-researcher-ui`).
- **Multi-agent system** (`multi_agents/`): A LangGraph-based team of agents (Human, Chief Editor, Researcher, Editor, Reviewer, Reviser, Writer, Publisher) that produces reports in multiple formats.
- **Client packages** (`docs/npm/`): A Node.js WebSocket client published as `gpt-researcher`.
- **Documentation site** (`docs/`): A Docusaurus site with guides, examples, and blog posts.
- **Evaluations** (`evals/`): A SimpleQA-based evaluation harness.

The core package's research loop, as described in the project documentation, generates research questions for a task, runs an agent for each question in parallel, summarizes relevant sources, and aggregates the results into a final report.

Supported report types from the CLI and documentation include `research_report`, `detailed_report`, `resource_report`, `outline_report`, `custom_report`, `subtopic_report`, and `deep` (Deep Research).

## Setup

### Requirements

- Python 3.11 or later (`requires-python = ">=3.11, <4"`)
- pip, or Poetry for the `pyproject.toml` workflow
- API keys for your chosen LLM and search provider. The default configuration uses OpenAI for LLM calls and Tavily for web search.
- Node.js 18.17.0 (recommended) and npm, only if you run the Next.js frontend without Docker

### Clone and configure

```bash
git clone https://github.com/assafelovic/gpt-researcher.git
cd gpt-researcher
cp .env.example .env
```

Edit `.env` (or export variables in your shell) with your keys:

```bash
OPENAI_API_KEY={Your OpenAI API Key here}
TAVILY_API_KEY={Your Tavily API Key here}
```

### Install dependencies

With pip:

```bash
pip install -r requirements.txt
```

Or with a virtual environment:

```bash
python -m venv env
# Windows PowerShell/CMD
.\env\Scripts\activate
python -m pip install -r requirements.txt
```

Or with Poetry:

```bash
poetry install
poetry shell
```

`requirements_minimal.txt` is also included, and `multi_agents/requirements.txt` lists the extra dependencies for the multi-agent workflow.

### Run with Docker

Docker Compose is defined in `docker-compose.yml`:

```bash
docker-compose up --build
```

This starts:

- `gpt-researcher` on port **8000** (the API server)
- `gptr-nextjs` on port **3000** (the Next.js frontend)

The `gpt-researcher-tests` service runs only with the `test` profile, and `discord-bot` runs only with the `discord` profile (port 3001).

You can also run the API image directly:

```bash
docker run -it --name gpt-researcher -p 8000:8000 --env-file .env -v /absolute/path/to/gptr_docs:/my-docs gpt-researcher
```

The Dockerfile builds on a Python 3.11 slim base image, installs Chromium, ChromeDriver, Firefox ESR, and Geckodriver, and runs the app as a non-root `gpt-researcher` user. It uses the `HOST`, `PORT` (default 8000), and `WORKERS` (default 1) build arguments.

## Usage

### Start the server

```bash
python -m uvicorn main:app --reload
```

Then open `http://localhost:8000`. The root endpoint returns a welcome message, and the WebSocket endpoint is `/ws`.

### Python package

```python
from gpt_researcher import GPTResearcher
import asyncio

async def main():
    researcher = GPTResearcher(
        query="What happened in the latest burning man floods?",
        report_type="research_report",
    )
    await researcher.conduct_research()
    report = await researcher.write_report()
    print(report)

if __name__ == "__main__":
    asyncio.run(main())
```

Other documented options include `source_urls` with `complement_source_urls`, `report_source` values such as `web`, `local`, `hybrid`, `static`, and `langchain_vectorstore`, and `vector_store`. Deep research is enabled with `report_type="deep"`.

### Command-line interface

```bash
python cli.py "<query>" --report_type <report_type> --tone <tone> --query_domains <foo.com,bar.com>
```

- `query` (required): the research question.
- `--report_type` (required): one of the report types listed above.
- `--tone` (optional, default `objective`): choices include `objective`, `formal`, `analytical`, `persuasive`, `informative`, `explanatory`, `descriptive`, `critical`, `comparative`, `speculative`, `reflective`, `narrative`, `humorous`, `optimistic`, and `pessimistic`.
- `--query_domains` (optional): a comma-separated list of domains to search.
- `--encoding` (optional, default `utf-8`): the output file encoding.

The report is written to `outputs/<uuid>.md`. Selecting `detailed_report` runs the `DetailedReport` class instead of `GPTResearcher`.

### Local documents

Set `DOC_PATH` to a folder of documents, then use `report_source="local"` (or `"hybrid"` to combine local and web sources). The documented supported formats are PDF, plain text, CSV, Excel, Markdown, PowerPoint, and Word. The `docker-compose.yml` file mounts `./my-docs` into the container.

### Multi-agent workflow

The workflow in `multi_agents/` is configured with `multi_agents/task.json`. Its documented fields are:

- `query`: the research task
- `model`: the model used by the agents
- `max_sections`: the maximum number of report sections
- `include_human_feedback`: whether a user can give feedback
- `publish_formats`: `markdown`, `pdf`, and/or `docx`
- `source`: `web` or `local`
- `follow_guidelines` and `guidelines`: report rules
- `verbose`: detailed console logging

Set `STRATEGIC_LLM` in the environment to override the model. Run the workflow with `python main.py` from the `multi_agents` directory, as described in `multi_agents/README.md`.

### Frontends

- **Static frontend:** Served by FastAPI at `http://localhost:8000`.
- **Next.js frontend:** Run with Docker, or from `frontend/nextjs` with `npm install --legacy-peer-deps` and `npm run dev`, at `http://localhost:3000`. It needs the backend on `localhost:8000`. Set `NEXT_PUBLIC_GPTR_API_URL` to point to a different backend.
- **npm client:** `npm install gpt-researcher` provides a WebSocket client that connects to `ws://<host>/ws`.
- **React package:** `npm install gpt-researcher-ui` provides a `GPTResearcher` component that accepts `apiUrl` and `defaultPrompt` props.

### Model Context Protocol (MCP)

MCP integration code lives in `gpt_researcher/mcp/`. The `mcp-server/` directory states that its content has moved to the separate `gptr-mcp` repository.

## Configuration

### Environment variables

Copy `.env.example` to `.env`. The repository references these variables:

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | OpenAI LLM access |
| `TAVILY_API_KEY` | Tavily web search |
| `LANGCHAIN_API_KEY` | LangSmith tracing (enables `LANGCHAIN_TRACING_V2` in the multi-agent code) |
| `LOGGING_LEVEL` | Logging level (`INFO` in `docker-compose.yml`) |
| `DOC_PATH` | Folder for local documents |
| `RETRIEVER` | Search provider (for example `tavily` or `google`) |
| `GOOGLE_API_KEY`, `GOOGLE_CX_KEY` | Google Custom Search |
| `PGVECTOR_CONNECTION_STRING` | PGVector connection (used in the data ingestion example) |
| `AZURE_CONNECTION_STRING`, `AZURE_CONTAINER_NAME` | Azure Blob Storage as a report source |
| `STRATEGIC_LLM` | Model override for the multi-agent workflow |
| `NEXT_PUBLIC_GPTR_API_URL` | Backend URL for the Next.js frontend |
| `NEXT_PUBLIC_GA_MEASUREMENT_ID` | Google Analytics measurement ID |
| `DISCORD_BOT_TOKEN`, `DISCORD_CLIENT_ID` | Discord bot |

### Config file

The default configuration is in `gpt_researcher/config/` (`config.py` and `variables/default.py`). You can supply an external JSON or YAML file with the `config_file` or `config_path` parameter. The documented options and their defaults include:

- `RETRIEVER`: `tavily`. Other retrievers in the repository include `duckduckgo`, `bing`, `google`, `searchapi`, `serper`, `serpapi`, `searx`, `exa`, `arxiv`, `pubmed_central`, `semantic_scholar`, and `mcp`.
- `EMBEDDING`: `openai:text-embedding-3-small`. Documented options include `ollama`, `huggingface`, `azure_openai`, and `custom`.
- `SIMILARITY_THRESHOLD`: `0.42`
- `FAST_LLM`: `openai:gpt-4o-mini` (summaries)
- `SMART_LLM`: `openai:gpt-4.1` (reports and reasoning)
- `STRATEGIC_LLM`: `openai:o4-mini` (research plans)
- `LANGUAGE`: `english`
- `CURATE_SOURCES`: `False`

Deep Research parameters, documented in `backend/report_type/deep_research/README.md`:

- `deep_research_breadth`: 4
- `deep_research_depth`: 2
- `deep_research_concurrency`: 2
- `reasoning_effort`: applies to reasoning models

Azure Blob Storage, PGVector, and other vector stores are configured through the Python API and the documentation in `docs/docs/gpt-researcher/context/`.

### Logging

`main.py` creates a `logs/` directory and writes `logs/app.log` as well as console output.

## Development

### Repository layout

- `gpt_researcher/`: core research package (`agent.py`, `actions/`, `skills/`, `retrievers/`, `scraper/`, `llm_provider/`, `vector_store/`, `mcp/`, `config/`)
- `backend/`: FastAPI server, chat agent, and report types (`basic_report`, `detailed_report`, `deep_research`)
- `multi_agents/`: LangGraph agents and workflow
- `frontend/`: static frontend and Next.js application
- `docs/`: Docusaurus documentation, blog, and Discord bot
- `evals/`: evaluation tools
- `tests/`: test scripts

### Dependencies

Dependencies are declared in `pyproject.toml` (Poetry and `[project]` sections), `requirements.txt`, `requirements_minimal.txt`, and `setup.py`, which reads `requirements.txt`. Development type stubs are listed under `[dependency-groups]` in `pyproject.toml`.

### Contributing

`CONTRIBUTING.md` describes the workflow:

1. Fork the repository and branch from `master`.
2. Make your changes and test them.
3. Follow the project's coding style.
4. Commit with clear messages.
5. Push to your fork and open a pull request.

Documentation changes follow the same process. The repository also includes a `CODE_OF_CONDUCT.md`, issue templates for bug reports and feature requests, and a Dependabot configuration.

### Documentation site

The site in `docs/` uses Docusaurus 3.7.0. From `docs/`, run `yarn install` and `yarn start`. `docs/README.md` also mentions `pydoc-markdown`.

### Continuous integration

Workflows are in `.github/workflows/`: `docker-build.yml` and `docker-push.yml`. Their contents are not included here, so this README does not describe their steps.

## Testing

### Pytest configuration

`pyproject.toml` configures pytest with `testpaths = ["tests"]`, `python_files = "test_*.py"`, `asyncio_mode = "strict"`, and `-v` output.

### Docker test service

```bash
docker-compose --profile test run --rm gpt-researcher-tests
```

This service installs `pytest`, `pytest-asyncio`, and `faiss-cpu`, then runs `tests/report-types.py` and `tests/vector-store.py`.

### GitHub Actions tests

The automated testing guide in the docs describes an environment named `tests` with the secrets `OPENAI_API_KEY` and `TAVILY_API_KEY`.

### Other test scripts

The `tests/` directory also contains scripts for logging, MCP, retrievers, LLMs, embeddings, document loaders, and the research flow, including `test_mcp.py`, `test_logging.py`, `research_test.py`, and `test-your-retriever.py`.

### Evaluations

The `evals/simple_evals/` harness adapts OpenAI's SimpleQA methodology:

```bash
cd evals/simple_evals
pip install -r requirements.txt
python run_eval.py --num_examples <number>
```

`--num_examples` defaults to 1. The grader defaults to a GPT-4-turbo model and assigns `CORRECT`, `INCORRECT`, or `NOT_ATTEMPTED`. The `logs/` directory includes a 100-problem run from February 22, 2025.

## License

The repository's `LICENSE` file contains the **Apache License, Version 2.0** text.

However, `pyproject.toml` and `setup.py` both declare the project license as **MIT**, and the npm package `docs/npm/package.json` and the React package `frontend/nextjs/package.json` also list MIT. The two sources disagree, so check with the maintainers before relying on either license.

Copyright is attributed to Assaf Elovic in the package metadata. Contact details are in `CODE_OF_CONDUCT.md` and `pyproject.toml`.

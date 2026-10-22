# GPT Researcher

GPT Researcher is an open-source autonomous research agent for investigating questions using web sources, local documents, or both. It plans research tasks, gathers and filters relevant material, and produces reports with source references. The Python package can be used directly in applications; this repository also includes a FastAPI backend, web interfaces, a command-line tool, and a LangGraph multi-agent example.

Research can use supported search retrievers and language models, and can be customized with report types, tones, source restrictions, and configuration settings. The project also includes optional Model Context Protocol (MCP) integration.

## Contents

- `gpt_researcher/` — Python research agent, configuration, retrievers, scrapers, and document handling.
- `backend/` — FastAPI server and report-generation implementations, including detailed and deep research.
- `frontend/` — Static frontend assets and a Next.js application.
- `multi_agents/` — A LangGraph example that coordinates specialized agents to research, review, revise, write, and publish reports.
- `cli.py` — Command-line report generation.
- `tests/` — Research, logging, loader, report-type, and integration-oriented test scripts.
- `docs/` — Docusaurus documentation site and examples.

For detailed guides, see the [GPT Researcher documentation](https://docs.gptr.dev/). The `docs/docs/gpt-researcher/` directory covers configuration, models, search engines, local documents, frontends, and more.

## Requirements

- Python 3.11 or later for the repository application and current package metadata.
- API credentials for the language model and search provider you choose. The documented default setup uses OpenAI and Tavily.
- Docker and Docker Compose for the containerized setup.
- Node.js and npm for the Next.js frontend. The frontend documentation recommends Node.js 18.17.0.

## Setup

### Install from source

Clone the repository and install its Python dependencies:

```bash
git clone https://github.com/assafelovic/gpt-researcher.git
cd gpt-researcher
pip install -r requirements.txt
```

Use a virtual environment if you want to isolate project dependencies. For example:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows, activate the environment using the appropriate script under `.venv\Scripts`.

Create a `.env` file in the repository root, or export credentials in your shell. For the documented OpenAI and Tavily setup:

```dotenv
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

The application loads `.env` through `python-dotenv`. Additional configuration may be needed for the LLM, retriever, or optional integrations you select.

### Start the backend

Run the FastAPI application with Uvicorn:

```bash
python -m uvicorn main:app --reload
```

The server listens on port `8000` by default. The root endpoint returns a welcome message, and the backend supports WebSocket communication at `/ws`.

### Start with Docker Compose

With Docker and Docker Compose installed, prepare a root `.env` file with the credentials required by the services, then run:

```bash
docker compose up --build
```

The Compose file defines the Python service on port `8000` and the Next.js development service on port `3000`. It also defines optional test and Discord bot services behind the `test` and `discord` profiles. Compose mounts `my-docs`, `outputs`, and `logs` for the backend; create those local directories as needed.

## Usage

### Python API

A basic research run uses the asynchronous `GPTResearcher` interface:

```python
import asyncio
from gpt_researcher import GPTResearcher

async def main():
    researcher = GPTResearcher(
        query="What are the latest developments in quantum computing?",
        report_type="research_report",
    )
    await researcher.conduct_research()
    report = await researcher.write_report()
    print(report)

asyncio.run(main())
```

`conduct_research()` gathers research context; `write_report()` generates the report. The report type can be changed, and `write_report()` also accepts a custom prompt for formatting. For example, `report_type="deep"` enables the deep-research flow described in `backend/report_type/deep_research/README.md`.

To research local documents, set `DOC_PATH` to their directory and use `report_source="local"`. The documentation lists PDF, plain text, CSV, Excel, Markdown, PowerPoint, and Word formats. Use `report_source="hybrid"` to combine local material with web research. You can also provide specific source URLs or domain restrictions; see the tailored research and domain-filtering guides in `docs/docs/gpt-researcher/context/`.

### Command line

The CLI writes generated Markdown reports to `outputs/` using a unique filename:

```bash
python cli.py "What are the main causes of climate change?" \
  --report_type research_report \
  --tone objective
```

`--report_type` is required. The CLI supports report types including `research_report`, `detailed_report`, `resource_report`, `outline_report`, `custom_report`, `subtopic_report`, and `deep_research`. Tone is optional and defaults to `objective`; other supported tones include formal, analytical, informative, and comparative. Domain filtering and output encoding can be supplied with `--query_domains` and `--encoding`. Run `python cli.py --help` for the available arguments.

### Frontend

For the Next.js interface, open another terminal:

```bash
cd frontend/nextjs
npm install --legacy-peer-deps
npm run dev
```

Visit `http://localhost:3000`. The frontend expects a backend; configure its API URL as needed. See `frontend/README.md` and `frontend/nextjs/README.md` for frontend options and package usage.

## Configuration

The main configuration is in `gpt_researcher/config/`. The documentation describes configuration through environment variables, a configuration file, or constructor arguments. An external JSON configuration file can be supplied using the `config_file` parameter.

Documented settings include:

- `RETRIEVER` — search provider; documented options include Tavily, DuckDuckGo, Bing, Google, SearchApi, Serper, and Searx.
- `FAST_LLM`, `SMART_LLM`, and `STRATEGIC_LLM` — models for fast operations, report/reasoning work, and research planning.
- `EMBEDDING` and `SIMILARITY_THRESHOLD` — embedding selection and document similarity threshold.
- `LANGUAGE` and `CURATE_SOURCES` — report language and whether to curate sources.

The documented configuration defaults include Tavily for retrieval, English for report language, and `CURATE_SOURCES=False`. Provider-specific credentials and settings depend on the integrations you choose. For deep research, `deep_research_breadth`, `deep_research_depth`, and `deep_research_concurrency` control exploration breadth, depth, and concurrency.

## Development

Keep changes focused and follow the existing style of the relevant Python, JavaScript, or TypeScript code. The repository’s contribution guide asks contributors to fork the project, branch from `master`, test their changes, use informative commits, and submit a pull request. Bug reports and feature requests can be submitted using the templates under `.github/ISSUE_TEMPLATE/`. Please also follow `CODE_OF_CONDUCT.md`.

The Next.js frontend provides scripts including `npm run dev`, `npm run build`, `npm run lint`, and `npm run build:lib`. The documentation site is built with Docusaurus; its `docs/README.md` describes local setup and development.

## Testing and evaluations

The project configures pytest in `pyproject.toml`. To run the repository tests:

```bash
python -m pytest
```

Some tests and evaluation tasks make external calls and may require API credentials. The Compose test profile installs pytest-related dependencies and runs the report-type and vector-store test scripts:

```bash
docker compose --profile test run --rm gpt-researcher-tests
```

For factuality evaluations, see `evals/README.md`. The SimpleQA evaluation can be run from `evals/simple_evals/` after installing its requirements and configuring the documented API keys:

```bash
pip install -r requirements.txt
python run_eval.py --num_examples 10
```

The evaluation script accepts `--num_examples`; its documented default is one example.

## License

The root `LICENSE` file contains the Apache License, Version 2.0. Project package metadata in `pyproject.toml` and `setup.py` identifies the package license as MIT. These files therefore report different licenses; consult the applicable license terms and project maintainers before relying on either designation.

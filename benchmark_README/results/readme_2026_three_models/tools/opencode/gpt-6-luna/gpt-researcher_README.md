# GPT Researcher

GPT Researcher is an autonomous research agent for investigating questions using web sources or supplied documents and generating research reports. It can be used as a Python library, through a command-line interface, or as a FastAPI web application. The repository also includes a separate LangGraph multi-agent example.

Research runs can plan sub-questions, retrieve and scrape source material, and use that material to write reports. Report types include research, detailed, resource, outline, custom, subtopic, and deep-research reports. The agent can also work with provided URLs, local documents, LangChain documents, or vector stores. Output quality and coverage depend on the selected models, source integrations, and configuration; generated material should be reviewed.

## Requirements

- Python 3.11 or later (the package metadata supports Python `<4`)
- Credentials for the LLM and retrieval integrations you choose

The default configuration uses OpenAI models and Tavily for web search. You can configure other supported LLM providers and retrievers; see [LLM configuration](https://docs.gptr.dev/docs/gpt-researcher/llms/llms) and [search engines](https://docs.gptr.dev/docs/gpt-researcher/search-engines/search-engines).

## Quick start

Clone the repository, install its Python dependencies, and set up credentials:

```bash
git clone https://github.com/assafelovic/gpt-researcher.git
cd gpt-researcher
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and provide the required credentials for your selected integrations. For the defaults, set at least:

```dotenv
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Start the web application:

```bash
python -m uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000). The application serves its web interface and provides the FastAPI backend. The `.env.example` file also documents `DOC_PATH` for local document workflows.

## Use as a Python library

The `GPTResearcher` API is asynchronous. A minimal example:

```python
import asyncio
from gpt_researcher import GPTResearcher


async def main():
    researcher = GPTResearcher(query="What are the main uses of geothermal energy?")
    await researcher.conduct_research()
    report = await researcher.write_report()
    print(report)


asyncio.run(main())
```

You can select report options and sources when constructing the researcher. For example, `report_type="research_report"` selects the standard research report; `query_domains` can restrict web search, and `source_urls` can provide URLs to research. `GPTResearcher` also exposes methods such as `get_source_urls()`, `get_research_context()`, `get_research_sources()`, `get_research_images()`, and `get_costs()` for retrieving information about a completed run.

See the [agent example](https://docs.gptr.dev/docs/gpt-researcher/gptr/example) and [configuration reference](https://docs.gptr.dev/docs/gpt-researcher/gptr/config) for more options, including local and hybrid data sources, custom prompts, models, and MCP integrations.

## Command-line interface

`cli.py` writes the generated report as a Markdown file under `outputs/`:

```bash
python cli.py "How is urban tree cover measured?" --report_type research_report
```

`--report_type` is required. Choices implemented by the CLI are `research_report`, `detailed_report`, `resource_report`, `outline_report`, `custom_report`, `subtopic_report`, and `deep`. You may also provide `--tone` (default `objective`), `--encoding`, and a comma-separated `--query_domains` list. For example:

```bash
python cli.py "Recent progress in battery recycling" \
  --report_type detailed_report \
  --tone analytical \
  --query_domains nature.com,energy.gov
```

Run `python cli.py --help` for the available tone choices and argument details.

## Configuration

Configuration is read from environment variables, including values in a root `.env` file. Useful settings include:

- `FAST_LLM`, `SMART_LLM`, and `STRATEGIC_LLM` to select models
- `EMBEDDING` to select the embedding provider and model
- `RETRIEVER` to choose one or more retrievers (comma-separated); it defaults to `tavily`
- `DOC_PATH` to set the local documents directory (defaults to `./my-docs`)
- `REPORT_FORMAT`, `LANGUAGE`, and `MAX_SUBTOPICS` to adjust report generation

The default LLM settings and the supported configuration keys are defined in `gpt_researcher/config/variables/default.py` and `gpt_researcher/config/variables/base.py`. Provider-specific API keys and extra dependencies may be needed when changing integrations. Refer to the [LLM guide](https://docs.gptr.dev/docs/gpt-researcher/llms/llms) and [configuration guide](https://docs.gptr.dev/docs/gpt-researcher/gptr/config) for details.

## Web app and deployment

The backend is a FastAPI application started by `main.py`; it serves the frontend from the `frontend/` directory and exposes report, file, and WebSocket functionality. The `frontend/` directory documents the static frontend and the separate Next.js frontend in its [README](frontend/README.md). Docker-related files are provided in `Dockerfile`, `Dockerfile.fullstack`, and `docker-compose.yml`; review the compose file and configure its environment variables before using it.

## Multi-agent example

The `multi_agents/` directory contains a LangGraph research workflow with specialized agents for planning, research, editing, review, revision, writing, and publishing. It has its own [README](multi_agents/README.md), dependencies, and `task.json` configuration; follow that guide to run the example.

## Tests

Tests are located in `tests/`. Pytest is configured in `pyproject.toml`; install the needed test dependencies in your environment, then run:

```bash
python -m pytest
```

Some tests exercise external LLM, search, embedding, or vector-store integrations and may require corresponding credentials or optional packages.

## Documentation and contributing

- Project documentation: [docs.gptr.dev](https://docs.gptr.dev/)
- Contribution guidelines: [CONTRIBUTING.md](CONTRIBUTING.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License

This repository is licensed under the Apache License 2.0. See [LICENSE](LICENSE).

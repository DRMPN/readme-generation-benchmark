# GPT Researcher

GPT Researcher is an open-source research assistant for investigating a question, gathering information from web and document sources, and producing a structured report with references. It uses configurable language models, search providers, retrievers, and report formats.

This repository includes the Python research engine, a web application and API, frontend packages, integrations, examples, and documentation.

## Contents

- [Features](#features)
- [How it works](#how-it-works)
- [Getting started](#getting-started)
- [Run with Docker](#run-with-docker)
- [Use as a Python library](#use-as-a-python-library)
- [Configuration](#configuration)
- [Research sources and integrations](#research-sources-and-integrations)
- [Project layout](#project-layout)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- Research a topic using web search and retrieved source material.
- Gather information from multiple sources and produce reports with citations.
- Choose from different report styles and research workflows.
- Configure supported language models, search engines, retrievers, and vector stores.
- Work with local documents and other ingestion sources.
- Stream research progress and logs through the web application.
- Extend the system with custom prompts, agents, tools, and integrations.
- Use the Python package, web application, JavaScript integrations, or React components.

Available providers and features depend on your configuration and installed dependencies.

## How it works

A typical research run follows these steps:

1. Accept a research question and options such as report type or source restrictions.
2. Plan searches or research subtasks.
3. Retrieve and process relevant web pages or documents.
4. Synthesize the gathered material into a report.
5. Include source references so readers can inspect the supporting material.

The repository also contains agent-based and LangGraph workflows. Exact behavior depends on the selected workflow and configuration.

## Getting started

### Requirements

- Python and Node.js versions compatible with the packages in this repository.
- API credentials for the language model and search providers you intend to use.
- Docker and Docker Compose if you plan to use the containerized full-stack application.

Check the package configuration and documentation for the version requirements applicable to your checkout.

### Install the Python package

To install the published package:

```bash
pip install gpt-researcher
```

Or install this repository in editable mode from its root:

```bash
pip install -e .
```

If the project’s dependencies are managed through Poetry in your checkout, you can install them with:

```bash
poetry install
```

### Configure credentials

Set the credentials required by your selected model and search providers. For example:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
```

You can place configuration in a `.env` file if your chosen entry point loads environment files. Do not commit secrets to version control.

Provider names and settings vary. See the configuration and supported-provider documentation before choosing environment variables for a particular backend.

## Run with Docker

The repository includes Docker and Docker Compose configuration for running the application. From the repository root, configure the required environment variables, then start the stack:

```bash
docker compose up --build
```

The full-stack Dockerfile is also provided as `Dockerfile.fullstack`. Check the Compose configuration and Docker documentation for the services, ports, and environment variables used by your checkout.

## Use as a Python library

The Python interface can be used to conduct research and generate a report:

```python
import asyncio
from gpt_researcher import GPTResearcher


async def main():
    researcher = GPTResearcher(
        query="How are heat pumps changing residential heating?",
        report_type="research_report",
    )

    await researcher.conduct_research()
    report = await researcher.write_report()

    print(report)


if __name__ == "__main__":
    asyncio.run(main())
```

Set the environment variables required by your configured model and search provider before running the example.

The repository’s examples and documentation include additional patterns for custom reports, source-only output, local documents, and tailored research workflows.

## Configuration

Configuration controls which language models, search providers, retrievers, vector stores, and research options are used. The repository contains configuration and provider modules for these integrations, along with documentation covering:

- Language model selection and provider setup.
- Search engine and retriever configuration.
- Embedding and vector-store options.
- Report types and research behavior.
- Filtering research by domain.
- Local document ingestion and other data sources.
- Logging, tracing, and troubleshooting.

Start with the configuration files and documentation included in this repository. Required settings depend on the providers and features you enable; a search provider’s API key, for example, is only needed if you use that provider.

## Research sources and integrations

The repository includes components and documentation for multiple search, scraping, and retrieval integrations. It also includes support material for local documents, Azure storage, MCP configurations, and integrations such as Claude and LangGraph.

Integrations may require additional credentials, packages, or services. Consult their individual setup guides before enabling them.

## Project layout

This repository contains several related projects and supporting resources:

- **Python research engine** — research planning, retrieval, scraping, report generation, prompts, and utilities.
- **Web application and API** — server, websocket handling, logging, and related application code.
- **Frontend** — a web interface for starting research, viewing progress, sources, and reports.
- **JavaScript and React packages** — reusable integrations and UI components.
- **Examples and evaluations** — example scripts, notebooks, tests, and evaluation utilities.
- **Documentation site** — guides for setup, configuration, integrations, and advanced usage.

## Testing

The repository includes tests and utilities for areas such as logging, retrievers, loaders, embeddings, LLMs, and MCP integrations. Some tests require provider credentials or external services.

Run the tests appropriate to your setup from the repository root. For example, if `pytest` is installed:

```bash
pytest
```

For tests that call external providers, configure the necessary credentials first. The documentation also includes guides for testing language models and retrievers.

## Documentation

The documentation in this repository covers installation, configuration, deployment, and advanced use. Topics include:

- Getting started with Docker, the Python package, and the CLI.
- Supported language models and search engines.
- Data ingestion, local documents, and vector stores.
- Filtering research by domain.
- Report types and tailored research.
- Websocket logs, backend querying, and frontend integrations.
- LangGraph, MCP, and other integrations.
- Testing, troubleshooting, and deployment.

Use the documentation files and site configuration included in the repository to find the guide most relevant to your setup.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before opening a pull request or participating in the project.

## License

See [LICENSE](LICENSE) for the terms under which this project is distributed.

# Chatsky

> **Note:** This README was inferred from the file listing. It describes the project as the Chatsky conversational framework, which the file names strongly suggest. Verify the commands and API examples against the actual source before publishing.

## Overview

This repository contains **Chatsky**, a Python framework for building conversational services. Chatsky lets you describe dialog logic as a declarative *script* of nodes and transitions, then runs that script inside a *pipeline* that handles message processing, context storage, slot (parameter) extraction, optional LLM integration, and deployment through web, chat, or messenger interfaces.

The repository also includes:

- Step-by-step **tutorials** covering basics through advanced topics
- **Context storage backends** for SQL, MongoDB, Redis, and Yandex Database (YDB)
- **Benchmarking** and **load-testing** tools
- A **statistics and monitoring stack** with OpenTelemetry collector configs and Apache Superset dashboards
- **Sphinx documentation** and API reference generation
- **Docker Compose** setup for running services and dependencies together

## Features

- **Declarative dialog scripts** with flows, nodes, responses, and transitions
- **Conditional transitions** and path-based routing
- **Pre-response and pre-transition processing** hooks
- **Slot extraction** for collecting structured information from user messages, including partial extraction and custom extractor functions
- **LLM integration** through LangChain-based helpers, with support for structured output and prompt usage
- **Context management**: serialization, history filtering, and pluggable storage backends
- **Multiple interfaces**: CLI, FastAPI, WebSocket chat, Streamlit chat, and messenger interfaces
- **Attachments and multi-message responses**, including media
- **Instrumentation** with OpenTelemetry
- **Statistics dashboards** for node visits, transitions, responses, and service load
- **Benchmarks and load tests** for comparing storage backends and measuring throughput

## Project Structure

```
.
├── chatsky/                  # Core framework package
│   ├── core/                 # Pipeline, script, context, message, transition, and actor logic
│   ├── context_storages/     # Storage backends: memory, SQL, Redis, MongoDB, YDB, file
│   ├── slots/                # Slot definitions, managers, and extraction logic
│   ├── llm/                  # LLM integration helpers (LangChain)
│   ├── messengers/           # CLI, FastAPI, WebSocket, Streamlit, and messenger interfaces
│   ├── stats/                # Statistics collection and instrumentation
│   └── utils/                # Shared helpers (serialization, async, logging, extra fields)
├── tutorials/                # Numbered tutorials, from basics to advanced usage
├── tests/                    # Unit and integration tests
├── benchmarks/               # Storage benchmarking and comparison tools
├── load_testing/             # Locust-based load tests
├── stats/                    # Statistics dashboards, Superset config, and Docker files
├── docs/                     # Sphinx documentation source
├── utils/                    # Development scripts (linting, docs, API regeneration, tests)
├── compose.yml               # Docker Compose definition for services and databases
├── pyproject.toml            # Project metadata and dependencies (Poetry)
├── poetry.lock               # Locked dependency versions
├── LICENSE
└── CONTRIBUTING.md
```

## Requirements

- Python 3.9 or newer (check `pyproject.toml` for the exact range)
- [Poetry](https://python-poetry.org/) for development installs
- Docker and Docker Compose (optional, for databases and the statistics stack)

## Installation

### From PyPI

```bash
pip install chatsky
```

### From source with Poetry

```bash
git clone <repository-url>
cd <repository-directory>
poetry install
```

To include optional extras such as database drivers, LLM libraries, or web interfaces, check `pyproject.toml` for the available extras and install them accordingly.

## Quick Start

The following example defines a minimal script and runs it in the console. The API follows the Chatsky 0.x style, so check the tutorials for the version you install.

```python
from chatsky import Pipeline, TRANSITIONS, RESPONSE, Message

toy_script = {
    "greeting_flow": {
        "start_node": {
            RESPONSE: Message("Hi! How can I help you?"),
            TRANSITIONS: {"help_node": lambda ctx, pipeline: "help" in ctx.last_request.text.lower()},
        },
        "help_node": {
            RESPONSE: Message("Tell me what you need."),
        },
        "fallback_node": {
            RESPONSE: Message("Sorry, I did not understand."),
        },
    }
}

pipeline = Pipeline.from_script(
    toy_script,
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
)

if __name__ == "__main__":
    pipeline.run()
```

Run the script, type messages in the console, and the pipeline will route between nodes based on your transition conditions.

## Core Concepts

| Concept | Description |
|---|---|
| **Script** | The full dialog definition, organized into flows and nodes. |
| **Flow** | A named group of related nodes. |
| **Node** | A single dialog state with a response and outgoing transitions. |
| **Transition** | A condition and destination that moves the dialog from one node to another. |
| **Context** | The per-user state and history, including requests, responses, and labels. |
| **Pipeline** | The runtime that ties together the script, context storage, services, and interfaces. |
| **Slot** | A typed piece of information (such as a name or date) extracted from user input. |
| **Context storage** | A backend that persists contexts between requests. |

## Tutorials

The `tutorials/` directory contains runnable examples, grouped by topic:

| Tutorial group | Topics |
|---|---|
| **1. Basics** | Creating a script, running a pipeline, basic responses |
| **2. Advanced** | Advanced script features and patterns |
| **3. Groups** | Organizing flows and nodes, global and local settings |
| **4. Conditions and paths** | Conditional transitions, transitions, and destinations |
| **5. Extra handlers** | Custom handlers and global or local behavior |
| **6. Context serialization** | Saving and restoring context |
| **7. Pre-response processing** | Modifying responses before they are sent |
| **8. Misc** | Utilities and miscellaneous features |
| **9. Pre-transition processing** | Hooks that run before transitions are evaluated |

Additional tutorial sets cover:

- **Slot extraction**: basic extractors, custom extractor functions, and partial extraction
- **Context storage**: SQLite, MySQL, PostgreSQL, MongoDB, Redis, Yandex Database, and database benchmarking
- **Messengers and interfaces**: FastAPI, WebSocket chat, and Streamlit chat
- **LLM integration**: basic LLM usage, prompt usage, filtering history, and structured output
- **Attachments and media**: sending and receiving files, images, and other media
- **Multi-message responses**: returning several messages from a single node
- **Pipeline integration**: loading pipelines from YAML or JSON configuration

Start with the basics tutorials, then move to the topic relevant to your application.

## Context Storage

Chatsky stores dialog contexts through pluggable backends. Choose one based on your deployment needs:

| Backend | Module | Typical use |
|---|---|---|
| In-memory | `memory.py` | Development and testing |
| SQLite | `sql.py` / `6_sqlite.py` | Local single-process use |
| MySQL | `sql.py` / `5_mysql.py` | Relational production deployments |
| PostgreSQL | `sql.py` / `2_postgresql.py` | Relational production deployments |
| MongoDB | `mongo.py` / `3_mongodb.py` | Document-oriented storage |
| Redis | `redis.py` / `4_redis.py` | Fast key-value caching and storage |
| Yandex Database (YDB) | `ydb.py` / `7_yandex_database.py` | Yandex Cloud deployments |
| File | `file.py` | Simple file-based persistence |

The `compose.yml` file provides containers for several of these databases, which makes local testing easier.

## Slots and Information Extraction

Slots let a dialog collect structured data from free-form user messages. Typical usage involves:

1. Defining slots with names and types.
2. Registering extractor functions that parse values from messages.
3. Using partial extraction to fill slots across several turns.
4. Checking slot values in transitions to decide what to ask next.

Relevant tutorials are in the slot extraction group, and the implementation lives in `chatsky/slots/`.

## LLM Integration

Chatsky provides helpers for using large language models within dialog scripts. These helpers wrap LangChain components and cover:

- Calling an LLM from a node response or condition
- Building prompts from templates and context
- Filtering conversation history before sending it to the model
- Requesting structured (typed) output from the model

Integration tests for LLM behavior are under `tests/`, and tutorials are in the LLM integration group.

## Interfaces and Deployment

Chatsky pipelines can be exposed through several interfaces:

- **Console (CLI)**: `python -m chatsky` or running a pipeline directly, with `cli.py` and `__main__.py` as entry points
- **FastAPI**: an HTTP service for handling messages
- **WebSocket**: real-time chat through a WebSocket connection
- **Streamlit**: a browser-based chat UI
- **Messenger interfaces**: adapters for external messaging platforms

Pipelines can also be described in YAML or JSON (see `example_config.yaml` and the pipeline JSON and YAML examples in the tutorials) and loaded at startup.

## Statistics and Monitoring

The `stats/` directory provides a complete analytics setup:

- **Instrumentation**: `chatsky/stats/instrumentor.py` records node visits, transitions, responses, and requests.
- **OpenTelemetry collector**: `otelcol-config.yml` and `otelcol-config-extras.yml` define how telemetry is collected and forwarded.
- **Storage**: `chatsky_database.yaml` and related files describe the statistics database.
- **Dashboards**: Apache Superset dashboards (in `chatsky_statistics_dashboard_1.yaml`) include charts for:
  - Node visit counts, ratios, and sunbursts
  - Transition counts, layouts, and chord diagrams
  - Response and request counts
  - Slot ratings and current topic distributions
  - Service load over time
  - Final node distribution
- **Superset configuration**: `superset_config_docker.py` and `entrypoint_stats.sh`, plus a Dockerfile for the stats stack
- **Documentation**: `stats/README.md` and the Superset guide in the docs

To explore dashboards, start the stats stack with Docker Compose and open Superset in your browser.

## Benchmarking

Benchmark tools compare context storage backends under realistic dialog workloads:

- `benchmarks/benchmark_dbs.py` runs benchmark sets against each backend.
- `benchmarks/benchmark_streamlit.py` shows results in an interactive UI.
- `benchmarks/benchmark_schema.json` defines the benchmark result format.
- `benchmarks/report.py` and `basic_config.py` generate reports and configure runs.
- `tests/test_benchmark.py` checks the benchmark code.

Benchmark results (for example, comparison charts) are documented in the docs.

## Load Testing

Load tests use [Locust](https://locust.io/). The scenario file is `load_testing/3_load_testing_with_locust.py`. Point it at a running service (such as the FastAPI or WebSocket interface), then start Locust to simulate concurrent users and measure response times and throughput.

## Running with Docker Compose

`compose.yml` defines services and supporting databases. A typical workflow:

```bash
docker compose up -d
```

Check the file for the exact service names, ports, and environment variables before running it. Use `docker compose down` to stop the services.

## Testing

Tests are in `tests/` and use pytest. Common areas:

- Script parsing, conditions, transitions, destinations, and node labels
- Context, context dictionaries, and context utilities
- Messages, actors, and pipeline behavior
- Slot management, types, functions, and partial extraction
- Serialization and validation
- Storage backends (`test_dbs.py`)
- LLM integration (`test_llm.py`)
- Tutorials (`test_tutorials.py`), which run the example code
- Instrumentation, messenger interfaces, and service behavior

Run the full test suite with:

```bash
poetry run pytest
```

Some tests require running databases or external services. Start them with Docker Compose first.

## Development

### Code Quality

The `utils/` directory contains development helpers:

- `codestyle.py`: formatting and linting checks
- `clean.py`: removes build and cache artifacts
- `doc.py` and `regenerate_apiref.py`: build documentation and regenerate the API reference
- `test.py`: test runner helper
- `patch_sphinx.py` and `custom_directives.py`: Sphinx customization

Check `pyproject.toml` for the configured linters, type checkers, and formatters.

### Documentation

Documentation is built with Sphinx from the `docs/` directory. The source includes:

- Getting started and basic concepts
- Context, slot extraction, and LLM integration guides
- Optimization and pipeline import guides
- Superset and statistics guides
- Examples, tutorials, and community pages
- An API reference generated from the source

Build the docs with the scripts in `utils/` (for example, `utils/doc.py`).

### Contributing

Contributions are welcome. Read `CONTRIBUTING.md` for guidelines on:

- Setting up a development environment
- Coding standards and commit conventions
- Running tests and checks before submitting changes
- Submitting pull requests

## Project Layout Reference

| Path | Purpose |
|---|---|
| `chatsky/core/` | Core runtime: script, pipeline, context, message, transition, actor |
| `chatsky/context_storages/` | Storage backends |
| `chatsky/slots/` | Slot management and extraction |
| `chatsky/llm/` | LLM helpers |
| `chatsky/messengers/` | Interface adapters |
| `chatsky/stats/` | Statistics and instrumentation |
| `chatsky/utils/` | Shared utilities |
| `tutorials/` | Numbered runnable examples |
| `tests/` | Test suite |
| `benchmarks/` | Storage benchmarks |
| `load_testing/` | Locust scenarios |
| `stats/` | Dashboards and telemetry configuration |
| `docs/` | Sphinx documentation |
| `utils/` | Development scripts |
| `compose.yml` | Docker Compose services |

## License

This project is distributed under the terms of the license in the [LICENSE](LICENSE) file.

## Acknowledgments

Chatsky is developed by the DeepPavlov team. See `docs/about_us.rst` and the community documentation for more information about the project and its contributors.

# Chatsky

Chatsky is a free and open-source software stack for creating chatbots, released under the terms of Apache License 2.0.

## Overview

Chatsky is a Python framework designed for building conversational agents (chatbots) with a script-based approach. It provides a structured way to define dialog flows, manage conversation context, integrate with various messaging platforms, and connect to different databases for context storage.

### Key Features

- **Script-based dialog engine** — Define conversation flows using `Script`, `Flow`, and `Node` structures with conditions, responses, transitions, and processing functions
- **Context management** — Store and serialize conversation state, including requests, responses, labels, and custom data
- **Multiple context storage backends** — Supports JSON file, Pickle file, SQLite, Redis, MongoDB, MySQL, PostgreSQL, and Yandex Database
- **Messenger interfaces** — Built-in support for console interaction, Telegram, and web API interfaces (FastAPI, WebSocket, Streamlit)
- **LLM integration** — Integrate Large Language Models via LangChain for prompt usage, filtering history, and structured output
- **Slot extraction** — Extract structured data from user messages using slot filling mechanisms
- **Statistics and monitoring** — Collect and visualize dialog statistics using OpenTelemetry and Apache Superset dashboards
- **Database benchmarking** — Built-in tools for benchmarking context storage performance

## Supported Platforms

- Python 3.9, 3.10, 3.11, 3.12
- OS Independent

## Installation

Chatsky uses Poetry for dependency management. Install it with pip:

```bash
pip install chatsky
```

### Optional Dependencies

Chatsky provides several optional dependency groups that can be installed as extras:

| Extra | Description |
|-------|-------------|
| `json` | JSON file context storage (aiofiles) |
| `pickle` | Pickle file context storage (aiofiles) |
| `sqlite` | SQLite context storage (sqlalchemy, aiosqlite) |
| `redis` | Redis context storage (redis) |
| `mongodb` | MongoDB context storage (motor) |
| `mysql` | MySQL context storage (sqlalchemy, asyncmy, cryptography) |
| `postgresql` | PostgreSQL context storage (sqlalchemy, asyncpg) |
| `ydb` | Yandex Database context storage (ydb, six) |
| `telegram` | Telegram messenger interface (python-telegram-bot) |
| `stats` | Statistics collection and dashboard (opentelemetry, requests, tqdm, omegaconf) |
| `benchmark` | Database benchmarking (pympler, humanize, pandas, altair, tqdm) |
| `yaml` | YAML script parsing (pyyaml) |
| `llm` | LLM integration (langchain) |

Example installation with specific extras:

```bash
pip install chatsky[telegram,sqlite,stats]
```

## Getting Started

### Basic Usage

Define a script with nodes containing transitions, conditions, and responses:

```python
from chatsky import Message, RESPONSE, TRANSITIONS
from chatsky.script.core import standard as std_conditions
from chatsky.messengers.console import ConsoleMessengerInterface
from chatsky.core.pipeline import Pipeline

script = {
    "greeting_flow": {
        "start_node": {
            TRANSITIONS: {"greeting_node": std_conditions.exact_match(Message("hi"))},
        },
        "greeting_node": {
            RESPONSE: Message(text="Hello!"),
            TRANSITIONS: {"greeting_node": std_conditions.exact_match(Message("hi"))},
        },
    }
}

pipeline = Pipeline(
    script=script,
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "greeting_node"),
    messenger_interface=ConsoleMessengerInterface(),
)

pipeline.run()
```

### Context Storages

Chatsky supports multiple database backends for persisting conversation context:

```python
from chatsky.context_storages.sql import SQLContextStorage

db = SQLContextStorage(
    path="postgresql+asyncpg://postgres:pass@localhost:5430/test"
)
```

Supported protocols include:
- `sqlite+aiosqlite://` — SQLite
- `mysql+asyncmy://` — MySQL
- `postgresql+asyncpg://` — PostgreSQL
- `redis://` — Redis
- `mongodb://` — MongoDB
- `grpc://` — Yandex Database

### LLM Integration

Integrate Large Language Models into your dialog system:

```python
from chatsky.llm import LLM_API
```

LLM features include:
- Prompt usage within dialog nodes
- Filtering conversation history
- Structured output generation

### Statistics

Chatsky includes a command-line tool for configuring Superset dashboards:

```bash
chatsky.stats config.yaml \
    -U superset_user \
    -P superset_password \
    -dP database_password \
    --db.user=database_user \
    --db.host=clickhouse \
    --db.port=8123 \
    --db.name=test \
    --db.table=otel_logs \
    --outfile=config_artifact.zip
```

The statistics module integrates with OpenTelemetry for collecting data and Apache Superset for visualization.

## Project Structure

```
chatsky/
├── conditions/          # Dialog flow conditions (standard, LLM, slots, service)
├── config/              # Superset dashboard configurations
├── context_storages/    # Database backends (SQL, Redis, MongoDB, YDB, files)
├── core/                # Framework core (context, pipeline, script, services)
├── destinations/        # Transition destinations
├── llm/                 # LLM integration via LangChain
├── messengers/          # Messenger interfaces (console, Telegram)
├── processing/          # Pre/post response and transition processing
├── responses/           # Node responses (standard, LLM, slots)
├── slots/               # Slot extraction system
├── stats/               # Statistics collection and CLI tools
└── utils/               # Utilities (benchmarking, logging, testing, docker)
```

## Development

### Setting Up the Development Environment

Chatsky uses `poetry` and `poethepoet` for development workflow automation:

```bash
# Install all dependencies including development tools
poetry install --with lint,test,devel,tutorials,docs --all-extras
```

### Running Tests

The project uses pytest with several test markers:
- `docker` — tests requiring Docker containers
- `slow` — tests taking more than a minute
- `no_coverage` — tests that don't affect coverage stats
- `needs_dependencies` — tests requiring extra dependencies

```bash
# Quick sanity check
poetry run poe quick_test

# Run all tests without coverage
poetry run poe test_no_cov

# Run all tests including DB integration (requires Docker)
poetry run poe test_all
```

### Code Style

The project uses `black`, `mypy`, and `flake8` for code style checking:

```bash
# Format code
poetry run poe format

# Run linters
poetry run poe lint
```

### Building Documentation

```bash
# Build documentation (requires pandoc)
poetry run poe docs

# Build without Docker (faster, some tutorials may show errors)
poetry run poe docs_no_docker
```

Documentation is built with Sphinx and includes:
- API reference documentation
- Tutorials (Jupyter notebooks)
- User guides for basic concepts, context, LLM integration, optimization, slot extraction, and Superset
- Examples and community resources

### Tutorials

The repository includes comprehensive tutorials organized by topic:

- **Script** — Core concepts, conditions, responses, transitions, processing
- **Context Storages** — Database integrations and benchmarking
- **Service** — Service basics, groups, extra handlers
- **Slots** — Basic and partial extraction
- **LLM** — Basics, prompt usage, filtering, structured output
- **Messengers** — Telegram, FastAPI, WebSocket, Streamlit, load testing
- **Stats** — Extractor functions and pipeline integration

### Docker

Chatsky provides Docker configurations for running statistics dashboards and other services. The `compose.yml` file defines the service orchestration, and Dockerfiles are available in `chatsky/utils/docker/`.

## Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Branch naming conventions
- Commit message format
- Workflow management with Poetry
- Testing and documentation practices

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

Copyright 2022 Neural Systems and Deep Learning Laboratory, Moscow Institute of Physics and Technology.

## Links

- **Homepage**: [https://github.com/deeppavlov/chatsky](https://github.com/deeppavlov/chatsky)
- **Documentation**: [https://deeppavlov.github.io/chatsky/](https://deeppavlov.github.io/chatsky/)
- **Project Template**: [https://github.com/deeppavlov/chatsky-template](https://github.com/deeppavlov/chatsky-template)

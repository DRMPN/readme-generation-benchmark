# Chatsky

Chatsky is a free and open-source Python framework for building chatbots and dialog systems, released under the [Apache License 2.0](LICENSE).

Dialog behavior is described as a *script*: a graph of nodes organized into flows. Each node defines the bot's response and the transitions to other nodes, which are triggered by conditions on the user's input. Chatsky then runs the script as a pipeline that processes each incoming message.

- Documentation: <https://deeppavlov.github.io/chatsky/>
- Project template: <https://github.com/deeppavlov/chatsky-template>

## Features

Based on the package's modules and tutorials, Chatsky provides:

- **Dialog scripts**: a dictionary-based DSL with `RESPONSE` and `TRANSITIONS` keywords, organized into flows and nodes (`chatsky.core.script`).
- **Conditions**, **responses**, and **destinations** for defining transitions and replies (`chatsky.conditions`, `chatsky.responses`, `chatsky.destinations`).
- **Pipeline processing hooks**: pre/post services and pre-transition and pre-response processing (`chatsky.core.service`, `chatsky.processing`).
- **Context storage** backends for persisting dialog contexts (`chatsky.context_storages`): in-memory, JSON and Pickle files, SQLite, MySQL, PostgreSQL, Redis, MongoDB, and Yandex Database (YDB).
- **Messenger interfaces** (`chatsky.messengers`): a command-line interface (the default), a Telegram interface, and common base classes for building other interfaces.
- **Slots** for slot filling, and **LLM** integration (`chatsky.slots`, `chatsky.llm`, `chatsky.conditions.llm`, `chatsky.responses.llm`).
- **Statistics collection** via OpenTelemetry (`chatsky.stats`) and a **benchmarking** utility for context storages (`chatsky.utils.db_benchmark`).
- **Testing helpers** such as `check_happy_path` (`chatsky.utils.testing`).

## Requirements

- Python 3.9 or newer (`python = "^3.9,!=3.9.7"` in `pyproject.toml`).
- The core package depends on `pydantic` (>= 2.0), `nest-asyncio`, `typing-extensions`, `eval_type_backport`, `wrapt`, and `colorama`.

## Installation

Install the core package from PyPI:

```bash
pip install chatsky
```

Optional dependencies are available as extras. The extras defined in `pyproject.toml` are:

| Extra | Installs support for |
| --- | --- |
| `json` | JSON context storage (`aiofiles`) |
| `pickle` | Pickle context storage (`aiofiles`) |
| `sqlite` | SQLite context storage (`sqlalchemy`, `aiosqlite`) |
| `redis` | Redis context storage |
| `mongodb` | MongoDB context storage (`motor`) |
| `mysql` | MySQL context storage (`sqlalchemy`, `asyncmy`, `cryptography`) |
| `postgresql` | PostgreSQL context storage (`sqlalchemy`, `asyncpg`) |
| `ydb` | Yandex Database context storage (`ydb`, `six`) |
| `telegram` | Telegram messenger interface (`python-telegram-bot`) |
| `stats` | Statistics collection (OpenTelemetry, `requests`, `tqdm`, `omegaconf`) |
| `benchmark` | Context storage benchmarking (`pympler`, `humanize`, `pandas`, `altair`, `tqdm`) |
| `yaml` | YAML pipeline files (`pyyaml`) |
| `llm` | LLM integration (`langchain`) |

Example:

```bash
pip install "chatsky[sqlite,telegram]"
```

### Installing from source

```bash
git clone https://github.com/deeppavlov/chatsky.git
cd chatsky
poetry install --all-extras
```

## Quick start

The following example defines a small dialog and runs it in the terminal:

```python
from chatsky import (
    TRANSITIONS,
    RESPONSE,
    Pipeline,
    Transition as Tr,
    conditions as cnd,
)

script = {
    "greeting_flow": {
        "start_node": {
            TRANSITIONS: [Tr(dst="node1", cnd=cnd.ExactMatch("Hi"))],
        },
        "node1": {
            RESPONSE: "Hi, how are you?",
            TRANSITIONS: [Tr(dst="node2", cnd=cnd.ExactMatch("I'm fine, how are you?"))],
        },
        "node2": {
            RESPONSE: "Good. What do you want to talk about?",
            TRANSITIONS: [Tr(dst="node1", cnd=cnd.ExactMatch("Hi"))],
        },
        "fallback_node": {
            RESPONSE: "Ooops",
            TRANSITIONS: [Tr(dst="node1", cnd=cnd.ExactMatch("Hi"))],
        },
    }
}

pipeline = Pipeline(
    script=script,
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
)

if __name__ == "__main__":
    pipeline.run()
```

`Pipeline.run()` uses `CLIMessengerInterface` by default, so you can chat with the bot through standard input and output.

### Core concepts

- **Script**: a dictionary whose keys are flow names. Each flow is a dictionary of nodes.
- **Flow**: a sub-dialog about one topic.
- **Node**: a single step of the dialog. It can contain a `RESPONSE` (what the bot sends) and `TRANSITIONS` (where the dialog goes next).
- **Transition**: a `Tr(dst=..., cnd=...)` object pairing a destination node with a condition.
- **Pipeline**: the object that receives user messages, determines the next node, and produces a response. `start_label` sets the initial node, and `fallback_label` is used when no transition condition matches. If `fallback_label` is omitted, it defaults to `start_label`.

### Calling the pipeline directly

A pipeline can also process one message at a time, which is useful for testing or integration:

```python
from chatsky import Message

ctx = pipeline(Message("Hi"), ctx_id="user-1")
print(ctx.last_response)
```

## Tutorials

The `tutorials/` directory contains runnable examples grouped by topic:

- `tutorials/script/`: core script features (basics, conditions, transitions, responses, global/local variables, context serialization, processing hooks).
- `tutorials/service/`: services, service groups, conditions and paths, and extra handlers.
- `tutorials/slots/`: slot filling and partial extraction.
- `tutorials/llm/`: LLM basics, prompts, filtering history, and structured output.
- `tutorials/context_storages/`: Redis, MongoDB, PostgreSQL, MySQL, SQLite, Yandex Database, partial updates, and benchmarking.
- `tutorials/messengers/`: Telegram examples and web API interfaces (FastAPI, WebSocket, Streamlit, and Locust load testing).
- `tutorials/stats/`: statistics extractors and pipeline integration.

Several tutorials require optional dependencies, external services, or API keys. See `.env_file` and the [documentation](https://deeppavlov.github.io/chatsky/) for details.

## Configuration

Tests and Docker services read their settings from [`.env_file`](.env_file). This file contains placeholder values for the following variables:

- Messenger and LLM API keys: `TG_BOT_TOKEN`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`.
- Database credentials and ports for MySQL, PostgreSQL, Redis, MongoDB, YDB, ClickHouse, and the Superset dashboard.

Replace the placeholder values with your own before using these services outside of local testing.

## Development

The repository uses [Poetry](https://python-poetry.org/) for dependency management and [poethepoet](https://github.com/nat-n/poethepoet) for task automation. Tasks are defined in `[tool.poe.tasks]` in `pyproject.toml`.

Set up a development environment:

```bash
poetry install --with lint,test,devel,tutorials,docs --all-extras
```

Common tasks:

| Command | Purpose |
| --- | --- |
| `poetry run poe test_no_cov` | Run the unit tests without coverage |
| `poetry run poe test_all` | Run all tests, including database and API integration tests (requires Docker) |
| `poetry run poe quick_test` | Quick sanity check that skips `slow` and `docker` tests |
| `poetry run poe quick_test_coverage` | Quick run with an HTML coverage report |
| `poetry run poe lint` | Run `flake8` and `black --check` |
| `poetry run poe format` | Format code with `black` |
| `poetry run poe docs` | Build the Sphinx documentation (requires `pandoc`; uses Docker) |
| `poetry run poe docs_no_docker` | Build the documentation without Docker |
| `poetry run poe info` | Show information about the Poetry environment |
| `poetry run poe clean` | Clean generated files (see `scripts/clean.py`) |

Tests are in `tests/`. The test runner uses `pytest`, with a coverage threshold of 90% for `test_all` and coverage runs.

### Docker services

`compose.yml` defines two groups of services, selected with Docker Compose profiles:

```bash
# Database services for integration tests (MySQL, PostgreSQL, Redis, MongoDB, YDB)
docker compose --profile context_storage up

# Statistics services (Superset dashboard, ClickHouse, OpenTelemetry Collector)
docker compose --profile stats up
```

Docker is required for `test_all` and for the docker-dependent tests. The Docker-based documentation build is also described above.

## Project structure

```
chatsky/          Library source code
  conditions/       Transition conditions
  config/           Superset dashboard configuration for statistics
  context_storages/ Context storage backends
  core/             Script, pipeline, context, transitions, services
  destinations/     Transition destinations
  llm/              LLM integration
  messengers/       Messenger interfaces (console, Telegram, common)
  processing/       Pre/post processing functions
  responses/        Response types
  slots/            Slot filling
  stats/            Statistics collection
  utils/            Testing, devel, benchmarking, Docker and OTel helpers
docs/             Sphinx documentation sources
scripts/          Poe task implementations
tests/            Test suite
tutorials/        Runnable tutorials
utils/            Standalone utilities and examples
```

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidance on branch and commit naming, pull request rules, the development workflow, and documentation conventions.

## License

Chatsky is released under the Apache License 2.0. See [LICENSE](LICENSE).

## Authors

Chatsky is developed by Denis Kuznetsov, Roman Zlobin, Aleksandr Sergeev, and Daniil Ignatiev, as listed in `pyproject.toml`.

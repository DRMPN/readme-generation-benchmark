# Chatsky

<p align="center">
  <img src="https://raw.githubusercontent.com/deeppavlov/chatsky/master/docs/images/Chatsky-full-light.svg" alt="Chatsky logo" width="400"/>
</p>

<p align="center">
  <a href="https://github.com/deeppavlov/chatsky/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0"/></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made with Python"/></a>
  <a href="https://github.com/deeppavlov/chatsky/actions"><img src="https://img.shields.io/github/actions/workflow/status/deeppavlov/chatsky/test.yml?branch=main" alt="Build status"/></a>
  <a href="https://pypi.org/project/chatsky/"><img src="https://img.shields.io/pypi/v/chatsky" alt="PyPI version"/></a>
  <a href="https://pypi.org/project/chatsky/"><img src="https://img.shields.io/pypi/pyversions/chatsky" alt="Supported Python versions"/></a>
</p>

**Chatsky** is a free, open-source software for building dialogue systems. It is designed primarily for research and development of conversational agents, chatbots and LLM-powered assistants.

Chatsky lets you define dialogue flows as **finite state machines (FSM)** — connected graphs of states ("nodes") grouped into "flows". Each node is associated with **conditions** (when to enter it) and **responses** (what to say when you're in it). Dialogue context can be stored in a wide range of databases, allowing both short-term and long-term memory, multi-user operation, and horizontal scaling of your bot behind HTTP/WebSocket services.

---

## Table of contents

1. [Features](#features)
2. [Installation](#installation)
3. [Quick start](#quick-start)
4. [Core concepts](#core-concepts)
5. [Context storages](#context-storages)
6. [Pipeline & services](#pipeline--services)
7. [LLM integration](#llm-integration)
8. [Slots (data extraction)](#slots-data-extraction)
9. [Messaging interfaces](#messaging-interfaces)
10. [Statistics & monitoring](#statistics--monitoring)
11. [Benchmarking](#benchmarking)
12. [Tutorials](#tutorials)
13. [Testing](#testing)
14. [Documentation](#documentation)
15. [Development](#development)
16. [Community & contributing](#community--contributing)
17. [License](#license)

---

## Features

- 🧩 **Declarative dialogue scripts** — describe your bot as a graph of flows and nodes with transitions, conditions and responses.
- 🗄️ **Pluggable context storages** — keep conversation state in memory, files, or databases: JSON, Pickle, Shelve, SQLite, MySQL, PostgreSQL, MongoDB, Redis, Yandex Database.
- 🤖 **LLM integration** — use LLMs (via [LangChain](https://www.langchain.com/)) as conditions, responses, extra handlers, and for structured output / slot extraction.
- 🛠️ **Pipeline as a service** — an extensible pipeline of services (actor, pre/post response processing, pre-transition processing, custom components) with per-service hooks and timeouts.
- 💬 **Multiple messenger interfaces** — console, Telegram, WebSocket, FastAPI, Streamlit, plus locust-based load testing harness.
- 📊 **Statistics & observability** — OpenTelemetry-based instrumentation, ClickHouse storage, and ready-made Apache Superset dashboards.
- ⏱️ **Benchmarking** — built-in benchmark suite for context storages and pipelines with comparison reports.
- 🧪 **Fully tested** — the library, its tutorials, and its LLM/stats components are covered by automated tests.

---

## Installation

### Stable release

```bash
pip install chatsky
```

Chatsky ships with a minimal core set of dependencies; optional features are enabled via extras:

```bash
# Telegram interface
pip install chatsky[telegram]

# Database connectors
pip install chatsky[sqlite]
pip install chatsky[mysql]
pip install chatsky[postgres]
pip install chatsky[mongodb]
pip install chatsky[redis]
pip install chatsky[ydb]

# LLM integration (LangChain-based)
pip install chatsky[llm]

# Statistics collection (OpenTelemetry / ClickHouse)
pip install chatsky[stats]

# Everything above in one shot
pip install chatsky[full]
```

### Development version

```bash
pip install git+https://github.com/deeppavlov/chatsky.git@main
```

### Development installation

```bash
git clone https://github.com/deeppavlov/chatsky.git
cd chatsky
make venv              # create a virtual environment
poetry install --all-extras   # install all dependencies via Poetry
```

---

## Quick start

The snippet below defines a small dialogue script and runs it as an interactive console bot (see `tutorials/pipeline_basics/1_basics.py`):

```python
import asyncio

from chatsky import (
    RESPONSE,
    TRANSITIONS,
    Message,
    Pipeline,
    conditions as cnd,
    destinations as dst,
    responses as rsp,
)

script = {
    "greeting_flow": {
        "start_node": {
            RESPONSE: Message(),
            TRANSITIONS: {
                "greeting_node": cnd.regexp(r"\b(hi|hello)\b", ignore_case=True),
            },
        },
        "greeting_node": {
            RESPONSE: rsp.repeat,
            TRANSITIONS: {"input_node": dst.forward()},
        },
        "input_node": {
            RESPONSE: rsp.echo,
            TRANSITIONS: {
                "fallback_node": cnd.regexp(r"\b(thank|good)\b", ignore_case=True),
            },
        },
        "fallback_node": {
            RESPONSE: Message(text="Ooops"),
            TRANSITIONS: {"start_node": dst.forward()},
        },
    }
}

pipeline = Pipeline.from_script(
    script,
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
)

if __name__ == "__main__":
    pipeline.run()
```

Running this file starts an interactive console session:

```text
-bot: Hello, user!
user: hi
-bot: hi
user: good
-bot: Ooops
user: exit
```

---

## Core concepts

| Concept | Description |
|---|---|
| **Script** | A dictionary-like description of the dialogue as a set of flows, each containing nodes. Validated and parsed by `chatsky.core.script`. |
| **Flow** | A named group of nodes (a subgraph). Supports `GLOBAL` and `LOCAL` scopes for shared transitions and handlers. |
| **Node** | A dialogue state with a `RESPONSE`, optional `PROCESSING`, `PRE_TRANSITIONS_PROCESSING` and outgoing `TRANSITIONS`. |
| **Condition** | A callable returning `True`/`False`, deciding whether a transition happens (regex, exact match, intents, LLM conditions, etc.). |
| **Transition** | A pair of destination label + condition. Destinations can be static labels, relative (`dst.forward`, `dst.backward`, `dst.repeat`) or computed dynamically. |
| **Response** | What the bot says in a node — a `Message` or a callable producing one. Supports media attachments and multi-messages. |
| **Context** | A serializable representation of the dialogue: history, current node label, misc data, per-request storage fields. |
| **Pipeline** | The runtime that executes services on each user request: interface → services (actor, handlers, custom components) → messenger. |
| **Service** | A unit of the pipeline: actor, extra handlers, pre/post response processing, pre-transition processing, etc. Services can be grouped and nested. |

Related documentation pages: `basic_conceptions.rst`, `context_guide.rst`, `pipeline_import.rst`.

---

## Context storages

Contexts are stored via `chatsky.context_storages`. Switching storages is a one-line change:

```python
from chatsky.context_storages import connector_factory

db = connector_factory("sqlite:///my_db.db")
pipeline = Pipeline.from_script(script, ..., context_storage=db)
```

| Storage | URI scheme example | Extra |
|---|---|---|
| Memory | `memory://` | built-in |
| JSON file | `json://file.json` | built-in |
| Pickle | `pickle://file.pkl` | built-in |
| Shelve | `shelve://file.shelve` | built-in |
| SQLite | `sqlite:///db.sqlite` | `chatsky[sqlite]` |
| MySQL | `mysql://user:pass@host/db` | `chatsky[mysql]` |
| PostgreSQL | `postgresql://user:pass@host/db` | `chatsky[postgres]` |
| MongoDB | `mongodb://user:pass@host/db` | `chatsky[mongodb]` |
| Redis | `redis://user:pass@host/db` | `chatsky[redis]` |
| Yandex Database | `ydb://endpoint/database` | `chatsky[ydb]` |

Tutorials: `tutorials/pipeline_basics/5_mysql.py`, `4_redis.py`, `6_sqlite.py`, `7_yandex_database.py`, `9_db_benchmarking.py`, plus serialization guides in `tutorials/script/6_context_serialization.py`.

---

## Pipeline & services

The `chatsky.pipeline` package turns a script into an async application:

- **Actor** — the core service executing script logic.
- **Component / Group / Service** — build blocks for custom logic; groups can be nested with their own timeouts, concurrency settings and hooks.
- **Extra handlers** — `before`/`after` hooks for any service (`tutorials/pipeline_basics/5_extra_handlers.py`).
- **Pre-response / pre-transition processing** — mutate the context before responses and transitions (`7_pre_response_processing.py`, `9_pre_transition_processing.py`).
- **Pipeline import** — pipelines can be loaded from YAML/JSON configs (`pipeline_import.rst`, `example_config.yaml`, `pipeline.json`).

---

## LLM integration

`chatsky.llm` wraps [LangChain](https://www.langchain.com/) LLM APIs so models can drive dialogue logic:

- **LLM conditions** — route transitions based on model judgment.
- **LLM responses** — generate replies from prompts.
- **Prompt management** — attach prompts to flows/nodes with inheritance (`tutorials/prompt/1_basics.py`, `2_prompt_usage.py`, `3_filtering_history.py`).
- **History filtering** — control what part of the dialogue history the model sees (`filters.py`).
- **Structured output** — parse model output into typed Pydantic structures (`tutorials/llm_funcs/4_structured_output.py`).
- **Context rendering** — `langchain_context.py` converts Chatsky contexts into LangChain messages.

Tutorials: `tutorials/llm_funcs/` (`1_basics.py`, `2_postgresql.py`, `3_mongodb.py`, `4_structured_output.py`).

> ⚠️ LLM conditions/responses require API credentials (e.g. OpenAI). See `llm_integration.rst`.

---

## Slots (data extraction)

`chatsky.slots` provides declarative extraction of structured data from user messages:

- **Standard slots** — regexp-based, function-based, etc. (`standard.py`).
- **Slot manager** — extraction with partial results (`2_partial_extraction.py`).
- **LLM slots** — use LLMs to extract structured data (`tutorials/slots/llm.py`, `slot_extraction.rst`).
- **Extractor functions** — reusable extraction pipelines (`tutorials/utils/1_extractor_functions.py`).

---

## Messaging interfaces

`chatsky.messengers` and `chatsky.interface` connect pipelines to channels:

| Interface | Tutorial |
|---|---|
| Console (built-in) | any tutorial |
| FastAPI (HTTP) | `tutorials/messenger/1_fastapi.py` |
| WebSocket chat | `tutorials/messenger/2_websocket_chat.py` |
| Telegram | `tutorials/messenger/` (requires `chatsky[telegram]`) |
| Streamlit chat UI | `tutorials/messenger/4_streamlit_chat.py` |
| Attachments & media | `tutorials/attachments/1_media.py`, `2_attachments.py`, `3_advanced.py` |
| Multi-message responses | `tutorials/attachments/1_basic.py`, `2_multi_message.py` |
| Load testing with Locust | `tutorials/messenger/3_load_testing_with_locust.py` |

---

## Statistics & monitoring

`chatsky.stats` instruments pipelines with [OpenTelemetry](https://opentelemetry.io/):

- **Default extractors** — node visits, transitions, timings, request/response payloads, custom stat handlers (`default_extractors.py`, `instrumentor.py`).
- **Backends** — spans are exported to ClickHouse (see `cleanup_db.py`, `otelcol-config.yml`, `otelcol-config-extras.yml`, `example_config.yaml`).
- **Superset dashboards** — the repository ships ready-made Superset dashboards and charts (see `superset_guide.rst`, `chatsky_statistics_dashboard_1.yaml`, `chatsky_node_stats.yaml`, `chatsky_stats.yaml`, `chatsky_database.yaml` and the chart YAML files).
- **CLI** — `python -m chatsky.stats` utilities via `cli.py` / `__main__.py`.

Tutorials & configs: `tutorials/stats/` (e.g. `pipeline.json`), dashboard data providers (`sample_data_provider.py`, `telegram_tutorial_data.py`).

---

## Benchmarking

`chatsky.benchmark` provides reproducible benchmarks:

- Context storage benchmarks (SQLite, Redis, MongoDB, YDB — `tutorials/pipeline_basics/9_db_benchmarking.py`).
- Pipeline load benchmarks (`benchmark_dbs.py`, `benchmark_streamlit.py`).
- Comparison reports against published benchmark sets (`report.py`, `basic_config.py`, `benchmark.py`).

The `benchmark_sets.png`, `benchmark_mass_compare.png`, `benchmark_compare.png` images in the docs visualize the latest results.

---

## Tutorials

All tutorials are runnable scripts in `tutorials/`:

| Directory | Contents |
|---|---|
| `tutorials/pipeline_basics/` | Building pipelines: basics, advanced usage, service groups, conditions & paths, extra handlers, database connectors (MySQL, Redis, SQLite, YDB), DB benchmarking |
| `tutorials/script/` | Script fundamentals: conditions, responses, transitions, global/local settings, context serialization, pre-response & pre-transition processing, misc features |
| `tutorials/prompt/` | LLM prompts: basics, prompt usage, history filtering |
| `tutorials/llm_funcs/` | LLM functions: basics, DB-backed contexts, structured output |
| `tutorials/messenger/` | FastAPI, WebSocket, Locust load testing, Streamlit |
| `tutorials/attachments/` | Media, attachments, advanced attachment handling |
| `tutorials/multi_message/` | Basic and multi-message responses |
| `tutorials/slots/` | Slot extraction (standard + LLM-based) |
| `tutorials/utils/` | Extractor functions and partial extraction |
| `tutorials/stats/` | Statistics collection and Superset visualization |

Run any tutorial with:

```bash
python tutorials/pipeline_basics/1_basics.py
```

---

## Testing

The project is tested with `pytest`. Tests live in dedicated packages covering:

- Core: script parsing, transitions, conditions, responses, node labels, destinations, messages, contexts, serialization, validation.
- Pipeline: services, actor, messenger interfaces, update/misc context fields, instrumentation, defaults, main pipeline behavior.
- Storages: `test_dbs.py` (all connectors), serialization, benchmark.
- LLM: `test_llm.py`.
- Slots: `test_slot_manager.py`, `test_slot_partial_extraction.py`, `test_slot_functions.py`, `test_slot_types.py`.
- Tutorials: `test_tutorials.py` (executed in non-interactive mode), `test_format.py`, `test_utils.py`.

Database-backed tests run against services defined in `compose.yml`:

```bash
docker compose up -d           # start test databases
make test                      # run the test suite
make test-all                  # run tests for all extras
```

Python files with test payloads: `pipeline.json`, `wrong_type.json`, `test_happy_paths.json`.

---

## Documentation

Documentation is built with [Sphinx](https://www.sphinx-doc.org/):

| Page | Content |
|---|---|
| `get_started.rst` | Installation & first steps |
| `basic_conceptions.rst` | Core concepts (scripts, nodes, transitions) |
| `context_guide.rst` | Working with contexts & storages |
| `pipeline_import.rst` | Importing pipelines from configs |
| `user_guides.rst` | Practical guides |
| `llm_integration.rst` | Using LLMs in dialogue scripts |
| `slot_extraction.rst` | Slot-based data extraction |
| `superset_guide.rst` | Statistics dashboards in Superset |
| `optimization_guide.rst` | Performance & optimization |
| `reference.rst` | API reference (autogenerated, see `regenerate_apiref.py`) |
| `development.rst` | Contribution & development workflow |
| `community.rst` / `about_us.rst` | Community and team info |

Build locally:

```bash
make docs-en            # build English docs
make docs-dev           # development docs build
```

Documentation tooling lives in `docs/source/_exts/` (`custom_directives.py`, `link_misc_files.py`, `generate_tutorials.py`, `notebook.py`, `regenerate_apiref.py`) and `docs/utils/` (`clean.py`, `doc.py`, `patch_sphinx.py`, `switcher_gen.py`).

---

## Development

- **Dependency management:** [Poetry](https://python-poetry.org/) (`pyproject.toml`, `poetry.lock`).
- **Code style:** formatting/linting helpers in `scripts/codestyle.py`; pre-commit style checks (`make lint`).
- **Docker:** `compose.yml` for test infrastructure; stats container assets in `docker/stats/` (`dockerfile_stats`, `entrypoint_stats.sh`, `superset_config_docker.py`).
- **Test helper scripts:** `scripts/test.py`, `scripts/misc.py`, `scripts/utils.py`.

---

## Community & contributing

We welcome contributions! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting a pull request.

- 💬 Ask questions in the project discussions or issue tracker.
- 🐛 Report bugs via [GitHub issues](https://github.com/deeppavlov/chatsky/issues).
- 📖 Improve docs, tutorials, or add new features.

---

## License

Chatsky is distributed under the [Apache 2.0 License](LICENSE).

© Chatsky contributors / DeepPavlov team.

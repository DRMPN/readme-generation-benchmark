# chatsky-701yr76h

---

[![PyPi](https://badge.fury.io/py/chatsky.svg)](https://badge.fury.io/py/chatsky)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style={0}&logo=Pydantic&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB.svg?style={0}&logo=Python&logoColor=white)
![redis](https://img.shields.io/badge/Redis-DC382D.svg?style={0}&logo=Redis&logoColor=white)
![sqlalchemy](https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style={0}&logo=SQLAlchemy&logoColor=white)
![tqdm](https://img.shields.io/badge/tqdm-FFC107.svg?style={0}&logo=tqdm&logoColor=black)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Chatsky is a free, open-source Python framework for building chatbots and dialog-driven conversational agents. It models conversations as dialog graphs (scripts of flows and nodes) that are executed by an actor within an asynchronous pipeline, with pluggable components for context storage, messaging interfaces, and optional LLM integration, slot extraction, and runtime statistics. It is intended for Python developers building conversational services, from simple console bots to bots integrated with external messaging platforms and monitoring tooling. Pipelines can be defined in code or imported from configuration files, and the project ships extensive tutorials and documentation; see Getting Started for runnable steps.

---

## Core Features

- **Dialog graph engine** — model conversations as graphs of states with conditional transitions, responses, and processing hooks, keeping complex multi-turn dialog logic declarative and easy to maintain.
- **Asynchronous pipeline orchestration** — run bots through a configurable asynchronous pipeline that wraps the dialog engine with pre- and post-processing services, before/after handlers, timeouts, and optional parallelism, giving you production-style control over the request lifecycle.
- **Pluggable context storage** — persist dialog state in memory, files, Redis, MongoDB, SQL databases, or YDB, so you can move from prototyping to production without changing bot logic.
- **Interchangeable messenger interfaces** — connect the same dialog logic to different communication channels, with console and Telegram support available out of the box.
- **LLM integration and slot extraction** — bring large language models (via LangChain) into conditions and responses, and extract structured slots from user messages to drive data-aware bot behavior.

---

## Installation

**Prerequisites:** requires Python ^3.9,!=3.9.7

Install chatsky-701yr76h using one of the following methods:

**Using PyPi:**

```sh
pip install chatsky
```

---

## Getting Started

**Prerequisites:** Python 3.9–3.12 (3.9.7 is not supported).

**Install:**

```bash
pip install chatsky
```

Optional integrations are available as pip extras, for example `pip install "chatsky[telegram]"` for the Telegram interface or `pip install "chatsky[llm]"` for LLM support. Further extras (e.g. `sqlite`, `redis`, `mongodb`, `postgresql`) add database backends.

**First run:**

1. Define a script: a collection of flows (`Flow`) containing nodes (`Node`), where each node declares its transitions and response.
2. Create a `Pipeline` (exported from the `chatsky` package root), passing the `script` and the required `start_label` — the first node of every context.
3. Run the pipeline. By default it communicates through the console (`CLIMessengerInterface`) and stores dialog contexts in memory (`MemoryContextStorage`), so no external services are needed.

Alternatively, a `Pipeline` can be loaded from a JSON or YAML file with `Pipeline.from_file`.

Complete runnable examples are available as tutorials in the documentation: https://deeppavlov.github.io/chatsky/. To start a new bot project from a prepared layout, use the project template: https://github.com/deeppavlov/chatsky-template.

---

## Architecture

Chatsky is organized as a single Python package built around a dialog-graph engine and an asyncio-based pipeline runtime. Core structures such as the dialog `Context` and `Message` types are Pydantic models.

- **Dialog graph engine** — Conversation logic is defined as a `Script` composed of `Flow`s and `Node`s. Nodes declare transitions, responses, pre-transition and pre-response processing, and metadata, and inherit properties from flow-level and global-level nodes. The `Actor` traverses this graph, evaluating transitions to select the next node and produce responses.

- **Pipeline runtime** — The `Pipeline` is the main executable element. It runs an asyncio-driven service group of pre-services, the `Actor`, and post-services, with before/after handlers, optional timeouts, and optional parallelized processing. It binds the script, a messenger interface, a context storage, slot definitions, and LLM models into a single runnable unit. Pipelines can also be imported from YAML or JSON files via `JSONImporter`.

- **Pluggable context storages** — Dialog context persistence is abstracted behind a storage interface with interchangeable backends: in-memory, file-based, Redis, MongoDB, SQL databases, and YDB. These integrations are enabled through optional dependency extras.

- **Messenger interfaces** — User interaction is handled by interchangeable messenger interfaces, with console and Telegram integrations provided.

- **Script building blocks** — Conditions, responses, destinations, processing functions, and slots form reusable component families covering transition checks, response generation, transition target resolution, pre- and post-processing hooks, and slot extraction.

- **LLM integration** — An optional LangChain-based integration lets pipelines declare named LLM models available to script functions and supports LLM-driven conditions, responses, and slots, including prompt construction and conversation-history filtering.

- **Stats and observability** — A stats module collects pipeline statistics via OpenTelemetry, ships a Superset dashboard configuration, and provides a `chatsky.stats` command-line entry point. Docker assets are included for deploying the monitoring stack.

---

## Testing

The test suite is based on **pytest**, with `pytest-asyncio` for asynchronous tests and `pytest-cov`/`coverage` for coverage measurement (declared in the optional `test` dependency group in `pyproject.toml`).

Test layout under `tests/`:

- `tests/core/` — core engine: script and script parsing, actor, conditions, responses, destinations, transitions, processing, context, message, and node labels.
- `tests/pipeline/` — pipeline behavior: services, validation, the messenger interface, and context updates.
- `tests/context_storages/` — database-backed context storages.
- `tests/slots/`, `tests/llm/`, `tests/stats/`, `tests/messengers/telegram/` — slot extraction, LLM integration, statistics, and the Telegram interface.
- `tests/tutorials/` — tutorial-related tests.
- `tests/utils/` — benchmarking and serialization utilities.

Shared test helpers are provided in `chatsky/utils/testing/` (`common.py`, `toy_script.py`, `cleanup_db.py`); Telegram tutorial test data comes from `utils/test_data_generators/`. Note that dependencies for optional integrations (database drivers, `langchain`, `python-telegram-bot`, OpenTelemetry exporters) are declared as extras in `pyproject.toml`.

The exact local run command is not specified in the repository files available here; the canonical invocations live in the project's own tooling — the helper script `scripts/test.py` and the GitHub Actions workflows `.github/workflows/test_full.yml` (full suite) and `.github/workflows/test_coverage.yml` (coverage). Consult these files and `CONTRIBUTING.md` for contributor guidance.

---

## Examples

Examples of how this should work and how it should be used are available [here](./tutorials).

---

## Documentation

A detailed chatsky-701yr76h description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to chatsky-701yr76h.

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). chatsky-701yr76h repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{chatsky-701yr76h,

        author = {README Benchmark},

        title = {chatsky-701yr76h repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
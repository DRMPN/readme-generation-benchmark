# chatsky-8s0dmazn

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

Chatsky is a Python framework for building conversational AI dialog systems. It provides a pipeline-based architecture in which dialog logic is expressed as a graph of flows and nodes, with pluggable components for context storage, messenger interfaces, and LLM integration. It is intended for developers who build chatbots and conversational agents and want to define dialog behavior programmatically. The repository includes a library API, tutorials covering several topics, and reference documentation; for runnable steps, see the Getting Started section.

---

## Core Features

- **Dialog graph scripting:** Define conversation logic as Flows and Nodes with transitions, responses, and global/local inheritance, so developers can model multi-turn dialogs declaratively.
- **Modular pipeline execution:** Compose pre-services, an actor, and post-services with before/after handlers, so developers can insert custom processing around each dialog turn.
- **Pluggable context storage:** Persist dialog state across multiple backends (in-memory, file, and database options such as MongoDB, Redis, SQL, and YDB), so conversations can be saved and resumed.
- **Messenger integrations:** Connect pipelines to user-facing channels through a messenger interface, including a console interface and a Telegram integration, so the same dialog logic can run on different platforms.
- **Pipeline configuration from files:** Load pipeline definitions from YAML or JSON, so developers can separate dialog configuration from application code.

---

## Installation

**Prerequisites:** requires Python ^3.9,!=3.9.7

Install chatsky-8s0dmazn using one of the following methods:

**Using PyPi:**

```sh
pip install chatsky
```

---

## Getting Started

### Prerequisites

- Python. The minimum supported version is not stated in the provided context. Check `pyproject.toml` for the project's Python requirement.
- Familiarity with the Chatsky `Pipeline`, which requires a `script` and a `start_label`.

### Steps

1. **Get the source code.** The clone URL was not provided in the context, so no clone command is listed here. Use the repository URL from your project's source.
2. **Install dependencies.** Dependencies are declared in `pyproject.toml` and locked in `poetry.lock`. The installation procedure is not documented in the provided context. See the Installation section of this README for setup details.
3. **Explore the examples.** The `tutorials/` directory contains examples grouped by topic: context storages, LLM, messengers, script, service, slots, and stats. Start with the `script` or `service` tutorials to see how a pipeline is built.
4. **Build a pipeline.** A pipeline is created from a script and a start label, for example `Pipeline(script=..., start_label=...)`. Alternatively, `Pipeline.from_file` loads pipeline parameters from a JSON or YAML file.

Run commands for the examples are not documented in the provided context. Consult the tutorials and the documentation in `docs/source/` for execution details.

---

## Architecture

Chatsky is a modular, component-based Python framework. The provided context shows the following major parts and how they interact:

- **Pipeline:** `Pipeline` is the main orchestration element. It composes `pre_services`, the `Actor`, and `post_services` into a services pipeline, with optional before/after handlers and a timeout. The `post_services` group is documented to execute after the `Actor`.
- **Actor and dialog graph:** The `Actor` uses a `Script` made of `Flow`s and `Node`s to select transitions and produce responses. Each node can inherit properties from its flow's local node and from the script's global node.
- **Context:** `Context` stores per-dialog data (labels, requests, responses). It can be connected to a context storage so a conversation can be saved and resumed.
- **Context storages:** `DBContextStorage` defines a common protocol with multiple backends, including memory, file, SQL, MongoDB, Redis, and YDB. Memory is the default.
- **Messenger interfaces:** A common `MessengerInterface` abstraction is implemented by console and Telegram interfaces to receive user input and deliver bot responses.
- **Pluggable components and loading:** Conditions, responses, processing functions, slots, and LLM integration plug into the pipeline. Pipelines can also be loaded from JSON or YAML via `Pipeline.from_file`.
- **Observability (optional):** OpenTelemetry collector configuration, a stats module, and Superset dashboard configuration are present.

The context does not show a distributed or microservices deployment split. Beyond optional Docker and Compose files, deployment topology is not documented here.

---

## Testing

Contributors verify changes by running the test suite in `tests/` and by relying on the CI workflows in `.github/workflows/`.

### Test layout

Tests are organized by component under `tests/`:

- `tests/core/`: core components such as actors, context, scripts, transitions, and conditions
- `tests/context_storages/`: context storage backends
- `tests/pipeline/`: pipeline and service behavior
- `tests/slots/`: slot extraction
- `tests/llm/`: LLM integration
- `tests/messengers/`: messenger interfaces
- `tests/stats/`: statistics and instrumentation
- `tests/tutorials/`: tutorial checks
- `tests/utils/`: utility modules

Shared fixtures are defined in `tests/conftest.py` and in several subpackage `conftest.py` files. Reusable testing helpers are in `chatsky/utils/testing/`.

### Running tests

The repository includes `scripts/test.py`, but its invocation is not documented in the provided context. Refer to `scripts/test.py` and `pyproject.toml` for the exact run command.

### CI checks

- `.github/workflows/test_full.yml`: full test workflow
- `.github/workflows/test_coverage.yml`: test coverage workflow
- `.github/workflows/codestyle.yml`: code style workflow (see `scripts/codestyle.py`)

See `CONTRIBUTING.md` for contribution guidelines.

---

## Examples

Examples of how this should work and how it should be used are available [here](./tutorials).

---

## Documentation

A detailed chatsky-8s0dmazn description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to chatsky-8s0dmazn.

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). chatsky-8s0dmazn repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{chatsky-8s0dmazn,

        author = {README Benchmark},

        title = {chatsky-8s0dmazn repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
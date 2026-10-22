# Chatsky

Chatsky is a Python framework for building conversational agents. It provides tools for defining dialogue flows, managing conversation context, processing messages, integrating language models and data stores, and running agents through different interfaces.

This repository contains the Chatsky package, tutorials, tests, documentation, and examples for integrations and deployment.

## Features

- **Dialogue pipelines:** define scripts, nodes, conditions, transitions, and destinations.
- **Conversation state:** manage context, serialize it, and update parts of it without replacing the whole state.
- **Message processing:** work with text and media, attach pre- and post-processing steps, and handle responses.
- **Slots and extraction:** extract structured information from messages, including with LLM-assisted extractors.
- **LLM integrations:** use prompt utilities, history filters, structured output, and pipeline integration.
- **Database options:** examples and integrations for SQLite, PostgreSQL, MySQL, MongoDB, Redis, and Yandex Database.
- **Interfaces and services:** examples for FastAPI, WebSockets, Streamlit, and Telegram.
- **Observability and benchmarking:** instrumentation, service statistics, database benchmarking, and load-testing examples.

## Installation

Install Chatsky from PyPI:

```bash
pip install chatsky
```

To work with a local checkout, install the project in editable mode:

```bash
git clone <repository-url>
cd chatsky-t5nl53yw
pip install -e .
```

The project also includes a `pyproject.toml` and `poetry.lock` for Poetry-based development. If you use Poetry, install the project and its dependencies with:

```bash
poetry install
```

## Getting started

The tutorials are the best starting point. They progress from basic dialogue construction to more advanced features and integrations. Read them in order where possible:

1. **Dialogue fundamentals:** `1_basics.py`, `2_advanced.py`, `3_groups.py`, and `4_conditions_and_paths.py`
2. **Handlers and transitions:** `5_extra_handlers.py`, `4_transitions.py`, and `9_pre_transition_processing.py`
3. **Context and responses:** `6_context_serialization.py`, `7_pre_response_processing.py`, and `3_responses.py`
4. **Slots and extraction:** the examples in the slot extraction and extractor tutorials
5. **Integrations:** the LLM, database, API, WebSocket, Streamlit, and Telegram tutorials

Tutorial scripts are organized by topic in the repository. Their filenames are listed below; consult the relevant files for complete, runnable examples and any integration-specific setup.

## Repository guide

| Area | Contents |
| --- | --- |
| Tutorials | Dialogue basics, conditions, transitions, slots, LLMs, databases, interfaces, and deployment examples |
| `chatsky` package | Core pipeline, script, message, context, transition, actor, slot, and service functionality |
| `tests` | Unit and integration-oriented tests for pipelines, scripts, messages, contexts, slots, services, and utilities |
| Documentation | Sphinx documentation, user guides, API-reference generation, examples, and tutorials |
| Benchmarking and instrumentation | Benchmark utilities, reporting, OpenTelemetry configuration, and statistics-dashboard assets |
| Configuration and examples | Example pipeline files, YAML configuration, database examples, and Docker Compose configuration |

## Documentation

The documentation sources are included in the repository. They cover getting started, core concepts, pipelines, context, slot extraction, LLM integration, optimization, and other user guides.

Documentation is built with Sphinx. From the documentation directory, use the project’s Sphinx configuration and build setup; for example:

```bash
cd docs
make html
```

The generated site is placed in the Sphinx build output directory.

## Tests

Run the test suite from the project root:

```bash
pytest
```

Tests cover core dialogue behavior as well as serialization, validation, slot processing, database utilities, instrumentation, and other package components. Some integration tests may require external services or optional dependencies.

## Integrations and examples

The repository includes focused examples for several optional components:

- **LLMs:** prompt usage, filtering conversation history, structured output, and pipeline integration.
- **Databases:** SQLite, PostgreSQL, MySQL, MongoDB, Redis, and Yandex Database.
- **Web applications:** FastAPI, WebSocket chat, and Streamlit chat.
- **Load testing:** Locust-based examples and database benchmarking.
- **Monitoring:** OpenTelemetry configuration and dashboard-related assets.

Check each example for its configuration requirements. Some integrations need additional packages, credentials, or a running service.

## Contributing

Contributions are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for project guidance, and use the test suite to check changes before submitting them.

## License

See [`LICENSE`](LICENSE) for the license terms.

# Chatsky

Chatsky is an open-source Python framework for building conversational services, including chatbots and virtual assistants. It provides a domain-specific language (DSL) built from Python functions and data structures to describe dialogue as a graph. A dialogue is organized into **flows**, each containing **nodes**. Nodes define responses and transitions, and conditions determine when the conversation moves between them.

Chatsky also provides tools for processing requests, extracting slots, integrating large language models (LLMs), connecting messenger interfaces, persisting conversation context, and collecting service statistics.

- **Package version in this repository:** 0.10.0
- **Python:** 3.9–3.12 (Python 3.9.7 is excluded)
- **Documentation:** [deeppavlov.github.io/chatsky](https://deeppavlov.github.io/chatsky/)
- **Source code:** [github.com/deeppavlov/chatsky](https://github.com/deeppavlov/chatsky)

## Installation

Install the core package with pip:

```bash
pip install chatsky
```

Optional integrations and features are available through extras. Install the extras you need, for example:

```bash
pip install "chatsky[postgresql]"
pip install "chatsky[telegram]"
pip install "chatsky[llm]"
```

Available extras include `json`, `pickle`, `sqlite`, `redis`, `mongodb`, `mysql`, `postgresql`, `ydb`, `telegram`, `stats`, `benchmark`, `yaml`, and `llm`. These add dependencies for the corresponding storage backends, integrations, or tools. For example, `yaml` enables YAML pipeline imports, `stats` adds statistics dependencies, and `llm` adds LangChain. Provider-specific LLM packages may also be needed for the model you choose.

To install from a clone instead:

```bash
git clone https://github.com/deeppavlov/chatsky.git
cd chatsky
poetry install --all-extras
```

## Quick start

A script is a mapping of flows to nodes. The following example defines a greeting, a response to “Hello!”, and a fallback for other input:

```python
from chatsky import Pipeline, RESPONSE, TRANSITIONS, Transition
import chatsky.conditions as cnd
import chatsky.destinations as dst

script = {
    "main": {
        "start": {
            TRANSITIONS: [
                Transition(dst="greeting", cnd=cnd.ExactMatch("/start"))
            ],
        },
        "greeting": {
            RESPONSE: "Hi!",
            TRANSITIONS: [
                Transition(dst="game", cnd=cnd.ExactMatch("Hello!"))
            ],
        },
        "fallback": {
            RESPONSE: "I didn't understand that.",
            TRANSITIONS: [Transition(dst="greeting")],
        },
        "game": {
            RESPONSE: "Let's play ping-pong!",
        },
    },
}

pipeline = Pipeline(
    script,
    start_label=("main", "start"),
    fallback_label=("main", "fallback"),
)

if __name__ == "__main__":
    pipeline.run()
```

`RESPONSE` defines what a node sends, and `TRANSITIONS` lists the possible next nodes and their conditions. Chatsky includes standard conditions such as `ExactMatch`, `HasText`, and `Regexp`, as well as conditions for slots, services, and LLMs. Responses can be strings, `Message` objects, or callbacks. See the [getting-started guide](https://deeppavlov.github.io/chatsky/latest/get_started.html) and [tutorials](https://deeppavlov.github.io/chatsky/latest/tutorials.html) for fuller examples.

## Features and integrations

- **Conversation context:** Each conversation has a `Context` that tracks requests, responses, node labels, and custom data. Callbacks can access it to read or update conversation state.
- **Context storage:** Chatsky supports in-memory and file-based storage, as well as SQLite, PostgreSQL, MySQL, MongoDB, Redis, and Yandex Database. Database integrations can be constructed from connection URIs using `context_storage_factory`.
- **Slots and processing:** Define slots for extracting values from user messages, then use them in conditions or response templates. Processing callbacks can run before transitions or responses.
- **LLM integration:** Use LangChain-backed models for generated responses and LLM-based conditions. Configure models on a pipeline and reference them by name.
- **Interfaces:** The repository includes console and Telegram messenger components and tutorials for building web interfaces.
- **Statistics:** The stats module supports instrumentation and a preconfigured Apache Superset dashboard backed by ClickHouse and OpenTelemetry.

## Configuration

### Optional dependencies and storage

Storage backends are optional: install the matching extra before using one. For example, `pip install "chatsky[redis]"` installs the Redis dependency. A storage URI identifies the backend and its connection details. Examples include:

```text
json://file.json
redis://:pass@localhost:6379/0
mongodb://admin:pass@localhost:27017/admin
postgresql+asyncpg://postgres:pass@localhost:5432/test
```

For an in-memory context storage, pass an empty string to `context_storage_factory`. See the [context guide](https://deeppavlov.github.io/chatsky/latest/user_guides/context_guide.html) for storage details and additional URI examples.

### Pipeline files

A pipeline can be initialized from JSON or YAML with `Pipeline.from_file`. YAML support requires the `yaml` extra. The import guide describes how to provide custom code and override parameters when loading a file.

### Statistics dashboard

To use the statistics dashboard, install `chatsky[stats]` and start the repository’s stats services with Docker Compose:

```bash
docker compose --profile stats up
```

The `chatsky.stats` command builds and imports a Superset dashboard configuration. It accepts a YAML configuration file and command-line overrides; run `chatsky.stats --help` for options. The shipped dashboard configuration files are intended to be populated by the CLI rather than edited manually.

The repository’s `.env_file` configures Docker services used for development and testing. Review it and `compose.yml` when changing service settings. Do not put real credentials into shared configuration or expose passwords in command history; the stats CLI supports interactive password entry.

## Development

Contributions are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for pull request, branch, and commit guidance. The project uses Poetry and Poe the Poet for dependency management and task commands.

For a development environment with linting, tests, tutorials, docs, and all optional integrations:

```bash
poetry install --with lint,test,devel,tutorials,docs --all-extras
```

Useful development tasks include:

```bash
poetry run poe info
poetry run poe lint
poetry run poe format
poetry run poe docs
```

`lint` runs the configured Flake8 and Black checks; `format` applies Black formatting. Building the full documentation requires Pandoc and Docker on Linux. `poetry run poe docs_no_docker` builds without Docker, but tutorials that depend on Docker services may report errors, and Draw.io diagrams are not built.

## Testing

Tests are in `tests/`. The test tasks load settings from `.env_file`. Run the quick suite for a fast check without Docker-dependent or slow tests:

```bash
poetry run poe quick_test
```

For unit tests without coverage, use:

```bash
poetry run poe test_no_cov
```

To run the full test suite, including integrations that require Docker services:

```bash
poetry run poe test_all
```

The full run requires Docker and Docker Compose. It starts the repository’s configured services and generates an HTML coverage report in `htmlcov/`. The quick coverage task is available as `poetry run poe quick_test_coverage`; its report may be incomplete because some tests are deselected.

To start the database services used for context-storage integration tests manually:

```bash
docker compose --profile context_storage up
```

## Documentation and support

The documentation includes guides for basic concepts, context, LLM integration, slot extraction, optimization, Superset, and pipeline imports, as well as API references and runnable tutorials. Questions and feedback can be shared through [GitHub Issues](https://github.com/deeppavlov/chatsky/issues), the [DeepPavlov Forum](https://forum.deeppavlov.ai), or the [DeepPavlov Telegram group](https://t.me/DeepPavlovDreamDiscussions).

## License

Chatsky is licensed under the **Apache License, Version 2.0**. See [`LICENSE`](LICENSE) for the license terms.

# Chatsky

Chatsky is a free and open-source software stack for creating chatbots, released under the Apache License 2.0. It is developed by the Chatsky development department of [DeepPavlov](https://deeppavlov.ai). The current package version is `0.10.0`.

Chatsky provides a domain-specific language based on standard Python functions and data structures for describing a dialog as a graph. A script is organized into flows, flows contain nodes, and nodes define the bot's response and the transitions to other nodes. A `Pipeline` traverses this graph as user requests arrive.

## Features

Based on the supplied documentation and source files, Chatsky includes:

- **Dialog graph DSL**: Scripts made of flows and nodes, with `RESPONSE` and `TRANSITIONS` keywords, plus `PRE_RESPONSE` and `PRE_TRANSITION` processing.
- **Conditions, destinations, and responses**: Built-in modules `chatsky.conditions` (`cnd`), `chatsky.destinations` (`dst`), `chatsky.responses` (`rsp`), and `chatsky.processing` (`proc`).
- **Context management**: A `Context` object that stores labels, requests, responses, `misc` data, and turn history.
- **Context storages**: In-memory, JSON, pickle, shelve, SQLite, PostgreSQL, MySQL, MongoDB, Redis, and Yandex Database backends.
- **Slot extraction**: `RegexpSlot`, `FunctionSlot`, `GroupSlot`, and slot-related processing and conditions.
- **LLM integration**: `LLM_API` wrapper around LangChain models, `LLMResponse`, and `LLMCondition`.
- **Messenger interfaces**: Console and Telegram interfaces, with tutorials for FastAPI, WebSocket, and Streamlit.
- **Statistics**: The `chatsky.stats` module and command-line tool for collecting telemetry and configuring a Superset dashboard.
- **Pipeline YAML/JSON import**: `Pipeline.from_file` for building pipelines from configuration files.
- **Testing utilities**: `chatsky.utils.testing`, including `check_happy_path` for end-to-end dialog tests.
- **Benchmarking**: A database benchmark utility under `chatsky.utils.db_benchmark`.

## Installation

Chatsky requires Python `^3.9` (excluding `3.9.7`). The package classifiers list support for Python 3.9 through 3.12.

Install the core package from PyPI:

```bash
pip install chatsky
```

Optional dependencies are available as extras:

```bash
pip install chatsky[json]        # JSON context storage
pip install chatsky[pickle]      # Pickle context storage
pip install chatsky[sqlite]      # SQLite backend
pip install chatsky[redis]       # Redis backend
pip install chatsky[mongodb]     # MongoDB backend
pip install chatsky[mysql]       # MySQL backend
pip install chatsky[postgresql]  # PostgreSQL backend
pip install chatsky[ydb]         # Yandex Database backend
pip install chatsky[telegram]    # Telegram interface
pip install chatsky[stats]       # Statistics collection and CLI
pip install chatsky[benchmark]   # Database benchmarking
pip install chatsky[yaml]        # YAML pipeline files
pip install chatsky[llm]         # LLM integration via LangChain
```

The core dependencies are `pydantic>=2.0`, `nest-asyncio`, `typing-extensions`, `eval_type_backport`, `wrapt`, and `colorama`.

To work from source, clone the repository and install all extras with Poetry:

```bash
git clone https://github.com/deeppavlov/chatsky.git
cd chatsky
poetry install --all-extras
```

For a ready-to-use starting point, the project documentation refers to the [Chatsky Project Template](https://github.com/deeppavlov/chatsky-template).

## Quick Start

The following example, taken from the basic concepts guide, implements a small ping-pong dialog. The bot replies `Pong!` to `Ping!` and treats other input as a rule violation.

```python
from chatsky import Pipeline, TRANSITIONS, RESPONSE, Transition as Tr
import chatsky.conditions as cnd
import chatsky.destinations as dst

ping_pong_script = {
    "greeting_flow": {
        "start_node": {
            TRANSITIONS: [Tr(dst="greeting_node", cnd=cnd.ExactMatch("/start"))]
        },
        "greeting_node": {
            RESPONSE: "Hi!",
            TRANSITIONS: [
                Tr(
                    dst=("ping_pong_flow", "game_start_node"),
                    cnd=cnd.ExactMatch("Hello!")
                )
            ]
        },
        "fallback_node": {
            RESPONSE: "That was against the rules",
            TRANSITIONS: [Tr(dst="greeting_node")],
        },
    },
    "ping_pong_flow": {
        "game_start_node": {
            RESPONSE: "Let's play ping-pong!",
            TRANSITIONS: [Tr(dst="response_node", cnd=cnd.ExactMatch("Ping!"))],
        },
        "response_node": {
            RESPONSE: "Pong!",
            TRANSITIONS: [Tr(dst=dst.Current(), cnd=cnd.ExactMatch("Ping!"))],
        },
    },
}

pipeline = Pipeline(
    ping_pong_script,
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
)

if __name__ == "__main__":
    pipeline.run()
```

The script has three levels: script, flow, and node. Each turn, the pipeline obtains the user request, travels to the next node based on the current node's transitions, and sends that node's response.

## Usage

### Testing a dialog

Chatsky provides `check_happy_path` to verify a pipeline against a sequence of request-response pairs:

```python
from chatsky.utils.testing.common import check_happy_path

happy_path = (
    ("/start", "Hi!"),
    ("Hello!", "Let's play ping-pong!"),
    ("Ping!", "Pong!"),
)

check_happy_path(pipeline, happy_path)
```

### Context storages

Persistent storage is created with `context_storage_factory`, which takes a connection URI. Examples from the source documentation include:

- `json://file.json`
- `sqlite+aiosqlite:////file.db`
- `redis://:pass@localhost:6379/0`
- `mongodb://admin:pass@localhost:27017/admin`
- `mysql+asyncmy://root:pass@localhost:3307/test`
- `postgresql+asyncpg://postgres:pass@localhost:5432/test`
- `grpc://localhost:2136/local` (Yandex Database)

An empty string selects the in-memory storage. The `tutorials/context_storages` directory contains examples for each backend.

### LLM integration

Models are wrapped with `LLM_API` and passed to the pipeline's `models` parameter. Responses are generated with `rsp.LLMResponse`, and transitions can be guided by `cnd.LLMCondition` with a method such as `Contains`. History is controlled with the `history` parameter and filters such as `IsImportant`. Prompts are ordered by a `PositionConfig`.

### Slot extraction

Slots are declared with classes such as `RegexpSlot` and `FunctionSlot`, grouped with `GroupSlot`, and passed to the pipeline's `slots` argument. Values are extracted with `proc.Extract` at `PRE_TRANSITION`, checked with `cnd.SlotsExtracted`, and inserted into responses with `proc.FillTemplate` or `rsp.FilledTemplate`.

### Loading a pipeline from a file

`Pipeline.from_file` accepts a JSON or YAML file whose keys are pipeline initialization parameters. Strings prefixed with `chatsky.`, `custom.`, or `external:` are resolved to objects. The `utils/pipeline_yaml_import_example` directory contains a complete example.

### Statistics and dashboards

The `chatsky.stats` command creates a configuration archive for a Superset dashboard and uploads it to a running Superset server. Using the example configuration in `tutorials/stats/example_config.yaml`:

```bash
chatsky.stats tutorials/stats/example_config.yaml -P superset -dP pass -U superset --outfile=config_artifact.zip
```

The documentation recommends omitting `-P` and `-dP` to be prompted for passwords interactively. Telemetry is stored in ClickHouse and collected through an OpenTelemetry Collector. The dashboard is available at `http://localhost:8088/` once the `stats` Docker profile is running.

### Tutorials and examples

The `tutorials/` directory covers context storages, LLM usage, Telegram and web interfaces, scripts, services, slots, and statistics. The `utils/` directory contains a stats sample data provider, a database benchmark script with a Streamlit interface, and a pipeline YAML import example.

## Configuration

### Environment file

Tests and Docker services read configuration from `.env_file`. The database services in `compose.yml` load it with `env_file`, and the documentation notes that the Superset username and password default to `superset` and can be changed there.

### Docker Compose

`compose.yml` defines services grouped by profile:

- `context_storage`: MySQL, PostgreSQL, Redis, MongoDB, and YDB.
- `stats`: Superset dashboard (`dashboard`), its metadata database, ClickHouse, and an OpenTelemetry Collector.
- `extras`: A DeepPavlov NER service on port 5000.

Start the databases with:

```bash
docker compose --profile context_storage up
```

Start the statistics stack with:

```bash
docker compose --profile stats up
```

### Dashboard configuration

Files under `chatsky/config/superset_dashboard/` define the dashboard, charts, datasets, and database connection. The directory's README states that these files should not be edited manually; placeholders are filled by `chatsky.stats`.

### Tool configuration

Project tooling is configured in `pyproject.toml`, including the `poe` task definitions, pytest markers, coverage exclusions, and the isort profile (`black`).

## Development

Development uses Poetry and poethepoet. Install the development environment with:

```bash
poetry install --with lint,test,devel,tutorials,docs --all-extras
```

Run `poetry run poe info` to list the available commands. The main tasks are:

| Command | Purpose |
| --- | --- |
| `poetry run poe lint` | Run flake8 and black checks |
| `poetry run poe format` | Format code with black |
| `poetry run poe quick_test` | Run tests without Docker and excluding slow tests |
| `poetry run poe quick_test_coverage` | Quick tests with an HTML coverage report |
| `poetry run poe test_no_cov` | Run tests without coverage |
| `poetry run poe test_all` | Run all tests, including Docker-backed integration tests |
| `poetry run poe test_no_deps` | Run tests with all dependency-dependent tests skipped |
| `poetry run poe docs` | Build Sphinx documentation (Docker required) |
| `poetry run poe docs_no_docker` | Build documentation without Docker |
| `poetry run poe clean` | Remove build and cache artifacts |

Documentation is written in reStructuredText using the Sphinx toolchain, and building it requires `pandoc`. The output is placed in `docs/build`.

The repository uses GitHub Actions workflows for linting, testing across Python 3.9 to 3.12 on Linux, macOS, and Windows, documentation publishing, release builds, and dashboard image publishing.

Contributions should follow [CONTRIBUTING.md](CONTRIBUTING.md), which describes branch and commit message conventions, the Poetry workflow, and the documentation directives available in tutorials. The pull request template asks contributors to add tests, update the API reference, tutorials, and guides, and update `CONTRIBUTING.md` when the development workflow changes.

## Testing

Tests live in `tests/` and run with pytest. The `pytest` configuration uses `--strict-markers` and `asyncio_mode = "auto"`. Defined markers are:

- `docker`: requires Docker containers.
- `slow`: takes more than a minute.
- `no_coverage`: cannot run under coverage or does not affect coverage stats.
- `needs_dependencies`: requires optional extras.

Tests that skip are reported as failures when `--allow-skip` restricts skipping, as configured in `tests/conftest.py`. The coverage run in `scripts/test.py` has a threshold of 90 percent.

## Documentation

The full documentation is published at [https://deeppavlov.github.io/chatsky/](https://deeppavlov.github.io/chatsky/). It includes:

- Getting started and basic concepts.
- User guides on the LLM integration, slot extraction, the `Context` object, Superset, optimization, and YAML import.
- Tutorials and the API reference.

Community resources linked from the documentation include the DeepPavlov Forum, a Telegram group, GitHub Issues, and Stack Overflow under the `chatsky` tag.

## Project Roadmap and Releases

The documentation links to the project's GitHub milestones for planned work and to GitHub releases for release notes.

## License

Chatsky is licensed under the [Apache License, Version 2.0](LICENSE). The license file states:

> Copyright 2022 Neural Systems and Deep Learning Laboratory, Moscow Institute of Physics and Technology

You may obtain a copy of the License at `http://www.apache.org/licenses/LICENSE-2.0`.

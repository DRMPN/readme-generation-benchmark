# Pythagora Core

Pythagora Core is the Python engine behind Pythagora, an AI-assisted application-building tool. It turns a user’s app description into a project specification, plans an architecture, and coordinates agents that generate and modify project files. During development, the workflow can also run commands, collect user input, and support troubleshooting and bug-fixing iterations.

The engine uses configurable large-language-model (LLM) providers and stores project history and state in a database. It includes starter templates for several JavaScript and React application structures, as well as command-line and user-interface integration code.

## What’s in the repository

- `core/agents/` contains agents for specification writing, architecture, frontend and backend development, command execution, troubleshooting, and related tasks.
- `core/llm/` contains the provider clients, prompt and conversation handling, parsing, and request logging.
- `core/prompts/` contains the prompt templates used by agents.
- `core/db/` contains database models, session setup, and Alembic migrations.
- `core/state/`, `core/disk/`, and `core/proc/` manage project state, files, and processes.
- `core/templates/` contains project templates and their starter files.
- `core/cli/` and `core/ui/` contain the command-line entry point and UI integration.
- `tests/` contains unit tests and provider integration tests.
- `cloud/` and `Dockerfile` contain files for a cloud workspace image that includes code-server and a preinstalled Pythagora VS Code extension.

## Requirements

The Python package declares support for Python `^3.9`; CI tests Python 3.9 and 3.12. Runtime dependencies are listed in `requirements.txt` and `pyproject.toml`. Development dependencies include pytest, Ruff, pytest-cov, pytest-asyncio, pytest-timeout, and pre-commit.

Pythagora generates JavaScript projects using Node.js and npm. Install those tools as appropriate for the projects you intend to build. The cloud image setup installs Python 3.12 and Node.js.

## Setup

### Install with Poetry

From the repository root:

```bash
python -m pip install poetry
poetry install --with=dev
```

Run project commands inside the Poetry environment with `poetry run`.

### Install with a virtual environment

Alternatively, create a virtual environment and install the pinned requirements:

```bash
python -m venv venv
```

Activate it, then run:

```bash
python -m pip install -r requirements.txt
```

The application entry point is `main.py`. If required imports are missing, it prints instructions for creating a virtual environment and installing `requirements.txt`.

## Configuration

`example-config.json` documents the main configuration areas:

- **`llm`**: Provider connection settings such as base URL, API key, and connection and read timeouts. Examples are provided for OpenAI, Anthropic, and Azure. The file notes that OpenRouter and local LLM servers can also be configured through the OpenAI provider.
- **`agent`**: Default provider, model, and temperature. Agent-specific model settings can also be defined.
- **`log`**: Log level, format, and output destination.
- **`db`**: Database URL and SQL debugging option. The example uses SQLite with the `aiosqlite` driver.
- **`ui`**: UI type.
- **`fs`**: Filesystem type, workspace root, ignored paths, and a file-size threshold.

Use the example file as a reference when preparing configuration for your environment. It contains placeholder credentials; supply valid provider credentials for the services you choose. The CLI includes a configuration-display action, but the precise configuration search and override rules are defined in the configuration modules.

Telemetry can be disabled by setting `telemetry.enabled` to `false` in `~/.gpt-pilot/config.json`. See [`docs/TELEMETRY.md`](docs/TELEMETRY.md) for the telemetry description and opt-out instructions.

## Usage

Start the command-line application from the repository root:

```bash
python main.py
```

The CLI initializes the UI and database, then starts or resumes a Pythagora session. For a new project, the workflow asks what you want to build and prompts for an app description. It then coordinates the agents through specification and project implementation. The CLI also has actions for listing projects, showing configuration, importing a legacy database, and deleting a project; consult the CLI’s help or implementation for the exact arguments.

The source includes frontend-only and full-stack project paths. The new-project UI offers a full-stack option and a frontend-only option for projects that use an OpenAPI/Swagger backend. Generated frontend projects may use Vite and React; included starter structures also cover Node/Express applications.

### Cloud image

The Dockerfile builds a cloud development workspace based on Ubuntu 22.04. It installs Python, Node.js, MongoDB, and code-server, and configures a workspace directory and application data directory. The build expects `pythagora-vs-code.vsix` in its build context; that file is not included in the listed repository tree. The image’s entry point starts the extension-install script and keeps the container running. Ports `27017`, `8000`, `8080`, `5173`, and `3000` are exposed in the image definition.

## Development

The project uses Poetry for packaging and dependency management. Python package metadata and tool settings are in `pyproject.toml`; Ruff is configured with a 120-character line length and import sorting.

Run the linter and formatter checks with:

```bash
poetry run ruff check
poetry run ruff format --check --diff
```

To apply Ruff’s formatting, run:

```bash
poetry run ruff format
```

The pre-commit configuration also runs Ruff with automatic fixes and formatting, checks Alembic migration status, and runs pytest. Install the development dependencies before using those hooks.

Database schema changes are managed with Alembic. The repository’s pre-commit hook runs:

```bash
alembic -c core/db/alembic.ini check
```

Review the existing migration files and database setup code when changing models or migrations.

## Testing

Run the test suite with:

```bash
poetry run pytest
```

Or, when using a virtual environment with development dependencies installed:

```bash
pytest
```

Pytest is configured to run quietly, collect coverage for `core`, and apply a 10-second test timeout. Tests include unit coverage for agents, configuration, the CLI, database models, filesystem behavior, LLM handling, state, templates, telemetry, and UI components. The `tests/integration/llm/` tests exercise provider integrations and may require provider credentials or external connectivity.

## Contributing

The repository includes issue templates for bug reports, feature requests, and usage questions, along with a Code of Conduct. The contribution guide is present but contains no additional instructions. Please follow the Code of Conduct when participating in project discussions.

## License

This project is licensed under the **Functional Source License, Version 1.1, MIT Future License (FSL-1.1-MIT)**. The current grant permits use, modification, and redistribution for permitted purposes, but excludes competing uses as defined in [`LICENSE`](LICENSE). The license also grants an MIT license effective on the second anniversary of the date the software is made available. Read the license text for the full terms, conditions, and limitations.

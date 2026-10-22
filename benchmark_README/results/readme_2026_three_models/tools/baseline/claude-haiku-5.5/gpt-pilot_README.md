# Pythagora Core

Pythagora Core (`pythagora-core`, version 1.3.25) is a Python application for building complete apps with AI agents. It is the core engine behind Pythagora. The repository also references GPT Pilot in its issue templates and documentation links.

## Overview

Pythagora takes an app description from the user and coordinates a set of agents to produce the project. The agents in `core/agents/` include:

- **Spec Writer** and **Wizard**: gather and refine the project description.
- **Architect**: selects project templates and chooses technologies and dependencies.
- **Tech Lead**: breaks the project into epics and tasks.
- **Developer** and **Code Monkey**: break tasks into steps and write files.
- **Frontend**: builds the frontend.
- **Executor**: runs shell commands for the project.
- **Troubleshooter**, **Bug Hunter**, **Problem Solver**, and **Error Handler**: diagnose and fix problems.
- **Technical Writer**, **Task Completer**, **External Docs**, and **Importer** (for existing projects) handle documentation, task completion, external documentation, and importing.

The **Orchestrator** (`core/agents/orchestrator.py`) decides which agent runs based on the current project state and commits state to the database.

Project state is stored through SQLAlchemy with asyncio support. The default database is SQLite via `aiosqlite`, and migrations are managed with Alembic. Project files are handled through a virtual file system layer (`core/disk/`).

LLM providers are implemented in `core/llm/`: OpenAI, Anthropic, Azure, Groq, and Relace.

## Requirements

From `pyproject.toml` and `requirements.txt`:

- Python 3.9 or later (`python = "^3.9"`). CI runs on Python 3.9 and 3.12.
- Pinned runtime dependencies in `requirements.txt`, including `openai`, `anthropic`, `groq`, `sqlalchemy`, `alembic`, `pydantic`, `jinja2`, `httpx`, and `prompt-toolkit`.
- API credentials for at least one supported LLM provider.

## Installation

### Local setup

1. Clone the repository and change into it.
2. Create a virtual environment in the project root. `main.py` expects it at `venv/`:

   ```bash
   python3 -m venv venv
   ```

3. Activate it and install the dependencies:

   ```bash
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Create your configuration file (see [Configuration](#configuration)).

If the required modules are missing, `main.py` prints setup instructions and exits with status 255.

### Docker

The `Dockerfile` builds an Ubuntu 22.04 image that includes the application, Python 3.12, Node.js, MongoDB, and code-server. The build copies `pythagora-vs-code.vsix` into `/var/init_data/`, so that file must be in the build context. The CI workflow copies it from the extension repository before building:

```bash
cp ../tmp_extension/*.vsix ./pythagora-vs-code.vsix
docker build --platform=linux/amd64 -f Dockerfile -t <image-name> .
```

The image exposes ports `27017`, `8000`, `8080`, `5173`, and `3000`. Its entrypoint (`cloud/entrypoint.sh`) starts the VS Code extension installer and keeps the container running. The image uses `cloud/config-docker.json` as its `config.json`, sets the workspace to `/pythagora/pythagora-core/workspace`, and creates a user named `devuser`.

## Usage

Run the application from the project root:

```bash
python main.py
```

`main.py` calls `core.cli.main.run_pythagora()`. The following command-line options are referenced in `core/cli/main.py`:

| Option | Purpose |
|---|---|
| `--list` | List projects, branches, and states |
| `--list-json` | List projects in JSON format |
| `--show-config` | Display the current configuration |
| `--import-v0 <path>` | Import a legacy (v0) database |
| `--delete <project>` | Delete a project |
| `--project`, `--branch`, `--step`, `--project-state-id` | Continue an existing project from a given point |
| `--email` | User email, used with Sentry and telemetry |
| `--access-token` | Access token for the session |
| `--auto-confirm-breakdown` | Skip the breakdown confirmation chat |
| `--use-git` | Enable git integration in the orchestrator |

When `initial_prompt` is provided, the CLI starts a new project and skips the stack selection question. Without it, the user chooses between a full-stack app ("node") and a frontend-only app ("swagger").

## Configuration

Configuration is read from a JSON file. `example-config.json` documents the available sections. The file supports `//` comments. Copy it and replace the placeholder values.

Main sections:

- **`llm`**: Provider settings for `openai`, `anthropic`, and `azure`. Each provider has `base_url`, `api_key`, `connect_timeout`, and `read_timeout`. Azure also takes an `extra` block with `azure_deployment` and `api_version`. The example notes that OpenRouter and local servers such as LM-Studio work through the `openai` provider.
- **`agent`**: Per-agent model settings. The `default` entry sets the provider, model, and temperature. Other keys match agent class names, such as `CodeMonkey` or `Developer.parse_task`. `cloud/config-docker.json` also configures the `relace` provider for `CodeMonkey.implement_changes`.
- **`log`**: `level`, `format`, and `output`. The default output is `pythagora.log`. Setting `output` to `null` sends logs to stdout.
- **`db`**: `url` and `debug_sql`. The default URL is `sqlite+aiosqlite:///data/database/pythagora.db`. `cloud/config-docker.json` also sets `save_llm_requests`. The database code converts `postgresql+asyncpg://` and `sqlite+aiosqlite://` URLs to synchronous forms for migrations.
- **`ui`**: `type`, set to `"plain"` in both example configs. The `core/ui/` directory also contains `api_server.py`, `console.py`, `ipc_client.py`, and `virtual.py`.
- **`fs`**: `type` (`local`), `workspace_root` (where projects are stored, default `workspace`), `ignore_paths` (patterns excluded when examining project files), and `ignore_size_threshold` (files larger than this are ignored, default 50000 bytes).
- **`prompt`**: `paths` to the prompt template directories. The Docker config sets this to `/pythagora/pythagora-core/core/prompts`.

The Docker configuration also includes `relace` provider settings and `save_llm_requests`.

### Telemetry

According to `docs/TELEMETRY.md`, Pythagora collects anonymous telemetry, including runtime, LLM request counts, operating system, Python version, and the project's initial prompt and architecture. To opt out, set `telemetry.enabled` to `false` in `~/.gpt-pilot/config.json`. The documentation says that file location, which differs from the example config, so verify it against the code if you rely on it. The test suite sets `DISABLE_TELEMETRY=1` in `tests/conftest.py`.

## Project Templates

`core/templates/` contains starter templates that the Architect can select:

- `javascript_react`
- `node_express_mongoose`
- `react_express`
- `vite_react`
- `vite_react_swagger`

Each template has a Python definition, a file tree under `core/templates/tree/`, and a summary under `core/templates/info/`.

## Development

Dependencies are managed with Poetry (`pyproject.toml`) and pinned in `requirements.txt`. To set up a development environment:

```bash
python -m pip install poetry
poetry install --with=dev
```

Code quality tools:

- **Ruff** is configured in `pyproject.toml` with a line length of 120, a target of `py39`, and import sorting (`I`).
- **pre-commit** (`.pre-commit-config.yaml`) runs `ruff --fix`, `ruff-format`, an Alembic migration check (`alembic -c core/db/alembic.ini check`), and `pytest` on commit.

Database migrations live in `core/db/migrations/`. `core/db/setup.py` runs them at startup with `command.upgrade(alembic_cfg, "head")`.

The CI workflow (`.github/workflows/ci.yml`) runs on pushes to `main` and on pull requests to `main` and `rewrite`. It tests Python 3.9 and 3.12 on Ubuntu, macOS, and Windows, and runs `ruff check`, `ruff format --check`, and `pytest`.

## Testing

Tests are in `tests/`, organized by component (agents, cli, config, db, disk, llm, log, proc, state, telemetry, templates, ui). Shared fixtures in `tests/conftest.py` provide an in-memory SQLite database, a `StateManager` with an in-memory file system, and a mocked LLM.

Run the tests with:

```bash
poetry run pytest
```

The pytest configuration in `pyproject.toml` runs with `-ra -q --cov=core --no-cov-on-fail --timeout 10`, which sets a 10-second timeout per test and reports coverage for `core`. Integration tests for Anthropic, Groq, and OpenAI are in `tests/integration/llm/`. This README does not document their required credentials.

## Contributing

Contribution guidance is provided through `.github/CONTRIBUTING.md` (currently empty in this repository), `.github/CODE_OF_CONDUCT.md`, and issue templates for bug reports, feature requests, and how-to questions. The Code of Conduct is adapted from the Contributor Covenant, version 2.0. Its enforcement contact is still a placeholder (`[INSERT CONTACT METHOD]`). Ownership is defined in `.github/CODEOWNERS`.

The `CHANGELOG.md` currently contains only a date heading.

## License

This project is licensed under the **Functional Source License, Version 1.1, MIT Future License (FSL-1.1-MIT)**, copyright 2024 Pythagora Technologies, Inc. See [LICENSE](LICENSE) for the full terms.

In summary:

- You may use, copy, modify, and redistribute the software for any Permitted Purpose. This excludes a Competing Use, which means offering the software in a commercial product or service that substitutes for or offers substantially similar functionality to it. Internal use, non-commercial education, non-commercial research, and certain professional services are permitted.
- Redistributions must include the license terms and retain copyright notices.
- The software is provided "as is," without warranties.
- Two years after the software is made available, the license grants the right to use it under the MIT license.

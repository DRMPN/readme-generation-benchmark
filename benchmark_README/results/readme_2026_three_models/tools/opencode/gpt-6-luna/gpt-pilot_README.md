# Pythagora Core

Pythagora Core is a Python command-line application that uses LLM-backed agents to create and continue software projects. It guides a project through a specification and implementation workflow, interacts with the user through a console UI or an IPC UI, and stores project history in a database.

The package metadata identifies this repository as `pythagora-core`; the executable entry point in the source tree is `main.py`.

## Requirements

- Python 3.9 or newer
- An API key and model access for the LLM provider you configure
- Node.js/npm for generated project templates that run their `npm install` hook

The default database is SQLite through `aiosqlite`. The configuration model also accepts PostgreSQL through `asyncpg` when that driver is installed.

## Setup

From the repository root, create an environment and install the pinned dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Create a local configuration from the included example and edit it to set credentials and preferences:

```sh
cp example-config.json config.json
```

`example-config.json` contains line comments; the configuration loader supports these comments. Set an API key under the relevant provider in the `llm` section, or use the provider's environment-based credentials, and set the provider and model under `agent.default`. The example includes OpenAI, Anthropic, and Azure-shaped configuration. The code defines clients/configuration for OpenAI-compatible endpoints, Azure, Anthropic, Groq, and Relace; consult the provider's API requirements when choosing a model and endpoint. The `openai` provider configuration can also specify a compatible custom `base_url`.

The default configuration uses a plain console UI, SQLite, and a `workspace` directory for generated projects. Use `--config` to load a configuration from another path. Avoid committing real API keys or other secrets.

## Run

Start an interactive session:

```sh
python main.py
```

The console asks what to build and offers a full-stack app or a frontend for an existing OpenAPI/Swagger backend. To pass a project description directly and start without the initial stack question:

```sh
python main.py --initial-prompt "A task tracker with projects and due dates"
```

Useful commands:

```sh
python main.py --help
python main.py --version
python main.py --show-config
python main.py --list
python main.py --list-json
```

`--list` prints projects, branches, and their last step; `--list-json` prints project information as JSON. To continue an existing project, pass its UUID with `--project`; `--branch`, `--step`, and `--project-state-id` can select a branch or saved state:

```sh
python main.py --project PROJECT_UUID
python main.py --project PROJECT_UUID --branch BRANCH_UUID --step 4
```

Other options include `--delete PROJECT_UUID`, `--use-git`, `--no-auto-confirm-breakdown`, `--llm-key PROVIDER:KEY`, `--llm-endpoint PROVIDER:URL`, `--database URL`, and `--level LEVEL`. Use `python main.py --help` for the complete option list. The local IPC server is enabled by default and can be configured with `--local-api-server-host` and `--local-api-server-port`.

## Configuration

The default configuration file path is `config.json` in the current working directory. If that file is missing, the application reports the missing file and uses built-in defaults. A partial JSON configuration may override only the settings that need changing. See [`example-config.json`](example-config.json) for the available sections:

- `llm`: provider credentials, base URLs, timeouts, and provider-specific options.
- `agent`: provider, model, and temperature by agent; agents without their own entry use `default`.
- `db`: database URL and SQL logging options.
- `ui`: plain console, IPC client, or virtual UI configuration.
- `fs`: workspace directory and file/directory ignore rules.
- `log`: log level, format, and output file.

`--show-config` prints built-in defaults, not the contents of a selected configuration file. CLI options such as `--database`, `--level`, `--llm-key`, and `--llm-endpoint` override the corresponding loaded settings for that run.

Global telemetry preferences are stored separately from `config.json`, under the platform's Pythagora user configuration directory. Telemetry is enabled by default in the implementation and can be disabled by setting `telemetry.enabled` to `false` in that global settings file, or by setting the `DISABLE_TELEMETRY` environment variable. See [`docs/TELEMETRY.md`](docs/TELEMETRY.md) for the repository's telemetry documentation and [`core/config/user_settings.py`](core/config/user_settings.py) for how the global settings path is resolved.

## Included templates

The template registry currently contains:

- `vite_react`: a Vite/React frontend with Tailwind CSS and TypeScript, alongside a Node.js/Express backend template with MongoDB support.
- `vite_react_swagger`: a Vite/React frontend intended to work with an existing OpenAPI/Swagger backend.

Both include Shadcn UI components and run an `npm install` install hook. Other template source files exist in the repository, but are not all enabled in the template registry.

## Development and tests

Install the project and its development dependencies with Poetry, then run the test suite:

```sh
poetry install
poetry run pytest
```

The test suite is under `tests/`; pytest configuration and coverage options are in `pyproject.toml`.

## Repository layout

- `main.py` — command-line entry point.
- `core/agents/` — project workflow, planning, coding, troubleshooting, and supporting agents.
- `core/llm/` — LLM client implementations, prompts/conversation handling, and request parsing.
- `core/config/` — application configuration and user settings.
- `core/db/` — database models, session management, and migrations.
- `core/state/` — project state and workflow management.
- `core/templates/` — template registry, rendering code, and generated-project source trees.
- `core/ui/` — console, IPC, and virtual UI adapters.
- `tests/` — unit and integration tests.

## License

This repository is licensed under the Functional Source License, Version 1.1, MIT Future License (`FSL-1.1-MIT`). See [`LICENSE`](LICENSE) for the full terms.

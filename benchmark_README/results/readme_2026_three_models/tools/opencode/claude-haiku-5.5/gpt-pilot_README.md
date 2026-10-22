# Pythagora Core

Pythagora Core is a Python engine that builds complete applications with AI agents. You describe the app you want, and a set of agents writes a specification, plans the work, writes and edits code, runs commands, and debugs the result inside a local project workspace.

It is the core of the Pythagora tool, a successor to the original GPT Pilot project. The package is named `pythagora-core` (version 1.3.25 in `pyproject.toml`). The core is driven from the command line (`main.py`) and can also be driven by a UI client over a local IPC connection. The VS Code extension that uses that connection is a separate project and is not in this repository.

## Features

- Interactive project creation: when started without a project, Pythagora asks what you want to build and offers a full-stack app or a frontend-only app that works with an existing OpenAPI/Swagger backend.
- Multi-agent workflow with agents for specification writing, architecture, technical planning, development, code editing, command execution, bug hunting, and troubleshooting (see [Architecture](#architecture)).
- Pluggable LLM providers: OpenAI, Anthropic, Azure OpenAI, Groq, and Relace, with per-agent provider and model selection.
- Project state stored in a database, so you can list, resume, and delete projects, and load a project at a specific branch, step, or project state.
- Optional Git version control for generated projects (`--use-git`).
- Project templates built on Vite, React, and TypeScript; see [Project templates](#project-templates).
- Optional local IPC server for external UI clients.
- Built-in telemetry, which is enabled by default and can be turned off (see [Telemetry](#telemetry)).

## Requirements

- Python 3.9 or newer. `pyproject.toml` requires `^3.9`, and CI runs the test suite on Python 3.9 and 3.12 on Ubuntu, macOS, and Windows.
- An API key for at least one supported LLM provider.
- Git, only if you use `--use-git`.
- Node.js and npm are needed for the generated frontend projects. The Vite template runs `npm install` as part of its setup.

## Installation

Clone the repository and create a virtual environment in the project directory:

```bash
git clone https://github.com/Pythagora-io/pythagora-core.git
cd pythagora-core
python3 -m venv venv
```

Install the dependencies into the virtual environment:

```bash
# Linux / macOS
venv/bin/python -m pip install -r requirements.txt

# Windows
venv\Scripts\python -m pip install -r requirements.txt
```

## Configuration

Pythagora reads its configuration from `config.json` in the current working directory by default. Create it from the example:

```bash
cp example-config.json config.json
```

Then edit `config.json` and set the API key for the provider you use. The example file ships with `"api_key": "your-api-key"` placeholders for Anthropic and Azure, and a `null` key for OpenAI.

Notes on the file format:

- The loader strips lines that begin with `//`, so the example's comments are allowed. Only full-line comments are supported; do not put comments after a value on the same line.
- If `config.json` is missing, Pythagora first tries to import a legacy `pilot/.env` file, and otherwise falls back to built-in defaults. The built-in defaults do not contain API keys, so you still need to supply one.
- Command-line options override some values from the file (see [Command-line options](#command-line-options)).

### Top-level sections

| Section | Purpose |
| --- | --- |
| `llm` | Per-provider settings: `base_url`, `api_key`, `connect_timeout`, `read_timeout`, and `extra`. |
| `agent` | Per-agent LLM choice: `provider`, `model`, and `temperature`. The `default` entry is used for any agent that is not listed. |
| `log` | `level` (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`), `format`, and `output` (file path, or `null` for stderr). |
| `db` | `url` and `debug_sql`. |
| `ui` | `type`: `plain` (console), `ipc-client`, or `virtual`. |
| `fs` | `type` (`local`), `workspace_root`, `ignore_paths`, and `ignore_size_threshold`. |

### LLM providers

The `llm` section and the `provider` field on each agent accept these values:

| Provider | Notes |
| --- | --- |
| `openai` | OpenAI API. Also used for any OpenAI-compatible endpoint by setting `base_url`. The example config says this covers OpenRouter and local servers such as LM Studio. |
| `anthropic` | Anthropic API. |
| `azure` | Azure OpenAI. Requires `base_url` (your resource endpoint) and `extra.azure_deployment` and `extra.api_version`. |
| `groq` | Groq API. |
| `relace` | Relace code-merge model. Requests go to a Pythagora-hosted endpoint (see [Relace](#relace)). |

`lm-studio` appears in the provider list but has no client implementation, so do not use it as a provider value. For a local OpenAI-compatible server, use `openai` with `base_url` set to the server's address.

A minimal configuration that sends every agent to OpenAI looks like this:

```json
{
  "llm": {
    "openai": {
      "base_url": null,
      "api_key": "sk-...",
      "connect_timeout": 60.0,
      "read_timeout": 20.0
    }
  },
  "agent": {
    "default": {
      "provider": "openai",
      "model": "gpt-4o-2024-05-13",
      "temperature": 0.5
    }
  }
}
```

Use the agent names from the source to override individual agents, for example `CodeMonkey`, `CodeMonkey.code_review`, `Developer.parse_task`, or `TechLead.plan_epic`. Each agent name matches the agent's class and step name in `core/config/__init__.py`.

### Database

The default database URL is `sqlite+aiosqlite:///data/database/pythagora.db`, which is relative to the current directory. Two URL schemes are accepted:

- `sqlite+aiosqlite://` (the default).
- `postgresql+asyncpg://`, which requires `asyncpg` to be installed. It is not in `requirements.txt`.

Database migrations run automatically at startup, using Alembic.

### Workspace and logs

- Generated projects are stored under `fs.workspace_root`, which defaults to a `workspace/` directory in the repository. `.gitignore` excludes `workspace/`.
- `ignore_paths` controls which files are excluded when Pythagora scans a project. Files larger than `ignore_size_threshold` (50,000 bytes by default) are also skipped. Binary files are always ignored.
- The built-in log output is `data/pythagora.log`. The example config writes to `pythagora.log`. Set `log.output` to `null` to log to stderr.

## Usage

Start a new project interactively:

```bash
venv/bin/python main.py
```

Pythagora asks what you want to build. Choose a full-stack app, or a frontend-only app if you already have a backend with an OpenAPI/Swagger definition. It then writes a specification and begins the build. The console shows the agents' messages and asks for your input when it needs it.

Start a project from a prompt without the interactive menu. This selects the full-stack ("node") option automatically:

```bash
venv/bin/python main.py --initial-prompt "A todo app with user login"
```

List existing projects, branches, and steps:

```bash
venv/bin/python main.py --list
venv/bin/python main.py --list-json
```

Resume a project. Pass a project ID, optionally with a branch ID and step:

```bash
venv/bin/python main.py --project <project-uuid>
venv/bin/python main.py --project <project-uuid> --branch <branch-uuid> --step 12
```

Delete a project:

```bash
venv/bin/python main.py --delete <project-uuid>
```

### Command-line options

| Option | Description |
| --- | --- |
| `--config PATH` | Configuration file to load. Default: `config.json`. |
| `--show-config` | Print the current configuration as JSON and exit. |
| `--version` | Print the version and exit. |
| `--level LEVEL` | Override the log level (`debug`, `info`, `warning`, `error`, `critical`). |
| `--database URL` | Override `db.url`. |
| `--llm-endpoint PROVIDER:URL` | Set the base URL for a provider. Can be repeated. |
| `--llm-key PROVIDER:KEY` | Set the API key for a provider. Can be repeated. |
| `--list` | List projects with their branches and last step. |
| `--list-json` | List projects in JSON format. |
| `--project UUID` | Load a project. |
| `--branch UUID` | Load a branch. Use with `--project` or alone. |
| `--step N` | Load a specific step in a project or branch. |
| `--project-state-id UUID` | Load a specific project state. |
| `--delete UUID` | Delete a project. |
| `--initial-prompt TEXT` | Start a new project from a prompt, using the full-stack option. |
| `--use-git` | Use Git for version control of the generated project. |
| `--no-auto-confirm-breakdown` | Do not auto-confirm when the LLM requests user input during task breakdown. |
| `--import-v0 PATH` | Import a project database from the original GPT Pilot (v0) format. |
| `--local-ipc-host HOST` | Host for the UI IPC connection. Default: `localhost`. |
| `--local-ipc-port PORT` | Port for the UI IPC connection. Enables the `ipc-client` UI. |
| `--enable-api-server` | Enable the local IPC API server. This flag defaults to on. |
| `--local-api-server-host HOST` | Host for the API server. Default: `localhost`. |
| `--local-api-server-port PORT` | Port for the API server. Default: `8222`. |
| `--email ADDRESS` | Your email address, recorded with telemetry and error reports. |
| `--access-token TOKEN` | Access token passed to LLM requests. |
| `--extension-version VERSION` | Version of the VS Code extension, if one is used. |

`--list`, `--list-json`, `--show-config`, `--import-v0`, and `--delete` each perform their action and exit without starting an agent session. `--project`, `--branch`, `--step`, and `--project-state-id` load an existing project and continue it.

### Running in Docker

The repository includes a `Dockerfile` that builds an Ubuntu 22.04 image with the dependencies, the application, and a `cloud/config-docker.json` configuration. The image's entrypoint installs the VS Code extension and then keeps the container running. It does not start `main.py` directly.

The build needs a file named `pythagora-vs-code.vsix` in the build context. That file is not included in this repository, so the build fails without it. The image exposes ports 27017, 8000, 8080, 5173, and 3000.

## Project templates

Templates are defined under `core/templates/`. The registry in `core/templates/registry.py` enables two of them:

- `vite_react`: described in the source as "Vite + React + Tailwind CSS + TypeScript + Shadcn + Nodejs + Mongo".
- `vite_react_swagger`: the frontend-only template, for use with an existing OpenAPI/Swagger backend.

Other templates (`javascript_react`, `node_express_mongoose`, and `react_express`) are present in the source but are commented out in the registry, so they are not offered.

## Architecture

The package is organized as follows:

| Path | Contents |
| --- | --- |
| `main.py` | Entry point. Calls `core.cli.main.run_pythagora()`. |
| `core/cli/` | Argument parsing, startup, and session flow. |
| `core/agents/` | Agent implementations. The `Orchestrator` runs the others based on project state. |
| `core/prompts/` | Prompt templates for each agent, in Jinja-style `.prompt` files. |
| `core/llm/` | LLM clients for each provider, plus request/response handling, retries, and rate-limit handling. |
| `core/config/` | Configuration models, the JSON loader, and agent defaults. |
| `core/db/` | SQLAlchemy models, sessions, and Alembic migrations. |
| `core/state/` | State manager for projects, branches, and steps. |
| `core/proc/` | Process manager for running commands in the project. |
| `core/disk/` | Virtual file system for the project workspace and ignore rules. |
| `core/templates/` | Project templates. |
| `core/ui/` | UI adapters: `console.py` (plain console), `ipc_client.py` (client to a UI), `api_server.py` (local IPC server), and `virtual.py`. |
| `core/telemetry/` | Telemetry collection and sending. |
| `core/log/` | Logging setup. |
| `cloud/` | Files for the Docker image: entrypoint, configuration, and VS Code extension setup scripts. |
| `docs/` | `TELEMETRY.md`, a description of the telemetry data. |
| `tests/` | Unit and integration tests. |

Agents named in the source include `SpecWriter`, `Architect`, `TechLead`, `Developer`, `CodeMonkey`, `Frontend`, `Executor`, `BugHunter`, `Troubleshooter`, `ProblemSolver`, `ExternalDocumentation`, and `TechnicalWriter`.

The UI adapter is chosen by the `ui.type` setting. `plain` prints to the console and reads your input from it. `ipc-client` connects to a UI at the host and port given by `--local-ipc-host` and `--local-ipc-port`. `virtual` takes its scripted answers from the `inputs` list in the configuration.

## Relace

The `relace` provider sends code-merge requests to `https://api.pythagora.io/v1/relace/merge`, which is a Pythagora-hosted endpoint. The request contains the initial code and the edit snippet, along with the model name. If the request fails, the client logs the error and returns empty content with zero token counts. It does not retry with another provider.

The built-in defaults in `core/config/__init__.py` assign the `CodeMonkey.implement_changes` agent to Relace. If you want to avoid this endpoint, override that agent to use a different provider in your configuration.

## Telemetry

Telemetry is enabled by default. When it is enabled, Pythagora collects anonymous usage data such as the platform, Python version, Pythagora version, LLM provider and model, the number of LLM requests and development steps, the initial prompt, and the architecture chosen. If you give an email address with `--email`, or use the VS Code extension, that address is included. The full list is in [`docs/TELEMETRY.md`](docs/TELEMETRY.md) and in `Telemetry.clear_data()` in `core/telemetry/__init__.py`.

Data is sent to `https://api.pythagora.io/telemetry`.

To turn telemetry off, set `telemetry.enabled` to `false` in the user settings file. The location depends on your system:

- `$XDG_CONFIG_HOME/gpt-pilot/config.json`, if `XDG_CONFIG_HOME` is set.
- `%APPDATA%\GPT Pilot\config.json` on Windows.
- `~/.gpt-pilot/config.json` otherwise.

Pythagora creates this file on first run if it does not exist.

Error reporting is separate from telemetry. When the `sentry-sdk` package is installed (it is listed in `requirements.txt`), fatal errors are sent to Sentry, using a DSN hard-coded in `core/cli/helpers.py`. Sentry is configured with `send_default_pii=True`. If you pass `--email`, that address is also attached to the Sentry user.

## Development

Install the development dependencies with Poetry, then run the checks CI runs:

```bash
pip install poetry
poetry install --with=dev
poetry run ruff check
poetry run ruff format --check
poetry run pytest
```

The pytest configuration in `pyproject.toml` runs with coverage for `core/` and a 10-second timeout per test. The `tests/` directory mirrors the layout of `core/` (for example `tests/llm/`, `tests/agents/`, `tests/db/`, and `tests/ui/`). Integration tests that call real LLM providers are in `tests/integration/llm/`. They run only when `INTEGRATION_TESTS` is set and the matching key (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GROQ_API_KEY`) is present; otherwise they are skipped.

Ruff is configured with a line length of 120 and the `I` (isort) rules. Pre-commit is configured in `.pre-commit-config.yaml`.

## Contributing

Contribution guidelines are in [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md). Issue templates for bug reports, feature requests, and how-to questions are in `.github/ISSUE_TEMPLATE/`.

## License

This project is licensed under the Functional Source License, Version 1.1, MIT Future License (FSL-1.1-MIT). See [`LICENSE`](LICENSE) for the full terms.

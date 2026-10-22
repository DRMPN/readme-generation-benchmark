# Pythagora Core

**Pythagora Core** (`pythagora-core`) is the engine behind [Pythagora](https://pythagora.ai), an AI development tool that builds complete web applications from a plain-language description. Evolved from the open-source GPT Pilot project, it coordinates a team of specialized AI agents that write the specification, design the architecture, generate code, run commands, test the app, and debug bugs — with you in the loop at every step.

- **Repository:** <https://github.com/Pythagora-io/pythagora-core>
- **Homepage:** <https://pythagora.ai>
- **License:** FSL-1.1-MIT (see [License](#license))

## How It Works

An **Orchestrator** agent drives the whole process. Based on the current project state, it invokes the other agents, commits each step to the database, and loops until the app is done:

| Agent | Responsibility |
| --- | --- |
| Spec Writer | Turns your description into a detailed, refinable specification; later handles new feature requests |
| Architect | Plans the architecture, picks technologies and starter templates, and verifies system dependencies are installed |
| Tech Lead | Breaks the project into epics and tasks and applies project templates |
| Frontend | Builds and iterates on the UI, including automatic debugging of the dev server |
| Developer | Breaks tasks and iterations into concrete development steps (save file, run command, human intervention) |
| Code Monkey | Creates and edits project files, reviews its own diffs, and generates file descriptions |
| Executor | Runs shell commands and analyzes their output |
| Bug Hunter | Reproduces bugs, adds logging, asks you to test, and offers a pair-programming mode |
| Troubleshooter | Drives the review/feedback loop after each task |
| Problem Solver | Proposes alternative solutions when development gets stuck in a loop |
| Documentation | Selects and fetches relevant external documentation for a task |
| Importer | Analyzes and imports an existing codebase (experimental) |
| Technical Writer | Creates and maintains project documentation |
| Error Handler, Human Input, Task Completer, Wizard | Support agents for error recovery, required user input, task completion, and project setup |

A typical run looks like: you describe the app → the Spec Writer produces a detailed specification you can refine → the Architect plans the stack and checks dependencies → the Frontend agent builds the UI → the Tech Lead breaks the backend into tasks → the Developer/Code Monkey/Executor implement each task → you test, report issues, and the Bug Hunter/Troubleshooter fix them.

## Features

- **Multiple LLM providers:** OpenAI, Azure OpenAI, Anthropic, and Groq, plus OpenRouter or local LLMs (e.g., LM Studio) through the OpenAI-compatible provider.
- **Per-agent model configuration:** assign a different provider, model, and temperature to each agent or even individual agent routes.
- **Project templates:** bundled starters including `javascript_react`, `react_express`, `vite_react`, `vite_react_swagger`, and `node_express_mongoose`.
- **Two project modes:** full-stack apps ("node") or frontend-only apps built against an existing backend described by OpenAPI/Swagger ("swagger").
- **Git integration:** optional repository initialization and commits with LLM-suggested commit messages.
- **Persistent, resumable state:** every step is committed to the database (SQLite by default, PostgreSQL supported via SQLAlchemy async), with branches and project states you can reload or roll back.
- **Knowledge base:** tracks implemented pages, API endpoints, and utility functions as the app grows.
- **VS Code integration:** powers the Pythagora VS Code extension and cloud workspaces (the Docker image bundles the extension and `code-server`).

## Requirements

- Python **3.9+** (CI runs against 3.9 and 3.12)
- Node.js and npm (generated projects are Node-based)
- Git (optional, for repository integration)
- An API key for at least one supported LLM provider

## Installation

Clone the repository and set up a Python virtual environment:

```bash
git clone https://github.com/Pythagora-io/pythagora-core
cd pythagora-core
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If you run `python main.py` without the environment set up, it will print exactly these instructions for your platform. For development, dependencies are managed with Poetry (see [Development](#development)).

## Usage

Start Pythagora from the repository root:

```bash
python main.py
```

You will be asked what you want to build (**Full stack app** or **Frontend only** with an existing OpenAPI/Swagger backend), then prompted to describe the app. From there, the agents take over and pause for your input at review, testing, and decision points.

Useful command-line options (run `python main.py --help` for the full list):

- `--initial-prompt "..."` — start a project non-interactively from a description
- `--list` / `--list-json` — list saved projects, branches, and states
- `--show-config` — display the loaded configuration
- `--delete` — delete a project
- `--import-v0` — import a legacy GPT Pilot v0 database
- `--project` / `--branch` / `--step` / `--project-state-id` — continue a previously saved project
- `--email` — associate your email with crash reports (used with Sentry when provided)

Project data is stored under `data/` (SQLite database at `data/database/pythagora.db`) and generated apps live under `workspace/`.

## Configuration

Pythagora reads a JSON configuration file; an annotated example is provided in [`example-config.json`](example-config.json) (the Docker image uses `cloud/config-docker.json` as its `config.json`, and the telemetry documentation references `~/.gpt-pilot/config.json`). Key sections:

- **`llm`** — per-provider settings (`base_url`, `api_key`, connect/read timeouts) for `openai`, `anthropic`, `azure`, `groq`, and `relace`.
- **`agent`** — model overrides per agent or agent route. Keys match agent class names (e.g., `CodeMonkey`) or dotted routes (e.g., `BugHunter.check_logs`), with `default` as the fallback.
- **`log`** — log level, format, and output file (default `pythagora.log`; set to `null` for stdout).
- **`db`** — asyncio-compatible SQLAlchemy URL (`sqlite+aiosqlite://...` by default; PostgreSQL supported) and `debug_sql`.
- **`ui`** — interface type (`plain` console UI; an IPC/API server mode is used by the extension).
- **`fs`** — filesystem type, `workspace_root`, ignored paths/patterns, and a size threshold (default 50 KB) above which files are ignored.
- **`prompt`** — search paths for agent prompt templates.

Database migrations are applied automatically with Alembic at startup (`core/db/setup.py`).

## Docker

A `Dockerfile` builds an Ubuntu 22.04 image containing Python 3.12, Node.js LTS, MongoDB, `code-server`, and the Pythagora VS Code extension, running as a non-root `devuser`:

```bash
docker build -t pythagora-core .
docker run -p 8080:8080 -p 5173:5175 -p 3000:3000 pythagora-core
```

The image exposes ports `27017` (MongoDB), `8000`, `8080` (code-server browser IDE serving the workspace), `5173` (Vite dev server), and `3000` (app). The entrypoint starts `code-server` and keeps the container running; Pythagora configuration comes from `cloud/config-docker.json`.

## Development

Dependencies and tooling are managed with [Poetry](https://python-poetry.org):

```bash
poetry install --with=dev
pre-commit install
```

- **Linting/formatting:** [Ruff](https://docs.astral.sh/ruff/) with a 120-character line limit and isort-style import sorting (`ruff check`, `ruff format`).
- **Pre-commit hooks:** Ruff lint + format, an Alembic `check` that ensures no database migrations are missing, and a full `pytest` run.
- **Migrations:** create/adjust Alembic migrations under `core/db/migrations/versions/` when changing models in `core/db/models/`.
- **Project layout:** `core/agents/` (agent implementations), `core/prompts/` (Jinja prompt templates per agent), `core/templates/` (project starter templates), `core/llm/` (provider clients and conversation/parsing utilities), `core/db/` (SQLAlchemy models, session, migrations), `core/ui/` (console and IPC interfaces), `core/proc/` (process management), `core/state/` (state manager).

## Testing

The test suite uses `pytest` with coverage over `core`, a 10-second per-test timeout, and in-memory SQLite fixtures that mock the UI and LLM (see `tests/conftest.py`):

```bash
poetry run pytest          # or simply: pytest
```

Tests cover agents, CLI helpers, configuration, database models, the virtual filesystem, LLM conversations/parsers/prompts, logging, process management, the state manager, telemetry, templates, and the UI layer. Integration tests for the OpenAI, Anthropic, and Groq clients live under `tests/integration/llm/`.

Continuous integration (GitHub Actions) runs Ruff lint, Ruff format checks, and pytest on Python 3.9 and 3.12 across Ubuntu, macOS, and Windows.

## Telemetry

Pythagora collects anonymous usage telemetry (runtime, command runs, development steps, LLM request counts, OS/Python/model info, and similar aggregates) to improve the product. No personal information is collected, and data is not shared with third parties. Full details, including every collected data point, are in [`docs/TELEMETRY.md`](docs/TELEMETRY.md).

To opt out, set `telemetry.enabled` to `false` in your `~/.gpt-pilot/config.json` configuration file.

## Support and Community

- Ask "how do I...?" questions and discuss ideas in the community [Discord](https://discord.gg/HaqXugmxr9).
- Check the GPT Pilot wiki [FAQ](https://github.com/Pythagora-io/gpt-pilot/wiki/Frequently-Asked-Questions) and open issues before filing a new one.
- Bug reports, feature requests, and questions can be filed through the GitHub issue templates.

## Contributing

Contributions are welcome via pull requests. Before opening a PR, make sure the pre-commit hooks pass (lint, formatting, migration check, and tests) and that CI is green. Please note the project's [Code of Conduct](.github/CODE_OF_CONDUCT.md) — all contributors are expected to uphold it.

## License

Pythagora Core is licensed under the **Functional Source License, Version 1.1, MIT Future License** (`FSL-1.1-MIT`), © 2024 Pythagora Technologies, Inc.

In short:

- You may use, copy, modify, and redistribute the software for any **permitted purpose**: internal use, non-commercial education, non-commercial research, and professional services provided to licensees.
- **Competing use** — offering the software, or substantially similar functionality, as part of a commercial product or service — is not permitted.
- Each version automatically becomes available under the standard **MIT license** two years after its release date.

See the [`LICENSE`](LICENSE) file for the complete terms.

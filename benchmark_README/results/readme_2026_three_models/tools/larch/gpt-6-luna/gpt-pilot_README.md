# GPT Pilot

GPT Pilot is an AI-assisted software development tool. It helps turn a project idea into a working application by guiding the development process, planning and writing code, running commands, and responding to errors or feedback.

The repository includes a Python development agent, command-line and API/IPC components, database models and migrations, prompt templates, and example application templates.

## Features

- **Guided development workflow:** Coordinate planning, implementation, review, and troubleshooting through the project orchestrator.
- **AI provider integrations:** Client implementations are included for OpenAI, Anthropic, Groq, Azure, and Relace.
- **Project-aware coding:** Inspect and manage project files with the virtual file system, and use Git-related functionality during development.
- **Command execution and recovery:** Run project commands, capture logs, and help diagnose or address errors.
- **Documentation support:** Search external documentation and use project context when building or changing an application.
- **Templates:** Start from included examples and templates, including React and Express-based projects.
- **Persistence:** Store project and conversation state using database models and migrations.
- **Optional interfaces:** The repository includes command-line, API server, console, and IPC components.

## Requirements

Check the project configuration and setup scripts for the current supported versions. In general, you will need:

- Python and `pip`
- Git
- Node.js and npm for working with JavaScript-based generated projects or templates
- Credentials for whichever AI provider you configure

Some features or templates may require additional system dependencies.

## Getting started

### 1. Clone the repository

```bash
git clone <repository-url>
cd gpt-pilot-ozu3t0xd
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the Python project dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

The repository also contains `setup-dependencies.sh` for additional setup. Review that script before running it, especially if you are installing on a system with custom package or security requirements.

### 4. Configure the application

Start with `example-config.json` and `settings.json` to understand the available settings. Configure an AI provider and supply its credentials using the configuration or environment-variable mechanism supported by the project.

Do not commit API keys or other secrets. Keep them in a local, untracked configuration or a secure environment-variable store.

For Docker-related settings, see `config-docker.json` and `Dockerfile`.

### 5. Run GPT Pilot

From the repository root, start the application with:

```bash
python main.py
```

The available options and workflow depend on the configured interface and project settings. If you are unsure which settings are required, consult the example configuration and the project’s CLI prompts.

## AI providers

The codebase includes clients for:

- OpenAI
- Anthropic
- Groq
- Azure OpenAI
- Relace

Configure the provider and credentials before starting a workflow. Provider-specific options may differ; use the configuration examples and relevant client implementation as the source of truth for supported settings.

## Development workflow

GPT Pilot’s development workflow is organized into roles and components, including:

- **Wizard and orchestrator:** Coordinate the interactive development flow.
- **Architect and tech lead:** Help plan work and break it into implementation tasks.
- **Developer and code monkey:** Work on project code and changes.
- **Frontend and tech writer:** Support frontend implementation and documentation.
- **Executor and process manager:** Run commands and manage their output.
- **Troubleshooter and error handler:** Help diagnose execution and implementation problems.
- **Bug hunter and task completer:** Support review and completion activities.

The exact sequence depends on the task and configuration. GPT Pilot may ask for clarification or feedback during a run.

## Working with generated projects

Generated applications can use different stacks. The repository contains templates for examples such as Vite/React and Express-based projects, along with frontend assets and package files.

When working with a generated JavaScript project, change into that project’s directory and use its own package scripts. For example:

```bash
cd <generated-project>
npm install
npm run dev
```

The actual commands depend on the generated project’s `package.json`.

## Docker

A `Dockerfile`, `entrypoint.sh`, and Docker-specific configuration are included. Review these files to see which services, environment variables, and volumes the container expects.

A typical local image build is:

```bash
docker build -t gpt-pilot .
```

Run the image with the configuration and credentials required by your setup. Avoid placing secrets directly in a Docker image or committing them to configuration files.

## Database and migrations

The repository contains database models and Alembic migrations. If you need to initialize, upgrade, or inspect the database, consult `alembic.ini` and the migration files before running migration commands. Back up existing project data before applying migrations to a database you care about.

## Running tests

Install the project dependencies, then run the test suite from the repository root:

```bash
pytest
```

Tests cover areas including provider clients, prompts and conversations, orchestration, project state, configuration, templates, logging, and process management. Some tests may require provider credentials or other external services; check the relevant test configuration before running them.

## Repository layout

| Path or files | Purpose |
|---|---|
| `main.py` | Main application entry point |
| `settings.json`, `example-config.json` | Application settings and configuration example |
| `config-docker.json`, `Dockerfile` | Docker configuration and image definition |
| `setup-dependencies.sh` | Additional dependency setup |
| `pyproject.toml` | Python project metadata and tooling configuration |
| `main/` and related Python modules | Application logic, agents, clients, and workflows |
| `prompts/` | Prompt templates used by the development workflow |
| `templates/` | Example project templates |
| `alembic.ini` and migration files | Database migration configuration and history |
| `tests/` | Automated tests |
| `api_server.py`, `console.py`, `ipc_client.py` | API, console, and IPC-related components |

Directory names may differ depending on how the project is checked out; use the repository’s actual file tree as the authoritative layout.

## Configuration and security notes

- Keep provider keys and other secrets out of source control.
- Review configuration files before sharing logs or project data.
- GPT Pilot may read and write files and execute commands in a project as part of its workflow. Run it with appropriate permissions and review changes and commands.
- Use a disposable project or a clean Git branch when evaluating changes.
- Check the project’s telemetry documentation and settings if you want to understand or control telemetry behavior.

## Contributing

Contributions should include tests or documentation updates where appropriate. Before opening a pull request:

1. Run the relevant tests.
2. Review the changes produced by the development workflow.
3. Avoid including credentials, generated secrets, or unrelated project files.

See `LICENSE` for licensing terms and `CHANGELOG.md` for release history.

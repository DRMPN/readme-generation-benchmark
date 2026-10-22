# GPT Pilot

> **Note:** This README was written from the repository's file listing alone. Commands, configuration keys, and behavior are inferred from file names and structure. Check them against the source code and the included `CHANGELOG.md` and `TELEMETRY.md` before relying on them.

## Overview

GPT Pilot is an AI-driven software development assistant. It takes a natural-language description of an application and works through the development process the way a human developer would: it clarifies requirements, writes a specification, plans the architecture, breaks the work into tasks, writes code, runs and debugs it, and documents the result.

The project is organized as a multi-agent system. Specialized agents handle distinct roles such as specification writing, architecture, development, frontend work, debugging, and documentation. An orchestrator coordinates them. The system is designed to be resumable: project state is persisted to a database, so a session can be stopped and continued later.

## Key Features

- **Multi-agent workflow.** Dedicated agents for specification, architecture, technical leadership, development, frontend, code execution, troubleshooting, problem solving, error handling, bug hunting, external documentation lookup, and technical writing.
- **Multiple LLM providers.** Clients are included for OpenAI, Anthropic, Azure OpenAI, Groq, and Relace, behind a common base client.
- **Project templates.** Starter templates for Vite + React, React + Express, Node + Express + Mongoose, JavaScript React, and Vite + React with Swagger. Templates are discovered through a registry and rendered with a templating engine.
- **Persistent, resumable projects.** Project state, specifications, files, conversations, execution logs, and branches are stored in a database managed with Alembic migrations.
- **Virtual file system and ignore rules.** Generated files are tracked in a virtual file system (VFS), and ignore rules keep irrelevant files out of prompts and processing.
- **Git integration.** A git module supports version control of the generated project.
- **Process management.** Long-running processes such as dev servers and test commands are started and monitored by a process manager.
- **Console and IPC interfaces.** A console UI runs in the terminal. An IPC layer with an API server and client allows external front ends, such as an editor extension, to communicate with the core.
- **Docker support.** A Dockerfile, entrypoint script, and Docker configuration are included.
- **Telemetry (documented).** `TELEMETRY.md` describes what is collected and how to control it.

## Repository Structure

```
gpt-pilot-c8acow6m/
├── core/                        # Main Python application
│   ├── agents/                  # AI agents and orchestration
│   │   ├── architect.py         # Designs system architecture
│   │   ├── bug_hunter.py        # Finds and reproduces bugs
│   │   ├── code_monkey.py       # Writes code for individual tasks
│   │   ├── developer.py         # Coordinates implementation of tasks
│   │   ├── error_handler.py     # Handles runtime and LLM errors
│   │   ├── executor.py          # Runs commands in the project
│   │   ├── external_docs.py     # Retrieves external documentation
│   │   ├── frontend.py          # Frontend-specific development
│   │   ├── importer.py          # Imports existing projects
│   │   ├── orchestrator.py      # Coordinates the agent workflow
│   │   ├── problem_solver.py    # Proposes fixes for problems
│   │   ├── spec_writer.py       # Produces the project specification
│   │   ├── tech_lead.py         # Plans tasks and technical decisions
│   │   ├── tech_writer.py       # Writes documentation
│   │   ├── troubleshooter.py    # Diagnoses failures
│   │   ├── wizard.py            # Guided project setup
│   │   ├── human_input.py       # Requests input from the user
│   │   ├── legacy_handler.py    # Handles older project formats
│   │   └── mixins.py            # Shared agent behavior
│   ├── llm/                     # LLM provider clients
│   │   ├── base.py              # Common client interface
│   │   ├── openai_client.py
│   │   ├── anthropic_client.py
│   │   ├── azure_client.py
│   │   ├── groq_client.py
│   │   ├── relace_client.py
│   │   ├── request_log.py       # Logs LLM requests
│   │   ├── parser.py            # Parses LLM responses
│   │   └── convo.py             # Conversation management
│   ├── prompts/                 # Prompt templates organized by agent
│   ├── templates/               # Project starter templates
│   │   ├── registry.py          # Template discovery
│   │   ├── render.py            # Template rendering
│   │   ├── vite_react.py
│   │   ├── react_express.py
│   │   ├── node_express_mongoose.py
│   │   ├── javascript_react.py
│   │   └── vite_react_swagger.py
│   ├── db/                      # Database models and migrations
│   │   ├── models/              # SQLAlchemy models (project, branch, spec, files, etc.)
│   │   ├── migrations/          # Alembic migration scripts
│   │   ├── setup.py
│   │   └── v0importer.py        # Imports data from older versions
│   ├── state/                   # Project state management
│   ├── config/                  # Configuration and settings
│   │   ├── user_settings.py
│   │   ├── env_importer.py      # Loads settings from environment
│   │   ├── magic_words.py
│   │   └── actions.py
│   ├── git.py                   # Git operations
│   ├── vfs.py                   # Virtual file system
│   ├── ignore.py                # Ignore-rule handling
│   ├── process_manager.py       # Starts and monitors processes
│   ├── telemetry/               # Telemetry collection
│   ├── ipc/                     # Inter-process communication
│   │   ├── api_server.py
│   │   └── ipc_client.py
│   ├── ui/                      # User interface
│   │   ├── base.py
│   │   ├── console.py           # Terminal interface
│   │   └── virtual.py           # Non-interactive interface
│   ├── log.py                   # Logging
│   ├── cli/main.py              # Command-line entry point
│   └── version.py
├── tests/                       # Test suite (pytest)
├── main.py                      # Application entry point
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Pinned dependencies
├── config-docker.json           # Configuration for Docker
├── example-config.json          # Example configuration
├── testconfig.json              # Configuration used by tests
├── settings.json                # Settings file
├── Dockerfile
├── entrypoint.sh                # Docker entrypoint
├── setup-dependencies.sh        # Dependency installation script
├── on-event-extension-install.sh
├── CHANGELOG.md
├── TELEMETRY.md
├── LICENSE
├── favicon.ico / favicon.svg
└── README
```

## Prerequisites

- **Python 3.9 or later** (confirm the exact minimum in `pyproject.toml`)
- **An API key for at least one supported LLM provider** (OpenAI, Anthropic, Azure OpenAI, Groq, or Relace)
- **Git** for version control features
- **Node.js and npm** if you plan to generate and run JavaScript or React projects
- **Docker** (optional), for containerized runs

## Installation

### Option 1: Local installation

1. Clone the repository:

   ```bash
   git clone <repository-url> gpt-pilot
   cd gpt-pilot
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Install dependencies, either with the included script or directly:

   ```bash
   bash setup-dependencies.sh
   # or
   pip install -r requirements.txt
   # or
   pip install -e .
   ```

4. Create your configuration file from the example:

   ```bash
   cp example-config.json config.json
   ```

   Then edit `config.json` as described in [Configuration](#configuration).

### Option 2: Docker

1. Build the image:

   ```bash
   docker build -t gpt-pilot .
   ```

2. Prepare a configuration file (`config-docker.json` is provided as a starting point) and supply your API keys through environment variables or the configuration file.

3. Run the container:

   ```bash
   docker run -it --env-file .env -v "$(pwd)/workspace:/app/workspace" gpt-pilot
   ```

   The `entrypoint.sh` script starts the application inside the container. Adjust the volume and environment flags to match your setup.

## Configuration

### Configuration file

`example-config.json` shows the expected structure. Copy it to `config.json` and adjust it. Typical settings include:

- The LLM provider and model to use for each agent or task type
- API endpoints for providers that require them, such as Azure
- Paths for the workspace and database
- Logging and telemetry options
- Default behavior for user interaction

Use `config-docker.json` for container deployments, where paths and hosts differ from a local setup.

### Environment variables

API keys are typically read from environment variables, which `env_importer.py` loads. Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
AZURE_API_KEY=your-azure-key
GROQ_API_KEY=your-groq-key
RELACE_API_KEY=your-relace-key
```

Only the keys for the providers you use are required. Exact variable names are defined in the configuration code and may differ; check `core/config/` if a key is not picked up.

### Settings

`settings.json` holds additional application settings. Editor integration and extension-related settings are handled through the IPC layer and the `on-event-extension-install.sh` script.

## Usage

Start GPT Pilot from the project root:

```bash
python main.py
```

A typical session proceeds as follows:

1. **Project name and description.** Describe the application you want to build. The system generates a project name and may ask follow-up questions.
2. **Specification.** The spec writer produces a detailed specification, which you can review and amend.
3. **Template selection.** Optionally choose a starter template such as Vite + React or React + Express.
4. **Architecture and planning.** The architect and tech lead define the system design and break the work into tasks.
5. **Implementation.** The developer and code monkey agents write code task by task. The executor runs commands, and the troubleshooter and problem solver handle failures.
6. **Review and iteration.** You can give feedback at review points. The system incorporates changes and continues.
7. **Documentation.** The tech writer generates project documentation.

Projects are saved in the database and workspace, so you can resume an earlier project. Check the console help or `core/cli/main.py` for available commands and flags.

### Using the IPC API

The IPC layer (`core/ipc/`) exposes an API server that external clients can connect to. This is how editor integrations and other front ends communicate with the core. The client library is in `ipc_client.py`. Message formats and endpoints are defined in `api_server.py`.

## Database and Migrations

Project data is stored in a database accessed through SQLAlchemy models in `core/db/models/`. Schema changes are managed with Alembic, configured by `alembic.ini` and the scripts in `core/db/migrations/`.

To apply migrations, run Alembic from the project root:

```bash
alembic upgrade head
```

To create a new migration after changing a model:

```bash
alembic revision --autogenerate -m "describe your change"
```

Projects created with older versions can be upgraded with the importer in `core/db/v0importer.py`.

## Templates

Templates are defined as Python classes in `core/templates/` and registered in `registry.py`. Each template provides a set of starter files, rendered with `render.py`, and is listed in the template-selection step.

To add a template:

1. Create a new module in `core/templates/` that follows the pattern of an existing template.
2. Register it in `registry.py`.
3. Add any template files and summaries it needs. The `summary.tpl` files show the expected format.
4. Add tests in `tests/`.

## Prompts

All prompts sent to LLMs live in `core/prompts/`, organized into subdirectories by agent or task (for example `spec_writer/`, `architect/`, `troubleshooter/`, `bug_hunter/`, `tech_writer/`). Most agents have a `system.prompt` and one or more task-specific prompts. Editing these files changes agent behavior without modifying code.

## Testing

The test suite lives in `tests/` and uses pytest. Tests cover agents, LLM clients, the database, templates, the VFS, the ignore system, the process manager, the console, and more. Shared fixtures are in `conftest.py`, and `factories.py` provides helpers for building test objects.

Run all tests:

```bash
pytest
```

Run a single module:

```bash
pytest tests/test_orchestrator.py
```

Tests that call external LLM providers should be run with `testconfig.json` and appropriate keys. Check the test files for any that are marked to skip or mock network calls.

## Logging

Logging is configured in `core/log.py`. LLM request and response activity is recorded by `core/llm/request_log.py`. Log levels and output locations are set in the configuration.

## Telemetry

Telemetry handling is implemented in `core/telemetry/`. See [TELEMETRY.md](TELEMETRY.md) for what is collected and how to opt out.

## Versioning and Changelog

The current version is defined in `core/version.py` and `pyproject.toml`. Release history and notable changes are recorded in [CHANGELOG.md](CHANGELOG.md).

## Troubleshooting

- **API key errors.** Confirm the key is set in `.env` or `config.json` and that the provider is selected in the configuration.
- **Migration errors.** Back up the database, then run `alembic upgrade head`. For projects from very old versions, use the v0 importer.
- **Generated project fails to start.** The troubleshooter agent attempts to diagnose these failures automatically. Check the logs for the command output and the request log for LLM interactions.
- **Docker volume permissions.** Make sure the mounted workspace directory is writable by the container user.

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes, following the existing structure: agents in `core/agents/`, clients in `core/llm/`, prompts in `core/prompts/`.
3. Add or update tests in `tests/`.
4. Add a database migration if you change any model.
5. Update `CHANGELOG.md` with a summary of your change.
6. Open a pull request describing the change and how you tested it.

## License

This project is distributed under the terms in the [LICENSE](LICENSE) file. Read it before using, modifying, or redistributing the software.

## Acknowledgments

GPT Pilot builds on the capabilities of large language model providers, and it uses open-source libraries for its database, templating, and testing infrastructure. See `pyproject.toml` and `requirements.txt` for the full list of dependencies.

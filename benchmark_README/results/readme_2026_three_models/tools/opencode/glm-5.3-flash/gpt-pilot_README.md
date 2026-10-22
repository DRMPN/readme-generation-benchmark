# Pythagora Core

Build complete apps using AI agents.

Pythagora Core is an AI-powered development tool that orchestrates multiple specialized agents to plan, build, debug, and iterate on full-stack applications from a single prompt.

## Features

- **Multi-Agent Architecture**: Uses specialized agents to handle every aspect of development, including the Orchestrator, Architect, Tech Lead, Spec Writer, Developer, Code Monkey, Tech Writer, Frontend, Bug Hunter, Troubleshooter, Problem Solver, and Error Handler.
- **Multiple LLM Support**: Integrates with OpenAI, Anthropic, Groq, Azure OpenAI, and Relace.
- **Project Management**: Create, load, delete, and manage projects, branches, and development states.
- **IPC/API Server**: Supports a local IPC server for integration with external clients (such as the Pythagora VS Code extension).
- **Full-Stack & Frontend-only Support**: Build full-stack apps or frontend-only apps connected to an existing backend with OpenAPI/Swagger.

## Requirements

- Python 3.9 or higher (`^3.9`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Pythagora-io/pythagora-core.git
   cd pythagora-core
   ```

2. Install dependencies using [Poetry](https://python-poetry.org/):

   ```bash
   poetry install
   ```

   Alternatively, install from `requirements.txt`:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the main entry point:

```bash
python main.py
```

### Command-Line Arguments

| Argument | Description |
| :--- | :--- |
| `--config` | Path to the configuration file (default: `config.json`). |
| `--show-config` | Output the default configuration to stdout. |
| `--level` | Log level (debug, info, warning, error, critical). |
| `--database` | Database URL. |
| `--local-ipc-host` | Local IPC host to connect to (default: `localhost`). |
| `--local-ipc-port` | Local IPC port to connect to. |
| `--version` | Show the version and exit. |
| `--list` | List all projects. |
| `--list-json` | List all projects in JSON format. |
| `--project` | Load a specific project by UUID. |
| `--branch` | Load a specific branch by UUID. |
| `--step` | Load a specific step in a project/branch. |
| `--project-state-id` | Load a specific project state by UUID. |
| `--delete` | Delete a specific project by UUID. |
| `--llm-endpoint` | Use a specific API endpoint for a given provider. |
| `--llm-key` | Use a specific LLM key for a given provider. |
| `--import-v0` | Import data from a legacy GPT Pilot (v0) database. |
| `--email` | User's email address. |
| `--extension-version` | Version of the VS Code extension. |
| `--use-git` | Use Git for version control. |
| `--no-auto-confirm-breakdown` | Disable auto-confirm when the LLM requests user input. |
| `--access-token` | Access token. |
| `--enable-api-server` | Enable IPC server for external clients (default: enabled). |
| `--local-api-server-host` | Host for the IPC server (default: `localhost`). |
| `--local-api-server-port` | Port for the IPC server (default: `8222`). |
| `--initial-prompt` | Initial prompt to automatically start a new project with the 'node' stack. |

### Docker

A `Dockerfile` is provided to run Pythagora in a containerized Ubuntu 22.04 environment with `code-server` support. It runs as a non-root user (`devuser`) and exposes ports `27017`, `8000`, `8080`, `5173`, and `3000`.

## Development

### Running Tests

The project uses `pytest` for testing. To run tests with coverage and a 10-second timeout:

```bash
pytest
```

### Code Style & Linting

The project uses `ruff` for linting and formatting with a maximum line length of 120 characters.

### Pre-commit Hooks

Install pre-commit hooks to ensure code quality:

```bash
pre-commit install
```

## Telemetry

Pythagora collects anonymous telemetry data to help understand how the tool is used and to improve quality. This includes total runtime, command runs, LLM requests, OS, Python version, and task/step details. No personal information is collected, and data is completely anonymized.

You can opt out at any time by setting `telemetry.enabled` to `false` in your `~/.gpt-pilot/config.json` configuration file. For more details, see [docs/TELEMETRY.md](docs/TELEMETRY.md).

## License

This project is licensed under the [Functional Source License, Version 1.1, MIT Future License (FSL-1.1-MIT)](LICENSE).

Copyright 2024 Pythagora Technologies, Inc.

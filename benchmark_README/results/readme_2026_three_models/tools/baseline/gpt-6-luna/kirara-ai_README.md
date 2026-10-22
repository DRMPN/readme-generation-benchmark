# Kirara AI

Kirara AI is a Python framework for building AI agents. It combines configurable language-model backends, instant-messaging (IM) adapters, workflows, plugins, memory, media handling, tracing, and a web management interface. Workflows are assembled from registered blocks, while dispatch rules determine which workflow handles an incoming message.

The package requires Python 3.10 or newer and is published as `kirara-ai` (version `3.3.0a2` in the project metadata). The web server serves a UI from a local `web/` directory and exposes its API under `/backend-api`.

## Features

- **Workflow engine:** Build and execute workflows using reusable blocks. The repository includes blocks for chat, messaging, memory, games, system actions, variables, and MCP tools.
- **Message dispatch:** Route messages to workflows using rules such as prefix, keyword, regular-expression, mention, chat-type, and fallback matches.
- **Model backends:** Register language-model adapters and model configurations. Preset adapter code is included for providers such as OpenAI, Gemini, Claude, DeepSeek, Ollama, and Voyage.
- **IM adapters and plugins:** Manage messaging integrations and extend the application through plugins.
- **Memory and media:** Configure memory persistence and work with media files and metadata.
- **Web management:** Use the web interface and API to manage application components. API modules cover workflows, blocks, dispatch rules, IM, LLMs, plugins, system status, media, tracing, and MCP servers.

## Requirements

- Python **3.10 or later**.
- A web UI installation in `web/` to use the browser interface. The server attempts to install the UI automatically if it is missing.
- Provider-specific credentials or connection settings for the LLM backends, messaging adapters, plugins, or MCP servers you configure.

The Docker image uses Python 3.11 and installs system packages including `ffmpeg`, `wkhtmltopdf`, and `libmagic1`.

## Installation

From a checkout of this repository, install the project and its declared dependencies:

```bash
python -m pip install .
```

The project also supports building a wheel with the Python `build` package:

```bash
python -m pip install build
python -m build
```

## Configuration

At startup, Kirara AI looks for `data/config.yaml`. Copy the supplied example to that path and edit it:

```bash
cp config.yaml.example data/config.yaml
```

Configuration is YAML validated against Pydantic models. The example file is the best starting point for the full configuration. The application can also start without a config file, in which case it uses model defaults and logs a warning.

The top-level configuration supports these areas:

| Section | Purpose |
| --- | --- |
| `ims` | IM adapter names, enablement, adapter type, and adapter-specific settings |
| `llms` | LLM backend definitions and model entries |
| `mcp` | MCP server definitions, including connection type, command or URL, arguments, headers, and environment |
| `defaults` | Default model name |
| `memory` | Persistence type, file or Redis settings, entry limit, and default scope |
| `web` | Bind address, port, JWT secret key, and password-file location |
| `plugins` | Enabled external plugins and plugin-market base URL |
| `update` | PyPI and npm registry URLs |
| `frpc` | Optional FRPC settings |
| `system` | System timezone |
| `tracing` | Whether LLM request content is recorded |
| `media` | Media cleanup interval and unreferenced-file cleanup settings |

For example, these are supported web and memory settings:

```yaml
web:
  host: 127.0.0.1
  port: 8080
  secret_key: "replace-with-a-secret"
  password_file: ./data/web/password.hash

memory:
  persistence:
    type: file
    file:
      storage_dir: ./data/memory
  max_entries: 100
  default_scope: member
```

The default web port is `8080`. The command-line host and port options override the corresponding `web` settings. Configure backend and adapter details according to their configuration schemas; the web API includes endpoints for retrieving IM and LLM adapter schemas.

Configuration and runtime data are kept under `data/` by default. The package also reads `DATA_PATH` to select a data directory; plugin data is stored in a `plugins` directory beneath it.

## Usage

Start the application from the repository root:

```bash
python -m kirara_ai
```

The installed console script is also available:

```bash
kirara_ai
```

To override the web server bind address or port for one run:

```bash
python -m kirara_ai --host 0.0.0.0 --port 8080
```

The application starts the web server, plugins, configured IM adapters, and MCP connections, then waits for events. Once started, open the configured address in a browser, for example:

```text
http://127.0.0.1:8080/
```

If the UI is not present, the server attempts an automatic installation. If that fails, the server displays a message explaining where to install the UI files. The API is mounted under `/backend-api`; for example, the system status endpoint is documented as `GET /backend-api/api/system/status`. Most API endpoints require a JWT bearer token. See the [web API overview](kirara_ai/web/README.md) and the API-specific documentation under `kirara_ai/web/api/`.

The repository includes sample workflows in `data/workflows/` and dispatch rules in `data/dispatch_rules/rules.yaml`. The supplied rules include chat, dice, gacha, help, memory-clearing, and fallback routes.

### Docker

Build the image from the repository root:

```bash
docker build -t kirara-ai .
```

Run it with port 8080 published:

```bash
docker run --name kirara-ai -p 8080:8080 kirara-ai
```

The container startup script creates `/app/data` if needed, copies bundled default data into an empty data directory, creates a basic config binding the web server to `0.0.0.0:8080` if no config exists, and launches the application. To keep configuration and runtime data outside the container, mount a host data directory at `/app/data`:

```bash
docker run --name kirara-ai -p 8080:8080 \
  -v "$PWD/data:/app/data" kirara-ai
```

The Docker build downloads the web UI and installs it under `/app/web`.

## Development

The source package is `kirara_ai/`; tests are in `tests/`. The main subsystems are separated into packages for configuration, database migrations, events, IM, LLMs, memory, media, plugins, tracing, web APIs, and workflow execution.

To add workflow behavior, implement or extend blocks under `kirara_ai/workflow/implementations/blocks` and register them through the block registry. Workflow definitions and dispatch rules are loaded from the data directories. For API changes, the web application registers modular API blueprints; the overview and module READMEs describe the API areas.

Plugins can be discovered externally and loaded by the plugin manager. The included plugin setup files use the `chatgpt_mirai.plugins` entry-point group. Follow the existing plugin packages when adding a plugin or adapter.

The repository’s pre-commit configuration includes `isort` and `autoflake`. Install and run the configured hooks with:

```bash
python -m pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Database migrations are managed with Alembic. The repository includes `alembic.ini` and migration scripts under `kirara_ai/alembic/`.

## Testing

Run the test suite from the repository root:

```bash
python -m pytest
```

To run a subset, pass a test directory or file, for example:

```bash
python -m pytest tests/workflow_executor
python -m pytest tests/test_config_loader.py
```

Pytest is configured for strict asyncio mode. Tests cover configuration loading, workflow building and execution, memory, tracing, media, MCP, adapters, web APIs, and authentication. Some media tests use a network image URL, so those tests may require network access.

## Documentation and support

- [Web API overview](kirara_ai/web/README.md)
- [API module documentation](kirara_ai/web/api/)
- [Project documentation](https://kirara-docs.app.lss233.com)
- [Issue tracker](https://github.com/lss233/chatgpt-mirai-qq-bot/issues)

## License

This project is licensed under the **GNU Affero General Public License v3.0 only (AGPL-3.0-only)**. See [`LICENSE`](LICENSE) for the complete terms.

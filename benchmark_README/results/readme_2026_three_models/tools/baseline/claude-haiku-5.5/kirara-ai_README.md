# Kirara AI

Kirara AI is a Python framework for building AI agents. It provides a workflow engine built from configurable blocks, message dispatch rules that route incoming messages to workflows, instant messaging (IM) adapters, LLM backend adapters, memory and media management, tracing, and a web management API. The package is published as `kirara-ai` (version `3.3.0a2`) and is licensed under AGPL-3.0-only.

## Features

Based on the modules in the repository, Kirara AI includes:

- **Workflows and blocks**: Workflows are composed of blocks (for example, message, LLM, memory, game, and system blocks) connected by wires. Workflow definitions are stored as YAML under `data/workflows/`.
- **Dispatch rules**: Rules in `data/dispatch_rules/rules.yaml` select a workflow for each message using prefix, keyword, regex, chat type, bot mention, and fallback matching.
- **IM adapters**: Bundled plugins cover HTTP legacy, QQBot, Telegram, and WeCom.
- **LLM adapters**: Bundled presets cover AlibabaCloud, Claude, DeepSeek, Gemini, MiniMax, Mistral, Moonshot, Ollama, OpenAI, OpenRouter, SiliconFlow, Tencent Cloud, Volcengine, and Voyage.
- **Memory**: Scoped memory (member, group, global) with file or Redis persistence.
- **Media**: Media registration, metadata, and cleanup.
- **MCP**: Connections to Model Context Protocol servers over `stdio` or `sse`.
- **Plugins**: Internal plugins live under `kirara_ai/plugins/`, and external plugins are discovered through the `chatgpt_mirai.plugins` entry point group.
- **Web API**: A REST API under `/backend-api` for managing IMs, LLMs, dispatch rules, blocks, workflows, plugins, system status, media, tracing, and MCP servers.
- **Database migrations**: SQLite storage at `./data/db/kirara.db`, managed with Alembic.

## Requirements

- Python 3.10 or newer (`requires-python = ">=3.10"`). The Docker image uses Python 3.11, and CI runs tests on Python 3.13 on Windows.
- Dependencies are declared in `pyproject.toml`. Key packages include Quart, FastAPI, Hypercorn, SQLAlchemy, Alembic, Pydantic, loguru, and MCP.
- For Docker builds, the image installs `wkhtmltopdf`, `ffmpeg`, `curl`, `jq`, `libmagic1`, and `unzip`.

## Installation

### From source

Install the project from the repository root:

```bash
python -m pip install .
```

For development, CI uses an editable install on Windows:

```bash
python -m pip install -e .
```

### With Docker

The repository includes a two-stage `Dockerfile`. The first stage builds a wheel with `python -m build`. The second stage installs the wheel, downloads the latest `kirara-ai-webui` package from npm into `/app/web`, and removes build-only tools. The container exposes port `8080` and starts with `docker/start.sh`.

```bash
docker build -t kirara-ai .
docker run -p 8080:8080 kirara-ai
```

CI also publishes images to Docker Hub as `lss233/kirara-agent-framework`, tagged `latest` by a manual workflow and with the Git tag by a tag-triggered workflow.

On container start, `docker/start.sh`:

1. Creates `/app/data` if it is missing.
2. Copies default data into `/app/data` if that directory is empty.
3. Writes a default `config.yaml` that sets `web.host` to `0.0.0.0` and `web.port` to `8080`, if none exists.
4. Creates a virtual environment at `/app/data/venv` if one does not exist.
5. Runs `python -m kirara_ai`.

### Windows quickstart

A GitHub Actions workflow builds a Windows x64 quickstart package. It bundles WinPython, FFmpeg, the Web UI, the `data` directory, and the startup scripts from `.github/quickstarts/windows/scripts/`. Release tags also upload this package as a zip archive.

## Usage

### Starting the server

Run the application with either command:

```bash
python -m kirara_ai
kirara_ai
```

Both commands call `kirara_ai.__main__:main`. The following options override the configured web address:

| Option | Description |
|--------|-------------|
| `-H`, `--host` | Overrides the service listen address |
| `-p`, `--port` | Overrides the service listen port |

Example:

```bash
python -m kirara_ai -H 127.0.0.1 -p 8080
```

On startup, the application loads the configuration, initializes the database and plugins, loads workflows, dispatch rules, LLM backends, and MCP servers, starts the web server, and then starts the IM adapters. When the server is ready, it logs the local WebUI address (`http://127.0.0.1:<port>/`).

### Web interface and API

The web server serves the Web UI from the `web` directory in the working directory. If `index.html` is missing, the application attempts to install the WebUI automatically from the npm registry configured under `update.npm_registry`. If that fails, it displays instructions for manual installation.

The REST API is mounted at `/backend-api`. Most endpoints require a JWT bearer token:

```http
Authorization: Bearer <your-jwt-token>
```

To obtain a token, POST a password to the login endpoint:

```http
POST /backend-api/api/auth/login
Content-Type: application/json

{
    "password": "your-password"
}
```

According to the API documentation, the admin password is created on first startup. Error responses use the JSON format `{"error": "..."}`.

### Stopping the server

Press `Ctrl+C` to stop the application gracefully. A second interrupt logs a warning, and a third forces shutdown.

### Logs

Logs are written to the `logs/` directory. The file sink rotates at midnight, keeps seven days of logs, and compresses old files as zip archives.

## Configuration

Configuration is read from `./data/config.yaml`. The repository provides `config.yaml.example` as a template:

```bash
cp config.yaml.example data/config.yaml
```

If the file does not exist, the application logs a warning and uses built-in defaults. The data directory can be changed with the `DATA_PATH` environment variable. If it is not set, the application uses `./data`.

The main configuration sections, as defined in `kirara_ai/config/global_config.py`, are:

| Section | Purpose | Notable defaults |
|---------|---------|------------------|
| `ims` | IM adapter list (`name`, `enable`, `adapter`, `config`) | Empty list |
| `llms.api_backends` | LLM backends (`name`, `adapter`, `config`, `enable`, `models`) | Empty list |
| `mcp.servers` | MCP servers (`id`, `connection_type`, `command`, `args`, `url`, `env`, `headers`, `enable`) | Empty list |
| `defaults.llm_model` | Default LLM model name | `gemini-1.5-flash` |
| `memory` | Memory persistence (`file` or `redis`), `max_entries`, `default_scope` | `file`, `100`, `member` |
| `web` | `host`, `port`, `secret_key`, `password_file` | `127.0.0.1`, `8080`, `./data/web/password.hash` |
| `plugins` | `enable` list of external plugins and `market_base_url` | Empty list |
| `update` | `pypi_registry` and `npm_registry` URLs | PyPI and npm public registries |
| `frpc` | FRP client settings (`enable`, `server_addr`, `server_port`, `token`, `remote_port`) | Disabled |
| `system` | `timezone` | `Asia/Shanghai` |
| `tracing` | `llm_tracing_content` | `false` |
| `media` | `cleanup_duration` (days), `auto_remove_unreferenced` | `30`, `true` |

Example snippet:

```yaml
web:
  host: 127.0.0.1
  port: 8080

system:
  timezone: Asia/Shanghai
```

Other configuration files in the repository include:

- `data/dispatch_rules/rules.yaml` for message routing.
- `data/workflows/chat/*.yaml` for chat workflows such as `normal_multimodal`, `dsr_thinking`, `memory_store`, and `talk_break`.
- `alembic.ini` for database migration settings. It points to `sqlite:///./data/db/kirara.db`.

## Plugins

Internal plugins are loaded from `kirara_ai/plugins/`. Each external plugin is a Python package that exposes an entry point in the `chatgpt_mirai.plugins` group. The repository's plugin `setup.py` files show this pattern. External plugins are listed under `plugins.enable`, and the plugin API can search a marketplace configured by `plugins.market_base_url`.

## Development

### Project layout

- `kirara_ai/`: the framework package. Key subpackages include `workflow/`, `llm/`, `im/`, `memory/`, `media/`, `tracing/`, `plugin_manager/`, `mcp_module/`, and `web/`.
- `kirara_ai/alembic/`: database migrations.
- `data/`: default workflows, dispatch rules, fonts, and runtime data directories.
- `docker/`: container startup script.
- `tests/`: test suite.

### Code quality

- `.pre-commit-config.yaml` runs `isort` and `autoflake` (with `--remove-all-unused-imports`).
- `.pylintrc` and `.editorconfig` define lint and editor settings.
- `pyproject.toml` configures mypy with selected error codes disabled.

### Continuous integration

The GitHub Actions workflows include:

- **Run Tests**: runs on pushes and pull requests. On Ubuntu, it builds the Docker image and runs pytest with coverage inside the container. On Windows, it runs pytest on Python 3.13.
- **PR Code Review**: runs mypy on changed Python files and posts line-level review comments for type errors in changed lines.
- **Project Check**: runs mypy on the `kirara_ai` package on pushes to `master` and opens an issue if problems are found.
- **Docker build workflows** and **Windows Quickstart** described above.
- **Stale**: marks issues and pull requests inactive for 60 days as stale and closes them 14 days later.
- **Dependabot**: checks pip dependencies weekly.

### Contributing

The repository includes bug report and feature request issue templates in `.github/ISSUE_TEMPLATE/`. The `.cursor/rules/create-workflow.mdc` file contains workflow creation guidance for Cursor users.

## Testing

Tests are located in `tests/` and use pytest. `pytest.ini` sets `asyncio_mode = strict`, `asyncio_default_fixture_loop_scope = class`, and `pythonpath = .`.

Install pytest, then run the full suite from the repository root:

```bash
python -m pip install pytest
python -m pytest ./tests -v
```

Coverage is also used in CI:

```bash
python -m pytest ./tests -v --cov=kirara_ai --cov-report=term-missing
```

The test directories cover:

- `tests/llm_adapters/`: adapter tests against mock FastAPI servers for Gemini, Ollama, OpenAI, and Voyage.
- `tests/memory/`: composers, decomposers, scopes, persistence, and the memory manager.
- `tests/system_blocks/` and `tests/workflow_executor/`: block and executor behavior.
- `tests/tracing/`: tracing core, decorators, LLM tracer, and models.
- `tests/web/`: API tests for auth, IM, LLM, media, plugin, system, and workflow endpoints.
- `tests/test_mcp_server.py`, `tests/test_media.py`, `tests/test_config_loader.py`, and others.

Some tests need network access. For example, `tests/test_media_element.py` fetches `https://httpbin.org/image/jpeg`.

## License

Kirara AI is licensed under the **GNU Affero General Public License v3.0** (`AGPL-3.0-only`), as declared in `pyproject.toml` and provided in the `LICENSE` file. Under this license, if you modify the program and make it available for remote interaction over a network, you must offer the Corresponding Source of your modified version to those users.

Contact information in the repository is limited to the package author entry in `pyproject.toml`: Lss233, `i@lss233.com`. The repository does not provide a postal mailing address.

Project links from `pyproject.toml`:

- Homepage: https://github.com/lss233/chatgpt-mirai-qq-bot
- Bug tracker: https://github.com/lss233/chatgpt-mirai-qq-bot/issues
- Documentation: https://kirara-docs.app.lss233.com

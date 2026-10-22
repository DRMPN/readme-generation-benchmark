# Kirara AI

Kirara AI is a framework for building AI agents and chatbots. It connects instant-messaging (IM) platforms and large language model (LLM) backends, routes incoming messages through configurable workflows, and provides a web management UI.

The project is at version `3.3.0a2` (alpha) and is licensed under the [GNU AGPL-3.0-only](LICENSE).

## Features

Based on the code in this repository, Kirara AI provides:

- **IM adapters** that receive and send messages on chat platforms (see [IM platforms](#im-platforms)).
- **LLM backend registry** with built-in adapters for many providers (see [LLM providers](#llm-providers)).
- **Workflows**: YAML-defined processing pipelines built from blocks, loaded from `data/workflows/`.
- **Dispatch rules**: rules that decide which workflow handles an incoming message, defined in `data/dispatch_rules/rules.yaml`. The bundled rules, for example, route private chats and group messages that start with `/chat` or @-mention the bot to the chat workflow.
- **Memory system** with `member`, `group`, and `global` scopes, persisted to files or Redis.
- **MCP client** support for connecting to MCP servers over `stdio` or `sse`.
- **Plugin system** with bundled (internal) plugins and external plugins distributed as Python packages.
- **LLM tracing**, with an option to record request content.
- **Web management API and UI** served on port 8080 by default.
- **Optional FRP tunnel** (`frpc`) for exposing the web service, downloaded at runtime.

## Requirements

- Python 3.10 or newer (`requires-python = ">=3.10"` in `pyproject.toml`). The Dockerfile uses Python 3.11.
- `libmagic` (installed automatically on Windows via `python-magic-bin`; on Linux the Dockerfile installs `libmagic1`).
- The Docker image also installs `ffmpeg` and `wkhtmltopdf`. These are not listed in `pyproject.toml`, so if you run from source you must install them yourself if you need features that use them.
- Redis is optional, and only needed if you set `memory.persistence.type` to `redis`.

## Installation

### Option 1: Docker

The repository's workflow publishes an image to Docker Hub as `lss233/kirara-agent-framework:latest` for `linux/amd64` and `linux/arm64`. To build the image yourself from this repository:

```bash
docker build -t kirara-ai .
docker run -p 8080:8080 -v "$(pwd)/data:/app/data" kirara-ai
```

Replace `kirara-ai` with `lss233/kirara-agent-framework:latest` to use the published image.

On first start, `docker/start.sh`:

- copies the default data (`data/`) into `/app/data` if that directory is empty,
- creates `/app/data/config.yaml` with the web server bound to `0.0.0.0:8080` if the file does not exist,
- creates a Python virtual environment at `/app/data/venv`,
- starts the application.

Mounting `./data` to `/app/data` keeps configuration, memory, and the database between container restarts.

The Docker build downloads the latest `kirara-ai-webui` package from npm and places it in `/app/web`.

### Option 2: From source

```bash
git clone https://github.com/lss233/chatgpt-mirai-qq-bot.git
cd chatgpt-mirai-qq-bot
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

The project's `pyproject.toml` defines a `kirara_ai` console script that points to `kirara_ai.__main__:main`.

### Option 3: Windows quickstart

The repository includes a launcher at `.github/quickstarts/windows/scripts/启动.cmd`. It sets `PATH` to a bundled Python (`WPy64-31320\python`) and `ffmpeg\bin` folder, creates `data\venv` if needed, activates it, and runs `python -m kirara_ai`. The portable Python and ffmpeg folders are not part of this repository.

## Configuration

Kirara AI reads its configuration from `./data/config.yaml`, relative to the working directory.

If the file does not exist, the application logs a warning and starts with built-in defaults. To configure it, copy the example file:

```bash
mkdir -p data
cp config.yaml.example data/config.yaml
```

Then edit `data/config.yaml`. The example file contains comments in Chinese. The main sections are:

| Section | Purpose |
| --- | --- |
| `ims` | List of IM adapter instances. Each has `name`, `enable`, `adapter`, and an adapter-specific `config`. |
| `llms.api_backends` | List of LLM backends. Each has `name`, `adapter`, `enable`, `config` (for example `api_key` and `api_base`), and `models`. |
| `defaults.llm_model` | Default model name used by the bot. |
| `plugins.enable` | List of external plugin names to enable. |
| `plugins.market_base_url` | Base URL of the plugin market. |
| `mcp.servers` | MCP servers to connect to. Each has `id`, `connection_type` (`stdio` or `sse`), `command`/`args`/`env` (for `stdio`), or `url`/`headers` (for `sse`), and `enable`. |
| `memory` | Memory settings: `persistence.type` (`file` or `redis`), `persistence.file.storage_dir`, `persistence.redis` (`host`, `port`, `db`), `max_entries`, and `default_scope` (`member`, `group`, or `global`). |
| `web` | Web server settings: `host` (default `127.0.0.1`), `port` (default `8080`), `secret_key`, and `password_file` (default `./data/web/password.hash`). |
| `system.timezone` | Timezone (default `Asia/Shanghai`). |
| `tracing.llm_tracing_content` | Whether to record LLM request content (default `false`). |
| `media` | Media cleanup settings: `cleanup_duration` (days, default 30) and `auto_remove_unreferenced` (default `true`). |
| `frpc` | FRP tunnel settings: `enable`, `server_addr`, `server_port`, `token`, and `remote_port`. |
| `update` | `pypi_registry` and `npm_registry` URLs used for update checks. |

Example IM and LLM entries from `config.yaml.example`:

```yaml
ims:
  - name: "telegram-bot-1234"
    enable: true
    adapter: "telegram"
    config:
      token: "abcd"

llms:
  api_backends:
    - name: "deepseek-official"
      adapter: "deepseek"
      enable: true
      config:
        api_key: "your-api-key"
        api_base: "https://api.deepseek.com/v1"
      models:
        - "deepseek-chat"
```

Replace the placeholder tokens and keys with your own values. The example also sets `web.secret_key`, which you should change to a secure value.

### Command-line options

```bash
python -m kirara_ai [-H HOST] [-p PORT]
```

- `-H`, `--host`: overrides the web server listen address.
- `-p`, `--port`: overrides the web server port.

## Running

Start the application from the directory that contains `data/`:

```bash
python -m kirara_ai
# or, after pip install -e .
kirara_ai
```

On startup, the application:

1. loads the configuration and initializes the database (SQLAlchemy and Alembic; the database is stored in `./data/db`),
2. discovers and loads plugins,
3. loads workflows, dispatch rules, LLM backends, and MCP servers,
4. starts the web server,
5. starts the enabled IM adapters and connects to MCP servers.

When the web server is running, the log prints its local address, `http://127.0.0.1:<port>/` by default.

### Web UI

The web UI is served from the `web/` directory under the working directory. If `web/index.html` is missing, the application downloads the latest `kirara-ai-webui` package from npm into `web/` on startup. Refresh the browser after installation finishes.

On the first visit, the web UI asks you to set a password. The password hash is stored in `web.password_file` (default `./data/web/password.hash`). Later logins check against this file, and the password can be changed through the API.

### Stopping

Press Ctrl+C once to shut down gracefully. Pressing it a third time forces the process to exit.

## IM platforms

Adapters are registered by the bundled plugins in `kirara_ai/plugins/`. The `adapter` value in `ims` must match one of these names:

| Adapter name | Platform | Notes |
| --- | --- | --- |
| `telegram` | Telegram bot | Uses the `python-telegram-bot` library. Requires a bot token from @BotFather. |
| `qqbot` | QQ Open Platform bot | Requires a server that can receive QQ webhook requests. In groups, the bot must be @-mentioned. |
| `wecom` | WeCom (Enterprise WeChat) application / WeChat Official Account | Requires a server that can receive webhook requests. |
| `http_legacy` | HTTP API | Lets third-party programs send and receive messages over HTTP. Supports an optional `api_key`. |

## LLM providers

The bundled `llm_preset_adapters` plugin registers these adapters. The `adapter` value in `llms.api_backends` is matched case-insensitively:

`OpenAI`, `DeepSeek`, `Gemini`, `Ollama`, `Claude`, `SiliconFlow`, `TencentCloud`, `AlibabaCloud`, `Moonshot`, `OpenRouter`, `Minimax`, `Volcengine`, `Mistral`

Each backend entry takes provider-specific `config` values. Check each adapter's config class under `kirara_ai/plugins/llm_preset_adapters/` for the exact fields.

## Plugins

Kirara AI has two kinds of plugins:

- **Internal plugins** live in `kirara_ai/plugins/`. Every subdirectory there is loaded automatically at startup. These include the IM adapters, LLM presets, `bundled_frpc`, and `im_http_legacy_adapter`.
- **External plugins** are installed Python packages that expose an entry point in the `Plugin.ENTRY_POINT_GROUP` group. They are discovered at startup, and they are loaded only if their name appears in `plugins.enable`.

Plugins extend the framework through the plugin base class in `kirara_ai/plugin_manager/plugin.py`. A plugin can register IM adapters, LLM adapters, and static assets, and it can hook into the application lifecycle through `on_load`, `on_start`, and `on_stop`.

## Workflows and blocks

Workflows are defined as YAML files. The bundled examples are in `data/workflows/chat/`:

- `normal_multimodal.yaml`
- `dsr_thinking.yaml`
- `memory_store.yaml`
- `talk_break.yaml`

Blocks are the reusable processing steps that workflows are built from. Built-in block categories include system, IM, LLM, memory, MCP tools, variables, and game features (dice and gacha). For authoring guidance, see `.cursor/rules/create-workflow.mdc`.

## MCP

Kirara AI includes an MCP client (`kirara_ai/mcp_module/`) that connects to servers listed under `mcp.servers` in the configuration. It supports `stdio` and `sse` connection types. Connected MCP tools can be used from workflows through the MCP tool block.

## Running tests

The test suite is in `tests/` and uses `pytest` (configured in `pytest.ini` with `asyncio_mode = strict`). Install the project and run:

```bash
pip install -e .
pip install pytest
python -m pytest ./tests -v
```

CI (`.github/workflows/run-tests.yml`) runs the tests in a Docker container on Ubuntu, and natively on Windows with Python 3.13.

## Project structure

```text
kirara_ai/            Main package
  __main__.py         CLI entry point
  entry.py            Application startup and shutdown
  config/             Pydantic configuration models and loader
  database/           Database manager (SQLAlchemy)
  alembic/            Database migrations
  im/                 IM abstractions and manager
  llm/                LLM abstractions, registry, and manager
  mcp_module/        MCP client
  media/              Media handling and cleanup
  memory/             Memory scopes, composers, decomposers, persistence
  plugin_manager/     Plugin loader and base classes
  plugins/            Bundled plugins
  tracing/            LLM tracing
  web/                Quart and FastAPI web server, API routes, and auth
  workflow/           Workflow, block, and dispatch core
data/                 Default workflows, dispatch rules, and fonts
docker/start.sh       Container startup script
tests/                Test suite
```

## Documentation

- Project documentation: <https://kirara-docs.app.lss233.com>
- Issues: <https://github.com/lss233/chatgpt-mirai-qq-bot/issues>

## License

Kirara AI is licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only). See [LICENSE](LICENSE) for the full text.

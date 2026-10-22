# Kirara AI

Kirara AI is a Python framework for building AI agents. It connects instant messaging (IM) platforms to large language model (LLM) backends through a block-based workflow engine, and ships with a Web UI for managing everything — IM adapters, LLM backends, workflows, dispatch rules, plugins, memory, media, and MCP servers.

- **Package:** `kirara-ai` (current version: 3.3.0a2)
- **Author:** Lss233
- **License:** AGPL-3.0-only
- **Python:** 3.10 or newer (the MCP component requires 3.10+)
- **Documentation:** https://kirara-docs.app.lss233.com
- **Homepage:** https://github.com/lss233/chatgpt-mirai-qq-bot
- **Issue tracker:** https://github.com/lss233/chatgpt-mirai-qq-bot/issues

## Features

- **IM adapters (built-in plugins):**
  - **Telegram** — official bot API, supports private chats, group chats, and Markdown messages
  - **QQ (QQ Open Platform)** — official bot, receives events via Webhook; must be @-mentioned in groups
  - **WeCom / WeChat Official Account** — official message API via Webhook
  - **HTTP API (legacy)** — HTTP message API for integrating third-party programs
- **LLM backends (preset adapters):** OpenAI, DeepSeek, Gemini, Ollama, Claude, SiliconFlow, TencentCloud, AlibabaCloud, Moonshot, OpenRouter, Minimax, Volcengine, Mistral, and Voyage
- **Workflow engine:** compose workflows from typed blocks (IM, LLM, memory, game, system, variables, MCP tools); a dispatcher routes incoming messages to workflows using configurable rules
- **Dispatch rules:** regex, message prefix, keywords, bot mention, chat sender (sender ID / group), and random chance
- **Preset workflows:** default chat workflow, dice roll, gacha, help, and clear-memory
- **Memory system:** per-member, per-group, and global scopes; pluggable composer/decomposer strategies; persistence to local files or Redis
- **Media management:** media library with reference tracking and automatic cleanup of unreferenced files
- **MCP support:** connect external Model Context Protocol servers (stdio or SSE) and use their tools as workflow blocks
- **Tracing:** tracing manager with an LLM tracer for observing workflow and LLM activity
- **Web UI + REST API:** async Quart-based backend serving a separate frontend, JWT-protected API covering auth, IM, LLM, dispatch, blocks, workflows, plugins, MCP, tracing, media, and system status
- **Plugin system:** internal plugins bundled with the framework, external plugins installed at runtime, and a plugin market; plugins can extend the IM and LLM registries, add workflow blocks, and register web routes
- **Persistence:** SQLAlchemy-based database with Alembic migrations
- **FRP tunneling (optional):** bundled `frpc` plugin to expose the local Web UI to the internet

## Requirements

- Python **3.10+**
- A configuration file (see below)

## Quick Start (from source)

1. **Install the package**

   ```bash
   pip install .
   ```

2. **Create a configuration file**

   ```bash
   mkdir -p data
   cp config.yaml.example data/config.yaml
   ```

   Then edit `data/config.yaml` to configure your IM platforms and LLM backends. If the file does not exist, the application starts with default configuration and logs a warning.

3. **Run**

   ```bash
   python -m kirara_ai
   # or, after pip install:
   kirara_ai
   ```

   Optional command-line flags:

   - `-H, --host` — override the web server listen address
   - `-p, --port` — override the web server listen port

4. **Open the Web UI**

   By default it is available at `http://127.0.0.1:8080/`. On first login, the password you submit becomes the admin password. The Web UI frontend is served from a `web/` directory; if it is missing, the backend can download it automatically (it is also fetched automatically in the Docker image).

## Quick Start (Docker)

CI publishes multi-architecture images (amd64/arm64) to Docker Hub as `lss233/kirara-agent-framework`:

```bash
docker run -d --name kirara-ai \
  -p 8080:8080 \
  -v kirara-data:/app/data \
  lss233/kirara-agent-framework:latest
```

- The container exposes port **8080**; the startup script writes a minimal `data/config.yaml` with `web.host: 0.0.0.0` so the Web UI is reachable.
- All runtime data lives in `/app/data` — mount a volume there to persist configuration, workflows, memory, and media.
- The image includes `ffmpeg`, `wkhtmltopdf`, and `libmagic1`, plus the Sarasa Mono SC font.

A Windows quickstart package (bundled Python, FFmpeg, Web UI, and a one-click launcher) is built by CI as `quickstart-windows-kirara-ai-amd64`.

## Configuration

Configuration is loaded from `./data/config.yaml`. See `config.yaml.example` for a fully commented sample. Top-level sections (defaults in parentheses):

| Section | Purpose |
| --- | --- |
| `ims` | List of IM platform instances: `name`, `enable`, `adapter`, adapter-specific `config` |
| `llms` | `api_backends`: LLM providers with `adapter`, `enable`, `config` (e.g. `api_key`, `api_base`), and available `models` |
| `mcp` | MCP servers: connection by `url` (SSE) or `command`/`args`/`env` (stdio), custom `headers`, `enable` |
| `web` | Web server `host` (`127.0.0.1`), `port` (`8080`), `secret_key` (JWT signing), `password_file` (`./data/web/password.hash`) |
| `plugins` | `enable`: list of external plugins to load; `market_base_url`: plugin market API |
| `memory` | `persistence` (`file` or `redis`, with per-type options), `max_entries` (100), `default_scope` (`member`) |
| `media` | Cleanup interval (days) and whether to auto-remove unreferenced media |
| `tracing` | Whether to record LLM request/response content (`llm_tracing_content`) |
| `frpc` | FRP tunnel: `enable`, `server_addr`, `server_port`, `token`, `remote_port` |
| `system` | `timezone` (default `Asia/Shanghai`) |
| `update` | Custom PyPI / npm registry URLs for update checks |
| `defaults` | `llm_model`: default model used by chat workflows |

## How It Works

1. Incoming messages arrive at an **IM adapter** (Telegram, QQ, WeCom, HTTP API, or a plugin-provided adapter).
2. The **WorkflowDispatcher** evaluates **dispatch rules** (regex, prefix, keyword, bot mention, sender, random chance) and selects a workflow.
3. The selected **workflow** executes as a graph of **blocks** — e.g. receive message → query chat memory → build prompt → LLM chat completion → convert response → send message — with typed inputs and outputs.
4. The **memory system** persists conversation state using the configured scope and storage backend; **tracing** records what happened; the **media manager** handles images and other media.

The default `chat/normal` workflow implements exactly this pipeline and is pre-registered, along with `game/dice`, `game/gacha`, `system/help`, and `system/clear_memory`. Workflows are stored under `data/workflows/` and dispatch rules under `data/dispatch_rules/rules.yaml`; both can be edited through the Web UI.

## Project Layout

```
kirara_ai/            # Main package
├── entry.py          # Application bootstrap and shutdown
├── im/               # IM adapter interfaces, message model, manager, registries
├── llm/              # LLM adapter interfaces, request/response formats, manager
├── workflow/         # Block/workflow core, executor, dispatch rules, built-in blocks & workflows
├── memory/           # Memory scopes, composer/decomposer strategies, persistence
├── media/            # Media manager, types, carriers
├── mcp_module/       # MCP server manager and client
├── plugins/          # Bundled plugins (IM adapters, preset LLM adapters, frpc)
├── plugin_manager/   # Plugin discovery, loading, event bus
├── web/              # Web server, auth (JWT), and REST API modules
├── config/           # Config loader and global config models
├── ioc/              # Dependency injection container
├── events/           # Event bus
├── tracing/          # Tracing manager and LLM tracer
└── database/         # SQLAlchemy database manager (Alembic migrations)
tests/                # pytest test suite (workflows, memory, LLM adapters, tracing, web API, ...)
data/                 # Runtime data: config.yaml, workflows, dispatch rules, memory, media, web UI, fonts
docker/               # Container startup script
Dockerfile            # Multi-stage build (wheel + Web UI download)
config.yaml.example   # Commented sample configuration
alembic.ini           # Database migration configuration
```

## Development

- **Install in editable mode:** `pip install -e .`
- **Run tests:** `python -m pytest tests` (async tests use strict asyncio mode; CI runs the suite on Ubuntu and Windows)
- **Code style & checks:** the repository ships with configuration for `pre-commit` (`.pre-commit-config.yaml`), `pylint` (`.pylintrc`), `mypy` (in `pyproject.toml`), and `editorconfig` (`.editorconfig`)
- **Database migrations:** managed with Alembic (`alembic.ini`)

### Writing plugins

Plugins subclass `kirara_ai.plugin_manager.plugin.Plugin` and implement lifecycle hooks (`on_load`, `on_start`, `on_stop`). Through dependency injection they can register IM adapters, LLM backends, workflow blocks, and web routes. Internal plugins live in `kirara_ai/plugins/`; external plugins are discovered at runtime and enabled via the `plugins.enable` config list or the Web UI.

## License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0-only). See [LICENSE](LICENSE) for details.

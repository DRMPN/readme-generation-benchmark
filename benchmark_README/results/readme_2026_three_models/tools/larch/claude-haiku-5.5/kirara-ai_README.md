# Kirara AI

Kirara AI is a Python framework for building multimodal LLM chatbots that run on instant messaging platforms. It connects large language model providers to chat platforms, supports configurable workflows and plugins, and includes persistent memory, media handling, and a web-based management interface.

> **Note:** This README was written from the repository's file layout. Commands, endpoints, and configuration keys are inferred from file names and should be checked against `pyproject.toml`, `start.sh`, `config.yaml.example`, and the source code before you rely on them.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Option 1: Docker](#option-1-docker)
  - [Option 2: From Source](#option-2-from-source)
- [Configuration](#configuration)
  - [Main Configuration (`config.yaml`)](#main-configuration-configyaml)
  - [LLM Providers](#llm-providers)
  - [IM Platforms](#im-platforms)
  - [Memory Storage](#memory-storage)
- [Workflows](#workflows)
- [Plugins](#plugins)
  - [Built-in Plugins](#built-in-plugins)
  - [Writing a Plugin](#writing-a-plugin)
- [Memory System](#memory-system)
- [Media Handling](#media-handling)
- [Web Interface and API](#web-interface-and-api)
- [Database Migrations](#database-migrations)
- [Testing](#testing)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **Multiple LLM providers.** Adapters for OpenAI, Anthropic Claude, Google Gemini, Ollama, DeepSeek, Mistral, Moonshot, Tencent Cloud, SiliconFlow, OpenRouter, MiniMax, Volcengine, Alibaba Cloud, and Voyage (embeddings and reranking).
- **Multiple chat platforms.** Adapters for QQ (QQ Bot), Telegram, WeCom (Enterprise WeChat), and a generic HTTP legacy adapter.
- **Multimodal support.** Text, images, and other media types are represented as typed media objects with MIME detection and metadata.
- **Workflow engine.** Message handling is modeled as composable blocks wired together by YAML-defined workflows, with a registry, a builder, and an executor.
- **Dispatch rules.** Incoming messages are routed to workflows through system, message, and sender rules.
- **Plugin system.** Plugins are discovered and loaded at runtime, can register workflow blocks and commands, and communicate through an event bus.
- **Persistent memory.** Conversation memory can be stored in local files or Redis.
- **Built-in games and utilities.** Examples include dice rolling, a gacha system, a help command, and user profiles.
- **Web management interface.** REST routes cover LLM, IM, plugin, workflow, and system management, with an authentication layer.
- **Code diagnostics.** Modules for pyflakes, Jedi, and import checks, plus a Python LSP integration, appear to support validating user-written plugin or workflow code.
- **Optional tunneling.** An `frpc` manager allows exposing a locally running instance through frp, which is useful for receiving webhooks behind NAT.
- **MCP server.** A Model Context Protocol server module is included.
- **Database migrations.** Alembic is configured for schema versioning.

---

## Architecture Overview

```
                ┌─────────────────────────────────────────┐
                │              IM Platforms               │
                │ QQ Bot · Telegram · WeCom · HTTP Legacy │
                └────────────────────┬────────────────────┘
                                     │  messages / media
                                     ▼
                ┌─────────────────────────────────────────┐
                │        Adapters & Message Models        │
                └────────────────────┬────────────────────┘
                                     ▼
                ┌─────────────────────────────────────────┐
                │ Dispatcher (system / message / sender   │
                │ rules) → selects a workflow             │
                └────────────────────┬────────────────────┘
                                     ▼
                ┌─────────────────────────────────────────┐
                │ Workflow Engine                         │
                │ Builder → Executor → Blocks             │
                │ (decomposer / composer strategies)      │
                └──────┬──────────────────────┬───────────┘
                       ▼                      ▼
        ┌──────────────────────┐   ┌──────────────────────┐
        │ LLM Manager          │   │ Memory Manager       │
        │ provider adapters    │   │ file / Redis         │
        └──────────────────────┘   └──────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────────────────────┐
        │ Plugins (event bus, registry, loader)            │
        └──────────────────────────────────────────────────┘
                       ▲
                       │
        ┌──────────────────────────────────────────────────┐
        │ Web server · REST routes · Config · Logger · DI  │
        └──────────────────────────────────────────────────┘
```

**Message flow:**

1. An IM adapter receives a platform event and converts it into a normalized message with media attachments.
2. The dispatcher evaluates system, message, and sender rules to decide which workflow should handle it.
3. The workflow executor runs the blocks defined in the selected workflow. Blocks may call LLMs, read or write memory, invoke tools, or produce media.
4. The response is converted back into the platform's format and sent through the same adapter.

---

## Repository Structure

The layout below is a best-effort summary inferred from the file tree.

```
kirara-ai/
├── kirara_ai/                  # Main Python package
│   ├── config/                 # Config loading (config_loader, global_config, manager)
│   ├── im/                     # Chat platform integrations
│   │   ├── qqbot/              # QQ Bot adapter (adapter, message, sender, setup)
│   │   ├── telegram/           # Telegram adapter
│   │   ├── wecom/              # WeCom adapter (includes delegates)
│   │   ├── http_legacy/        # Legacy HTTP adapter
│   │   ├── im_registry.py
│   │   └── profile.py
│   ├── llm/                    # LLM integration layer
│   │   ├── adapters/           # One adapter per provider (openai, claude, gemini, ollama, ...)
│   │   ├── llm_manager.py
│   │   ├── llm_registry.py
│   │   ├── request.py / response.py / message.py / tool.py
│   │   ├── embedding.py / rerank.py
│   │   └── model_types.py
│   ├── workflow/               # Workflow engine
│   │   ├── blocks/             # Built-in workflow blocks
│   │   ├── builder.py
│   │   ├── executor.py
│   │   ├── dispatcher.py
│   │   ├── dispatch_rules/     # system_rules, message_rules, sender_rules
│   │   ├── decomposer_strategy.py / composer_strategy.py
│   │   ├── type_system.py / schema.py / param.py
│   │   └── registry.py
│   ├── memory/                 # Conversation memory
│   │   ├── memory_manager.py
│   │   └── persistence/        # file_persistence, redis_persistence
│   ├── media/                  # Media objects, MIME detection, metadata
│   ├── plugins/                # Plugin loader, plugin event bus, plugin models
│   ├── plugin_loader.py
│   ├── builtin plugins/        # chat, image, dice, gacha, help, basic, user_profile, ...
│   ├── web/ (or api/)          # Server, application, middleware, auth, routes
│   ├── diagnostics/            # Code checks: pyflakes, jedi, import, LSP
│   ├── frpc_manager.py         # frp tunnel manager
│   ├── mcp/                    # MCP server
│   ├── migrations/             # Alembic environment and versions
│   ├── logger.py
│   ├── container.py / inject.py  # Dependency injection
│   └── __main__.py             # Entry point
├── workflows/                  # Example workflow YAML files
│   ├── dsr_thinking.yaml
│   ├── normal_multimodal.yaml
│   ├── memory_store.yaml
│   ├── talk_break.yaml
│   └── rules.yaml
├── fonts/
│   └── sarasa-mono-sc-regular.ttf   # Font for rendering text into images
├── tests/                      # pytest test suite
├── config.yaml.example
├── pytest.ini
├── pyproject.toml
├── alembic.ini
├── Dockerfile
├── MANIFEST.in
├── start.sh
└── LICENSE
```

---

## Requirements

- Python 3.9 or newer (confirm the exact minimum in `pyproject.toml`)
- pip or another PEP 517-compatible installer
- Optional: Redis, if you use Redis-backed memory
- Optional: Docker and Docker Compose, for containerized deployment
- API keys for the LLM providers you intend to use
- Credentials for the IM platforms you intend to connect (for example, a QQ Bot app or a Telegram bot token)

---

## Installation

### Option 1: Docker

1. Copy the example configuration:

   ```bash
   cp config.yaml.example config.yaml
   ```

2. Edit `config.yaml` with your API keys and platform credentials (see [Configuration](#configuration)).

3. Build the image:

   ```bash
   docker build -t kirara-ai .
   ```

4. Run the container, mounting your configuration and data directories. Adjust the port to match your setup:

   ```bash
   docker run -d \
     --name kirara-ai \
     -p 8080:8080 \
     -v "$(pwd)/config.yaml:/app/config.yaml" \
     -v "$(pwd)/data:/app/data" \
     kirara-ai
   ```

### Option 2: From Source

1. Clone the repository and enter it:

   ```bash
   git clone <repository-url> kirara-ai
   cd kirara-ai
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```

3. Install the package in editable mode with development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

   If the project does not define a `dev` extra, run `pip install -e .` and install test dependencies separately.

4. Prepare the configuration:

   ```bash
   cp config.yaml.example config.yaml
   ```

5. Apply database migrations (see [Database Migrations](#database-migrations)):

   ```bash
   alembic upgrade head
   ```

6. Start the application:

   ```bash
   python -m kirara_ai
   # or
   ./start.sh
   ```

---

## Configuration

### Main Configuration (`config.yaml`)

All runtime settings live in `config.yaml`, which is created from `config.yaml.example`. The exact keys come from that example file. The sections below describe what is typically configured:

| Section | Purpose |
|---|---|
| Server | Host, port, and public URL for the web interface and webhooks |
| Auth | Admin credentials and token settings for the management API |
| LLM | Default provider, model names, and API keys per provider |
| IM | Enabled chat platforms and their credentials |
| Memory | Storage backend (file or Redis) and its options |
| Workflows | Which workflow files to load and which rules map messages to them |
| Plugins | Plugin directories and which plugins are enabled |
| Logging | Log level and output destinations |
| Tunnel | Optional frp settings for exposing the service |

Never commit `config.yaml` to version control, since it contains secrets.

### LLM Providers

Each provider has an adapter in `kirara_ai/llm/adapters/`. To use a provider:

1. Add its API key and any required endpoint or model settings to `config.yaml`.
2. Reference the provider and model in your workflow or default LLM configuration.

Supported adapters (from the source tree):

| Provider | Adapter | Notes |
|---|---|---|
| OpenAI | `openai_adapter.py` | Chat and vision models |
| Anthropic Claude | `claude_adapter.py` | |
| Google Gemini | `gemini_adapter.py` | |
| Ollama | `ollama_adapter.py` | Local models; no API key required |
| DeepSeek | `deepseek_adapter.py` | |
| Mistral | `mistral_adapter.py` | |
| Moonshot | `moonshot_adapter.py` | |
| Tencent Cloud | `tencentcloud_adapter.py` | |
| SiliconFlow | `siliconflow_adapter.py` | |
| OpenRouter | `openrouter_adapter.py` | Access to many models via one key |
| MiniMax | `minimax_adapter.py` | |
| Volcengine | `volcengine_adapter.py` | |
| Alibaba Cloud | `alibabacloud_adapter.py` | |
| Voyage | `voyage_adapter.py` | Embeddings and reranking |

Adapters can be checked with the tests in `tests/` (for example, `test_openai_adapter.py` and `test_ollama_adapter.py`).

### IM Platforms

Each platform has an adapter in `kirara_ai/im/`.

| Platform | Adapter | Setup notes |
|---|---|---|
| QQ Bot | `im/qqbot/` | Requires a QQ Bot application with app ID and secret |
| Telegram | `im/telegram/` | Requires a bot token from BotFather |
| WeCom | `im/wecom/` | Requires corp ID, agent ID, and secret; webhook must be publicly reachable |
| HTTP Legacy | `im/http_legacy/` | Generic HTTP-based integration kept for compatibility |

Each platform's `setup.py` and `README.md` (where present) describe its specific steps. Webhook-based platforms need a public URL. If you run locally, you can use the built-in frp tunnel manager or your own reverse proxy.

### Memory Storage

Conversation memory is handled by `memory_manager.py` and one of two persistence backends:

- **File persistence** (`file_persistence.py`): stores memory on local disk. Suitable for single-instance deployments.
- **Redis persistence** (`redis_persistence.py`): stores memory in Redis. Suitable for multiple instances or when you need shared, fast access.

Select the backend in `config.yaml`. The `memory_store.yaml` workflow handles how memory is written during conversations.

---

## Workflows

Workflows define how a message is processed. Each workflow is a YAML file that lists blocks and how their inputs and outputs are connected. The engine:

1. Loads workflow YAML files.
2. Validates them against the schema and the type system (`schema.py`, `type_system.py`).
3. Builds an executable graph (`builder.py`).
4. Runs it with the executor (`executor.py`), passing data between blocks.

### Example Workflows

| File | Purpose (as inferred from name) |
|---|---|
| `normal_multimodal.yaml` | Standard chat flow that accepts text and media and replies with an LLM |
| `dsr_thinking.yaml` | Chat flow with an explicit reasoning step before responding |
| `memory_store.yaml` | Stores conversation context into memory |
| `talk_break.yaml` | Handles conversation breaks or topic resets |
| `rules.yaml` | Maps incoming messages to workflows using dispatch rules |

### Blocks

Blocks are the units of work inside a workflow. They are registered in `workflow/blocks/` and the registry (`registry.py`). Built-in block groups include:

- **System blocks** (`system_blocks.py`): core operations such as calling an LLM or sending a reply.
- **Variable blocks** (`variable_blocks.py`): read and write workflow variables.
- **Chat and image blocks**: message composition and image handling.
- **Game blocks** (`gacha.py`, `dice.py`): game logic exposed as blocks.

Each block declares typed inputs and outputs through `input_output.py` and `param.py`. The executor checks these types when a workflow runs.

### Dispatch Rules

Rules determine which workflow handles an incoming message:

- **System rules** (`system_rules.py`): global conditions, such as maintenance mode.
- **Message rules** (`message_rules.py`): content-based matching, such as prefixes or keywords.
- **Sender rules** (`sender_rules.py`): matching by user or group, useful for permissions.

The dispatcher (`dispatcher.py`) evaluates rules in order and selects the first match. Rule definitions are read from `rules.yaml`.

### Composer and Decomposer Strategies

Strategies control how structured data is split into parts and recombined. They are useful for splitting long replies into several messages or handling multi-part media. Built-in strategies are in `builtin_composes.py`, and the registry is in `composer_strategy.py` and `decomposer_strategy.py`.

### Scopes

Scopes (`builtin_scopes.py`) limit where variables and state are visible during workflow execution, which prevents one conversation from leaking state into another.

---

## Plugins

### Built-in Plugins

| Plugin | Directory | Function |
|---|---|---|
| Basic | `plugins/basic.py` | Core commands |
| Chat | `plugins/chat.py` | Conversational responses |
| Chat memory | `plugins/chat_memory.py` | Memory-related chat features |
| Clear memory | `plugins/clear_memory.py` | Command to reset conversation memory |
| Help | `plugins/help.py` | Lists available commands; can render help as an image |
| Image | `plugins/image.py` | Image generation or handling |
| Dice | `plugins/dice.py` | Dice-rolling game |
| Gacha | `plugins/gacha.py` | Random draw system |
| Messages | `plugins/messages.py` | Message utilities |
| User profile | `plugins/user_profile.py` | Stores per-user information |
| States | `plugins/states.py` | Persistent state for plugins |
| Tool | `plugins/tool.py` | Exposes tools for LLM function calling |
| System workflows | `system_workflows.py` | Registers workflow-related system features |

### How Plugins Load

`plugin_loader.py` discovers plugins, reads their metadata from `plugin.py` and `models.py`, and registers them with the plugin registry. Plugins communicate through `plugin_event_bus.py`, so one plugin can react to events emitted by another without a direct dependency.

The `decorator.py` and `entry.py` modules provide the decorators and entry points that plugin authors use to expose commands and handlers.

### Writing a Plugin

A minimal plugin structure:

```
plugins/my_plugin/
├── __init__.py
├── plugin.py      # Plugin class and metadata
└── models.py      # Optional: data models
```

General steps:

1. Create a directory in the plugins location.
2. Define a plugin class in `plugin.py` and decorate it or register it according to the decorator pattern in `decorator.py`.
3. Register any commands or blocks it provides.
4. Subscribe to or publish events through the event bus when needed.
5. Restart the application or trigger a plugin reload, if the management API supports it.
6. Add tests in `tests/` following the existing patterns (for example, `test_plugin.py`).

The diagnostics module can help catch import errors, syntax issues, and undefined names before a plugin is loaded.

---

## Memory System

The memory system keeps conversation context so the LLM can respond with history.

- **Memory manager** (`memory_manager.py`): coordinates reads and writes.
- **Persistence backends**: file or Redis, as described in [Memory Storage](#memory-storage).
- **Codecs** (`codecs.py`): serialize messages and media for storage.
- **Updater** (`updater.py`): handles memory compaction or summarization when history grows.

Memory is typically scoped per user or per conversation. Users can clear their memory with the `clear_memory` plugin.

---

## Media Handling

Media is represented by typed objects in `kirara_ai/media/`:

- `media_object.py`: the base media object (image, audio, file, and so on).
- `metadata.py`: dimensions, size, duration, and other properties.
- `mime.py` and `media_type.py`: MIME type detection and classification.

The media layer lets adapters convert between platform-specific formats and the internal representation. It also lets LLM adapters send images or other media to multimodal models.

The included `sarasa-mono-sc-regular.ttf` font is used for rendering text into images, such as help pages or generated cards.

---

## Web Interface and API

The web server is built on the modules under `web/` (or `api/`) and includes:

- `server.py` and `application.py`: server startup and app construction.
- `middleware.py`: request processing.
- `utils.py`: shared helpers.
- Route modules for each area, each with `routes.py`, `models.py`, and often a `README.md`: for example, LLM, IM, plugins, workflows, and system settings.
- Authentication utilities (`auth_test_utils.py` is used in tests), which protect management endpoints.

Depending on configuration, the server exposes:

- A management API for configuring LLM providers, IM platforms, plugins, and workflows.
- Webhook endpoints for IM platforms that use callbacks (for example, WeCom).
- A diagnostics endpoint that runs the code checks described under [Features](#features).

Check the route files or the auto-generated API documentation (if enabled) for exact paths and request formats.

### MCP Server

The MCP (Model Context Protocol) server module lets MCP-compatible clients access Kirara AI's tools and capabilities. It is tested by `test_mcp_server.py`.

---

## Database Migrations

Schema changes are managed with Alembic.

- Configuration: `alembic.ini`
- Environment: `migrations/env.py`
- Template: `script.py.mako`
- Initial migration: `4a364dbb8dab_initial_migration.py`

Common commands:

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration after changing models
alembic revision --autogenerate -m "describe the change"

# Roll back one revision
alembic downgrade -1

# Show current revision
alembic current
```

Run migrations before the first start and after pulling updates that change models.

---

## Testing

The test suite uses pytest. Configuration is in `pytest.ini`, and shared fixtures are in `conftest.py`.

```bash
# Run all tests
pytest

# Run a specific module
pytest tests/test_workflow_basic.py

# Run with coverage (requires pytest-cov)
pytest --cov=kirara_ai --cov-report=term-missing
```

Test areas (from the file names):

- **Workflow:** builder, executor, blocks, registry, decorators, input/output, scopes, composer and decomposer strategies, memory manager, persistence.
- **Config:** `test_config_loader.py`.
- **LLM adapters:** OpenAI, Ollama, Gemini, Voyage, and LLM manager and tracer.
- **IM:** `test_im.py`.
- **Media:** `test_media.py`, `test_media_element.py`.
- **Plugins:** block, game, image, chat, memory, and user-facing command tests.
- **Auth and system:** `test_auth.py`, `test_system.py`, `test_system_blocks.py`.

Some adapter tests may need API keys or a running Ollama instance. Mock or skip them when those are unavailable.

---

## Development Guide

### Code Organization Principles

- Keep adapters thin. Platform and provider logic should translate formats, not make business decisions.
- Put behavior in blocks and plugins, not in the core engine.
- Use the event bus for cross-plugin communication instead of direct imports.
- Declare types for every block input and output so the executor can validate workflows.

### Adding an LLM Provider

1. Create `kirara_ai/llm/adapters/<provider>_adapter.py`.
2. Implement the adapter interface defined in `llm/adapter.py`.
3. Register it in the LLM registry (`llm_registry.py`).
4. Add configuration keys to `config.yaml.example`.
5. Add tests in `tests/test_<provider>_adapter.py`.

### Adding an IM Platform

1. Create `kirara_ai/im/<platform>/` with `adapter.py`, `message.py`, `sender.py`, and `setup.py`.
2. Register the platform in `im_registry.py`.
3. Add credentials to `config.yaml.example`.
4. If the platform uses webhooks, add routes in the web layer.

### Adding a Workflow Block

1. Create a block class in `workflow/blocks/`.
2. Declare inputs and outputs using the types in `type_system.py`.
3. Register the block in `registry.py` or with the block decorator.
4. Reference it in a workflow YAML file.
5. Add a test in `tests/test_block.py` or a new file.

### Code Style

Follow the conventions already in the repository. If the project includes linter or formatter settings in `pyproject.toml`, run them before committing.

---

## Troubleshooting

| Symptom | Possible cause | What to do |
|---|---|---|
| Application fails at startup with a config error | `config.yaml` is missing or malformed | Compare with `config.yaml.example` and validate the YAML |
| Database errors on first run | Migrations not applied | Run `alembic upgrade head` |
| LLM requests fail with authentication errors | Wrong or missing API key | Check the provider section in `config.yaml` |
| Messages from IM platform are not answered | Dispatch rules don't match, or the webhook is unreachable | Check `rules.yaml` and confirm the public URL is reachable |
| WeCom or Telegram webhook not receiving events | No public address | Use a reverse proxy or the frp tunnel manager |
| Redis memory errors | Redis not running or wrong connection string | Verify the Redis host, port, and password |
| Plugin does not load | Import error or missing metadata | Run the diagnostics checks on the plugin file |
| Help or card images show missing characters | Font not found | Confirm `sarasa-mono-sc-regular.ttf` is present and the path is correct |
| Tests fail on adapter modules | Missing API keys or local service | Mock the external call or skip with the appropriate marker |

Logs are produced by `logger.py`. Increase the log level in `config.yaml` when debugging.

---

## License

This project is distributed under the terms in the [LICENSE](LICENSE) file. Please read it before using, modifying, or redistributing the software.

The bundled font `sarasa-mono-sc-regular.ttf` is subject to its own license. Check the font's upstream project for its terms.

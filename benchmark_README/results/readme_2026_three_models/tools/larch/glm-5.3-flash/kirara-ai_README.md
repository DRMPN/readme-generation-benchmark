# README

<div align="center">

# 🌸 Kirara AI

**A modular AI chatbot framework — plug state-of-the-art LLMs into your favorite messaging platforms.**

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![API](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Tests](https://img.rules.io/badge/Tests-pytest-6DA55F?logo=pytest&logoColor=white)

[Features](#-features) · [Quick Start](#-quick-start) · [Architecture](#-architecture) · [LLM Providers](#-supported-llm-providers) · [IM Adapters](#-im-platform-adapters) · [Plugins](#-plugin-system) · [Development](#-development)

</div>

---

## 📖 Introduction

**Kirara AI** is a modular, plugin-driven chatbot framework that connects large language models to instant-messaging platforms. Instead of hard-coding bot behavior, Kirara is composed of three interchangeable layers:

- **IM adapters** connect the bot to QQ, Telegram, WeCom (WeChat Work), or any HTTP-based service;
- **A workflow engine** orchestrates how incoming events are processed, using graphs of typed, reusable blocks;
- **LLM adapters** talk to OpenAI, Claude, Gemini, DeepSeek, Ollama and a dozen other providers through one unified interface.

A built-in **web dashboard** lets you configure adapters, edit workflows, manage plugins (including an in-browser code editor with live syntax diagnostics), and inspect LLM/pipeline traces — without restarting the bot or hand-editing JSON.

## ✨ Features

### Core
- 🧩 **Plugin architecture** — self-contained Python packages that hot-load blocks, adapters, and event listeners, with a dedicated plugin event bus for inter-plugin communication.
- 🔄 **Workflow engine** — graph-based automation built from typed blocks (declared inputs/outputs, parameter schemas, async executor).
- 🚌 **Event bus + dispatch rules** — pluggable message/sender/system rules decide which events trigger which workflows.
- 💉 **Dependency injection** — a lightweight DI container wires services, adapters, and plugins together.

### AI
- 🤖 **14+ LLM providers** — OpenAI, Claude, Gemini, DeepSeek, Ollama, Moonshot, MiniMax, Mistral, OpenRouter, SiliconFlow, Volcengine, Alibaba Cloud, Tencent Cloud, and more, behind one request/response API.
- 🖼️ **Multimodal support** — send and receive images through both IM messages and LLM requests.
- 🛠️ **Tool calling** — first-class function/tool definitions in LLM requests.
- 🧠 **Short- and long-term memory** — scoped memory with composer/decomposer strategies, LLM-driven long-term memory distillation, and file or Redis persistence.
- 🔎 **Embeddings & reranking** — dedicated embedding/rerank interfaces (e.g. Voyage AI) for semantic memory retrieval.
- 🧪 **LLM tracing** — decorator-based tracing of every LLM and pipeline call, viewable in the dashboard.

### Platforms & operations
- 💬 **Multiple IM platforms** — QQ (official bot API), Telegram, WeCom, and a generic HTTP bridge.
- 🌉 **frpc tunnel manager** — the HTTP adapter ships an integrated reverse-proxy client so webhook callbacks work behind NAT/firewalls.
- 🌐 **Web dashboard & REST API** — adapter config, workflow editing, plugin management, diagnostics, and trace inspection.
- 🗄️ **Database migrations** — SQLAlchemy models with Alembic versioning.
- 🧯 **Diagnostics service** — pyflakes linting, Jedi syntax analysis, import checks, mandatory-function validation, and a Python LSP powering the in-browser plugin editor.
- 🎲 **Game blocks out of the box** — dice rolls, gacha draws, and user-state blocks for entertainment commands.

## 🏗️ Architecture

```
 ┌─────────────────┐        ┌──────────────┐        ┌──────────────────┐
 │   IM Adapter    │ events │  Event Bus   │ routed │   Dispatcher     │
 │ qq · telegram · │───────▶│  (pub/sub)   │───────▶│ (dispatch rules) │
 │ wecom · http    │        └──────────────┘        └────────┬─────────┘
 └────────▲────────┘                                         │ triggers
          │ replies                                          ▼
          │                                        ┌──────────────────┐
          └────────────────────────────────────────│ Workflow Engine  │
                                                   │ typed blocks +   │
                                                   │  async executor  │
                                                   └────────┬─────────┘
                                                            │ uses
                    ┌─────────────────┬─────────────────────┼─────────────────┐
                    ▼                 ▼                     ▼                 ▼
             ┌─────────────┐  ┌───────────────┐   ┌──────────────┐   ┌────────────┐
             │ LLM Manager │  │Memory Manager │   │Media Service │   │  Plugins   │
             │ + adapters  │  │scopes/persist │   │ MIME/storage │   │ event bus  │
             └─────────────┘  └───────────────┘   └──────────────┘   └────────────┘
```

| Subsystem | Key modules | Responsibility |
|---|---|---|
| Application core | `application.py`, `event_bus.py`, `listen.py`, `container.py` | Bootstrap, lifecycle, global event bus, dependency injection |
| Configuration | `config/` (`config_loader.py`, `global_config.py`, `manager.py`) | Central YAML configuration loading and management |
| IM | `im/` (`message.py`, `sender.py`, `im_registry.py`, `profile.py`) | Platform-agnostic messages, senders, user profiles, adapter registry |
| Dispatch | `dispatch/` (`dispatcher.py`, `dispatch_rules.py`, `rules/`) | Rule engine that routes events to pipelines/workflows |
| Workflow | `workflow/` (`base.py`, `builder.py`, `executor.py`, `blocks/`, `factories/`) | Graph-based automation with typed blocks |
| LLM | `llm/` (`manager.py`, `llm_registry.py`, `request.py`, `response.py`, `tool.py`) | Unified chat / embedding / rerank API over all providers |
| Trace | `trace/` (`llm_tracer.py`, `core.py`, `decorator.py`, `entry.py`) | Decorator-based tracing of LLM and pipeline calls |
| Memory | `memory/` (`memory_manager.py`, scopes, `persistence/`, `updater.py`) | Scoped short/long-term memory with pluggable backends |
| Media | `media/` (`media_object.py`, `metadata.py`, `mime.py`, `provider.py`, `service.py`) | Storage and retrieval of images, audio, and files |
| Plugins | `plugin/` (`plugin_loader.py`, `plugin.py`, `plugin_event_bus.py`) | Discovery, lifecycle, and inter-plugin events |
| Services | `services/` (`logger.py`, `server.py`, `internal.py`) | Logging and the internal streaming/trace server |
| Web | `web/` (`app.py`, `middleware.py`, `routes/`) | FastAPI backend for the dashboard |
| Migrations | `migrations/`, `alembic.ini` | Database schema versioning |

## 🚀 Quick Start

### Prerequisites
- Python **3.9+**
- (Optional) A **Redis** instance for memory persistence at scale
- (Optional) **Docker** for containerized deployment

### Run from source

```bash
git clone https://github.com/kirara-ai/kirara-ai.git
cd kirara-ai

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install the package
pip install -e .

# Initialize the database schema
alembic upgrade head

# Start the bot
python -m kirara
```

On Linux/macOS you can also use the bundled launcher, which handles environment setup and startup:

```bash
./start.sh
```

### Run with Docker

```bash
docker build -t kirara-ai .
docker run -d --name kirara \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  kirara-ai
```

Mount a volume for the data directory so the database, media files, and plugins survive container restarts.

### First run

1. Watch the console for startup logs and initial administrator setup information.
2. Open the dashboard at **http://127.0.0.1:8080/web** and log in.
3. Add an **LLM adapter** (provider + API key) and an **IM adapter** (platform credentials).
4. Adjust workflows and dispatch rules to taste — changes apply without code changes.

## ⚙️ Configuration

Copy the bundled template and edit it, or configure everything from the dashboard:

```bash
cp config.yaml.example config.yaml
```

Typical configuration areas:

| Area | Contents |
|---|---|
| Web server | Host/port of the dashboard and REST API |
| Database | SQLAlchemy connection (SQLite by default) |
| Logging | Verbosity and output targets |
| Memory | Scope defaults, persistence backend (file / Redis), long-term memory behavior |
| Adapters | Provider credentials and platform credentials (managed per adapter) |

Refer to `config.yaml.example` for the fully documented reference of all options.

## 🤖 Supported LLM Providers

| Provider | Adapter | Capabilities | Notes |
|---|---|---|---|
| OpenAI & compatible | `openai_adapter` | Chat · Vision · Tools · Embeddings | Works with any OpenAI-compatible gateway (vLLM, one-api, …) |
| Anthropic Claude | `claude_adapter` | Chat · Vision · Tools | |
| Google Gemini | `gemini_adapter` | Chat · Vision · Tools | |
| DeepSeek | `deepseek_adapter` | Chat · Tools | Pair with the `dsr_thinking` workflow for reasoning-model output |
| Moonshot AI (Kimi) | `moonshot_adapter` | Chat | |
| MiniMax | `minimax_adapter` | Chat | |
| Mistral | `mistral_adapter` | Chat · Tools | |
| OpenRouter | `openrouter_adapter` | Chat | One key, hundreds of models |
| SiliconFlow | `siliconflow_adapter` | Chat | |
| Volcengine (Doubao) | `volcengine_adapter` | Chat | |
| Alibaba Cloud (Qwen) | `alibabacloud_adapter` | Chat | |
| Tencent Cloud (Hunyuan) | `tencentcloud_adapter` | Chat | |
| Ollama | `ollama_adapter` | Chat (local) | Run models fully offline |
| Voyage AI | `voyage_adapter` | Embeddings · Rerank | Powers semantic memory retrieval |

All chat adapters share common capabilities: streaming responses, function/tool calling, multimodal (vision) input, and full integration with the tracing system. Custom providers can be added by subclassing the adapter base class and registering with the LLM registry.

## 💬 IM Platform Adapters

| Adapter | Platform | Highlights |
|---|---|---|
| QQ Bot | QQ (official open platform) | Official bot API integration |
| Telegram | Telegram | Bot API messaging |
| WeCom | 企业微信 / WeChat Work | Application messaging |
| HTTP Legacy | Any platform | REST/webhook bridge with an API test console; includes a built-in **frpc manager** so callback webhooks can reach instances running behind NAT or firewalls |

Adapters implement the message/sender interfaces and register themselves with `im_registry`; writing a new one requires no changes to core code.

## 🔄 Workflow Engine

Workflows are directed graphs of **blocks**. Every block declares typed inputs/outputs (`input_output.py`, `type_system.py`) and a parameter schema (`schema.py`, `param.py`); the builder validates connections against the type system, and the async `executor.py` runs the graph for each triggering event, propagating errors as structured block exceptions.

### Built-in block categories

| Factory / category | Files | Typical blocks |
|---|---|---|
| System | `system_factory.py` → `system_blocks.py`, `variable_blocks.py` | LLM chat request, message sending, variable get/set, flow control |
| Memory | `chat_memory.py`, `clear_memory.py`, `basic.py`, `help.py` | Append/read/clear conversation memory |
| Game | `game_factory.py` → `gacha.py`, `dice.py`, `messages.py` | Dice rolls, gacha simulations, message utilities |
| User state | `states.py`, `user_profile.py` | Per-user persistent state and profile accessors |
| Media / chat | `image.py`, `chat.py`, `basic.py` | Image handling and rendering (uses the bundled Sarasa Mono SC font for CJK text) |

### Bundled workflow templates

Kirara ships ready-made YAML workflow templates that can be used as-is or cloned and edited in the dashboard:

| Template | Purpose |
|---|---|
| `rules.yaml` | Core message-handling workflow implementing the default reply rules |
| `normal_multimodal.yaml` | Standard chat workflow with multimodal (image) input support |
| `dsr_thinking.yaml` | Tuned for reasoning models (e.g. DeepSeek-R1 style "thinking" output) |
| `memory_store.yaml` | Persists conversation history into long-term memory |
| `talk_break.yaml` | Handles reply segmentation / conversation interruption |

Built-in system workflows are registered at startup by `system_workflows.py`.

## 🎯 Dispatch Rules

Incoming events flow through the event bus into the dispatcher, which evaluates registered rule classes to decide whether — and which — workflow should handle a message:

- **Message rules** (`message_rules.py`) — match on message content, type, or elements (e.g. commands, keywords, mentions).
- **Sender rules** (`sender_rules.py`) — match on sender identity, role, or permissions.
- **System rules** (`system_rules.py`) — global conditions such as administrative controls.

Rules are composable and priority-ordered, and can be managed from the web dashboard.

## 🧠 Memory System

- **Scopes** (`builtin_scopes.py`) — memory is partitioned per scope (conversation, user, global, …).
- **Composer / decomposer strategies** (`composer_strategy.py`, `decomposer_strategy.py`, `builtin_composes.py`, `xml_helper.py`) — control how stored memory is rendered into LLM prompts (including structured XML formats) and parsed back.
- **Persistence** (`persistence/`) — local **file** backend or **Redis** backend, with pluggable serialization codecs.
- **Long-term updater** (`updater.py`) — periodically distills raw chat history into durable long-term memories using the LLM (see the `memory_store.yaml` workflow).

## 🖼️ Media Subsystem

- `media_object.py` / `metadata.py` — first-class media objects carrying metadata.
- `mime.py` / `media_type.py` — MIME detection and media-type classification.
- `provider.py` / `service.py` / `registry.py` — pluggable storage providers for saving and resolving media.

The media service is used by both IM messages (image/audio/file elements) and multimodal LLM requests.

## 🧩 Plugin System

- Plugins are self-contained Python packages discovered and loaded by `plugin_loader.py`, with declarative metadata models and lifecycle management.
- `plugin_event_bus.py` provides a dedicated event bus for inter-plugin communication.
- The dashboard supports installing, enabling, disabling, and inspecting plugins.
- **In-browser code editor with diagnostics**: editing plugin code from the web UI is backed by a diagnostics service — pyflakes linting, Jedi syntax analysis, import checking, mandatory-function validation, and an integrated Python LSP for completions.
- Ships an experimental **MCP (Model Context Protocol) server** component for tool-based integrations with MCP-compatible clients.

## 🌐 Web Dashboard & REST API

The dashboard backend is a FastAPI application (`web/app.py`) with authentication middleware and modular routers. Each route group ships its own `README.md` documenting its endpoints:

| Route group | Purpose |
|---|---|
| `auth` | Login, token-based authentication, account management |
| `config` | Read and update global configuration |
| `plugins` | Plugin lifecycle and management |
| `workflows` | Create, edit, and validate workflows and dispatch rules |
| LLM adapters | Manage providers, models, and API keys |
| IM adapters | Manage platform connections |
| `diagnostics` | Code-editor backend (pyflakes / Jedi / import checks / LSP) |
| Trace | Browse pipeline and LLM execution traces |
| MCP | MCP server endpoints |

## 🗄️ Persistence

- Database access uses **SQLAlchemy** with schema versioning via **Alembic** (`alembic.ini`, initial migration `4a364dbb8dab_initial_migration.py`).
- SQLite works out of the box; any SQLAlchemy-supported database can be configured.
- Memory persistence can use the local filesystem or **Redis**.

## 🗂️ Project Structure

*Abridged — see the repository for the full tree.*

```
kirara-ai/
├── kirara/
│   ├── __main__.py                 # python -m kirara entry point
│   ├── ai/
│   │   ├── application.py          # application bootstrap & lifecycle
│   │   ├── event_bus.py            # global event bus
│   │   ├── listen.py               # event listener helpers
│   │   ├── container.py            # dependency-injection container
│   │   ├── config/                 # configuration loading & management
│   │   ├── dispatch/               # dispatcher + message/sender/system rules
│   │   ├── im/                     # IM abstractions (message, sender, profile)
│   │   ├── llm/                    # LLM manager, requests, tools, embeddings
│   │   │   └── adapters/           # OpenAI, Claude, Gemini, DeepSeek, Ollama, …
│   │   ├── media/                  # media objects, MIME handling, providers
│   │   ├── memory/                 # scopes, composer/decomposer, updater
│   │   │   └── persistence/        # file & Redis backends, codecs
│   │   ├── plugin/                 # plugin loader & plugin event bus
│   │   ├── services/               # logging, internal trace server
│   │   ├── trace/                  # LLM tracing core & decorators
│   │   └── workflow/               # engine: base, registry, builder, executor
│   │       ├── blocks/             # system / memory / game / user-state blocks
│   │       └── factories/          # block factories (system, game, default)
│   ├── migrations/                 # Alembic migrations
│   └── web/                        # FastAPI dashboard backend
│       ├── app.py                  # ASGI app, middleware, router mounting
│       ├── auth/ · config/ · plugins/ · workflows/
│       ├── adapters/ · diagnostics/ · trace/ · …
├── tests/                          # pytest suite, organized per subsystem
├── assets/
│   ├── workflows/                  # rules / normal_multimodal / dsr_thinking / …
│   └── sarasa-mono-sc-regular.ttf  # bundled CJK font for image rendering
├── config.yaml.example
├── alembic.ini · pytest.ini · pyproject.toml · MANIFEST.in
├── Dockerfile · start.sh
└── LICENSE
```

## 🛠️ Development

```bash
git clone https://github.com/kirara-ai/kirara-ai.git
cd kirara-ai
python -m venv venv && source venv/bin/activate
pip install -e .

# Run the test suite (configuration in pytest.ini)
pytest
```

The test suite mirrors the subsystems of the project:

- **Workflow engine** — `test_workflow_builder.py`, `test_executor.py`, `test_block.py`, `test_workflow_basic.py`, `test_input_output.py`, …
- **Blocks & factories** — `test_system_blocks.py`, `test_game_blocks.py`, `test_block_registry.py`, `test_workflow_factories.py`
- **Memory** — `test_memory_manager.py`, `test_composer_strategy.py`, `test_decomposer_strategy.py`, `test_scope.py`, `test_persistence.py`
- **LLM** — `test_llm_tracer.py`, `test_openai_adapter.py`, `test_ollama_adapter.py`, `test_gemini_adapter.py`, `test_voyage_adapter.py`
- **Web API** — `test_auth.py`, `test_plugin.py`, `test_mcp_server.py`, `test_im.py`, `test_media.py`
- **Game & utility blocks** — `test_gacha.py`, `test_dice.py`, `test_states.py`, `test_help.py`, …

Common development tasks:

- **Add an LLM provider** — subclass the LLM adapter base, implement the request/response mapping, and register it in the LLM registry (see any existing adapter as a reference).
- **Add an IM platform** — implement the message/sender interfaces and register with `im_registry`.
- **Change the database schema** — generate a revision with `alembic revision --autogenerate -m "…"`, then review and apply it.

## ❓ FAQ

**Do I need an OpenAI API key?**
No. Any of the supported providers works, including fully local setups via the Ollama adapter.

**Can multiple LLM providers coexist?**
Yes. Register as many adapters as you like and choose the model per workflow block.

**Where is my data stored?**
In the application data directory (database, media files, plugin data). Memory persistence can be moved to Redis if desired.

**How do I receive webhooks behind a firewall?**
The HTTP legacy adapter includes an frpc (reverse-proxy) manager for tunneling callback URLs.

## 🤝 Contributing

Contributions are welcome! Please:

1. Open an issue to discuss significant changes first.
2. Add or update tests for the affected subsystem.
3. Keep adapters and plugins self-contained.
4. Update the per-route `README.md` files when changing the REST API.

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgements

- [Sarasa Mono SC](https://github.com/be5invis/Sarasa-Gothic) — the bundled CJK monospace font used for image text rendering.
- All the LLM and platform providers that make multi-backend AI chat possible.

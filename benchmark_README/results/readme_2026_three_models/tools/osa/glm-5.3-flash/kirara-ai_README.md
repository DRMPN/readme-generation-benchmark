# kirara-ai-uavfddjj

---

[![PyPi](https://badge.fury.io/py/kirara-ai.svg)](https://badge.fury.io/py/kirara-ai)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![aiohttp](https://img.shields.io/badge/AIOHTTP-2C5BB4.svg?logo=AIOHTTP&logoColor=white)
![pre-commit](https://img.shields.io/badge/precommit-FAB040.svg?logo=pre-commit&logoColor=black)
![pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?logo=Pytest&logoColor=white)
![sqlalchemy](https://img.shields.io/badge/SQLAlchemy-D71F00.svg?logo=SQLAlchemy&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Kirara AI is a self-hosted Python framework for building AI agents, primarily a chatbot server that connects large language model backends to instant-messaging platforms such as Telegram, QQ, and WeCom. It is aimed at developers and bot operators who want to deploy, configure, and extend their own LLM-powered bots, and its plugin system and built-in web interface also make it approachable for self-hosters. At its core is a workflow engine that routes incoming messages through configurable processing pipelines, alongside supporting subsystems for memory, media, tracing, and MCP integration. The server exposes a web API and WebUI for administration, and new users should consult the Getting Started section for setup and run instructions.

---

## Core Features

- **Multi-platform messaging integration**: Connect LLM-powered bots to instant-messaging platforms (Telegram, QQ, WeCom, and more) through pluggable adapters, so one bot deployment can serve multiple chat services.
- **Workflow engine**: Build and dispatch agent behaviors using configurable workflows with blocks and dispatch rules, letting developers tailor how messages are processed without hardcoding logic.
- **Pluggable LLM backends**: Configure multiple LLM providers (e.g., OpenAI, DeepSeek) via adapters and switch models per deployment, enabling flexible backend choices from a single configuration file.
- **Built-in WebUI and web API**: Manage the running server—IM connections, LLM backends, workflows, plugins, and MCP servers—through a browser-based dashboard backed by a REST API.
- **Extensible plugin and memory systems**: Extend functionality with dynamically loaded plugins and give bots persistent, scoped memory (per-member, per-group, or global) backed by file or Redis storage.

---

## Installation

**Prerequisites:** requires Python >=3.10

Install kirara-ai using one of the following methods:

**Using PyPi:**

```sh
pip install kirara-ai
```

---

## Getting Started

### Prerequisites
*   **Python:** Python 3.10 or newer.
*   **Dependencies:** Install required libraries (refer to installation instructions).
*   **Configuration:** Ensure your API keys and desired platform settings are configured.

### Quickstart
1.  **Configure Settings:** Copy the sample configuration file to define your desired behavior and API credentials.
```bash
    cp config.yaml.example ./data/config.yaml
```
    *Note: Edit `./data/config.yaml` to configure LLM API backends (e.g., OpenAI, DeepSeek) and messaging platforms.*

2.  **Prepare WebUI:** The built-in WebUI frontend must be present in the `web` directory.
    *   Acquire the required WebUI frontend resources.
    *   Extract the files into the `web` folder, ensuring `web/index.html` exists.

3.  **Run the Server:** Start the AI Chatbot Server using the primary script.
```bash
    kirara_ai
    # Alternatively, use the module entry point:
    # python -m kirara_ai
```

---

## Architecture

Kirara AI is a plugin-based monolith wired together by a lightweight IoC dependency container. On startup, `kirara_ai/entry.py` loads configuration, initializes the database (SQLAlchemy + Alembic), and registers the core services into a single `DependencyContainer` before discovering and loading plugins.

Major subsystems:

- **IoC container** (`kirara_ai/ioc`): the central `DependencyContainer` that all managers and services are registered into and resolved from.
- **Workflow engine** (`kirara_ai/workflow/core`): the core execution layer, composed of blocks (registered via `BlockRegistry`), workflows (`WorkflowRegistry`), dispatch rules (`DispatchRuleRegistry` / `WorkflowDispatcher`), and an execution module. System blocks under `workflow/implementations/blocks` provide LLM, memory, IM, MCP, media, and variable operations.
- **IM layer** (`kirara_ai/im`): `IMManager` and `IMRegistry` manage connections to messaging platforms. Actual platform adapters (Telegram, QQ Bot, WeCom, legacy HTTP) are bundled plugins under `kirara_ai/plugins`.
- **LLM layer** (`kirara_ai/llm`): `LLMManager` and `LLMBackendRegistry` route requests to configured API backends (e.g., OpenAI, DeepSeek presets in `config.yaml.example`); adapters are provided by the `llm_preset_adapters` plugin.
- **Memory system** (`kirara_ai/memory`): scoping (`member`, `group`, `global`), composers/decomposers, and pluggable persistence (file or Redis).
- **Media, tracing, and MCP** (`kirara_ai/media`, `kirara_ai/tracing`, `kirara_ai/mcp_module`): media storage with carrier registry, LLM tracing, and MCP server management.
- **Web layer** (`kirara_ai/web`): a FastAPI app serving the downloaded WebUI frontend and a Quart app exposing REST API blueprints under `/api/*` (im, llm, workflow, mcp, plugin, system, etc.), served by Hypercorn.
- **Plugin system** (`kirara_ai/plugin_manager`): `PluginLoader` discovers plugins, each with its own `setup.py`; plugins extend IM adapters, LLM backends, and other capabilities.

Control flow: incoming IM messages are routed by the workflow dispatcher's dispatch rules into workflows, which execute registered blocks (LLM calls, memory reads/writes, media handling, etc.) and send responses back through the IM adapters. The EventBus provides internal event distribution, and the tracing system records LLM activity. Persistence is handled by `DatabaseManager` with Alembic migrations.

---

## Testing

The project uses [pytest](pytest.ini) as its test framework; `pytest` is declared as a dependency in `pyproject.toml`, and test configuration lives in `pytest.ini`.

Test layout:

- `tests/` — top-level test modules such as `test_config_loader.py`, `test_workflow_builder.py`, `test_workflow_factories.py`, `test_system_blocks.py`, `test_media.py`, `test_media_element.py`, `test_mcp_server.py`, and `test_game_blocks.py`
- `tests/system_blocks/` — tests for system blocks grouped by area (`im`, `llm`, `memory`, `game`, `system`)
- `tests/web/` — tests for the web API blueprints (`im`, `llm`, `media`, `plugin`, `system`, `workflow`) and auth
- `tests/memory/`, `tests/tracing/`, `tests/workflow_executor/`, `tests/llm_adapters/` — memory, tracing, workflow execution, and LLM adapter tests (including a mock app under `tests/llm_adapters/mock_app/`)
- `tests/resources/` — shared test resources

Some bundled plugins ship their own test suites, e.g. `kirara_ai/plugins/im_http_legacy_adapter/tests/` and `kirara_ai/plugins/llm_preset_adapters/tests/`.

To verify your changes, run the test suite with `pytest` from the repository root (configuration is picked up from `pytest.ini`). When touching a specific subsystem, you can scope the run to the relevant `tests/` subdirectory. Note that the contents of `.github/workflows` were not verified here, so CI-invoked test commands cannot be confirmed; local `pytest` runs are the reliable way to check your work.

---

## Contributing

Please refer to the project repository for detailed guidelines on how to contribute code, report bugs, or suggest features.

---

## License

This project is protected under the AGPL-3.0 license. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    kirara-ai (2026). kirara-ai repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{kirara-ai,

        author = {{kirara-ai}},

        title = {kirara-ai repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}
    }

---
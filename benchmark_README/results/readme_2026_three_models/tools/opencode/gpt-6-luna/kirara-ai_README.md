# Kirara AI

Kirara AI is a Python framework for building AI agents. It runs configurable workflows, connects them to instant-messaging (IM) adapters and language-model backends, and provides a web interface and API for managing the application.

## Features

- **Workflow engine:** compose and execute workflows from registered blocks. Bundled blocks cover chat and other LLM calls, IM messages and user information, memory, MCP tools, variables, system functions, and game functions. Preset workflows include chat, help, memory clearing, dice, and gacha workflows.
- **Model backends:** configure multiple backends. The bundled preset adapters register OpenAI, DeepSeek, Gemini, Ollama, Claude, SiliconFlow, Tencent Cloud, Alibaba Cloud, Moonshot, OpenRouter, MiniMax, Volcengine, and Mistral.
- **IM integrations:** bundled adapters include Telegram, QQ Bot, WeCom, and a legacy HTTP API adapter.
- **Web management:** serves a web UI at `/` and a backend API under `/backend-api`, with routes for workflows, blocks, IM and LLM configuration, plugins, MCP servers, media, tracing, and system status. The server attempts to install the web UI if it is missing.
- **Memory and media:** includes scoped memory with file or Redis persistence, plus media management and metadata support.
- **Extensibility:** plugins can register adapters and other application components.

## Requirements

- Python 3.10 or newer
- Dependencies listed in `pyproject.toml` (installed with the package)

## Quick start

Install from a checkout:

```bash
python -m pip install .
```

Create the runtime configuration directory and copy the example configuration:

```bash
mkdir -p data
cp config.yaml.example data/config.yaml
```

Edit `data/config.yaml` before starting the service. In particular, configure the LLM backend and model you want to use, any IM adapters, and a non-empty `web.secret_key`. The example file shows the supported configuration sections, including `ims`, `llms`, `mcp`, `memory`, `web`, `plugins`, and `defaults`. Keep API tokens and other credentials private.

Start the server from the project directory:

```bash
kirara_ai
```

Alternatively, run it as a Python module:

```bash
python -m kirara_ai
```

The default web bind address is `127.0.0.1:8080`. Override it for a run with `--host` and `--port`, for example:

```bash
kirara_ai --host 0.0.0.0 --port 8080
```

Open `http://127.0.0.1:8080/` for the web UI. The backend API is mounted under `/backend-api` (for example, `/backend-api/api/system/status`).

## Configuration

At startup, the application loads `./data/config.yaml` relative to the current working directory. If the file is missing, it starts with default configuration and logs a reminder to create the file. `config.yaml.example` is the repository's example; copy it to `data/config.yaml` and adjust it for your setup.

Common settings include:

| Section | Purpose |
| --- | --- |
| `ims` | Enabled IM adapter instances and their adapter-specific settings |
| `llms.api_backends` | LLM adapter configuration and available models |
| `defaults.llm_model` | Default model name |
| `mcp.servers` | MCP server connection settings |
| `memory` | Persistence type (`file` or `redis`), storage settings, limits, and default scope |
| `web` | Bind host, port, secret key, and password file |
| `plugins.enable` | External plugins to enable |

Adapter configuration fields depend on the selected adapter. The web API exposes adapter types and configuration schemas, and the configuration models are defined in `kirara_ai/config/global_config.py`.

## Docker

The repository includes a Dockerfile. Build and run the image from the repository root:

```bash
docker build -t kirara-ai .
docker run --name kirara-ai -p 8080:8080 -v kirara-ai-data:/app/data kirara-ai
```

The container entrypoint initializes `/app/data` with the image's bundled data when that directory is empty, creates a default web bind configuration if needed, and starts the application. The named volume keeps runtime data outside the container. The image exposes port `8080`.

## Development

Install the project and run the test suite with pytest:

```bash
python -m pip install .
python -m pytest
```

Tests are under `tests/`, including coverage for workflows, adapters, web APIs, memory, media, tracing, and system blocks.

## Project layout

- `kirara_ai/` — application package, including configuration, workflow execution, adapters, plugins, web APIs, memory, media, and tracing
- `data/workflows/` and `data/dispatch_rules/` — bundled workflow definitions and message dispatch rules
- `tests/` — automated tests
- `config.yaml.example` — sample runtime configuration
- `Dockerfile` and `docker/` — container build and startup files

## Documentation and links

- [Kirara AI documentation](https://kirara-docs.app.lss233.com)
- [Project repository](https://github.com/lss233/chatgpt-mirai-qq-bot)
- [Issue tracker](https://github.com/lss233/chatgpt-mirai-qq-bot/issues)

## License

This project is licensed under the GNU Affero General Public License, version 3 only (AGPL-3.0-only). See [LICENSE](LICENSE).

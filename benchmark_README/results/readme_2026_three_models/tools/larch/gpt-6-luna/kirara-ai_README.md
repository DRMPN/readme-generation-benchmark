# Kirara AI

Kirara AI is a Python framework for building conversational AI applications that connect language models, chat platforms, workflows, tools, and persistent memory. It includes adapters for a range of LLM providers and messaging services, along with a plugin system and a web/API layer.

This README describes the project’s main components and how to get started. For exact configuration keys and provider-specific options, use the examples and documentation included in the repository.

## Features

- **Multiple LLM providers:** adapters for services including OpenAI, Anthropic Claude, Google Gemini, DeepSeek, Mistral, Moonshot, MiniMax, Ollama, OpenRouter, SiliconFlow, Tencent Cloud, Alibaba Cloud, Volcengine, and Voyage.
- **Messaging integrations:** adapters for platforms including QQ Bot, Telegram, WeCom, and a legacy HTTP integration.
- **Composable workflows:** workflow builders, blocks, factories, and system workflows for organizing application behavior.
- **Tools and plugins:** extensible tool and plugin registries, event handling, and an MCP server component.
- **Memory and persistence:** chat memory management with file- and Redis-backed persistence options.
- **Multimodal support:** media abstractions and message handling for content such as images.
- **Web and API components:** routes, middleware, services, and application setup for exposing functionality over HTTP.
- **Supporting utilities:** configuration loading, logging, tracing, model management, embeddings, reranking, and a Python-language-server integration.

## Repository layout

The repository is organized into several areas:

| Area | Purpose |
| --- | --- |
| Core and workflow modules | Application core, workflow execution, workflow blocks, factories, and system workflows |
| LLM integrations | Provider adapters, model and request types, response handling, embeddings, and reranking |
| Messaging integrations | Message and sender abstractions, platform registries, and platform adapters |
| Memory | Memory management and file or Redis persistence |
| Plugins and tools | Plugin loading, event bus, tool registry, and MCP-related components |
| Web/API | Application setup, routes, services, middleware, and server components |
| Tests | Unit and integration tests for workflows, adapters, memory, plugins, messaging, and other modules |
| Examples and configuration | Example configuration, workflow YAML files, environment helpers, and deployment files |

## Requirements

Use the Python version and dependency requirements declared in `pyproject.toml`. Some integrations may also require provider-specific credentials, external services, or optional dependencies.

## Installation

Clone the repository, then install it in editable mode:

```bash
git clone <repository-url>
cd <repository-directory>
python -m pip install --upgrade pip
python -m pip install -e .
```

If a provider or messaging adapter has its own installation instructions or dependencies, consult the adapter’s files and documentation before enabling it.

## Configuration

Start with the example configuration:

```bash
cp config.yaml.example config.yaml
```

Edit `config.yaml` and supply the settings required by the integrations you intend to use. For credentials, prefer environment variables or a secrets manager over committing keys to source control. The repository includes `env.py` and `.env`-related support; check the configuration loader and example files for the expected variable names and precedence.

The repository also contains example workflow and rules files, including:

- `normal_multimodal.yaml`
- `dsr_thinking.yaml`
- `memory_store.yaml`
- `talk_break.yaml`
- `rules.yaml`

Review these files before using or modifying them. Their available options depend on the workflow and component implementations in the installed version.

> **Important:** Do not publish a populated configuration file, API key, bot token, or other secret.

## Running the application

The project contains a Python module entry point. From the repository root, try:

```bash
python -m kirara_ai
```

The exact startup behavior depends on the configured application and enabled adapters. If the project’s packaging configuration defines a console command, it will also be listed in `pyproject.toml`.

A `start.sh` script and a `Dockerfile` are included for deployment workflows. Review them before running them in production, especially to confirm which configuration files, ports, and environment variables they expect.

## Using providers and messaging adapters

Kirara AI separates provider and platform integrations behind adapter interfaces and registries. In general:

1. Install the project and any adapter-specific dependencies.
2. Configure the provider or platform credentials.
3. Enable or register the adapter using the project configuration.
4. Start the application and check its logs for connection or authentication errors.

Available provider integrations include OpenAI-compatible services as well as provider-specific adapters. Messaging integrations include QQ Bot, Telegram, and WeCom. The adapters may have different setup requirements; refer to their `setup.py`, implementation, and related tests for details.

## Workflows, tools, and plugins

Workflows are assembled from reusable blocks and executed through the workflow system. The repository includes system workflow and factory modules, block registries, and workflow tests. YAML files in the repository provide examples of workflow-related configuration.

Tools and plugins extend application behavior. The codebase includes registries, a plugin loader, an event bus, and tool-related interfaces. For an extension:

1. Look for the relevant base class or interface in the corresponding module.
2. Check its registry and builder for how components are discovered or constructed.
3. Review existing implementations and tests for expected behavior.
4. Add tests for the extension and its integration with the application.

The exact plugin and workflow APIs are defined by the source code and may change between versions.

## Memory and persistence

Chat memory is managed separately from persistence. The repository includes memory-management code and file- and Redis-backed persistence implementations. Select and configure the appropriate backend for your deployment, and consider retention, privacy, and access controls when storing conversation data.

## Web and API

The repository includes an application layer with routes, services, middleware, and server components. It also includes route modules and tests for web-related functionality. Consult those modules for available endpoints, authentication behavior, and configuration before exposing the service to a network.

## Development

Install the project in editable mode and run the test suite:

```bash
python -m pip install -e .
python -m pytest
```

The repository also includes `pytest.ini` and tests covering areas such as workflow execution, model adapters, memory persistence, plugins, media, messaging, and configuration. To run a specific test module:

```bash
python -m pytest path/to/test_module.py
```

For linting and static checks, inspect the project’s development dependencies and scripts in `pyproject.toml`. Diagnostic modules are also present in the repository.

## Deployment notes

- Store API keys and bot tokens outside version control.
- Use a production-appropriate persistence backend and protect stored user data.
- Restrict access to web/API endpoints and configure authentication as needed.
- Review the Dockerfile and startup scripts for ports, volumes, and runtime assumptions.
- Check provider and platform terms, rate limits, and data-handling policies.

## License

See the `LICENSE` file for the applicable license and usage terms.

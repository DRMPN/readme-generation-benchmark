# Devika

Devika is an AI software-engineering assistant with a web interface and a Python backend. It uses a set of task-specific agents to plan a coding task, research it on the web, generate files, and continue working on an existing project through follow-up requests. Projects, messages, and agent state are stored locally.

## What it includes

- A SvelteKit web UI for project chats, generated files, agent activity, settings, and logs.
- A Flask and Flask-SocketIO backend that coordinates planning, research, code generation, and follow-up actions.
- Configurable language-model clients for Anthropic Claude, OpenAI, Google Gemini, Mistral, Groq, Ollama, and LM Studio. Available models depend on the provider configuration; Ollama models are discovered from the configured server.
- Web research using Bing, Google Custom Search, or DuckDuckGo, followed by Playwright-based page reading.
- Project and agent-state persistence in SQLite, with project files stored under the configured projects directory.
- Follow-up workflows for answering questions, running project code, implementing features, addressing bugs, creating reports, and deploying through Netlify.

These integrations require the relevant service to be configured. Generated code and agent output should be reviewed before use.

## Requirements

- Python 3 and pip
- [Bun](https://bun.sh/) for the web UI
- Playwright's Chromium browser and its system dependencies
- An LLM provider: either a configured hosted provider or a running local Ollama/LM Studio service
- API credentials for whichever hosted LLM and search/deployment services you use

The repository does not pin a Python version. Its Docker backend is based on Debian 12.

## Setup

Run these commands from the repository root. A virtual environment is recommended:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m playwright install-deps chromium

cd ui
bun install
```

`playwright install-deps` may require administrator privileges to install operating-system packages. Alternatively, `setup.sh` installs the Python requirements, Playwright and its system dependencies, and UI packages; it uses `pip3` directly rather than creating a virtual environment.

## Configuration

On first backend startup, Devika creates `config.toml` in the repository root by copying `sample.config.toml`. The generated file is ignored by Git. You can edit it directly or configure values in the UI's **Settings** page.

The sample config covers:

- **API keys:** Bing, Google Custom Search, Claude, OpenAI, Gemini, Mistral, Groq, and Netlify.
- **API endpoints:** Bing, Google, Ollama, LM Studio, and OpenAI-compatible API endpoint.
- **Storage paths:** SQLite database, projects, screenshots, PDFs, logs, and cloned repositories.
- **Logging and inference timeout** settings.

Replace placeholder credentials with real values for any hosted services you select. Bing and Google search require their corresponding credentials; DuckDuckGo does not require a key. For local inference, start Ollama or LM Studio and set the endpoint in `config.toml` (the sample defaults to Ollama at `http://127.0.0.1:11434` and LM Studio at `http://localhost:1234/v1`). Ollama models must be available on that Ollama server to appear in the model list.

More details: [Ollama setup](docs/Installation/ollama.md) and [search-engine setup](docs/Installation/search_engine.md).

## Run locally

Start the backend from the repository root in one terminal:

```sh
source .venv/bin/activate
python devika.py
```

The backend listens on port `1337`. Start the UI in a second terminal:

```sh
cd ui
bun run dev
```

Open [http://localhost:3000](http://localhost:3000). The UI connects to the backend at `http://127.0.0.1:1337` when accessed through localhost. In the UI, create or select a project, choose an available model and search engine, and send a task.

For non-localhost UI hosting, the frontend derives its default backend address from the page hostname and uses port `1337`; the backend CORS configuration in `devika.py` currently allows only localhost origins on port `3000`. Adjust that configuration if your frontend is served from another origin.

## Docker

The repository includes `docker-compose.yaml` and backend/frontend Dockerfiles. The backend Dockerfile copies `config.toml` during image build, while the generated config is not committed. Before building with Compose, create it from the sample:

```sh
cp sample.config.toml config.toml
docker compose up --build
```

Review the Compose and Dockerfile settings before relying on container persistence or exposing the services; their port mappings and storage configuration are defined in those files.

## Repository layout

```text
devika.py                 Flask/Socket.IO backend entry point
src/agents/               Planning, research, coding, and follow-up agents
src/llm/                  LLM provider clients and model selection
src/browser/              Search, browser, and web interaction code
src/project.py            Project and conversation persistence
src/state.py              Agent-state persistence
ui/                       SvelteKit frontend
sample.config.toml         Configuration template
docs/Installation/        Provider and search setup guides
docs/architecture/        Architecture documentation
```

## Further documentation

- [Detailed architecture](ARCHITECTURE.md)
- [Architecture overview](docs/architecture/README.md)
- [Under the hood](docs/architecture/UNDER_THE_HOOD.md)
- [Benchmarks](benchmarks/BENCHMARKS.md) and [SWE-bench notes](benchmarks/SWE-bench.md)
- [Contributing](CONTRIBUTING.md)

## License

Devika is distributed under the [MIT License](LICENSE).

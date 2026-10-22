# Devika

Devika is an AI software engineer that takes high-level instructions, breaks them into steps, researches relevant information, and writes code to meet an objective. It has a Python/Flask backend with Socket.IO for real-time updates and a Svelte web interface.

![Devika screenshot](.assets/devika-screenshot.png)

## Overview

Devika's backend coordinates a set of specialized agents, each implemented as a Python class under `src/agents/`:

- **Planner**: turns a prompt into a step-by-step plan.
- **Researcher**: extracts search queries and keywords, and can ask the user for more context.
- **Formatter**: cleans up raw page content gathered during research.
- **Coder**: writes code files into the project directory.
- **Action**: maps a follow-up message to an action such as `answer`, `run`, `deploy`, `feature`, `bug`, or `report`.
- **Runner**: executes project commands and calls the Patcher when a command fails.
- **Feature** and **Patcher**: modify existing project code for new features or bug fixes.
- **Reporter**: generates a Markdown report, which is converted to PDF.
- **Decision**: handles special requests, such as browser interaction or PDF generation.
- **Internal Monologue** and **Answer**: produce status text and direct replies.

According to `ARCHITECTURE.md`, a new prompt flows through the planner, researcher, search and crawl, formatter, and coder. Later prompts go through the Action agent, which dispatches to the appropriate specialized agent.

Other components described in the repository include:

- **Language model access** through a unified `LLM` class. Supported providers in `src/llm/` are Claude, OpenAI, Google Gemini, Mistral, Groq, Ollama, and LM Studio.
- **Web search** through Bing, Google Custom Search, and DuckDuckGo implementations in `src/browser/search.py`.
- **Browser automation** with Playwright in `src/browser/`, including a natbot-style interaction loop.
- **Persistence** of projects, conversation history, and agent state in SQLite using SQLModel.
- **Services** for Netlify deployment and GitHub/Git operations.
- **Keyword extraction** with KeyBERT in `src/bert/sentence.py`.

The `docs/architecture/` directory and `ARCHITECTURE.md` contain more detail on these components.

## Requirements

The supplied files indicate the following requirements:

- **Python**: the code uses `dict | bool` type hints, which require Python 3.10 or newer. The exact supported version is not stated.
- **Python packages**: listed in `requirements.txt`, including Flask, Flask-SocketIO, gevent, Playwright, SQLModel, KeyBERT, and the LLM client libraries.
- **Node.js and Bun**: the UI is set up with `bun install`, and `ui/package.json` uses Vite and SvelteKit. The issue templates ask for Node and bun versions.
- **Docker and Docker Compose** (optional): required for the `make compose-up` workflow.
- **Ollama** (optional): for running local models. See `docs/Installation/ollama.md`.

## Setup

### Option 1: Local installation

1. Clone the repository and change into it.
2. Run the setup script:

   ```bash
   bash setup.sh
   ```

   The script runs the following steps:
   - `pip3 install -r requirements.txt`
   - `playwright install`
   - `python3 -m playwright install-deps`
   - `cd ui/` and `bun install`

3. Start the backend from the repository root:

   ```bash
   python devika.py
   ```

   The backend listens on `0.0.0.0:1337`.

4. In a second terminal, start the frontend:

   ```bash
   cd ui
   bun run dev
   ```

   The Vite dev server is configured for port 3000. The `preview` script uses port 3001.

5. Open `http://localhost:3000` in a browser.

On first run, `src/init.py` creates the storage directories and loads the BERT model used for keyword extraction, so the first startup may take longer.

### Option 2: Docker Compose

The `Makefile` provides Docker targets. These require `docker` and `docker-compose` to be installed. The `deps` target checks for both.

```bash
make compose-up
```

This runs `docker-compose up --build` and starts three services defined in `docker-compose.yaml`:

- `ollama-service` (port 11434)
- `devika-backend-engine` (port 1337), built from `devika.dockerfile`
- `devika-frontend-app` (port 3000), built from `app.dockerfile`

The frontend image is built with `VITE_API_BASE_URL=http://127.0.0.1:1337`. Backend database data is stored in the named volume `devika-backend-dbstore`.

To stop the stack, run `make compose-down`. To remove images and volumes, run `make compose-destroy`.

> **Note:** The `Makefile`'s `setup` target runs `sh +x build`, but no file named `build` appears in the repository. Use `setup.sh` for local setup instead.

## Usage

1. Start the backend and frontend as described above.
2. Open the web interface. The UI fetches the project list, model list, and search engine list from `/api/data`.
3. Select an LLM model and a search engine. The available search engines are Bing, Google, and DuckDuckGo.
4. Create a project and send a prompt describing what you want built.
5. Watch the agent's progress. The backend emits state, token usage, inference timing, and warnings over Socket.IO, and the UI displays them.
6. When the agent finishes, send follow-up messages. Devika selects an action such as answering a question, running the project, deploying to Netlify, adding a feature, fixing a bug, or generating a PDF report.

Project files are written to `data/projects/<project-name>`. The UI can list them through `/api/get-project-files`. Projects can also be downloaded as ZIP files through `/api/download-project`, and generated PDF reports through `/api/download-project-pdf`.

The backend exposes these REST endpoints (among others):

- `GET /api/status`: health check.
- `GET /api/data`: projects, models, and search engines.
- `GET`/`POST /api/settings`: read and update configuration.
- `GET /api/logs`: the contents of the log file.

Browser-based interaction is started by the Decision agent through `start_interaction`. It uses Playwright to drive a headless Chromium instance.

## Configuration

Configuration is managed by `src/config.py`, which reads `config.toml` from the working directory. If `config.toml` does not exist, it is copied from `sample.config.toml`. On each load, any keys missing from `config.toml` are added using the defaults in the sample file.

### Storage

```toml
[STORAGE]
SQLITE_DB = "data/db/devika.db"
SCREENSHOTS_DIR = "data/screenshots"
PDFS_DIR = "data/pdfs"
PROJECTS_DIR = "data/projects"
LOGS_DIR = "data/logs"
REPOS_DIR = "data/repos"
```

### API keys

The `[API_KEYS]` section holds credentials for search and model providers:

- `BING`
- `GOOGLE_SEARCH` and `GOOGLE_SEARCH_ENGINE_ID`
- `CLAUDE`
- `OPENAI`
- `GEMINI`
- `MISTRAL`
- `GROQ`
- `NETLIFY`

Keys can be set in `config.toml` or through the UI settings. Setup instructions for Bing and Google search keys are in `docs/Installation/search_engine.md`. DuckDuckGo does not require a key.

### API endpoints

The `[API_ENDPOINTS]` section configures service URLs:

- `BING` (default `https://api.bing.microsoft.com/v7.0/search`)
- `GOOGLE` (default `https://www.googleapis.com/customsearch/v1`)
- `OLLAMA` (default `http://127.0.0.1:11434`)
- `LM_STUDIO` (default `http://localhost:1234/v1`)
- `OPENAI` (default `https://api.openai.com/v1`)

Running Ollama on another address requires changing `OLLAMA` here or in the UI. The Docker Compose setup sets the `OLLAMA_HOST` environment variable to `http://ollama-service:11434`.

### Logging and timeouts

```toml
[LOGGING]
LOG_REST_API = "true"
LOG_PROMPTS = "false"

[TIMEOUT]
INFERENCE = 60
```

- `LOG_REST_API` controls whether REST requests are logged. Settings responses are masked in logs.
- `LOG_PROMPTS` controls whether model responses are logged at debug level.
- `INFERENCE` sets the maximum number of seconds to wait for a model response.

Logs are written to `data/logs/devika_agent.log` by default.

### Models

The model list is defined in `src/llm/llm.py`. It includes Claude 3 Opus, Sonnet, and Haiku; several OpenAI, Gemini, Mistral, and Groq models; LM Studio's `local-model`; and any models returned by a running Ollama server.

## Development

### Project layout

- `devika.py`: Flask and Socket.IO entry point.
- `src/`: backend code, including `agents/`, `llm/`, `browser/`, `services/`, `memory/`, `filesystem/`, and `documenter/`.
- `src/agents/<name>/`: each agent with its `prompt.jinja2` template.
- `ui/`: SvelteKit frontend using Tailwind CSS, Monaco Editor, and xterm.js.
- `docs/` and `ARCHITECTURE.md`: installation guides and architecture notes.
- `benchmarks/`: benchmark notes. `SWE-bench.md` currently reads "Not yet."

Several modules are placeholders. For example, `src/experts/` contains only docstrings describing planned domain experts, `src/sandbox/` files are empty, and `src/documenter/graphwiz.py` and `uml.py` are empty. `src/experts/__UNIMPLEMENTED__` also marks this. The `/api/run-code` endpoint currently returns a message and contains a `TODO`.

### Contributing

`CONTRIBUTING.md` describes the workflow:

1. Fork the repository.
2. Create a feature branch.
3. Make changes and make sure the code passes all tests.
4. Open a pull request.

Pull request titles should start with one of these prefixes: `Feature:`, `Fix:`, `Docs:`, `Refactor:`, `Improve:`, or `Other:`. New dependencies should be added to `requirements.txt` or `ui/package.json`. The pull request template asks for a description, a test plan, and linked issues.

Bug reports and feature requests should use the templates in `.github/ISSUE_TEMPLATE/`.

### Roadmap

`ROADMAP.md` lists these planned items:

- An extensive testing suite for all agents.
- Fixing runtime errors ahead of a stable release.
- Cross-platform installation and setup scripts.
- Tutorial videos for Windows, Linux, and macOS.
- SWE-bench testing with Claude 3 Opus.

## Testing

No test files, test directory, or pytest configuration appear in the supplied repository. `requirements.txt` includes `pytest-playwright`, and `CONTRIBUTING.md` asks contributors to ensure their code passes all tests, but no test command is defined in the repository. The roadmap lists a testing suite as future work.

To check the backend manually, start `python devika.py` and request `http://127.0.0.1:1337/api/status`. The Docker Compose health checks use the same pattern.

## License

Devika is released under the MIT License. The license text is in `LICENSE`, and the copyright line reads "Copyright (c) 2024 stition."

# Devika

Devika is an open-source AI software engineering agent. You give it a high-level instruction in a chat UI, and it plans the work, researches relevant information on the web, writes code into a per-project directory, and can then run, patch, extend, or report on that code. It is licensed under the [MIT License](LICENSE).

The project is experimental. See [Known limitations](#known-limitations) before relying on it.

## Features

- **Chat-driven projects**: Create named projects and talk to the agent about each one. Conversation history is stored per project.
- **Planning**: A Planner agent turns a request into a step-by-step plan and a summary.
- **Web research**: A Researcher agent proposes search queries. The backend runs them against the configured search engine (Bing, Google, or DuckDuckGo), opens the top result in a headless Chromium browser via Playwright, and extracts its text.
- **Code generation**: A Coder agent writes code from the plan and research results, and saves it into the project's directory.
- **Follow-up actions**: After the first pass, an Action agent classifies each follow-up message as `answer`, `run`, `deploy`, `feature`, `bug`, or `report`, and dispatches it to the matching agent.
- **Live visibility**: The UI streams agent state over Socket.IO, including the internal monologue, a browser widget with screenshots, a terminal widget, token usage, and inference timing.
- **Multiple LLM backends**: Ollama (local), LM Studio (local), Anthropic Claude, OpenAI, Google Gemini, Mistral, and Groq.
- **Optional integrations**: Netlify deployment (requires a Netlify API key) and PDF report generation.
- **Settings and logs in the UI**: A settings page that reads and writes `config.toml`, and a logs page.

## Architecture

- **Backend** (`devika.py`, `src/`): A Flask application with Flask-SocketIO, served by gevent on port `1337`. Key modules:
  - `src/agents/`: The agent classes (Planner, Researcher, Formatter, Coder, Action, Answer, Runner, Feature, Patcher, Reporter, Decision, InternalMonologue) and their Jinja2 prompt templates. `src/agents/agent.py` holds the orchestration logic.
  - `src/llm/`: Provider clients and the `LLM` wrapper that selects a backend from the model ID.
  - `src/browser/`: Search engine clients and the Playwright browser wrapper.
  - `src/project.py`, `src/state.py`: Project and agent-state persistence, using SQLite through SQLModel.
  - `src/config.py`: Reads and writes `config.toml`.
- **Frontend** (`ui/`): A SvelteKit application built with Vite and Tailwind CSS, served by the Vite dev server on port `3000`. It uses the `bun` package manager.

For more detail, see [ARCHITECTURE.md](ARCHITECTURE.md). Note that parts of that document describe the design more broadly than the current code; the source is the authority.

## Requirements

- Python 3 with `pip`
- [Bun](https://bun.sh) (used by `setup.sh` to install and run the UI)
- At least one LLM backend, either:
  - a local [Ollama](https://ollama.com) server (see [docs/Installation/ollama.md](docs/Installation/ollama.md)),
  - a local [LM Studio](https://lmstudio.ai) server, or
  - an API key for a hosted provider (Claude, OpenAI, Gemini, Mistral, or Groq)
- Optional: Bing or Google Custom Search API credentials (see [docs/Installation/search_engine.md](docs/Installation/search_engine.md)). DuckDuckGo needs no key.
- Optional: Docker and Docker Compose, for the containerized setup

## Installation

### Option 1: Local setup

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/stitionai/devika.git
   cd devika
   ```

2. Install dependencies. `setup.sh` runs the following steps:

   ```bash
   pip3 install -r requirements.txt
   playwright install
   python3 -m playwright install-deps
   cd ui/ && bun install && cd ..
   ```

   Or run `bash setup.sh` from the repository root.

3. Create your configuration file (optional; see [Configuration](#configuration)). If `config.toml` is missing, the backend creates it from `sample.config.toml` on first start.

### Option 2: Docker Compose

The repository includes `docker-compose.yaml`, which defines three services:

| Service | Image / Dockerfile | Port |
| --- | --- | --- |
| `ollama-service` | `ollama/ollama:latest` | `11434` |
| `devika-backend-engine` | `devika.dockerfile` | `1337` |
| `devika-frontend-app` | `app.dockerfile` | `3000` |

Both Dockerfiles `COPY config.toml`, so create it first:

```bash
cp sample.config.toml config.toml
docker-compose up --build
```

`make compose-up` runs the same command after checking that Docker and `docker-compose` are installed. `make compose-down` stops the stack, and `make compose-destroy` removes Devika images and prunes volumes.

## Running

Start the backend from the repository root. Relative paths in the code (such as `config.toml`, `sample.config.toml`, and the `src/agents/*/prompt.jinja2` templates) depend on the working directory:

```bash
python3 devika.py
```

The API listens on `http://0.0.0.0:1337`. Check it with:

```bash
curl http://127.0.0.1:1337/api/status
```

In a second terminal, start the UI:

```bash
cd ui
bun run dev
```

Open `http://localhost:3000`. The UI sends requests to `http://127.0.0.1:1337` when accessed from `localhost` or `127.0.0.1`, and to `http://<host>:1337` otherwise. Set `VITE_API_BASE_URL` to override this.

### Using Devika

1. Create a project in the sidebar.
2. Select an LLM model and a search engine.
3. Send a request. The agent plans, researches, and writes code into the project's directory.
4. Send follow-up messages to run, fix, extend, or report on the code. Use the Settings page to set API keys if you have not edited `config.toml` directly.

Generated projects are stored under the configured projects directory (`data/projects` by default).

## Configuration

Settings live in `config.toml`, in the directory where the backend runs. It is generated from `sample.config.toml` if missing. Keys missing from an existing `config.toml` are filled in from the sample on startup. You can also change API keys, endpoints, and logging options through the UI, which writes to the same file.

| Section | Key | Default | Purpose |
| --- | --- | --- | --- |
| `STORAGE` | `SQLITE_DB` | `data/db/devika.db` | SQLite database path |
| `STORAGE` | `SCREENSHOTS_DIR` | `data/screenshots` | Browser screenshots |
| `STORAGE` | `PDFS_DIR` | `data/pdfs` | Generated PDF reports |
| `STORAGE` | `PROJECTS_DIR` | `data/projects` | Project files |
| `STORAGE` | `LOGS_DIR` | `data/logs` | Log files |
| `STORAGE` | `REPOS_DIR` | `data/repos` | Repository storage |
| `API_KEYS` | `BING`, `GOOGLE_SEARCH`, `GOOGLE_SEARCH_ENGINE_ID` | placeholders | Search engine credentials |
| `API_KEYS` | `CLAUDE`, `OPENAI`, `GEMINI`, `MISTRAL`, `GROQ` | placeholders | LLM provider keys |
| `API_KEYS` | `NETLIFY` | placeholder | Netlify deployment |
| `API_ENDPOINTS` | `BING`, `GOOGLE` | Microsoft and Google search API URLs | Search endpoints |
| `API_ENDPOINTS` | `OLLAMA` | `http://127.0.0.1:11434` | Ollama server |
| `API_ENDPOINTS` | `LM_STUDIO` | `http://localhost:1234/v1` | LM Studio server |
| `API_ENDPOINTS` | `OPENAI` | `https://api.openai.com/v1` | OpenAI base URL |
| `LOGGING` | `LOG_REST_API` | `"true"` | Log REST API calls |
| `LOGGING` | `LOG_PROMPTS` | `"false"` | Log prompts and responses |
| `TIMEOUT` | `INFERENCE` | `60` | Seconds before an LLM call is treated as timed out |

Placeholder values such as `<YOUR_CLAUDE_API_KEY>` must be replaced before use. Do not commit `config.toml`, because it holds your API keys.

### Model selection

The model list is built at request time from the code in `src/llm/llm.py`:

- **Ollama**: Models returned by your Ollama server, if it is reachable when the backend starts.
- **LM Studio**: A single entry, `local-model`.
- **Claude, OpenAI, Gemini, Mistral, Groq**: A fixed list of models hard-coded in `src/llm/llm.py`.

Setting `LOG_PROMPTS = "true"` logs prompts and responses. Only enable it when you are comfortable with that data being written to the log files.

### Search engines

- **Bing** and **Google** require API keys and endpoints as described in [docs/Installation/search_engine.md](docs/Installation/search_engine.md).
- **DuckDuckGo** needs no keys. The source comments in `src/browser/search.py` state that this integration may not work with the current setup, so expect it to be unreliable.

## Repository layout

```
devika.py              Flask + Socket.IO backend entry point
requirements.txt       Python dependencies
setup.sh               Local install helper (pip, Playwright, bun)
sample.config.toml     Default configuration template
docker-compose.yaml    Multi-service Docker setup
devika.dockerfile      Backend image
app.dockerfile         Frontend image
Makefile               Docker Compose helper targets
src/
  agents/              Agent implementations and prompt templates
  apis/                Project REST endpoints (Flask blueprint)
  bert/                Keyword extraction (KeyBERT / sentence embeddings)
  browser/             Search clients and Playwright browser control
  documenter/          PDF, UML, and Graphviz output helpers
  experts/             Domain knowledge modules (web design, math, physics, etc.)
  filesystem/          Code reading utilities
  llm/                 LLM provider clients
  memory/              Knowledge base and RAG modules
  sandbox/             Placeholder for sandboxed execution (currently empty)
  services/            GitHub, Git, and Netlify integrations
ui/                    SvelteKit frontend
docs/                  Installation guides and architecture notes
benchmarks/            Benchmark documentation (currently empty)
```

## REST API

These endpoints are defined in `devika.py` and `src/apis/project.py`. Requests and responses are JSON unless noted.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/status` | Health check |
| GET | `/api/data` | Projects, available models, and search engines |
| POST | `/api/messages` | Messages for a project |
| POST | `/api/is-agent-active` | Whether the agent is running for a project |
| POST | `/api/get-agent-state` | Latest agent state for a project |
| GET | `/api/get-browser-session` | Browser session for a project |
| GET | `/api/get-terminal-session` | Terminal session for a project |
| GET | `/api/get-browser-snapshot` | Serves a screenshot file (`snapshot_path` query parameter) |
| POST | `/api/calculate-tokens` | Token count for a prompt |
| GET | `/api/token-usage` | Token usage for a project |
| GET | `/api/logs` | Log file contents |
| GET / POST | `/api/settings` | Read or update configuration |
| GET | `/api/get-project-files` | Files in a project (`project_name` query parameter) |
| POST | `/api/create-project` | Create a project |
| POST | `/api/delete-project` | Delete a project and its agent state |
| GET | `/api/download-project` | Download a project as a zip |
| GET | `/api/download-project-pdf` | Download a generated PDF report |

Chat messages are sent over Socket.IO, not REST. The client emits `user-message` with `message`, `base_model`, `project_name`, and `search_engine`. The server streams updates back on channels such as `agent-state`, `server-message`, `tokens`, `inference`, and `info`.

`POST /api/run-code` is a stub. It returns a success message without running code.

## Security notes

- **Code execution is not sandboxed.** The Runner agent executes the shell commands the LLM proposes with `subprocess.run` in the project directory, on the host (or inside the container if you use Docker). `src/sandbox/` contains no working code. Run Devika only in an environment you are willing to give the agent full access to, and review generated commands before using it on anything important.
- **Keys are stored in plain text** in `config.toml`.
- **CORS**: The Flask app allows `localhost:3000` origins. The Socket.IO server is configured with `cors_allowed_origins="*"`.

## Known limitations

- **Sandboxing is not implemented** (see Security notes).
- **Git clone is not implemented.** The `git_clone` branch in `src/agents/agent.py` contains only a placeholder comment.
- **Run-code endpoint is a stub**: `POST /api/run-code` does nothing beyond returning a message.
- **No automated test suite is included.** `ROADMAP.md` lists creating one as a goal.
- **Benchmarks**: `benchmarks/BENCHMARKS.md` and `benchmarks/SWE-bench.md` contain no results in this repository, and `ROADMAP.md` lists SWE-bench testing as planned. This README makes no performance claims.
- **Docker volume path**: The compose file mounts a volume at `/home/nonroot/devika/db`, but the default database path is `data/db/devika.db`, which resolves to `/home/nonroot/devika/data/db/devika.db` inside the container. Data may not persist across container rebuilds unless you update `SQLITE_DB` or the volume path.
- **Docker Ollama endpoint**: The compose file sets `OLLAMA_HOST`, but the application reads its Ollama URL from `config.toml` (`API_ENDPOINTS.OLLAMA`, default `http://127.0.0.1:11434`). Inside Docker, set this to `http://ollama-service:11434` so the backend can reach the Ollama container.
- **Agent prompts and models**: Output quality depends on the chosen model and on the prompt templates in `src/agents/`. Results will vary.

## Roadmap

From [ROADMAP.md](ROADMAP.md):

- [ ] Extensive testing suite for all agents
- [ ] Fix runtime errors ahead of a stable release
- [ ] Cross-platform installation and setup scripts
- [ ] Tutorial videos for installation, setup, and usage
- [ ] Testing on SWE-bench, focusing on Claude 3 Opus

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the pull request workflow and title prefixes (`Feature:`, `Fix:`, `Docs:`, `Refactor:`, `Improve:`, `Other:`). Report bugs as [GitHub issues](https://github.com/stitionai/devika/issues).

## License

Devika is released under the MIT License. See [LICENSE](LICENSE). Copyright (c) 2024 stition.

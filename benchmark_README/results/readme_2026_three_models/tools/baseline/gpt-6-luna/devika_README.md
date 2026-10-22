# Devika

Devika is an AI software-engineering assistant with a web interface. It takes a high-level task, creates a plan, researches relevant information, and generates files in a project workspace. In follow-up conversations, it can answer questions about a project, run commands, implement features, attempt bug fixes, create reports, and deploy through Netlify.

The application is made up of a Flask and Flask-SocketIO backend, a SvelteKit frontend, and a collection of specialized Python agents. Project messages and agent state are persisted in SQLite. The interface provides project and model selection, a chat view, project-file browsing and editing, and views for agent activity, browser information, terminal output, settings, and logs.

## Capabilities and architecture

The main agent flow uses specialized agents for planning, research, formatting research results, coding, and internal-monologue updates. The planner turns a request into steps; the researcher identifies queries and may ask the user for more context; and the coder writes files to the project directory. Follow-up messages are classified into actions such as answering, running code, adding a feature, fixing a bug, or reporting.

Devika can search using Bing, Google, or DuckDuckGo and uses Playwright for browser access. It supports language-model providers including Anthropic Claude, OpenAI, Google Gemini, Mistral, Groq, Ollama, and LM Studio. Optional service integrations include GitHub and Netlify. Provider availability depends on configuration and credentials; local providers also require their respective services to be running.

For a deeper technical description, see [ARCHITECTURE.md](ARCHITECTURE.md) and the documents in [`docs/architecture`](docs/architecture/).

## Requirements

The repository does not specify minimum operating-system, Python, Node.js, or Bun versions. The setup scripts and project configuration use:

- Python 3 and `pip3` for the backend dependencies.
- Playwright and its browser/system dependencies for browser automation.
- Bun for installing and running the frontend.
- Docker and Docker Compose if using the container setup.

Some LLM and search providers require API keys. Ollama and LM Studio require a reachable local or remote service if selected.

## Installation

### Local setup

From the repository root, run the supplied setup script:

```bash
bash setup.sh
```

The script installs Python packages from `requirements.txt`, installs Playwright browsers and system dependencies, and installs frontend packages in `ui/` with Bun.

On first backend startup, Devika creates `config.toml` from `sample.config.toml` if it does not already exist. Edit `config.toml` before using features that require provider credentials or non-default endpoints. See [Configuration](#configuration).

Start the backend from the repository root:

```bash
python3 devika.py
```

The backend starts on port `1337` and listens on `0.0.0.0`. In another terminal, start the frontend:

```bash
cd ui
bun run dev
```

The Vite development server uses port `3000`. Open the frontend at `http://localhost:3000`. The UI’s API client defaults to `http://127.0.0.1:1337` for local browser hosts.

### Docker Compose

The supplied Compose configuration builds and starts an Ollama service, the Devika backend, and the frontend:

```bash
docker-compose up --build
```

The Compose file publishes Ollama on port `11434`, the backend on `1337`, and the frontend on `3000`. It configures the backend to connect to the Compose Ollama service and persists backend database data in a named volume. The frontend build receives `VITE_API_BASE_URL=http://127.0.0.1:1337`.

The Makefile also defines `compose-up`, `compose-down`, and `compose-destroy` targets. Its Docker dependency checks expect both `docker` and `docker-compose` commands to be available.

## Configuration

Configuration is stored in the root-level `config.toml`. The sample file groups settings into these sections:

- **`STORAGE`**: SQLite database, screenshots, PDFs, projects, logs, and repository directories. The sample defaults use paths under `data/`.
- **`API_KEYS`**: Credentials for Bing, Google Search, Claude, OpenAI, Gemini, Mistral, Groq, and Netlify. Replace the sample placeholders with credentials for the services you use.
- **`API_ENDPOINTS`**: Bing and Google Search endpoints, the Ollama endpoint, the LM Studio endpoint, and the OpenAI-compatible endpoint.
- **`LOGGING`**: Whether REST API calls and prompts are logged.
- **`TIMEOUT`**: The inference timeout, shown as 60 seconds in the sample.

The configuration loader fills missing settings from the sample configuration. The UI also exposes settings, and the backend provides `GET` and `POST /api/settings` endpoints for reading and updating them.

DuckDuckGo search does not require an API key. Bing and Google require credentials; Google also needs a Custom Search Engine ID. See [`docs/Installation/search_engine.md`](docs/Installation/search_engine.md) for setup instructions. For Ollama installation, model downloads, and endpoint configuration, see [`docs/Installation/ollama.md`](docs/Installation/ollama.md). The Ollama guide notes that the default service address is `http://localhost:11434`.

## Usage

1. Start the backend and frontend, then open the web UI.
2. Create or select a project.
3. Select an available language model and a search engine.
4. Enter a task in the chat interface. Devika plans the work, may research the web or request more context, and writes generated files into the project workspace.
5. Continue in the same project to ask questions or request actions such as running the project, changing a feature, fixing a problem, or generating a report.

Project files are stored beneath the configured projects directory. The sample path is `data/projects`; project names are converted to lowercase, with spaces replaced by hyphens, for directory names. The backend also provides endpoints to list project files, create or delete projects, and download a project archive. Reports can be generated as PDFs in the configured PDF directory.

The backend exposes `GET /api/status` as a basic server status check and uses Socket.IO to send messages, agent-state updates, token counts, and other activity to the frontend. The UI also includes settings and logs pages.

## Development

The backend entry point is `devika.py`. Agent implementations and their Jinja2 prompts are under `src/agents`; provider clients are under `src/llm`; browser and search code is under `src/browser`; and project persistence and agent-state persistence are implemented in `src/project.py` and `src/state.py`.

The frontend is a SvelteKit application in `ui/`, built with Vite. Its package scripts include:

```bash
cd ui
bun run dev
bun run build
bun run preview
```

`bun run build` creates a production frontend build. The Vite preview server is configured for port `3001`.

Contributions are welcome. Before starting, check existing issues and pull requests. The project’s [contribution guide](CONTRIBUTING.md) asks contributors to work on a branch, test changes, document relevant behavior, and include dependency changes in `requirements.txt` or `ui/package.json` as appropriate. Pull request titles should use prefixes such as `Feature:`, `Fix:`, `Docs:`, `Refactor:`, `Improve:`, or `Other:`.

## Testing

The supplied repository does not include a dedicated test suite or test files. `pytest` and `pytest-playwright` are listed in `requirements.txt`, but no project-specific test command is defined. When submitting a change, describe the checks you performed in the pull request; the pull request template requests a test plan. For frontend changes, `bun run build` checks that the UI can be built.

The roadmap lists creating an extensive agent test suite and addressing runtime errors as future work. Benchmark documentation is present, but the SWE-bench file states that results are not yet available.

## License

Devika is distributed under the [MIT License](LICENSE). The license permits use, modification, distribution, sublicensing, and sale, subject to retaining the copyright and permission notice. The software is provided “as is,” without warranty.

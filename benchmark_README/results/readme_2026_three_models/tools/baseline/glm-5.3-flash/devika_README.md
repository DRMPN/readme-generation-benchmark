# Devika

Devika is an advanced AI software engineer that can understand high-level human instructions, break them down into steps, research relevant information, and write code to achieve a given objective. It is built as a Python backend (Flask + Socket.IO) paired with a SvelteKit web UI, and is designed to plan, research, code, run, patch, and report on software projects with minimal human intervention.

## Overview

Devika combines several key components into a single agentic system:

- **Agent Core** — the central engine that orchestrates planning, reasoning, and execution. It manages conversation history, agent state, internal monologue, and context accumulation, and emulates a "thinking" process while agents work.
- **Specialized Agents** — dedicated sub-agents, each implemented as a Python class with a Jinja2 prompt template:
  - **Planner** — generates a step-by-step plan from the user's prompt
  - **Researcher** — extracts and ranks search queries from the plan
  - **Coder** — generates code segmented into files and directories
  - **Action** — maps follow-up user messages to actions (run, test, deploy, fix, implement, report)
  - **Runner** — executes written code in a sandboxed environment and streams output in real time
  - **Feature** — implements new features while preserving existing code structure
  - **Patcher** — debugs and fixes issues based on error messages or descriptions
  - **Reporter** — generates comprehensive project reports, exportable as PDF
  - **Decision** — handles special command-like instructions (e.g. git clone, browser interaction)
- **Language Models** — a unified `LLM` interface over multiple providers, with dedicated clients for **Claude (Anthropic)**, **OpenAI (GPT-4/GPT-3)**, **Ollama** (self-hosted models), **Gemini**, **Groq**, **Mistral**, and **LM Studio**.
- **Browser Interaction** — automated web browsing, searching, and page interaction built on Playwright, including a search integration (see `docs/Installation/search_engine.md` for configuring search engines).
- **Project Management** — organization and persistence of project data, messages, and files.
- **Memory** — a knowledge base with RAG (retrieval-augmented generation) and sentence embedding support.
- **Services** — integrations with **GitHub** and **Netlify** for deployment, plus Git support.
- **Sandbox** — sandboxed code execution, including a Firejail-based runner.
- **Experts** — domain-specific expert modules (chemistry, math, medical, physics, game dev, web design, Stack Overflow).
- **Utilities** — configuration (`sample.config.toml`), logging, token counting, and PDF/graphviz/UML documenters.

For a deep dive into how these components fit together, see [ARCHITECTURE.md](ARCHITECTURE.md), [docs/architecture/UNDER_THE_HOOD.md](docs/architecture/UNDER_THE_HOOD.md), and [ROADMAP.md](ROADMAP.md).

## Project Structure

```
├── devika.py                 # Backend entrypoint (Flask + Socket.IO server)
├── setup.sh                  # Setup script
├── sample.config.toml        # Sample configuration file
├── requirements.txt          # Python dependencies
├── Makefile                  # Docker convenience targets
├── app.dockerfile            # Dockerfile for the full app
├── devika.dockerfile         # Dockerfile for the backend
├── docker-compose.yaml       # Docker Compose configuration
├── src/
│   ├── agents/               # Planner, Researcher, Coder, Action, etc.
│   ├── llm/                  # LLM clients (Claude, OpenAI, Ollama, Gemini, ...)
│   ├── browser/              # Browser automation and search
│   ├── memory/               # Knowledge base and RAG
│   ├── sandbox/              # Sandboxed code execution
│   ├── services/             # GitHub, Netlify, Git services
│   ├── apis/                 # API layer
│   ├── experts/              # Domain expert modules
│   ├── bert/, documenter/, filesystem/, ...
├── ui/                       # SvelteKit frontend
├── benchmarks/               # Benchmark documentation (SWE-bench)
└── docs/                     # Architecture and installation docs
```

## Requirements

- **Python** with `pip` (dependencies listed in `requirements.txt`)
- **Docker** and **docker-compose** (only if using the Docker setup; the `Makefile` checks for both)
- A configured **search engine** — see `docs/Installation/search_engine.md` for Bing and Google setup instructions with screenshots
- Optionally, **Ollama** for self-hosted models — see `docs/Installation/ollama.md`
- API keys for your chosen LLM providers (configured via the settings file/UI)

## Setup

### Manual setup

1. Clone the repository.
2. Run the provided setup script:

   ```sh
   sh +x setup.sh
   ```

3. Install the Python dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Copy `sample.config.toml` to your config file and fill in provider API keys and other settings.

### Docker setup

The repository ships with Dockerfiles and a `docker-compose.yaml`, plus a `Makefile` with convenience targets:

```sh
make setup            # run the setup script
make compose-up       # build and start the Docker Compose stack
make compose-down     # stop the stack
make compose-destroy  # remove Devika images and prune volumes
```

The `deps` target verifies that `docker` and `docker-compose` are installed before running the other targets.

## Running

### Backend

Start the Flask/Socket.IO server:

```sh
python devika.py
```

The backend serves the API on port **1337**. The UI determines the backend address from `window.location.hostname` (i.e. `http://127.0.0.1:1337` locally), or from the `VITE_API_BASE_URL` environment variable if set.

### Frontend

The `ui/` directory contains a SvelteKit application (with a Bun lockfile present, but standard npm/pnpm flows work with the scripts in `ui/package.json`):

```sh
cd ui
npm install
npm run dev       # development server
npm run build     # production build
npm run preview   # preview the production build
```

### Frontend environment

- `VITE_API_BASE_URL` — overrides the backend URL used by the UI (defaults to `http://127.0.0.1:1337` or `http://<host>:1337`).

## Usage

Once the backend and UI are running:

1. **Create a project** — projects organize prompts, messages, files, and agent state. Projects can be created and deleted from the UI (or via the API).
2. **Select a model and search engine** — pick from the available LLMs and configured search engines in the UI.
3. **Send a prompt** — describe what you want built. Devika will plan, research, write code, and stream its progress live to the UI.
4. **Follow up** — send follow-up messages; the Action agent routes them to the Runner, Feature, Patcher, Reporter, or other agents as appropriate.
5. **Inspect artifacts** — the UI provides:
   - A **Monaco-based code editor** with file tree and tab switching
   - A **browser snapshot widget** showing what Devika browsed
   - A **terminal widget** (xterm) for streamed command output
   - A **logs page** for detailed logs
   - A **settings page** for managing configuration
   - Live **token usage** tracking

### API Endpoints

The backend exposes a JSON API used by the UI (all under `/api`):

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/status` | GET | Check server status |
| `/api/data` | GET | Fetch projects, models, and search engines |
| `/api/create-project` | POST | Create a new project |
| `/api/delete-project` | POST | Delete a project |
| `/api/messages` | POST | Fetch messages for a project |
| `/api/get-agent-state` | POST | Fetch agent state for a project |
| `/api/execute-agent` | POST | Execute the agent with a prompt, model, and project |
| `/api/browser-snapshot` | POST | Fetch a browser snapshot |
| `/api/get-project-files` | GET | List files for a project |
| `/api/settings` | GET/POST | Fetch or update settings |
| `/api/logs` | GET | Fetch server logs |

Real-time updates (agent state, messages, token usage, toasts) are pushed over **Socket.IO**.

## Configuration

Configuration is defined in a TOML file; `sample.config.toml` in the repository root serves as the template. It is loaded by `src/config.py` and can also be managed at runtime through the `/api/settings` endpoints and the settings page in the UI. The configuration covers LLM provider API keys, search engine credentials, and other runtime options — consult the sample file for the exact schema.

## Development

- **Backend**: Python, Flask, Flask-SocketIO, and eventlet/gevent for real-time communication. Agents live in `src/agents/`, each with its own Jinja2 prompt template (`prompt.jinja2`). The `LLM` class in `src/llm/llm.py` abstracts provider-specific clients, making it straightforward to add or swap models.
- **Frontend**: SvelteKit + Vite, Tailwind CSS, `bits-ui` component primitives (tabs, select, resizable panes, sonner toasts), Monaco editor for code display, and xterm for terminal output. State is managed with Svelte stores, with selections (project, model, search engine) persisted in `localStorage`.
- **Documentation**: architecture details are in `ARCHITECTURE.md` and `docs/architecture/`; a roadmap is in `ROADMAP.md`.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. The repository includes issue templates for bug reports, feature requests, and general issues, plus a pull request template — please use them when opening issues or PRs.

## Testing

`pytest-playwright` is included in the Python dependencies, so tests can be run with:

```sh
pytest
```

## Benchmarks

The `benchmarks/` directory contains benchmark documentation, including SWE-bench results and methodology ([benchmarks/SWE-bench.md](benchmarks/SWE-bench.md)).

## License

This project is licensed under the [MIT License](LICENSE) — Copyright (c) 2024 stition. Permission is granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the license terms included in the `LICENSE` file.

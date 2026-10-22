# Devika

Devika is an open-source agentic AI software engineer. Given a high-level request, it plans the work, researches the relevant information, writes and runs code, and reports back. It is inspired by Devin, the autonomous coding agent from Cognition AI, and is designed to work with multiple large language model (LLM) providers, including local models.

> **Note:** This README was generated from the repository's file layout. Commands, ports, and config keys are based on typical conventions for this project. Check them against `sample.config.toml`, `setup.sh`, `Makefile`, and the source before relying on them.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Option 1: Local Setup](#option-1-local-setup)
  - [Option 2: Docker](#option-2-docker)
- [Configuration](#configuration)
  - [LLM Providers](#llm-providers)
  - [Search Engines](#search-engines)
  - [Other Settings](#other-settings)
- [Usage](#usage)
- [Agents](#agents)
- [Prompt Templates](#prompt-templates)
- [Sandboxed Code Execution](#sandboxed-code-execution)
- [Knowledge Base and RAG](#knowledge-base-and-rag)
- [Real-Time Communication](#real-time-communication)
- [Frontend](#frontend)
- [Development](#development)
- [Benchmarks](#benchmarks)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Autonomous planning:** Breaks a user's prompt into steps and decides which agent handles each step.
- **Web research:** Searches the web through several engines, browses pages with a headless browser, and extracts relevant text from PDFs and other sources.
- **Code generation and editing:** Writes new code, patches existing files, and reruns failing steps after fixes.
- **Sandboxed execution:** Runs generated code inside a Firejail sandbox to limit access to the host system.
- **Multiple LLM backends:** Supports hosted APIs (OpenAI, Claude, Gemini, Mistral, Groq) and local runtimes (Ollama, LM Studio).
- **Knowledge base and retrieval:** Stores and retrieves project context with a retrieval-augmented generation (RAG) pipeline.
- **Project management:** Organizes work into projects, tracks state, and integrates with Git, GitHub, and Netlify for version control and deployment.
- **Diagram generation:** Creates UML and Graphviz diagrams to document designs.
- **Live web UI:** A Svelte-based interface streams the agent's progress, internal reasoning, and outputs in real time.
- **Containerized deployment:** Ships with Dockerfiles and a Docker Compose configuration.

---

## How It Works

1. **Prompt:** The user describes a task in the web UI, such as "Build a Snake game in Python" or "Research the latest Rust async runtimes and write a comparison."
2. **Decision:** The decision agent determines the type of request, for example a question, a research task, or a coding task.
3. **Planning:** The planner agent breaks the task into an ordered list of steps.
4. **Research:** When a step needs outside information, the researcher agent runs searches, opens pages in the browser, and summarizes what it finds.
5. **Coding:** The coder agent writes code for the step. The patcher agent applies targeted edits to existing files.
6. **Execution:** The runner agent executes the code in a sandbox and captures stdout, stderr, and exit codes.
7. **Recovery:** If a run fails, the rerunner and action agents analyze the error, adjust the plan or code, and try again.
8. **Reporting:** The reporter agent summarizes the results for the user. The internal monologue module records the agent's reasoning so it can be inspected in the UI.

---

## Architecture

```
┌──────────────────────────┐        WebSocket        ┌─────────────────────────────┐
│   Svelte Frontend (Vite) │ <─────────────────────> │  Python Backend (devika.py) │
│   - Chat & project views │                         │  - Socket instance          │
│   - Agent state display  │                         │  - Agent orchestration      │
└──────────────────────────┘                         │  - State & project storage  │
                                                     └──────────────┬──────────────┘
                                                                    │
                    ┌───────────────────────┬───────────────────────┼──────────────────────┐
                    │                       │                       │                      │
             ┌──────▼──────┐        ┌───────▼───────┐       ┌───────▼────────┐      ┌──────▼───────┐
             │  LLM layer  │        │ Search/Browse │       │ Code execution │      │ Integrations │
             │  (clients)  │        │ Bing/Google   │       │ Firejail       │      │ Git/GitHub   │
             │             │        │ Browser, PDF  │       │ Runner         │      │ Netlify      │
             └─────────────┘        └───────────────┘       └────────────────┘      └──────────────┘
```

The backend is organized around agents. A central orchestrator sends messages to the right agent, and each agent calls the LLM layer with a prompt template. Agents use tools such as the browser, search engines, and the code runner to gather information and act on the environment. State is persisted so that a project can be resumed later.

---

## Project Structure

The layout below is a reconstruction based on the repository's files. Some paths are inferred.

```
devika/
├── devika.py                  # Main entry point for the backend
├── requirements.txt           # Python dependencies
├── sample.config.toml         # Template for the runtime configuration
├── setup.sh                   # Local setup helper script
├── Makefile                   # Common development commands
├── docker-compose.yaml        # Multi-container setup
├── devika.dockerfile          # Backend image
├── app.dockerfile             # Frontend image
├── src/
│   ├── config.py              # Loads configuration values
│   ├── state.py               # Agent and project state management
│   ├── llm/                   # LLM provider clients
│   │   ├── llm.py             # Provider-agnostic interface
│   │   ├── openai_client.py
│   │   ├── claude_client.py
│   │   ├── gemini_client.py
│   │   ├── mistral_client.py
│   │   ├── groq_client.py
│   │   ├── ollama_client.py
│   │   └── lm_studio_client.py
│   ├── agents/                # Agent implementations, each with a prompt.jinja2
│   │   ├── planner/
│   │   ├── researcher/
│   │   ├── coder/
│   │   ├── patcher/
│   │   ├── runner/
│   │   ├── rerunner/
│   │   ├── action/
│   │   ├── decision/
│   │   ├── feature/
│   │   ├── answer/
│   │   ├── formatter/
│   │   ├── reporter/
│   │   ├── internal_monologue/
│   │   └── agent.py           # Base agent class
│   ├── knowledge_base.py      # Knowledge storage
│   ├── rag.py                 # Retrieval-augmented generation
│   ├── socket_instance.py     # WebSocket server setup
│   ├── services/              # Tools used by agents
│   │   ├── browser.py         # Headless browser automation
│   │   ├── search.py          # Search engine interface
│   │   ├── sentence.py        # Text processing utilities
│   │   ├── code_runner.py     # Code execution
│   │   ├── firejail.py        # Sandboxing wrapper
│   │   ├── pdf.py             # PDF text extraction
│   │   ├── uml.py             # UML diagram generation
│   │   ├── graphwiz.py        # Graphviz diagram generation
│   │   ├── logger.py
│   │   ├── git.py
│   │   ├── github.py
│   │   ├── netlify.py
│   │   ├── read_code.py
│   │   └── utils.py
│   ├── project.py             # Project management
│   └── __UNIMPLEMENTED__/     # Experimental, unfinished modules (game-dev, physics, math, medical, chemistry, stackoverflow, web-design)
├── frontend/                  # Svelte + Tailwind UI (Vite)
│   ├── src/
│   │   ├── app.html
│   │   ├── routes/            # +layout.js, +page.svelte, +layout.svelte
│   │   ├── app.pcss
│   │   └── components/
│   ├── static/                # Avatars, favicon, bootup.mp3, loading animation
│   ├── package.json
│   ├── bun.lockb
│   ├── svelte.config.js
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.cjs
│   └── components.json
└── docs/
    ├── README.md
    ├── ARCHITECTURE.md
    ├── UNDER_THE_HOOD.md
    ├── BENCHMARKS.md
    ├── SWE-bench.md
    ├── CONTRIBUTING.md
    ├── ollama.md
    ├── search_engine.md
    ├── ROADMAP.md
    └── images/                # Screenshots of search engines (google, bing)
```

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Python** | 3.10 or newer is recommended. |
| **Node.js / Bun** | Bun is used for the frontend (`bun.lockb` is present). |
| **Git** | Required for the Git and GitHub integrations. |
| **Firejail** | Linux sandboxing for code execution. Install it with your package manager, for example `sudo apt install firejail`. |
| **Docker and Docker Compose** | Needed only for the containerized setup. |
| **At least one LLM provider** | A hosted API key, or a local runtime such as Ollama or LM Studio. |
| **Search API key** (optional) | Needed for Bing or Google search. See [Search Engines](#search-engines). |

---

## Installation

### Option 1: Local Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/stitionai/devika.git
   cd devika
   ```

2. **Create the configuration file**

   ```bash
   cp sample.config.toml config.toml
   ```

   Edit `config.toml` and add your API keys and preferred models. See [Configuration](#configuration).

3. **Run the setup script** (optional but recommended)

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   If you prefer manual setup, continue with the next steps.

4. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

5. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

6. **Install the browser runtime** (needed by the browser tool)

   ```bash
   playwright install
   ```

   Depending on the implementation, you may need to run `playwright install-deps` on Linux to install system libraries.

7. **Start the backend**

   ```bash
   python devika.py
   ```

   The backend listens on port **1337** by default.

8. **Install and start the frontend** (in a second terminal)

   ```bash
   cd frontend
   bun install
   bun run dev
   ```

   Open **http://localhost:3000** in your browser.

If `Makefile` targets are defined, you can use them instead, for example `make install` or `make run`. Check the file for the exact target names.

### Option 2: Docker

1. Create and edit `config.toml` as described above.

2. Build and start the containers:

   ```bash
   docker compose up --build
   ```

   `docker-compose.yaml` starts the backend using `devika.dockerfile` and the frontend using `app.dockerfile`.

3. Open **http://localhost:3000**.

To stop the containers:

```bash
docker compose down
```

---

## Configuration

Devika reads its settings from `config.toml`, which you create from `sample.config.toml`. Never commit this file, because it contains API keys. Add it to `.gitignore` if it is not already listed.

A minimal configuration might look like this. The exact keys are defined in `sample.config.toml` and `src/config.py`, so treat this as an illustration:

```toml
[API_KEYS]
OPENAI = ""
CLAUDE = ""
GEMINI = ""
MISTRAL = ""
GROQ = ""
BING = ""
GOOGLE_SEARCH = ""
GOOGLE_CX = ""
NETLIFY = ""

[API_ENDPOINTS]
OLLAMA = "http://localhost:11434"
LM_STUDIO = "http://localhost:1234/v1"

[MODELS]
DEFAULT = "claude-3-5-sonnet"

[STORAGE]
PROJECT_DIR = "./projects"
```

### LLM Providers

Devika supports the following providers. Set the API key for the provider you use, and choose a model name that the provider supports.

| Provider | Type | Client file | Requirements |
|---|---|---|---|
| OpenAI | Hosted | `openai_client.py` | API key |
| Anthropic Claude | Hosted | `claude_client.py` | API key |
| Google Gemini | Hosted | `gemini_client.py` | API key |
| Mistral | Hosted | `mistral_client.py` | API key |
| Groq | Hosted | `groq_client.py` | API key |
| Ollama | Local | `ollama_client.py` | Ollama installed and a model pulled, for example `ollama pull llama3` |
| LM Studio | Local | `lm_studio_client.py` | LM Studio running its local server |

**Using Ollama:**

```bash
ollama serve
ollama pull llama3
```

Then select the Ollama provider and model in the settings. See `ollama.md` for details.

**Tips for model selection:** Agents rely on structured output and multi-step reasoning, so larger and more capable models generally produce better results. Local models work, but they may need more retries and more careful prompting.

### Search Engines

Devika's researcher agent can search the web through several engines:

- **Bing** (requires a Bing Search API key)
- **Google** (requires a Google Custom Search API key and a Search Engine ID, `GOOGLE_CX`)
- **Other engines** may be available depending on the search module. See `search_engine.md`.

The `bing.png`, `bing-1.png`, `google.png`, and `google-2.png` files in the repository are reference screenshots for these integrations.

### Other Settings

| Setting | Purpose |
|---|---|
| Project directory | Where generated projects are stored |
| Browser options | Headless mode and timeouts for the browser tool |
| Sandbox options | Firejail profile and limits for code execution |
| Netlify token | Enables one-click deployment of generated static sites |
| GitHub token | Enables creating repositories and pushing code |

---

## Usage

1. Start the backend and frontend (see [Installation](#installation)).
2. Open **http://localhost:3000**.
3. Select an LLM provider and model in the settings panel.
4. Create a new project or start a chat, and describe the task. Examples:
   - *"Create a to-do list web app with React and local storage."*
   - *"Research how transformers handle long context and summarize the main approaches."*
   - *"Write a Python script that scrapes the titles from a news site and saves them to CSV."*
5. Watch the agent's progress in the live panel. You can see the plan, search results, code, execution output, and internal reasoning.
6. Review the final report and the generated files in the project directory.

---

## Agents

Each agent has a single responsibility and a dedicated prompt template.

| Agent | Responsibility |
|---|---|
| **Decision** | Classifies the request and chooses the workflow |
| **Planner** | Produces the step-by-step plan |
| **Feature** | Handles feature-level requests within an existing project |
| **Researcher** | Searches the web, reads sources, and summarizes findings |
| **Coder** | Writes new code files |
| **Patcher** | Makes targeted edits to existing code |
| **Runner** | Executes code and captures output |
| **Rerunner** | Re-executes code after a fix and checks the result |
| **Action** | Chooses the next tool or operation to run |
| **Formatter** | Normalizes output into the expected format |
| **Answer** | Responds directly to conversational or factual questions |
| **Reporter** | Produces the final summary for the user |
| **Internal Monologue** | Records the agent's reasoning for transparency and debugging |

All agents inherit from a base class in `src/agents/agent.py`. To add a new agent, create a folder with an `__init__.py`, an agent module, and a `prompt.jinja2` file, then register it with the orchestrator.

---

## Prompt Templates

Prompts are stored as Jinja2 templates (`prompt.jinja2`), one per agent. This keeps prompt text separate from Python logic, so you can tune behavior without changing code. Templates receive variables such as the user's request, the current plan, search results, and error output.

When editing a template, test with several models. Small changes in wording can noticeably change how an agent behaves.

---

## Sandboxed Code Execution

Generated code can contain bugs, unsafe commands, or malicious instructions, so Devika runs it in a sandbox:

- **Firejail** (`firejail.py`) restricts filesystem access, network access, and system calls.
- **The code runner** (`code_runner.py`) executes the code within the sandbox and captures output, errors, and exit codes.

**Important:** Sandboxing reduces risk but does not eliminate it. Do not run Devika with untrusted prompts on a machine that holds sensitive data. For stronger isolation, use the Docker setup.

---

## Knowledge Base and RAG

- **`knowledge_base.py`** stores information gathered during research and project work.
- **`rag.py`** retrieves the most relevant stored content for each prompt, so agents can use earlier findings without exceeding context limits.
- **`sentence.py`** and **`pdf.py`** help split and extract text from documents before storage.

---

## Real-Time Communication

The backend and frontend communicate over WebSockets. `socket_instance.py` sets up the server, and the frontend subscribes to events such as step updates, log messages, search results, and final responses. This is how the UI can display the agent's progress as it happens.

---

## Frontend

The frontend is a Svelte application built with Vite and styled with Tailwind CSS.

- **Routes:** `+layout.js`, `+layout.svelte`, and `+page.svelte` define the main pages.
- **Components:** Reusable UI pieces, such as the chat, plan view, and log panels, live in `components/`.
- **Assets:** Avatars, a favicon, a loading animation (`loading-lottie.json`), and a startup sound (`bootup.mp3`) are in `static/`.
- **Tooling:** `components.json` configures the component library, and `tailwind.config.js` and `postcss.config.cjs` control styling.

To run the frontend in development mode:

```bash
cd frontend
bun run dev
```

To build for production:

```bash
bun run build
```

---

## Development

### Setting up a development environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp sample.config.toml config.toml
```

### Running tests

If the project includes a test suite, run it with:

```bash
pytest
```

### Code organization tips

- Keep provider-specific logic inside its client file in `llm/`.
- Put tools that agents call into `services/`.
- Keep prompts in `prompt.jinja2` files rather than hard-coding them.
- Use `state.py` for anything that must persist across agent steps.

### Experimental modules

The `__UNIMPLEMENTED__` directory contains early-stage modules for domains such as game development, physics, math, medicine, chemistry, web design, and Stack Overflow search. These are not production-ready and are not wired into the main workflow. They are a good starting point for contributors.

---

## Benchmarks

`BENCHMARKS.md` and `SWE-bench.md` describe how Devika is evaluated. SWE-bench is a benchmark that measures how well an agent resolves real GitHub issues. Refer to those files for methodology, results, and reproduction steps.

---

## Documentation

| Document | Contents |
|---|---|
| `README.md` | Project overview and quick start |
| `ARCHITECTURE.md` | System design and component relationships |
| `UNDER_THE_HOOD.md` | Internal mechanics of the agent pipeline |
| `BENCHMARKS.md` | Performance evaluations |
| `SWE-bench.md` | SWE-bench evaluation details |
| `CONTRIBUTING.md` | How to contribute |
| `ROADMAP.md` | Planned features and priorities |
| `ollama.md` | Setting up Ollama with Devika |
| `search_engine.md` | Configuring search engines |

---

## Roadmap

Planned work is described in `ROADMAP.md`. Typical priorities for projects like this include stronger sandboxing, better error recovery, broader model support, improved long-horizon planning, and more deployment targets.

---

## Troubleshooting

**The backend starts, but the UI cannot connect.**
Confirm the backend is running on port 1337 and that the frontend is using the same address. Check the browser console for WebSocket errors.

**"Firejail not found" or sandbox errors.**
Install Firejail (`sudo apt install firejail` on Debian and Ubuntu). On Docker, confirm the container has the required capabilities.

**Ollama models are not listed.**
Make sure `ollama serve` is running and that the endpoint in `config.toml` matches (default `http://localhost:11434`).

**Search returns no results.**
Verify the Bing or Google API key and, for Google, the `GOOGLE_CX` value. Check your quota.

**Playwright or browser errors on Linux.**
Run `playwright install-deps` to install required system libraries.

**The agent loops or produces invalid output.**
Try a more capable model, or tune the relevant `prompt.jinja2` file. Local models often need simpler prompts.

**Docker containers exit immediately.**
Check the logs with `docker compose logs`. A missing or malformed `config.toml` is a common cause.

---

## Contributing

Contributions are welcome. To get started:

1. Read `CONTRIBUTING.md` and `ARCHITECTURE.md`.
2. Fork the repository and create a feature branch.
3. Make your changes and test them locally.
4. Open a pull request with a clear description of the change and its motivation.

Good first contributions include adding an LLM provider client, improving a prompt template, fixing bugs listed in the issue tracker, or completing one of the modules in `__UNIMPLEMENTED__`.

---

## License

This project is licensed under the terms in the `LICENSE` file in the repository root.

---

## Acknowledgments

Devika is inspired by Devin by Cognition AI. Thanks to the open-source projects that make it possible, including Svelte, Vite, Tailwind CSS, Playwright, Firejail, and the LLM providers and local runtimes it supports.

# Devika - AI Software Engineer

> **Devika is an agentic AI software engineer that can understand high-level human instructions, break them down into steps, research relevant information, and write code to accomplish the given objective.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Frontend-Svelte%20%7C%20Bun-orange" alt="Svelte">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

Devika aims to be a competitive open-source alternative to Devin by Cognition Labs — an AI assistant that plans, researches, codes, debugs, and deploys software projects from a single natural-language prompt.

---

## Table of Contents

- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Agent Pipeline](#agent-pipeline)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Docker Deployment](#docker-deployment)
- [LLM Provider Support](#llm-provider-support)
- [Search Engines](#search-engines)
- [Examples](#examples)
- [Benchmarks](#benchmarks)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Key Features

- 🤖 **Multi-LLM support** — Claude 3 (Anthropic), GPT-4 / GPT-3.5 (OpenAI), Gemini (Google), Groq, Mistral, LM Studio, and local models via **Ollama**
- 🧠 **Advanced planning and reasoning** — intelligent task decomposition into concrete, actionable steps
- 🔍 **Autonomous web research** — searches and extracts information from the web to ground its decisions
- 💻 **Multi-language code generation** — writes, patches, and rewrites code across programming languages
- 🏃 **In-process code execution** — runs generated code in a sandboxed (Firejail) environment
- 🩹 **Self-correction loop** — dedicated patcher and re-run agents that fix broken outputs and retry
- 📊 **Real-time state tracking** — live agent state visualization over WebSockets (Socket.IO)
- 💬 **Natural-language chat interface** — interact with Devika conversationally
- 🧾 **Rich artifacts** — generates PDF reports, UML diagrams (Mermaid/Graphviz), and formatted answers
- 🌐 **Deployment automation** — push to GitHub and deploy static sites to Netlify from the chat
- 🖥️ **Modern web UI** — SvelteKit + Tailwind frontend with animated avatars and boot-up sounds

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                         │
│            SvelteKit + Tailwind (Bun, port 5173)            │
└──────────────────────┬──────────────────────────────────────┘
                       │ Socket.IO (real-time events)
┌──────────────────────┴──────────────────────────────────────┐
│                      Backend Server                         │
│              devika.py (Flask + Socket.IO, :1337)           │
├─────────────────────────────────────────────────────────────┤
│                       Agent Core                            │
│   planner → researcher → coder → runner → feature → ...     │
├──────────────┬──────────────┬───────────────┬───────────────┤
│  LLM Layer   │   Research   │   Execution   │  Integrations │
│  openai      │   bing       │   code_runner │   git/github  │
│  claude      │   browser    │   firejail    │   netlify     │
│  gemini      │   sentence   │   pdf/uml     │   knowledge   │
│  groq        │              │   graphviz    │   base (RAG)  │
│  mistral     │              │               │               │
│  ollama      │              │               │               │
│  lm_studio   │              │               │               │
└──────────────┴──────────────┴───────────────┴───────────────┘
```

Devika consists of two main components:

1. **Backend** (`devika.py`) — a Python Flask + Socket.IO server that orchestrates agents, LLM calls, research, and code execution.
2. **Frontend** — a SvelteKit application that communicates with the backend in real time and renders the chat interface, project browser, and agent state.

---

## Agent Pipeline

Each agent lives in `src/agents/` with its own Jinja2 prompt template (`prompt.jinja2`):

| Agent | Role |
|---|---|
| `planner` | Decomposes the user's objective into a step-by-step plan |
| `internal_monologue` | Maintains a running "thought process" shown in the UI |
| `decision` | Decides the next action (execute, retry, finish) |
| `action` | Executes the chosen action |
| `researcher` | Performs web searches, scrapes, and ranks relevant information |
| `coder` | Writes the actual source code for the current step |
| `runner` | Executes code / project-level commands |
| `patcher` | Diagnoses failed runs and applies fixes |
| `feature` | Adds or modifies features in an existing codebase |
| `reporter` | Produces final summaries and reports |
| `formatter` | Formats output artifacts (PDF, UML, Graphviz) |
| `answer` | Composes the final natural-language answer to the user |

The top-level `agent.py` coordinates this pipeline, streaming progress and messages to the frontend via `socket_instance.py`.

---

## Tech Stack

**Backend**
- Python 3.10+, Flask, Flask-SocketIO
- Playwright (headless browser automation)
- LlamaIndex / RAG for the knowledge base
- Firejail sandbox for safe code execution
- Jinja2 templating for agent prompts

**Frontend**
- SvelteKit, Svelte
- Tailwind CSS + PostCSS
- Bun (package manager & runtime)
- Vite
- Lottie animations (`loading-lottie.json`)

**Integrations**
- Git / GitHub CLI
- Netlify CLI
- Mermaid / Graphviz for diagram generation

---

## Project Structure

```
devika/
├── devika.py                  # Backend entry point
├── requirements.txt           # Python dependencies
├── setup.sh                   # One-shot environment setup
├── sample.config.toml         # Template configuration file
├── config.toml                # Your local config (API keys, toggles)
├── Makefile                   # Common dev commands
├── docker-compose.yaml        # Full-stack Docker deployment
├── app.dockerfile             # Frontend container image
├── devika.dockerfile          # Backend container image
│
├── src/
│   ├── agents/                # Agent implementations + prompt templates
│   │   ├── agent.py           # Orchestrator
│   │   ├── planner/, coder/, researcher/, runner/, ...
│   │   └── <agent>/prompt.jinja2
│   ├── llm/                   # LLM provider clients
│   │   ├── llm.py             # Unified LLM interface
│   │   ├── claude_client.py
│   │   ├── openai_client.py
│   │   ├── gemini_client.py
│   │   ├── groq_client.py
│   │   ├── mistral_client.py
│   │   ├── ollama_client.py
│   │   └── lm_studio_client.py
│   ├── browser/               # Headless browsing & scraping
│   ├── search/                # Search engine integration
│   ├── knowledge_base/        # Vector store / RAG
│   ├── rag.py
│   ├── config.py              # Config loader
│   ├── state.py               # Agent state management
│   ├── socket_instance.py     # Socket.IO server instance
│   ├── project.py             # Project/workspace management
│   ├── code_runner.py         # Executes generated code
│   ├── firejail.py            # Sandbox wrapper
│   ├── pdf.py, uml.py, graphwiz.py
│   ├── git.py, github.py, netlify.py
│   ├── logger.py, utils.py
│   └── init.py
│
├── src/webui/                 # SvelteKit frontend
│   ├── src/routes/+page.svelte, +layout.svelte
│   ├── static/                # avatars, favicon, bootup.mp3, lottie
│   ├── package.json
│   ├── svelte.config.js
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── examples/                  # Domain example scripts
    ├── game-dev.py
    ├── physics.py
    ├── web-design.py
    ├── stackoverflow.py
    ├── math.py
    ├── medical.py
    └── chemistry.py
```

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Bun** (frontend runtime & package manager)
- **Git**
- A **Bing Search API key** and at least one LLM API key
- (Linux) `firejail` for sandboxed execution
- (Recommended) `uv` or `pip` for dependency management

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<owner>/devika-ut2fblq4.git
   cd devika-ut2fblq4
   ```

2. **Set up the backend**

   ```bash
   cd src/backend

   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate        # Linux / macOS
   # .\venv\Scripts\activate       # Windows
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Or with `uv`:

   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

4. **Install Playwright browsers**

   ```bash
   playwright install
   playwright install-deps        # Linux only
   ```

   > This step requires elevated permissions (`sudo`) on some Linux distributions.

5. **Configure API keys** (see [Configuration](#configuration))

   ```bash
   cp sample.config.toml config.toml
   # edit config.toml with your keys
   ```

6. **Start the backend server**

   ```bash
   python devika.py
   ```

   The API and Socket.IO server will run at `http://127.0.0.1:1337`.

7. **Set up and run the frontend**

   ```bash
   cd src/webui
   bun install
   bun run dev
   ```

8. **Open Devika**

   Navigate to `http://127.0.0.1:5173` in your browser.

---

## Configuration

Devika reads its settings from `config.toml` (see `sample.config.toml` for the template):

```toml
[API_KEYS]
OPENAI = "sk-..."
CLAUDE = "sk-ant-..."
GEMINI = "..."
GROQ = "..."
MISTRAL = "..."
BING = "..."          # Search
GOOGLE_SEARCH = "..." # Alternative search
GITHUB = "ghp-..."
NETLIFY = "..."

[LLM]
CLAUDE = false
OPENAI = true
GEMINI = false
GROQ = false
MISTRAL = false
OLLAMA = false
LM_STUDIO = false

[API_ENDPOINTS]
OLLAMA = "http://localhost:11434"
LM_STUDIO = "http://localhost:1234/v1"
```

Key notes:

- **At least one LLM provider must be enabled**, and its API key must be present (local providers like Ollama / LM Studio only need an endpoint URL).
- The **Bing Search API key is required** for web research. See [`search_engine.md`](search_engine.md) for details.
- For local models, see [`ollama.md`](ollama.md).

---

## Docker Deployment

Run the full stack (frontend + backend) with Docker Compose:

```bash
docker compose up
```

- `devika.dockerfile` builds the backend image.
- `app.dockerfile` builds the frontend image.
- Mount or bake your `config.toml` into the backend container.

Alternatively, build images individually:

```bash
docker build -t devika-backend -f devika.dockerfile .
docker build -t devika-frontend -f app.dockerfile .
```

---

## LLM Provider Support

| Provider | Module | Notes |
|---|---|---|
| Anthropic (Claude 3) | `claude_client.py` | Recommended default |
| OpenAI (GPT-4 / GPT-3.5) | `openai_client.py` | |
| Google (Gemini) | `gemini_client.py` | |
| Groq | `groq_client.py` | Extremely fast inference |
| Mistral | `mistral_client.py` | |
| Ollama | `ollama_client.py` | Local models (`ollama.md`) |
| LM Studio | `lm_studio_client.py` | Local OpenAI-compatible server |

All clients implement a common interface exposed through `llm.py`, so switching providers is a one-line config change.

---

## Search Engines

Devika currently uses the **Bing Search API** as its primary research backend. Refer to [`search_engine.md`](search_engine.md) for how to obtain a key and plug it into `config.toml`.

---

## Examples

The `examples/` directory contains prompts and showcases demonstrating Devika in different domains:

- **game-dev.py** — build a playable browser game
- **physics.py** — physics simulations and visualizations
- **web-design.py** — full landing pages and UI layouts
- **stackoverflow.py** — answer real-world programming questions
- **math.py**, **medical.py**, **chemistry.py** — domain-specific problem solving

> Some examples are marked `__UNIMPLEMENTED__` and serve as roadmap targets for future agent capabilities.

---

## Benchmarks

Devika is evaluated against real-world software engineering tasks. See:

- [`SWE-bench.md`](SWE-bench.md) — results and methodology on the SWE-bench suite
- [`BENCHMARKS.md`](BENCHMARKS.md) — internal benchmark suite and comparisons

---

## Roadmap

See [`ROADMAP.md`](ROADMAP.md) for the full list. Highlights include:

- Expanded search engine backends (Google, Searx, etc.)
- Persistent long-term memory across projects
- Multi-agent collaboration
- IDE plugin integration
- One-click deployment targets beyond Netlify

---

## Documentation

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — deep dive into system design
- [`UNDER_THE_HOOD.md`](UNDER_THE_HOOD.md) — how the agent loop, prompts, and execution sandbox work
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to contribute code, docs, or prompts

---

## Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Areas especially in need of help: new LLM clients, alternative search backends, sandbox hardening, and frontend UX.

---

## License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

> ⚠️ **Note**: Devika executes AI-generated code. Always use it in a controlled environment, keep the Firejail sandbox enabled, and never expose the backend directly to the public internet.

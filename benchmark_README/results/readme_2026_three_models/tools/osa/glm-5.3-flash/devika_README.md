# devika-41d__q9x

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![anthropic](https://img.shields.io/badge/Anthropic-191919.svg?style=flat&logo=Anthropic&logoColor=white)
![flask](https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white)
![google-generativeai](https://img.shields.io/badge/Google%20Gemini-8E75B2.svg?style=flat&logo=Google-Gemini&logoColor=white)
![jinja2](https://img.shields.io/badge/Jinja-B41717.svg?style=flat&logo=Jinja&logoColor=white)
![markdown](https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white)
![openai](https://img.shields.io/badge/OpenAI-412991.svg?style=flat&logo=OpenAI&logoColor=white)
![playwright](https://img.shields.io/badge/Playwright-2EAD33.svg?style=flat&logo=Playwright&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Example](#example)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project is an AI-powered software assistant that decomposes high-level user prompts into plans, performs web research, generates code, and can run or deploy the resulting projects through an orchestrated set of specialized agents. It is aimed at developers, AI researchers, and data scientists who want to build on or study agentic task-execution systems. The system exposes a web-based interface backed by a Python server with REST and WebSocket endpoints, supports multiple LLM providers, and includes flows for planning, research, coding, execution, and PDF reporting. See Getting Started for runnable setup and first-use steps.

---

## Core Features

- **Multi-agent task execution**: A modular pipeline of specialized agents (planning, research, coding, answering, running, patching, and reporting) breaks user prompts into plans, gathers information, and generates code, so developers can hand off a goal and get actionable output.

- **Web research with configurable search engines**: Built-in search integration (Bing, Google, DuckDuckGo) with automated browsing, page reading, and screenshot capture lets agents ground their plans and code in up-to-date online information.

- **Multi-provider LLM support**: Pluggable backends for Claude, OpenAI, Google Gemini, Mistral, Groq, Ollama, and LM Studio let developers choose hosted or local models without changing application code.

- **Real-time agent monitoring**: A Socket.IO-driven UI streams agent state, screenshots, terminal sessions, logs, and token usage live, so developers can follow and debug each run as it happens.

- **Project-based session management**: Persistent per-project state (messages, agent status, generated code) allows resuming and continuing tasks across interactions, with deployment support for finished projects.

---

## Installation

Install devika-41d__q9x using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/devika-41d__q9x
```

2. Install the backend project dependencies:

```sh
pip install -r requirements.txt
```

**Using Docker:**

1. From the repository root, start the Docker-based deployment:

```sh
docker-compose up --build
```

Refer to the Docker configuration files in the repository for the exact services and ports exposed by the deployment.

**Frontend (Svelte/Tailwind UI):**

The web UI is a separate Svelte/Tailwind application in `ui/` and must be installed and served for the system to be usable:

1. Move to the frontend directory and install its dependencies:

```sh
cd ui
npm install
```

2. Start the frontend dev server:

```sh
npm run dev
```

The UI runs at `http://localhost:3000`. See `ui/package.json` for the exact scripts and package manager supported by this checkout.

---

## Getting Started

## Prerequisites

- Python with the project dependencies installed (see the Installation docs).
- A Svelte/Tailwind frontend served locally (Devika's UI runs at `http://localhost:3000`; see the frontend steps under Installation).
- API keys for at least one supported LLM provider, configured in `config.toml` (root directory) or via the UI.
- A search engine: DuckDuckGo works without keys; Bing or Google require API keys and endpoints (see `docs/Installation/search_engine.md`).
- Optional: [Ollama](https://ollama.com) for running local open-source models (see `docs/Installation/ollama.md`). Ollama's default address is `http://localhost:11434` and is auto-detected by Devika; if you serve it elsewhere, update `config.toml`.

## Quickstart

1. Configure your LLM provider keys and search engine credentials in `config.toml` (or set them via the UI after launch).

2. Start the backend server:

```bash
   python devika.py
```

   The Flask/SocketIO server listens on `0.0.0.0:1337`. On startup, `init_devika()` creates the required directories (SQLite DB, screenshots, PDFs, projects, logs) and loads the sentence-transformer BERT model.

3. Open the web UI at `http://localhost:3000`.

4. In the UI, create a project, select a base model and a search engine, then send your first message. Devika's agent will plan, research, and generate code for your request, with progress shown in real time via the socket-connected interface.

---

## Example

A typical end-to-end run after completing the Quickstart:

1. In the UI, create a new project (for example, `todo-api`).
2. Select a base model (e.g., a Claude or OpenAI model) and a search engine (e.g., DuckDuckGo).
3. Send a prompt such as: "Build a simple Python REST API for managing a to-do list."
4. Follow the agents as they work: the Planner decomposes the request, the Researcher gathers relevant information from the web, and the Coder generates the implementation — with agent state, screenshots, and logs streamed to the UI in real time.
5. Review and edit the generated code in the UI's editor, run it via the execution flow, and, when finished, publish it using the built-in Git, GitHub, and Netlify deployment integrations.

---

## Architecture

Devika follows a client–server agent architecture. A Flask backend (`devika.py`) exposes REST APIs and SocketIO channels for real-time communication, while a Svelte/Tailwind frontend (`ui/`) renders the chat, editor, terminal, and browser widgets and talks to the backend over HTTP and WebSockets (`ui/src/lib/sockets.js`, `ui/src/lib/api.js`).

- **Agent orchestration (`src/agents/`)**: A central `Agent` class coordinates specialized agents — Planner, Researcher, Formatter, Coder, Runner, Patcher, Feature, Action, Internal Monologue, Answer, Reporter, and Decision — each implemented as a module with its own Jinja2 prompt template. User messages arrive via SocketIO, and each request is executed in a background thread, tracking state through `AgentState`.
- **LLM abstraction (`src/llm/`)**: A unified `LLM` interface routes inference to provider clients (Claude, OpenAI, Gemini, Mistral, Groq, Ollama, LM Studio), tracks token usage with `tiktoken`, and streams updates to the UI.
- **Supporting subsystems**: `src/browser/` handles web search (Bing, Google, DuckDuckGo) and page interaction with screenshots; `src/memory/` provides a knowledge base with RAG and BERT-based keyword extraction (`src/bert/`); `src/filesystem/` reads project code; `src/sandbox/` runs code (including a Firejail option); and `src/services/` integrates Git, GitHub, and Netlify deployment.
- **Project and state management**: `ProjectManager` (`src/project.py`) persists per-project messages and files, while `AgentState` (`src/state.py`) tracks active/completed agent runs and token usage; `src/apis/project.py` exposes project-management endpoints as a Flask blueprint.

More detailed architecture notes are available in `docs/architecture/` (including `ARCHITECTURE.md` and `UNDER_THE_HOOD.md`).

---

## Documentation

A detailed devika-41d__q9x description is available [here](./docs). Key subtopics referenced in this README:

- **Architecture**: `docs/architecture/ARCHITECTURE.md` and `docs/architecture/UNDER_THE_HOOD.md` — how the agents, backend, and frontend fit together.
- **Search engine setup**: `docs/Installation/search_engine.md` — configuring Bing, Google, or DuckDuckGo.
- **Ollama setup**: `docs/Installation/ollama.md` — running local open-source models.

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to devika-41d__q9x.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

<!-- TODO: Replace the placeholders below (authors, year, and REPOSITORY_URL) with the real project attribution and the canonical repository URL before publishing the citation. -->

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    TODO: Project Authors. (TODO: Year). devika-41d__q9x repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{devika-41d__q9x,

        author = {TODO: Project Authors},

        title = {devika-41d__q9x repository},

        year = {TODO: Year},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
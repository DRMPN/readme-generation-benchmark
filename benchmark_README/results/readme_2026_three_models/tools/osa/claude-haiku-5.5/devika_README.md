# devika-ib3k3ay5

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![anthropic](https://img.shields.io/badge/Anthropic-191919.svg?style={0}&logo=Anthropic&logoColor=white)
![flask](https://img.shields.io/badge/Flask-000000.svg?style={0}&logo=Flask&logoColor=white)
![google-generativeai](https://img.shields.io/badge/Google%20Gemini-8E75B2.svg?style={0}&logo=Google-Gemini&logoColor=white)
![jinja2](https://img.shields.io/badge/Jinja-B41717.svg?style={0}&logo=Jinja&logoColor=white)
![markdown](https://img.shields.io/badge/Markdown-000000.svg?style={0}&logo=Markdown&logoColor=white)
![openai](https://img.shields.io/badge/OpenAI-412991.svg?style={0}&logo=OpenAI&logoColor=white)
![playwright](https://img.shields.io/badge/Playwright-2EAD33.svg?style={0}&logo=Playwright&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Devika is an autonomous AI software-engineering agent that takes a natural-language request and coordinates role-specific agents, such as planning, research, coding, running, and reporting, to work on a software project. It is intended for developers and researchers who are experimenting with autonomous coding agents, and it assumes familiarity with LLM provider setup and local development tooling. The repository provides a Python backend that exposes REST and Socket.IO interfaces, paired with a separate web user interface for interacting with projects and agent activity. For runnable setup and launch steps, see Getting Started.

---

## Core Features

- **Autonomous coding workflow:** Coordinates specialized agents for planning, research, coding, running, patching, and reporting. Developers can describe a task in natural language and get a working project without manually orchestrating each step.
- **Multi-provider LLM support:** Works with multiple LLM providers, including local runtimes such as Ollama and LM Studio. Teams can choose hosted or self-hosted models without changing the rest of the workflow.
- **Web search and page reading:** Gathers context for coding tasks by searching the web and extracting page content. Agents can use current external information when building a project.
- **Persistent per-project state:** Stores conversation history and agent state for each project. Developers can continue work on an existing project across multiple messages without losing context.
- **Live web UI:** Provides a browser interface that receives real-time updates from the backend over sockets. Developers can monitor agent progress and logs while tasks run.

---

## Installation

Install devika-ib3k3ay5 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/devika-ib3k3ay5
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

### Prerequisites

- Python (version not specified in the provided context)
- An LLM provider: a local runtime such as Ollama (see `docs/Installation/ollama.md`) or an API key for a supported provider set in `config.toml`
- Dependencies as described in the [Installation](#installation) section

### Quickstart

1. **Install dependencies.** Follow the [Installation](#installation) section.

2. **Start the backend.** From the repository root:

```bash
   python devika.py
```

   `devika.py` runs the Flask/Socket.IO server. Check the `__main__` block in `devika.py` for the host and port it binds to.

3. **Review the configuration.** On first run, `config.toml` is created from `sample.config.toml` if it does not exist. Set LLM endpoints and API keys in the `API_ENDPOINTS` and `API_KEYS` sections of `config.toml`.

4. **Set up the frontend.** The web UI lives in `ui/` and is built with Bun (`ui/bun.lockb` is present). Check the scripts defined in the project files under `ui/` for the exact install and run commands.

5. **Optional: run with Docker.** Container setup is defined in `devika.dockerfile`, `app.dockerfile`, and `docker-compose.yaml`. Review these files before use.

---

## Architecture

Devika is a client-server application with a Python backend and a separate Svelte single-page UI.

- **Backend server (`devika.py`)**: A Flask app with Flask-SocketIO. It exposes REST endpoints such as `/api/data`, `/api/settings`, and `/api/get-agent-state`, and socket events such as `socket_connect` and `user-message`. Server-to-client messages are sent through `emit_agent` in `src/socket_instance.py`.
- **Frontend (`ui/`)**: A Svelte app. `ui/src/lib/api.js` and `ui/src/lib/sockets.js` handle REST and socket communication with the backend. Components include message, browser, editor, and terminal widgets.
- **Agent orchestration (`src/agents/agent.py`)**: The `Agent` class instantiates role agents (planner, researcher, coder, runner, patcher, reporter, and others). The `user-message` socket handler in `devika.py` creates an `Agent` and calls either `execute` or `subsequent_execute`, depending on the stored agent state for the project.
- **Model access (`src/llm/`)**: Provider clients for Claude, Gemini, Groq, Mistral, Ollama, OpenAI, and LM Studio. The base model is passed to each role agent.
- **Project and state storage**: `src/project.py` stores per-project message histories in SQLite through SQLModel. `src/state.py` holds agent state, which the REST endpoints query. Configuration is loaded by `src/config.py` from `config.toml`, which is generated from `sample.config.toml`.
- **Tooling and external services**: Browser automation (`src/browser`), search engine integrations (`src/browser/search.py`), a Firejail sandbox wrapper (`src/sandbox/firejail.py`), and Git, GitHub, and Netlify services (`src/services`).

**Primary flow:** The UI sends a `user-message` over the socket. The backend routes it to the `Agent`, which invokes role agents that call LLM clients and tools. Results are stored through `ProjectManager` and sent back to the UI via `emit_agent`. The UI also queries agent state and project data through REST endpoints.

### Limitations

- `/api/run-code` is a stub. It returns a success message without executing code.
- The `git_clone` branch in `Agent.make_decision` has no implementation.
- Modules under `src/experts` are marked `__UNIMPLEMENTED__` and are mostly placeholders.
- The provided context does not fully document component boundaries. See `docs/architecture/` for more detail.

---

## Documentation

A detailed devika-ib3k3ay5 description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to devika-ib3k3ay5.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). devika-ib3k3ay5 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{devika-ib3k3ay5,

        author = {README Benchmark},

        title = {devika-ib3k3ay5 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
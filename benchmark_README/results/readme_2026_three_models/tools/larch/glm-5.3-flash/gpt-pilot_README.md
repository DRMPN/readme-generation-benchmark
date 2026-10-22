# GPT Pilot

[![License](https://img.shields.io/badge/license-AGPL%20v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-green.svg)](https://www.python.org/)

**GPT Pilot** is an open-source AI development agent that aims to write *fully working, scalable applications* while a human developer supervises the process. Unlike tools that autocomplete code or generate one-off scripts, GPT Pilot works like a virtual developer: it creates a specification, breaks it down into tasks, codes each task, debugs its own work, and asks you for help only when it gets stuck.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Supported LLM Providers](#supported-llm-providers)
- [The Agent Workflow](#the-agent-workflow)
- [Project Structure](#project-structure)
- [Docker Support](#docker-support)
- [Running Tests](#running-tests)
- [Telemetry](#telemetry)
- [Database Migrations](#database-migrations)
- [Extending GPT Pilot](#extending-gpt-pilot)
- [Contributing](#contributing)
- [License](#license)

---

## How It Works

GPT Pilot mimics the workflow of a real software development team. Given a high-level app description, it:

1. **Clarifies the requirements** — asks you questions until it fully understands what you want to build.
2. **Generates a specification** — writes a detailed, step-by-step technical specification (produced by the **Spec Writer** agent).
3. **Designs the architecture** — the **Architect** agent chooses the technologies, project type, and scaffolding templates.
4. **Breaks down the work** — the **Tech Lead** agent splits the spec into development tasks, and each task into concrete, code-level steps.
5. **Implements step by step** — the **Developer** agent writes the code for each step; the **Code Monkey** performs routine, well-defined file edits.
6. **Runs and debugs** — the **Troubleshooter** executes the app, analyzes logs and errors, and the **Bug Hunter** reproduces and fixes bugs.
7. **Reviews changes** — every task is reviewed against the specification before being marked complete (**Task Completer**, review prompts).
8. **Keeps you in the loop** — whenever the agent needs a decision, credentials, or human intervention, it pauses and asks via the **Human Input** handler.

All state is persisted in a database, so you can stop and resume the project at any time.

---

## Key Features

- **End-to-end app development** — from a one-line description to a running application.
- **Human-in-the-loop** — you review and approve at every critical step; the agent never proceeds blindly.
- **Scalable context management** — a **Virtual File System (VFS)**, file importance filtering (`filter_files` prompts), and RAG-style external documentation search keep LLM context small even on large codebases.
- **Self-debugging** — the agent analyzes runtime errors, reproduction steps, and logs (`bug_hunter.py`, `troubleshooter.py`), and iterates until the app works.
- **Project templates** — ready-made scaffolds for popular stacks (see [Templates](#project-templates)).
- **Multiple LLM providers** — OpenAI, Azure OpenAI, Anthropic, and Groq are supported out of the box.
- **Git integration** — the agent commits its work (`git.py`) so you can always roll back.
- **Docker support** — run everything in a container with `Dockerfile`, `entrypoint.sh`, and `setup-dependencies.sh`.

---

## Installation

### Prerequisites

- Python **3.9+**
- Git
- An API key for at least one supported LLM provider
- Node.js (required for the web/frontend project templates)

### Install from source

```bash
git clone https://github.com/YourOrg/gpt-pilot-a_w7z_92.git
cd gpt-pilot-a_w7z_92

# Install dependencies
bash setup-dependencies.sh

# or manually:
pip install -e .
```

### Docker

```bash
docker build -t gpt-pilot .
docker run -it \
  -e OPENAI_API_KEY=sk-... \
  -v $(pwd)/your-app:/app/projects/your-app \
  gpt-pilot
```

---

## Quick Start

Create a new app from the command line:

```bash
python main.py create "A task manager app where users can register, log in, and manage their daily to-do lists"
```

Continue working on an existing project:

```bash
python main.py --project <project-name> continue
```

Other useful commands:

```bash
python main.py --help          # list all commands
```

GPT Pilot will guide you interactively: it will ask for a project name, ask clarifying questions, present the spec for your review, and then start building. At each task, you can:

- approve and continue,
- provide feedback,
- manually edit the code and tell the agent to proceed.

---

## Configuration

GPT Pilot is configured through JSON files and environment variables.

| File | Purpose |
|------|---------|
| `example-config.json` | Reference configuration showing all available options |
| `config-docker.json` | Defaults used when running inside Docker |
| `settings.json` | Local runtime settings |

Copy the example config to start:

```bash
cp example-config.json config.json
```

Key configuration areas:

- **LLM settings** — model name, temperature, max tokens, endpoint, and API key per provider.
- **Telemetry** — opt-in/out anonymous usage reporting (see `TELEMETRY.md`).
- **Limits** — max step iterations, max output tokens, debug loop limits.

Sensitive values (API keys) should be set as **environment variables** rather than in files:

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-...
export GROQ_API_KEY=gsk_...
export AZURE_OPENAI_API_KEY=...
```

---

## Supported LLM Providers

Provider clients live in `pilot/llm/`:

| Provider | Client file | Notes |
|----------|-------------|-------|
| OpenAI | `openai_client.py` | GPT-4 / GPT-4o family recommended |
| Azure OpenAI | `azure_client.py` | Uses your Azure deployment |
| Anthropic | `anthropic_client.py` | Claude models |
| Groq | `groq_client.py` | Fast open models (Llama, Mixtral, …) |
| Relace / OpenRouter-style routing | `relace_client.py` | Model routing/fallback |

All clients share the same interface (`base.py`), implement retry/rate-limit logic, and log every request/response pair to `request_log.py` for debugging and cost tracking.

---

## The Agent Workflow

GPT Pilot is built around a set of specialized agents (`pilot/agents/`), each with its own prompt set (`pilot/prompts/`):

### Agents

| Agent | File | Responsibility |
|-------|------|----------------|
| **Product Owner / Wizard** | `wizard.py` | Onboarding, project creation, clarifying questions (`ask_questions.prompt`, `project_name.prompt`) |
| **Spec Writer** | `spec_writer.py` | Builds the full technical specification (`build_full_specification.prompt`, `add_to_specification.prompt`) |
| **Architect** | `architect.py` | Chooses technologies and environment (`technologies.prompt`, `system.prompt`) |
| **Development Planner** | `breakdown.prompt` | Splits the spec into tasks and user stories |
| **Tech Lead** | `tech_lead.py` | Breaks tasks into development steps, reviews code (`parse_task.prompt`, `review_changes.prompt`) |
| **Developer** | `developer.py` | Writes the actual code for each step (`implement_changes.prompt`, `coding_rules.prompt`) |
| **Code Monkey** | `code_monkey.py` | Executes precise, mechanical code changes |
| **Code Monkey / Frontend** | `frontend.py` | Handles frontend-specific implementation (`build_frontend.prompt`, `iterate_frontend.prompt`) |
| **Troubleshooter** | `troubleshooter.py` | Runs the app, diagnoses problems (`get_run_command.prompt`, `analyze_project.prompt`) |
| **Bug Hunter** | `bug_hunter.py` | Reproduces bugs and fixes them (`get_bug_reproduction_instructions.prompt`, `bug_found_or_add_logs.prompt`) |
| **Task Completer** | `task_completer.py` | Marks tasks/steps complete, tracks iteration limits |
| **Legacy / Import Handler** | `legacy_handler.py`, `importer.py`, `v0importer.py` | Imports existing projects (including v0.dev exports) into GPT Pilot |
| **Technical Writer** | `tech_writer.py` | Generates README/docs (`create_readme.prompt`, `create_docs_queries.prompt`) |
| **External Docs** | `external_docs.py` | Searches external documentation and injects relevant snippets (`select_docset.prompt`, `doc_snippets.prompt`) |
| **Human Input** | `human_input.py` | Manages all human-in-the-loop interactions |
| **Convo / Mixins** | `convo.py`, `mixins.py` | Shared conversation management for all agents |
| **Error Handler** | `error_handler.py` | Handles agent errors and recovery (`get_alternative_solutions.prompt`) |

### Conversation engine

Every agent communicates with the LLM through a structured **conversation** model (`pilot/llm/` + `convo.py`): messages are appended, tool outputs are recorded, and the full history can be persisted and replayed.

---

## Project Structure

```
gpt-pilot-a_w7z_92/
├── main.py                    # CLI entry point
├── pyproject.toml             # Python package definition
├── Dockerfile                 # Container build
├── setup-dependencies.sh      # Dependency installer script
├── entrypoint.sh              # Docker entrypoint
├── config-docker.json         # Docker default configuration
├── example-config.json        # Reference configuration
├── TELEMETRY.md               # Telemetry documentation
│
├── pilot/                     # Core application
│   ├── const/                 # Constants and magic words (magic_words.py, actions.py)
│   ├── helpers/               # Helpers: process management, env importing,
│   │                          #   git, exec logging, user settings, project setup
│   ├── llm/                   # LLM clients (openai, azure, anthropic, groq, relace)
│   │                          #   and prompt/response/request plumbing (prompt.py,
│   │                          #   response.py, convo.py, request_log.py)
│   ├── agents/                # All agents described above
│   ├── prompts/               # One folder per agent, each with its .prompt files
│   ├── project/               # Project DB models: project, file, file_content,
│   │                          #   specification, knowledge_base, branch,
│   │                          #   chat_message, chat_convo, exec_log, user_input,
│   │                          #   llm_request, project_state, session, setup
│   ├── db/                    # Database layer and Alembic migrations
│   ├── extensions/            # Extension point + on-event hooks
│   │                          #   (e.g. on-event-extension-install.sh)
│   ├── telemetry/             # Anonymous usage telemetry
│   ├── api/                   # API server + IPC client/console/virtual transport
│   └── vfs/                   # Virtual file system and ignore rules (vfs.py, ignore.py)
│
├── templates/                 # Project scaffolding templates
│   ├── base.py / registry.py  # Template registry and common logic
│   ├── vite_react.py, react_express.py, node_express_mongoose.py,
│   ├── javascript_react.py, vite_react_swagger.py
│   └── (full-stack template assets: React+Vite frontends, Express/Node
│        backends with auth, Prisma/Mongoose models, shadcn/ui components…)
│
└── tests/                     # Unit and integration tests (pytest)
```

---

## Project Templates

GPT Pilot ships with ready-made scaffolds so it doesn't have to build boilerplate from scratch. Templates are registered in `templates/registry.py` and selected automatically by the Architect agent (`select_templates.prompt`, `configure_template.prompt`).

Included stacks (non-exhaustive):

- **Vite + React + TypeScript** — modern SPA with shadcn/ui component library, Tailwind CSS, ESLint, auth pages (Login/Register), protected routing, toast/dialog/sidebar components.
- **React + Express (JS)** — full-stack JavaScript with REST API, auth middleware, MongoDB/Mongoose models, JWT auth.
- **Node + Express + Mongoose** — backend service template with users, auth, mail, and logging.
- **Vite + React + Swagger** — API-first template with generated client types.
- **Prisma-based Node backend** — `schema.prisma` with user management and auth.

Each template includes a post-scaffold hook (`add_raw_tags.py`, `render.py`) that fills in project-specific values (names, package IDs, etc.).

---

## Database & Migrations

Project state (files, specification, tasks, conversations, branches, knowledge base, execution logs, LLM requests) is stored in a local database using **SQLAlchemy** and managed with **Alembic**.

- `alembic.ini` — Alembic configuration
- `script.py.mako` — migration template
- Migration files include history such as:
  - `0a1bb637fa26_initial.py`
  - `675268601278_add_chat_messages_and_convos.py`
  - `69e50fdaf067_move_knowledge_base_to_separate_table.py`
  - `0173e14719aa_move_metadata_from_file_to_file_content_.py`
  - `b760f66138c0_add_docs_column_to_project_states.py`
  - `3968d770dced_add_project_type_to_project.py`
  - and others

To apply migrations manually:

```bash
alembic upgrade head
```

---

## Running Tests

The project has an extensive pytest test suite covering every layer:

```bash
pytest
```

Test areas include:

- LLM clients (`test_openai.py`, `test_anthropic.py`, `test_groq.py`)
- Prompt/response parsing (`test_prompt.py`, `test_parser.py`)
- Agents (`test_tech_lead.py`, `test_orchestrator.py`, `test_base.py`)
- Project & state (`test_project.py`, `test_project_state.py`, `test_state_manager.py`)
- Database (`test_db.py`), VFS (`test_vfs.py`, `test_ignore.py`)
- Helpers (`test_process_manager.py`, `test_env_importer.py`, `test_config.py`, `test_version.py`)
- IPC & console (`test_ipc_client.py`, `test_console.py`)
- Templates (`test_templates.py`) and telemetry (`test_telemetry.py`)

Shared fixtures live in `tests/factories.py` and `tests/conftest.py`.

---

## Telemetry

GPT Pilot collects **optional, anonymous** telemetry (agent steps, LLM model usage, error types) to help improve the tool. No source code, prompts, or user data are collected.

- See **`TELEMETRY.md`** for exactly what is recorded.
- Telemetry can be disabled in `config.json`:

```json
{ "telemetry": false }
```

---

## Extending GPT Pilot

### Extensions

The `pilot/extensions/` package defines an event-based extension system. Extensions can hook into the agent lifecycle (e.g., after a task completes, before an LLM request). The `on-event-extension-install.sh` script shows how extension installation events are handled.

### IPC & API

GPT Pilot can run in a **server mode** (`pilot/api/api_server.py`) where a frontend (such as the Pythagora VS Code extension or web UI) drives the agents over an IPC channel (`ipc_client.py`, `console.py`, `virtual.py`). This is how the same agent core powers both the CLI and the GUI experience.

### Custom prompts

All agent behavior is defined in `.prompt` files under `pilot/prompts/`. Each file supports Jinja-style templating (see `script.py.mako` conventions and `prompt.py` for the loader). You can:

- tweak existing prompts,
- add new prompt files and reference them from agents,
- fork the whole prompting layer for your own workflow.

---

## Contributing

Contributions are welcome!

1. Fork the repository and create a feature branch.
2. Make your changes and add/adjust tests.
3. Run the full test suite:

   ```bash
   pytest
   ```

4. Update documentation (`README.md`, `TELEMETRY.md`, prompt docs) if behavior changes.
5. Open a pull request with a clear description of the change.

Please keep bug reports detailed: include the project description, the task the agent was working on, the relevant logs (`exec_log`, `request_log`), and the model you used.

---

## License

This project is licensed under the terms found in the [LICENSE](LICENSE) file (GNU AGPL v3).

---

> **Note:** GPT Pilot is designed to be *supervised* by a developer. Review the code it produces, test the app, and use Git branches (`pilot/helpers/git.py`) to stay in control. The agent is powerful, but you are the team lead. 🚀

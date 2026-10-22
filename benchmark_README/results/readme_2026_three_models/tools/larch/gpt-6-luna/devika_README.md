# Devika

Devika is an open-source AI software-engineering agent. It can take a natural-language task, research the problem, plan an approach, work with a project’s code, run commands, and report its progress and results.

This repository contains Devika’s Python agent and backend, a Svelte web interface, model-provider clients, browser and search integrations, and optional Docker setup.

> **Important:** Devika can modify files and execute commands. Run it only in a project and environment you trust, and review generated changes before using them.

## Contents

- [Features](#features)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running Devika](#running-devika)
- [Using Devika](#using-devika)
- [Docker](#docker)
- [Project structure](#project-structure)
- [Security and limitations](#security-and-limitations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Task planning and execution:** turns a request into a plan and works through it using specialized agent components.
- **Code assistance:** reads and edits project files, runs code, and can attempt to repair errors.
- **Research:** uses search and browser-related tools to gather information.
- **Multiple model providers:** includes clients for OpenAI, Groq, LM Studio, Ollama, Google Gemini, Mistral, and Anthropic Claude. Availability depends on your configuration and credentials.
- **Project context:** includes a knowledge base and retrieval-augmented generation (RAG) components for working with project information.
- **Progress reporting:** provides agent status, internal reasoning summaries, and task reports through the application.
- **Integrations and utilities:** includes modules for GitHub, Netlify, PDF handling, UML generation, logging, and more. Some integrations may require additional local tools or configuration.

## How it works

At a high level, Devika:

1. Receives a task and the selected project context.
2. Plans the work and identifies relevant research or coding steps.
3. Uses its configured language model and available tools to carry out those steps.
4. Runs or inspects code as appropriate, and may revise its work after errors.
5. Reports the outcome through the application interface.

The Python code contains the agent, model clients, browser and search tools, project utilities, and task-specific components. The web application is built with Svelte and Vite.

## Requirements

The exact requirements depend on your operating system and the integrations you use. In general, you will need:

- Python 3 and the packages listed in `requirements.txt`
- A configured language model provider, either local or hosted
- Bun or Node.js for working on the web interface
- Git, if you want Devika to work with Git repositories
- Additional browser or system dependencies if required by the setup script or selected tools

For sandboxed command execution, the repository also includes Firejail-related support. Firejail availability and behavior depend on your operating system.

## Setup

Clone the repository and enter its directory:

```bash
git clone <repository-url>
cd devika-gzrxwwzh
```

The repository includes a setup script. Review it before running, then use it if it matches your environment:

```bash
bash setup.sh
```

Alternatively, install the Python dependencies manually:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

If Devika’s browser features require Playwright in your environment, install its browser dependencies as needed:

```bash
python -m playwright install
```

### Web interface dependencies

The frontend uses Svelte and Vite. Install its dependencies from the directory containing `package.json`. For example, with Bun:

```bash
bun install
```

The available frontend commands are defined in `package.json`; inspect that file for the exact scripts supported by this checkout.

## Configuration

The repository includes `sample.config.toml` as a starting point. Review it and configure the model provider, credentials, and other settings required for your setup. If the application expects a local `config.toml`, create it from the sample:

```bash
cp sample.config.toml config.toml
```

Then edit the copy rather than the sample. Follow the names and format used in `sample.config.toml` and the application’s configuration code; do not assume that credentials or provider settings are interchangeable between providers.

Depending on the provider you select, you may need to:

- Add an API key or other credentials.
- Choose a model name supported by that provider.
- Start a local model server, such as Ollama or LM Studio.
- Configure search or browser-related settings.
- Configure optional integrations such as GitHub or Netlify.

Keep credentials private. Do not commit local configuration files or API keys to version control.

## Running Devika

Start the Python application from the repository root:

```bash
python devika.py
```

Use the address and port printed by the application to open the interface. If the frontend is run separately during development, start it using the relevant script in `package.json` (commonly a Vite development script):

```bash
bun run dev
```

If the frontend and backend run as separate processes, keep both running and use the frontend’s displayed address. Check the project configuration and startup output for the correct ports and any required backend URL settings.

## Using Devika

1. Start Devika and open its web interface.
2. Select or configure a model provider.
3. Choose the project or working directory Devika should use.
4. Describe the task clearly, including constraints, expected behavior, and relevant context.
5. Review the plan and progress, where available.
6. Inspect the resulting code and run the project’s tests yourself before relying on the changes.

For best results, give Devika a well-scoped task and specify how you will verify completion. Avoid supplying production credentials or asking it to perform irreversible operations without supervision.

## Docker

The repository includes `docker-compose.yaml` and Dockerfiles for container-based use. Review the compose file and configuration requirements before starting the stack:

```bash
docker compose up --build
```

Stop the services with:

```bash
docker compose down
```

The compose configuration determines which services are started, which ports are exposed, and how local files and configuration are mounted. Consult it before exposing the application beyond your local machine.

## Project structure

The repository’s files are grouped into several functional areas:

- **Agent and orchestration:** planning, task decisions, execution, reporting, rerunning, and patching.
- **Language-model clients:** integrations for OpenAI, Groq, LM Studio, Ollama, Gemini, Mistral, and Claude.
- **Research and knowledge:** search, browser, sentence-processing, knowledge-base, and RAG components.
- **Project and execution tools:** project handling, code reading and running, Git, PDF, UML, and logging utilities.
- **Integrations:** GitHub and Netlify modules, plus additional task-oriented modules.
- **Frontend:** Svelte layouts, pages, components, styling, assets, and Vite configuration.
- **Deployment and documentation:** Docker files, setup scripts, configuration examples, and project documentation.

## Security and limitations

Devika is an agent that may interact with files, browsers, and command execution tools. Treat its outputs as untrusted until reviewed.

- Use a disposable or otherwise isolated project when evaluating unfamiliar tasks.
- Review file changes and commands before running them in important environments.
- Do not expose API keys, private repositories, or sensitive data unnecessarily.
- Be cautious when enabling browser, shell, network, or third-party integrations.
- Use appropriate sandboxing and operating-system permissions.
- Verify generated code with tests, code review, and any project-specific checks.

Model quality, tool availability, and behavior vary by provider and configuration. Some integrations or task modules may be incomplete or require additional setup. Devika’s output should not be treated as a substitute for security review or testing.

## Troubleshooting

- **The application cannot connect to a model:** Check the selected provider, model name, credentials, and—if using a local provider—that its server is running and reachable.
- **The frontend does not start:** Install dependencies in the directory containing `package.json` and check the scripts defined there.
- **Browser features fail:** Check the browser dependencies required by your setup and any browser configuration in the sample configuration.
- **A command or integration is unavailable:** Check the relevant module’s requirements and your operating system’s installed tools.
- **The application fails during startup:** Review the terminal output, Python dependencies, local configuration, and Docker Compose settings if applicable.

## Contributing

Contributions are welcome. Before making changes, review `CONTRIBUTING.md`. For substantial changes, open an issue or discussion first to align on the intended behavior. Please include relevant tests or manual verification steps with bug fixes and feature changes.

## License

See the [`LICENSE`](LICENSE) file for the terms that apply to this repository.

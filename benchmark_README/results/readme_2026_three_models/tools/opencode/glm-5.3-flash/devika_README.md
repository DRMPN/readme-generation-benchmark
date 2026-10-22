# Devika

Devika is an advanced AI software engineer. It is designed to understand high-level human instructions, break them down into steps, research relevant information, and write code to achieve a given objective.

## Key Features

- **Multi-Step Planning**: Breaks down high-level objectives into actionable steps using a Planner sub-agent.
- **Web Research**: Extracts relevant search queries from a plan and performs web research using Bing, Google, or DuckDuckGo. It can also crawl and interact with live web pages (e.g., clicking, typing, scrolling) via Playwright.
- **Code Generation**: Generates code based on the plan and research context, segmenting it into appropriate files and directories with support for multiple languages and frameworks.
- **Code Execution**: Runs the written code in a sandboxed environment and streams terminal output to the user.
- **Feature & Patching**: Implements new features on existing projects, or debugs and fixes issues based on user descriptions or error messages.
- **Project Reporting**: Generates project reports summarizing technical design, setup instructions, and API details, exporting them as PDF documents.
- **External Integrations**: Supports GitHub operations (cloning repos, listing commits/files) and deploying sites to Netlify.
- **Multiple LLM Support**: Works with Claude (Anthropic), OpenAI (GPT), Gemini, Mistral, Groq, as well as locally hosted models via Ollama or LM Studio.

## System Architecture

Devika's system architecture consists of the following key components:

1. **User Interface**: A web-based chat interface for interacting with Devika, viewing project files, and monitoring the agent's state.
2. **Agent Core**: The central component that orchestrates the AI planning, reasoning, and execution process. It communicates with various sub-agents and modules to accomplish tasks.
3. **Large Language Models**: Devika leverages state-of-the-art language models like **Claude**, **GPT-4**, and **Local LLMs via Ollama** for natural language understanding, generation, and reasoning.
4. **Planning and Reasoning Engine**: Responsible for breaking down high-level objectives into actionable steps and making decisions based on the current context.
5. **Research Module**: Utilizes keyword extraction and web browsing capabilities to gather relevant information for the task at hand.
6. **Code Writing Module**: Generates code based on the plan, research findings, and user requirements. Supports multiple programming languages.
7. **Browser Interaction Module**: Enables Devika to navigate websites, extract information, and interact with web elements as needed.
8. **Knowledge Base**: Stores and retrieves project-specific information, code snippets, and learned knowledge for efficient access.
9. **Database**: Persists project data, agent states, and configuration settings.

### Specialized Sub-Agents

Devika's cognitive abilities are powered by a collection of specialized sub-agents. Each agent is implemented as a separate Python class, and agents communicate with the underlying LLMs through prompt templates defined in Jinja2 format.

- **Planner**: Generates a high-level step-by-step plan based on the user's prompt.
- **Researcher**: Extracts and ranks relevant search queries based on relevance and specificity.
- **Coder**: Generates code based on the step-by-step plan and researched context.
- **Action**: Determines the appropriate action to take based on the user's follow-up prompt (e.g., run, test, deploy, fix, implement, report).
- **Runner**: Executes written code in a sandboxed environment across OS environments and streams output in real-time.
- **Feature**: Implements a new feature based on the user's specification and maintains code structure.
- **Patcher**: Debugs and fixes issues based on user descriptions or error messages.
- **Reporter**: Generates comprehensive project reports summarizing technical design and setup instructions, exported as a PDF.
- **Decision**: Handles special command-like instructions that don't fit other agents (e.g., git clone, browser interaction).

## Installation

### Setting Up API Keys

You need to configure your API keys in `config.toml` (you can copy `sample.config.toml` as a template). The following API keys and endpoints are required depending on the features you use:

- Search Engine: Bing, Google, or DuckDuckGo.
- LLM Provider: Claude, OpenAI, Gemini, Mistral, Groq, Ollama, or LM Studio.
- Netlify: To enable site deployment features.

### Manual Setup

To install dependencies and set up the local environment, run the provided `setup.sh` script:

```sh
sh setup.sh
```

This will:
1. Install the Python dependencies from `requirements.txt`.
2. Set up Playwright with the required browsers.
3. Install frontend dependencies in the `ui/` directory using Bun.

### Docker Compose Setup

Alternatively, you can run Devika using Docker Compose. The `docker-compose.yaml` file is configured to run three services:

- `ollama-service`: For local model inference.
- `devika-backend-engine`: The Python backend engine running on port `1337`.
- `devika-frontend-app`: The Svelte-based frontend UI running on port `3000`.

To build and launch the containers, run:

```sh
make compose-up
```

## Usage

Once the backend engine is running, it starts the API on port `1337` (accessible via `devika.py`).

The frontend (in the `ui/` directory) is a Svelte-based web application that connects to the backend via API routes. You can run the frontend in development mode using:

```sh
cd ui
bun run dev
```

Once launched, you can interact with Devika through the web interface by providing high-level instructions and monitoring the agent's state in real-time.

## Configuration

Configuration is managed through `config.toml`. The configuration covers:

- **[STORAGE]**: Paths for the SQLite database, screenshots, PDFs, projects, logs, and repositories.
- **[API_KEYS]**: API keys for external services (Bing, Google Search, Claude, OpenAI, Gemini, Mistral, Groq, Netlify).
- **[API_ENDPOINTS]**: API endpoints for search engines, Ollama, LM Studio, and OpenAI.
- **[LOGGING]**: Settings for REST API logging and prompt logging.
- **[TIMEOUT]**: Inference timeout settings.

## Contributing

We welcome contributions to enhance Devika's capabilities and improve its performance. To report bugs, create a [GitHub issue](https://github.com/stitionai/devika/issues).

Before contributing, read through the existing issues and pull requests to see if someone else is already working on something similar. To contribute, fork the repository, create a new branch for your feature or bug fix, make your changes, and submit a pull request.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

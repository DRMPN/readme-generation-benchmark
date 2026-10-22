# TaskMatrix-6go5kmu_

TaskMatrix-6go5kmu_ is a Python project that connects large language models (LLMs) with a collection of tools and APIs so they can complete multi-step tasks. A planning model breaks a user request into steps, an executing model runs those steps through the appropriate tools, and a low-code layer lets users generate, inspect, and extend the resulting workflows.

The project is based on the TaskMatrix.AI concept: foundation models act as a "brain" that can call millions of APIs and visual tools. It includes a Visual ChatGPT-style interface for working with images, a Flask-style web app with a browser front end, and a Docker-based deployment path.

> **Note:** This README was written from the repository's file listing. Some details (exact ports, configuration keys, and endpoint paths) are marked as assumptions and should be checked against the source code before publishing.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
  - [Running Locally](#running-locally)
  - [Running with Docker](#running-with-docker)
  - [Running with Supervisord](#running-with-supervisord)
- [Usage](#usage)
- [Workflow Concepts](#workflow-concepts)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Security](#security)
- [Code of Conduct](#code-of-conduct)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Natural-language task planning.** Converts a user request into an ordered plan of sub-tasks.
- **Tool execution.** Runs each step through the matching tool or API and passes results to later steps.
- **Low-code workflow generation.** Produces an editable workflow from a request so users can see and modify the process.
- **Workflow extension.** Adds new steps to an existing workflow without regenerating it from scratch.
- **Visual tooling.** Supports image-related tasks through a Visual ChatGPT-style module.
- **OpenAI integration.** Wraps OpenAI API calls in a single module so models and parameters are easy to change.
- **Web interface.** A browser front end (`index.html`) for entering requests and viewing workflows and results.
- **Containerized deployment.** Includes a `Dockerfile` and `supervisord.conf` for running services in a container.
- **Test suite.** Test cases for workflow generation, workflow extension, and execution, driven by JSON fixtures.

---

## Architecture

The system is organized into three logical layers:

```
┌──────────────────────────────────────────────────────────┐
│                  Web UI (index.html)                     │
└───────────────────────────┬──────────────────────────────┘
                            │ HTTP requests
┌───────────────────────────▼──────────────────────────────┐
│                    Application (app.py)                  │
│   Routes requests to the low-code and planning layers    │
└──────┬──────────────────────┬───────────────────┬────────┘
       │                      │                   │
┌──────▼──────────┐  ┌────────▼─────────┐  ┌──────▼─────────┐
│  lowCodeLLM.py  │  │  planningLLM.py  │  │ executingLLM.py│
│ Build/extend    │  │ Decompose a task │  │ Run each step  │
│ workflows       │  │ into sub-tasks   │  │ with tools     │
└──────┬──────────┘  └────────┬─────────┘  └──────┬─────────┘
       │                      │                   │
       └──────────────┬───────┴───────────────────┘
                      │
          ┌───────────▼────────────┐       ┌──────────────────────┐
          │  openAIWrapper.py      │       │  visual_chatgpt.py   │
          │  LLM API access        │       │  Visual tools        │
          └────────────────────────┘       └──────────────────────┘
```

### Component Summary

| Component | Responsibility |
|---|---|
| `app.py` | Application entry point. Defines the server, routes, and request handling. |
| `lowCodeLLM.py` | Generates workflows from requests and extends existing workflows. |
| `planningLLM.py` | Decomposes a high-level request into an ordered list of steps. |
| `executingLLM.py` | Executes each step by selecting and calling the appropriate tool. |
| `openAIWrapper.py` | Centralizes calls to the OpenAI API (authentication, model selection, retries). |
| `visual_chatgpt.py` | Visual foundation-model tools for image-based tasks. |
| `index.html` | Front-end page for interacting with the system. |

---

## Repository Structure

```
TaskMatrix-6go5kmu_/
├── app.py                          # Main application entry point
├── lowCodeLLM.py                   # Low-code workflow generation and extension
├── planningLLM.py                  # Task planning logic
├── executingLLM.py                 # Step execution logic
├── openAIWrapper.py                # OpenAI API wrapper
├── visual_chatgpt.py               # Visual tooling (image tasks)
├── index.html                      # Web front end
├── config.template                 # Configuration template (copy and edit)
├── Dockerfile                      # Container build definition
├── supervisord.conf                # Process manager configuration
├── requirements.txt                # Python dependencies
├── test_get_workflow.py            # Tests for workflow generation
├── test_extend_workflow.py         # Tests for workflow extension
├── test_execute.py                 # Tests for execution
├── get_workflow_test_cases.json    # Fixtures for workflow generation tests
├── extend_workflow_test_cases.json # Fixtures for workflow extension tests
├── execute_test_cases.json         # Fixtures for execution tests
├── README.md                       # Project documentation
├── CONTRIBUTING.md                 # Contribution guidelines
├── CODE_OF_CONDUCT.md              # Community standards
├── SECURITY.md                     # Security policy
├── LICENSE.txt                     # License terms
├── paradigm.png                    # Architecture/paradigm diagram
├── low-code-llm.png                # Low-code LLM diagram
├── low-code-operation.png          # Low-code operation diagram
├── overview.png                    # Project overview diagram
├── figure.jpg                      # Figure for documentation
├── demo.gif                        # Demo animation
├── demo_short.gif                  # Short demo animation
├── demo_inf.gif                    # Demo animation
└── low-code-demovideo.mp4          # Low-code demo video
```

The repository also contains a second `requirements.txt` and `README.md`, which are likely used by a sub-component (for example, the Visual ChatGPT module). Check whether these are intended to be installed separately.

---

## Prerequisites

- **Python 3.8 or later** (confirm the minimum version in `Dockerfile` or the project's requirements).
- **pip** for installing Python packages.
- **An OpenAI API key** with access to the models the project uses.
- **Docker** (optional), for containerized deployment.
- **A GPU** (optional), if you enable local visual models. CPU-only operation is possible for the core planning and workflow features.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/TaskMatrix-6go5kmu_.git
cd TaskMatrix-6go5kmu_
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If the Visual ChatGPT module needs its own dependencies, install them too:

```bash
pip install -r path/to/visual/requirements.txt
```

---

## Configuration

Configuration values are kept out of source code. Start from the provided template:

```bash
cp config.template config.py   # or the filename the code expects
```

Then edit the copied file and set your values. Typical settings include:

| Setting | Description | Example |
|---|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |
| `OPENAI_MODEL` | Model used for planning and execution | `gpt-4` |
| `HOST` | Address the server binds to | `0.0.0.0` |
| `PORT` | Port the server listens on | `5000` |
| `DEBUG` | Enable debug mode (disable in production) | `False` |

> **Security:** Never commit your real API key. Add your configuration file to `.gitignore`, and use environment variables in production:
>
> ```bash
> export OPENAI_API_KEY="your-key-here"
> ```

---

## Running the Application

### Running Locally

With dependencies installed and configuration set:

```bash
python app.py
```

Then open the web interface in your browser, typically at:

```
http://localhost:5000
```

(The port depends on your configuration.)

### Running with Docker

Build the image:

```bash
docker build -t taskmatrix .
```

Run the container, passing your API key as an environment variable:

```bash
docker run -p 5000:5000 -e OPENAI_API_KEY="your-key-here" taskmatrix
```

Adjust the port mapping if you changed the default port.

### Running with Supervisord

`supervisord.conf` manages the application as a background process. This is useful inside containers or on servers where the app should restart automatically.

```bash
supervisord -c supervisord.conf
supervisorctl status
```

Check `supervisord.conf` for the exact program names and log locations.

---

## Usage

1. **Start the server** using one of the methods above.
2. **Open the web interface** in your browser.
3. **Describe a task** in natural language, for example:
   > "Find the three most recent news articles about renewable energy and summarize each in one sentence."
4. **Review the generated workflow.** The low-code layer displays the steps the system plans to take.
5. **Extend or edit the workflow** if needed by adding steps or changing the order.
6. **Execute the workflow.** The executing layer runs each step and returns the results.

### Example Workflow Flow

```
User request
   │
   ▼
[lowCodeLLM]    → Generate workflow: [Step 1] → [Step 2] → [Step 3]
   │
   ▼
[planningLLM]   → Refine each step into concrete actions
   │
   ▼
[executingLLM]  → Run Step 1 → Run Step 2 → Run Step 3
   │
   ▼
Final result returned to the user
```

---

## Workflow Concepts

- **Workflow:** An ordered list of steps that together complete a task.
- **Step:** A single unit of work, such as calling a tool, querying a model, or processing an image.
- **Plan:** The decomposition of a request into steps, produced by `planningLLM.py`.
- **Execution:** Running each step in sequence and passing outputs forward, handled by `executingLLM.py`.
- **Extension:** Adding steps to an existing workflow, handled by `lowCodeLLM.py`.

---

## Testing

The test suite uses JSON fixtures so that test cases can be added or changed without editing code.

| Test file | Fixture file | What it tests |
|---|---|---|
| `test_get_workflow.py` | `get_workflow_test_cases.json` | Workflow generation from requests |
| `test_extend_workflow.py` | `extend_workflow_test_cases.json` | Adding steps to existing workflows |
| `test_execute.py` | `execute_test_cases.json` | Step execution and results |

Run all tests:

```bash
python -m pytest
```

Run a specific file:

```bash
python -m pytest test_get_workflow.py -v
```

> **Note:** Tests that call the OpenAI API will incur usage costs and require a valid `OPENAI_API_KEY`. Consider mocking `openAIWrapper.py` for fast, offline runs.

### Adding a Test Case

Add an entry to the relevant JSON file, following the structure of the existing entries. Then run the matching test file to confirm it is picked up.

---

## Troubleshooting

| Problem | Possible cause | Solution |
|---|---|---|
| `AuthenticationError` from OpenAI | Missing or invalid API key | Check `OPENAI_API_KEY` in your config or environment |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` inside your virtual environment |
| Port already in use | Another process uses the port | Change `PORT` in the config or stop the conflicting process |
| Docker container exits immediately | Missing environment variables or config | Run `docker logs <container>` to inspect the error |
| Slow or failing tests | Live API calls | Mock `openAIWrapper.py` or use a smaller fixture set |
| Visual features fail | Missing visual dependencies or GPU | Install the visual module's requirements and confirm your hardware setup |

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

General workflow:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes and add or update tests.
4. Run the test suite: `python -m pytest`.
5. Commit with a clear message and push your branch.
6. Open a pull request describing the change and its motivation.

---

## Security

To report a security vulnerability, follow the process in [SECURITY.md](SECURITY.md). Please do not open a public issue for security problems.

Security reminders for users:

- Keep API keys out of source control.
- Review any tool or API the system is allowed to call, since LLM-driven execution can trigger external actions.
- Run the container with the least privileges needed.

---

## Code of Conduct

This project follows the [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

---

## License

This project is licensed under the terms in [LICENSE.txt](LICENSE.txt).

---

## Acknowledgements

- The TaskMatrix.AI concept and its research paper, which describe connecting foundation models with large collections of APIs.
- The Visual ChatGPT project, which inspired the visual tooling in this repository.
- OpenAI, for the language model APIs used by the wrapper module.

---

*If you have questions or find problems, please open an issue in the repository.*

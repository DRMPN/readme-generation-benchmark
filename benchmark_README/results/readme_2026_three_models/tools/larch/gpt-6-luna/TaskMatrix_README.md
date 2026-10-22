# TaskMatrix

TaskMatrix is a Python project for experimenting with low-code workflows powered by large language models. Its modules cover workflow planning, execution, and extension, with an application entry point, a web interface, and a Visual ChatGPT example.

## Contents

- [Features](#features)
- [How it fits together](#how-it-fits-together)
- [Repository layout](#repository-layout)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the project](#running-the-project)
- [Tests](#tests)
- [Security notes](#security-notes)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Workflow planning:** `planningLLM.py` contains planning-related functionality.
- **Workflow execution:** `executingLLM.py` contains execution-related functionality.
- **Workflow extension:** the project includes tests and test cases for extending workflows.
- **LLM integration:** `openAIWrapper.py` provides an integration layer for OpenAI-related calls.
- **Application and interface:** `app.py` and `index.html` provide the application and its web interface.
- **Visual ChatGPT example:** `visual_chatgpt.py` demonstrates a visual-task-oriented interface or workflow.

The exact behavior and available options are defined by the source code and configuration template in this repository.

## How it fits together

At a high level, the project separates workflow tasks into modules:

1. A planning component can help determine how a requested task should be handled.
2. An execution component can carry out workflow steps.
3. Workflow extension logic can add or modify workflow behavior.
4. The LLM wrapper centralizes communication with the model provider.
5. The application and web interface provide a way to interact with the functionality.

This is a conceptual overview based on the repository structure; consult the individual modules for their concrete interfaces and behavior.

## Repository layout

| File or directory | Purpose |
|---|---|
| `app.py` | Main application entry point. |
| `index.html` | Web interface. |
| `planningLLM.py` | Workflow planning logic. |
| `executingLLM.py` | Workflow execution logic. |
| `lowCodeLLM.py` | Low-code LLM-related functionality. |
| `openAIWrapper.py` | OpenAI integration wrapper. |
| `visual_chatgpt.py` | Visual ChatGPT-related example or application. |
| `config.template` | Configuration template. |
| `requirements.txt` | Python dependencies. |
| `test_get_workflow.py` | Tests for retrieving workflows. |
| `test_extend_workflow.py` | Tests for extending workflows. |
| `test_execute.py` | Tests for workflow execution. |
| `*_test_cases.json` | Test-case data for workflow operations. |
| `overview.png`, `paradigm.png`, `low-code-operation.png`, `low-code-llm.png`, `figure.jpg` | Project diagrams and images. |
| `demo.gif`, `demo_short.gif`, `demo_inf.gif`, `low-code-demovideo.mp4` | Demonstration media. |
| `LICENSE.txt` | Project license. |
| `CONTRIBUTING.md` | Contribution guidance. |
| `CODE_OF_CONDUCT.md` | Community standards. |
| `SECURITY.md` | Security reporting guidance. |

## Requirements

- Python 3
- `pip`
- The packages listed in `requirements.txt`
- Any credentials or external services required by the configured LLM integration

Check the dependency file and configuration template for the versions and services applicable to your environment.

## Installation

Clone the repository and enter its directory:

```bash
git clone <repository-url>
cd TaskMatrix-84zy97pw
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Review `config.template` before running the application. It indicates the configuration values the project expects. In particular:

1. Identify any required API keys, service URLs, or model settings.
2. Provide credentials using the configuration mechanism expected by the code.
3. Keep private credentials out of source control.

The precise configuration filename and required fields depend on how the application modules load settings. Check references to `config.template` and configuration imports in the source before creating your local configuration file.

## Running the project

The likely application entry point is `app.py`:

```bash
python app.py
```

If the application uses a framework-specific development server or requires command-line arguments, follow the instructions and options implemented in `app.py`.

The repository also contains a Visual ChatGPT-related module:

```bash
python visual_chatgpt.py
```

Its availability may depend on additional services, credentials, or configuration. Review the module before running it.

## Tests

Run the tests with `pytest`:

```bash
python -m pytest
```

The repository includes test suites for workflow retrieval, workflow extension, and execution. JSON files such as `get_workflow_test_cases.json`, `extend_workflow_test_cases.json`, and `execute_test_cases.json` provide test data for those operations.

If `pytest` is not installed as part of the project dependencies, install it in your active environment:

```bash
python -m pip install pytest
```

## Security notes

- Do not commit API keys, access tokens, or other secrets.
- Treat model-generated plans and outputs as untrusted input, particularly if workflows can invoke tools or affect external systems.
- Review `SECURITY.md` for instructions on reporting vulnerabilities.
- Use only services and credentials you are authorized to access.

## Contributing

Contributions are welcome. Before submitting changes, review:

- `CONTRIBUTING.md` for contribution instructions
- `CODE_OF_CONDUCT.md` for community expectations
- The existing tests and test-case files for expected behavior

Please include tests when changing workflow planning, execution, or extension behavior.

## License

See `LICENSE.txt` for the terms under which this project is distributed.

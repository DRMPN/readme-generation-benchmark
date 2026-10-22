# TaskMatrix-x98hbzgq

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![flask](https://img.shields.io/badge/Flask-000000.svg?style={0}&logo=Flask&logoColor=white)
![gunicorn](https://img.shields.io/badge/Gunicorn-499848.svg?style={0}&logo=Gunicorn&logoColor=white)
![openai](https://img.shields.io/badge/OpenAI-412991.svg?style={0}&logo=OpenAI&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

LowCodeLLM is a Python web service that uses large language models to turn a task description into a standard operating procedure (SOP), a sequence of steps with conditional jumps, and then runs a chat that follows that SOP. It is intended for developers building or hosting LLM-driven workflow applications. The project exposes an HTTP API for generating, extending, and executing workflows, along with a bundled web page for interactive use. For runnable steps, see the Getting Started section. The repository also contains a separate project, TaskMatrix.AI, documented in its [own README](TaskMatrix.AI/README.md).

---

## Core Features

- **Task-to-workflow generation:** Turns a natural-language task prompt into a step-by-step standard operating procedure (SOP) with optional conditional jumps, so developers can start from a structured plan instead of writing one manually.
- **Workflow step extension:** Expands a selected step of an existing workflow into a more detailed sub-workflow, letting developers refine rough steps without regenerating the whole plan.
- **Workflow-guided chat execution:** Runs a conversation against a confirmed workflow and returns responses based on the task and conversation history, enabling workflow-driven assistants.
- **JSON API endpoints:** Exposes workflow generation, extension, and execution as HTTP POST endpoints that accept and return JSON, making the service easy to call from any client.
- **OpenAI and Azure OpenAI configuration:** Selects between OpenAI and Azure OpenAI backends through environment variables, allowing deployment to either provider without code changes.

---

## Installation

Install TaskMatrix-x98hbzgq using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/TaskMatrix-x98hbzgq
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

**Prerequisites**
- Python. The required version is not specified in the provided context.
- An OpenAI API key, set in the `OPENAIKEY` environment variable. Azure OpenAI is also supported through `USE_AZURE`, `API_BASE`, `API_VERSION`, and `MODEL`.

**Steps**
1. Install dependencies using the steps in the Installation section. The dependency list is in `LowCodeLLM/src/requirements.txt`.
2. Set `OPENAIKEY`. For Azure OpenAI, also set `USE_AZURE=true`, `API_BASE`, `API_VERSION`, and `MODEL`.
3. Start the Flask app defined in `LowCodeLLM/src/app.py`, using the run command from the Installation section.
4. Open the root route (`/`), which serves `index.html`.
5. Send a `POST` request to `/api/get_workflow` with a JSON body containing `task_prompt`.

> **Note:** The run command is unverified. Confirm the launch method in the Installation section before relying on it.

---

## API Reference

The LowCodeLLM backend exposes a small Flask HTTP API and Python classes in `LowCodeLLM/src/`. The shown files do not define a stable library API intended for import by other packages.

### HTTP routes (`LowCodeLLM/src/app.py`)

| Route | Method | Purpose |
|---|---|---|
| `/` | Not specified in route | Serves `index.html`. |
| `/api/get_workflow` | POST | Generates a workflow (SOP) from a task prompt. |
| `/api/extend_workflow` | POST | Generates a sub-workflow for a step in an existing workflow. |
| `/api/execute` | POST | Runs a chat turn using a confirmed workflow. |

### Classes

| Class | Module | Purpose |
|---|---|---|
| `lowCodeLLM` | `lowCodeLLM.py` | Orchestrates workflow generation, extension, and execution. |
| `planningLLM` | `planningLLM.py` | Generates and extends workflows, and converts workflow text to JSON. |
| `executingLLM` | `executingLLM.py` | Produces chat responses that follow a workflow. |
| `OpenAIWrapper` | `openAIWrapper.py` | Wraps OpenAI chat completion calls, including Azure OpenAI configuration. |

### Other modules

- `visual_chatgpt.py` (repository root): No public functions or classes are defined in the provided content. It is script-oriented, and its entry point was not provided.

---

## Testing

The LowCodeLLM project includes automated test files in `LowCodeLLM/src/test/`:

- `test_execute.py`
- `test_extend_workflow.py`
- `test_get_workflow.py`
- `testcases/` (contents not reviewed)

No test framework configuration, CI configuration, or exact test run command was found in the provided context, so this section does not specify how to run the tests. Review the test files to confirm their dependencies and whether they require a configured `OPENAIKEY` (see `LowCodeLLM/src/openAIWrapper.py`).

No tests were observed for the `TaskMatrix.AI` component (`visual_chatgpt.py`).

No CI workflow directory was observed in the repository tree, so contributors should run the tests locally before submitting changes. See `CONTRIBUTING.md` for contribution guidelines.

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to TaskMatrix-x98hbzgq.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE.txt) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). TaskMatrix-x98hbzgq repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{TaskMatrix-x98hbzgq,

        author = {README Benchmark},

        title = {TaskMatrix-x98hbzgq repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
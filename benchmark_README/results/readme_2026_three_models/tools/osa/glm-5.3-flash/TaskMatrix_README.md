# TaskMatrix-ea7uiih0

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
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

TaskMatrix-ea7uiih0 is a Python-based research and demonstration repository for LLM-driven agents, containing two largely independent components: Visual ChatGPT, a visual dialogue assistant that chains vision models in a browser-based interface, and LowCodeLLM, a web service that plans, extends, and executes SOP-style workflows via large language models. It targets developers and ML/AI researchers exploring tool-based agents and LLM workflow planning. The repository offers an interactive dialogue application and a REST-style web service, with runnable steps described in the Getting Started section.

---

## Core Features

- **Visual dialogue assistant with a wide vision toolset**: an interactive chat agent that can generate, edit, segment, caption, and answer questions about images by chaining many vision models (including diffusion-based generation and open-vocabulary grounding), so users accomplish complex visual tasks through natural conversation.
- **LLM-driven SOP planning**: given a task description, a planning LLM produces a structured, step-by-step standard operating procedure with conditional jump logic, breaking hard tasks into followable workflows.
- **Interactive workflow refinement**: any step of a generated SOP can be expanded into a more detailed sub-procedure that stays consistent with the rest of the workflow, letting users iteratively improve guidance where it is too coarse.
- **SOP-guided conversational execution**: an executing LLM follows a confirmed workflow to guide end-user dialogue step by step, producing responses that adhere to the agreed procedure without exposing its internal steps.
- **Service-ready REST API**: a Flask-based HTTP service exposes workflow generation, extension, and execution endpoints with CORS support, making the low-code capabilities easy to integrate into web applications.

---

## Installation

Install TaskMatrix-ea7uiih0 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/TaskMatrix-ea7uiih0
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

### Prerequisites

- Python with pip.
- An OpenAI API key, or an Azure OpenAI service deployment if you use the Azure configuration path.
- Install the project dependencies:

```bash
pip install -r requirements.txt
```

### Configure LLM access

The LowCodeLLM service reads its settings from environment variables (see `LowCodeLLM/config.template`):

- `OPENAIKEY` – your OpenAI API key (always required).
- `USE_AZURE` – set to `true` to use Azure OpenAI; otherwise the service uses the default OpenAI `gpt-3.5-turbo` model.
- When `USE_AZURE=true`, also set `API_BASE`, `API_VERSION`, and `MODEL` (your Azure deployment name).

Example Azure configuration:

```bash
export USE_AZURE=true
export OPENAIKEY=your-azure-openai-service-key
export API_BASE=your-base-url-for-azure
export API_VERSION=2023-03-15-preview
export MODEL=your-gpt-deployment-name
```

For non-Azure usage, only `OPENAIKEY` is required.

### Run the LowCodeLLM service

Start the Flask application defined in `LowCodeLLM/src/app.py`. A `Dockerfile` is also provided for containerized serving. Use the host and port from your serving configuration (for example, gunicorn/supervisord if configured) in the steps below.

### Try the API

The service exposes three POST endpoints: `/api/get_workflow`, `/api/extend_workflow`, and `/api/execute`. Each accepts a JSON body; `/api/get_workflow` requires a `task_prompt` field:

```bash
curl -X POST "http://localhost:PORT/api/get_workflow" -H "Content-Type: application/json" -d '{"task_prompt": "Plan a weekend trip"}'
```

Replace `PORT` with the actual port of your deployment. A successful call returns a JSON workflow; an internal failure returns a 500 response with an `errmsg` field.

The other endpoints use additional fields confirmed in `LowCodeLLM/src/app.py`:

- `/api/extend_workflow`: `task_prompt`, `current_workflow`, `step`
- `/api/execute`: `task_prompt`, `confirmed_workflow`, `curr_input`, `history`

### Alternative: Visual ChatGPT

The repository also includes `visual_chatgpt.py`, a Gradio-based visual dialogue assistant built on PyTorch, Hugging Face transformers, diffusers, and LangChain. Run it after installing the top-level `requirements.txt` and configuring OpenAI access; note that the vision models typically require a GPU-capable environment.

---

## Testing

Tests for the LowCodeLLM service are located in `LowCodeLLM/src/test/`:

- `test_get_workflow.py`
- `test_extend_workflow.py`
- `test_execute.py`
- `testcases/` (directory alongside the test files)

The test file names correspond to the three API endpoints exposed in `LowCodeLLM/src/app.py` (`/api/get_workflow`, `/api/extend_workflow`, `/api/execute`), covering the workflow planning, extension, and execution paths of the service.

When verifying changes:

- No CI configuration is present in the repository tree, so tests must be run locally.
- The repository does not document a test runner or exact run command; inspect the files in `LowCodeLLM/src/test/` to determine the framework and how to execute them.
- The modules under test call the OpenAI API via `LowCodeLLM/src/openAIWrapper.py`, which reads `OPENAIKEY` from the environment (and `API_BASE`, `API_VERSION`, and `MODEL` when `USE_AZURE=true`, per `LowCodeLLM/config.template`); confirm the required environment setup before running tests.
- No test files are present for `visual_chatgpt.py`.

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to TaskMatrix-ea7uiih0.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE.txt) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). TaskMatrix-ea7uiih0 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{TaskMatrix-ea7uiih0,

        author = {README Benchmark},

        title = {TaskMatrix-ea7uiih0 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
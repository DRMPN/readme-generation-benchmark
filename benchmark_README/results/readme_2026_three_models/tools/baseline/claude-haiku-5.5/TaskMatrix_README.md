# Low-code LLM

**Low-code LLM** is a human-LLM interaction pattern in which a person stays in the loop to make LLM responses more controllable and stable. Instead of relying only on prompt engineering, the system first asks a Planning LLM to decompose a task into a structured workflow. The user then reviews and edits that workflow with low-code operations before an Executing LLM produces responses that follow it.

- Paper: [Low-code LLM: Visual Programming over LLMs](https://arxiv.org/abs/2304.08103)
- Demo video: https://user-images.githubusercontent.com/43716920/233937121-cd057f04-dec8-45b8-9c52-a9e9594eec80.mp4 (a conceptual demo of the full process)

This repository is part of Microsoft's TaskMatrix project. The LowCodeLLM directory contains the low-code LLM web application. The project README notes that TaskMatrix.AI aims to connect foundation models with APIs of other AI models and systems, and that the low-code interaction pattern can give users more control over the process and a way to express their preferences.

The LowCodeLLM code is a minimum viable version that demonstrates the core human-LLM interaction concept. The front-end interface is basic, and the authors invite contributions to improve it.

## System Overview

The interaction works in four stages:

1. **Planning LLM** generates a highly structured workflow (a standard operating procedure, or SOP) for a complex task.
2. **Users edit the workflow** using predefined low-code operations, performed by clicking, dragging, or editing text.
3. **Executing LLM** generates responses that follow the reviewed workflow.
4. **Users refine the workflow** until the results are satisfactory.

The project highlights three advantages: controllable generation, because responses follow a user-reviewed workflow; friendly interaction, because the workflow shows the model's execution logic and reduces time spent on prompt engineering; and wide applicability to complex tasks where human intelligence or preference matters.

## Repository Structure

Key files in `LowCodeLLM/`:

| Path | Purpose |
|------|---------|
| `Dockerfile` | Builds an Ubuntu 22.04 image that installs dependencies and runs the app under supervisord |
| `config.template` | Template for the configuration file (see Configuration) |
| `src/app.py` | Flask application that exposes the HTTP API and serves the front end |
| `src/lowCodeLLM.py` | Coordinates the planning and executing LLMs and converts workflows between JSON and text |
| `src/planningLLM.py` | Planning LLM: generates and extends workflows |
| `src/executingLLM.py` | Executing LLM: generates responses that follow a confirmed workflow |
| `src/openAIWrapper.py` | Wrapper around the OpenAI ChatCompletion API, with Azure OpenAI support |
| `src/index.html` | Web front end served at `/` |
| `src/requirements.txt` | Python dependencies for the application |
| `src/supervisord.conf` | Process configuration used by the container |
| `src/test/` | Test modules and JSON test cases |

The repository root also contains `visual_chatgpt.py` and a `requirements.txt` for the Visual ChatGPT part of TaskMatrix. These are separate from the LowCodeLLM application.

## Setup

### Prerequisites

- Docker
- An OpenAI API key, or an Azure OpenAI Service deployment

### Running with Docker

```bash
# clone the repository
git clone https://github.com/microsoft/TaskMatrix.git

# go to the project directory
cd LowCodeLLM

# build the image
docker build -t lowcode:latest .
```

The Dockerfile installs system packages (git, Python, pip, and supervisor), upgrades pip and setuptools, installs the packages in `src/requirements.txt`, copies `src` to `/app/src`, and starts the app with `supervisord -c supervisord.conf`. It sets the environment variable `WORKERS` to `2`.

**With the OpenAI API**, you only need to provide your key:

```bash
docker run -p 8888:8888 --env OPENAIKEY={Your_Private_Openai_Key} lowcode:latest
```

**With Azure OpenAI Service**, store the settings in a configuration file (see Configuration below):

```bash
docker run -p 8888:8888 --env-file config.ini lowcode:latest
```

When the container is running, open the demo page at `http://localhost:8888/`.

### Running without Docker

The supplied files do not include a documented procedure for running the application outside Docker. `src/requirements.txt` lists the dependencies (Flask, Flask-Cors, openai, gunicorn, and gevent), and the Dockerfile shows that `src` is the working directory, but the process setup is defined in `supervisord.conf`, which is not documented in this README.

## Configuration

The application reads its settings from environment variables in `src/openAIWrapper.py`:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAIKEY` | Yes | OpenAI API key. Used for both the OpenAI API and Azure OpenAI. |
| `USE_AZURE` | No | Set to `true` to use Azure OpenAI Service. Any other value, or no value, uses the OpenAI API. |
| `API_BASE` | Azure only | Azure OpenAI endpoint base URL. |
| `API_VERSION` | Azure only | Azure OpenAI API version. |
| `MODEL` | Azure only | Azure OpenAI deployment name, passed as the `engine` parameter. |

When `USE_AZURE` is not `true`, the wrapper calls the `gpt-3.5-turbo` model.

For Azure OpenAI, copy `config.template` to `config.ini` and fill in the values. The template's contents are not included in the supplied files, so the expected format is inferred from the variable names above. The file is passed to Docker with `--env-file`, which expects `NAME=value` lines.

The wrapper uses these fixed request parameters: `max_tokens=2048`, `frequency_penalty=0`, and `presence_penalty=0`. Temperature is set per LLM. `lowCodeLLM` defaults to `0.4` for the Planning LLM and `0` for the Executing LLM. The test code uses `0.5` for the Planning LLM and `0` for the Executing LLM.

## Usage

### Web Interface

Go to `http://localhost:8888/` to open the demo page. The `/` route serves `index.html`. The supplied files do not describe the front end's controls, so refer to the page itself for the workflow editing interface.

### HTTP API

The Flask app exposes three POST endpoints. Each returns a JSON body on success with HTTP 200. On failure, it logs the error and returns `{"errmsg": "internal errors"}` with HTTP 500.

**`POST /api/get_workflow`**: generates a workflow for a task.

```bash
curl -X POST http://localhost:8888/api/get_workflow \
  -H "Content-Type: application/json" \
  -d '{"task_prompt": "Write an essay about drunk driving issue."}'
```

**`POST /api/extend_workflow`**: generates a detailed sub-workflow for one step.

Request fields: `task_prompt`, `current_workflow` (a JSON string), and `step` (for example, `"STEP 1"`).

**`POST /api/execute`**: generates a response that follows a confirmed workflow.

Request fields: `task_prompt`, `confirmed_workflow` (a JSON string), `history` (a list of `{"role", "content"}` messages), and `curr_input` (the user's current message).

### Workflow Format

A workflow is a JSON array of steps. Each step has these fields:

```json
{
  "stepId": "STEP 1",
  "stepName": "Research",
  "stepDescription": "Gather statistics and information about the topic",
  "jumpLogic": [
    {"Condition": "if 'lack of information'", "Target": "STEP 1"}
  ],
  "extension": []
}
```

- `jumpLogic` lists conditions and the step to jump to when a condition is met. It may be empty.
- `extension` holds sub-steps produced by `extend_workflow`. Sub-steps are named like `STEP 2.1`.

The Planning LLM is prompted to return steps in this text form:

```
STEP 1: [step name][step descriptions][[[if 'condition1'][Jump to STEP]], ...]
```

`planningLLM.py` parses this text into JSON. `lowCodeLLM.py` converts JSON back into text, using the `extension` steps, before sending it to the LLMs.

## Development

- **Code layout:** Put application logic in `src/`. Each LLM role has its own class: `planningLLM` for workflow generation and extension, and `executingLLM` for response generation. `lowCodeLLM` ties them together.
- **Prompts:** The planning and execution prompts are constants in `planningLLM.py` and `executingLLM.py`. Changes to the prompt format must stay consistent with the parser in `planningLLM._txt2json`.
- **Model access:** All LLM calls go through `openAIWrapper.OpenAIWrapper`. On failure, it returns `False` as its status. The planning and execution classes then return the string `"OpenAI API error."`.
- **Contributions:** The root `CONTRIBUTING.md` describes a fork-and-pull-request workflow. It asks contributors to fork the repository, create a branch, commit with a clear message, push the branch, and open a pull request against the upstream repository.

## Testing

The tests are in `src/test/` and use JSON fixtures in `src/test/testcases/`:

| Test file | Fixture | What it checks |
|-----------|---------|----------------|
| `test_get_workflow.py` | `get_workflow_test_cases.json` | Each task prompt produces a workflow with at least one step |
| `test_extend_workflow.py` | `extend_workflow_test_cases.json` | Each extension request returns at least one step |
| `test_execute.py` | `execute_test_cases.json` | Each execution returns a non-empty string |

The tests call the real LLMs, so they need a valid `OPENAIKEY` (and Azure settings if `USE_AZURE=true`). They also sleep for 5 seconds after each case. The test files use `sys.path.append(os.getcwd())` and relative fixture paths (`./test/testcases/...`), so run them from the `src` directory. The supplied files do not include a test runner command or CI configuration.

Note that `test_execute.py` defines its function as `test_extend_workflow`, so the name does not describe what the test checks.

## Visual ChatGPT and TaskMatrix

The repository root includes `visual_chatgpt.py` and a `requirements.txt` for the TaskMatrix Visual ChatGPT system. TaskMatrix.AI is described as an ecosystem that connects foundation models with APIs for task completion. Visual ChatGPT is one example applied to the visual domain. The paper is at [arXiv:2303.16434](https://arxiv.org/abs/2303.16434). The supplied files do not include instructions for running Visual ChatGPT, so this README does not describe them. Refer to the root and TaskMatrix documentation for that material.

## Security

Do not report security vulnerabilities through public GitHub issues. Report them to the Microsoft Security Response Center at [https://msrc.microsoft.com/create-report](https://aka.ms/opensource/security/create-report), or by email to [secure@microsoft.com](mailto:secure@microsoft.com). See `SECURITY.md` for details.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). Send questions or concerns to [opencode@microsoft.com](mailto:opencode@microsoft.com).

## License

This project is released under the MIT License, Copyright (c) 2023 Microsoft. See `LICENSE.txt`.

The TaskMatrix license text also states that the recommended models in the repository are examples for scientific research. Users may replace them. When using the recommended models, users must comply with each model's own license. Microsoft is not liable for third-party rights infringement arising from use of the repository. To report a possible infringement, contact the project owner at the address listed in `LICENSE.txt`.

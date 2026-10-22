# TaskMatrix

TaskMatrix is a Microsoft research repository exploring ways to use foundation models together with APIs and other AI systems to complete tasks across digital and physical domains. The repository contains several related but distinct components:

- **Low-code LLM** (`LowCodeLLM/`) demonstrates a human-in-the-loop interaction pattern. A planning model turns a task into a structured workflow; users can review and refine that workflow; an executing model then responds using the confirmed workflow.
- **Visual ChatGPT** (`visual_chatgpt.py`) is an example of applying the TaskMatrix idea to visual tasks. It combines a language model with tools for interpreting and generating images.
- **TaskMatrix.AI** is described in `TaskMatrix.AI/README.md` as an ecosystem for connecting foundation models with APIs. Its online system is described there as in progress.

The Low-code LLM implementation is described by its own README as a **minimum viable version** focused on demonstrating the interaction concept. For background, see the [Low-code LLM paper](https://arxiv.org/abs/2304.08103) and the [TaskMatrix.AI paper](https://arxiv.org/abs/2303.16434). Visual ChatGPT is discussed in the [Visual ChatGPT paper](https://arxiv.org/abs/2303.04671).

## Low-code LLM overview

The Low-code LLM separates task planning from task execution:

1. The **Planning LLM** generates a structured standard operating procedure (SOP) from a task prompt.
2. A user can review and edit the workflow using the interface’s low-code operations.
3. The **Executing LLM** responds to user input while following the confirmed SOP.
4. The user can continue refining the workflow and responses.

The planner can also generate a detailed sub-workflow for a selected step. Workflow steps can include conditional jump logic. The system’s main implementation is in `LowCodeLLM/src/`: `planningLLM.py` handles workflow planning, `executingLLM.py` handles responses, `lowCodeLLM.py` connects those functions, and `app.py` exposes them through a Flask web application. The application serves its page at `/` and provides three POST API routes: `/api/get_workflow`, `/api/extend_workflow`, and `/api/execute`.

## Setup and run

The documented quick start uses Docker. It requires Docker and credentials for either the OpenAI API or Azure OpenAI Service.

```bash
git clone https://github.com/microsoft/TaskMatrix.git
cd TaskMatrix/LowCodeLLM
docker build -t lowcode:latest .
```

For the OpenAI API, provide an API key when starting the container:

```bash
docker run -p 8888:8888 \
  --env OPENAIKEY=YOUR_PRIVATE_OPENAI_KEY \
  lowcode:latest
```

For Azure OpenAI Service, copy `config.template` to `config.ini`, fill in the required settings, and pass the file to Docker:

```bash
cp config.template config.ini
# Edit config.ini with your Azure OpenAI settings.
docker run -p 8888:8888 --env-file config.ini lowcode:latest
```

After the container starts, open [http://localhost:8888/](http://localhost:8888/) to access the demo page. The application’s Docker image installs the dependencies listed in `LowCodeLLM/src/requirements.txt` and starts Supervisor using `src/supervisord.conf`.

## Configuration

The Low-code LLM’s OpenAI wrapper reads configuration from environment variables:

| Variable | Purpose |
| --- | --- |
| `OPENAIKEY` | API key used to authenticate requests. |
| `USE_AZURE` | Set to `true` to select Azure OpenAI; if absent, the wrapper uses the OpenAI API. |
| `API_BASE` | Azure OpenAI API base URL. |
| `API_VERSION` | Azure OpenAI API version. |
| `MODEL` | Azure deployment/engine name used for chat completion requests. |

For the standard OpenAI API, the wrapper selects `gpt-3.5-turbo`. For Azure, `USE_AZURE` must be set to `true` and the Azure settings must be supplied. Do not commit API keys or other secrets to the repository.

## API usage

Each endpoint expects a JSON request body. Successful calls return the generated result with HTTP status `200`; exceptions are logged and return an `errmsg` field with HTTP status `500`.

- **`POST /api/get_workflow`** — provide `task_prompt` to generate a workflow.
- **`POST /api/extend_workflow`** — provide `task_prompt`, `current_workflow`, and `step` to request a sub-workflow for a step.
- **`POST /api/execute`** — provide `task_prompt`, `confirmed_workflow`, `curr_input`, and `history` to generate a response using the confirmed workflow.

For example, a workflow-generation request has this shape:

```json
{
  "task_prompt": "Write an essay about the effects of drunk driving."
}
```

Workflow results are JSON strings representing arrays of steps. Each step contains `stepId`, `stepName`, `stepDescription`, `jumpLogic`, and `extension` fields. The execution endpoint takes the confirmed workflow as a JSON string and a conversation history represented as a list of role/content messages.

## Development

The Low-code LLM service has its own dependency file, `LowCodeLLM/src/requirements.txt`, which lists Flask, Flask-Cors, OpenAI, Gunicorn, and gevent. The repository-root `requirements.txt` is a separate dependency list for the broader Visual ChatGPT-related code; it includes packages such as PyTorch, Gradio, Transformers, Diffusers, and OpenAI. Install the dependencies appropriate to the component you intend to work on rather than assuming the two manifests describe one unified environment.

To work on the service without Docker, install the Low-code LLM dependencies in a Python environment, then run the Flask application from `LowCodeLLM/src` with the required API environment variables set. The checked-in Dockerfile uses Ubuntu 22.04, installs Python and Supervisor, copies the service source into `/app/src`, and launches Supervisor. The repository also includes Visual ChatGPT’s source script and image/demo assets; its model and tool dependencies are distinct from the Low-code LLM web service.

Follow the contribution steps in [`CONTRIBUTING.md`](CONTRIBUTING.md): fork the repository, create a branch, make and commit changes, then open a pull request. The project has adopted the [Microsoft Open Source Code of Conduct](CODE_OF_CONDUCT.md).

## Testing

Low-code LLM tests are under `LowCodeLLM/src/test/`, with JSON test cases in `LowCodeLLM/src/test/testcases/`. They cover workflow generation, workflow extension, and execution. To run them from the service source directory, install `pytest` if it is not already available, configure valid API credentials, and run:

```bash
cd LowCodeLLM/src
pytest
```

These tests call the configured language-model API; they are not isolated unit tests. The workflow and extension tests parse model output as JSON, and the execution test checks that a non-empty string is returned. The test cases also include short delays between repeated requests.

## License and security

This repository is distributed under the MIT License; see [`LICENSE.txt`](LICENSE.txt) for the complete terms. The license file also notes that recommended models are examples for research and that users must comply with each third-party model’s license. Microsoft disclaims liability for third-party rights infringements resulting from use of the repository.

To report a security vulnerability, do not open a public GitHub issue. Follow the reporting instructions in [`SECURITY.md`](SECURITY.md), which direct reports to the Microsoft Security Response Center or `secure@microsoft.com`.

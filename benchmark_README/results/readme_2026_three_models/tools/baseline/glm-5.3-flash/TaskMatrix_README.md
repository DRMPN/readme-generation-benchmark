# TaskMatrix

**TaskMatrix.AI** is an AI ecosystem that connects foundation models with millions of APIs for task completion. Rather than improving a single AI model, it uses existing foundation models as a brain-like central system and the APIs of other AI models and systems as sub-task solvers to achieve diversified tasks in both digital and physical domains. This repository contains two reference implementations of that vision:

- **Low-code LLM** (`LowCodeLLM/`) — a novel human-LLM interaction pattern that involves the human in the loop to achieve more controllable and stable responses. See the paper [Low-code LLM: Visual Programming over LLMs](https://arxiv.org/abs/2304.08103).
- **Visual ChatGPT** (`visual_chatgpt.py`) — an example of applying TaskMatrix.AI to the visual domain. See the paper [TaskMatrix.AI](https://arxiv.org/abs/2303.16434).

Demo material, including GIFs (`assets/demo.gif`, `assets/demo_short.gif`, `assets/demo_inf.gif`), figures, and a conceptual walkthrough video (`assets/low-code-demovideo.mp4`), is available in the `assets/` directory.

## Repository Layout

```
.
├── LowCodeLLM/                  # Low-code LLM web service and demo
│   ├── Dockerfile               # Ubuntu 22.04 based container image
│   ├── config.template          # Template for Azure OpenAI configuration
│   └── src/
│       ├── app.py               # Flask application and REST API
│       ├── lowCodeLLM.py        # Orchestrates planning and executing LLMs
│       ├── planningLLM.py       # Generates structured workflows (SOPs)
│       ├── executingLLM.py      # Generates responses following a workflow
│       ├── openAIWrapper.py     # OpenAI / Azure OpenAI client wrapper
│       ├── index.html           # Browser-based demo front end
│       ├── supervisord.conf     # Process manager config used in Docker
│       └── test/                # Pytest-style tests and JSON test cases
├── TaskMatrix.AI/README.md      # Project description and paper links
├── visual_chatgpt.py            # Visual ChatGPT implementation
├── requirements.txt             # Dependencies for Visual ChatGPT
├── assets/                      # Demo GIFs, figures, and video
├── CONTRIBUTING.md              # Contribution workflow
├── CODE_OF_CONDUCT.md           # Microsoft Open Source Code of Conduct
├── SECURITY.md                  # Security reporting guidance
└── LICENSE.txt                  # MIT License
```

## Low-code LLM

### How It Works

Human-LLM interaction is completed through the following loop:

- A **Planning LLM** generates a highly structured workflow (a standard operating procedure, or SOP) for a complex task, including steps and conditional jump logic.
- Users edit the workflow with **six kinds of predefined low-code operations**, all supported through clicking, dragging, or text editing.
- An **Executing LLM** generates responses that strictly follow the reviewed workflow.
- Users continue refining the workflow until satisfactory results are obtained.

Key advantages highlighted by the project:

- **Controllable Generation** — tasks are decomposed into structured plans that users can adjust, producing responses more aligned with their requirements.
- **Friendly Interaction** — the intuitive workflow and GUI-based low-code operations mitigate time-consuming prompt engineering.
- **Wide Applicability** — the framework applies to complex tasks across domains, especially where human intelligence or preference is indispensable.

> **Note:** The provided code is a minimum viable version demonstrating the core concept of the Low-code LLM human-LLM interaction. Contributions to improve the front-end interface are welcome.

### Quick Start

Both the OpenAI API and Azure OpenAI Service are supported; API credentials are required in either case.

```bash
# clone the repo
git clone https://github.com/microsoft/TaskMatrix.git

# go to directory
cd LowCodeLLM

# build and run docker
docker build -t lowcode:latest .

# If the OpenAI API is used, only the API key is necessary
docker run -p 8888:8888 --env OPENAIKEY={Your_Private_Openai_Key} lowcode:latest

# For Azure OpenAI Service, duplicate config.template as config.ini,
# fill in the required information, and launch with the config file
docker run -p 8888:8888 --env-file config.ini lowcode:latest
```

Then open the demo page at [http://localhost:8888/](http://localhost:8888/).

### Configuration

The service reads its settings from environment variables:

| Variable | Description |
|---|---|
| `OPENAIKEY` | Your private OpenAI API key. |
| `USE_AZURE` | Set to `true` to use the Azure OpenAI Service instead of the OpenAI API. |
| `API_BASE` | Azure OpenAI endpoint (Azure mode only). |
| `API_VERSION` | Azure OpenAI API version (Azure mode only). |
| `MODEL` | Azure deployment/engine name (Azure mode only). |
| `WORKERS` | Number of service workers, set to `2` in the Dockerfile. |

In OpenAI mode the chat model defaults to `gpt-3.5-turbo`. Requests are sent with `max_tokens` of 2048 and `top_p` of 1. The planning LLM defaults to temperature 0.4 and the executing LLM to temperature 0 (the tests use 0.5 and 0 respectively).

### REST API

The Flask application (`src/app.py`) exposes CORS-enabled endpoints:

- `GET /` — serves the demo front end (`index.html`).
- `POST /api/get_workflow` — body: `{"task_prompt": "..."}`. Returns a workflow in JSON format.
- `POST /api/extend_workflow` — body: `{"task_prompt", "current_workflow", "step"}`. Returns a sub-workflow that expands the given step.
- `POST /api/execute` — body: `{"task_prompt", "confirmed_workflow", "curr_input", "history"}`. Returns the response generated while following the confirmed workflow.

Example:

```bash
curl -X POST http://localhost:8888/api/get_workflow \
     -H "Content-Type: application/json" \
     -d '{"task_prompt": "Write an essay about drunk driving issue."}'
```

On failure, endpoints return HTTP 500 with `{"errmsg": "internal errors"}` and log details.

### Workflow Format

Workflows are JSON arrays of steps, each with an identifier, name, description, optional conditional jump logic, and an `extension` list for sub-steps:

```json
[
  {
    "stepId": "STEP 1",
    "stepName": "Research",
    "stepDescription": "Gather statistics and information about drunk driving issue",
    "jumpLogic": [
      {"Condition": "if 'lack of information'", "Target": "STEP 1"}
    ],
    "extension": []
  }
]
```

Internally, `planningLLM.py` parses the LLM's text-formatted SOP into this JSON structure, and `lowCodeLLM.py` converts JSON workflows back to text before execution.

## Visual ChatGPT

`visual_chatgpt.py` implements a Gradio-based assistant that connects an OpenAI LLM (via a LangChain agent) to visual foundation models. Tools defined in the file include text-to-image generation (Stable Diffusion), image captioning and visual question answering (BLIP), InstructPix2Pix-based instruction-guided editing, and ControlNet-conditioned generation from canny edges, straight lines (MLSD), HED boundaries, sketches, human poses (Openpose), segmentations, depth maps, and normal maps. Supporting dependencies (e.g., `torch`, `diffusers`, `transformers`, `controlnet-aux`, `gradio`, `langchain`) are pinned or listed in the top-level `requirements.txt`. Models are loaded from the Hugging Face Hub, and the code selects `float16` on CUDA devices and `float32` otherwise.

## Development

### Prerequisites

- Docker for running the Low-code LLM service, or Python 3.11 with pip for working on the source directly.
- An OpenAI API key, or an Azure OpenAI deployment with its endpoint, version, and engine name.

### Architecture

- `openAIWrapper.py` — wraps `openai.ChatCompletion.create`, resolves credentials and Azure settings from environment variables, and returns `(response, status)` pairs.
- `planningLLM.py` — prompts the LLM to emit a strictly formatted SOP and parses it into JSON; supports `get_workflow` and `extend_workflow`.
- `executingLLM.py` — conducts the conversation, embedding the SOP as system context; supports `execute`.
- `lowCodeLLM.py` — facade combining both LLMs with JSON/text workflow conversion.
- `app.py` — Flask app with CORS, Gunicorn-aware logging, and the REST routes described above.

The Docker image installs Python 3.11, copies `src/` into `/app/src`, and starts the service with `supervisord -c supervisord.conf`. Gunicorn (listed in `LowCodeLLM/src/requirements.txt`, alongside Flask, Flask-Cors, and gevent) serves the application, and the container exposes port 8888.

## Testing

Tests live in `LowCodeLLM/src/test/` and follow pytest conventions:

- `test_get_workflow.py` — verifies `get_workflow` returns parseable JSON with at least one step for each test case.
- `test_extend_workflow.py` — verifies `extend_workflow` returns a parseable sub-workflow.
- `test_execute.py` — verifies `execute` returns a non-empty string.

Inputs are provided in `test/testcases/` (`get_workflow_test_cases.json`, `extend_workflow_test_cases.json`, `execute_test_cases.json`). The tests invoke the live OpenAI API, so `OPENAIKEY` must be set (plus the Azure variables when applicable), and some tests sleep five seconds between cases to pace API calls. Run them from the source directory:

```bash
cd LowCodeLLM/src
export OPENAIKEY={Your_Private_Openai_Key}
python -m pytest test/
```

Note that `pytest` itself is not listed in `LowCodeLLM/src/requirements.txt` and may need to be installed separately.

## Contributing

Contributions follow the standard fork-and-pull-request workflow described in [CONTRIBUTING.md](CONTRIBUTING.md): fork the repository, create a feature branch, commit changes with meaningful messages, push to your fork, and open a pull request for maintainer review.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). Questions or concerns can be directed to [opencode@microsoft.com](mailto:opencode@microsoft.com).

## Security

Per [SECURITY.md](SECURITY.md), please do not report security vulnerabilities through public GitHub issues. Instead, report them to the Microsoft Security Response Center at [https://msrc.microsoft.com/create-report](https://msrc.microsoft.com/create-report) or via email to [secure@microsoft.com](mailto:secure@microsoft.com). Microsoft follows Coordinated Vulnerability Disclosure.

## License

This project is licensed under the [MIT License](LICENSE.txt) (© 2023 Microsoft). The recommended models in this repository are examples used for scientific research exploring task automation; users who use those models must comply with the respective model licenses, and Microsoft shall not be held liable for infringement of third-party rights resulting from usage of this repository. Inquiries regarding rights can be sent to the project owner at [chewu@microsoft.com](mailto:chewu@microsoft.com).

## Acknowledgement

Part of the Low-code LLM paper was collaboratively crafted through interactions with the proposed system: GPT-4 outlined the framework, the authors supplemented it with ideas and refined the workflow structure, and GPT-4 generated the final cohesive text.

# TaskMatrix

**TaskMatrix.AI** is an AI ecosystem that can connect foundation models with millions of APIs for task completion. Unlike most previous work that aimed to improve a single AI model, TaskMatrix.AI focuses on using existing foundation models (as a brain-like central system) and APIs of other AI models and systems (as sub-task solvers) to achieve diversified tasks in both digital and physical domains.

This repository contains:

| Component | Description |
|---|---|
| [Visual ChatGPT](#visual-chatgpt) | A single-file demo (`visual_chatgpt.py`) that connects ChatGPT and a series of Visual Foundation Models to enable sending and receiving images during chatting. |
| [TaskMatrix.AI](#taskmatrixai) | Concept documentation for the TaskMatrix.AI ecosystem (see `TaskMatrix.AI/README.md`). |
| [Low-code LLM](#low-code-llm) | A demo of the low-code human–LLM interaction pattern (see `LowCodeLLM/`), including a Dockerized Flask app. |

## Papers

- [Visual ChatGPT: Talking, Drawing and Editing with Visual Foundation Models](https://arxiv.org/abs/2303.04671)
- [TaskMatrix.AI: Completing Tasks by Connecting Foundation Models with Millions of APIs](https://arxiv.org/abs/2303.16434)
- [Low-code LLM: Visual Programming over LLMs](https://arxiv.org/abs/2304.08103)

## Visual ChatGPT

Visual ChatGPT is a visual dialogue assistant built on ChatGPT. Since the language model cannot read images directly, `visual_chatgpt.py` exposes a set of Visual Foundation Models as [LangChain](https://github.com/hwchase17/langchain) tools; a LangChain conversational-reAct agent decides which tools to call, and the UI displays the images that the tools produce and reference by file name.

<img src="assets/figure.jpg" alt="Visual ChatGPT system figure" width="800">

The UI supports both **English** and **Chinese** (a language selector appears at the top of the chat).

### Quick Start

```bash
# clone the repository
git clone https://github.com/microsoft/TaskMatrix.git
cd TaskMatrix

# install dependencies
pip install -r requirements.txt

# launch the demo
python visual_chatgpt.py --load "ImageCaptioning_cuda:0,Text2Image_cuda:0"
```

This starts a Gradio web UI on port **7861** (`0.0.0.0:7861`).

Notes:

- The agent calls the OpenAI API through LangChain's `OpenAI` client, which reads the standard `OPENAI_API_KEY` environment variable.
- The `--load` argument is a comma-separated list of `ModelName_device` entries that selects which Visual Foundation Models are loaded and where they are placed, e.g. `ImageCaptioning_cuda:0,Text2Image_cuda:0`. You can load multiple models across devices, e.g. `{'VisualQuestionAnswering': 'cuda:0', 'ImageCaptioning': 'cuda:1'}`. Models run in `float16` on CUDA devices and `float32` otherwise.
- `ImageCaptioning` must be loaded; the program raises a `ValueError` without it.
- Model weights are downloaded on startup (into a `checkpoints/` directory, which is created automatically), and generated/edited images are stored under an `image/` directory.
- `visual_chatgpt.py` additionally imports `groundingdino` and `segment_anything`, which are **not** listed in `requirements.txt`.

### Available Tools

The tools registered with the agent (name in the agent's tool list → backing implementation in `visual_chatgpt.py`):

| Tool | Implementation |
|---|---|
| Instruct Image Using Text | `InstructPix2Pix` |
| Generate Image From User Input Text | `Text2Image` |
| Get Photo Description | `ImageCaptioning` |
| Answer Question About The Image | `VisualQuestionAnswering` |
| Edge Detection On Image | `Image2Canny` |
| Generate Image Condition On Canny Image | `CannyText2Image` |
| Line Detection On Image | `Image2Line` |
| Generate Image Condition On Line Image | `LineText2Image` |
| Hed Detection On Image | `Image2Hed` |
| Generate Image Condition On Soft Hed Boundary Image | `HedText2Image` |
| Sketch Detection On Image | `Image2Scribble` |
| Generate Image Condition On Sketch Image | `ScribbleText2Image` |
| Pose Detection On Image | `Image2Pose` |
| Generate Image Condition On Pose Image | `PoseText2Image` |
| Generate Image Condition On Segmentations | `SegText2Image` |
| Predict Depth On Image | `Image2Depth` |
| Generate Image Condition On Depth | `DepthText2Image` |
| Predict Normal Map On Image | `Image2Normal` |
| Generate Image Condition On Normal Map | `NormalText2Image` |
| Segment the Image | `Segmenting` |
| Detect the Give Object | `Text2Box` |
| Extend An Image | `InfinityOutPainting` |
| Segment the given object | `ObjectSegmenting` |
| Remove Something From The Photo | `ImageEditing` |
| Replace Something From The Photo | `ImageEditing` |
| Remove the background | `BackgroundRemoving` |

Template models (`InfinityOutPainting`, `ObjectSegmenting`, `ImageEditing`, `BackgroundRemoving`) are composite tools that are assembled automatically from the loaded base models, so the corresponding base models must be included in `--load` for them to appear.

## TaskMatrix.AI

**TaskMatrix.AI** connects foundation models with APIs of other AI models and systems for task completion. Visual ChatGPT is an example of applying TaskMatrix.AI to the visual domain. See [`TaskMatrix.AI/README.md`](TaskMatrix.AI/README.md) for details.

- **Paradigm Shift**

  <img src="assets/paradigm.png" alt="paradigm" width="1000">

- **System Overview**

  <img src="assets/overview.png" alt="overview" width="1000">

## Low-code LLM

**Low-code LLM** is a novel human–LLM interaction pattern that involves humans in the loop to achieve more controllable and stable responses. A conceptual video demo is available at [`assets/low-code-demovideo.mp4`](assets/low-code-demovideo.mp4).

<img src="assets/low-code-llm.png" alt="low-code LLM overview" width="800">

The human–LLM interaction proceeds as follows:

- A **Planning LLM** generates a highly structured workflow (a standard operating procedure with steps and conditional jump logic) for a complex task.
- The user edits the workflow with predefined **low-code operations**, all supported by clicking, dragging, or text editing.
- An **Executing LLM** generates responses by following the reviewed workflow.
- The user continues to refine the workflow until satisfactory results are obtained.

<img src="assets/low-code-operation.png" alt="six low-code operations" width="800">

### Quick Start

> Note: the code provided here is a minimal viable version demonstrating the core concept of the low-code human–LLM interaction. Both the **OpenAI API** and the **Azure OpenAI Service** are supported; you must provide the credentials to invoke these APIs.

```bash
# clone the repo
git clone https://github.com/microsoft/TaskMatrix.git
cd LowCodeLLM

# build and run docker
docker build -t lowcode:latest .

# If the OpenAI API is used, only the API key is required
docker run -p 8888:8888 --env OPENAIKEY={Your_Private_Openai_Key} lowcode:latest

# When using the Azure OpenAI Service, store the necessary information in a
# config file: duplicate config.template as config.ini and fill it in
docker run -p 8888:8888 --env-file config.ini lowcode:latest
```

Then open the demo page at <http://localhost:8888/>.

Configuration variables (see `LowCodeLLM/config.template`):

| Variable | Purpose |
|---|---|
| `OPENAIKEY` | OpenAI (or Azure OpenAI) API key |
| `USE_AZURE` | Set to `True` to use the Azure OpenAI Service |
| `API_BASE` | Azure service base URL |
| `API_VERSION` | Azure API version |
| `MODEL` | Azure deployment (engine) name |

Without `USE_AZURE=True`, the wrapper calls the OpenAI chat model `gpt-3.5-turbo`.

### Implementation

- `LowCodeLLM/src/app.py` — Flask app serving the web page (`index.html`) and the JSON API below; run under gunicorn (gevent workers) via `supervisord` inside the Docker image, bound to `0.0.0.0:8888`.
- `LowCodeLLM/src/lowCodeLLM.py` — orchestrates the two LLMs and converts workflows between JSON and text form.
- `LowCodeLLM/src/planningLLM.py` — the Planning LLM: generates a standard operating procedure as text and parses it into a JSON workflow (steps with names, descriptions, jump logic, and extensions).
- `LowCodeLLM/src/executingLLM.py` — the Executing LLM: answers user messages while strictly following the confirmed workflow.
- `LowCodeLLM/src/openAIWrapper.py` — thin wrapper around the OpenAI/Azure chat-completion API, configured from environment variables.

HTTP API (JSON over POST):

| Endpoint | Input fields | Behavior |
|---|---|---|
| `/api/get_workflow` | `task_prompt` | Generates the initial workflow for the task. |
| `/api/extend_workflow` | `task_prompt`, `current_workflow`, `step` | Generates a sub-workflow that expands the given step. |
| `/api/execute` | `task_prompt`, `confirmed_workflow`, `curr_input`, `history` | Produces a response that follows the confirmed workflow. |

### Tests

`LowCodeLLM/src/test/` contains pytest-style tests (`test_get_workflow.py`, `test_extend_workflow.py`, `test_execute.py`) driven by JSON cases in `LowCodeLLM/src/test/testcases/`. They instantiate the real `lowCodeLLM` and call the OpenAI API, so valid API credentials are required to run them.

## Repository Structure

```
.
├── visual_chatgpt.py          # Visual ChatGPT demo (Gradio + LangChain)
├── requirements.txt           # Python dependencies for Visual ChatGPT
├── TaskMatrix.AI/
│   └── README.md              # TaskMatrix.AI concept and paper
├── LowCodeLLM/
│   ├── Dockerfile             # Ubuntu 22.04 image; runs supervisord → gunicorn
│   ├── config.template        # Azure OpenAI configuration template
│   ├── README.md              # Low-code LLM overview and usage
│   └── src/
│       ├── app.py             # Flask app and JSON API
│       ├── index.html         # Web front end
│       ├── lowCodeLLM.py      # Planning LLM + Executing LLM orchestration
│       ├── planningLLM.py     # Workflow generation
│       ├── executingLLM.py    # Workflow-guided execution
│       ├── openAIWrapper.py   # OpenAI/Azure API wrapper
│       ├── supervisord.conf   # Process manager config
│       └── test/              # pytest-style tests and JSON test cases
└── assets/                    # Figures and demo videos/GIFs
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the fork–branch–pull-request workflow used by this project.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](CODE_OF_CONDUCT.md).

## Security

See [SECURITY.md](SECURITY.md). Please do not report security vulnerabilities through public GitHub issues; use the Microsoft Security Response Center instead.

## License

This repository is licensed under the [MIT License](LICENSE.txt) (Copyright © 2023 Microsoft). The recommended models in this repo are examples for research; when using them, you need to comply with their respective licenses — see the note in [LICENSE.txt](LICENSE.txt).

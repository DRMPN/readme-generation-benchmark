# README

# TaskMatrix.ai: Low-Code LLM Demo

This repository contains a demo implementation of **TaskMatrix** — a framework that connects large language models (LLMs) with external APIs and tools, allowing users to solve complex tasks through a **low-code, natural language workflow builder**.

The project combines several cooperating LLM agents:

- **Planning LLM** (`planningLLM.py`) — decomposes a user's high-level request into a structured workflow of steps.
- **Low-Code LLM** (`lowCodeLLM.py`) — lets users review and edit the generated workflow in a low-code manner (approving, modifying, or extending steps).
- **Executing LLM** (`executingLLM.py`) — maps each workflow step to the appropriate API/tool and executes it, returning results to the user.
- **OpenAI Wrapper** (`openAIWrapper.py`) — a thin wrapper around the OpenAI API used by all agents.

A visual overview of the architecture is shown in `overview.png` and `low-code-llm.png`; the paradigm is illustrated in `paradigm.png`.

---

## ✨ Features

- **Task decomposition**: automatically converts a natural-language request into an executable multi-step workflow.
- **Human-in-the-loop editing**: users can inspect, modify, and extend the generated workflow before execution (low-code interaction).
- **Tool/API execution**: each step is grounded in a concrete API, and execution results are fed back to refine subsequent steps.
- **Web demo UI**: an interactive browser interface (`index.html`, served via `app.py`).
- **Visual ChatGPT integration**: optional image-generation and image-editing capabilities via `visual_chatgpt.py`.
- **Test coverage**: unit tests for workflow generation (`test_get_workflow.py`), workflow extension (`test_extend_workflow.py`), and execution (`test_execute.py`), with fixture files in JSON.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- An OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/microsoft/TaskMatrix.git
cd TaskMatrix-do0cqeu6

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy the template configuration and add your credentials:

```bash
cp config.template config
```

Then edit `config` and set, at minimum:

```
OPENAI_API_KEY=<your OpenAI API key>
```

Additional options (ports, model names, cache paths, etc.) are documented inside `config.template`.

### Running the Demo

```bash
python app.py
```

Then open `http://localhost:7860` (or the port configured in `supervisord.conf`) in your browser. A sample UI screenshot is available in `demo_short.gif` and `demo.gif`.

---

## 🧩 Project Structure

```
├── app.py                          # Web application entry point
├── planningLLM.py                  # Planner agent: request → workflow
├── lowCodeLLM.py                   # Low-code agent: workflow review/editing
├── executingLLM.py                 # Executor agent: workflow → API calls
├── openAIWrapper.py                # OpenAI API wrapper
├── visual_chatgpt.py               # Visual (image) tool integration
├── index.html                      # Frontend UI
├── config.template                 # Configuration template
├── supervisord.conf                # Process manager config for deployment
├── Dockerfile                      # Container build
├── requirements.txt                # Python dependencies
├── test_get_workflow.py            # Tests for workflow planning
├── test_extend_workflow.py         # Tests for workflow extension
├── test_execute.py                 # Tests for execution
├── get_workflow_test_cases.json    # Test fixtures (planning)
├── extend_workflow_test_cases.json # Test fixtures (extension)
├── execute_test_cases.json         # Test fixtures (execution)
└── media assets                    # overview.png, paradigm.png, demo gifs, video
```

---

## 🧪 Running Tests

```bash
python -m pytest
# or individually:
python test_get_workflow.py
python test_extend_workflow.py
python test_execute.py
```

Test case inputs/expected outputs are provided in the accompanying JSON fixture files.

---

## 🐳 Docker

```bash
docker build -t taskmatrix-demo .
docker run -p 7860:7860 --env-file config taskmatrix-demo
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. For security issues, refer to [SECURITY.md](SECURITY.md).

## 📜 License & Code of Conduct

This project is released under the license in [LICENSE.txt](LICENSE.txt). By participating, you agree to abide by the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## 🔗 Resources

- Architecture overview: `overview.png`, `paradigm.png`
- Demo video: `low-code-demovideo.mp4`
- Demo animations: `demo.gif`, `demo_short.gif`, `demo_inf.gif`

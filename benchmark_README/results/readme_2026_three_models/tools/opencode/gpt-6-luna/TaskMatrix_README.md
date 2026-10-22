# TaskMatrix

TaskMatrix is a research repository exploring how foundation models can coordinate specialized models and tools to carry out tasks. This checkout contains two related demonstrations:

- **Visual ChatGPT** (`visual_chatgpt.py`): a Gradio chat application that uses a language model to select visual tools for image understanding and editing.
- **Low-code LLM** (`LowCodeLLM/`): a web demo where a user can review and edit a workflow proposed by a planning LLM before an executing LLM uses it to answer.

The projects illustrate different ideas and have separate dependencies and startup instructions. The repository does not include a single unified launcher.

## Contents

```text
.
├── visual_chatgpt.py       # Visual ChatGPT application
├── requirements.txt        # Python dependencies for Visual ChatGPT
├── LowCodeLLM/             # Low-code LLM web application and Dockerfile
├── TaskMatrix.AI/          # Brief TaskMatrix.AI description
├── assets/                 # Figures and demo media
├── LICENSE.txt
└── ...                     # Contribution, conduct, and security guidance
```

## Visual ChatGPT

Visual ChatGPT connects a conversational language model to image tools. Depending on which classes are loaded, the tools in `visual_chatgpt.py` include captioning and visual question answering, text-to-image generation, image-to-image editing, edge/line/pose/depth/normal-map processing, segmentation, object detection, inpainting, outpainting, and background removal. It supports English and Chinese interface prompts.

### Requirements and setup

The root [`requirements.txt`](requirements.txt) lists the Python dependencies, including PyTorch, Transformers, Diffusers, Gradio, and LangChain. Install them in an appropriate Python environment:

```bash
python -m pip install -r requirements.txt
```

This list does **not** install the `groundingdino` and `segment_anything` modules imported by `visual_chatgpt.py`. Those modules are not present in this checkout; install and configure their source separately if you need the related object detection and segmentation tools. The app also downloads pretrained model weights from their configured model sources when initializing tools, and some tools may download checkpoints into `checkpoints/`. Access to those sources and sufficient compute, especially for diffusion models, may be needed.

The application uses LangChain's OpenAI integration for chat; configure `OPENAI_API_KEY` in the environment before launching, for example with `export OPENAI_API_KEY=YOUR_OPENAI_API_KEY`. A GPU is not specified as a universal requirement by the code, but the default launch configuration selects CUDA device `cuda:0` and is intended for a CUDA-capable setup.

### Run

From the repository root, run:

```bash
python visual_chatgpt.py
```

This starts the Gradio interface on port `7861` and binds it to `0.0.0.0`. The default `--load` value initializes image captioning and text-to-image generation on `cuda:0`. The option accepts a comma-separated list of `ClassName_device` entries, for example:

```bash
python visual_chatgpt.py --load 'ImageCaptioning_cuda:0,Text2Image_cuda:0'
```

`ImageCaptioning` must be included. The classes and device values are parsed from `--load` in `visual_chatgpt.py`; each selected model is initialized at startup, which may download weights and use substantial memory.

## Low-code LLM

Low-code LLM is a human-in-the-loop workflow interface. Its planning LLM proposes a structured workflow for a task; the user can review or modify it, then the executing LLM responds using the confirmed workflow. The interface also supports extending a selected workflow step. The accompanying README describes the implementation as a minimum viable version.

### Run with Docker

Build the image from the `LowCodeLLM/` directory:

```bash
cd LowCodeLLM
docker build -t lowcode:latest .
```

For the OpenAI configuration documented by the project, provide an API key and publish port `8888`:

```bash
docker run --rm -p 8888:8888 \
  --env OPENAIKEY=YOUR_OPENAI_API_KEY \
  lowcode:latest
```

For Azure OpenAI, copy `config.template` to `config.ini`, fill in the values, and pass the file as an environment file:

```bash
cp config.template config.ini
# Edit config.ini with your Azure key, endpoint, API version, and deployment name.
docker run --rm -p 8888:8888 --env-file config.ini lowcode:latest
```

The template provides `USE_AZURE`, `OPENAIKEY`, `API_BASE`, `API_VERSION`, and `MODEL`. Keep credentials private and do not commit a populated configuration file. After the container starts, open [http://localhost:8888/](http://localhost:8888/).

The service exposes its workflow and execution operations at `/api/get_workflow`, `/api/extend_workflow`, and `/api/execute` (POST). The request fields are read by the handlers in `LowCodeLLM/src/app.py`.

## Research papers and project context

- [Visual ChatGPT: Talking, Drawing and Editing with Visual Foundation Models](https://arxiv.org/abs/2303.04671)
- [TaskMatrix.AI](https://arxiv.org/abs/2303.16434)
- [Low-code LLM: Visual Programming over LLMs](https://arxiv.org/abs/2304.08103)

The `TaskMatrix.AI/README.md` describes TaskMatrix.AI as a broader ecosystem concept; Visual ChatGPT is presented there as an application of that idea to the visual domain.

## License and third-party models

The repository is distributed under the MIT License; see [`LICENSE.txt`](LICENSE.txt). The license file notes that the recommended models are examples for research and that each third-party model has its own license terms. Review and comply with those terms when downloading or using model weights. The repository license does not replace third-party model licenses.

## Contributing and security

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution guidance and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for the project code of conduct. Please follow [`SECURITY.md`](SECURITY.md) when reporting a security issue.

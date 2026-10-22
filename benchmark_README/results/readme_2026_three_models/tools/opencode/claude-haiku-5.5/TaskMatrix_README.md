# TaskMatrix

This repository contains two related research projects from Microsoft:

- **Visual ChatGPT** (`visual_chatgpt.py`): a Gradio chat app in which a language model (via OpenAI) uses a set of visual foundation models as tools to understand, generate, and edit images.
- **Low-code LLM** (`LowCodeLLM/`): a Flask web app in which a planning LLM drafts an editable step-by-step workflow for a task, and an executing LLM answers the user while following the workflow the user has confirmed.

The repository is released under the MIT License (see [LICENSE.txt](LICENSE.txt)).

## Background

- **TaskMatrix.AI** ([arXiv:2303.16434](https://arxiv.org/abs/2303.16434)) describes an ecosystem that uses existing foundation models as a central system and connects them to APIs of other AI models and systems to complete tasks in digital and physical domains. Visual ChatGPT is an example of applying this approach to the visual domain.
- **Low-code LLM: Visual Programming over LLMs** ([arXiv:2304.08103](https://arxiv.org/abs/2304.08103)) proposes a human-in-the-loop interaction pattern in which users review and edit an LLM-generated workflow before the LLM produces responses.

The repository does not include an online demo for TaskMatrix.AI; its README lists it as "in progress."

## Repository Layout

| Path | Description |
| --- | --- |
| `visual_chatgpt.py` | Visual ChatGPT application: tool classes, agent setup, and Gradio UI. |
| `requirements.txt` | Python dependencies for Visual ChatGPT. |
| `LowCodeLLM/` | Low-code LLM project (see its own [README](LowCodeLLM/README.md)). |
| `LowCodeLLM/Dockerfile` | Builds a container that serves the Low-code LLM web app. |
| `LowCodeLLM/config.template` | Template for environment variables used by Low-code LLM. |
| `LowCodeLLM/src/` | Low-code LLM server code, web front end (`index.html`), and tests. |
| `TaskMatrix.AI/README.md` | Short project description for TaskMatrix.AI. |
| `assets/` | Images, GIFs, and a video used in the documentation. |
| `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` | Contribution, conduct, and security policies. |

## Visual ChatGPT

Visual ChatGPT lets you chat with a language model about images. You can upload an image, ask questions about it, and ask for new images to be generated or edited. The agent picks which tools to call. Images are saved under `image/`. Text-to-image tools save files named with an 8-character random ID (for example `image/3f2a9c1b.png`), and tools that transform an existing image save files named `<4-char-id>_<operation>_<previous-name>_<original-name>.png`. The agent is instructed to refer to images only by the filenames returned by tools.

![Visual ChatGPT demo](assets/demo_short.gif)

### Tools

Each tool is a method on a class in `visual_chatgpt.py`. The name below is the name the agent sees.

| Tool name | Model or method | What it does |
| --- | --- | --- |
| Generate Image From User Input Text | `Text2Image` (Stable Diffusion v1.5) | Generates an image from text. |
| Get Photo Description | `ImageCaptioning` (BLIP captioning) | Describes an image. |
| Answer Question About The Image | `VisualQuestionAnswering` (BLIP VQA) | Answers a question about an image. |
| Instruct Image Using Text | `InstructPix2Pix` | Edits an image according to a text instruction. |
| Edge Detection On Image | `Image2Canny` (OpenCV Canny) | Produces a Canny edge image. |
| Generate Image Condition On Canny Image | `CannyText2Image` (ControlNet) | Generates an image from a Canny edge image and a text description. |
| Line Detection On Image | `Image2Line` (MLSD) | Detects straight lines. |
| Generate Image Condition On Line Image | `LineText2Image` (ControlNet) | Generates an image from a line image and a text description. |
| Hed Detection On Image | `Image2Hed` (HED) | Produces a soft HED boundary image. |
| Generate Image Condition On Soft Hed Boundary Image | `HedText2Image` (ControlNet) | Generates an image from a HED image and a text description. |
| Sketch Detection On Image | `Image2Scribble` (HED, scribble mode) | Produces a scribble/sketch image. |
| Generate Image Condition On Sketch Image | `ScribbleText2Image` (ControlNet) | Generates an image from a scribble and a text description. |
| Pose Detection On Image | `Image2Pose` (OpenPose) | Detects human poses. |
| Generate Image Condition On Pose Image | `PoseText2Image` (ControlNet) | Generates an image from a pose image and a text description. |
| Predict Depth On Image | `Image2Depth` (Hugging Face depth-estimation pipeline) | Estimates a depth map. |
| Generate Image Condition On Depth | `DepthText2Image` (ControlNet) | Generates an image from a depth map and a text description. |
| Predict Normal Map On Image | `Image2Normal` (DPT hybrid MiDaS + Sobel gradients) | Estimates a normal map. |
| Generate Image Condition On Normal Map | `NormalText2Image` (ControlNet) | Generates an image from a normal map and a text description. |
| Segment the Image | `Segmenting` (Segment Anything, automatic mask generator) | Segments all objects in an image. |
| Segment the given object | `ObjectSegmenting` (Grounding DINO + SAM) | Segments objects matching a text description. |
| Detect the Give Object | `Text2Box` (Grounding DINO) | Draws bounding boxes around objects matching a text description. |
| Generate Image Condition On Segmentations | `SegText2Image` (ControlNet) | Generates an image from a segmentation image and a text description. |
| Extend An Image | `InfinityOutPainting` | Extends an image to a larger resolution using captions and inpainting. |
| Remove Something From The Photo | `ImageEditing` (Grounding DINO + SAM + inpainting) | Removes an object and fills the area. |
| Replace Something From The Photo | `ImageEditing` (Grounding DINO + SAM + inpainting) | Replaces an object with a described object. |
| Remove the background | `BackgroundRemoving` | Keeps the main object and makes the background transparent. |

The `Segmenting`, `Text2Box`, `Inpainting`, and `ImageEditing` classes are also used internally by other tools. `Inpainting` has no tool entry of its own.

### Requirements

- Python dependencies from `requirements.txt`. The file pins `langchain==0.0.101`, `torch==1.13.1`, and `torchvision==0.14.1`; the other packages are not pinned.
- `visual_chatgpt.py` also imports the `groundingdino` and `segment_anything` packages. These are **not** listed in `requirements.txt` and must be installed separately.
- An OpenAI API key. The agent uses LangChain's `OpenAI` client, which reads the `OPENAI_API_KEY` environment variable.
- GPU memory and disk space for the models you choose to load. The default configuration assumes a CUDA device (`cuda:0`). The code also accepts other device strings, such as `cpu`, and uses float32 when the device is not CUDA.
- Internet access on first run. Model weights are downloaded automatically (see below).

### Running

```bash
pip install -r requirements.txt
# Also install groundingdino and segment_anything (see Requirements above).
export OPENAI_API_KEY=your-openai-key

python visual_chatgpt.py --load "ImageCaptioning_cuda:0,Text2Image_cuda:0"
```

The app starts a Gradio server on `0.0.0.0:7861`. Open it in a browser at `http://localhost:7861`.

The `--load` option takes a comma-separated list of `ClassName_device` pairs. For example:

```bash
python visual_chatgpt.py --load "ImageCaptioning_cuda:0,Text2Image_cuda:0,Image2Canny_cpu,CannyText2Image_cuda:0"
```

- `ImageCaptioning` must always be loaded; the program raises an error without it.
- Composite tools (`InfinityOutPainting`, `ObjectSegmenting`, `ImageEditing`, `BackgroundRemoving`) are created automatically once all classes they depend on are loaded. For example, `ImageEditing` needs `Text2Box`, `Segmenting`, and `Inpainting`.
- The default `--load` value loads only `ImageCaptioning` and `Text2Image`.

In the UI, choose a language (Chinese or English), then type a message or use the image button to upload an image. The **Clear** button resets the conversation.

### Model Downloads

On first load, the following are downloaded automatically:

- Hugging Face models, including `runwayml/stable-diffusion-v1-5`, `runwayml/stable-diffusion-inpainting`, `timbrooks/instruct-pix2pix`, `CompVis/stable-diffusion-safety-checker`, `Salesforce/blip-image-captioning-base`, `Salesforce/blip-vqa-base`, `Intel/dpt-hybrid-midas`, several `fusing/stable-diffusion-v1-5-controlnet-*` ControlNet models, and the default depth-estimation pipeline.
- Segment Anything ViT-H weights, saved to `checkpoints/sam`.
- Grounding DINO SwinT weights, saved to `checkpoints/groundingdino`, and its config, saved to `checkpoints/grounding_config.py`.

The `checkpoints/` directory is created automatically when the program starts.

### Known Limitations

- The code is not pinned for all of its dependencies. For example, `InfinityOutPainting` uses `Image.ANTIALIAS`, which was removed in Pillow 10, and the Gradio UI uses the `.style(...)` API from older Gradio versions. Pin compatible versions if you hit errors.
- The Gradio app is launched with `demo.launch(server_name="0.0.0.0", server_port=7861)`. Restrict network access if you do not want it reachable from other machines.

## Low-code LLM

Low-code LLM is a minimum viable web app that demonstrates the interaction pattern from the paper. The user:

1. Enters a task. The **planning LLM** returns a step-by-step workflow, with optional conditional jumps between steps.
2. Edits the workflow with the predefined low-code operations shown in the figure below.
3. Chats with the **executing LLM**, which answers while following the confirmed workflow without showing the steps to the user.
4. Refines the workflow until the results are satisfactory.

![Low-code LLM system overview](assets/low-code-llm.png)

![Low-code LLM operations](assets/low-code-operation.png)

The code provides the core concept only, and the front end is minimal. The authors welcome contributions to the interface.

A conceptual demo video is at `assets/low-code-demovideo.mp4`.

### How It Works

- `LowCodeLLM/src/planningLLM.py` generates a workflow in a text format (`STEP n: [name][description][[[if 'condition'][Jump to STEP m]]]`) and converts it to JSON. Each step has `stepId`, `stepName`, `stepDescription`, `jumpLogic`, and `extension` fields.
- `LowCodeLLM/src/executingLLM.py` receives the task, the confirmed workflow, and the chat history. It is instructed to follow the workflow and not to expose it to the user.
- `LowCodeLLM/src/openAIWrapper.py` calls the OpenAI Chat Completions API, either directly or through Azure OpenAI.
- Planning uses temperature 0.4 and execution uses temperature 0 (set in `lowCodeLLM.py`).

### API Endpoints

The Flask server is in `LowCodeLLM/src/app.py`. All endpoints accept JSON `POST` bodies.

| Endpoint | Request fields | Response |
| --- | --- | --- |
| `POST /api/get_workflow` | `task_prompt` | The workflow as a JSON-encoded string. |
| `POST /api/extend_workflow` | `task_prompt`, `current_workflow`, `step` | A sub-workflow (steps named like `STEP 2.1`) as a JSON-encoded string. |
| `POST /api/execute` | `task_prompt`, `confirmed_workflow`, `curr_input`, `history` | The executing LLM's reply. |

If a request raises an exception, the server returns HTTP 500 with `{"errmsg": "internal errors"}`. If the OpenAI call fails inside the planning or executing LLM, the response is the string `OpenAI API error.` with HTTP 200.

The web front end (`LowCodeLLM/src/index.html`) sends requests to `http://127.0.0.1:8888`, so the server must run on that address for the bundled UI to work.

### Configuration

Copy `LowCodeLLM/config.template` to `config.ini` and fill in the values:

| Variable | Purpose |
| --- | --- |
| `USE_AZURE` | `True` to use Azure OpenAI; anything else uses the standard OpenAI API. |
| `OPENAIKEY` | API key for OpenAI or Azure OpenAI. |
| `API_BASE` | Azure OpenAI endpoint base URL (Azure only). |
| `API_VERSION` | Azure OpenAI API version (Azure only). |
| `MODEL` | Azure OpenAI deployment name (Azure only). |

With the standard OpenAI API, the code uses the model `gpt-3.5-turbo`.

### Running with Docker

```bash
cd LowCodeLLM

# Build the image.
docker build -t lowcode:latest .

# Standard OpenAI API: pass only the key.
docker run -p 8888:8888 --env OPENAIKEY={Your_Private_Openai_Key} lowcode:latest

# Azure OpenAI: pass the config file.
docker run -p 8888:8888 --env-file config.ini lowcode:latest
```

Then open `http://localhost:8888/`.

The image is based on Ubuntu 22.04 and installs Python 3.11 and `supervisor`. `supervisord.conf` starts Gunicorn on `0.0.0.0:8888` with the `gevent` worker class and a 300-second timeout.

### Running Without Docker

Install the packages in `LowCodeLLM/src/requirements.txt`, set the environment variables from the configuration table, and start the server from the `LowCodeLLM/src` directory:

```bash
cd LowCodeLLM/src
pip install -r requirements.txt
gunicorn --timeout 300 --bind "0.0.0.0:8888" "app:app" --worker-class gevent
```

### Tests

Tests are in `LowCodeLLM/src/test/`, with cases in `LowCodeLLM/src/test/testcases/`. The `test_get_workflow.py` test calls the configured LLM through `lowCodeLLM`, so it needs valid API credentials and network access. Run tests from `LowCodeLLM/src`, because the test code reads cases from `./test/testcases/`. `pytest` is not listed in `requirements.txt`, so install it separately.

## Documentation Assets

The `assets/` folder contains:

- `paradigm.png` and `overview.png`: TaskMatrix.AI diagrams.
- `demo.gif`, `demo_short.gif`, and `demo_inf.gif`: Visual ChatGPT demos.
- `figure.jpg`: an image file that is not referenced by the README.
- `low-code-llm.png`, `low-code-operation.png`, and `low-code-demovideo.mp4`: Low-code LLM figures and video.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the fork-and-pull-request workflow. Please also read the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

To report a security vulnerability, follow the instructions in [SECURITY.md](SECURITY.md).

## License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt).

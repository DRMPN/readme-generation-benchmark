# ChatGLM-6B

This repository contains example code for running **ChatGLM-6B**, a conversational language model, with command-line and browser demos. It also includes an HTTP API example, multi-GPU loading helpers, a P-Tuning v2 fine-tuning implementation, and separate demos for the image-capable VisualGLM-6B model.

The demos load model files from Hugging Face using `trust_remote_code=True`. Review the model code and the applicable terms before using it. The repository does not include the model weights; they are downloaded when the model is first loaded unless you configure a local model directory.

## Contents

- `cli_demo.py` — interactive command-line chat with streamed output.
- `web_demo.py` — Gradio browser chat with conversation history and generation controls.
- `web_demo2.py` — alternate Streamlit chat demo.
- `api.py` — a FastAPI endpoint for chat requests.
- `utils.py` — helpers for distributing the model over multiple GPUs.
- `ptuning/` — P-Tuning v2 training, evaluation, and deployment code; see [`ptuning/README.md`](ptuning/README.md).
- `cli_demo_vision.py` and `web_demo_vision.py` — demos for **VisualGLM-6B**, a separate model that accepts images.
- `FAQ.md`, `UPDATE.md`, and `improve/README.md` — troubleshooting, historical project updates, and the bad-case feedback plan.

## Requirements

The main demos require Python dependencies listed in [`requirements.txt`](requirements.txt), including PyTorch, Transformers 4.27.1, `cpm_kernels`, Gradio, and SentencePiece. Install them with:

```bash
pip install -r requirements.txt
```

The standard CLI and web demos call `.half().cuda()`, so they are written for CUDA-capable PyTorch installations and a CUDA device. The repository also contains code for quantized loading and multi-GPU dispatch, described below. Hardware needs depend on the checkpoint, precision, input, and generation settings; this repository does not specify a universal minimum for running inference.

## Run ChatGLM-6B

### Command line

```bash
python cli_demo.py
```

Enter a message to chat. Type `clear` to clear the conversation history or `stop` to exit. The program loads `THUDM/chatglm-6b` from Hugging Face by default.

### Gradio web demo

```bash
python web_demo.py
```

The demo launches a local Gradio interface, opens it in a browser, and provides controls for maximum generation length, `top_p`, and temperature. It keeps the conversation history until **Clear History** is selected. The launch call uses `share=False`.

An alternate Streamlit interface is in `web_demo2.py`. It has additional dependencies (`streamlit` and `streamlit-chat`) that are not listed in the root `requirements.txt`.

### Load a local model directory

The demos use the Hugging Face model ID `THUDM/chatglm-6b`. To use a local copy instead, change that ID in the relevant script to the local model directory. The P-Tuning scripts also accept a local model path via their `model_name_or_path` setting; see [`ptuning/README.md`](ptuning/README.md).

## Quantized and multi-GPU loading

The model implementation exposes a `quantize` method. For example, the P-Tuning deployment instructions show loading a model and quantizing it to 4-bit before moving it to CUDA:

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = model.quantize(4).half().cuda().eval()
response, history = model.chat(tokenizer, "你好", history=[])
```

The repository's update notes also reference ChatGLM-6B INT4 and INT8 checkpoints. See [`UPDATE.md`](UPDATE.md) for the linked checkpoint pages and the associated historical notes. Quantized loading may have platform-specific dependencies; [`FAQ.md`](FAQ.md) documents one OpenMP issue on macOS.

`utils.py` provides `load_model_on_gpus(...)`, which uses Accelerate's `dispatch_model` to distribute model layers when more than one GPU is used. The helper is not wired into the default CLI or web demo; callers must use it in their own loading code. The root requirements include `accelerate`.

## HTTP API example

The API example loads the default ChatGLM-6B checkpoint and listens on port 8000:

```bash
pip install fastapi uvicorn
python api.py
```

Send a JSON `POST` request to `/` with a prompt and optional generation settings. `history` is a list of `[user_message, assistant_message]` pairs; pass the returned history to continue a conversation.

```bash
curl http://localhost:8000/ \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"你好","history":[],"max_length":2048,"top_p":0.7,"temperature":0.95}'
```

The response JSON contains `response`, `history`, `status`, and `time`. The server code binds to `0.0.0.0`; it does not implement authentication.

## Fine-tuning

The `ptuning/` directory implements parameter-efficient tuning based on P-Tuning v2, along with full fine-tuning scripts and evaluation/deployment code. The documented example uses the ADGEN advertising-generation dataset. It has additional dependencies beyond the root requirements and requires `transformers==4.27.1`; see [`ptuning/README.md`](ptuning/README.md) for dataset setup, commands, configuration, and checkpoint loading details.

## VisualGLM-6B image demos

The vision scripts load `THUDM/visualglm-6b`, not `THUDM/chatglm-6b`:

```bash
python cli_demo_vision.py
```

or

```bash
python web_demo_vision.py
```

These demos require the VisualGLM-6B-specific dependencies, including SwissArmyTransformer and `torchvision`. Follow the installation and model instructions in the [VisualGLM-6B project](https://github.com/THUDM/VisualGLM-6B).

## Limitations and licensing

Generated answers can be inaccurate or inconsistent. The repository's [bad-case feedback notes](improve/README.md) discuss examples of model limitations; do not treat model output as verified information.

The source code is licensed under [Apache License 2.0](LICENSE). The ChatGLM-6B model parameters have a separate license in [`MODEL_LICENSE`](MODEL_LICENSE); read it before downloading, using, or redistributing model weights. VisualGLM-6B has its own project and model terms.

## Additional documentation

- [FAQ and troubleshooting](FAQ.md)
- [Project update history](UPDATE.md)
- [P-Tuning v2 documentation](ptuning/README.md)
- [Related projects and resources](PROJECT.md)

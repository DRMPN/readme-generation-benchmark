# ChatGLM-6B

ChatGLM-6B is an open bilingual (Chinese and English) conversational language model based on the GLM architecture. This repository contains code for running the model locally, serving it through a web interface or API, and fine-tuning it on custom data.

> **Model weights are not included in this repository.** Download the ChatGLM-6B checkpoint separately and make it available to the scripts before running them.

## Contents

- [Features](#features)
- [Repository files](#repository-files)
- [Requirements](#requirements)
- [Download the model](#download-the-model)
- [Run inference](#run-inference)
  - [Command-line demo](#command-line-demo)
  - [Web demo](#web-demo)
  - [HTTP API](#http-api)
  - [Quantized inference](#quantized-inference)
- [Fine-tuning](#fine-tuning)
- [Evaluation](#evaluation)
- [Vision demos](#vision-demos)
- [Limitations and responsible use](#limitations-and-responsible-use)
- [License](#license)

## Features

- Chinese and English conversation.
- Local command-line and browser-based demos.
- An API server for integrating the model with other applications.
- Low-bit quantization options to reduce inference memory use.
- Training and evaluation scripts for adapting the model to custom data.
- Separate vision demo scripts for visual-language functionality.

## Repository files

| File or group | Purpose |
|---|---|
| `cli_demo.py` | Interactive command-line chat demo. |
| `web_demo.py`, `web_demo2.py`, `web_demo_old.py` | Browser-based chat demos. |
| `api.py` | API server for model inference. |
| `train.sh`, `train_chat.sh`, `ds_train_finetune.sh` | Training launch scripts. |
| `trainer.py`, `trainer_seq2seq.py`, `main.py`, `arguments.py` | Training and model utility code. |
| `evaluate.sh`, `evaluate_finetune.sh` | Evaluation launch scripts. |
| `data_sample.jsonl` | Example data for fine-tuning. |
| `requirements.txt` | Python dependencies. |
| `deepspeed.json` | DeepSpeed configuration. |
| `web_demo_vision.py`, `cli_demo_vision.py` | Vision-related demo scripts. |
| `README_en.md`, `UPDATE.md`, `FAQ.md`, `PROJECT.md`, `WECHAT.md` | Additional project documentation. |
| `MODEL_LICENSE`, `LICENSE` | Model and code license information. |

## Requirements

Use a Python environment with a PyTorch build compatible with your operating system and CUDA version. Install the project dependencies:

```bash
pip install -r requirements.txt
```

The model code is loaded using Hugging Face Transformers with `trust_remote_code=True`. Use a Transformers version compatible with the checkpoint and this repository’s requirements. If you encounter loading or generation errors, check the pinned dependency versions and the project’s [FAQ](FAQ.md).

### Hardware

Memory use depends on the checkpoint, precision, sequence length, and generation settings. As a rough guide, the full-precision model needs substantially more GPU memory than a quantized model; 8-bit and 4-bit quantization can make local inference possible on smaller GPUs. Actual requirements vary, so start with shorter prompts and lower generation limits if you run out of memory.

## Download the model

Download the ChatGLM-6B checkpoint from the model source you use, such as Hugging Face or ModelScope. For example, with Git LFS:

```bash
git lfs install
git clone https://huggingface.co/THUDM/chatglm-6b
```

If you use a local checkpoint, configure the demo or training script to point to its directory. Several scripts may use a model identifier or path directly in the source; update those values if needed.

## Run inference

### Command-line demo

After installing dependencies and making the checkpoint available, run:

```bash
python cli_demo.py
```

Type a message at the prompt to chat with the model. Use the demo’s exit command or `Ctrl-C` to stop it.

### Web demo

Start the standard browser demo with:

```bash
python web_demo.py
```

The script will print a local URL when the web interface is ready. Open that URL in a browser. If the model checkpoint is not found, update the model path used by the script.

Other web demo variants are included in the repository. Check their source and comments before using them, as they may have different interface or model-loading behavior.

### HTTP API

Start the API server with:

```bash
python api.py
```

The server’s address, routes, request fields, and response format are defined in `api.py`. Refer to that file for the exact API schema and example requests. Ensure the server can access the model checkpoint before sending requests.

### Quantized inference

Quantization reduces the model’s memory requirements, usually at the cost of some speed or output quality. The model-loading code in the demos can be configured for lower-bit inference where supported by the installed dependencies and hardware.

A typical loading pattern for 4-bit inference is:

```python
from transformers import AutoModel, AutoTokenizer

model_name_or_path = "THUDM/chatglm-6b"

tokenizer = AutoTokenizer.from_pretrained(
    model_name_or_path,
    trust_remote_code=True,
)
model = AutoModel.from_pretrained(
    model_name_or_path,
    trust_remote_code=True,
).quantize(4).cuda().eval()

response, history = model.chat(tokenizer, "你好", history=[])
print(response)
```

For a GPU without enough memory for full-precision inference, use a supported quantization option or the quantized loading configuration in the demo scripts. Quantization methods and device support depend on the model implementation and installed packages.

## Fine-tuning

The repository includes training code and launch scripts for adapting the model. Before training:

1. Install the training dependencies from `requirements.txt`.
2. Download the base model checkpoint.
3. Review `data_sample.jsonl` and prepare your dataset in the format expected by the training code.
4. Update the model path, dataset path, output directory, and training settings in the selected launch script.
5. Choose a launch script appropriate for your hardware and setup.

The supplied sample data uses JSON Lines (`.jsonl`): each line is a separate JSON example. Use the field names and structure shown in `data_sample.jsonl`; the training scripts may expect conversation history as well as a prompt and response.

Training entry points and configurations include:

- `train.sh` and `train_chat.sh` for the training workflows configured by those scripts.
- `ds_train_finetune.sh` and `deepspeed.json` for the DeepSpeed workflow.
- `trainer.py`, `trainer_seq2seq.py`, `main.py`, and `arguments.py` for training implementation and argument handling.

For example, to launch a workflow after configuring its script:

```bash
bash train.sh
```

Check the script before running it: paths, batch sizes, precision settings, and distributed-training options are specific to the environment and may need to be changed. Training large models can require substantial GPU memory and storage.

## Evaluation

The repository provides evaluation launch scripts:

```bash
bash evaluate.sh
```

For fine-tuned models, use the corresponding fine-tuning evaluation script:

```bash
bash evaluate_finetune.sh
```

Review each script to confirm the checkpoint, dataset, and output paths it uses. Evaluation results depend on the selected data and generation settings.

## Vision demos

The repository includes `web_demo_vision.py` and `cli_demo_vision.py` for vision-related interactions. These demos may require additional model files, dependencies, or configuration beyond the standard ChatGLM-6B text checkpoint. Follow the setup and model-loading instructions in the relevant script and project documentation; do not assume the standard text checkpoint alone is sufficient.

## Limitations and responsible use

ChatGLM-6B can produce inaccurate, incomplete, biased, or fabricated responses. It may not reliably follow instructions, cite sources, or distinguish fact from speculation. Review generated content before relying on it, especially for medical, legal, financial, safety-critical, or other high-impact decisions.

Treat user input and model output as untrusted data when integrating the API into an application. Apply appropriate privacy, security, and content safeguards.

## License

This repository includes separate code and model license files. Read `LICENSE` and `MODEL_LICENSE` before using, modifying, redistributing, or deploying the code or model. The model’s usage terms may differ from the code license.

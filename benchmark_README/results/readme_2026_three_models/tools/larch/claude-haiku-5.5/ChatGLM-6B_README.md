# ChatGLM-6B-dvdfcpv5

> **Note:** This README was drafted from the repository's file listing and from the public ChatGLM-6B project it appears to derive from. I haven't read the source code, so commands, arguments, and defaults should be checked against the actual files before publishing. Items marked **[verify]** are the most likely to differ in this fork.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Command-Line Demo](#command-line-demo)
  - [Web Demos](#web-demos)
  - [API Server](#api-server)
  - [Multimodal (Vision) Demo](#multimodal-vision-demo)
- [Model Loading and Quantization](#model-loading-and-quantization)
- [Fine-Tuning](#fine-tuning)
- [Evaluation](#evaluation)
- [Data Format](#data-format)
- [Hardware Requirements](#hardware-requirements)
- [FAQ](#faq)
- [Known Limitations](#known-limitations)
- [Project Documentation](#project-documentation)
- [License](#license)
- [Citation](#citation)
- [Acknowledgments](#acknowledgments)

---

## Overview

ChatGLM-6B-dvdfcpv5 is a Python project for running, serving, and fine-tuning **ChatGLM-6B**, an open bilingual (Chinese and English) dialogue language model based on the General Language Model (GLM) architecture. The model has about 6.2 billion parameters.

The repository provides:

- Command-line and browser-based chat interfaces
- A REST API server
- A multimodal (image + text) demo
- Scripts for supervised fine-tuning with full-parameter training, DeepSpeed, or parameter-efficient methods
- Evaluation scripts
- Documentation for common problems and project background

## Features

- **Bilingual chat** in Chinese and English
- **Streaming responses** in the CLI and web interfaces
- **Multi-turn conversation** with history management
- **INT4 / INT8 quantization** to reduce GPU memory use
- **Multiple front ends**: terminal, Gradio, Streamlit, and FastAPI
- **Vision-language demo** (VisualGLM-style, based on the included `visualglm.png` and `*_vision.py` files)
- **Fine-tuning pipeline** with DeepSpeed configuration (`deepspeed.json`)
- **Evaluation** on fine-tuned checkpoints

## Repository Structure

```
.
├── main.py                  # Main entry point for training/inference scripts [verify]
├── api.py                   # FastAPI server exposing a chat endpoint
├── cli_demo.py              # Terminal chat interface
├── cli_demo_vision.py       # Terminal interface for the multimodal model
├── web_demo.py              # Gradio web UI (primary)
├── web_demo_old.py          # Earlier Gradio web UI
├── web_demo2.py             # Streamlit web UI
├── web_demo_vision.py       # Gradio web UI for the multimodal model
├── web_demo.sh              # Shell wrapper to launch web_demo.py
├── utils.py                 # Shared helper functions (model loading, etc.) [verify]
│
├── trainer.py               # Custom Trainer class
├── trainer_seq2seq.py       # Seq2Seq trainer used for fine-tuning
├── arguments.py             # Command-line argument definitions
├── train.sh                 # Launch script for training
├── train_chat.sh            # Launch script for chat-format fine-tuning
├── ds_train_finetune.sh     # DeepSpeed fine-tuning launcher
├── deepspeed.json           # DeepSpeed configuration
├── evaluate.sh              # Evaluation script for the base model
├── evaluate_finetune.sh     # Evaluation script for fine-tuned checkpoints
├── data_sample.jsonl        # Example training data
│
├── requirements.txt         # Python dependencies
├── README.md                # Chinese README
├── README_en.md             # English README
├── FAQ.md                   # Frequently asked questions
├── UPDATE.md                # Changelog / update notes
├── PROJECT.md               # Project background and related work
├── WECHAT.md                # Community contact information
├── LICENSE                  # Code license
├── MODEL_LICENSE            # Model weights license
│
└── images/                  # Screenshots, diagrams, and demo assets
    ├── web-demo.png, web-demo.gif, cli-demo.png
    ├── visualglm.png, webglm.jpg, wechat.jpg
    ├── english-q*-old/new.png, math_error.png, factual_error.png, self-confusion_*.jpg
    └── *-writing-*.png, role-play.png, tour-guide.png, sport.png, ...
```

> Several image files are stored at the repository root in this layout. You may want to move them into an `assets/` or `images/` folder.

## Requirements

- Python 3.8 or newer **[verify]**
- PyTorch with CUDA support (recommended)
- An NVIDIA GPU for practical inference and all fine-tuning

Core dependencies are listed in `requirements.txt`. Typical packages include:

- `torch`
- `transformers` (a version compatible with ChatGLM's remote code; older releases are often required, for example 4.27.x) **[verify]**
- `protobuf`, `sentencepiece`
- `cpm_kernels` (for INT4/INT8 quantization on CUDA)
- `accelerate`
- `gradio`, `streamlit`
- `fastapi`, `uvicorn`
- `mdtex2html`
- `deepspeed` (for distributed fine-tuning)
- `rouge_chinese`, `nltk`, `jieba` (for evaluation metrics) **[verify]**

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url> ChatGLM-6B-dvdfcpv5
   cd ChatGLM-6B-dvdfcpv5
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate           # Windows
   ```

3. **Install PyTorch** for your CUDA version from [pytorch.org](https://pytorch.org).

4. **Install the remaining dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Download the model weights.** The weights are fetched automatically from Hugging Face on first run (`THUDM/chatglm-6b`). To use a local copy, pass the local path to the model loader.

## Quick Start

```python
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
model = model.eval()

response, history = model.chat(tokenizer, "你好", history=[])
print(response)

response, history = model.chat(tokenizer, "介绍一下你自己", history=history)
print(response)
```

## Usage

### Command-Line Demo

```bash
python cli_demo.py
```

- Type a message and press Enter to chat.
- Type `clear` to reset conversation history. **[verify]**
- Type `stop` or press Ctrl+C to exit. **[verify]**

### Web Demos

**Gradio (recommended):**

```bash
python web_demo.py
# or
bash web_demo.sh
```

Then open the URL printed in the terminal (typically `http://127.0.0.1:7860`).

**Streamlit:**

```bash
streamlit run web_demo2.py
```

**Legacy Gradio UI:**

```bash
python web_demo_old.py
```

### API Server

Start the server:

```bash
python api.py
```

By default it listens on port `8000`. Send a request:

```bash
curl -X POST "http://127.0.0.1:8000" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "你好", "history": []}'
```

Example response:

```json
{
  "response": "你好！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。",
  "history": [["你好", "你好！我是人工智能助手 ChatGLM-6B..."]],
  "status": 200,
  "time": "2023-03-20 10:00:00"
}
```

> The request and response fields above follow the upstream ChatGLM-6B API. Check `api.py` for the exact schema. **[verify]**

### Multimodal (Vision) Demo

The repository includes a multimodal variant that accepts an image alongside text.

```bash
# Terminal
python cli_demo_vision.py

# Web
python web_demo_vision.py
```

Upload an image, then ask a question about it. The demo is intended for image description, visual question answering, and similar tasks. **[verify model checkpoint required]**

## Model Loading and Quantization

ChatGLM-6B can run in several precisions to fit different GPUs:

```python
# FP16 (full quality, ~13 GB VRAM)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()

# INT8 (~8 GB VRAM)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).quantize(8).half().cuda()

# INT4 (~6 GB VRAM)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).quantize(4).half().cuda()
```

CPU inference is supported but slow. It requires substantial RAM and typically uses float32. **[verify]**

## Fine-Tuning

The repository supports supervised fine-tuning on custom datasets.

### 1. Prepare data

Format your data as JSON Lines. See [Data Format](#data-format).

### 2. Configure arguments

Training options are defined in `arguments.py`. Common parameters include:

| Argument | Description |
|---|---|
| `--model_name_or_path` | Model ID or local path (e.g., `THUDM/chatglm-6b`) |
| `--train_file` | Path to the training `.jsonl` file |
| `--validation_file` | Optional validation file |
| `--prompt_column` | Field name for the input prompt |
| `--response_column` | Field name for the target response |
| `--max_source_length` | Maximum input token length |
| `--max_target_length` | Maximum output token length |
| `--learning_rate` | Learning rate |
| `--num_train_epochs` | Number of epochs |
| `--per_device_train_batch_size` | Batch size per GPU |
| `--output_dir` | Where checkpoints are saved |

**[verify]** Argument names and defaults should be confirmed in `arguments.py`.

### 3. Run training

Single-node training:

```bash
bash train.sh
```

Chat-format training:

```bash
bash train_chat.sh
```

DeepSpeed training (multi-GPU):

```bash
bash ds_train_finetune.sh
```

The DeepSpeed configuration is in `deepspeed.json`. Adjust batch sizes, ZeRO stage, and offload settings there to match your hardware.

### 4. Run inference with a fine-tuned checkpoint

Point the demos or API to your checkpoint directory, or load it manually:

```python
model = AutoModel.from_pretrained("output/checkpoint-1000", trust_remote_code=True).half().cuda()
```

## Evaluation

Evaluate the base model:

```bash
bash evaluate.sh
```

Evaluate a fine-tuned checkpoint:

```bash
bash evaluate_finetune.sh
```

Scripts typically report generation metrics such as ROUGE and BLEU. **[verify]** Check the scripts for the dataset path, checkpoint path, and metric configuration.

## Data Format

Training data uses JSON Lines (one JSON object per line). Example from `data_sample.jsonl`:

```json
{"prompt": "请用一句话解释什么是机器学习。", "response": "机器学习是让计算机通过数据自动学习规律并做出预测或决策的技术。"}
{"prompt": "Write a haiku about autumn.", "response": "Crimson leaves drifting\nwhispers of the cooling wind\nthe year exhales slow"}
```

Field names are configurable through `--prompt_column` and `--response_column`. **[verify]**

## Hardware Requirements

| Task | Precision | Approximate GPU Memory |
|---|---|---|
| Inference | FP16 | ~13 GB |
| Inference | INT8 | ~8 GB |
| Inference | INT4 | ~6 GB |
| Fine-tuning (P-tuning / LoRA-style) | FP16 | ~16 GB+ |
| Full fine-tuning | FP16 | Multiple high-memory GPUs with DeepSpeed |

Memory figures vary with sequence length and batch size.

## FAQ

Common questions are answered in `FAQ.md`. Topics typically include:

- Out-of-memory errors and quantization options
- Installation problems with `cpm_kernels` or `transformers` versions
- Model download issues
- Limitations of model responses (hallucination, math errors, self-identification)

## Known Limitations

As described in the project's documentation, ChatGLM-6B:

- Can produce **factual errors** and **hallucinated** content
- Can make **mistakes on math and logic** problems
- May give **inconsistent answers** to similar questions
- Has a **limited context window** and may lose track of long conversations
- Is trained primarily on Chinese and English text and may perform worse in other languages
- Should not be relied on for medical, legal, or other high-stakes decisions

Example failure cases are shown in the images folder (`math_error.png`, `factual_error.png`, `self-confusion_*.jpg`).

## Project Documentation

| File | Contents |
|---|---|
| `README.md` | Chinese documentation |
| `README_en.md` | English documentation |
| `FAQ.md` | Frequently asked questions |
| `UPDATE.md` | Version history and changes |
| `PROJECT.md` | Background, papers, and related projects |
| `WECHAT.md` | Community group information |

## License

- **Code**: see `LICENSE`.
- **Model weights**: see `MODEL_LICENSE`. The weights have usage restrictions, so review that file before commercial use or redistribution.

## Citation

If you use this project in research, please cite the ChatGLM and GLM papers:

```bibtex
@inproceedings{du2022glm,
  title={GLM: General Language Model Pretraining with Autoregressive Blank Infilling},
  author={Du, Zhengxiao and Qian, Yujie and Liu, Xiao and Ding, Ming and Qiu, Jiezhong and Yang, Zhilin and Tang, Jie},
  booktitle={Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={320--335},
  year={2022}
}
```

## Acknowledgments

This project builds on the GLM architecture and the ChatGLM series from Tsinghua University's Knowledge Engineering Group (KEG) and Zhipu AI. It also relies on open-source work from Hugging Face Transformers, PyTorch, DeepSpeed, Gradio, and Streamlit.

---

*If you find issues in this README or in the repository, please open an issue or submit a pull request.*

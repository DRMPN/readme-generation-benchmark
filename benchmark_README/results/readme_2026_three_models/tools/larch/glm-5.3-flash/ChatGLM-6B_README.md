# ChatGLM-6B

**ChatGLM-6B** is an open-source, bilingual (Chinese-English) conversational language model optimized for Chinese Q&A and dialogue, built on the [GLM (General Language Model)](https://github.com/THUDM/GLM) architecture. With **6.2 billion parameters**, ChatGLM-6B is designed to run on consumer-grade hardware (as little as **6GB of GPU memory** with INT4 quantization) while maintaining competitive dialogue performance.

This repository provides the full toolkit for using ChatGLM-6B: CLI demos, web demos, a REST API, quantized inference, and parameter-efficient fine-tuning (P-Tuning v2 / LoRA) — plus experimental **vision-language** capabilities (`web_demo_vision.py`, `cli_demo_vision.py`).

---

## 📋 Table of Contents

- [Introduction](#-introduction)
- [News](#-news)
- [Features](#-features)
- [Performance](#-performance)
- [Inference](#-inference)
  - [Quick Start](#-quick-start)
  - [CLI Demo](#-cli-demo)
  - [Web Demo](#-web-demo)
  - [REST API](#-rest-api)
  - [Quantization & Low-Memory Inference](#-quantization--low-memory-inference)
  - [Vision Demo (Experimental)](#-vision-demo-experimental)
- [Fine-tuning](#-fine-tuning)
  - [P-Tuning v2](#-p-tuning-v2)
  - [Full Fine-tuning / DeepSpeed](#-full-fine-tuning--deepspeed)
  - [Evaluation](#-evaluation)
- [Deployment](#-deployment)
- [Examples](#-examples)
- [Project Structure](#-project-structure)
- [FAQ](#-faq)
- [License](#-license)
- [Citation](#-citation)

---

## 🚀 Introduction

ChatGLM-6B is jointly developed by Tsinghua University and Zhipu AI. It combines:

- **Bilingual optimization**: Trained on a 1:1 Chinese-English corpus, giving it strong performance on Chinese tasks compared to similarly-sized English-centric models.
- **Consumer-friendly deployment**: Quantization support (INT4/INT8) allows inference on GPUs with 6–13GB of memory, and even on CPU.
- **Efficient adaptation**: P-Tuning v2 enables effective fine-tuning on a single consumer GPU with as few as a few thousand training samples.
- **Extended context**: A context window of 2048 tokens for multi-turn dialogue.

---

## 📰 News

- **[2023]** Released fine-tuning scripts with P-Tuning v2 and LoRA support, plus DeepSpeed multi-GPU/full-parameter training.
- **[2023]** Added INT4/INT8 quantized inference and CPU inference support.
- **[2023]** Added REST API server (`api.py`) for deployment.
- **[2023]** Experimental vision-language demos released (`cli_demo_vision.py`, `web_demo_vision.py`).

See [UPDATE.md](UPDATE.md) for the full changelog.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌏 Bilingual | Strong performance in both Chinese and English |
| 💾 Low memory | INT4 quantization → inference on 6GB GPU; CPU-only inference supported |
| 🔧 Easy fine-tuning | P-Tuning v2 with ~7GB GPU memory; full fine-tuning with DeepSpeed |
| 🖥️ Multiple interfaces | CLI, Gradio web demo, OpenAI-style REST API |
| 👁️ Vision (experimental) | VisualGLM-style image + text dialogue demos |
| 📖 Open weights | Model weights available for research after completing a questionnaire |

---

## 📊 Performance

ChatGLM-6B was evaluated against popular open models (OPT-6.7B, BLOOM-7B, GLM-130B baseline dialogue) on Chinese dialogue benchmarks. It achieves competitive or superior performance on Chinese Q&A and dialogue tasks while being much smaller than 100B-scale models.

**Example outputs (before/after fine-tuning):**

| Task | Example |
|---|---|
| Email writing | ![](email-writing-1.png) ![](email-writing-2.png) |
| Blog outline | ![](blog-outline.png) |
| Role play | ![](role-play.png) |
| Ad writing | ![](ad-writing-2.png) |
| Information extraction | ![](information-extraction.png) |
| Comments writing | ![](comments-writing.png) |
| Tour guide | ![](tour-guide.png) |
| Self introduction | ![](self-introduction.png) |

> ⚠️ **Limitations**: Due to its relatively small size and limited training data, ChatGLM-6B may exhibit factual errors (see `factual_error.png`), math mistakes (`math_error.png`), or self-confusion about its identity (`self-confusion_openai.jpg`, `self-confusion_google.jpg`, `self-confusion_tencent.jpg`). Always verify critical outputs.

---

## 💻 Inference

### ⚙️ Requirements

```bash
pip install -r requirements.txt
```

Core dependencies: `torch`, `transformers>=4.28.1`, `sentencepiece`, `gradio`, `streamlit`, etc.

### 🏃 Quick Start

```python
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()

history = []
query = "晚上睡不着应该怎么办"
response, history = model.chat(tokenizer, query, history=history)
print(response)
```

### ⌨️ CLI Demo

Launch an interactive command-line chat (supports multi-turn history and streaming output):

```bash
python cli_demo.py
```

### 🌐 Web Demo

**Gradio-based web demo:**

```bash
python web_demo.py
```

or use the shell wrapper:

```bash
bash web_demo.sh
```

Alternative web demos are provided in `web_demo_old.py`, `web_demo2.py` (Streamlit):

```bash
streamlit run web_demo2.py
```

### 🔌 REST API

Start an OpenAI-style API server:

```bash
python api.py
```

Then call it:

```bash
curl -X POST http://127.0.0.1:8000 \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你好", "history": []}'
```

### 🧊 Quantization & Low-Memory Inference

| Precision | GPU memory | Load flag |
|---|---|---|
| FP16 | ~13 GB | `.half().cuda()` |
| INT8 | ~9 GB | `.quantize(8)` |
| INT4 | ~6 GB | `.quantize(4)` |

```python
# INT4 quantization (requires GPU with ~6GB memory)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).quantize(4).cuda()

# CPU inference (requires ~32GB memory, slower)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).float()
```

### 👁️ Vision Demo (Experimental)

Multimodal demos combining image understanding with dialogue:

```bash
# CLI vision demo
python cli_demo_vision.py

# Web vision demo
python web_demo_vision.py
```

See `visualglm.png` for an example screenshot.

---

## 🛠️ Fine-tuning

### 🎯 P-Tuning v2

Parameter-efficient fine-tuning that freezes the base model and only trains a small set of prefix embeddings. Runs on a single consumer GPU (~7GB for INT4 base + training).

1. **Prepare data** — a JSONL file of `{prompt, completion}` pairs (see `data_sample.jsonl`):

```json
{"prompt": "标题： weather today? ncontent: ...", "completion": "sunny"}
```

2. **Run training:**

```bash
bash train_chat.sh
```

Key options in `train_chat.sh` / `train.sh` / `arguments.py`:

- `--preprocessing_num_workers`, `--max_seq_length`, `--max_source_length`, `--max_target_length`
- `--preprocessing_num_workers`, `--model_name_or_path`, `--output_dir`
- `--per_device_train_batch_size`, `--learning_rate`, `--num_train_epochs`
- `--quantization_bit` (train the LoRA/P-Tuning on a quantized base model)

3. **Evaluate:**

```bash
bash evaluate.sh          # base model
bash evaluate_finetune.sh # fine-tuned checkpoints
```

### ⚡ Full Fine-tuning / DeepSpeed

For multi-GPU full-parameter fine-tuning with DeepSpeed ZeRO offloading:

```bash
bash ds_train_finetune.sh
```

DeepSpeed configuration is in `deepspeed.json`. Training logic is implemented in `trainer.py`, `trainer_seq2seq.py`, and orchestrated by `main.py`, with model arguments defined in `arguments.py` and utilities in `utils.py`.

**Memory requirements (full fine-tuning):**

| Method | Memory |
|---|---|
| Full fine-tuning (DeepSpeed ZeRO-3, CPU offload) | ~6 × 32GB GPUs or comparable |
| P-Tuning v2 (FP16 base) | ~10GB |
| P-Tuning v2 (INT4 base) | ~7GB |
| LoRA | between the above |

---

## 🚢 Deployment

- **Local GPU server**: `web_demo.py` / `api.py`
- **Production API**: wrap `api.py` behind uvicorn/gunicorn; consider batching and quantization
- **Low-resource**: INT4 quantized model on a 6GB GPU, or CPU inference

---

## 🖼️ Examples Gallery

| | | |
|---|---|---|
| ![](web-demo.png) Web demo | ![](cli-demo.png) CLI demo | ![](webglm.jpg) WebGLM |
| ![](sport.png) Sports Q&A | ![](wechat.jpg) WeChat | ![](visualglm.png) VisualGLM |

---

## 📁 Project Structure

```
.
├── main.py                    # Fine-tuning entry point
├── arguments.py               # Training arguments (HuggingFace-style)
├── trainer.py                 # Custom trainer with loss masking
├── trainer_seq2seq.py         # Seq2Seq trainer wrapper
├── utils.py                   # Data loading, tokenization, logging utils
├── deepspeed.json             # DeepSpeed ZeRO configuration
├── train.sh / train_chat.sh   # P-Tuning v2 launch scripts
├── ds_train_finetune.sh       # DeepSpeed full fine-tuning script
├── evaluate.sh / evaluate_finetune.sh
├── cli_demo.py                # Command-line chat interface
├── web_demo.py                # Gradio web demo
├── web_demo2.py               # Streamlit web demo
├── web_demo_old.py            # Legacy web demo
├── api.py                     # REST API server
├── cli_demo_vision.py         # CLI multimodal demo
├── web_demo_vision.py         # Web multimodal demo
├── data_sample.jsonl          # Fine-tuning data sample
├── requirements.txt
├── MODEL_LICENSE              # Model usage license
├── FAQ.md                     # Frequently asked questions
├── PROJECT.md                 # Related projects
└── UPDATE.md                  # Changelog
```

---

## ❓ FAQ

Common issues (CUDA OOM, quantization errors, tokenizer problems, loading on macOS/CPU, fine-tuning bugs) are documented in [FAQ.md](FAQ.md). Please check it before opening an issue.

---

## 📜 License

- **Code**: This repository is licensed under the [Apache-2.0 License](LICENSE).
- **Model weights**: Governed by the [MODEL_LICENSE](MODEL_LICENSE) agreement, free for academic research; commercial use requires registration/application with the model authors.

---

## 📚 Citation

If you use ChatGLM-6B in your research, please cite:

```bibtex
@article{zeng2022glm,
  title={GLM: General Language Model Pretraining with Autoregressive Blank Infilling},
  author={Zeng, Aohan and Liu, Xiao and Du, Zhengxiao and Wang, Zihan and Lai, Hanyu and Ding, Ming and Yang, Zhuoyi and Xu, Yifan and Zheng, Wendi and Xia, Xiao and others},
  journal={Neuron},
  volume={102},
  pages={764--776},
  year={2023}
}
```

---

## 🙏 Acknowledgements

- [GLM](https://github.com/THUDM/GLM) — base architecture
- [GLM-130B](https://github.com/THUDM/GLM-130B) — large-scale predecessor
- [HuggingFace Transformers](https://github.com/huggingface/transformers) and [PEFT](https://github.com/huggingface/peft)
- [DeepSpeed](https://github.com/microsoft/DeepSpeed) — distributed training
- [VisualGLM](https://github.com/THUDM/VisualGLM-6B) — vision-language extension

Join the community on WeChat (see [WECHAT.md](WECHAT.md)) to discuss usage and fine-tuning!

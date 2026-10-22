# ChatGLM-6B

ChatGLM-6B is an open-source, bilingual (Chinese and English) dialogue language model released by the ChatGLM-6B Model Team (THUDM). This repository contains the model's inference demos (command line, web, API), parameter-efficient fine-tuning code, and related documentation. The model weights are downloaded from Hugging Face (`THUDM/chatglm-6b`) when the scripts run.

Most of the repository's documentation and code comments are written in Chinese. This README is in English; the linked Chinese documents contain more detail.

## Contents

- [Repository layout](#repository-layout)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Running the demos](#running-the-demos)
- [HTTP API](#http-api)
- [Fine-tuning](#fine-tuning)
- [VisualGLM-6B (multimodal)](#visualglm-6b-multimodal)
- [Model versions and quantized variants](#model-versions-and-quantized-variants)
- [Known limitations](#known-limitations)
- [Badcase feedback](#badcase-feedback)
- [Related projects](#related-projects)
- [License](#license)
- [Community](#community)

## Repository layout

| Path | Description |
| --- | --- |
| `cli_demo.py` | Command-line chat with streaming output. |
| `web_demo.py` | Gradio web chat interface. |
| `web_demo2.py` | Streamlit web chat interface. |
| `web_demo_old.py` | Earlier Gradio web demo. |
| `api.py` | FastAPI/uvicorn HTTP service exposing the model. |
| `utils.py` | `load_model_on_gpus()` and `auto_configure_device_map()` for loading the model across multiple GPUs. |
| `cli_demo_vision.py`, `web_demo_vision.py` | Command-line and web demos for VisualGLM-6B. |
| `ptuning/` | P-Tuning v2 and full fine-tuning code, training and evaluation scripts, and its own [README](ptuning/README.md) (also available in [English](ptuning/README_en.md)). |
| `improve/` | Badcase feedback program description and sample data (`improve/data_sample.jsonl`). See its [README](improve/README.md). |
| `resources/` | Images and media used in the documentation. |
| `examples/` | Screenshots of example tasks. |
| `limitations/` | Screenshots of known model errors. |
| `UPDATE.md` | Changelog (Chinese and English). |
| `FAQ.md` | Troubleshooting notes (currently a macOS OpenMP entry). |
| `PROJECT.md` | List of related and derivative projects (Chinese). |
| `LICENSE`, `MODEL_LICENSE` | Code license and model license. |

## Requirements

Python dependencies are listed in `requirements.txt`:

```
protobuf
transformers==4.27.1
cpm_kernels
torch>=1.10
gradio
mdtex2html
sentencepiece
accelerate
```

Notes:

- `transformers` is pinned to `4.27.1`.
- The demo scripts call `.half().cuda()`, so they expect a CUDA-capable NVIDIA GPU as written.
- `web_demo2.py` imports `streamlit` and `streamlit_chat`, which are not in `requirements.txt`. Install them separately.
- `cli_demo_vision.py` and `web_demo_vision.py` (VisualGLM-6B) additionally require [SwissArmyTransformer](https://github.com/THUDM/SwissArmyTransformer/) and `torchvision`, per `UPDATE.md`.
- Fine-tuning requires additional packages listed in [Fine-tuning](#fine-tuning). Full-parameter fine-tuning also requires [DeepSpeed](https://github.com/microsoft/DeepSpeed).

`UPDATE.md` states that GPU acceleration on Apple Silicon Macs was added. The scripts in this repository use `.cuda()`, and this README does not document a setup for Apple Silicon. `FAQ.md` describes an OpenMP installation step for macOS when loading quantized models.

Memory figures stated in the repository:

- P-Tuning v2 with INT4 quantization: "at least 7 GB" of GPU memory (`UPDATE.md`, `ptuning/README.md`). The default configuration is documented as needing about 6.7 GB for training.

## Installation

```bash
git clone https://github.com/THUDM/ChatGLM-6B
cd ChatGLM-6B
pip install -r requirements.txt
```

The first run downloads `THUDM/chatglm-6b` from Hugging Face. To use a local copy, replace `THUDM/chatglm-6b` in the scripts with the local path, as described in `ptuning/README.md`.

## Quick start

Load the model in Python and chat with it:

```python
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
model = model.eval()

response, history = model.chat(tokenizer, "你好", history=[])
print(response)
```

To quantize the model to INT4 before use, call `model.quantize(4)` before `.half().cuda()`, as shown in `ptuning/README.md`:

```python
model = model.quantize(4)
model = model.half().cuda()
model = model.eval()
```

The model also provides `stream_chat`, which yields partial responses. `cli_demo.py` and `web_demo.py` use it.

## Running the demos

Run these from the repository root. Each script loads the model when it starts.

| Command | What it does |
| --- | --- |
| `python cli_demo.py` | Terminal chat. Type `clear` to reset history and `stop` to exit. |
| `python web_demo.py` | Gradio web UI. Opens a browser tab (`inbrowser=True`). |
| `streamlit run web_demo2.py` | Streamlit web UI. Requires `streamlit` and `streamlit_chat`. |
| `python api.py` | Starts the HTTP API on port 8000. See [HTTP API](#http-api). |
| `python web_demo_old.py` | Earlier Gradio demo. |

The `cli_demo.py` script shows the most recent response on screen, redrawing the terminal every few tokens.

## HTTP API

`api.py` runs a FastAPI application with uvicorn on `0.0.0.0:8000`. It has a single endpoint, `POST /`, which takes a JSON body:

| Field | Type | Default when omitted | Description |
| --- | --- | --- | --- |
| `prompt` | string | — | The user message. |
| `history` | list | `None` | Prior conversation turns, as returned in `history`. |
| `max_length` | integer | `2048` | Maximum length passed to `model.chat`. |
| `top_p` | float | `0.7` | Nucleus sampling parameter. |
| `temperature` | float | `0.95` | Sampling temperature. |

Example:

```bash
curl -X POST http://127.0.0.1:8000 \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你好", "history": []}'
```

The response is a JSON object with the fields `response`, `history`, `status` (always `200`), and `time`. Pass the returned `history` into the next request to continue the conversation.

The server does not implement authentication. It binds to all network interfaces (`0.0.0.0`), so restrict access (for example, with a firewall) if you run it on a shared network.

## Fine-tuning

The `ptuning/` directory contains fine-tuning code. Its [README](ptuning/README.md) has full details. The summary below is taken from that file and the scripts.

### Dataset

The examples use the [ADGEN](https://aclanthology.org/D19-1321.pdf) advertisement-generation dataset. Download the processed dataset from the links in `ptuning/README.md` and place the extracted `AdvertiseGen` directory inside `ptuning/`. Each record has a `content` field (the input) and a `summary` field (the target text).

### P-Tuning v2

```bash
cd ptuning
bash train.sh
```

`train.sh` freezes the base model and trains a prefix encoder. Key settings:

- `PRE_SEQ_LEN=128` and `LR=2e-2` (soft prompt length and learning rate).
- `--quantization_bit 4` (INT4 base model).
- `--max_steps 3000`, `--gradient_accumulation_steps 16`.

Evaluate with `bash evaluate.sh`, which writes `generated_predictions.txt` to the output directory. Launch the web demo with a trained checkpoint using `bash web_demo.sh`.

### Full fine-tuning

```bash
cd ptuning
bash ds_train_finetune.sh
```

This script uses DeepSpeed with 4 GPUs (`--num_gpus=4`) and `deepspeed.json`.

### Multi-turn chat data

`train_chat.sh` trains on chat data with a `history` field. The script refers to the environment variables `CHAT_TRAIN_DATA`, `CHAT_VAL_DATA`, and `CHECKPOINT_NAME`, which must be set before running it. The `ptuning/README.md` gives a three-turn JSON Lines example.

### Results reported in `ptuning/README.md`

| | Finetune | P-tuning v2 | LoRA |
| --- | --- | --- | --- |
| BLEU-4 | 8.01 | 8.10 | 7.62 |
| Rouge-1 | 31.23 | 31.12 | 30.60 |
| Rouge-2 | 7.36 | 7.11 | 6.96 |
| Rouge-l | 25.08 | 24.97 | 24.80 |
| Training Loss | 3.00 | 3.74 | 3.32 |

The LoRA implementation is credited in `ptuning/README.md` to [simple_thu_chatglm6b](https://github.com/yuanzhoulvpi2017/zero_nlp/tree/main/simple_thu_chatglm6b). The LoRA training code is not part of this repository.

### Loading a fine-tuned checkpoint

P-Tuning v2 checkpoints store only the `PrefixEncoder` weights, so they must be loaded on top of the base model. `ptuning/README.md` gives the full code. Checkpoints saved with the older full-parameter format can be loaded directly with `AutoModel.from_pretrained(CHECKPOINT_PATH, trust_remote_code=True)`.

## VisualGLM-6B (multimodal)

Per `UPDATE.md`, VisualGLM-6B is a multimodal model that supports image understanding, released 2023/05/17. Its demos are in this repository:

```bash
python cli_demo_vision.py
python web_demo_vision.py
```

Both scripts load `THUDM/visualglm-6b`. The command-line demo asks for an image path, then describes the image; the web demo lets you upload an image. VisualGLM-6B requires the extra dependencies listed in [Requirements](#requirements). More information is at [VisualGLM-6B](https://github.com/THUDM/VisualGLM-6B).

## Model versions and quantized variants

`UPDATE.md` records the following model releases and variants:

- **v1.1 checkpoint (2023/05/15):** added English instruction data to balance Chinese and English training data, reducing Chinese words in English answers. Before-and-after examples are in `UPDATE.md`.
- **INT4 quantized model:** [THUDM/chatglm-6b-int4](https://huggingface.co/THUDM/chatglm-6b-int4).
- **INT8 quantized model:** [THUDM/chatglm-6b-int8](https://huggingface.co/THUDM/chatglm-6b-int8).
- **Embedding-quantized model** `THUDM/chatglm-6b-int4-qe`: listed in `UPDATE.md` as discontinued ("已停止维护").
- **Streaming output:** `stream_chat` was added in 2023/03/19.
- **Multi-GPU deployment:** added 2023/04/16. `utils.py` provides the device-map helpers.

## Known limitations

`improve/README.md` states that ChatGLM-6B can still:

- misunderstand complex instructions and task requirements;
- lack understanding of some domain concepts;
- produce factual errors;
- generate harmful content;
- lose dialogue-context consistency.

The `limitations/` directory contains example screenshots of factual errors, math errors, and self-confusion (file names `self-confusion_*`). The model is also documented as possibly mixing Chinese words into English answers, which v1.1 aimed to reduce.

Fine-tuning can fix some of these issues, but `improve/README.md` notes that it can cause catastrophic forgetting, which may reduce general conversation ability or generalization.

## Badcase feedback

The repository's `improve/` directory describes a program that collects user-reported badcases to improve the model. To contribute, fill in the [questionnaire](https://www.wjx.cn/vm/rAoGx9X.aspx#) and upload data in JSON Lines format, with `prompt` (the input) and `response` (the expected output) fields. `improve/data_sample.jsonl` contains sample data. Submitted data must not contain personal information, trade secrets, or content that endangers national security or infringes third-party intellectual property. The program's full terms are in `improve/README.md`.

## Related projects

`PROJECT.md` (in Chinese) lists open-source projects that accelerate or reimplement ChatGLM-6B, projects built on it, projects that fine-tune it, and tutorials. Examples include:

- [SwissArmyTransformer](https://github.com/THUDM/SwissArmyTransformer), a Transformer programming framework where ChatGLM-6B is implemented and supports P-tuning fine-tuning.
- [ChatGLM-Efficient-Tuning](https://github.com/hiyouga/ChatGLM-Efficient-Tuning) for supervised fine-tuning and RLHF training.
- [chatgpt_academic](https://github.com/binary-husky/chatgpt_academic), an academic writing and programming toolkit that supports ChatGLM-6B.

The list is maintained in `PROJECT.md`; this README does not verify the projects' claims.

## License

- **Code:** licensed under the [Apache License 2.0](LICENSE).
- **Model weights:** licensed under the [ChatGLM-6B License](MODEL_LICENSE). Under that license, you may not use the model for military or illegal purposes, for activities that harm national security or national unity, or for activities that harm the public interest or infringe on individuals' rights. The license is governed by the laws of the People's Republic of China, and disputes go to the Haidian District People's Court in Beijing. The license covers ChatGLM-6B only, not ChatGLM2-6B or later models.

The model license is also published in English in `MODEL_LICENSE`. Contact: license@zhipuai.cn.

## Community

`resources/WECHAT.md` includes a QR code (`resources/wechat.jpg`) for the official WeChat account and "ChatGLM交流群" (ChatGLM discussion group).

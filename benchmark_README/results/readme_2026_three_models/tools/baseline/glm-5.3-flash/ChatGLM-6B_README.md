# ChatGLM-6B

ChatGLM-6B is an open bilingual (Chinese-English) conversational language model, optimized for Chinese Q&A and dialogue. Based on the GLM (General Language Model) architecture, the 6B-parameter model can run on consumer-grade GPUs thanks to quantization support (INT4/INT8), requiring as little as ~6GB of GPU memory for inference. The repository provides:

- **Inference demos**: a command-line chat demo, a Gradio web demo, a Streamlit web demo, and an OpenAI-style API server
- **Vision demo**: support for [VisualGLM-6B](https://github.com/THUDM/VisualGLM-6B), a multimodal conversational model with image understanding
- **Parameter-efficient fine-tuning**: a full [P-Tuning v2](https://github.com/THUDM/P-tuning-v2) training pipeline (in the `ptuning/` directory) that requires as little as ~7GB of GPU memory for tuning
- **Multi-GPU deployment**: utilities to dispatch the model across multiple GPUs

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI Demo](#cli-demo)
  - [Web Demo (Gradio)](#web-demo-gradio)
  - [Web Demo (Streamlit)](#web-demo-streamlit)
  - [API Deployment](#api-deployment)
  - [Vision Demo (VisualGLM-6B)](#vision-demo-visualglm-6b)
  - [Multi-GPU Deployment](#multi-gpu-deployment)
- [Fine-tuning with P-Tuning v2](#fine-tuning-with-p-tuning-v2)
- [Project Structure](#project-structure)
- [Known Limitations](#known-limitations)
- [FAQ](#faq)
- [Community and Related Projects](#community-and-related-projects)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Bilingual dialogue**: trained with a balanced mix of Chinese and English instruction data (as of the v1.1 checkpoint update on 2023/05/15, English training data was added to fix Chinese words appearing in English answers).
- **Streaming output**: the `stream_chat` interface streams responses incrementally and is used by both the CLI and web demos.
- **Quantization**: INT4 and INT8 quantized model checkpoints are available on Hugging Face (`THUDM/chatglm-6b-int4`, `THUDM/chatglm-6b-int8`), reducing the memory required for deployment.
- **Multi-GPU support**: model layers can be split across GPUs automatically.
- **Apple Silicon support**: GPU inference on Macs with Apple Silicon chips is supported.
- **Efficient fine-tuning**: P-Tuning v2 freezes all model parameters and only trains a small prefix encoder, so with INT4 quantization and gradient checkpointing, fine-tuning needs a minimum of about 6.7GB GPU memory.

## Installation

### Requirements

The Python dependencies are listed in `requirements.txt`:

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

Install them with:

```bash
pip install -r requirements.txt
```

Note: `transformers` must be version **4.27.1** for the model code to work correctly.

### Additional dependencies for fine-tuning

To run the P-Tuning v2 training pipeline, additionally install:

```bash
pip install rouge_chinese nltk jieba datasets
```

For full-parameter fine-tuning, [Deepspeed](https://github.com/microsoft/DeepSpeed) is also required.

### Model weights

The demos load the model by default from the Hugging Face hub:

```python
tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
```

Quantized checkpoints such as `THUDM/chatglm-6b-int4` can be substituted to reduce GPU memory usage. If you load the model from a local path, replace `"THUDM/chatglm-6b"` with your local model directory in the demo scripts and training scripts.

> **Note for Mac users**: loading the INT4-quantized model on macOS may require installing OpenMP first (see the [FAQ](FAQ.md) for detailed instructions). If you previously ran the model with an error, clear the Hugging Face cache (e.g. `rm -rf ${HOME}/.cache/huggingface/modules/transformers_modules/chatglm-6b-int4`).

## Usage

### CLI Demo

Run an interactive command-line chat session with streaming output:

```bash
python cli_demo.py
```

Commands within the demo:
- Type your message to chat with the model.
- `clear` — clears the conversation history.
- `stop` — exits the program.
- `Ctrl+C` — interrupts an in-progress generation.

### Web Demo (Gradio)

Launch a Gradio web interface (recommended, improved UI as of 2023/04/06):

```bash
python web_demo.py
```

The interface exposes sliders for **Maximum length** (up to 4096), **Top P**, and **Temperature**, plus a "Clear History" button. Responses stream into the chat window as they are generated.

An older-style Gradio demo is also available:

```bash
python web_demo_old.py
```

### Web Demo (Streamlit)

Launch a Streamlit-based web demo:

```bash
python web_demo2.py
```

This variant uses the `streamlit-chat` UI components, with `max_length`, `top_p`, and `temperature` settings in the sidebar. (You will need `pip install streamlit streamlit-chat`.)

### API Deployment

A FastAPI-based API server is provided in `api.py`:

```bash
python api.py
```

This starts a server on `0.0.0.0:8000`. Send a POST request to `/` with a JSON body:

```json
{
  "prompt": "你好",
  "history": [],
  "max_length": 2048,
  "top_p": 0.7,
  "temperature": 0.95
}
```

Fields other than `prompt` are optional; defaults are `max_length=2048`, `top_p=0.7`, `temperature=0.95`. The response contains:

```json
{
  "response": "...",
  "history": [[prompt, response], ...],
  "status": 200,
  "time": "2023-05-17 12:00:00"
}
```

The server clears the CUDA cache after each request and logs each exchange with a timestamp.

### Vision Demo (VisualGLM-6B)

As of 2023/05/17, the repository supports [VisualGLM-6B](https://github.com/THUDM/VisualGLM-6B), a multimodal conversational language model with image understanding. VisualGLM-6B requires additional dependencies: [SwissArmyTransformer](https://github.com/THUDM/SwissArmyTransformer/) and `torchvision`.

Run the CLI vision demo:

```bash
python cli_demo_vision.py
```

You will be prompted to enter an image path; the model describes the image and you can continue the conversation about it.

Run the web vision demo:

```bash
python web_demo_vision.py
```

This Gradio app accepts an uploaded image plus a text prompt, and automatically describes a newly uploaded image ("描述这张图片。"). Note that the vision demo uses `THUDM/visualglm-6b` as the model.

### Multi-GPU Deployment

`utils.py` provides helpers for splitting the 30 transformer layers (28 transformer blocks plus the word embeddings and final layernorm/lm_head) across multiple GPUs:

```python
from utils import load_model_on_gpus

model = load_model_on_gpus("THUDM/chatglm-6b", num_gpus=2)
```

The `auto_configure_device_map` function automatically assigns layers evenly across GPUs, keeping `transformer.word_embeddings`, `transformer.final_layernorm`, and `lm_head` on the first card to avoid device-mismatch errors on Linux. You can also pass a custom `device_map` dictionary.

## Fine-tuning with P-Tuning v2

The `ptuning/` directory implements parameter-efficient tuning of ChatGLM-6B based on [P-Tuning v2](https://github.com/THUDM/P-tuning-v2). P-Tuning v2 reduces trainable parameters to 0.1% of full fine-tuning; combined with quantization and gradient checkpointing, tuning requires a minimum of ~7GB GPU memory. See [ptuning/README.md](ptuning/README.md) (Chinese) or [ptuning/README_en.md](ptuning/README_en.md) (English) for full documentation.

### Software dependencies

Requires `transformers==4.27.1` plus:

```bash
pip install rouge_chinese nltk jieba datasets
```

### Dataset

The default example uses the [ADGEN](https://aclanthology.org/D19-1321.pdf) (advertisement generation) dataset, where the model generates an ad text (`summary`) from product attribute tags (`content`). Download the preprocessed ADGEN dataset from [Google Drive](https://drive.google.com/file/d/13_vf0xRTQsyneRKdD1bZIr93vBGOczrk/view?usp=sharing) or [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/f/b3f119a008264b1cabd1/?dl=1) and place the extracted `AdvertiseGen` directory under `ptuning/`.

### Training

P-Tuning v2 training:

```bash
bash train.sh
```

Key settings in `train.sh`:
- `PRE_SEQ_LEN` — soft prompt length (default 128)
- `LR` — learning rate (default 2e-2)
- `quantization_bit` — quantization level of the frozen base model; omit for FP16. The default (`quantization_bit=4`, `per_device_train_batch_size=1`, `gradient_accumulation_steps=16`) needs only ~6.7GB GPU memory.

Full-parameter fine-tuning with DeepSpeed:

```bash
bash ds_train_finetune.sh
```

### Multi-turn dialogue training

To fine-tune on multi-turn conversation data, provide JSON-lines records with a `history` field and run:

```bash
bash train_chat.sh
```

Specify `--history_column` (e.g. `history`) so the training script stitches the chat history into the prompt; content exceeding `max_source_length` is truncated.

### Evaluation

Run evaluation with:

```bash
bash evaluate.sh        # for P-Tuning v2 checkpoints
bash evaluate_finetune.sh  # for full fine-tuning checkpoints
```

Metrics are Chinese Rouge scores (Rouge-1, Rouge-2, Rouge-l) and BLEU-4. Predictions are written to `./output/<checkpoint>/generated_predictions.txt`.

For P-Tuning v2 checkpoints, evaluation needs both the base model and the prefix encoder weights (`--model_name_or_path THUDM/chatglm-6b --ptuning_checkpoint $CHECKPOINT`). Old full-parameter checkpoints load directly via `--model_name_or_path $CHECKPOINT`.

### Reported results (ADGEN)

|               | Finetune | P-tuning v2 | LoRA |
| ------------- | -------- | ----------- | ---- |
| BLEU-4        | 8.01     | 8.10        | 7.62 |
| Rouge-1       | 31.23    | 31.12       | 30.60 |
| Rouge-2       | 7.36     | 7.11        | 6.96 |
| Rouge-l       | 25.08    | 24.97       | 24.80 |
| Training Loss | 3.00     | 3.74        | 3.32 |

Experiment settings: `max_source_length=64`, `max_target_length=64`, `max_steps=3000`.

### Deploying a fine-tuned model

Load the tokenizer, then either load the base model plus the PrefixEncoder weights (new checkpoints), or load a full checkpoint directly. You can also launch a web demo with the fine-tuned checkpoint:

```bash
bash web_demo.sh
```

Edit `web_demo.sh` to point `--ptuning_checkpoint` at your actual checkpoint path.

### Using your own dataset

Modify `train_file`, `validation_file`, and `test_file` in `train.sh`/`evaluate.sh` to point to your own JSON/JSONL data, and set `prompt_column` and `response_column` to the corresponding keys. Adjust `max_source_length` and `max_target_length` to fit your data. Data files must be `.csv` or `.json` format.

## Project Structure

```
├── api.py                  # FastAPI OpenAI-style API server
├── cli_demo.py             # Command-line chat demo
├── cli_demo_vision.py      # Command-line demo for VisualGLM-6B
├── web_demo.py             # Gradio web demo (recommended)
├── web_demo2.py            # Streamlit web demo
├── web_demo_old.py         # Legacy Gradio web demo
├── web_demo_vision.py      # Gradio web demo for VisualGLM-6B
├── utils.py                # Multi-GPU model loading utilities
├── requirements.txt        # Python dependencies
├── ptuning/                # P-Tuning v2 / fine-tuning pipeline
│   ├── main.py             # Training/evaluation entry point
│   ├── arguments.py        # Model and data argument definitions
│   ├── trainer.py          # Modified HuggingFace Trainer
│   ├── trainer_seq2seq.py  # Seq2Seq trainer with generation
│   ├── train.sh            # P-Tuning v2 training script
│   ├── train_chat.sh       # Multi-turn dialogue training script
│   ├── ds_train_finetune.sh # DeepSpeed full fine-tuning script
│   ├── evaluate.sh         # Evaluation scripts
│   ├── web_demo.py/sh      # Web demo loading fine-tuned checkpoints
│   └── deepspeed.json      # DeepSpeed configuration
├── examples/               # Example task outputs (ads, emails, blogs, etc.)
├── limitations/            # Example known failure cases
├── improve/                # Badcase feedback program info and data samples
├── resources/              # Images, WeChat group info
├── FAQ.md                  # Frequently asked questions
├── PROJECT.md              # Links to community projects
├── UPDATE.md               # Release/update history
├── LICENSE                 # Apache 2.0 license
└── MODEL_LICENSE           # Model-specific license terms
```

## Known Limitations

Due to the model's size and the composition of its training data, ChatGLM-6B exhibits known weaknesses, with example cases in the `limitations/` directory:

- **Factual errors** on knowledge-intensive questions.
- **Mathematical errors** in calculation tasks.
- **Self-confusion**: the model may incorrectly identify itself as other assistants such as Google's, OpenAI's, or Tencent's models.

The model may also struggle with complex instructions, domain-specific concepts, and consistency across dialogue context.

## Community Badcase Feedback Program

The `improve/` directory describes the ChatGLM-6B Badcase feedback program. Community members can submit `prompt`/`response` pairs (JSONL format, one per line) providing corrected answers for cases where the model underperforms. Data is screened every 2–4 weeks, and qualifying examples are added to the training data for subsequent open model releases. Submissions must not contain personal information, trade secrets, or content that may harm national security or infringe third-party IP. See `improve/README.md` and `improve/data_sample.jsonl` for details.

## FAQ

See [FAQ.md](FAQ.md) for troubleshooting. Highlights:

- **Mac OpenMP error** (`clang: error: unsupported option '-fopenmp'`): install OpenMP from [mac.r-project.org/openmp](https://mac.r-project.org/openmp/) and clear the Hugging Face transformers module cache if errors persist.

## Contributing

Issues and pull requests are welcome. The repository provides GitHub issue templates:

- **Bug report** (`bug_report.yaml`): please search existing issues first, and include current/expected behavior, reproduction steps, and your environment (OS, Python, Transformers, PyTorch, CUDA availability).
- **Feature request** (`feature_request.yml`): describe the problem and proposed solution.

If you have built a project or tutorial based on ChatGLM-6B, you can add it to `PROJECT.md` via a pull request.

## Community and Related Projects

A curated list of acceleration/reimplementation and derivative projects lives in [PROJECT.md](PROJECT.md). Highlights include:

- **Inference acceleration/reimplementations**: lyraChatGLM (9000+ tokens/s), ChatGLM-MNN (C++ inference), JittorLLMs (runs with as little as 3GB VRAM or CPU-only), InferLLM (lightweight x86/Arm/mobile inference), SwissArmyTransformer (SAT-based implementation with P-tuning).
- **Applications built on ChatGLM-6B**: chatgpt_academic, 闻达 (wenda), langchain-ChatGLM, Chinese-LangChain, ChatGLM-web, Chuanhu Chat, ChatGLM-OpenAI-API, ChatSQL, and more.
- **Fine-tuning projects**: InstructGLM, ChatGLM-Efficient-Tuning, ChatGLM-Finetuning, ChatGLM-Tuning (LoRA).
- **Tutorials**: Windows deployment guide, Docker container setup guide.

For community discussion, scan the WeChat QR code in `resources/WECHAT.md` to join the "ChatGLM Discussion Group".

## Update History

Key milestones (full details in [UPDATE.md](UPDATE.md)):

- **2023/03/19**: Added `stream_chat` streaming output, INT4 quantized model.
- **2023/03/23**: Added API deployment, Apple Silicon GPU support, embedding-quantized INT4-QE model.
- **2023/03/31**: Added P-Tuning v2 fine-tuning (min. 7GB GPU memory at INT4).
- **2023/04/06**: Improved web demo UI, removed image tokens from embeddings, removed `icetk` dependency.
- **2023/04/16**: Added INT8 quantized model and multi-GPU deployment.
- **2023/05/15**: v1.1 checkpoint with balanced Chinese/English training data.
- **2023/05/17**: Released VisualGLM-6B multimodal support with CLI and web demos.

## License

- The **code** in this repository is licensed under the **Apache License 2.0** (copyright Zhengxiao Du).
- The **model weights** are subject to a separate license — see [MODEL_LICENSE](MODEL_LICENSE) for the terms governing use of the ChatGLM-6B model itself.

Please consult both files before using or redistributing this project.

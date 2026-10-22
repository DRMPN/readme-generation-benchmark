# ChatGLM-6B

ChatGLM-6B is a bilingual (Chinese and English) conversational language model. This repository provides the model's demo applications (command line, web, streaming, and API), a P-Tuning v2 fine-tuning implementation in `ptuning/`, and supporting documentation. The repository also includes a multimodal variant, VisualGLM-6B, with its own demo scripts.

## Overview

The repository contains the following main components:

- **Model demos** that load `THUDM/chatglm-6b` from Hugging Face:
  - `cli_demo.py`: a terminal chat loop with streaming output.
  - `web_demo.py`: a Gradio web interface.
  - `web_demo2.py`: a Streamlit interface that uses `streamlit_chat`.
  - `web_demo_old.py`: an older Gradio interface.
  - `api.py`: a FastAPI service that exposes the model over HTTP.
- **VisualGLM-6B demos** (`cli_demo_vision.py`, `web_demo_vision.py`) for image understanding. These load `THUDM/visualglm-6b`.
- **Parameter-efficient fine-tuning** in `ptuning/`, based on [P-Tuning v2](https://github.com/THUDM/P-tuning-v2). The `ptuning/README.md` describes it in Chinese, and `ptuning/README_en.md` describes it in English.
- **Utilities**: `utils.py` provides helpers for loading the model across multiple GPUs.
- **Documentation and examples**: FAQ, update notes, a list of related projects, example images, and a Badcase feedback plan (`improve/README.md`).

The `UPDATE.md` file lists notable changes. For example, the v1.1 checkpoint (2023/05/15) added English instruction data to balance Chinese and English training data. The INT4 and INT8 quantized models were released in March and April 2023.

## Requirements

- Python with the packages in `requirements.txt`:
  - `protobuf`
  - `transformers==4.27.1`
  - `cpm_kernels`
  - `torch>=1.10`
  - `gradio`
  - `mdtex2html`
  - `sentencepiece`
  - `accelerate`
- A CUDA GPU is assumed by most scripts, which call `.half().cuda()` when loading the model. The FAQ and update notes also mention GPU inference on Apple Silicon Macs and a CPU-oriented workaround involving OpenMP.

## Setup

1. Clone the repository and move into it.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The code requires `transformers==4.27.1`, which is pinned in `requirements.txt`.

3. The scripts download model weights from Hugging Face using the identifier `THUDM/chatglm-6b` (or `THUDM/visualglm-6b` for the vision demos). To use a local copy, replace this identifier in the relevant script with your local path. The `ptuning/README.md` also describes loading from a local model path.

4. Optional dependencies, which are not listed in `requirements.txt`:
   - `streamlit` and `streamlit_chat` for `web_demo2.py`.
   - `SwissArmyTransformer` and `torchvision` for VisualGLM-6B, as noted in `UPDATE.md`.
   - `rouge_chinese nltk jieba datasets` for fine-tuning, as noted in `ptuning/README.md`.
   - `deepspeed` for full-parameter fine-tuning (`ds_train_finetune.sh`).

5. **macOS note:** The FAQ describes an error (`clang: error: unsupported option '-fopenmp'`) when loading a quantized model on a Mac. It explains that the OpenMP library must be installed separately. Without it, the model runs on a single core. The FAQ provides commands to install the OpenMP package and recommends clearing the Hugging Face module cache after a failed run.

## Usage

### Command-line demo

```bash
python cli_demo.py
```

Type input at the `用户：` prompt. Type `clear` to reset the conversation history and `stop` to exit. The demo streams responses by calling `model.stream_chat`.

### Web demo (Gradio)

```bash
python web_demo.py
```

The script launches a Gradio interface and opens it in a browser (`inbrowser=True`). It provides sliders for Maximum length, Top P, and Temperature, and a button to clear the history.

### Streamlit demo

```bash
streamlit run web_demo2.py
```

This script requires `streamlit` and `streamlit_chat`, which are not included in `requirements.txt`.

### API server

```bash
python api.py
```

The server listens on `0.0.0.0:8000`. It accepts JSON `POST` requests at the root path (`/`). The accepted fields are `prompt`, `history`, `max_length`, `top_p`, and `temperature`. The response contains `response`, `history`, `status`, and `time`.

Example request, based on the fields the code reads:

```bash
curl -X POST http://127.0.0.1:8000 \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你好", "history": []}'
```

### VisualGLM-6B demos

```bash
python cli_demo_vision.py
python web_demo_vision.py
```

The command-line demo asks for an image path, then describes the image using the query `描述这张图片。` (Describe this picture). The web demo lets you upload an image and chat about it.

## Configuration

Most configuration is done by editing constants or defaults in the source files:

- **Model identifier:** `THUDM/chatglm-6b` or `THUDM/visualglm-6b`, hard-coded in each demo script.
- **Device:** `api.py` defines `DEVICE = "cuda"` and `DEVICE_ID = "0"`.
- **Generation parameters:**
  - `api.py` defaults: `max_length=2048`, `top_p=0.7`, `temperature=0.95`, applied when the request does not supply them.
  - `web_demo.py` sliders: Maximum length (0–4096, default 2048), Top P (default 0.7), and Temperature (default 0.95).
  - `web_demo_vision.py` defaults: Top P 0.4 and Temperature 0.8.
- **Multi-GPU loading:** `utils.py` provides `load_model_on_gpus(checkpoint_path, num_gpus=2, device_map=None)`. It uses `auto_configure_device_map(num_gpus)` to distribute the 28 transformer layers, plus the embedding and output layers, across the available GPUs.

Fine-tuning parameters are set in the shell scripts in `ptuning/` and in `ptuning/arguments.py`. Key options include:

- `--model_name_or_path`: the base model.
- `--pre_seq_len`: the length of the soft prompt (`PRE_SEQ_LEN`, set to 128 in `train.sh`).
- `--quantization_bit`: the quantization level of the frozen base model (4 in the P-Tuning scripts).
- `--prompt_column` and `--response_column`: the JSON keys for input and output text.
- `--history_column`: the JSON key for chat history, used for multi-turn data.
- `--max_source_length` and `--max_target_length`: input and output token limits.

## Fine-tuning with P-Tuning v2

The `ptuning/` directory contains the fine-tuning code. According to `ptuning/README.md`, P-Tuning v2 freezes the base model and trains a small prefix encoder. The README reports that it reduces the trainable parameters to 0.1% of the full model and runs in as little as 7 GB of GPU memory with quantization and gradient checkpointing.

### Data

The examples use the ADGEN (advertisement generation) dataset. Download the processed dataset from the links in `ptuning/README.md`, then place the extracted `AdvertiseGen` directory inside `ptuning/`. Each record has a `content` field (the input) and a `summary` field (the target advertisement text).

### Training

```bash
cd ptuning
bash train.sh
```

The default `train.sh` settings are `PRE_SEQ_LEN=128`, `LR=2e-2`, `quantization_bit 4`, `per_device_train_batch_size 1`, `gradient_accumulation_steps 16`, and `max_steps 3000`. The README notes that these settings yield an effective batch size of 16.

For full-parameter fine-tuning with DeepSpeed, install `deepspeed` and run `bash ds_train_finetune.sh`. The configuration is in `deepspeed.json`.

For multi-turn training data, use `bash train_chat.sh`. It expects `CHAT_TRAIN_DATA`, `CHAT_VAL_DATA`, and `CHECKPOINT_NAME` to be set.

### Evaluation and inference

- `bash evaluate.sh` runs prediction with a P-Tuning v2 checkpoint. It writes `generated_predictions.txt` to the output directory.
- `evaluate_finetune.sh` evaluates a full fine-tuned checkpoint.
- `bash web_demo.sh` launches the P-Tuning web demo (`ptuning/web_demo.py`) with a checkpoint.

Evaluation uses Chinese ROUGE and BLEU-4 metrics, computed with `rouge_chinese`, `jieba`, and `nltk`. The results table in `ptuning/README.md` compares Finetune, P-tuning v2, and LoRA on ADGEN:

| | Finetune | P-tuning v2 | LoRA |
|---|---|---|---|
| BLEU-4 | 8.01 | 8.10 | 7.62 |
| Rouge-1 | 31.23 | 31.12 | 30.60 |
| Rouge-2 | 7.36 | 7.11 | 6.96 |
| Rouge-l | 25.08 | 24.97 | 24.80 |

## Development

- **Project structure:** Demo scripts live at the repository root. Fine-tuning code lives in `ptuning/`, which contains its own `README.md` and `README_en.md`.
- **Issue templates:** `.github/ISSUE_TEMPLATE/` provides a bug report form (`bug_report.yaml`) and a feature request form (`feature_request.yml`). `config.yml` sets `blank_issues_enabled: false`, so users must choose a template.
- **Contributing related projects:** `PROJECT.md` lists open-source projects that accelerate, reimplement, build on, or fine-tune ChatGLM-6B. It invites additions through a pull request.
- **Data feedback:** `improve/README.md` describes the ChatGLM-6B Badcase feedback plan. It asks users to submit corrected prompt/response pairs in JSON Lines format (`{"prompt": ..., "response": ...}`). `improve/data_sample.jsonl` contains sample data. The document asks contributors not to submit personal information, trade secrets, or content that infringes third-party rights.
- **Community:** `resources/WECHAT.md` links to a WeChat discussion group.

## Testing

The repository does not include an automated test suite, such as a `tests/` directory or a test runner configuration. The only quantitative evaluation is the ADGEN metric pipeline in `ptuning/`, which generates predictions and computes ROUGE and BLEU-4 scores. Other validation is manual, through the demo applications.

## License

- **Code:** Licensed under the Apache License, Version 2.0, as stated in the `LICENSE` file. The copyright notice in that file's appendix reads "Copyright Zhengxiao Du."
- **Model:** The repository includes a separate `MODEL_LICENSE` file. Its contents were not included in the supplied files, so this README does not summarize its terms. Review `MODEL_LICENSE` before using or redistributing the model weights.

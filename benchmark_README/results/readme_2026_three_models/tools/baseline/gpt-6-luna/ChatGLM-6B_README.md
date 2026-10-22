# ChatGLM-6B

This repository provides demos, an HTTP API, and parameter-efficient fine-tuning code for ChatGLM-6B. It also includes command-line and web demos for VisualGLM-6B, a multimodal conversational model that supports image understanding.

The included demos load pretrained model and tokenizer files through Hugging Face Transformers using `trust_remote_code=True`. The standard ChatGLM-6B examples use `THUDM/chatglm-6b`; the vision examples use `THUDM/visualglm-6b`. The repository also contains P-Tuning v2 training and evaluation scripts, example screenshots, and project update and FAQ documents.

> Model-generated answers can contain factual errors, mishandle complex instructions, produce harmful content, or lose consistency across a conversation. Review generated content before relying on it.

## Contents

- `cli_demo.py`, `web_demo.py`, `web_demo2.py`, and `web_demo_old.py`: text-chat demos.
- `cli_demo_vision.py` and `web_demo_vision.py`: VisualGLM image-chat demos.
- `api.py`: a FastAPI endpoint for text chat.
- `ptuning/`: P-Tuning v2 and full fine-tuning scripts, trainer code, and instructions.
- `FAQ.md`: troubleshooting notes.
- `UPDATE.md`: project update history, including model and demo changes.
- `improve/`: information about submitting model bad cases and example data.

## Requirements and installation

The root `requirements.txt` lists these dependencies: `protobuf`, `transformers==4.27.1`, `cpm_kernels`, `torch>=1.10`, `gradio`, `mdtex2html`, `sentencepiece`, and `accelerate`. The demos load the model in half precision on CUDA, so the supplied demo scripts expect a CUDA-capable PyTorch environment.

Create and activate a virtual environment, then install the listed packages:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. Install a PyTorch build appropriate for your system and CUDA setup if the default installation does not provide the required GPU support.

The first run of a demo loads its model from the Hugging Face model identifier in the script. For P-Tuning, install the additional dependencies:

```bash
pip install rouge_chinese nltk jieba datasets
```

VisualGLM demos require additional dependencies not listed in the root requirements: install [SwissArmyTransformer](https://github.com/THUDM/SwissArmyTransformer/) and `torchvision`, as described in `UPDATE.md`.

## Usage

### Command-line chat

Run the text demo from the repository root:

```bash
python cli_demo.py
```

Enter a message to start a conversation. Type `clear` to clear conversation history or `stop` to exit. The demo streams responses as they are generated.

For image conversations, run:

```bash
python cli_demo_vision.py
```

Enter an image path when prompted, then ask follow-up questions. This script loads VisualGLM-6B.

### Web demos

Launch the Gradio text demo with:

```bash
python web_demo.py
```

The interface supports streaming chat, conversation history, and controls for maximum generation length, `top_p`, and temperature. It launches with `share=False` and opens a browser window. The repository also includes a Streamlit alternative (`web_demo2.py`) and an older Gradio interface (`web_demo_old.py`).

For image chat, run:

```bash
python web_demo_vision.py
```

Upload an image and enter a prompt, or upload an image to request a description. The vision interface also provides generation controls and a clear-history action.

### HTTP API

`api.py` defines a FastAPI `POST /` endpoint and starts Uvicorn on port `8000` when run directly. FastAPI and Uvicorn are imported by this file but are not listed in the root requirements, so install them separately:

```bash
pip install fastapi uvicorn
python api.py
```

Send JSON with a `prompt` and, optionally, `history`, `max_length`, `top_p`, and `temperature`. For example:

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"prompt":"你好","history":[],"max_length":2048,"top_p":0.7,"temperature":0.95}'
```

The response includes `response`, updated `history`, a `status` value, and a timestamp in `time`. The API script loads the text model onto CUDA and configures Uvicorn for one worker.

## Configuration and deployment

The demo scripts specify their model identifiers and device placement in code. The basic chat and vision demos use `.half().cuda()`. To use a local model copy, change the `from_pretrained` model identifier in the relevant script to its local path. The web demo sliders and API defaults define generation settings; for the API, omitted or false-valued settings fall back to a maximum length of `2048`, `top_p=0.7`, and `temperature=0.95`.

`utils.py` provides `load_model_on_gpus` and `auto_configure_device_map` for loading a model across multiple GPUs. The update notes also describe multi-GPU deployment. For Mac users encountering an OpenMP `-fopenmp` error with a quantized model, see the OpenMP guidance in `FAQ.md`.

## Fine-tuning

The `ptuning/` directory implements P-Tuning v2 and full-parameter fine-tuning. The scripts use ChatGLM-6B and show ADGEN, an advertising-generation dataset, as an example. Follow [`ptuning/README.md`](ptuning/README.md) or its [English instructions](ptuning/README_en.md) for dataset download, checkpoint loading, and deployment details.

The example scripts expect the processed dataset under `ptuning/AdvertiseGen/`. Start P-Tuning v2 training from that directory:

```bash
cd ptuning
bash train.sh
```

The script sets `PRE_SEQ_LEN`, `LR`, data paths, input and output columns, sequence lengths, batch sizes, training steps, and quantization. Its example uses a prefix length of `128`, learning rate `2e-2`, and 4-bit quantization. Adjust these values and the data paths for your task and hardware. The documented default P-Tuning configuration uses gradient accumulation; memory use depends on batch size and quantization settings.

For full-parameter fine-tuning, the supplied script requires DeepSpeed and launches a four-GPU run:

```bash
bash ds_train_finetune.sh
```

Training and evaluation accept JSON or CSV data files through arguments such as `--train_file`, `--validation_file`, and `--test_file`. Specify the input and output field names with `--prompt_column` and `--response_column`. For conversational datasets, provide a history field containing prior query/response pairs and set `--history_column` (for example, `history`). Input and target lengths can be controlled with `--max_source_length` and `--max_target_length`.

P-Tuning v2 checkpoints contain PrefixEncoder parameters; inference therefore loads both the base model and the checkpoint. The included `evaluate.sh` and `web_demo.sh` illustrate the checkpoint arguments. Evaluation computes Chinese Rouge and BLEU-4 metrics and writes generated predictions to `generated_predictions.txt`.

## Development and testing

The repository does not include a dedicated automated test suite. For a basic installation check, run a demo in an environment with the required model access and GPU support, or start the API and send a request to `POST /`. Training scripts can also be exercised with a small dataset using the sample-limit arguments supported by `ptuning/main.py`.

When reporting a bug, search existing issues first and include reproduction steps and environment details such as operating system, Python, Transformers, PyTorch, and CUDA support. Feature requests should describe the proposed solution. The issue templates provide these prompts.

## License

The repository includes an Apache License 2.0 `LICENSE` file. A separate `MODEL_LICENSE` file is also present; review it for the terms that apply to model use. The code license does not by itself establish the licensing terms for pretrained model weights or other separately licensed materials.

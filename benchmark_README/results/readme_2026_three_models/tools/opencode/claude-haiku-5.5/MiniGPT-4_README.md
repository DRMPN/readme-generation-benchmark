# MiniGPT-4 and MiniGPT-v2

This repository contains the code for **MiniGPT-4** and **MiniGPT-v2**, vision-language models that connect a visual encoder to a large language model so the model can answer questions about images and chat about them. The repository includes model code, Gradio demos, training and evaluation scripts, dataset preparation notes, and configuration files.

Project links referenced in the repository:

- MiniGPT-4 project page: https://minigpt-4.github.io
- MiniGPT-v2 project page: https://minigpt-v2.github.io
- MiniGPT-v2 paper: [`MiniGPTv2.pdf`](MiniGPTv2.pdf) (included in this repository)

## Contents

- [Repository layout](#repository-layout)
- [Model variants](#model-variants)
- [Installation](#installation)
- [Model weights and configuration](#model-weights-and-configuration)
- [Running the demos](#running-the-demos)
- [Training](#training)
- [Evaluation](#evaluation)
- [Datasets](#datasets)
- [Known gaps](#known-gaps)
- [License](#license)

## Repository layout

| Path | Purpose |
| --- | --- |
| `demo.py` | Gradio demo for MiniGPT-4 (Vicuna or LLaMA-2 based configs). |
| `demo_v2.py` | Gradio demo for MiniGPT-v2 with grounding, referring, detection, identification, and VQA prompts. |
| `train.py` | Training entry point. Launch with `torchrun`. |
| `minigpt4/` | Python package: models, datasets, processors, tasks, runners, conversation templates, and common utilities. |
| `minigpt4/configs/` | Default model, dataset, and runner configs (`models/`, `datasets/`). |
| `train_configs/` | YAML configs for MiniGPT-4 stage 1 and stage 2, and MiniGPT-v2 fine-tuning. |
| `eval_configs/` | YAML configs for MiniGPT-4 and MiniGPT-v2 inference and benchmark evaluation. |
| `eval_scripts/` | `eval_ref.py` (referring expression evaluation) and `eval_vqa.py` (VQA-style evaluation), plus [`EVAL_README.md`](eval_scripts/EVAL_README.md). |
| `dataset/` | Dataset preparation notes and conversion scripts (`convert_cc_sbu.py`, `convert_laion.py`). |
| `examples/`, `examples_v2/`, `figs/` | Example images and figures. |
| `environment.yml` | Conda environment specification. |
| `MiniGPT4_Train.md`, `MiniGPTv2_Train.md` | Training instructions for each model. |

## Model variants

The model is selected by the `arch` and `model_type` fields in a config file.

| Config | `arch` | `model_type` | Language model | Notes |
| --- | --- | --- | --- | --- |
| `eval_configs/minigpt4_eval.yaml` | `minigpt4` | `pretrain_vicuna0` | Vicuna (path set via `llama_model` in `minigpt4/configs/models/minigpt4_vicuna0.yaml`) | Image size 224; `low_resource: True`. |
| `eval_configs/minigpt4_llama2_eval.yaml` | `minigpt4` | `pretrain_llama2` | LLaMA-2-chat-7B | Image size 224; `low_resource: True`. |
| `eval_configs/minigptv2_eval.yaml` | `minigpt_v2` | `pretrain` | LLaMA-2-chat-7B | Image size 448; LoRA rank 64, alpha 16. Default config for `demo_v2.py`. |

## Installation

The repository provides a Conda environment file, `environment.yml`, which creates an environment named `minigptv` with Python 3.9. There is no `requirements.txt` in this repository.

```bash
conda env create -f environment.yml
conda activate minigptv
```

Pinned versions in `environment.yml` include `torch==2.0.0`, `transformers==4.30.0`, `gradio==3.47.1`, `peft==0.2.0`, `accelerate==0.20.3`, and `bitsandbytes==0.37.0`. The demos and model code place models on `cuda:<gpu-id>` (see `demo.py` and `demo_v2.py`), so a CUDA-capable GPU is required.

## Model weights and configuration

This repository does not include model weights or the base language model. Before running anything, set the paths in the relevant YAML config:

- **`llama_model`**: path to the base language model. The configs refer to a Vicuna model for `pretrain_vicuna0` and to LLaMA-2-chat-7B for `pretrain_llama2` and MiniGPT-v2.
- **`ckpt`**: path to the pretrained MiniGPT checkpoint. The eval configs ship with a placeholder value that must be replaced.

Checkpoints linked from the repository's documentation:

- MiniGPT-4 stage-1-only checkpoints (13B and 7B) are linked in [`MiniGPT4_Train.md`](MiniGPT4_Train.md). The documentation notes that this checkpoint generates incomplete and repeated sentences more often than the model after stage 2.
- MiniGPT-v2 checkpoints (after stage 2, after stage 3, and the online developing demo version) are linked in [`MiniGPTv2_Train.md`](MiniGPTv2_Train.md).

The repository does not link a final MiniGPT-4 (post stage 2) checkpoint.

For the `minigpt4` architecture, `low_resource: True` loads the language model in 8-bit and places the vision encoder on CPU, according to a code comment in `minigpt4/models/minigpt4.py`.

## Running the demos

### MiniGPT-4 demo (`demo.py`)

`--cfg-path` is required. `--gpu-id` selects the GPU (default `0`).

```bash
python demo.py --cfg-path eval_configs/minigpt4_eval.yaml --gpu-id 0
```

Use `eval_configs/minigpt4_llama2_eval.yaml` for the LLaMA-2 variant. Set `llama_model` and `ckpt` in the config first.

The demo supports image upload, a chat interface, and adjustable beam count and temperature. It calls `demo.launch(share=True, ...)`, which creates a public share link when it starts.

### MiniGPT-v2 demo (`demo_v2.py`)

The default config is `eval_configs/minigptv2_eval.yaml`.

```bash
python demo_v2.py --cfg-path eval_configs/minigptv2_eval.yaml --gpu-id 0
```

The demo supports these task prompts, selectable from the interface:

| Task | Prompt prefix | Behavior |
| --- | --- | --- |
| No tag | (none) | Free-form chat. |
| Grounding | `[grounding]` | Grounded image description. |
| Refer | `[refer]` | Locate an object described by a phrase. |
| Detection | `[detection]` | Locate objects named in a caption or phrase. |
| Identify | `[identify]` | Identify an object inside a drawn bounding box. |
| VQA | `[vqa]` | Short answer to a visual question. |

The demo also calls `demo.launch(share=True, ...)`.

## Training

Training is run with `train.py` through `torchrun`. Each training config sets `output_dir` (under `run:`) for checkpoints. Training configs set `wandb_log: True` by default, so `train.py` calls `wandb.login()` and expects Weights & Biases to be set up, unless you change that setting.

### MiniGPT-4

MiniGPT-4 training has two stages, as described in [`MiniGPT4_Train.md`](MiniGPT4_Train.md).

1. **Stage 1 (pretraining):** aligns the vision and language models using image-text pairs from LAION and CC/SBU. Data preparation is described in [`dataset/README_1_STAGE.md`](dataset/README_1_STAGE.md). The experiments in the documentation used 4 A100 GPUs.

   ```bash
   torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
   ```

2. **Stage 2 (fine-tuning):** uses a small, curated image-text dataset converted to a conversation format. Data preparation is described in [`dataset/README_2_STAGE.md`](dataset/README_2_STAGE.md). The experiments used 1 A100 GPU. Set `ckpt` in `train_configs/minigpt4_stage2_finetune.yaml` to the stage-1 checkpoint before running.

   ```bash
   torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigpt4_stage2_finetune.yaml
   ```

### MiniGPT-v2

Fine-tuning is described in [`MiniGPTv2_Train.md`](MiniGPTv2_Train.md). Dataset preparation is in [`dataset/README_MINIGPTv2_FINETUNE.md`](dataset/README_MINIGPTv2_FINETUNE.md). In `train_configs/minigptv2_finetune.yaml`, set:

- `model.llama_model`: path to the LLaMA checkpoint.
- `model.ckpt`: path to the pretrained checkpoint to start from.
- `run.output_dir`: path where checkpoints are saved.

```bash
torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigptv2_finetune.yaml
```

The fine-tuning config mixes many datasets, each with a `sample_ratio`, including COCO captions and VQA, Visual Genome, TextCaps, RefCOCO/RefCOCO+/RefCOCOg, OK-VQA, AOK-VQA, OCR-VQA, GQA, Flickr-30k, LLaVA, multitask conversation, and unnatural instructions.

Other training configs in `train_configs/` include `minigpt4_llama2_stage1_pretrain.yaml`, `minigpt4_llama2_stage2_finetune.yaml`, and `minigpt4_stage1_pretrain.yaml`.

## Evaluation

Evaluation for MiniGPT-v2 is described in [`eval_scripts/EVAL_README.md`](eval_scripts/EVAL_README.md). Before running, set `llama_model`, `ckpt`, and the dataset paths (`eval_file_path`, `img_path`, `save_path`) in `eval_configs/minigptv2_benchmark_evaluation.yaml`. The shared evaluation parser also accepts `--cfg-path`, `--name`, `--max_new_tokens`, and `--batch_size`.

Set `PYTHONPATH` to the repository root first:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/MiniGPT-4
```

**Referring expressions** (RefCOCO, RefCOCO+, RefCOCOg):

```bash
torchrun --master-port ${port} --nproc_per_node 1 eval_scripts/eval_ref.py \
  --cfg-path ${cfg_path} --dataset refcoco,refcoco+,refcocog --resample
```

**Visual question answering** (OK-VQA, VizWiz, IconQA, GQA, VSR, hateful memes):

```bash
torchrun --master-port ${port} --nproc_per_node 1 eval_scripts/eval_vqa.py \
  --cfg-path ${cfg_path} --dataset okvqa,vizwiz,iconvqa,gqa,vsr,hm
```

The `--dataset` values are checked by name in `eval_vqa.py`. Results are written to the `save_path` set in the config. Evaluation expects the dataset folder structure shown in `eval_scripts/EVAL_README.md`.

## Datasets

Dataset preparation notes are in `dataset/`:

- [`README_1_STAGE.md`](dataset/README_1_STAGE.md): LAION and CC/SBU filtered synthetic captions, downloaded with `img2dataset`. Conversion scripts are `dataset/convert_cc_sbu.py` and `dataset/convert_laion.py`. Dataset paths are set in `minigpt4/configs/datasets/laion/defaults.yaml` and `minigpt4/configs/datasets/cc_sbu/defaults.yaml`. The documentation says the LAION and CC/SBU data together need about 2.3 TB of storage.
- [`README_2_STAGE.md`](dataset/README_2_STAGE.md): the stage-2 alignment dataset (`cc_sbu_align`). Set the path in `minigpt4/configs/datasets/cc_sbu/align.yaml`.
- [`README_MINIGPTv2_FINETUNE.md`](dataset/README_MINIGPTv2_FINETUNE.md): COCO, VQAv2, Visual Genome, TextCaps, RefCOCO family, OK-VQA, AOK-VQA, OCR-VQA, GQA, Flickr-30k, LLaVA, multitask conversation, and unnatural instruction data.

Dataset sources and licenses are those of the original providers. Check each source's terms before use.

## Known gaps

- `train_configs/minigpt4_stage2_finetune.yaml` sets `prompt_path: "prompts/alignment.txt"`, but no `prompts/` directory exists in this repository. The model code only reads this file when the path is set, so the file must be provided if that config is used.
- `MiniGPT4_Train.md` links to `train_configs/minigpt4_stage1_pretrain.yaml` in the stage-2 section. The stage-2 config is `train_configs/minigpt4_stage2_finetune.yaml`.
- `demo.py` and `demo_v2.py` use `share=True` when launching, which creates a public Gradio link.

## License

The code is released under the BSD 3-Clause License. See [`LICENSE.md`](LICENSE.md) (Copyright 2023 Deyao Zhu). The repository also includes [`LICENSE_Lavis.md`](LICENSE_Lavis.md) for code derived from Salesforce LAVIS, and the VQA tools in `minigpt4/common/vqa_tools/` have their own `license.txt`.

Model weights, base language models (Vicuna, LLaMA-2), and datasets are governed by their own licenses and are not included in this repository.

For security reports, see [`SECURITY.md`](SECURITY.md). For community guidelines, see [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

# MiniGPT-4 and MiniGPT-v2

This repository contains the code for MiniGPT-4 and MiniGPT-v2, vision-language models that connect a visual encoder to a large language model. It includes a Gradio demo, training configurations and instructions, dataset preparation notes, and evaluation scripts for MiniGPT-v2.

## Overview

The codebase is organized around a registry-based framework under the `minigpt4/` package:

- **Models** (`minigpt4/models/`): `MiniGPT4` and `MiniGPTv2` built on a shared `MiniGPTBase`. The vision encoder is an EVA ViT-g implementation (`eva_vit.py`). MiniGPT-4 uses a Q-Former (`Qformer.py`) and a linear projection (`llama_proj`) into the language model's embedding space. The language model is loaded from a LLaMA-family checkpoint, and LoRA is supported through `peft`.
- **Configs** (`minigpt4/configs/`, `train_configs/`, `eval_configs/`): YAML files that define model architecture, dataset loaders, and training or evaluation settings.
- **Datasets and processors** (`minigpt4/datasets/`, `minigpt4/processors/`): dataset builders for image-text pairs, conversation data, grounding (RefCOCO family, Visual Genome, Flickr), and VQA benchmarks.
- **Training** (`train.py`, `minigpt4/runners/`, `minigpt4/tasks/`): a training entry point that builds the task, datasets, and model from a config file.
- **Conversation** (`minigpt4/conversation/`): prompt templates and a `Chat` class used by the demos.

The repository includes two demos:

- `demo.py`: the MiniGPT-4 Gradio demo.
- `demo_v2.py`: the MiniGPT-v2 Gradio demo, which supports task tags such as `[grounding]`, `[refer]`, `[detection]`, `[identify]`, and `[vqa]`.

Example images are provided in `examples/`, `examples_v2/`, and `figs/`.

## Setup

### Environment

A conda environment is defined in `environment.yml`:

```bash
conda env create -f environment.yml
conda activate minigptv
```

The environment targets Python 3.9 and pins several packages, including `torch==2.0.0`, `transformers==4.30.0`, `timm==0.6.13`, `peft==0.2.0`, `accelerate==0.20.3`, `bitsandbytes==0.37.0`, and `gradio==3.47.1`. It also installs `cudatoolkit`, so a CUDA-capable GPU is expected by the code, which calls `cuda:{gpu_id}` directly.

### Model weights

- **LLaMA-family language model:** the configs require a local path to a LLaMA checkpoint (for MiniGPT-v2, `llama_model` in `train_configs/minigptv2_finetune.yaml`). The repository does not include these weights.
- **Pretrained MiniGPT checkpoints:** the training documentation links to stage-one MiniGPT-4 checkpoints (7B and 13B) and to MiniGPT-v2 checkpoints after stage 2 and stage 3, plus an online-demo checkpoint. Set the `ckpt` field in the relevant config to the downloaded file.

## Usage

### MiniGPT-4 demo

`demo.py` requires a config file path and optionally a GPU index:

```bash
python demo.py --cfg-path eval_configs/minigpt4_eval.yaml --gpu-id 0
```

The `eval_configs/` directory includes `minigpt4_eval.yaml` (Vicuna-based) and `minigpt4_llama2_eval.yaml` (LLaMA-2-based). Set `ckpt` in the chosen file first. The demo calls `demo.launch(share=True, enable_queue=True)`, so Gradio will create a public share link.

### MiniGPT-v2 demo

`demo_v2.py` defaults to `eval_configs/minigptv2_eval.yaml`:

```bash
python demo_v2.py --cfg-path eval_configs/minigptv2_eval.yaml --gpu-id 0
```

Set `ckpt` in `eval_configs/minigptv2_eval.yaml` before running. The interface offers task shortcuts for grounding, referring, detection, identification (drawing a bounding box on the image), and VQA, along with free-form chat.

### Training

Training is launched with `torchrun` and `train.py`:

```bash
torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```

MiniGPT-4 training has two stages:

1. **Stage 1 (alignment pretraining)** uses `train_configs/minigpt4_stage1_pretrain.yaml`, which draws on LAION and Conceptual Captions/SBU data. The authors report using 4 A100 GPUs.
2. **Stage 2 (finetuning)** uses `train_configs/minigpt4_stage2_finetune.yaml` on a smaller high-quality dataset. Set `ckpt` in this file to the stage-1 checkpoint. The authors report using 1 A100 GPU.

Equivalent LLaMA-2 configurations are provided as `minigpt4_llama2_stage1_pretrain.yaml` and `minigpt4_llama2_stage2_finetune.yaml`.

For MiniGPT-v2, run:

```bash
torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigptv2_finetune.yaml
```

Before this, set `llama_model`, `ckpt`, and `output_dir` in that file.

### Evaluation (MiniGPT-v2)

Evaluation scripts are in `eval_scripts/`. First, set `PYTHONPATH` to the repository root:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/MiniGPT-4
```

Then fill in `eval_configs/minigptv2_benchmark_evaluation.yaml`, including `llama_model`, `ckpt`, each dataset's `eval_file_path` and `img_path`, and `save_path`.

Referring expression comprehension (`refcoco`, `refcoco+`, `refcocog`):

```bash
torchrun --master-port ${port} --nproc_per_node 1 eval_ref.py \
 --cfg-path ${cfg_path} --dataset refcoco,refcoco+,refcocog --resample
```

Visual question answering (`okvqa`, `vizwiz`, `iconvqa`, `gqa`, `vsr`, `hm`):

```bash
torchrun --master-port ${port} --nproc_per_node 1 eval_vqa.py \
 --cfg-path ${cfg_path} --dataset okvqa,vizwiz,iconvqa,gqa,vsr,hm
```

See `eval_scripts/EVAL_README.md` for the expected evaluation dataset layout.

## Configuration

Configuration is YAML-based and merged with defaults from the model and dataset registries. Key fields include:

| Field | Location | Purpose |
|---|---|---|
| `arch`, `model_type` | `model:` | Selects the model class (`minigpt4` or `minigpt_v2`) and its pretrained config. |
| `ckpt` | `model:` | Path to a pretrained or finetuned checkpoint. |
| `llama_model` | `model:` | Path to the LLaMA checkpoint (MiniGPT-v2 configs). |
| `end_sym`, `prompt_template` | `model:` | Conversation stop symbol and prompt format, e.g., `###Human: {} ###Assistant: ` for Vicuna-based MiniGPT-4. |
| `low_resource` | `model:` | Enables 8-bit loading in the eval configs. |
| `lora_r`, `lora_alpha` | `model:` | LoRA settings used by MiniGPT-v2. |
| `image_size` | `vis_processor` | Input resolution (224 for MiniGPT-4, 448 for MiniGPT-v2 training and evaluation). |
| `batch_size`, `sample_ratio` | `datasets:` | Per-dataset batch size and sampling weight. |
| `init_lr`, `min_lr`, `warmup_steps`, `max_epoch`, `iters_per_epoch` | `run:` | Optimizer and schedule settings. |
| `output_dir` | `run:` | Where training outputs are saved. |
| `wandb_log`, `job_name` | `run:` | Weights & Biases logging; the training script calls `wandb.login()` when enabled. |

`minigpt4/configs/default.yaml` sets `env.cache_root`, which is used for cached files. Its value points to an internal path and is commented as intended for persistent storage; adjust it for your environment.

Dataset paths are configured in per-dataset YAML files under `minigpt4/configs/datasets/`. For example, the LAION and CC/SBU loading paths are set on line 5 of their `defaults.yaml` files, and the second-stage path is set in `cc_sbu/align.yaml`.

## Datasets

Dataset preparation instructions are in `dataset/`:

- **`README_1_STAGE.md`**: downloads BLIP-filtered synthetic captions for LAION and CC3M+CC12M+SBU. It notes that about 2.3 TB is needed for storage. The process uses `dataset/convert_cc_sbu.py` and `dataset/convert_laion.py` to convert annotation files to TSV, followed by `img2dataset`-style download scripts. Note that the README refers to `download_cc_sbu.sh` and `download_laion.sh`, which are not included in the supplied file list.
- **`README_2_STAGE.md`**: a second-stage dataset (`cc_sbu_align` with `filter_cap.json` and an `image/` folder) to be placed at a path set in `cc_sbu/align.yaml`.
- **`README_MINIGPTv2_FINETUNE.md`**: lists the sources for MiniGPT-v2 finetuning, including COCO 2014 captions and VQAv2, Visual Genome, TextCaps, RefCOCO/RefCOCO+/RefCOCOg, OK-VQA, AOK-VQA, OCR-VQA, GQA, filtered Flickr-30k, multi-task conversation, filtered unnatural instructions, and LLaVA data. Each section gives the expected folder layout and the config files to update.

## Development

### Repository layout

- `minigpt4/common/`: config handling, registry, distributed utilities, logging, optimizers and schedulers, and evaluation helpers. It also contains a vendored VQA evaluation toolkit under `vqa_tools/`.
- `minigpt4/models/`: model implementations (`minigpt4.py`, `minigpt_v2.py`, `minigpt_base.py`), the Q-Former, the EVA ViT, and a modified LLaMA model (`modeling_llama.py`).
- `minigpt4/datasets/`, `minigpt4/processors/`, `minigpt4/tasks/`, `minigpt4/runners/`: data pipeline and training orchestration.
- `minigpt4/conversation/`: conversation templates and the `Chat` helper.

Components are registered with decorators such as `@registry.register_model("minigpt4")`. New models, datasets, tasks, and schedulers can be added by following that pattern.

### Contributing

- Bug reports and feature requests use the templates in `.github/ISSUE_TEMPLATE/`.
- `CODE_OF_CONDUCT.md` is based on the Contributor Covenant, version 2.0. Reports go to the community leaders via the Discord link in that file.
- `SECURITY.md` contains a supported-versions table and a vulnerability-reporting section. The reporting text is still template placeholder language, so check it before relying on it.

## Testing

The supplied file tree does not include a unit test suite or CI configuration. The closest equivalents are the evaluation scripts in `eval_scripts/`, which compute RefCOCO-family grounding accuracy (IoU above 0.5) and VQA accuracy on OK-VQA, VizWiz, IconQA, GQA, VSR, and Hateful Memes. Results are written as JSON files to `save_path`.

## License

The code is released under the BSD 3-Clause License. `LICENSE.md` credits Deyao Zhu (2023).

`LICENSE_Lavis.md` contains a separate BSD 3-Clause License credited to Salesforce, Inc. (2022). Many source files carry SPDX headers that reference this file, which indicates that portions of the code derive from Salesforce's LAVIS project.

The bundled VQA tools under `minigpt4/common/vqa_tools/VQA/` include their own `license.txt`, which was not included in the supplied content. Review it separately. Note also that the datasets and pretrained weights referenced in this README have their own licenses and terms, which are not covered here.

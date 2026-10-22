# MiniGPT-4 / MiniGPT-v2

This repository contains the code, training scripts, evaluation tooling, and interactive demos for **MiniGPT-4** and **MiniGPT-v2**, a family of vision-language models that align a frozen visual encoder with a frozen large language model (LLM) through lightweight trainable projection layers. The result is a model capable of understanding images and generating coherent, human-like text about them — including image description, grounded captioning, visual question answering, referring expressions, and multi-task conversation.

The codebase is built on the LAVIS-style architecture (registry, configs, dataset builders, tasks, runners) originally released by Salesforce under a BSD 3-Clause license, with the MiniGPT-specific code (copyright 2023 Deyao Zhu) also released under BSD 3-Clause.

## Overview

The repository provides two main model families:

- **MiniGPT-4** (`minigpt4.models.MiniGPT4`, registered as `minigpt4`) — supports two model types, `pretrain_vicuna0` (Vicuna v0) and `pretrain_llama2` (LLaMA-2), with configuration files at `minigpt4/configs/models/minigpt4_vicuna0.yaml` and `minigpt4/configs/models/minigpt4_llama2.yaml`.
- **MiniGPT-v2** (`minigpt4.models.MiniGPTv2`, registered as `minigpt_v2`) — a multi-task model supporting grounded image captioning, caption-to-bbox, phrase-to-bbox, referring expression comprehension, and various VQA tasks. Configuration is at `minigpt4/configs/models/minigpt_v2.yaml`.

Both models share a common base class, `MiniGPTBase`, which combines:

- A frozen **EVA ViT-G** vision encoder (`eva_clip_g`) loaded from BLIP-2 released weights.
- For MiniGPT-4, an optional frozen **Q-Former** (`BertLMHeadModel` with cross-attention, initialized from BLIP-2 pretrained weights) with 32 learnable query tokens; when disabled, visual features are reshaped and projected directly.
- A frozen LLM (Vicuna v0, LLaMA-2, or the model configured for MiniGPT-v2), with optional **LoRA** fine-tuning via the `peft` library (`lora_r`, `lora_target_modules`, `lora_alpha`, `lora_dropout`).
- A trainable linear projection (`llama_proj`) that maps visual features into the LLM embedding space.

## Repository Structure

```
├── train.py                          # Unified training entry point
├── demo.py                           # Gradio demo for MiniGPT-4 (Vicuna0 / LLaMA2)
├── demo_v2.py                        # Gradio demo for MiniGPT-v2
├── train_configs/                    # YAML configs for stage 1/2 training and v2 finetuning
├── eval_configs/                     # YAML configs for evaluation and benchmark runs
├── eval_scripts/                     # eval_ref.py, eval_vqa.py, EVAL_README.md
├── dataset/                          # Dataset preparation docs and conversion scripts
├── examples/, examples_v2/, figs/    # Example images and figures
└── minigpt4/                         # Main Python package
    ├── common/                       # Registry, config, logging, dist utils, VQA tools
    ├── configs/                      # Model, dataset, and default configs
    ├── conversation/                 # Conversation templates and Chat controller
    ├── datasets/                     # Dataset builders and dataset classes
    ├── models/                       # MiniGPT4, MiniGPTv2, Q-Former, EVA ViT, LLaMA modeling
    ├── processors/                   # Image/text processors and augmentation
    ├── runners/                      # Base training runner
    └── tasks/                        # Task definitions (e.g., image-text pretraining)
```

## Installation

The project ships a conda environment file. Python 3.9 and PyTorch 2.0.0 are the pinned core versions.

```bash
conda env create -f environment.yml
conda activate minigptv
```

Key pinned dependencies include:

- `torch==2.0.0`, `torchvision`, `torchaudio`
- `transformers==4.30.0`, `tokenizers==0.13.2`
- `huggingface-hub==0.18.0`
- `peft==0.2.0`, `accelerate==0.20.3`, `bitsandbytes==0.37.0` (for 8-bit loading and LoRA)
- `omegaconf==2.3.0`, `pyyaml==6.0`
- `timm==0.6.13`
- `webdataset==0.2.48` (for LAION / CC-SBU webdataset shards)
- `gradio==3.47.1` (for the demos)
- `decord`, `opencv-python==4.7.0.72`, `scikit-image`, `sentence-transformers`, `wandb`, `visual-genome`

You will also need to download the underlying LLM weights yourself and point the `llama_model` (or equivalent) config entry to their local path.

## Running the Demos

Two Gradio demos are provided:

- **`demo.py`** — launches an interactive image-chat interface for MiniGPT-4. It accepts `--cfg-path` (one of `eval_configs/minigpt4_eval.yaml` for Vicuna0 or `eval_configs/minigpt4_llama2_eval.yaml` for LLaMA-2), an optional `--gpu-id` to select the GPU, and optional `--options` key-value overrides. The conversation template is selected automatically based on the `model_type` in the config (`pretrain_vicuna0` → Vicuna0 template, `pretrain_llama2` → LLaMA-2 template).
- **`demo_v2.py`** — launches the MiniGPT-v2 demo, configured via `eval_configs/minigptv2_eval.yaml`. Example input images are included in `examples_v2/` (e.g., product photos, office scenes, sofa, and other test images).

Before running a demo, edit the corresponding eval config to point `llama_model` and `ckpt` to your downloaded LLM weights and trained checkpoint. Example images for MiniGPT-4-style tasks (advertising, cooking, describing, fact-checking, fixing, fun, logos, operation, people, rhyming, stories, web, and more) are available under `examples/` and `figs/examples/`.

## Training MiniGPT-4

MiniGPT-4 training consists of two alignment stages. See `MiniGPT4_Train.md` for the authoritative instructions.

**Stage 1 — Pretraining.** The model is trained on image-text pairs from LAION and the CC3M/CC12M/SBU datasets (with BLIP-filtered synthetic captions) to align vision and language. In the reference experiments this used 4 A100 GPUs. First prepare the data (see [Dataset Preparation](#dataset-preparation) below), then edit the output paths in `train_configs/minigpt4_stage1_pretrain.yaml` (or `train_configs/minigpt4_llama2_stage1_pretrain.yaml`) and run:

```bash
torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```

**Stage 2 — Finetuning.** A small, high-quality, hand-curated image-text conversation dataset is used to further align the model so it talks about images coherently and in a user-friendly way. Download the second-stage dataset, set its path in `minigpt4/configs/datasets/cc_sbu/align.yaml`, specify the stage-1 checkpoint in `train_configs/minigpt4_stage2_finetune.yaml` (or `train_configs/minigpt4_llama2_stage2_finetune.yaml`), then run (reference experiments used 1 A100):

```bash
torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigpt4_stage2_finetune.yaml
```

## Finetuning MiniGPT-v2

For MiniGPT-v2, follow `MiniGPTv2_Train.md` and the dataset instructions in `dataset/README_MINIGPTv2_FINETUNE.md`. In `train_configs/minigptv2_finetune.yaml`, you must set:

- the LLM checkpoint path (`llama_model`),
- the pretrained MiniGPT-v2 checkpoint path (`ckpt`) — you may download one of the released pretrained checkpoints (after stage-2, after stage-3, or the online-developing demo checkpoint),
- the checkpoint save path.

Then run:

```bash
torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigptv2_finetune.yaml
```

## Dataset Preparation

### Stage 1 (MiniGPT-4 pretraining)

Detailed in `dataset/README_1_STAGE.md`. In summary:

1. Download the BLIP-filtered synthetic caption annotations (`ccs_synthetic_filtered_large.json` for CC3M+CC12M+SBU and `laion_synthetic_filtered_large.json` for LAION115M). This requires roughly 2.3 TB of storage for the full image sets.
2. Set `export MINIGPT4_DATASET=/your/large/dataset/path` and create `cc_sbu` and `laion` subfolders.
3. Copy `dataset/convert_cc_sbu.py` and `dataset/convert_laion.py` into the respective folders and run them to convert the annotation JSON files to the `img2dataset` format.
4. Download the images with `img2dataset` (the referenced `download_cc_sbu.sh` / `download_laion.sh` scripts), producing webdataset `.tar`/`.parquet` shards.
5. Update the shard globs in `minigpt4/configs/datasets/cc_sbu/defaults.yaml` and `minigpt4/configs/datasets/laion/defaults.yaml` to point to your dataset location.

### Stage 2 (MiniGPT-4 alignment)

Detailed in `dataset/README_2_STAGE.md`. Download the `cc_sbu_align` archive, which contains `filter_cap.json` and an `image/` folder, place it anywhere, and set the path in `minigpt4/configs/datasets/cc_sbu/align.yaml`.

### MiniGPT-v2 finetuning data

Detailed in `dataset/README_MINIGPTv2_FINETUNE.md`. It covers the full multi-task training mix, including: COCO 2014 captions and COCO VQA, Visual Genome, TextCaps, RefCOCO / RefCOCO+ / RefCOCOg (plus inverse referring tasks), OKVQA, AOK-VQA, OCR-VQA, GQA, filtered Flickr-30k (grounded caption, caption-to-bbox, phrase-to-bbox), multi-task conversation, filtered Unnatural Instructions (text-only), and the LLaVA-Instruct-150K splits (complex reasoning, detailed description, conversation). Each dataset has an associated config under `minigpt4/configs/datasets/` where `image_path` and `ann_path` must be set to your local locations.

## Evaluation

Evaluation instructions for MiniGPT-v2 benchmarks are in `eval_scripts/EVAL_README.md`.

**Data preparation** — download the evaluation datasets (OKVQA, GQA, Hateful Memes, IconQA, VizWiz, VSR, and RefCOCO/RefCOCO+/RefCOCOg) and arrange them under an evaluation dataset root following the directory layout shown in the eval README.

**Configuration** — in `eval_configs/minigptv2_benchmark_evaluation.yaml`, set:

- `llama_model`: path to the LLaMA weights
- `ckpt`: path to the pretrained MiniGPT-v2 checkpoint
- `eval_file_path`, `img_path`, and `save_path` for each evaluation dataset

**Environment** — set `PYTHONPATH` to include the repository root.

**Running** — two scripts are provided:

```bash
# Referring expression comprehension
torchrun --master-port ${port} --nproc_per_node 1 eval_scripts/eval_ref.py \
    --cfg-path eval_configs/minigptv2_benchmark_evaluation.yaml \
    --dataset refcoco,refcoco+,refcocog --resample

# Visual question answering
torchrun --master-port ${port} --nproc_per_node 1 eval_scripts/eval_vqa.py \
    --cfg-path eval_configs/minigptv2_benchmark_evaluation.yaml \
    --dataset okvqa,vizwiz,iconvqa,gqa,vsr,hm
```

VQA scoring utilities from the official VQA evaluation toolkit are bundled under `minigpt4/common/vqa_tools/`.

## Development Notes

- The project uses a LAVIS-style **registry system** (`minigpt4/common/registry.py`); models, datasets, processors, and tasks register themselves by name, and everything is wired through OmegaConf YAML configs (`minigpt4/configs/default.yaml` plus model/dataset configs).
- Training runs through `minigpt4/runners/runner_base.py` with distributed training via `torchrun`; `train.py` is the single entry point for all stages.
- Conversation behavior (system prompts, templates, stopping criteria such as `StoppingCriteriaSub`) lives in `minigpt4/conversation/conversation.py`.
- The model supports low-resource inference (8-bit LLM loading with `low_resource` and `device_8bit` settings) and optional gradient checkpointing in the vision encoder.
- Bug reports and feature requests can be filed using the templates in `.github/ISSUE_TEMPLATE/`.

## Security

A security policy is provided in `SECURITY.md`. Please review it before reporting potential vulnerabilities.

## License

This project is released under the **BSD 3-Clause License**:

- `LICENSE.md` — BSD 3-Clause, Copyright 2023 Deyao Zhu, covering the MiniGPT code.
- `LICENSE_Lavis.md` — BSD 3-Clause, Copyright 2022 Salesforce, Inc., covering the LAVIS-derived infrastructure code.

Both licenses permit redistribution and use with attribution, subject to the standard BSD 3-Clause conditions (retain the copyright notice, reproduce the disclaimer, and do not use contributor names for endorsement without permission). The bundled VQA evaluation toolkit carries its own license under `minigpt4/common/vqa_tools/VQA/license.txt`. Please also check the licenses of any LLM weights, vision encoder weights, and datasets you download, as they carry their own terms.

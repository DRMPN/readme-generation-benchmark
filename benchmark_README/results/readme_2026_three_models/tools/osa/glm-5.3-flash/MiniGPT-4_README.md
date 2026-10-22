# MiniGPT-4-vcwbiw3t

Train, fine-tune, evaluate, and demo MiniGPT-4 and MiniGPT-v2 multimodal vision-language models for image-conditioned chat and visual grounding.

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This repository implements MiniGPT-4 and MiniGPT-v2, multimodal vision-language models that connect image inputs to a large language model for image-conditioned conversation, including grounded responses visualized with bounding boxes. The code is written in Python and is intended for ML researchers and practitioners who want to reproduce, train, fine-tune, or extend these models; it is a research codebase that assumes manual dataset and pretrained-weight preparation and GPU hardware, rather than a ready-to-use product. The repository provides configuration-driven training and fine-tuning pipelines, benchmark evaluation workflows, dataset preparation and conversion utilities, and interactive web-based demos for chatting with the models over images. See Getting Started for runnable setup and usage steps.

---

## Core Features

- **Image-conditioned chat with large language models**: converse about uploaded images with MiniGPT-4 and MiniGPT-v2 through web-based chat interfaces, enabling hands-on exploration of multimodal behavior without writing code.
- **Visual grounding and localization**: the MiniGPT-v2 interface draws predicted bounding boxes directly onto images, making spatial outputs easy to inspect and verify.
- **End-to-end training and fine-tuning pipelines**: two-stage pretraining and fine-tuning workflows with multi-GPU distributed support and optional Weights & Biases logging let you reproduce results or adapt the models to your own datasets.
- **Benchmark evaluation**: built-in evaluation workflows for visual question answering and referring expression understanding provide quantitative performance measurements.
- **Swappable LLM backends**: select between Vicuna-0 and Llama-2 language models through configuration, so you can work with the checkpoints and hardware you have available.

---

## Installation

Install from the current local checkout using conda:

1. Open the repository root:

```sh
cd path/to/MiniGPT-4-vcwbiw3t
```

2. Create and activate the conda environment defined in `environment.yml` (the environment name is the value of the `name` field at the top of that file):

```bash
conda env create -f environment.yml
conda activate <env-name>
```

---

## Getting Started

**Prerequisites**

- NVIDIA GPU with CUDA: the demos load the model onto `cuda:0` by default; use `--gpu-id` to select another GPU.
- Conda: dependencies are defined in `environment.yml`.
- Pretrained weights: a trained MiniGPT-4 / MiniGPT-v2 checkpoint and the matching Vicuna-0 or Llama-2 LLM checkpoint. BLIP-2 Q-Former weights are fetched automatically from the URL configured in `minigpt4/models/minigpt4.py`.

**Steps**

1. Set up the conda environment as described in [Installation](#installation).

2. Edit the eval config you plan to run and set the paths to your weights: the LLM checkpoint (`llama_model`) and your trained MiniGPT-4 / MiniGPT-v2 checkpoint. For example, `eval_configs/minigptv2_eval.yaml` is the default config used by `demo_v2.py`.

3. Launch the Gradio demo:

```bash
# MiniGPT-v2 demo (uses eval_configs/minigptv2_eval.yaml by default)
python demo_v2.py

# MiniGPT-4 demo (--cfg-path is required)
python demo.py --cfg-path <path-to-eval-config>
```

4. Open the Gradio URL printed in the terminal, upload an image, and start chatting.

For training, follow the training guides listed in [Documentation](#documentation) and run `python train.py --cfg-path <train-config>` with a config from `train_configs/`.

---

## Architecture

- **Registry-driven package core.** The `minigpt4/` package is organized into `models`, `datasets` (builders plus dataset classes), `processors`, `runners`, `tasks`, `conversation`, and `common` utilities. Components self-register in a central registry (`minigpt4/common/registry.py`); entry points import these subpackages so that classes become available and are then assembled from YAML configs (`minigpt4/configs`, `train_configs`, `eval_configs`).
- **Model stack.** `MiniGPT4` (`minigpt4/models/minigpt4.py`, built on `MiniGPTBase`) combines an EVA ViT vision encoder (`eva_clip_g`), a BLIP-2-style Q-Former built on `bert-base-uncased` with learnable query tokens (freezable or disabled via `has_qformer`), and a linear projection (`llama_proj`) that maps image features into the LLM's hidden size. LLM backends — Vicuna-0 or Llama-2 — are selected through model configs in `minigpt4/configs/models/`. `MiniGPT-v2` (`minigpt_v2.py`, configured by `minigpt_v2.yaml`) is the second model variant, used with grounding-oriented interactions in `demo_v2.py`.
- **Conversation layer.** `minigpt4/conversation/conversation.py` provides the `Chat` controller plus prompt templates (`CONV_VISION_Vicuna0`, `CONV_VISION_LLama2`) that manage image encoding, multi-turn dialogue state, and stopping criteria during generation.
- **Data pipeline.** Dataset builders (`minigpt4/datasets/builders/`) instantiate task-specific dataset classes (`minigpt4/datasets/datasets/`) from per-dataset YAML configs, with image/text preprocessing handled by processors in `minigpt4/processors/`.
- **Training flow.** `train.py` builds a `Config`, initializes distributed training (NCCL), uses `tasks.setup_task` to construct datasets and the model, then hands them to a registry-selected runner (`runners/runner_base.py`) that runs training with LR schedulers from `common/optims.py`; optional Weights & Biases logging is supported.
- **Inference and evaluation entry points.** `demo.py` and `demo_v2.py` are Gradio apps that load the model from an eval config, wrap it in a `Chat` instance, and serve image-conditioned chat; `demo_v2.py` additionally parses bounding-box tokens from generated text and overlays them on the image. `eval_scripts/` runs VQA and referring-expression evaluation driven by configs in `eval_configs/`.

---

## Examples

Examples of how this should work and how it should be used are available in [`examples/`](./examples). Additional MiniGPT-v2 examples are available in [`examples_v2/`](./examples_v2).

---

## Documentation

- **Training guides:** `MiniGPT4_Train.md` and `MiniGPTv2_Train.md` describe how to train the models; runnable configs live under `train_configs/`.
- **Dataset preparation:** step-by-step guides under `dataset/` — `README_1_STAGE.md`, `README_2_STAGE.md`, and `README_MINIGPTv2_FINETUNE.md`.
- **Evaluation:** evaluation instructions in `eval_scripts/EVAL_README.md`, covering VQA and referring-expression evaluation driven by configs in `eval_configs/`.

---

## Contributing

Contributions are welcome. To propose changes or report problems:

- Open an issue describing the bug or the improvement you have in mind.
- Submit pull requests with a clear description of the change and, where relevant, the configs and dataset setup needed to reproduce it.

---

## License

License terms are documented in the license files included in the repository:

- [LICENSE.md](./LICENSE.md) — repository license file.
- [LICENSE_Lavis.md](./LICENSE_Lavis.md) — license covering the LAVIS-derived portions of the code, which carry a BSD-3-Clause header (for example, in `train.py`).

Consult these files directly to determine the terms that apply to your use.

---

## Citation

> **Note:** The citation below is placeholder boilerplate for a local checkout. Replace the author, title, and repository URL with the canonical repository information before publishing.

### APA format:

    README Benchmark (2026). MiniGPT-4-vcwbiw3t repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{MiniGPT-4-vcwbiw3t,

        author = {README Benchmark},

        title = {MiniGPT-4-vcwbiw3t repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
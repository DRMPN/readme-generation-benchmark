# MiniGPT-4 & MiniGPTv2

**Enhancing Vision-Language Advanced Understanding with Advanced Large Language Models**

This repository contains the implementation, training scripts, evaluation tooling, and demos for **MiniGPT-4** (based on Vicuna / LLaMA-2) and its successor **MiniGPTv2** (based on LLaMA-2), which connect a frozen visual encoder (EVA-ViT), a lightweight projection layer (Q-Former style), and a frozen LLM to enable advanced multimodal understanding and generation.

---

## 📋 Table of Contents

- [Introduction](#-introduction)
- [News](#-news)
- [Method Overview](#-method-overview)
- [Repository Structure](#-repository-structure)
- [Installation](#-installation)
- [Preparation](#-preparation)
  - [LLM Weights](#llm-weights)
  - [Vision Encoder Weights](#vision-encoder-weights)
  - [Pre-trained MiniGPT-4 / MiniGPTv2 Weights](#pre-trained-minigpt-4--minigptv2-weights)
- [Inference / Demo](#-inference--demo)
- [Training](#-training)
  - [MiniGPT-4 Two-Stage Training](#minigpt-4-two-stage-training)
  - [MiniGPT-4 One-Stage Training](#minigpt-4-one-stage-training)
  - [MiniGPTv2 Training](#minigptv2-training)
- [Evaluation](#-evaluation)
  - [VQA Evaluation](#vqa-evaluation)
  - [Referring Expression Evaluation](#referring-expression-evaluation)
- [Configuration Files](#-configuration-files)
- [Datasets](#-datasets)
- [Acknowledgments](#-acknowledgments)
- [License](#-license)
- [Citation](#-citation)

---

## 🔥 Introduction

MiniGPT-4 aligns a frozen visual encoder with a frozen LLM using just one projection layer. The alignment is achieved in two stages:

1. **Stage 1:** Train the projection layer on massive, loosely-paired image-text pairs (CC3M, LAION) using conventional captioning loss — the model learns basic visual-language alignment.
2. **Stage 2:** Fine-tune on a small, high-quality, carefully curated image-text dataset (created with a proposed dataset generation method using ChatGPT) to significantly improve generation quality, human-friendliness, and holistic capabilities.

**MiniGPTv2** extends this into a unified multi-task interface, trained on a mixture of tasks (captioning, VQA, grounding, OCR, referring expression comprehension, object detection-style localization, etc.), with task identifiers (`[vQA]`, `[CAPTION]`, `[identify]`, `[grounding]`, `[detection]`, `[OCR]`) embedded in the prompt.

Some of the demonstrated capabilities include:

- Detailed image description and visual question answering
- Writing poems, stories, and rhymes from images
- Solving problems shown in images (math, coding, etc.)
- Image-based advertisement and website generation
- Photo cropping / OCR-free text reading
- Locating and identifying objects in images (bounding boxes)

---

## 📰 News

- ✅ **MiniGPTv2** released — unified multi-task visual instruction tuning with LLaMA-2.
- ✅ **MiniGPT-4 (LLaMA-2 version)** released.
- ✅ **MiniGPT-4 (Vicuna v0 version)** released.
- ✅ Online demo and local `gradio` demos available.

---

## 🧠 Method Overview

```
                 ┌──────────────┐
  Image ────────►│  EVA ViT-g   │  (frozen)
                 └──────┬───────┘
                        │  linear projection
                 ┌──────▼───────┐
                 │   Q-Former   │  (query tokens / projection layer)
                 └──────┬───────┘
                        │
                 ┌──────▼───────┐
   Text ────────►│ LLaMA / LLaMA-2 / Vicuna │ (frozen)
                 └──────────────┘
                        │
                     Response
```

Only the **linear projection layer** (and optionally the Q-Former) is trained; the vision encoder and LLM remain frozen throughout.

---

## 📁 Repository Structure

```
MiniGPT-4/
├── minigpt4/                       # Core package
│   ├── common/                     # Registry, utils, logger, dist utils, optims
│   ├── config/                     # Configuration utilities
│   ├── datasets/
│   │   ├── dataloaders/            # (dataset mixins: coco, laion, vqa, refcoco, ocrvqa, ...)
│   │   └── data_utils/             # Base dataset/builder classes
│   ├── models/                     # minigpt4.py, minigpt_v2.py, Qformer.py,
│   │   └── modeling_llama/         # eva_vit.py, modeling_llama.py, base_model.py
│   ├── processors/                 # Image/text processors (blip_processors, randaugment)
│   ├── runners/                    # runner_base (training loop)
│   ├── tasks/                      # Task definitions (image_text_pretrain)
│   └── conversation.py             # Chat prompt templates
├── train.py                        # Training entry point
├── demo.py                         # MiniGPT-4 Gradio demo
├── demo_v2.py                      # MiniGPTv2 Gradio demo
├── eval_vqa.py                     # VQA / multi-task evaluation script
├── eval_ref.py                     # Referring expression evaluation script
├── dataloader_utils.py             # Dataloader helpers for evaluation
├── eval_configs/                   # Eval YAML configs (minigpt4_eval.yaml, minigptv2_eval.yaml, ...)
├── train_configs/                  # Training YAML configs (stage 1/2, finetune, v2)
├── examples/                       # Demo images (kitchen, documents, scenes, etc.)
├── environment.yml                 # Conda environment file
└── README.md
```

---

## ⚙️ Installation

```bash
# 1. Create a conda environment
conda env create -f environment.yml
conda activate minigpt4

# 2. Install additional required packages
pip install pillow==9.5.0
pip install grpcio grpcio-tools
pip install accelerate peft bitsandbytes
```

### Requirements

- Python ≥ 3.8
- PyTorch ≥ 1.12 (2.0 recommended)
- CUDA-capable GPU (a single **16GB+** GPU is sufficient for inference; training stage 1 can be done on 4×V100/RTX-3090/4090; stage 2 fits on a single GPU)

---

## 📦 Preparation

### LLM Weights

Prepare the LLM checkpoints and edit `minigpt4/configs/models/minigpt4.yaml` (or `minigpt_v2.yaml`) to point `llama_model` to their paths.

| Model | Source |
|---|---|
| **Vicuna v0 (13B)** | Released by LMSYS — follow instructions to convert the delta weights: [Vicuna](https://github.com/lm-sys/FastChat) |
| **LLaMA-2 (7B / 13B)** | Download from [Meta LLaMA-2](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) or use HuggingFace `meta-llama/Llama-2-7b-chat-hf` |

> ⚠️ For Vicuna v0, a conversion step is required:
> ```bash
> python -m fastchat.model.apply_delta --base /path/to/llama-13b-hf --target /path/to/vicuna-13b-v0 --delta lmsys/vicuna-13b-delta-v0
> ```

### Vision Encoder Weights

Download the pretrained **EVA-ViT-g** checkpoint and specify its path in the model config (`model_config` / `vit_model` field):

- `eva_vit_g.pth` ([EVA-CLIP, 1B parameters](https://github.com/baaivision/EVA))

### Pre-trained MiniGPT-4 / MiniGPTv2 Weights

Download the trained projection / alignment weights and edit the `ckpt` path in the corresponding eval config (`eval_configs/minigpt4_eval.yaml`, `minigpt4_llama2_eval.yaml`, `minigptv2_eval.yaml`):

- **MiniGPT-4 (Vicuna v0, 13B)** — stage-2 aligned weights
- **MiniGPT-4 (LLaMA-2, 7B)** — stage-2 aligned weights
- **MiniGPTv2 (LLaMA-2, 7B)** — multi-task finetuned weights

---

## 🎮 Inference / Demo

### MiniGPT-4 demo

```bash
python demo.py --cfg-path eval_configs/minigpt4_eval.yaml --gpu-id 0
```

### MiniGPT-4 (LLaMA-2) demo

```bash
python demo.py --cfg-path eval_configs/minigpt4_llama2_eval.yaml --gpu-id 0
```

### MiniGPTv2 demo (multi-task)

```bash
python demo_v2.py --cfg-path eval_configs/minigptv2_eval.yaml --gpu-id 0
```

For the v2 demo, prepend the task identifier to your prompt, e.g.:

- `[vQA]` — visual question answering
- `[CAPTION]` — image captioning
- `[identify]` — identify what/where an object is
- `[grounding]` — produce bounding box coordinates for a described object
- `[detection]` — detect all objects and output bounding boxes
- `[OCR]` — read text in the image

After launching, upload an image in the Gradio interface and start chatting. Try prompts like:

- "What is in this image?"
- "Explain what's funny about this image."
- `[grounding] where are the people?`

---

## 🏋️ Training

All training is launched via `train.py` with a YAML config:

```bash
python train.py --cfg-path train_configs/<config>.yaml
```

Useful options:

```bash
--cfg-path train_configs/minigpt4_stage2_finetune.yaml   # config file
--options run.num_nodes=1 run.max_num_nodes=1            # override any YAML field
```

### MiniGPT-4 Two-Stage Training

**Stage 1 (pretraining on image-text pairs):**

```bash
python train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```

- Data: **CC3M** (approx. 595k images) and/or **LAION** subsets.
- Goal: align the projection layer with broad visual concepts using the conventional captioning objective.
- Note: using more data (e.g., LAION-400M subsets) improves visual knowledge but produces harsher, less human-like language; stage 2 fixes that.

**Stage 2 (finetuning on curated data):**

```bash
python train.py --cfg-path train_configs/minigpt4_stage2_finetune.yaml
```

- Data: a small (~3.5k pairs) carefully curated dataset of detailed image descriptions generated by ChatGPT, plus short-caption pairs from CC3M/LAION.
- `max_epoch` is typically small (e.g., 5) with a small learning rate; warm-start from the stage-1 checkpoint.

For **LLaMA-2-based** models use the analogous configs:

```bash
python train.py --cfg-path train_configs/minigpt4_llama2_stage1_pretrain.yaml
python train.py --cfg-path train_configs/minigpt4_llama2_stage2_finetune.yaml
```

> 📄 See `MiniGPT4_Train.md` and `README_1_STAGE.md` / `README_2_STAGE.md` for detailed data preparation steps (`convert_cc_sbu.py`, `convert_laion.py` handle dataset conversion).

### MiniGPT-4 One-Stage Training

Alternatively, combine a large caption dataset with the curated dataset in a single stage:

```bash
python train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```

with both datasets mixed in the config — this yields comparable performance in one pass (see `README_1_STAGE.md`).

### MiniGPTv2 Training

MiniGPTv2 is finetuned with multiple tasks simultaneously:

```bash
python train.py --cfg-path train_configs/minigptv2_finetune.yaml
```

Datasets used (prepared in `minigpt4/datasets/`):

- **Captioning:** COCO Caption, TextCaps (`caption.yaml`)
- **VQA:** OK-VQA, A-OKVQA, GQA, OCR-VQA, Visual7W-style COCO VQA (`reason.yaml`, `detail.yaml`, `conversation.yaml`, `ocrvqa.yaml`, `balanced_val.yaml`)
- **Referring expression:** RefCOCO, RefCOCO+, RefCOCOg and their inverses (`refcoco.yaml`, `refcocog.yaml`, `refcocop.yaml`, `invrefcoco*.yaml`, `ref.yaml`, `default.yaml`, `object_to_phrase.yaml`, `caption_to_phrase.yaml`)
- **Language-only:** unnatural instructions (`unnatural_instruction.yaml`)

---

## 📊 Evaluation

### VQA Evaluation

Evaluate on VQA benchmarks (OK-VQA, A-OKVQA, GQA, OCR-VQA, COCO captioning, etc.):

```bash
python eval_vqa.py --cfg-path eval_configs/minigptv2_eval.yaml \
    --data_path /path/to/dataset \
    --task <task_name>   # e.g. caption, ok_vqa, aok_vqa, gqa, ocr_vqa
```

Edit `eval_configs/minigptv2_eval.yaml` / `minigpt4_eval.yaml` to set the checkpoint, LLM path, and dataset options. The script uses `dataloader_utils.py` to build the dataloader for each benchmark and computes accuracy / CIDEr depending on the task.

### Referring Expression Evaluation

Evaluate grounding / identifying / detection-style tasks on RefCOCO / RefCOCO+ / RefCOCOg:

```bash
python eval_ref.py --cfg-path eval_configs/minigptv2_eval.yaml \
    --data_path /path/to/refcoco_data \
    --task grounding   # or identify
```

Predicted bounding boxes are compared against ground-truth annotations using IoU metrics.

### Traditional VQA utilities

The repository also bundles the standard VQA toolkit (`vqaEval.py`, `vqa.py`, question-type lists `mscoco_question_types.txt`, `abstract_v002_question_types.txt`) for official VQA evaluation flows.

---

## 🛠️ Configuration Files

Key configs (YAML) and their purpose:

| Config | Purpose |
|---|---|
| `train_configs/minigpt4_stage1_pretrain.yaml` | Stage-1 image-text alignment training |
| `train_configs/minigpt4_stage2_finetune.yaml` | Stage-2 instruction finetuning |
| `train_configs/minigpt4_llama2_stage1_pretrain.yaml` | Stage 1 for LLaMA-2 variant |
| `train_configs/minigpt4_llama2_stage2_finetune.yaml` | Stage 2 for LLaMA-2 variant |
| `train_configs/minigptv2_finetune.yaml` | MiniGPTv2 multi-task finetuning |
| `eval_configs/minigpt4_eval.yaml` | Eval config for Vicuna-based MiniGPT-4 |
| `eval_configs/minigpt4_llama2_eval.yaml` | Eval config for LLaMA-2-based MiniGPT-4 |
| `eval_configs/minigptv2_eval.yaml` | Eval config for MiniGPTv2 |
| `minigpt4/configs/models/minigpt4.yaml` / `minigpt_v2.yaml` | Model architecture (ViT path, LLM path, Q-Former settings) |
| `minigpt4/configs/default.yaml` | Default runner/training hyperparameters |

All fields can be overridden at runtime via `--options key=value ...`.

---

## 🗂️ Datasets

The `minigpt4/datasets/` directory provides dataset loaders/mixins for:

- **COCO / COCO VQA / COCO Caption**
- **LAION** (conceptual captions via `laion_dataset.py`, built with `image_text_pair_builder.py`)
- **CC-SBU / CC3M** (`cc_sbu_dataset.py`)
- **OCR-VQA** (`ocrvqa_dataset.py`)
- **A-OKVQA / OK-VQA** (`aok_vqa_datasets.py`, `vqa_datasets.py`)
- **GQA** (`gqa_datasets.py`)
- **Visual Genome** (`vg_dataset.py`)
- **RefCOCO family** (`flickr.py`, `refcoco`-style configs, `multitask_conversation.py`)
- **LLaVA-style instruction data** (`llava_dataset.py`)
- **TextCaps** (`text_caps.py`)
- **Unnatural Instructions** (language-only supervision, `unnatural_instruction.py`)

Dataset builders follow the LAVIS-style registry pattern (`base_dataset_builder.py`, `base_dataset.py`, `data_utils.py`).

---

## 🙏 Acknowledgments

This project builds upon outstanding open-source work:

- [BLIP-2](https://github.com/salesforce/LAVIS) — Q-Former architecture and LAVIS codebase (`LICENSE_Lavis.md`)
- [EVA / EVA-CLIP](https://github.com/baaivision/EVA) — vision encoder
- [LLaMA / LLaMA-2](https://github.com/facebookresearch/llama) and [FastChat / Vicuna](https://github.com/lm-sys/FastChat)
- [LLaVA](https://github.com/haotian-liu/LLaVA) — visual instruction data inspiration
- [ImageBind](https://github.com/facebookresearch/ImageBind) — design inspiration
- [OpenFlamingo](https://github.com/LAION-AI/Open-Language-Modeling) — inspiration
- The official [VQA evaluation toolkit](https://visualqa.org/)

---

## 📄 License

This repository is released under the BSD 3-Clause License (see `LICENSE.md`), with components under their original licenses (`LICENSE_Lavis.md`, `license.txt` in the VQA evaluation tools). Please check each third-party component's license for redistribution terms.

---

## ✒️ Citation

If you find this work useful in your research, please consider citing:

```bibtex
@misc{zhu2023minigpt4,
      title={MiniGPT-4: Enhancing Vision-Language Understanding with Advanced Large Language Models},
      author={Deyao Zhu and Jun Chen and Xiaoqian Shen and Xiang Li and Mohamed Elhoseiny},
      year={2023},
      eprint={2304.10592},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

```bibtex
@article{chen2023minigptv2,
      title={MiniGPT-v2: large language model as a unified interface for vision-language multi-task learning},
      author={Chen, Jun and Zhu, Deyao and Shen, Xiaoqian and Li, Xiang and Liu, Zechun and Zhang, Pengchuan and Elhoseiny, Mohamed},
      journal={arXiv preprint arXiv:2310.09478},
      year={2023}
}
```

---

## ⚖️ Code of Conduct

Please refer to `CODE_OF_CONDUCT.md` and `SECURITY.md` for community guidelines and security disclosure procedures.

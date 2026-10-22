# MiniGPT-4 (MiniGPT-v2 Included)

MiniGPT-4 is a vision-language model that aligns a frozen visual encoder with a frozen large language model (LLM) so the LLM can understand images. This repository contains the code for **MiniGPT-4**, which uses Vicuna or LLaMA-2 as the LLM, and **MiniGPT-v2**, a follow-up model for multi-task vision-language understanding. It includes demos, training pipelines, evaluation scripts, and dataset tooling.

> **Note:** This README was written from the repository's file listing. Some directory paths are inferred from the file names, so check the actual tree before relying on a specific path.

---

## Table of Contents

- [Features](#features)
- [Repository Structure](#repository-structure)
- [Model Overview](#model-overview)
- [Installation](#installation)
- [Model Weights and Preparation](#model-weights-and-preparation)
- [Quick Start: Running the Demos](#quick-start-running-the-demos)
- [Configuration Files](#configuration-files)
- [Training](#training)
- [Datasets](#datasets)
- [Evaluation](#evaluation)
- [Inference API Usage](#inference-api-usage)
- [Core Components](#core-components)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Citation](#citation)

---

## Features

- **Multimodal chat:** Upload an image and chat about it with an LLM-based assistant.
- **Two model families:**
  - **MiniGPT-4** with Vicuna (v0) or LLaMA-2 Chat as the backbone.
  - **MiniGPT-v2**, a unified interface for many vision-language tasks, including grounding and referring expression tasks.
- **Two-stage training:** Stage 1 pretraining on image-text pairs, then Stage 2 instruction finetuning.
- **Benchmark evaluation:** Scripts for VQA and referring expression comprehension.
- **Dataset support:** Many public datasets (COCO, Visual Genome, GQA, OCR-VQA, RefCOCO family, LAION, Conceptual Captions, SBU, and more), plus instruction-style data.
- **Modular design:** Registry-based models, datasets, tasks, and processors, built on the LAVIS framework.

---

## Repository Structure

The repository is organized into the following main areas:

```
MiniGPT-4/
├── demo.py                       # Gradio demo for MiniGPT-4
├── demo_v2.py                    # Gradio demo for MiniGPT-v2
├── train.py                      # Training entry point
├── eval_vqa.py                   # VQA benchmark evaluation
├── eval_ref.py                   # Referring expression evaluation
├── environment.yml               # Conda environment specification
├── eval_configs/                 # Evaluation and inference configs (YAML)
│   ├── minigpt4_eval.yaml
│   ├── minigpt4_llama2_eval.yaml
│   ├── minigptv2_eval.yaml
│   └── minigptv2_benchmark_evaluation.yaml
├── train_configs/                # Training configs (YAML)
│   ├── minigpt4_stage1_pretrain.yaml
│   ├── minigpt4_stage2_finetune.yaml
│   ├── minigpt4_llama2_stage1_pretrain.yaml
│   ├── minigpt4_llama2_stage2_finetune.yaml
│   └── minigptv2_finetune.yaml
├── minigpt4/                     # Main Python package
│   ├── models/                   # Model definitions
│   │   ├── minigpt_base.py       # Shared base model logic
│   │   ├── minigpt4.py           # MiniGPT-4 model
│   │   ├── minigpt_v2.py         # MiniGPT-v2 model
│   │   ├── base_model.py         # Base class for models
│   │   ├── blip2.py / Qformer.py # Q-Former (BLIP-2 style) module
│   │   ├── eva_vit.py            # EVA-CLIP vision transformer
│   │   └── modeling_llama.py     # LLaMA model modifications
│   ├── configs/                  # Model, dataset, and runner configs
│   ├── common/                   # Shared utilities (config, registry, logger, etc.)
│   ├── conversation/             # Conversation templates and chat logic
│   ├── datasets/                 # Dataset classes and builders
│   ├── processors/               # Image and text preprocessing
│   ├── runners/                  # Training runners
│   ├── tasks/                    # Task definitions (captioning, VQA, etc.)
│   └── ...
├── figures/ and assets/          # Images used in the README and demos
├── docs/ and READMEs            # Training and evaluation documentation
└── LICENSE.md / LICENSE_Lavis.md
```

### Key Root-Level Files

| File | Purpose |
|------|---------|
| `demo.py` | Launches the MiniGPT-4 chat interface |
| `demo_v2.py` | Launches the MiniGPT-v2 interface |
| `train.py` | Launches training from a config file |
| `eval_vqa.py` | Runs VQA evaluation on benchmark datasets |
| `eval_ref.py` | Runs referring expression evaluation |
| `environment.yml` | Conda environment with pinned dependencies |
| `MiniGPT4_Train.md` | Training guide for MiniGPT-4 |
| `MiniGPTv2_Train.md` | Training guide for MiniGPT-v2 |
| `EVAL_README.md` | Evaluation guide |
| `CODE_OF_CONDUCT.md` | Community guidelines |
| `SECURITY.md` | Security policy |

### Dataset Modules

The dataset package contains one module per data source, including:

- **Captioning:** `caption_datasets.py`, `coco_caption.py`, `text_caps.py`, `flickr.py`, `cc_sbu_dataset.py`, `laion_dataset.py`
- **VQA:** `vqa_datasets.py`, `coco_vqa_datasets.py`, `aok_vqa_datasets.py`, `gqa_datasets.py`, `ocrvqa_dataset.py`
- **Grounding and referring:** `vg_dataset.py` and related REC/REG datasets
- **Instruction and conversation:** `llava_dataset.py`, `unnatural_instruction.py`, `multitask_conversation.py`
- **Infrastructure:** `base_dataset.py`, `base_dataset_builder.py`, `image_text_pair_builder.py`, `dataloader_utils.py`

### Evaluation Utilities

The VQA evaluation code is adapted from the official VQA toolkit and includes:

- `vqa.py` and `vqaEval.py`: Core VQA scoring
- `vqaDemo.py` and `vqaEvalDemo.py`: Example usage
- Question-type files such as `mscoco_question_types.txt` and `abstract_v002_question_types.txt`

---

## Model Overview

### MiniGPT-4

MiniGPT-4 consists of:

1. **Vision encoder:** EVA-CLIP ViT (`eva_vit.py`), frozen.
2. **Q-Former:** A query transformer from BLIP-2 (`Qformer.py`) that compresses visual features into a fixed number of query tokens.
3. **Linear projection:** Maps Q-Former outputs into the LLM embedding space. This is the main trainable component in Stage 1.
4. **LLM:** Vicuna (v0) or LLaMA-2 Chat, frozen during pretraining.

Training happens in two stages:

- **Stage 1 (alignment pretraining):** Train the projection layer on large image-text pairs (e.g., CC3M, LAION subsets) to align visual and text representations.
- **Stage 2 (instruction finetuning):** Finetune on a smaller, high-quality dataset of detailed image descriptions and conversations to improve generation quality.

### MiniGPT-v2

MiniGPT-v2 extends this approach to many vision-language tasks. It uses task-specific identifier tokens in the prompt (for example, `[vqa]`, `[grounding]`, `[caption]`, `[refer]`) so one model can handle captioning, VQA, referring expression comprehension, and grounding.

---

## Installation

### Prerequisites

- Linux (recommended) with an NVIDIA GPU
- CUDA-compatible PyTorch installation
- Conda (recommended)
- Enough GPU memory for your target model:
  - Inference with 4-bit or 8-bit quantization can run on smaller GPUs.
  - Full-precision 7B/13B inference and training need substantially more VRAM. Multi-GPU setups are recommended for training.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Vision-CAIR/MiniGPT-4.git
cd MiniGPT-4
```

### Step 2: Create the Environment

Using the provided environment file:

```bash
conda env create -f environment.yml
conda activate minigpt4
```

Or create the environment manually:

```bash
conda create -n minigpt4 python=3.9 -y
conda activate minigpt4
pip install -r requirements.txt   # if provided in your copy of the repo
```

### Step 3: Verify the Installation

```bash
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

---

## Model Weights and Preparation

The code does not include model weights. You need to download:

1. **LLM weights**
   - **Vicuna (v0, 7B or 13B):** Convert the Vicuna delta weights to a full model following the official Vicuna instructions. Then update the path in the model config.
   - **LLaMA-2 Chat (7B):** Obtain access through Meta and convert to a Hugging Face-compatible format if needed.

2. **MiniGPT-4 checkpoint**
   - Pretrained MiniGPT-4 weights (the projection layer, plus the Q-Former if applicable) released by the authors.

3. **MiniGPT-v2 checkpoint**
   - Pretrained MiniGPT-v2 weights released by the authors.

4. **Vision encoder and Q-Former**
   - EVA-CLIP and BLIP-2 Q-Former weights, downloaded automatically or manually depending on the config.

### Setting Checkpoint Paths

Edit the relevant model config (in `minigpt4/configs/models/`) and set the paths:

```yaml
model:
  arch: mini_gpt4
  llama_model: "/path/to/vicuna-7b"        # LLM path
  ckpt: "/path/to/pretrained_minigpt4.pth" # Pretrained checkpoint
```

For LLaMA-2 variants, use `minigpt4_llama2.yaml`. For Vicuna v0, use `minigpt4_vicuna0.yaml`. For MiniGPT-v2, use `minigpt_v2.yaml`.

---

## Quick Start: Running the Demos

### MiniGPT-4 Demo

```bash
python demo.py --cfg-path eval_configs/minigpt4_eval.yaml --gpu-id 0
```

For the LLaMA-2 variant:

```bash
python demo.py --cfg-path eval_configs/minigpt4_llama2_eval.yaml --gpu-id 0
```

### MiniGPT-v2 Demo

```bash
python demo_v2.py --cfg-path eval_configs/minigptv2_eval.yaml --gpu-id 0
```

Both demos launch a Gradio web interface. Open the printed local URL in your browser, upload an image, and start chatting.

### Command-Line Arguments

| Argument | Description |
|----------|-------------|
| `--cfg-path` | Path to the evaluation/inference YAML config |
| `--gpu-id` | GPU index to use (default: 0) |
| `--options` | Optional config overrides in `key=value` format |

---

## Configuration Files

The project uses YAML configs organized in three layers.

### 1. Evaluation and Inference Configs (`eval_configs/`)

| Config | Purpose |
|--------|---------|
| `minigpt4_eval.yaml` | MiniGPT-4 (Vicuna) demo and inference |
| `minigpt4_llama2_eval.yaml` | MiniGPT-4 (LLaMA-2) demo and inference |
| `minigptv2_eval.yaml` | MiniGPT-v2 demo and inference |
| `minigptv2_benchmark_evaluation.yaml` | Benchmark evaluation settings for MiniGPT-v2 |

### 2. Training Configs (`train_configs/`)

| Config | Purpose |
|--------|---------|
| `minigpt4_stage1_pretrain.yaml` | Stage 1 pretraining for Vicuna-based MiniGPT-4 |
| `minigpt4_stage2_finetune.yaml` | Stage 2 finetuning for Vicuna-based MiniGPT-4 |
| `minigpt4_llama2_stage1_pretrain.yaml` | Stage 1 pretraining for LLaMA-2 MiniGPT-4 |
| `minigpt4_llama2_stage2_finetune.yaml` | Stage 2 finetuning for LLaMA-2 MiniGPT-4 |
| `minigptv2_finetune.yaml` | MiniGPT-v2 multi-task finetuning |

### 3. Model and Dataset Configs (`minigpt4/configs/`)

- **Model configs:** `minigpt4_llama2.yaml`, `minigpt4_vicuna0.yaml`, `minigpt_v2.yaml`
- **Dataset configs:** Per-dataset YAMLs such as `align.yaml`, `unnatural_instruction.yaml`, `ocrvqa.yaml`, `caption.yaml`, `ref.yaml`, `refcoco.yaml`, `refcocog.yaml`, `refcocop.yaml`, `invrefcoco.yaml`, `invrefcocog.yaml`, `invrefcocop.yaml`, `object_to_phrase.yaml`, `caption_to_phrase.yaml`, `balanced_val.yaml`, `conversation.yaml`, `detail.yaml`, `reason.yaml`, and `defaults*.yaml`.
- **Runner and task configs:** Set the learning rate schedule, batch size, number of epochs, and output directory.

### Overriding Config Values

Any value can be overridden on the command line:

```bash
python train.py --cfg-path train_configs/minigpt4_stage2_finetune.yaml \
    --options run.batch_size_train=4 run.init_lr=1e-5
```

---

## Training

Detailed instructions are in `MiniGPT4_Train.md`, `MiniGPTv2_Train.md`, `README_1_STAGE.md`, `README_2_STAGE.md`, and `README_MINIGPTv2_FINETUNE.md`.

### Overview

Training follows the two-stage recipe for MiniGPT-4:

1. **Stage 1: Pretraining**
   - Uses large-scale image-text pairs.
   - Only the projection layer is trained; the vision encoder and LLM are frozen.

   ```bash
   torchrun --nproc-per-node 4 train.py \
       --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
   ```

2. **Stage 2: Instruction Finetuning**
   - Uses a smaller, curated dataset of detailed descriptions.
   - Set the Stage 1 checkpoint as the starting point in the config.

   ```bash
   torchrun --nproc-per-node 4 train.py \
       --cfg-path train_configs/minigpt4_stage2_finetune.yaml
   ```

For LLaMA-2, use the `minigpt4_llama2_*` configs.

### MiniGPT-v2 Training

MiniGPT-v2 uses a single multi-task finetuning stage:

```bash
torchrun --nproc-per-node 4 train.py \
    --cfg-path train_configs/minigptv2_finetune.yaml
```

### Data Conversion Scripts

Two scripts convert raw data into the format the loaders expect:

- `convert_laion.py`: Converts LAION data.
- `convert_cc_sbu.py`: Converts Conceptual Captions and SBU data.

Example:

```bash
python convert_cc_sbu.py --help
```

### Checkpoints and Logs

Training outputs (checkpoints, logs) are written to the `output_dir` specified in the runner config. The logger is defined in `minigpt4/common/logger.py`.

---

## Datasets

The project supports the following data sources. Download and place them according to the paths in the dataset configs.

### Pretraining and Captioning

- **LAION** and **Conceptual Captions (CC3M/CC12M)**: Large image-text pairs.
- **SBU Captions**
- **COCO Captions**
- **Flickr30k**
- **TextCaps**

### Visual Question Answering

- **VQAv2**
- **OK-VQA**
- **A-OKVQA**
- **GQA**
- **OCR-VQA**

### Grounding and Referring Expressions

- **RefCOCO, RefCOCO+, RefCOCOg**
- **Visual Genome (VG)**
- Inverse referring variants (`invrefcoco*`)

### Instruction and Conversation

- **LLaVA instruction data**
- **Unnatural Instructions**
- Multi-task conversation datasets (`multitask_conversation.py`)

### Dataset Structure

Each dataset class inherits from `base_dataset.py` and is built through `base_dataset_builder.py` or `image_text_pair_builder.py`. A dataset is typically defined by:

- An annotation file (JSON or similar)
- An image root directory
- Preprocessing, handled by the processors in `minigpt4/processors/`

---

## Evaluation

Detailed instructions are in `EVAL_README.md`.

### VQA Evaluation

```bash
python eval_vqa.py --cfg-path eval_configs/minigptv2_benchmark_evaluation.yaml --gpu-id 0
```

This script runs the model on the configured VQA benchmarks and computes accuracy with the official VQA scoring logic in `minigpt4/common/vqa_tools/` (`vqa.py`, `vqa_eval.py`).

### Referring Expression Evaluation

```bash
python eval_ref.py --cfg-path eval_configs/minigptv2_benchmark_evaluation.yaml --gpu-id 0
```

This computes accuracy on RefCOCO-family benchmarks by checking whether the predicted bounding box matches the ground truth with an IoU threshold (commonly 0.5).

### Evaluation Metrics

- **VQA:** Standard VQA accuracy.
- **Referring expression comprehension:** Accuracy at IoU ≥ 0.5.
- **Captioning:** BLEU, METEOR, ROUGE, CIDEr, and SPICE, where configured.

---

## Inference API Usage

You can use the model directly from Python. The example below shows the general pattern; check `demo.py` and `demo_v2.py` for the exact method names in your version.

```python
import torch
from minigpt4.common.config import Config
from minigpt4.common.registry import registry
from minigpt4.conversation.conversation import CONV_VISION_Vicuna0, Chat

# Load the config
cfg = Config.from_args(argparse.Namespace(
    cfg_path="eval_configs/minigpt4_eval.yaml",
    options=None,
))

# Build the model and vision processor
model_cls = registry.get_model_class(cfg.model_cfg.arch)
model = model_cls.from_config(cfg.model_cfg).to("cuda:0")
vis_processor_cfg = cfg.datasets_cfg.cc_sbu_align.vis_processor.train
vis_processor = registry.get_processor_class(vis_processor_cfg.name).from_config(vis_processor_cfg)

# Chat interface
chat = Chat(model, vis_processor, device="cuda:0")
chat_state = CONV_VISION_Vicuna0.copy()
img_list = []

chat.upload_img("example.jpg", chat_state, img_list)
chat.ask("Describe this image in detail.", chat_state)
answer = chat.answer(chat_state, img_list, num_beams=1, temperature=1.0)[0]
print(answer)
```

Notes:

- `Config.from_args` may expect a parsed argument namespace. Adapt the snippet to match how `demo.py` builds its arguments.
- The conversation templates (`CONV_VISION_*`) are defined in `minigpt4/conversation/conversation.py`.

---

## Core Components

### `minigpt4/models/`

- **`base_model.py`:** Base class with shared utilities such as parameter freezing and checkpoint loading.
- **`minigpt_base.py`:** Shared logic for building the vision encoder, Q-Former, projection layer, and LLM.
- **`minigpt4.py`:** MiniGPT-4 model class.
- **`minigpt_v2.py`:** MiniGPT-v2 model class with task identifier handling.
- **`eva_vit.py`:** EVA-CLIP vision transformer.
- **`Qformer.py`:** Q-Former query transformer.
- **`modeling_llama.py`:** LLaMA model code used for LLaMA-2 variants.

### `minigpt4/common/`

- **`config.py`:** Loads and merges YAML configs with command-line overrides.
- **`registry.py`:** Central registry for models, datasets, tasks, runners, and processors. Components are looked up by name.
- **`dist_utils.py`:** Distributed training helpers.
- **`logger.py`:** Logging setup.
- **`optims.py`:** Optimizers and learning rate schedulers.
- **`utils.py`, `eval_utils.py`:** General and evaluation helpers.
- **`gradcam.py`:** Grad-CAM visualization utilities.
- **`vqa.py`, `vqa_eval.py`:** VQA scoring.

### `minigpt4/tasks/`

- **`base_task.py`:** Base task class.
- **`image_text_pretrain.py`:** Task for image-text pretraining.

### `minigpt4/processors/`

- **`blip_processors.py`:** Image and text processors.
- **`randaugment.py`:** RandAugment image augmentation.
- **`base_processor.py`:** Base processor class.

### `minigpt4/runners/`

- **`runner_base.py`:** Training loop, checkpointing, and evaluation orchestration.

### `minigpt4/conversation/`

- **`conversation.py`:** Chat state, prompt templates, and the `Chat` class for interactive use.

---

## Troubleshooting

| Problem | Possible Cause and Fix |
|---------|------------------------|
| CUDA out of memory | Reduce `batch_size`, enable 8-bit or 4-bit loading, or use a smaller LLM. |
| Model path not found | Check `llama_model` and `ckpt` in the model config. Use absolute paths. |
| `ModuleNotFoundError` | Reinstall with `environment.yml`, and confirm the environment is active. |
| Gradio demo not accessible | Check the port and firewall, or set `share=True` if the demo supports it. |
| Slow data loading | Increase `num_workers` in the dataloader config. |
| Distributed training hangs | Verify `torchrun` arguments and that all GPUs are visible (`CUDA_VISIBLE_DEVICES`). |
| Mismatched checkpoint keys | Make sure the checkpoint matches the model architecture (Vicuna vs. LLaMA-2, MiniGPT-4 vs. MiniGPT-v2). |

---

## Contributing

Contributions are welcome. Please:

1. Fork the repository and create a feature branch.
2. Follow the existing code style and add docstrings for new components.
3. Test changes with the demos or a small training run before opening a pull request.
4. Read `CODE_OF_CONDUCT.md` before participating.

To report security issues, see `SECURITY.md` and follow the process described there rather than opening a public issue.

---

## License

- The MiniGPT-4 code is released under the **BSD 3-Clause License**. See `LICENSE.md`.
- Portions of the code are derived from **LAVIS**, which is also BSD 3-Clause. See `LICENSE_Lavis.md`.
- The LLM weights (Vicuna, LLaMA-2) and datasets have their own licenses and terms of use. You are responsible for complying with them.

---

## Acknowledgements

This project builds on several open-source works:

- [LAVIS](https://github.com/salesforce/LAVIS), the framework for the registry, datasets, and training pipeline.
- [BLIP-2](https://github.com/salesforce/LAVIS/tree/main/projects/blip2) and its Q-Former.
- [EVA-CLIP](https://github.com/baaivision/EVA) for the vision encoder.
- [Vicuna](https://github.com/lm-sys/FastChat) and [LLaMA-2](https://ai.meta.com/llama/) for the language models.
- The official VQA evaluation toolkit for the scoring code.

---

## Citation

If you use this work, please cite the MiniGPT-4 and MiniGPT-v2 papers:

```bibtex
@article{zhu2023minigpt4,
  title={MiniGPT-4: Enhancing Vision-Language Understanding with Advanced Large Language Models},
  author={Zhu, Deyao and Chen, Jun and Shen, Xiaoqian and Li, Xiang and Elhoseiny, Mohamed},
  journal={arXiv preprint arXiv:2304.10592},
  year={2023}
}

@article{chen2023minigptv2,
  title={MiniGPT-v2: Large Language Model as a Unified Interface for Vision-Language Multi-Task Learning},
  author={Chen, Jun and Zhu, Deyao and Shen, Xiaoqian and Li, Xiang and Liu, Zechun and Zhang, Pengchuan and Krishnamoorthi, Raghuraman and Chandra, Vikas and Xiong, Yunyang and Elhoseiny, Mohamed},
  journal={arXiv preprint arXiv:2310.09478},
  year={2023}
}
```

---

## Contact

For questions about the research, open an issue on the GitHub repository. For other inquiries, contact the maintainers listed in the project's documentation.

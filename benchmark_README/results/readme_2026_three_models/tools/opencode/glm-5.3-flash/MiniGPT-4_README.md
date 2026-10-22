# MiniGPT-4

This repository implements **MiniGPT-4** and **MiniGPT-v2**, two vision-language models that connect a frozen vision encoder with a frozen large language model (LLM) through trainable projection layers, enabling image understanding and multi-modal chat.

- **MiniGPT-4** aligns a BLIP-2-style vision encoder (frozen ViT, with a Q-Former for the Vicuna-based variants) to Vicuna-0 (7B/13B) or LLaMA-2-chat-7B, producing image-grounded dialogue.
- **MiniGPT-v2** extends this to a single multi-task model built on LLaMA-2-chat-7B with LoRA fine-tuning, covering multiple vision-language tasks selected via prompt tags.

Model configurations live in [`minigpt4/configs/models/`](minigpt4/configs/models/):

| Config | Architecture | LLM | Notes |
| --- | --- | --- | --- |
| `minigpt4_vicuna0.yaml` | `minigpt4` | Vicuna (path must be set) | ViT @ 224, frozen ViT and Q-Former, 32 query tokens |
| `minigpt4_llama2.yaml` | `minigpt4` | LLaMA-2-chat-7B (path must be set) | ViT @ 224, no Q-Former (`has_qformer: False`) |
| `minigpt_v2.yaml` | `minigpt_v2` | LLaMA-2-chat-7B (path must be set) | ViT @ 448, frozen ViT, LoRA (`lora_r: 64`, `lora_alpha: 16`) |

## Repository layout

```
MiniGPT-4/
├── train.py                     # Training entry point (torchrun distributed training)
├── demo.py                      # Gradio demo for MiniGPT-4 image chat
├── demo_v2.py                   # Gradio multi-task demo for MiniGPT-v2
├── environment.yml              # Conda environment (env name: minigptv)
├── minigpt4/                    # Main Python package
│   ├── common/                  # Config, registry, distributed utils, loggers, optimizers
│   ├── configs/                 # Model, dataset, and default run configs
│   ├── conversation/            # Conversation templates and the Chat wrapper
│   ├── datasets/                # Dataset builders and dataset implementations
│   ├── models/                  # Model implementations
│   ├── processors/              # Image/text processors
│   ├── runners/                 # Training runners
│   └── tasks/                   # Task setup (build datasets/models)
├── train_configs/               # Training configs (stage 1/2, LLaMA-2 variants, MiniGPT-v2)
├── eval_configs/                # Demo and benchmark evaluation configs
├── eval_scripts/                # Benchmark evaluation scripts + EVAL_README.md
├── dataset/                     # Dataset download/conversion instructions and scripts
├── examples/                    # MiniGPT-4 example images
├── examples_v2/                 # MiniGPT-v2 example images
├── figs/                        # Figures (overview, demos, example outputs)
├── MiniGPT4_Train.md            # MiniGPT-4 training instructions
├── MiniGPTv2_Train.md           # MiniGPT-v2 fine-tuning instructions
├── MiniGPTv2.pdf                # MiniGPT-v2 paper
├── LICENSE.md                   # BSD 3-Clause license
└── LICENSE_Lavis.md             # BSD 3-Clause license for LAVIS-derived code
```

## Installation

1. Clone this repository and create the conda environment:

   ```bash
   conda env create -f environment.yml
   conda activate minigptv
   ```

   The environment uses Python 3.9 and pins, among others, `torch==2.0.0`, `transformers==4.30.0`, `huggingface-hub==0.18.0`, `peft==0.2.0`, `bitsandbytes==0.37.0`, and `gradio==3.47.1` (see [`environment.yml`](environment.yml) for the full list).

2. Prepare a base LLM checkpoint and point the model configs to it:
   - For MiniGPT-4 (Vicuna variant): set `llama_model` in [`minigpt4/configs/models/minigpt4_vicuna0.yaml`](minigpt4/configs/models/minigpt4_vicuna0.yaml) to the path of the Vicuna model.
   - For MiniGPT-4 (LLaMA-2 variant) and MiniGPT-v2: set `llama_model` in [`minigpt4/configs/models/minigpt4_llama2.yaml`](minigpt4/configs/models/minigpt4_llama2.yaml) or [`minigpt4/configs/models/minigpt_v2.yaml`](minigpt4/configs/models/minigpt_v2.yaml) to the path of `llama2-chat-7b`.

3. Prepare the aligned vision-language checkpoint (MiniGPT-4 or MiniGPT-v2) and set `ckpt` in the relevant config under [`eval_configs/`](eval_configs/).

## Data preparation

- **MiniGPT-4 stage 1 (pretraining)**: LAION and CC3M/CC12M/SBU image-text pairs with BLIP-filtered synthetic captions. Follow [`dataset/README_1_STAGE.md`](dataset/README_1_STAGE.md); conversion utilities are provided in [`dataset/convert_cc_sbu.py`](dataset/convert_cc_sbu.py) and [`dataset/convert_laion.py`](dataset/convert_laion.py).
- **MiniGPT-4 stage 2 (fine-tuning)**: a small, high-quality image-text conversation dataset (`cc_sbu_align`). Follow [`dataset/README_2_STAGE.md`](dataset/README_2_STAGE.md).
- **MiniGPT-v2 fine-tuning**: a multi-task dataset mixture (COCO captions/VQA, Visual Genome, TextCaps, RefCOCO/RefCOCO+/RefCOCOg, OK-VQA, AOK-VQA, OCR-VQA, GQA, filtered Flickr30k, multi-task conversations, filtered Unnatural Instructions, and LLaVA-Instruct-150K subsets). Follow [`dataset/README_MINIGPTv2_FINETUNE.md`](dataset/README_MINIGPTv2_FINETUNE.md).
- **Benchmark evaluation data**: OK-VQA, GQA, Hateful Memes, IconQA, VizWiz, VSR, and RefCOCO/RefCOCO+/RefCOCOg. Follow [`eval_scripts/EVAL_README.md`](eval_scripts/EVAL_README.md).

## Training

Training is launched through [`train.py`](train.py) with a config file; the code supports distributed training via `torchrun` and optional Weights & Biases logging (`wandb_log`). Full instructions are in [`MiniGPT4_Train.md`](MiniGPT4_Train.md) and [`MiniGPTv2_Train.md`](MiniGPTv2_Train.md).

### MiniGPT-4

MiniGPT-4 training consists of two alignment stages:

1. **Stage 1 — pretraining** on LAION and CC/SBU data to align the vision encoder with the LLM. Reference hardware in the original experiments: 4× A100 GPUs.

   ```bash
   torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
   ```

2. **Stage 2 — fine-tuning** on the curated high-quality conversation dataset. Set the stage-1 checkpoint path and output path in [`train_configs/minigpt4_stage2_finetune.yaml`](train_configs/minigpt4_stage2_finetune.yaml). Reference hardware: 1× A100 GPU.

   ```bash
   torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigpt4_stage2_finetune.yaml
   ```

Additional configs are provided for the LLaMA-2 variants: [`train_configs/minigpt4_llama2_stage1_pretrain.yaml`](train_configs/minigpt4_llama2_stage1_pretrain.yaml) and [`train_configs/minigpt4_llama2_stage2_finetune.yaml`](train_configs/minigpt4_llama2_stage2_finetune.yaml).

### MiniGPT-v2

Set the `llama_model` checkpoint path, the pretrained `ckpt` path, and the checkpoint save path in [`train_configs/minigptv2_finetune.yaml`](train_configs/minigptv2_finetune.yaml), then run:

```bash
torchrun --nproc-per-node NUM_GPU train.py --cfg-path train_configs/minigptv2_finetune.yaml
```

## Demos

Both demos launch a Gradio web UI (with `share=True`) and accept `--cfg-path` and `--gpu-id` arguments:

```bash
python demo.py --cfg-path eval_configs/minigpt4_eval.yaml --gpu-id 0
python demo_v2.py --cfg-path eval_configs/minigptv2_eval.yaml --gpu-id 0
```

- **[`demo.py`](demo.py)** — MiniGPT-4 chat demo: upload an image, then chat about it; exposes beam-search and temperature controls. Conversation templates are selected automatically for the Vicuna-0 (`CONV_VISION_Vicuna0`) and LLaMA-2 (`CONV_VISION_LLama2`) model types. The corresponding configs are [`eval_configs/minigpt4_eval.yaml`](eval_configs/minigpt4_eval.yaml) and [`eval_configs/minigpt4_llama2_eval.yaml`](eval_configs/minigpt4_llama2_eval.yaml).
- **[`demo_v2.py`](demo_v2.py)** — MiniGPT-v2 multi-task demo with task shortcuts and streaming responses. Tasks are selected via prompt tags:
  - `[grounding]` — grounded image description with drawn bounding boxes
  - `[refer]` — localize a described object in the image
  - `[detection]` — detect objects for a given caption or phrase
  - `[identify]` — identify an object inside a drawn bounding box (draw on the uploaded image; the bounding box is parsed from the mask)
  - `[vqa]` — short visual question answering
  - no tag — free-form conversation

  Bounding boxes returned by the model are rendered back onto the image in the chat UI. Example inputs are included from [`examples_v2/`](examples_v2/). Config: [`eval_configs/minigptv2_eval.yaml`](eval_configs/minigptv2_eval.yaml).

## Benchmark evaluation

Evaluation scripts for MiniGPT-v2 live in [`eval_scripts/`](eval_scripts/) and are configured via [`eval_configs/minigptv2_benchmark_evaluation.yaml`](eval_configs/minigptv2_benchmark_evaluation.yaml). After setting the LLaMA model path, checkpoint path, and per-dataset `eval_file_path`, `img_path`, and `save_path` values:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/MiniGPT-4

# Referring expression comprehension
torchrun --master-port ${port} --nproc_per_node 1 eval_scripts/eval_ref.py \
    --cfg-path ${cfg_path} --dataset refcoco,refcoco+,refcocog --resample

# Visual question answering
torchrun --master-port ${port} --nproc_per_node 1 eval_scripts/eval_vqa.py \
    --cfg-path ${cfg_path} --dataset okvqa,vizwiz,iconvqa,gqa,vsr,hm
```

Supported benchmark datasets: `refcoco`, `refcoco+`, `refcocog` (referring) and `okvqa`, `vizwiz`, `iconvqa`, `gqa`, `vsr`, `hm` (VQA). See [`eval_scripts/EVAL_README.md`](eval_scripts/EVAL_README.md) for download links and the required dataset directory structure.

## Examples

- [`examples/`](examples/) contains sample outputs demonstrating MiniGPT-4 capabilities such as image description, ad creation, photo-to-recipe/HTML conversion, problem solving, rhyming, and storytelling.
- [`examples_v2/`](examples_v2/) contains the sample images wired into the MiniGPT-v2 demo.
- [`figs/`](figs/) contains the project overview and demo figures.

## License

This repository is released under the BSD 3-Clause License (see [`LICENSE.md`](LICENSE.md)). Code derived from the [LAVIS](https://github.com/salesforce/LAVIS) framework (e.g., [`train.py`](train.py)) is covered by [`LICENSE_Lavis.md`](LICENSE_Lavis.md), also BSD 3-Clause.

## Notes

- The demo entry points in this repository reference the project pages `minigpt-4.github.io` (MiniGPT-4) and `minigpt-v2.github.io` (MiniGPT-v2).
- `.github/ISSUE_TEMPLATE/` contains GitHub issue templates for reporting problems.
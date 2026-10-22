# README

**FLUX** (`flux-0f014y28`) — Inference toolkit, demos, CLIs and TensorRT acceleration for the **FLUX.1** family of image generation and editing models.

FLUX.1 is a family of state-of-the-art, 12-billion-parameter rectified-flow transformer models developed by Black Forest Labs. This repository contains the code needed to run them: a modular inference stack, task-specific CLIs, interactive Gradio and Streamlit demos, TensorRT engine building/management, LoRA adapter loading, and built-in safety filtering.

![FLUX.1 sample grid](grid.jpg)

---

## Table of Contents

- [Overview](#overview)
- [Models](#models)
- [Features](#features)
- [Installation](#installation)
- [Model Weights & Authentication](#model-weights--authentication)
- [Quick Start](#quick-start)
- [Task Guides](#task-guides)
  - [Text-to-Image](#1-text-to-image)
  - [Image Editing (FLUX.1 Kontext)](#2-image-editing-flux1-kontext)
  - [Fill — Inpainting & Outpainting](#3-fill--inpainting--outpainting)
  - [Structural Conditioning (Canny / Depth)](#4-structural-conditioning-canny--depth)
  - [Image Variation (FLUX.1 Redux)](#5-image-variation-flux1-redux)
- [TensorRT Acceleration](#tensorrt-acceleration)
- [LoRA Support](#lora-support)
- [Content Safety](#content-safety)
- [Memory & Performance Tips](#memory--performance-tips)
- [Codebase Tour](#codebase-tour)
- [Project Layout](#project-layout)
- [Documentation](#documentation)
- [Licenses](#licenses)
- [Troubleshooting](#troubleshooting)
- [Citation & Acknowledgements](#citation--acknowledgements)

---

## Overview

The FLUX.1 suite covers the full spectrum of generative image tasks:

| Capability | Model | Description |
|---|---|---|
| Text-to-image | FLUX.1 [dev] / FLUX.1 [schnell] | High-fidelity prompt following, strong typography, diverse aspect ratios |
| Image editing | FLUX.1 [dev] Kontext | In-context, instruction-based editing with character consistency |
| Inpainting / Outpainting | FLUX.1 [dev] Fill | Mask-based image completion and canvas extension |
| Structural conditioning | FLUX.1 [dev] Canny / Depth | Edge- and depth-guided generation |
| Image variation | FLUX.1 [dev] Redux | Re-imagine and vary input images, optionally steered by text |

This repository packages all of the above behind a single, consistent interface:

- **CLI entry points** — one module per task (`python -m flux`, `python -m flux.cli_fill`, …)
- **Interactive demos** — Gradio (`demo_gr.py`) and Streamlit (`demo_st.py`, `demo_st_fill.py`)
- **A composable Python API** — transformer, conditioners, image embedders, VAE and samplers as separate, reusable modules
- **Optional TensorRT backends** — per-component engines (CLIP, T5, transformer, VAE) with a build/cache manager

---

## Models

| Model | Hugging Face repo | Task | License | Typical steps | Guidance |
|---|---|---|---|---|---|
| FLUX.1 [dev] | `black-forest-labs/FLUX.1-dev` | text-to-image | FLUX.1 [dev] Non-Commercial | 20–50 (default 50) | 3.5 |
| FLUX.1 [schnell] | `black-forest-labs/FLUX.1-schnell` | text-to-image | Apache-2.0 | 1–4 (default 4) | 0.0 |
| FLUX.1 [dev] Fill | `black-forest-labs/FLUX.1-Fill-dev` | inpaint / outpaint | FLUX.1 [dev] Non-Commercial | 50 | 30 |
| FLUX.1 [dev] Canny | `black-forest-labs/FLUX.1-Canny-dev` | structural conditioning | FLUX.1 [dev] Non-Commercial | 50 | 30 |
| FLUX.1 [dev] Depth | `black-forest-labs/FLUX.1-Depth-dev` | structural conditioning | FLUX.1 [dev] Non-Commercial | 50 | 30 |
| FLUX.1 [dev] Redux | `black-forest-labs/FLUX.1-Redux-dev` (adapter, used with [dev]) | image variation | FLUX.1 [dev] Non-Commercial | 50 | 2.5 |
| FLUX.1 [dev] Kontext | `black-forest-labs/FLUX.1-Kontext-dev` | in-context image editing | FLUX.1 [dev] Non-Commercial | 20–50 | 2.5 |

- **[dev]** models are guidance-distilled and offer the highest quality; their weights and outputs are governed by a **non-commercial license**.
- **[schnell]** is step-distilled for 1–4 step generation and is fully **open-source (Apache-2.0)**.

---

## Features

- 🖼️ **Five task families** from one codebase: text-to-image, editing, fill, control, variation
- ⚡ **TensorRT acceleration** — compiled engines for CLIP, T5, the transformer and the VAE, with automatic build & caching
- 🧩 **Modular architecture** — `model`, `conditioner`, `image_embedders`, `autoencoder`, `sampling` can be used independently in your own pipelines
- 🎛️ **LoRA support** — attach community or custom adapters at inference time
- 🖥️ **Three frontends** — headless CLI, Gradio web UI, Streamlit apps
- 🔒 **Safety filters** — prompt/image NSFW checking included, as required by the model licenses
- 💾 **Automatic weight download** from Hugging Face, with local-path overrides via environment variables
- 🔋 **Memory offloading** — run large [dev] models on modest GPUs by streaming components on/off the accelerator

---

## Installation

### Requirements

- Python **3.10+**
- PyTorch **2.x** with CUDA
- NVIDIA GPU (CUDA 12.x recommended)
- ~**60 GB** disk space for full model weights (transformers + text encoders + VAE)
- Linux is recommended; Windows works with WSL2

### Install

```bash
git clone <this-repository> flux-0f014y28
cd flux-0f014y28
pip install -e .
```

Optional dependency groups are provided via `pyproject.toml` extras:

```bash
pip install -e ".[gradio]"      # Gradio web demo (demo_gr.py)
pip install -e ".[streamlit]"   # Streamlit demos (demo_st*.py)
pip install -e ".[generators]"  # streaming generation utilities
pip install -e ".[tensorrt]"    # TensorRT engine building & inference
```

---

## Model Weights & Authentication

Weights are pulled automatically from Hugging Face on first use.

- **FLUX.1 [dev]-family repos are gated.** Accept the license on the model page, then authenticate:

```bash
huggingface-cli login
# or
export HF_TOKEN=hf_...
```

Weights are cached in the standard Hugging Face cache (`~/.cache/huggingface`). To point the code at **local copies** of individual components (e.g. on a shared cluster), export any of the following environment variables:

| Variable | Component |
|---|---|
| `FLUX_DEV` | FLUX.1 [dev] transformer |
| `FLUX_SCHNELL` | FLUX.1 [schnell] transformer |
| `FLUX_DEV_FILL` | Fill transformer |
| `FLUX_DEV_KONTEXT` | Kontext transformer |
| `FLUX_DEV_CANNY` / `FLUX_DEV_DEPTH` | Canny / Depth transformers |
| `FLUX_DEV_REDUX` | Redux image adapter |
| `AE` | Autoencoder (VAE) |
| `CLIP` | CLIP-L text encoder |
| `T5XXL` | T5-XXL text encoder |

---

## Quick Start

### CLI (text-to-image)

The package exposes a `__main__` entry point, so the simplest way to generate an image is:

```bash
# One-shot generation
python -m flux \
  --name flux-schnell \
  --width 1024 --height 1024 \
  --steps 4 \
  --prompt "a robot holding a red cup, studio lighting" \
  --save-path samples/

# Interactive prompt loop — keeps the model in VRAM between prompts
python -m flux --name flux-dev --loop
```

Commonly used options (see `python -m flux --help` for the full list):

| Flag | Meaning |
|---|---|
| `--name` | Model preset (`flux-dev`, `flux-schnell`, `flux-fill-dev`, `flux-kontext-dev`, `flux-canny-dev`, `flux-depth-dev`) |
| `--prompt` | Text prompt |
| `--width` / `--height` | Output resolution |
| `--steps` | Sampling steps |
| `--guidance` | Guidance strength (0 for schnell) |
| `--seed` | Random seed |
| `--device` | Torch device (default `cuda`) |
| `--offload` | Offload text encoders/VAE to CPU between phases (lower VRAM) |
| `--save-path` | Output directory |
| `--add_sampling_metadata` | Embed prompt/settings in EXIF |
| `--loop` | Keep the process alive for multiple prompts |

### Gradio web UI

```bash
python demo_gr.py --name flux-schnell --device cuda
# → open http://127.0.0.1:7860
```

### Streamlit demos

```bash
streamlit run demo_st.py -- --name flux-dev        # text-to-image playground
streamlit run demo_st_fill.py -- --name flux-fill-dev  # inpainting / outpainting playground
```

---

## Task Guides

Each task ships with a dedicated CLI module and a markdown guide (see [Documentation](#documentation)).

### 1. Text-to-Image

Plain prompt → image generation with FLUX.1 [dev] or [schnell].

```bash
python -m flux --name flux-dev --guidance 3.5 --steps 50 \
  --prompt "a tiny robot drinking coffee in a cozy cafe"
```

📖 Full guide: [`text-to-image.md`](text-to-image.md) · Model notes: [`FLUX.1-dev.md`](FLUX.1-dev.md), [`FLUX.1-schnell.md`](FLUX.1-schnell.md)

Example grids produced with the two models:

![dev grid](dev_grid.jpg)
![schnell grid](schnell_grid.jpg)

### 2. Image Editing (FLUX.1 Kontext)

In-context editing: pass a **reference image plus an editing instruction**. Kontext preserves identity and composition across iterative edits.

```bash
python -m flux.cli_kontext \
  --input robot.webp \
  --prompt "Turn the robot into a stormtrooper, keep everything else the same" \
  --name flux-kontext-dev \
  --offload
```

![Kontext example](kontext.png)

📖 Full guide: [`image-editing.md`](image-editing.md) · Model notes: [`FLUX.1-kontext-dev.md`](FLUX.1-kontext-dev.md)

### 3. Fill — Inpainting & Outpainting

Mask-driven completion. Provide a conditioning image and a binary mask; the model regenerates only the masked region (inpainting) or extends the canvas (outpainting — supply a mask covering the new borders).

```bash
python -m flux.cli_fill \
  --img-cond cup.png \
  --img-mask cup_mask.png \
  --prompt "a black coffee cup filled to the brim with espresso" \
  --name flux-fill-dev \
  --offload
```

| Input | Mask | Result |
|---|---|---|
| ![cup](cup.png) | ![cup mask](cup_mask.png) | ![inpainting](inpainting.png) |

For outpainting, place your image on a larger canvas and mask the empty border region — see `outpainting.png` for a reference result.

📖 Full guide: [`fill.md`](fill.md)

### 4. Structural Conditioning (Canny / Depth)

Guide generation with a structural map extracted from an input image.

```bash
# Edge-guided
python -m flux.cli_control \
  --control-image robot.webp \
  --control-mode canny \
  --prompt "a vintage robot made of rusty scrap metal" \
  --name flux-canny-dev \
  --offload

# Depth-guided
python -m flux.cli_control \
  --control-image robot.webp \
  --control-mode depth \
  --prompt "a shiny chrome robot in a modern kitchen" \
  --name flux-depth-dev \
  --offload
```

| Canny | Depth |
|---|---|
| ![canny](canny.png) | ![depth](depth.png) |

📖 Full guide: [`structural-conditioning.md`](structural-conditioning.md)

### 5. Image Variation (FLUX.1 Redux)

Re-imagine an input image. Redux encodes the reference with a vision encoder and mixes it into the prompt embedding; a text prompt optionally steers the variation.

```bash
python -m flux.cli_redux \
  --input robot.webp \
  --prompt "the same robot, but made of translucent ice" \
  --name flux-dev \
  --offload
```

![Redux example](redux.png)

📖 Full guide: [`image-variation.md`](image-variation.md)

---

## TensorRT Acceleration

For production and benchmarking workloads, every heavy component of the pipeline can be executed on **NVIDIA TensorRT** engines instead of vanilla PyTorch, typically yielding substantially lower latency per image.

**Architecture**

| File | Role |
|---|---|
| `base_engine.py` | Common engine runtime abstraction (build, load, infer) |
| `clip_engine.py` / `t5_engine.py` | Text-encoder engines |
| `transformer_engine.py` | Denoising transformer engine |
| `vae_engine.py` | Autoencoder (decode/encode) engine |
| `base_trt_config.py` | Shared engine-config base (shapes, dtypes, workspace) |
| `clip_trt_config.py` / `t5_trt_config.py` / `transformer_trt_config.py` / `vae_trt_config.py` | Per-component build configs |
| `trt_manager.py` | Orchestrates building, versioning and caching of all engines |

**Workflow**

1. Install the extra: `pip install -e ".[tensorrt]"`.
2. Build engines once per model/GPU — plans are serialized and cached, so subsequent runs load instantly:

```bash
python -m flux.trt_manager --name flux-dev
```

3. Run any CLI or demo; engine-backed components are used where available (check each entry point's `--help` for engine-selection flags).

Notes:

- The first build compiles kernels and can take several minutes per component.
- Engines are **not portable across GPU architectures or TensorRT versions** — rebuild when either changes.
- Fixed-shape engines are fastest; dynamic shapes add flexibility at a small runtime cost (configure this in the `*_trt_config.py` files).

---

## LoRA Support

`lora.py` implements LoRA (Low-Rank Adaptation) layers and utilities for attaching adapters to the FLUX transformer's linear layers at inference time — no base-weight changes required. Use cases include community fine-tunes, style adapters, and personalization.

```python
from flux.model import Flux
from flux.lora import load_lora

model = Flux(params)                       # instantiate the 12B transformer
load_lora(model, "my_adapter.safetensors", scale=0.9)  # attach adapter weights
```

Adapters are composable: load multiple adapters with different scales, or remove them at runtime to restore the base model exactly.

---

## Content Safety

`content_filters.py` provides the safety machinery required by the FLUX.1 model licenses:

- **Prompt-side filtering** of user text before generation.
- **Output-side NSFW classification** of generated images; flagged images are **blurred** before being written to disk or shown in a UI.

The filters are used by all CLIs and demos by default. If you build your own pipeline on top of this codebase, please retain equivalent checks — this is a condition of the FLUX.1 [dev] license terms.

---

## Memory & Performance Tips

| Situation | Recommendation |
|---|---|
| ≥ 24 GB VRAM | Run [dev]-family models directly in bfloat16 |
| 12–16 GB VRAM | Use `--offload` (streams text encoders / VAE between CPU and GPU) |
| Speed-critical serving | Build TensorRT engines (see above) |
| Fast iteration | Use `flux-schnell` with 4 steps |
| Repeated prompts | Use `--loop` in the CLI to keep weights resident in VRAM |
| Lower resolution | 768 px outputs scale VRAM usage down roughly quadratically |

---

## Codebase Tour

| Module | Role |
|---|---|
| `model.py` | FLUX transformer: double-stream + single-stream MMDiT blocks with adaLN modulation |
| `layers.py` | Building blocks: attention, QK-norm, MLPs, embeddings |
| `math.py` | RoPE and attention math utilities |
| `sampling.py` | Flow-matching schedules and samplers (e.g. Euler with time-shift) |
| `conditioner.py` | T5-XXL and CLIP-L text conditioning |
| `image_embedders.py` | Image-side conditioning: Redux encoder, Canny/Depth preprocessor + encoders, Fill conditions |
| `autoencoder.py` | VAE encoder/decoder (latent ⇄ pixels) |
| `lora.py` | LoRA layers and adapter loading |
| `content_filters.py` | NSFW safety filters |
| `util.py` | Weight loading, Hugging Face helpers, model configs, image I/O |
| `cli.py`, `__main__.py` | Main text-to-image CLI (`python -m flux`) |
| `cli_fill.py`, `cli_kontext.py`, `cli_control.py`, `cli_redux.py` | Task-specific CLIs |
| `*_engine.py`, `*_trt_config.py`, `trt_manager.py` | TensorRT runtime, configs and manager |

---

## Project Layout

```
flux-0f014y28/
├── LICENSE, LICENSE-FLUX1-dev, LICENSE-FLUX1-schnell
├── pyproject.toml, setup.py
├── demo_gr.py                  # Gradio web UI
├── demo_st.py                  # Streamlit text-to-image demo
├── demo_st_fill.py             # Streamlit fill (inpaint/outpaint) demo
├── text-to-image.md            # task guides ↓
├── image-editing.md
├── fill.md
├── structural-conditioning.md
├── image-variation.md
├── FLUX.1-dev.md, FLUX.1-schnell.md, FLUX.1-kontext-dev.md
├── grid.jpg, dev_grid.jpg, schnell_grid.jpg        # sample grids
├── cup.png, cup_mask.png, robot.webp, kontext.png  # example inputs
├── canny.png, depth.png, redux.png                 # example conditions
├── inpainting.png, outpainting.png                 # example outputs
└── src/
    └── flux/
        ├── __init__.py, __main__.py
        ├── cli.py, cli_fill.py, cli_kontext.py, cli_control.py, cli_redux.py
        ├── model.py, layers.py, math.py, sampling.py
        ├── conditioner.py, image_embedders.py, autoencoder.py
        ├── lora.py, content_filters.py, util.py
        ├── base_engine.py, clip_engine.py, t5_engine.py,
        │   transformer_engine.py, vae_engine.py
        ├── base_trt_config.py, clip_trt_config.py, t5_trt_config.py,
        │   transformer_trt_config.py, vae_trt_config.py
        └── trt_manager.py
```

---

## Documentation

| Document | Contents |
|---|---|
| [`text-to-image.md`](text-to-image.md) | Prompting, resolutions, sampler settings for [dev]/[schnell] |
| [`FLUX.1-dev.md`](FLUX.1-dev.md) | Model card for FLUX.1 [dev] |
| [`FLUX.1-schnell.md`](FLUX.1-schnell.md) | Model card for FLUX.1 [schnell] |
| [`image-editing.md`](image-editing.md) | Kontext editing workflows and prompting tips |
| [`FLUX.1-kontext-dev.md`](FLUX.1-kontext-dev.md) | Model card for Kontext |
| [`fill.md`](fill.md) | Inpainting/outpainting mask formats and recipes |
| [`structural-conditioning.md`](structural-conditioning.md) | Canny & Depth control usage |
| [`image-variation.md`](image-variation.md) | Redux variation and text steering |

---

## Licenses

This repository ships three license files:

| File | Applies to | Terms |
|---|---|---|
| `LICENSE` | The **code** in this repository | Apache-2.0 |
| `LICENSE-FLUX1-schnell` | FLUX.1 [schnell] **weights & outputs** | Apache-2.0 |
| `LICENSE-FLUX1-dev` | FLUX.1 [dev]-family **weights & outputs** (dev, Fill, Canny, Depth, Redux, Kontext) | FLUX.1 [dev] Non-Commercial License |

⚠️ **Important:** images generated with any `[dev]`-family model fall under the non-commercial license terms and may additionally be subject to the "additional guidelines" appended to that license. Code remains Apache-2.0 regardless of which weights you run.

---

## Troubleshooting

- **`401 / gated repo` errors** → accept the model license on Hugging Face and log in (`huggingface-cli login` or `HF_TOKEN`).
- **CUDA out-of-memory** → add `--offload`, reduce `--width/--height`, or switch to `flux-schnell`.
- **First run is slow** → weights are being downloaded/cached; subsequent runs are fast.
- **TensorRT engine rebuilds every launch** → engines are keyed by GPU architecture and TensorRT version; make sure the cache directory is writable and persistent.
- **LoRA has no effect** → verify the adapter matches the FLUX architecture and that the scale is non-zero.

---

## Citation & Acknowledgements

If you use the FLUX.1 models or this codebase in your work, please cite:

```bibtex
@misc{FLUX.1,
  author       = {Black Forest Labs},
  title        = {{FLUX.1}: State-of-the-art image generation with corrected flow transformer},
  year         = {2024},
  howpublished = {\url{https://blackforestlabs.ai}},
}
```

Built with [PyTorch](https://pytorch.org), [Hugging Face Transformers/Diffusers](https://huggingface.co), [Gradio](https://gradio.app), [Streamlit](https://streamlit.io) and [NVIDIA TensorRT](https://developer.nvidia.com/tensorrt). Models by **Black Forest Labs** — see the individual model cards and license files for usage terms.

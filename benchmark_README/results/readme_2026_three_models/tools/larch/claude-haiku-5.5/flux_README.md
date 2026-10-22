# FLUX

FLUX is a family of rectified-flow transformer models for text-to-image generation and image editing. This repository provides inference code, command-line tools, and interactive demos for the FLUX.1 model family. It supports text-to-image generation, inpainting and outpainting, structural conditioning (Canny edges and depth), image variation via Redux, and instruction-based image editing via Kontext.

> **Note:** The command-line flags and module paths below reflect the typical layout of this codebase. Run `python -m flux --help` or check the relevant `cli_*.py` file to confirm exact options for your version.

---

## Table of Contents

- [Features](#features)
- [Model Variants](#model-variants)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Downloading Model Weights](#downloading-model-weights)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Text-to-Image](#text-to-image)
  - [Inpainting and Outpainting (Fill)](#inpainting-and-outpainting-fill)
  - [Structural Conditioning (Canny and Depth)](#structural-conditioning-canny-and-depth)
  - [Image Variation (Redux)](#image-variation-redux)
  - [Image Editing (Kontext)](#image-editing-kontext)
- [Interactive Demos](#interactive-demos)
- [Using FLUX from Python](#using-flux-from-python)
- [TensorRT Acceleration](#tensorrt-acceleration)
- [Content Safety Filter](#content-safety-filter)
- [Memory Optimization](#memory-optimization)
- [Architecture Overview](#architecture-overview)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [License](#license)
- [Citation](#citation)

---

## Features

- **Text-to-image generation** with FLUX.1 schnell (fast, few steps) and FLUX.1 dev (higher quality, guidance-distilled).
- **Inpainting and outpainting** with a dedicated Fill model and a mask.
- **Structural conditioning** with Canny-edge and depth-map control via LoRA adapters.
- **Image variation** with Redux, which conditions generation on a reference image.
- **Instruction-based editing** with Kontext, which edits an image from a text instruction.
- **Command-line interfaces** for each task.
- **Gradio and Streamlit demos** for interactive use.
- **Optional TensorRT engines** for faster inference on NVIDIA GPUs.
- **Built-in content filtering** for generated outputs.
- **Memory-saving options** such as model offloading and quantization-friendly loading.

---

## Model Variants

| Model | Purpose | Typical Steps | License |
|---|---|---|---|
| FLUX.1 [schnell] | Fast text-to-image | 1–4 | Apache 2.0 |
| FLUX.1 [dev] | High-quality text-to-image | ~20–50 | FLUX.1 [dev] Non-Commercial License |
| FLUX.1 Fill [dev] | Inpainting and outpainting | ~20–50 | FLUX.1 [dev] Non-Commercial License |
| FLUX.1 Depth / Canny [dev] | Structural conditioning | ~20–50 | FLUX.1 [dev] Non-Commercial License |
| FLUX.1 Redux [dev] | Image variation | ~20–50 | FLUX.1 [dev] Non-Commercial License |
| FLUX.1 Kontext [dev] | Instruction-based editing | ~20–30 | FLUX.1 [dev] Non-Commercial License |

Check each model's license before commercial use. The `LICENSE-FLUX1-schnell` and `LICENSE-FLUX1-dev` files in this repository contain the full terms.

---

## Repository Structure

```
flux/
├── flux/                       # Main Python package
│   ├── __init__.py
│   ├── __main__.py             # Entry point: python -m flux
│   ├── cli.py                  # Text-to-image CLI
│   ├── cli_fill.py             # Inpainting/outpainting CLI
│   ├── cli_control.py          # Canny/depth structural conditioning CLI
│   ├── cli_redux.py            # Redux image variation CLI
│   ├── cli_kontext.py          # Kontext image editing CLI
│   ├── sampling.py             # Denoising loops and noise/latent utilities
│   ├── model.py                # Core FLUX transformer definition
│   ├── layers.py               # Transformer building blocks (attention, MLP, embeddings)
│   ├── math.py                 # Attention and RoPE math helpers
│   ├── autoencoder.py          # VAE encoder/decoder
│   ├── conditioner.py          # Text encoder wrappers (CLIP and T5)
│   ├── image_embedders.py      # Image encoders used by Redux and Kontext
│   ├── lora.py                 # LoRA loading and merging
│   ├── content_filters.py      # Safety/NSFW filtering of outputs
│   ├── util.py                 # Model loading, configs, image I/O helpers
│   ├── trt/                    # TensorRT acceleration
│   │   ├── __init__.py
│   │   ├── trt_manager.py      # Builds, loads, and manages TRT engines
│   │   ├── base_engine.py      # Shared engine logic
│   │   ├── transformer_engine.py
│   │   ├── vae_engine.py
│   │   ├── clip_engine.py
│   │   ├── t5_engine.py
│   │   ├── base_trt_config.py
│   │   ├── transformer_trt_config.py
│   │   ├── vae_trt_config.py
│   │   ├── clip_trt_config.py
│   │   └── t5_trt_config.py
│   └── ...
├── demo_gr.py                  # Gradio web demo
├── demo_st.py                  # Streamlit web demo
├── demo_st_fill.py             # Streamlit demo for inpainting/outpainting
├── setup.py                    # Package setup (legacy)
├── pyproject.toml              # Build configuration and dependencies
├── LICENSE
├── LICENSE-FLUX1-schnell
├── LICENSE-FLUX1-dev
├── text-to-image.md            # Task docs
├── image-variation.md
├── fill.md
├── structural-conditioning.md
├── image-editing.md
├── FLUX.1-schnell.md           # Model cards
├── FLUX.1-dev.md
├── FLUX.1-kontext-dev.md
├── grid.jpg, dev_grid.jpg, schnell_grid.jpg   # Sample grids
├── cup.png, robot.webp, kontext.png, canny.png,
│   depth.png, redux.png, inpainting.png,
│   outpainting.png             # Example inputs
└── cup_mask.png                # Example mask for inpainting
```

### Key Modules

| Module | Responsibility |
|---|---|
| `model.py` | The diffusion transformer (MMDiT-style double-stream and single-stream blocks). |
| `layers.py` | Attention, MLP, modulation, and positional embedding layers. |
| `sampling.py` | Prepares latents and image tokens, and runs the flow-matching sampler. |
| `autoencoder.py` | Converts between pixel space and latent space. |
| `conditioner.py` | Encodes prompts with CLIP (pooled) and T5 (sequence) text encoders. |
| `image_embedders.py` | Encodes reference images for Redux and Kontext. |
| `lora.py` | Applies LoRA weights for structural conditioning. |
| `util.py` | Loads checkpoints, selects model configs, and handles image I/O. |
| `content_filters.py` | Screens generated images before they are returned or saved. |
| `trt/` | Builds and runs TensorRT engines for the transformer, VAE, and text encoders. |

---

## Requirements

### Hardware

- **NVIDIA GPU** with CUDA support. Recommended VRAM:
  - FLUX.1 schnell: ~12–16 GB
  - FLUX.1 dev and derived models: ~24 GB, or less with offloading
- **System RAM:** 32 GB or more is recommended, especially when loading T5 and CLIP.
- **Disk:** Roughly 30–60 GB free for model weights, depending on which models you download.

### Software

- Python 3.10 or newer (3.10–3.12 recommended)
- CUDA-enabled PyTorch (2.x)
- Git and Git LFS (only if you clone model repositories)
- Optional: TensorRT and the matching CUDA toolkit, for TRT acceleration

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url> flux
cd flux
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows
```

### 3. Install PyTorch with CUDA

Install the build that matches your CUDA version from [pytorch.org](https://pytorch.org). For example:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### 4. Install FLUX

Install in editable mode:

```bash
pip install -e .
```

To include the optional demo dependencies (Gradio, Streamlit) and TensorRT support, install the extras defined in `pyproject.toml`:

```bash
pip install -e ".[all]"
```

Check `pyproject.toml` for the exact extra names available in your version.

### 5. Verify the installation

```bash
python -c "import flux; print('FLUX import OK')"
python -m flux --help
```

---

## Downloading Model Weights

Model weights are downloaded automatically from Hugging Face on first use. You need to:

1. Create a Hugging Face account and accept the license for each gated model (for example, FLUX.1 dev) on its model page.
2. Create an access token at https://huggingface.co/settings/tokens.
3. Authenticate:

```bash
huggingface-cli login
# or
export HF_TOKEN=hf_xxxSecretTokenxxx
```

Weights are cached in the Hugging Face cache directory (`~/.cache/huggingface` by default). To change the location:

```bash
export HF_HOME=/path/to/large/disk/huggingface
```

To pre-download a model:

```bash
huggingface-cli download black-forest-labs/FLUX.1-dev
```

---

## Quick Start

Generate an image with FLUX.1 schnell from the command line:

```bash
python -m flux --name flux-schnell --prompt "a cup of coffee on a wooden table, morning light" --width 1024 --height 1024
```

Then open the Gradio demo:

```bash
python demo_gr.py
```

---

## Usage

### Text-to-Image

Generate images from a text prompt. See `text-to-image.md` and the model cards (`FLUX.1-schnell.md`, `FLUX.1-dev.md`) for details.

```bash
# Fast generation with schnell
python -m flux --name flux-schnell \
  --prompt "a robot painting a landscape, oil on canvas" \
  --width 1024 --height 768 \
  --num_steps 4 \
  --seed 42 \
  --out outputs/robot.png

# Higher quality with dev
python -m flux --name flux-dev \
  --prompt "a photorealistic red fox in snow, 85mm lens" \
  --width 1024 --height 1024 \
  --num_steps 50 \
  --guidance 3.5 \
  --seed 1234
```

**Common options:**

| Option | Description |
|---|---|
| `--name` | Model variant (`flux-schnell`, `flux-dev`). |
| `--prompt` | Text prompt. |
| `--width`, `--height` | Output size. Use multiples of 16. |
| `--num_steps` | Number of denoising steps. |
| `--guidance` | Guidance scale (used by dev). |
| `--seed` | Random seed for reproducibility. |
| `--out` | Output path. |
| `--loop` | Keep the model loaded and prompt repeatedly. |
| `--offload` | Offload modules to CPU to reduce VRAM usage. |

### Inpainting and Outpainting (Fill)

Fill the masked region of an image based on the prompt. See `fill.md`.

- **Inpainting:** Provide an image and a mask. White areas are regenerated.
- **Outpainting:** Extend the canvas and mask the new region.

```bash
# Inpainting
python -m flux.cli_fill \
  --img_file_path inpainting.png \
  --mask_file_path cup_mask.png \
  --prompt "a ceramic mug with steam rising" \
  --num_steps 50 \
  --guidance 30 \
  --out outputs/inpainted.png

# Outpainting: pad the image first, then mask the padded area
python -m flux.cli_fill \
  --img_file_path outpainting.png \
  --mask_file_path outpainting_mask.png \
  --prompt "a wide mountain valley at sunset" \
  --out outputs/outpainted.png
```

The Fill model expects the mask to be white where content should be generated and black where the original image should be kept. Check your mask polarity if results look wrong.

### Structural Conditioning (Canny and Depth)

Guide generation with the edges or depth of a reference image. See `structural-conditioning.md`.

```bash
# Canny edge conditioning
python -m flux.cli_control \
  --name flux-canny \
  --img_control canny.png \
  --prompt "a sports car in a futuristic city, neon lights" \
  --num_steps 50 \
  --out outputs/canny_result.png

# Depth conditioning
python -m flux.cli_control \
  --name flux-depth \
  --img_control depth.png \
  --prompt "a stone statue in a sunlit garden" \
  --out outputs/depth_result.png
```

Pass a pre-computed control image (edge map or depth map) to `--img_control`. If the codebase supports automatic preprocessing, the CLI may also accept a raw photo. Consult `--help` to confirm.

### Image Variation (Redux)

Generate variations of an input image. The model encodes the reference image and uses it as conditioning. See `image-variation.md`.

```bash
python -m flux.cli_redux \
  --img_file_path redux.png \
  --prompt "same scene in watercolor style" \
  --out outputs/redux_variation.png
```

Redux can also be combined with a text prompt to steer the variation.

### Image Editing (Kontext)

Edit an image with a natural-language instruction. See `image-editing.md` and `FLUX.1-kontext-dev.md`.

```bash
python -m flux.cli_kontext \
  --img_file_path kontext.png \
  --prompt "change the background to a snowy forest" \
  --num_steps 28 \
  --out outputs/kontext_edit.png
```

Good instructions are short and specific, such as "make the car red," "remove the person on the left," or "turn it into a pencil sketch."

---

## Interactive Demos

### Gradio

```bash
python demo_gr.py
```

Then open the printed local URL (typically `http://127.0.0.1:7860`). Add `--share` if the script supports it to get a temporary public link.

### Streamlit

```bash
streamlit run demo_st.py
```

For the inpainting and outpainting interface:

```bash
streamlit run demo_st_fill.py
```

The Streamlit app typically opens at `http://localhost:8501`.

---

## Using FLUX from Python

The CLI is a thin layer over the library. You can call the components directly.

```python
import torch
from flux.util import load_flow_model, load_ae, load_clip, load_t5
from flux.sampling import prepare, get_noise, denoise, unpack
from flux.util import load_flow_model

device = "cuda"
name = "flux-schnell"

# Load models
t5 = load_t5(device, max_length=256)
clip = load_clip(device)
model = load_flow_model(name, device=device)
ae = load_ae(name, device=device)

prompt = "a lighthouse on a cliff during a storm, cinematic lighting"
width, height = 1024, 1024
num_steps = 4
seed = 42

# Prepare inputs
x = get_noise(1, height, width, device=device, dtype=torch.bfloat16, seed=seed)
inp = prepare(t5=t5, clip=clip, img=x, prompt=prompt)

# Denoise and decode
with torch.no_grad():
    x = denoise(model, **inp, num_steps=num_steps, guidance=0.0)
    x = unpack(x.float(), height, width)
    image = ae.decode(x)
```

> The function names and signatures above are illustrative of the typical FLUX API. Check `flux/sampling.py` and `flux/util.py` for the exact signatures in your version.

Saving the decoded tensor to disk requires converting it from `[-1, 1]` to `[0, 255]` uint8. The CLI handles this for you.

---

## TensorRT Acceleration

The `flux/trt/` package builds TensorRT engines for the transformer, VAE, CLIP, and T5 components, which can significantly reduce inference latency on NVIDIA GPUs.

**Requirements:**
- TensorRT matching your CUDA and driver versions
- Sufficient disk space for engine files (several GB per component)

**Workflow:**
1. Enable TRT with the CLI flag (for example, `--trt`).
2. On the first run, `trt_manager.py` builds engines from the PyTorch weights. This takes several minutes.
3. Engines are cached and reused on later runs.

**Configuration:** Each component has its own config file (`*_trt_config.py`) that sets:
- Min, opt, and max input shapes (resolution and batch size)
- Precision (FP16, BF16, or FP8 where supported)
- Build options

If you change the resolution, you may need to rebuild engines whose shape profiles don't cover the new size. Build for the largest resolution you plan to use.

---

## Content Safety Filter

`content_filters.py` screens generated images before they are returned. When a output is flagged, the pipeline typically returns a blacked-out or placeholder image and logs a warning.

- The filter is enabled by default in the demos and CLIs in most configurations.
- To disable it for research or testing, look for a flag such as `--no_filter` or set the corresponding option in your configuration.

Do not rely on the filter as your only safeguard for public-facing deployments. Add your own moderation of prompts and outputs.

---

## Memory Optimization

If you run out of VRAM:

| Strategy | How |
|---|---|
| Use schnell instead of dev | Requires fewer steps and less memory. |
| Enable CPU offloading | Use `--offload` or the equivalent option. Slower but uses much less VRAM. |
| Lower the resolution | Try 768×768 or 512×512 first. |
| Reduce the T5 max length | Shorter prompt embeddings use less memory. |
| Use bfloat16 or FP8 | Halves or quarters weight memory. |
| Run one model at a time | Unload models you aren't using. |
| Set allocator options | `export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` |

---

## Architecture Overview

FLUX uses the following pipeline:

```
Prompt ──► CLIP (pooled) ─┐
     └───► T5 (sequence) ─┤
                          ▼
Noise latent ──► Flow-matching transformer (double + single stream blocks)
                          │  (optional: LoRA, Redux/Kontext image tokens,
                          │   Fill mask tokens, control tokens)
                          ▼
                   Denoised latent ──► VAE decoder ──► Image
                                                        │
                                                        ▼
                                             Content filter ──► Output
```

Key ideas:

- **Rectified flow:** The model predicts a velocity field that moves noise toward the data distribution along near-straight paths. This lets schnell produce good images in very few steps.
- **Dual-stream then single-stream blocks:** Text and image tokens are first processed in separate streams, then concatenated for joint attention.
- **Rotary positional embeddings:** Implemented in `math.py` and `layers.py`.
- **Conditioning via tokens:** Redux, Kontext, and control signals are encoded as extra tokens that the transformer attends to, rather than through a separate network.

---

## Troubleshooting

**`CUDA out of memory`**
Use `--offload`, lower the resolution, or switch to schnell. See [Memory Optimization](#memory-optimization).

**`401 Unauthorized` or `GatedRepoError` when downloading**
You haven't accepted the model license on Hugging Face, or your token is missing or invalid. Accept the terms on the model page and run `huggingface-cli login`.

**Black or blank images**
The content filter may have flagged the output. Check the logs. Also confirm you're using a supported dtype (bfloat16 is recommended on Ampere and newer GPUs).

**Image dimensions error**
Width and height must be multiples of 16. Resize your input images to match.

**Mask results look inverted (Fill)**
Confirm that white marks the region to regenerate. Some tools export masks with the opposite convention.

**TensorRT build fails**
Check that your TensorRT version matches your CUDA version. Delete the partial engine directory and rebuild. Make sure the requested shapes fit within the profile limits in the `*_trt_config.py` files.

**Slow first generation**
Model loading and, with TRT, engine building dominate the first run. Later runs are much faster.

**`ModuleNotFoundError`**
Reinstall in editable mode with `pip install -e .`, and make sure your virtual environment is active.

---

## Development

### Running from source

All commands work from the repository root with the package installed in editable mode.

### Code layout tips

- To add a new task, create a new `cli_*.py` module following the pattern of `cli.py`, and register it in the entry point.
- To add a new conditioning type, extend `image_embedders.py` and the token preparation in `sampling.py`.
- To support a new LoRA, follow the loading logic in `lora.py`.
- To add a TensorRT component, mirror one of the existing `*_engine.py` and `*_trt_config.py` pairs.

### Formatting and linting

If the project includes linting configuration in `pyproject.toml`, run the configured tools before submitting changes:

```bash
ruff check .
ruff format .
```

---

## License

This repository contains code under multiple licenses:

- **Repository code:** See `LICENSE`.
- **FLUX.1 [schnell]:** Apache 2.0. See `LICENSE-FLUX1-schnell`.
- **FLUX.1 [dev] and derived models (Fill, Depth, Canny, Redux, Kontext):** FLUX.1 [dev] Non-Commercial License. See `LICENSE-FLUX1-dev`. Commercial use requires a separate license from the model provider.

Read the applicable license before using the models or their outputs.

---

## Citation

If you use FLUX in your research, please cite the technical report:

```bibtex
@misc{flux2024,
  title  = {FLUX.1: Rectified Flow Transformers for High-Resolution Image Synthesis},
  author = {Black Forest Labs},
  year   = {2024},
  howpublished = {\url{https://github.com/black-forest-labs/flux}}
}
```

---

## Acknowledgments

FLUX builds on prior work in rectified flow, diffusion transformers, and the open-source ecosystem around PyTorch, Hugging Face, and TensorRT. Sample images in this repository are provided for demonstration purposes.

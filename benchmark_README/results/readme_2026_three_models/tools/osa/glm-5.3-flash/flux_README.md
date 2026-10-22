# flux-enr7z850

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project is an image-generation toolkit built around the FLUX family of flow-matching transformer models, supporting tasks such as text-to-image synthesis, image editing and variation, and structure-conditioned generation. It is written in Python and targets ML researchers and developers working with generative image models, as well as engineers deploying or optimizing inference. The repository provides a command-line interface, a Python API for direct model use, interactive demo applications, and an optional accelerated inference backend. See the Getting Started section for installation and runnable steps.

---

## Core Features

- **Text-to-image generation** via a multi-command CLI and Python API, with interactive prompt-driven sessions that let you adjust resolution, seed, guidance, and step count on the fly.
- **Inpainting and image editing** through fill and kontext workflows, enabling generation inside masked regions and instruction-guided edits of existing images.
- **Structurally conditioned generation** with canny and depth control as well as redux-based image variations, so outputs can follow a reference image's composition or content.
- **Flexible inference backends** including a PyTorch path with model offloading for lower-memory setups and an optional TensorRT backend for accelerated serving.
- **Ready-to-use demo frontends** (Gradio-based, with interactive model loading and generation controls) for experimenting without writing code.

---

## Installation

**Prerequisites:** requires Python >=3.10

Install from a local checkout of the repository; packaging is defined in `setup.py` and `pyproject.toml`:

```sh
pip install .
```

---

## Getting Started

**Prerequisites**

- A completed [Installation](#installation) of the package and its dependencies.
- A CUDA-capable GPU is recommended: the CLI automatically uses `cuda` when available and falls back to `cpu`.

**Steps**

1. Make the model weights available. They are downloaded automatically to `checkpoints/` from HuggingFace when you start a demo. To use locally downloaded weights instead, place them in `checkpoints/` or point to them with environment variables:

```bash
    export FLUX_MODEL=<your model path here>
    export FLUX_AE=<your autoencoder path here>
```

2. Generate your first image with the text-to-image command:

```bash
    python -m flux t2i --name flux-schnell
```

    `flux-schnell` is the default model; `--name` also accepts `flux-dev`. Images are saved to `output/`. Customize with flags such as `--prompt`, `--width`, `--height`, `--seed`, and `--num_steps`, or add `--loop` for an interactive session where size, seed, guidance, and step count can be changed between samples.

3. Explore the other tasks exposed by the same CLI: the subcommands `control`, `fill`, `kontext`, and `redux` (for example, `python -m flux kontext --loop` for interactive image editing). Worked examples are shown in the [Examples](#examples) section, and per-task flags are covered in `docs/`.

4. Optionally run an interactive frontend: a Gradio demo is provided in `demo_gr.py` (interactive model loading and generation controls). A Streamlit fill demo may also be available as `demo_st_fill.py`; if present in your checkout, start it with:

```bash
    streamlit run demo_st_fill.py
```

---

## Examples

All examples use the CLI exposed as `python -m flux <command>` (see [API Reference](#api-reference)); on memory-constrained setups, the CLI supports the `--offload` flag to keep model components on CPU when they are not in use.

**Text-to-image** with the default model:

```bash
python -m flux t2i --name flux-schnell
```

Images are saved to `output/`. With explicit parameters (the default size is 1360x768; width and height must be multiples of 16):

```bash
python -m flux t2i --name flux-dev --prompt "a photograph of a mountain at sunrise" --width 1360 --height 768 --seed 42
```

**Interactive session**, where resolution, seed, guidance, and step count can be changed between samples:

```bash
python -m flux t2i --loop
```

**Instruction-guided image editing:**

```bash
python -m flux kontext --loop
```

**Other tasks** — `control` (canny/depth-conditioned generation), `fill` (inpainting and masked generation), and `redux` (image variation) — are invoked the same way (`python -m flux <command>`). Their task-specific parameters are defined in the corresponding `flux.cli_*` modules and covered in `docs/`.

For the interactive demo frontends (Gradio and Streamlit), see step 4 in [Getting Started](#getting-started).

---

## Architecture

The codebase is a monolithic Python package (`src/flux`) built around the FLUX family of flow-matching transformer models, with a multi-command CLI and optional TensorRT-accelerated inference.

- **Entry points**: `python -m flux` exposes subcommands via Python Fire — `t2i`, `control`, `fill`, `kontext`, and `redux` (defined in `src/flux/__main__.py`, each backed by a `cli_*.py` module). Standalone demo frontends (`demo_gr.py` for Gradio) wrap the same core components.
- **Core model**: `src/flux/model.py` defines the `Flux` transformer (double-stream and single-stream blocks, positional embedding, guidance embedding) parameterized by `FluxParams`. LoRA adaptation is supported via `FluxLoraWrapper` and `flux.modules.lora`.
- **Model modules**: `src/flux/modules/` contains the `AutoEncoder` (VAE for latent encoding/decoding), `HFEmbedder` text conditioners (T5 and CLIP, loaded via `flux.util`), and image embedders (`CannyImageEncoder`, `DepthImageEncoder`, `ReduxImageEncoder`) used for structural conditioning and redux.
- **Sampling pipeline**: `src/flux/sampling.py` implements the shared generation flow — noise generation (`get_noise`), prompt/image preparation (`prepare`, `prepare_control`, `prepare_fill`, `prepare_redux`), and iterative denoising (`denoise`). Task-specific preparation functions encode conditioning images or masks with the autoencoder before feeding them to the transformer.
- **CLI orchestration**: the CLI modules load the required components (T5, CLIP, flow model, autoencoder) through helpers in `flux.util`, run sampling, apply an NSFW content filter (`flux.content_filters`, Transformers image-classification pipeline), and save output images. Model offloading to CPU is supported via the `offload` flag.
- **Optional TensorRT backend**: `src/flux/trt/` provides engines for each component (`clip_engine`, `t5_engine`, `transformer_engine`, `vae_engine`), matching TRT config classes, and a `trt_manager` for engine building/execution. It is lazily imported so the TensorRT dependency is optional.

In short, control flows from the CLI or demo frontend into sampling utilities, which coordinate the text conditioners, image embedders, the Flux transformer, and the autoencoder to produce images — with the TensorRT subsystem serving as a drop-in accelerated path for the same components.

---

## API Reference

The stable usage surface is the Fire-based CLI exposed via `python -m flux`, plus the Python modules under `src/flux` used by the CLI and demo apps.

**CLI commands** (`src/flux/__main__.py`, run as `python -m flux <command>`):

| Command | Target |
| --- | --- |
| `t2i` | `flux.cli.main` |
| `control` | `flux.cli_control.main` |
| `fill` | `flux.cli_fill.main` |
| `kontext` | `flux.cli_kontext.main` |
| `redux` | `flux.cli_redux.main` |

**`flux.cli`** — text-to-image entry point:

| Symbol | Purpose |
| --- | --- |
| `SamplingOptions` | Dataclass holding `prompt`, `width`, `height`, `num_steps`, `guidance`, `seed`. |
| `parse_prompt(options: SamplingOptions)` | Interactive loop that updates options via slash commands (`/w`, `/h`, `/s`, `/g`, `/n`); returns `None` on `/q`. |
| `main(...)` | Generates images (single run or interactive with `loop=True`). Parameters include `name` (default `"flux-schnell"`), `width`/`height` (defaults 1360/768, multiples of 16 enforced), `seed`, `prompt` (`|` separates additional prompts), `device`, `num_steps` (4 for schnell, 50 otherwise), `guidance`, `offload`, `output_dir`, `add_sampling_metadata`, `trt`, `trt_transformer_precision`, `track_usage`. |

**`flux.sampling`** — sampling utilities shared by the CLI and demos:

| Symbol | Purpose |
| --- | --- |
| `get_noise(num_samples, height, width, device, dtype, seed)` | Creates the seeded initial latent noise tensor. |
| `prepare(t5, clip, img, prompt)` | Packs the image and T5/CLIP text embeddings into a dict (`img`, `img_ids`, `txt`, `txt_ids`, `vec`). |
| `prepare_control(t5, clip, img, prompt, ae, encoder, img_cond_path)` | Adds an encoded conditioning image (`img_cond`) via a depth/canny image encoder. |
| `prepare_fill(t5, clip, img, prompt, ae, img_cond_path, mask_path)` | Adds `img_cond` combining the conditioning image and mask for fill/inpainting. |
| `prepare_redux(t5, clip, img, prompt, encoder, img_cond_path)` | Adds `img_cond` encoded with `ReduxImageEncoder`. |
| `denoise`, `get_schedule`, `unpack` | Additional sampling helpers exported by this module and used by the CLI and demos. |

**`flux.model`** — transformer definition:

| Symbol | Purpose |
| --- | --- |
| `FluxParams` | Dataclass describing transformer configuration (in/out channels, hidden size, heads, block depths, axes dims, `guidance_embed`). |
| `Flux(params: FluxParams)` | Flow-matching transformer; `forward(img, img_ids, txt, txt_ids, timesteps, y, guidance=None)` validates 3D inputs and returns the output tensor. `guidance` is required when `guidance_embed` is set. |
| `FluxLoraWrapper(lora_rank=128, lora_scale=1.0, ...)` | `Flux` subclass with linear layers replaced by LoRA; `set_lora_scale(scale)` adjusts the scale at runtime. |

**`flux.util`** — model loading and output helpers (imported by the CLI and demos):

| Symbol | Purpose |
| --- | --- |
| `configs` | Registry of known model names; `cli.main` validates `name` against its keys. |
| `load_flow_model(name, device=...)` | Loads the FLUX transformer (placed on CPU when offloading). |
| `load_t5(device, max_length=...)` | Loads the T5 text encoder (max length 256 for `flux-schnell`, 512 otherwise). |
| `load_clip(device)` | Loads the CLIP text encoder. |
| `load_ae(name, device=...)` | Loads the autoencoder. |
| `save_image` | Saves output images. |
| `embed_watermark`, `track_usage_via_api` | Watermarking of outputs and usage tracking (used by `demo_gr.py`). |
| `check_onnx_access_for_trt` | Access check used by the TensorRT path. |

The TensorRT backend (`flux.trt`, e.g. `trt_manager`) is lazy-imported by `cli.main` when `trt=True`, so it is an optional dependency.

**Gradio demo** (`demo_gr.py`):

| Symbol | Purpose |
| --- | --- |
| `FluxGenerator(model_name, device, offload, track_usage)` | Loads all models once at init; `generate_image(width, height, num_steps, guidance, seed, prompt, init_image=None, image2image_strength=0.0, add_sampling_metadata=True)` produces images (seed `-1` means random). |

---

## Documentation

The main in-repo references are the [Getting Started](#getting-started), [Examples](#examples), and [API Reference](#api-reference) sections. Additional project documentation — including per-task CLI flags and worked examples — is located in the [`docs/`](./docs) directory.

---

## Contributing

Contributions are welcome. Please open an issue first to report bugs or discuss proposed changes. Keep pull requests focused on a single change, compatible with the supported Python version (see [Installation](#installation)), and update the related documentation (for example, the [Examples](#examples) or [API Reference](#api-reference) sections) when behavior or usage changes.

---

## License

A `LICENSE` file is included in this repository; refer to [LICENSE](./LICENSE) for the applicable license terms.

---

## Citation

If you use this project in your work, cite it using the templates below, replacing `<AUTHOR>`, `<YEAR>`, and `<REPOSITORY_URL>` with the project's actual attribution details and canonical repository URL.

### APA format:

    <AUTHOR> (<YEAR>). flux-enr7z850 repository [Computer software]. <REPOSITORY_URL>

### BibTeX format:

    @misc{flux-enr7z850,

        author = {<AUTHOR>},

        title = {flux-enr7z850 repository},

        year = {<YEAR>},

        note = {Repository URL: <REPOSITORY_URL>}

    }

---

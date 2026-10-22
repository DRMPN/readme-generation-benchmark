# FLUX

Inference codebase for FLUX, a family of rectified flow transformers for text-to-image generation and related image editing tasks. The package provides a command-line interface, Streamlit and Gradio demos, optional TensorRT acceleration, and reference sampling code for the released FLUX.1 models.

## Overview

The repository includes:

- **Text-to-image** generation with `FLUX.1 [schnell]` and `FLUX.1 [dev]`.
- **Inpainting and outpainting** with `FLUX.1 Fill [dev]`.
- **Structural conditioning** (canny edge and depth) with `FLUX.1 Canny [dev]` and `FLUX.1 Depth [dev]`, each with a LoRA variant.
- **Image variations** with `FLUX.1 Redux [dev]`, an adapter for the base models.
- **Instruction-based image editing** with `FLUX.1 Kontext [dev]`.
- **Optional TensorRT backends** for BF16, FP8, and FP4 transformer precisions.

The Python package is named `flux` and requires Python 3.10 or newer. Its description in `pyproject.toml` is "Inference codebase for FLUX."

Each model family has a dedicated document in `docs/`, and model cards are in `model_cards/`.

| Model | CLI command | Documentation |
| --- | --- | --- |
| `FLUX.1 [schnell]`, `FLUX.1 [dev]` | `python -m flux t2i` | `docs/text-to-image.md` |
| `FLUX.1 Fill [dev]` | `python -m flux fill` | `docs/fill.md` |
| `FLUX.1 Canny [dev]`, `FLUX.1 Depth [dev]` (and LoRAs) | `python -m flux control` | `docs/structural-conditioning.md` |
| `FLUX.1 Redux [dev]` | `python -m flux redux` | `docs/image-variation.md` |
| `FLUX.1 Kontext [dev]` | `python -m flux kontext` | `docs/image-editing.md` |

## Installation

The project is packaged with setuptools and uses `setuptools_scm` for its version. Install it from a clone of the repository. Optional dependencies are defined as extras in `pyproject.toml`:

| Extra | Contents |
| --- | --- |
| `torch` | `torch==2.6.0`, `torchvision` |
| `streamlit` | `streamlit`, `streamlit-drawable-canvas`, `streamlit-keyup` |
| `gradio` | `gradio` |
| `tensorrt` | `tensorrt-cu12==10.12.0.36`, `onnx`, `onnxruntime`, `onnxruntime-gpu`, `onnx-graphsurgeon`, `polygraphy`, and related packages |
| `all` | `gradio`, `streamlit`, and `torch` extras |

Core dependencies include `accelerate`, `einops`, `fire`, `huggingface-hub`, `safetensors`, `sentencepiece`, `transformers>=4.45.2`, `tokenizers`, `protobuf`, `requests`, and `invisible-watermark`.

A typical editable install with all optional components:

```bash
git clone <repository-url>
cd <repository-directory>
pip install -e ".[all]"
```

For TensorRT support, install the `tensorrt` extra as well:

```bash
pip install -e ".[torch,tensorrt]"
```

The TensorRT documentation notes that the repository must be installed with TensorRT support, and the TensorRT engine builds depend on `polygraphy`.

## Model Weights

Weights are downloaded automatically from HuggingFace into `checkpoints/` the first time you run one of the demos or commands. You can also download them manually into `checkpoints/`, or point to existing files with environment variables:

```bash
export FLUX_MODEL=<path to flow model>     # e.g. flux1-dev.safetensors
export FLUX_AE=<path to autoencoder>
export FLUX_REDUX=<path to redux adapter> # Redux only
export FLUX_LORA=<path to LoRA>           # optional, Canny/Depth LoRA variants
```

If an environment variable points to a file that does not exist, the code prints a warning and falls back to the default location.

Some repositories are gated. The loader calls `ensure_hf_auth()`, which uses the `HF_TOKEN` environment variable if set, or an existing HuggingFace login. If a download fails because the repository is gated, the code prompts for a token interactively.

The following HuggingFace model repositories are referenced in the code and docs:

- `black-forest-labs/FLUX.1-schnell`, `FLUX.1-dev`, `FLUX.1-Fill-dev`, `FLUX.1-Redux-dev`, `FLUX.1-Canny-dev`, `FLUX.1-Depth-dev`, `FLUX.1-Kontext-dev`, and the LoRA repositories for Canny and Depth.
- Auxiliary models: `google/t5-v1_1-xxl`, `openai/clip-vit-large-patch14`, `Falconsai/nsfw_image_detection`, `LiheYoung/depth-anything-large-hf`, `google/siglip-so400m-patch14-384`, and `mistral-community/pixtral-12b` (used by the Kontext content filter).

## Usage

### Command-line interface

Run the CLI through the `flux` package:

```bash
python -m flux <command> [options]
```

Available commands are `t2i`, `control`, `fill`, `kontext`, and `redux`. Options are parsed with Fire, so each command's arguments mirror the Python function signatures in `src/flux/cli_*.py`.

**Text-to-image**

```bash
# Interactive session
python -m flux t2i --name flux-dev --loop

# Single image
python -m flux t2i --name flux-schnell \
  --height 768 --width 1360 \
  --prompt "a photo of a forest with mist swirling around the tree trunks"
```

The `t2i` command accepts `flux-dev` or `flux-schnell`. The default number of steps is 4 for `flux-schnell` and 50 otherwise. In the main prompt, `|` separates additional prompts for batch-style sequential generation.

**Structural conditioning**

```bash
python -m flux control --name flux-dev-canny --loop
```

Valid names are `flux-dev-canny`, `flux-dev-depth`, `flux-dev-canny-lora`, and `flux-dev-depth-lora`. The default conditioning image is `assets/robot.webp`.

**Inpainting and outpainting**

```bash
python -m flux fill --loop

python -m flux fill \
  --img_cond_path <path_to_input_image> \
  --img_mask_path <path_to_input_mask>
```

The mask must have the same size as the conditioning image and contain only black and white pixels. Both dimensions must be divisible by 32. The default inputs are `assets/cup.png` and `assets/cup_mask.png`.

**Image variations (Redux)**

```bash
python -m flux redux --name flux-dev --loop
```

The `--name` option accepts `flux-dev` or `flux-schnell`.

**Editing (Kontext)**

```bash
python -m flux kontext --loop

python -m flux kontext \
  --img_cond_path <path_to_input_image> \
  --prompt <your_prompt> \
  --num_steps 30 --aspect_ratio "16:9" --guidance 2.5 --seed 1
```

`--aspect_ratio` is optional. When omitted, the output uses the input image's resolution, snapped to one of the preferred Kontext resolutions.

Interactive sessions (`--loop`) accept slash commands. For text-to-image, these include `/w <width>`, `/h <height>`, `/s <seed>`, `/g <guidance>`, `/n <steps>`, and `/q`. Kontext uses `/ar <width>:<height>` in place of `/w` and `/h`, and the other commands are similar.

### Demo applications

**Gradio**

```bash
python demo_gr.py --name flux-schnell --device cuda
```

Options: `--name` (`flux-schnell` or `flux-dev`), `--device` (defaults to CUDA when available, otherwise CPU), `--offload` (move models to CPU when not in use), `--share` (create a public link), and `--track_usage`.

**Streamlit**

```bash
streamlit run demo_st.py       # text-to-image and image-to-image
streamlit run demo_st_fill.py  # inpainting and outpainting
```

The Streamlit text-to-image demo accepts `device`, `offload`, `output_dir`, and `track_usage` parameters.

### Python library

`FLUX.1 [schnell]` and `FLUX.1 [dev]` are also integrated with the HuggingFace `diffusers` library, which the docs show with `FluxPipeline`. Flux Control, including the LoRAs, is documented as compatible with `diffusers` as well.

## Configuration

### Command-line options and defaults

| Command | Notable defaults |
| --- | --- |
| `t2i` | `name=flux-schnell`, `width=1360`, `height=768`, `guidance=2.5`, `output_dir=output` |
| `control` | `width=1024`, `height=1024`, `num_steps=50`, `lora_scale=0.85`; guidance 30.0 for Canny and 10.0 for Depth when unspecified |
| `fill` | `num_steps=50`, `guidance=30.0`, prompt `"a white paper cup"` |
| `kontext` | `num_steps=30`, `guidance=2.5`, `aspect_ratio=None` |
| `redux` | `name=flux-dev`, `width=1360`, `height=768`, `guidance=2.5` |

Common options across commands include `device`, `offload`, `output_dir`, `seed`, `loop`, `add_sampling_metadata`, `track_usage`, and, for TensorRT-enabled commands, `trt` and `trt_transformer_precision`.

### Environment variables

| Variable | Purpose |
| --- | --- |
| `HF_TOKEN` | HuggingFace token used for authentication, including for gated repositories |
| `BFL_API_KEY` | Required when `track_usage` is enabled; used to report usage to the BFL licensing API |
| `FLUX_MODEL`, `FLUX_AE`, `FLUX_REDUX`, `FLUX_LORA` | Local paths for model checkpoints |
| `TRT_ENGINE_DIR` | TensorRT engine directory. If unset, `checkpoints/trt_engines` is used |
| `TRT_T5_PRECISION` | T5 precision for TensorRT: `bf16` (default) or `fp8` |
| `TRT_TIMING_CACHE_FILE` | Optional TensorRT timing cache file |
| `CUSTOM_ONNX_PATHS` | Optional custom ONNX paths, in `module:path` comma-separated form |
| `TRT_ALLOCATION_POLICY` | `global` (default) or `dynamic` |

### TensorRT

The TensorRT backend is enabled with `--trt`. The transformer precision is set with `--trt_transformer_precision`, which accepts `bf16`, `fp8`, `fp4`, or `fp4_sdvd32` in the documentation (the manager accepts `fp4_svd32` and maps it to `fp4`). Engines are built from ONNX exports downloaded from HuggingFace (`black-forest-labs/FLUX.1-*-onnx` repositories) or from custom paths. Text-to-image with ONNX exports requires height and width between 768 and 1344. The LoRA variants do not support TensorRT.

### Outputs and safety features

- Generated images are saved to `output/` as `img_{idx}.jpg`, with the index continuing from existing files. Gradio saves to `output/gradio/`.
- Images are saved as JPEG with EXIF metadata including the software tag, manufacturer, and model name. The prompt is stored in the image description when `add_sampling_metadata` is enabled.
- Every output is passed through an invisible watermark (`invisible-watermark`, `dwtDct` method).
- A NSFW classifier (`Falconsai/nsfw_image_detection`) scores outputs. Images with a score at or above 0.85 are not saved, and a warning is printed.
- The Kontext CLI runs a content filter (Pixtral-based) on prompts and input and output images, and reports when content is flagged.
- The Kontext CLI also writes an intermediate tensor file to `output/noise.sft` during sampling.

## Development

Dependencies and tool settings are defined in `pyproject.toml`:

- **Ruff** (`ruff==0.6.8`) is the linter and formatter. Line length is 110, the target version is `py310`, and quotes are double-quoted. The E501 rule is ignored, and isort settings treat `flux` as first-party and `src` as a local folder.
- **Pyright** type checking is configured for `src`, with stubs in `./typings`.
- **toml-sort** is configured for `pyproject.toml`.

Run the same checks as CI from the repository root:

```bash
pip install ruff==0.6.8
ruff check .
ruff check --select I .
ruff format --check .
```

The GitHub Actions workflow (`.github/workflows/ci.yaml`) runs on every push. It installs Ruff on Python 3.10 on Ubuntu, then runs the lint, import-order, and formatting checks listed above.

The repository contains TensorRT modules adapted from NVIDIA's demo code (headers in `src/flux/trt/` indicate Apache-2.0 licensing). Engine build and runtime logic is organized into `trt/engine/` (runtime engines), `trt/trt_config/` (per-module build configuration), and `trt/trt_manager.py` (orchestration).

## Testing

The repository does not include a test suite, and no test files or test configuration appear in the file tree. The CI workflow performs linting and formatting checks only. To verify changes, run the CLI commands or demos described above with a model and input of your choice.

## Limitations and Responsible Use

The model cards list these limitations for the FLUX.1 models:

- The models are not intended or able to provide factual information.
- As statistical models, they might amplify existing societal biases.
- They may fail to generate output matching the prompt.
- Prompt following is heavily influenced by prompting style.

The model cards also list out-of-scope uses, including unlawful activity, content that exploits minors, non-consensual intimate imagery, harassment, fully automated decisions that adversely affect individuals' legal rights, and large-scale disinformation campaigns.

## License

The source code is released under the **Apache License, Version 2.0** (see `LICENSE`).

Model weights are governed by separate licenses in `model_licenses/`:

- `FLUX.1 [schnell]` is released under **Apache-2.0** (`model_licenses/LICENSE-FLUX1-schnell`).
- `FLUX.1 [dev]` and the dev-based models (Fill, Redux, Canny, Depth, their LoRAs, and Kontext) are released under the **FLUX.1-dev Non-Commercial License** (`model_licenses/LICENSE-FLUX1-dev`).

Generated outputs from the dev models may be used for personal, scientific, and commercial purposes under the terms described in the model cards. Commercial use of the dev models is subject to the usage-tracking requirements referenced in `track_usage_via_api`, which posts usage to the BFL licensing API using `BFL_API_KEY`. Review the license files before use.

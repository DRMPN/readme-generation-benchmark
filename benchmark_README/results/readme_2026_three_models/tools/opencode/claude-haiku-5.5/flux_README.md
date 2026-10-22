# FLUX

Inference code for the FLUX.1 family of rectified-flow image models from Black Forest Labs. The repository provides a command-line interface, two demo apps (Gradio and Streamlit), and TensorRT support for optimized inference. It contains inference code only; no training code is included.

## Supported models

| Model | How to run it | Hugging Face repo | License |
| --- | --- | --- | --- |
| FLUX.1 [schnell] | `t2i --name flux-schnell` | `black-forest-labs/FLUX.1-schnell` | Apache-2.0 |
| FLUX.1 [dev] | `t2i --name flux-dev` | `black-forest-labs/FLUX.1-dev` | FLUX.1 [dev] Non-Commercial |
| FLUX.1 Fill [dev] (inpainting / outpainting) | `fill` | `black-forest-labs/FLUX.1-Fill-dev` | FLUX.1 [dev] Non-Commercial |
| FLUX.1 Canny [dev] | `control --name flux-dev-canny` | `black-forest-labs/FLUX.1-Canny-dev` | FLUX.1 [dev] Non-Commercial |
| FLUX.1 Depth [dev] | `control --name flux-dev-depth` | `black-forest-labs/FLUX.1-Depth-dev` | FLUX.1 [dev] Non-Commercial |
| FLUX.1 Canny [dev] LoRA | `control --name flux-dev-canny-lora` | `black-forest-labs/FLUX.1-Canny-dev-lora` (applied to FLUX.1 [dev]) | FLUX.1 [dev] Non-Commercial |
| FLUX.1 Depth [dev] LoRA | `control --name flux-dev-depth-lora` | `black-forest-labs/FLUX.1-Depth-dev-lora` (applied to FLUX.1 [dev]) | FLUX.1 [dev] Non-Commercial |
| FLUX.1 Redux [dev] (image variations) | `redux --name flux-dev` or `flux-schnell` | `black-forest-labs/FLUX.1-Redux-dev` | FLUX.1 [dev] Non-Commercial |
| FLUX.1 Kontext [dev] (instruction-based editing) | `kontext` | `black-forest-labs/FLUX.1-Kontext-dev` | FLUX.1 [dev] Non-Commercial |

The sha256 checksums for each open-weight file are listed in `docs/`.

## Requirements

- Python 3.10 or newer.
- PyTorch. `torch` is an optional extra rather than a core dependency, so install it with the `torch` extra or install it yourself. The extra pins `torch == 2.6.0`.
- The default device is `cuda` when CUDA is available and `cpu` otherwise. The repository does not document hardware requirements.
- Access to Hugging Face. Weights are downloaded automatically. Some repositories may require accepting a license on Hugging Face and authenticating (see [Authentication](#authentication-and-environment-variables)).

## Installation

Clone the repository and install it from the project root. `pyproject.toml` defines these optional extras:

| Extra | Installs |
| --- | --- |
| `torch` | `torch==2.6.0`, `torchvision` |
| `gradio` | `gradio` |
| `streamlit` | `streamlit`, `streamlit-drawable-canvas`, `streamlit-keyup` |
| `tensorrt` | TensorRT and related tooling (`tensorrt-cu12==10.12.0.36`, `onnx`, `onnxruntime-gpu`, `onnx-graphsurgeon`, `polygraphy`, and others) |
| `all` | `gradio`, `streamlit`, and `torch` (does not include `tensorrt`) |

```bash
pip install -e ".[torch]"
```

Add extras as needed, for example `pip install -e ".[torch,gradio,streamlit]"`. For TensorRT, see [TensorRT inference](#tensorrt-inference).

The `flux` console script declared in `pyproject.toml` does not currently work (see [Known issues](#known-issues)). Run the CLI with `python -m flux` instead.

## Authentication and environment variables

Some model downloads and the usage-tracking feature need credentials. The code reads these environment variables:

| Variable | Purpose |
| --- | --- |
| `HF_TOKEN` | Hugging Face token. Used to log in when a download needs authentication. If it is unset, the code falls back to an existing `huggingface-cli login` token or prompts for one on gated-repository errors. |
| `BFL_API_KEY` | Black Forest Labs API key. Required when `--track_usage` is enabled. |
| `FLUX_MODEL` | Path to a local base model `.safetensors` file. Skips the download for the flow model. |
| `FLUX_AE` | Path to a local autoencoder `.safetensors` file. |
| `FLUX_LORA` | Path to a local LoRA `.safetensors` file (used by the `*-lora` control models). |
| `FLUX_REDUX` | Path to a local Redux `.safetensors` file. |
| `TRT_ENGINE_DIR` | Directory for TensorRT engines. Defaults to `checkpoints/trt_engines`. |
| `CUSTOM_ONNX_PATHS` | Custom ONNX model paths for TensorRT, as comma-separated `module:path` pairs. |
| `TRT_T5_PRECISION` | TensorRT precision for the T5 text encoder: `bf16` (default) or `fp8`. |
| `TRT_TIMING_CACHE_FILE` | Optional TensorRT timing cache file. |
| `TRT_ALLOCATION_POLICY` | TensorRT memory allocation policy: `global` (default) or `dynamic`. |

If a path in `FLUX_MODEL`, `FLUX_AE`, `FLUX_LORA`, or `FLUX_REDUX` does not exist, the code prints a warning and falls back to downloading the file.

## Model weights

Weights download automatically from Hugging Face on first use and are stored under `checkpoints/`, in a folder named after the repo (`/` replaced by `_`), for example:

```
checkpoints/black-forest-labs_FLUX.1-dev/flux1-dev.safetensors
```

You can also download weights manually into `checkpoints/` or point the environment variables above at your own files. Importing `flux.util` creates `checkpoints/` in the current working directory.

Other components are loaded from Hugging Face by name:

- Text encoders: `google/t5-v1_1-xxl` and `openai/clip-vit-large-patch14`.
- NSFW classifier: `Falconsai/nsfw_image_detection`, used on every generated image.
- Kontext content filter: `mistral-community/pixtral-12b`, used by the `kontext` command.

## Quick start

Interactive text-to-image with FLUX.1 [schnell]:

```bash
python -m flux t2i --name flux-schnell --loop
```

Single image with FLUX.1 [dev]:

```bash
python -m flux t2i --name flux-dev --height 768 --width 1360 --prompt "a red fox in the snow"
```

Images are written to `output/` as `img_0.jpg`, `img_1.jpg`, and so on. The index continues from any existing files in the directory.

## Command-line interface

The CLI has five subcommands:

```bash
python -m flux <subcommand> [options]
```

| Subcommand | Purpose |
| --- | --- |
| `t2i` | Text-to-image with `flux-schnell` or `flux-dev` |
| `control` | Canny or depth structural conditioning, with or without LoRA |
| `fill` | Inpainting and outpainting with FLUX.1 Fill [dev] |
| `redux` | Image variations with FLUX.1 Redux [dev] |
| `kontext` | Instruction-based image editing with FLUX.1 Kontext [dev] |

Options are parsed with [Fire](https://github.com/google/python-fire), so `--option value` and `--option=value` both work. Common options:

- `--output_dir` (default `output`): where to save images.
- `--device`: `cuda` or `cpu`.
- `--seed`: integer seed. If omitted, a random seed is chosen and printed.
- `--offload`: move models to CPU when they are not in use, to reduce GPU memory use.
- `--add_sampling_metadata` (default `True`): write the prompt into the image's EXIF metadata.
- `--track_usage`: report generations to the Black Forest Labs licensing API (see [Usage tracking](#usage-tracking)).
- `--loop`: start an interactive session instead of generating one image.

### `t2i`: text-to-image

| Option | Default | Notes |
| --- | --- | --- |
| `--name` | `flux-schnell` | `flux-schnell` or `flux-dev` |
| `--prompt` | a forest with mist and "FLUX" painted in red brush strokes | Separate several prompts with `\|` to generate one image per prompt in sequence. Not allowed together with `--loop`. |
| `--width`, `--height` | `1360`, `768` | Rounded down to a multiple of 16 |
| `--num_steps` | `4` for schnell, `50` for dev | |
| `--guidance` | `2.5` | Guidance value for guidance-distilled sampling |
| `--trt` | `False` | Use TensorRT engines |
| `--trt_transformer_precision` | `bf16` | `bf16`, `fp8`, `fp4`, or `fp4_svd32` |

In `--loop` mode, type a prompt to generate. Press Enter with an empty prompt to repeat the last one. Slash commands:

- `/w <width>` and `/h <height>`: set the resolution.
- `/s <seed>`: set the seed for the next image.
- `/g <guidance>`: set guidance (meaningful for `flux-dev`).
- `/n <steps>`: set the number of sampling steps.
- `/q`: quit.

### `control`: canny and depth conditioning

| Option | Default | Notes |
| --- | --- | --- |
| `--name` | required | `flux-dev-canny`, `flux-dev-depth`, `flux-dev-canny-lora`, or `flux-dev-depth-lora` |
| `--prompt` | `a robot made out of gold` | |
| `--img_cond_path` | `assets/robot.webp` | Conditioning image (`.jpg`, `.jpeg`, `.png`, or `.webp`) |
| `--width`, `--height` | `1024`, `1024` | |
| `--num_steps` | `50` | |
| `--guidance` | `30.0` for canny, `10.0` for depth | |
| `--lora_scale` | `0.85` | Used by the `*-lora` variants only |
| `--trt` | `False` | Not supported with the LoRA variants |

In `--loop` mode you can also change the conditioning image and, for LoRA variants, the LoRA scale.

Example:

```bash
python -m flux control --name flux-dev-canny --img_cond_path assets/robot.webp --prompt "a robot made out of gold"
```

### `fill`: inpainting and outpainting

| Option | Default | Notes |
| --- | --- | --- |
| `--prompt` | `a white paper cup` | |
| `--img_cond_path` | `assets/cup.png` | Input image |
| `--img_mask_path` | `assets/cup_mask.png` | Mask with the same size as the input image, containing only black and white pixels. The Streamlit demo treats white as the region to fill. |
| `--num_steps` | `50` | |
| `--guidance` | `30.0` | |

Image dimensions must be divisible by 32. In `--loop` mode, the CLI checks that the mask matches the image size.

```bash
python -m flux fill --img_cond_path assets/cup.png --img_mask_path assets/cup_mask.png --prompt "a white paper cup"
```

### `redux`: image variations

| Option | Default | Notes |
| --- | --- | --- |
| `--name` | `flux-dev` | `flux-dev` or `flux-schnell` (base model) |
| `--img_cond_path` | `assets/robot.webp` | Image to create variations of |
| `--width`, `--height` | `1360`, `768` | |
| `--num_steps` | `4` for schnell, `50` for dev | |
| `--guidance` | `2.5` | |

```bash
python -m flux redux --name flux-dev --img_cond_path assets/robot.webp
```

The Redux command does not accept a text prompt (see [Known issues](#known-issues)).

### `kontext`: instruction-based editing

| Option | Default | Notes |
| --- | --- | --- |
| `--prompt` | `replace the logo with the text 'Black Forest Labs'` | Editing instruction |
| `--img_cond_path` | `assets/cup.png` | Image to edit |
| `--aspect_ratio` | not set | For example `16:9`. If omitted, the output uses the input image's size. |
| `--num_steps` | `30` | |
| `--guidance` | `2.5` | |
| `--trt` | `False` | Use TensorRT engines |
| `--trt_transformer_precision` | `bf16` | `bf16`, `fp8`, `fp4`, or `fp4_svd32` |

The `kontext` command only accepts `--name flux-dev-kontext`. Every prompt and input image is checked by a content filter, and generated outputs are also checked. Flagged content is rejected.

```bash
python -m flux kontext --img_cond_path assets/cup.png --prompt "make the cup blue" --num_steps 30 --aspect_ratio "16:9" --guidance 2.5 --seed 1
```

The kontext command also writes a `output/noise.sft` file on every run.

## Demo apps

### Gradio

Install the `gradio` extra, then run:

```bash
python demo_gr.py --name flux-schnell --device cuda
```

Options:

- `--name`: `flux-schnell` (default) or `flux-dev`.
- `--device`: `cuda` if available, otherwise `cpu`.
- `--offload`: move models to CPU when not in use.
- `--share`: create a public Gradio link.
- `--track_usage`: enable [usage tracking](#usage-tracking).

Gradio outputs are saved to `output/gradio/`. The demo supports text-to-image and, for `flux-dev`, image-to-image with a noising-strength slider.

### Streamlit

Install the `streamlit` extra, then run either demo:

```bash
streamlit run demo_st.py       # text-to-image and image-to-image
streamlit run demo_st_fill.py  # inpainting and outpainting with FLUX.1 Fill [dev]
```

`demo_st.py` lets you pick a model and load it. Image-to-image is only available for `flux-dev`. `demo_st_fill.py` provides a drawing canvas for inpainting and controls for outpainting borders.

## Output details

Each generated image is:

- Saved as a JPEG with quality 95 and no chroma subsampling.
- Watermarked with an invisible watermark (`invisible-watermark`, DWT-DCT method) before saving. The demos apply the same watermark.
- Tagged with EXIF metadata: the Software field starts with `AI generated;`, Make is `Black Forest Labs`, Model is the model name, and the prompt is stored in ImageDescription unless `--add_sampling_metadata` is disabled.

Images are checked with the `Falconsai/nsfw_image_detection` classifier. If the NSFW score is 0.85 or higher, the image is not saved and a message is printed.

## Usage tracking

With `--track_usage` (CLI or demos), each successful generation is reported to the Black Forest Labs licensing API. This requires `BFL_API_KEY` to be set. The code reports usage for `flux-dev`, `flux-dev-kontext`, `flux-dev-fill`, the Canny and Depth models and LoRAs, and `flux-dev-redux`. Other models, including `flux-schnell`, are not tracked. The code's docstring links to the licensing dashboard at `https://dashboard.bfl.ai/licensing/subscriptions?showInstructions=true`.

## TensorRT inference

TensorRT support is optional and requires:

- The `tensorrt` extra: `pip install -e ".[tensorrt]"`.
- A CUDA GPU. The code asserts that CUDA is available.
- Access to the FLUX ONNX repositories on Hugging Face (`black-forest-labs/FLUX.1-*-onnx`), which the code downloads into `checkpoints/`. These repositories may be gated.

Engines are built on first use with the `polygraphy` CLI and stored in `TRT_ENGINE_DIR` (default `checkpoints/trt_engines`). Later runs reuse existing engines.

```bash
python -m flux t2i --name flux-dev --loop --trt --trt_transformer_precision fp8
python -m flux control --name flux-dev-canny --loop --img_cond_path assets/robot.webp --trt --static_shape=False --trt_transformer_precision bf16
```

According to the repository docs, ONNX exports support heights and widths between 768 and 1344. The LoRA variants of `control` do not support `--trt`.

## Using the models with Diffusers

The docs in `docs/text-to-image.md` describe using FLUX.1 [schnell] and [dev] with Hugging Face's `diffusers` library (`FluxPipeline`). That path is separate from this repository's code. The docs say diffusers support needs the development version of `diffusers`, installed from GitHub. Flux Control and its LoRAs are also documented as diffusers-compatible in `docs/structural-conditioning.md`.

## Project layout

```
src/flux/
  cli.py              t2i command (and shared sampling options)
  cli_control.py      control command (canny / depth, LoRA)
  cli_fill.py         fill command (inpainting / outpainting)
  cli_redux.py        redux command (image variations)
  cli_kontext.py      kontext command (image editing)
  __main__.py         entry point for `python -m flux`
  sampling.py         noise, input preparation, schedule, and denoising
  util.py             model configs, checkpoint download, loaders, saving
  content_filters.py  Pixtral-based content filter (used by kontext)
  model.py            FLUX transformer
  modules/            building blocks (layers, autoencoder, conditioners, LoRA, image encoders)
  trt/                TensorRT configs, engine builders, and runtime
demo_gr.py            Gradio demo
demo_st.py            Streamlit demo (text-to-image / image-to-image)
demo_st_fill.py       Streamlit demo (inpainting / outpainting)
docs/                 per-feature usage notes and model tables
model_cards/          model cards for FLUX.1 [schnell], [dev], and Kontext [dev]
model_licenses/       license texts for the FLUX.1 [dev] and [schnell] weights
assets/               sample images used as defaults and in docs
```

## Development

Code style is enforced with Ruff (version 0.6.8). The settings are in `pyproject.toml`: line length 110, double quotes, and isort rules with `flux` as first-party. The GitHub Actions workflow in `.github/workflows/ci.yaml` runs on every push and checks:

```bash
ruff check .
ruff check --select I .
ruff format --check .
```

The repository does not include a test suite.

## Known issues

- The `flux` console script in `pyproject.toml` points to `flux.cli:app`, which does not exist. Use `python -m flux` instead.
- The Redux command has no text-prompt option, and its interactive `--loop` mode does not apply typed prompts, so generation uses an empty prompt.
- Both LoRA control models read the same `FLUX_LORA` variable, so a single path cannot be set for both the Canny and Depth LoRAs.
- `pyproject.toml` sets `license = { file = "LICENSE.md" }`, but the license file is named `LICENSE`.
- `ruff` is listed under runtime dependencies even though it is a development tool.
- `docs/structural-conditioning.md` shows `python flux control`, which is missing `-m`. The correct form is `python -m flux control`.

## License

The code in this repository is licensed under the Apache License 2.0 (see `LICENSE`).

Model weights have their own licenses, which are stored in `model_licenses/`:

- FLUX.1 [schnell] is licensed under Apache 2.0.
- FLUX.1 [dev] and the models derived from it (Fill, Canny, Depth, Redux, Kontext, and the LoRAs) are licensed under the FLUX.1 [dev] Non-Commercial License v1.1.1. That license permits non-commercial and non-production use. Commercial use requires a separate license from Black Forest Labs. It also has content-filtering and disclosure requirements. Read the full text before use.

This section summarizes the license files and is not legal advice.

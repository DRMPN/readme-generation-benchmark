# FLUX

Inference codebase for Black Forest Labs' FLUX image-generation models. It includes command-line sampling workflows for text-to-image, structural conditioning, inpainting/outpainting, image variation, and image editing, as well as Streamlit and Gradio demos.

## Contents

- [Installation](#installation)
- [Model access and checkpoints](#model-access-and-checkpoints)
- [Command-line usage](#command-line-usage)
- [Web demos](#web-demos)
- [TensorRT](#tensorrt)
- [Usage reporting](#usage-reporting)
- [Documentation](#documentation)
- [Licenses](#licenses)

## Installation

Python 3.10 or newer is required. From the repository root, install the package with its PyTorch dependencies:

```bash
python -m pip install -e '.[torch]'
```

The package's base dependencies are declared in `pyproject.toml`; PyTorch and torchvision are provided by the `torch` extra. Install optional UI dependencies as needed:

```bash
python -m pip install -e '.[streamlit]'  # Streamlit demos
python -m pip install -e '.[gradio]'     # Gradio demo
```

To install the UI extras and PyTorch together, use `python -m pip install -e '.[all]'`.

## Model access and checkpoints

Model files are downloaded from Hugging Face on first use into the repository's `checkpoints/` directory. Some model repositories are gated: sign in to Hugging Face and accept the applicable model terms before downloading. Authentication can be supplied with `HF_TOKEN` or configured using the Hugging Face CLI; if a gated download needs authentication, the code can prompt for a token.

The checkpoint directory can be overridden for individual model components with environment variables:

```bash
export FLUX_MODEL=/path/to/flow-model.safetensors
export FLUX_AE=/path/to/ae.safetensors
export FLUX_LORA=/path/to/lora.safetensors  # only for LoRA variants
export FLUX_REDUX=/path/to/redux.safetensors # optional Redux adapter path
```

`FLUX_MODEL` and `FLUX_AE` are used by the regular model-loading code; `FLUX_LORA` selects a local LoRA checkpoint. Redux accepts `FLUX_REDUX` and otherwise downloads its adapter automatically.

## Command-line usage

Run commands from the repository root. The module entry point exposes five subcommands:

```text
python -m flux t2i     # text-to-image
python -m flux control # Canny/depth structural conditioning
python -m flux fill    # inpainting and outpainting
python -m flux redux   # image variations
python -m flux kontext # image editing
```

Most commands generate one image by default. Add `--loop` to enter interactive sampling. Output images are written as numbered JPEGs (`img_0.jpg`, `img_1.jpg`, …) under `output/` by default. Sampling metadata is added to image EXIF by default and can be disabled with `--add_sampling_metadata=False`.

### Text-to-image

Choose `flux-schnell` or `flux-dev` with `--name`:

```bash
python -m flux t2i --name flux-schnell \
  --width 1360 --height 768 \
  --prompt "A cat holding a sign that says hello world" \
  --seed 42
```

If omitted, the model defaults to `flux-schnell`, the dimensions to 1360×768, and the prompt to a built-in example. The default step count is 4 for schnell and 50 for dev. Width and height should be multiples of 16; other values are rounded down to a multiple of 16. Use `--guidance` to set guidance (used by the guidance-distilled model).

To generate a sequence of prompts in one invocation, separate them with `|` in the prompt. For an interactive session, run `python -m flux t2i --name flux-dev --loop`; the loop accepts prompt text and slash commands for width (`/w`), height (`/h`), seed (`/s`), guidance (`/g`), step count (`/n`), and quit (`/q`).

### Structural conditioning: Canny and depth

The `control` command supports these model names: `flux-dev-canny`, `flux-dev-depth`, `flux-dev-canny-lora`, and `flux-dev-depth-lora`.

```bash
python -m flux control --name flux-dev-canny \
  --img_cond_path assets/robot.webp \
  --prompt "A robot made out of gold"
```

The input image is processed as a Canny edge or depth condition according to the selected model. LoRA variants use the corresponding adapter; their scale can be set with `--lora_scale` (default 0.85). The CLI also supports `--loop`, `--seed`, `--width`, `--height`, `--num_steps`, and `--guidance`.

### Inpainting and outpainting

The `fill` command uses `flux-dev-fill` and takes a conditioning image and a mask of matching dimensions. The mask should contain black and white areas; see [`assets/cup.png`](assets/cup.png) and [`assets/cup_mask.png`](assets/cup_mask.png) for the included example.

```bash
python -m flux fill \
  --img_cond_path assets/cup.png \
  --img_mask_path assets/cup_mask.png \
  --prompt "A white paper cup"
```

Image and mask dimensions must match and be divisible by 32. The defaults point to the included cup and mask. For an interactive session, add `--loop` to change prompts and conditioning files between generations.

### Image variations (Redux)

Redux varies an input image using either the `flux-dev` or `flux-schnell` base model. The default input is `assets/robot.webp`.

```bash
python -m flux redux --name flux-dev \
  --img_cond_path assets/robot.webp \
  --width 1360 --height 768
```

Add `--loop` for repeated interactive generations and input-image changes. The command uses the FLUX.1 Redux adapter, which is downloaded as needed.

### Image editing (Kontext)

The `kontext` command uses `flux-dev-kontext` to edit an input image according to a prompt:

```bash
python -m flux kontext \
  --img_cond_path assets/cup.png \
  --prompt "Replace the logo with the text 'Black Forest Labs'" \
  --num_steps 30 --aspect_ratio 16:9 --guidance 2.5 --seed 1
```

`--aspect_ratio` is optional; if omitted, output dimensions follow the input image. The interactive loop supports prompt and image changes, and can change aspect ratio with `/ar` (use `/ar auto` for the input image's dimensions).

### Common options

Sampling commands provide options such as `--device`, `--seed`, `--num_steps`, `--guidance`, `--offload`, `--output_dir`, and `--add_sampling_metadata`. Defaults and additional command-specific options are defined in the relevant CLI module under [`src/flux/`](src/flux/).

## Web demos

Install the corresponding optional dependencies before launching a demo.

The Streamlit text-to-image and image-to-image demo is:

```bash
streamlit run demo_st.py
```

The Streamlit Fill demo provides inpainting and outpainting:

```bash
streamlit run demo_st_fill.py
```

The Gradio text-to-image demo accepts `flux-schnell` or `flux-dev` (and other names in the model config):

```bash
python demo_gr.py --name flux-schnell --device cuda
```

Useful Gradio flags include `--offload` to move models to CPU when not in use and `--share` to create a public demo link. See `python demo_gr.py --help` for available arguments.

## TensorRT

TensorRT support is optional. Install the declared extra with:

```bash
python -m pip install -e '.[torch,tensorrt]'
```

The extra declares TensorRT for CUDA 12 and related ONNX/runtime dependencies. To select this backend, pass `--trt` to a supported CLI workflow and choose a transformer precision where applicable, for example:

```bash
python -m flux t2i --name flux-dev --trt \
  --trt_transformer_precision bf16 \
  --width 1024 --height 768
```

The transformer precision options used by the CLI are `bf16`, `fp8`, and `fp4` (Kontext documentation also mentions `fp4_sdvd32`). TensorRT engines and ONNX assets may need to be downloaded or built and can require access to gated Hugging Face repositories. `TRT_ENGINE_DIR` sets the engine directory; it defaults to `checkpoints/trt_engines`. The code also recognizes `TRT_T5_PRECISION`, `TRT_TIMING_CACHE_FILE`, and `CUSTOM_ONNX_PATHS`. See the workflow-specific documentation for further notes and constraints.

## Usage reporting

Some CLI and demo workflows can report generation counts to the Black Forest Labs licensing API. Reporting is opt-in via `--track_usage` for the command-line workflows and demos that expose it, and requires the `BFL_API_KEY` environment variable. See the [BFL licensing dashboard](https://dashboard.bfl.ai/licensing/subscriptions?showInstructions=true) for licensing and reporting information.

## Documentation

- [Text-to-image](docs/text-to-image.md)
- [Inpainting and outpainting](docs/fill.md)
- [Canny and depth conditioning](docs/structural-conditioning.md)
- [Image variation with Redux](docs/image-variation.md)
- [Image editing with Kontext](docs/image-editing.md)
- [Model cards](model_cards/)

## Licenses

The repository's inference code is distributed under the [Apache License 2.0](LICENSE). Model weights have separate terms: FLUX.1 schnell is listed with Apache-2.0 terms, while FLUX.1 dev and the documented dev-derived models use the FLUX.1-dev Non-Commercial License. Review the relevant model repository terms and the copies in [`model_licenses/`](model_licenses/) before downloading or using weights; the code license does not replace model licenses.

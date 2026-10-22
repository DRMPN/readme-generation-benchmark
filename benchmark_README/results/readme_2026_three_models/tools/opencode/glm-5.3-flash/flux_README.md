# FLUX.1 — Inference Codebase

This is the inference codebase for the **FLUX.1** model family by Black Forest Labs. It provides reference implementations and sampling code for running the open-weight FLUX.1 models locally, covering text-to-image generation, image variation, inpainting and outpainting, structural conditioning, and instruction-based image editing.

The code is packaged as the `flux` Python package (`src/flux/`) with a command-line interface and interactive demos built on [Gradio](https://gradio.app/) and [Streamlit](https://streamlit.io/).

## Models

The codebase supports the following open-weight models. The weights are downloaded automatically from Hugging Face (see [Model weights](#model-weights)).

| Name | Hugging Face repo | License |
| --- | --- | --- |
| `FLUX.1 [schnell]` | [black-forest-labs/FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) | [Apache-2.0](model_licenses/LICENSE-FLUX1-schnell) |
| `FLUX.1 [dev]` | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) | [FLUX.1-dev Non-Commercial License](model_licenses/LICENSE-FLUX1-dev) |
| `FLUX.1 Fill [dev]` | [black-forest-labs/FLUX.1-Fill-dev](https://huggingface.co/black-forest-labs/FLUX.1-Fill-dev) | [FLUX.1-dev Non-Commercial License](model_licenses/LICENSE-FLUX1-dev) |
| `FLUX.1 Redux [dev]` | [black-forest-labs/FLUX.1-Redux-dev](https://huggingface.co/black-forest-labs/FLUX.1-Redux-dev) | [FLUX.1-dev Non-Commercial License](model_licenses/LICENSE-FLUX1-dev) |
| `FLUX.1 Canny [dev]` | [black-forest-labs/FLUX.1-Canny-dev](https://huggingface.co/black-forest-labs/FLUX.1-Canny-dev) | [FLUX.1-dev Non-Commercial License](model_licenses/LICENSE-FLUX1-dev) |
| `FLUX.1 Depth [dev]` | [black-forest-labs/FLUX.1-Depth-dev](https://huggingface.co/black-forest-labs/FLUX.1-Depth-dev) | [FLUX.1-dev Non-Commercial License](model_licenses/LICENSE-FLUX1-dev) |
| `FLUX.1 Canny [dev] LoRA` | [black-forest-labs/FLUX.1-Canny-dev-lora](https://huggingface.co/black-forest-labs/FLUX.1-Canny-dev-lora) | [FLUX.1-dev Non-Commercial License](model_licenses/LICENSE-FLUX1-dev) |
| `FLUX.1 Depth [dev] LoRA` | [black-forest-labs/FLUX.1-Depth-dev-lora](https://huggingface.co/black-forest-labs/FLUX.1-Depth-dev-lora) | [FLUX.1-dev Non-Commercial License](model_licenses/LICENSE-FLUX1-dev) |
| `FLUX.1 Kontext [dev]` | [black-forest-labs/FLUX.1-Kontext-dev](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev) | [FLUX.1-dev Non-Commercial License](model_licenses/LICENSE-FLUX1-dev) |

The corresponding model names used by the CLI and demos are:

- `flux-dev`, `flux-schnell` — text-to-image
- `flux-dev-fill` — inpainting / outpainting
- `flux-dev-redux` — image variation (used with a base `flux-dev` or `flux-schnell` model)
- `flux-dev-canny`, `flux-dev-depth` — structural conditioning
- `flux-dev-canny-lora`, `flux-dev-depth-lora` — structural conditioning via LoRA adapters
- `flux-dev-kontext` — image editing

Task-specific details and example outputs are documented in [`docs/`](docs/):

- [Text-to-image](docs/text-to-image.md)
- [Image variation](docs/image-variation.md) (Redux)
- [Fill / inpainting and outpainting](docs/fill.md)
- [Structural conditioning](docs/structural-conditioning.md) (Canny / Depth)
- [Image editing](docs/image-editing.md) (Kontext)

## Installation

Requires Python `>=3.10`. Install the package with the extras matching your intended use:

```bash
# Base installation
pip install -e .

# Extras
pip install -e ".[torch]"        # PyTorch (pinned to torch 2.6.0) — required for inference
pip install -e ".[streamlit]"    # Streamlit demos
pip install -e ".[gradio]"       # Gradio demo
pip install -e ".[tensorrt]"     # TensorRT backend
pip install -e ".[all]"          # Everything above (torch, streamlit, gradio)
```

## Model weights

Weights are downloaded automatically into `checkpoints/` from Hugging Face the first time you start one of the demos or CLI commands. Alternatively, download the weights manually and place them in `checkpoints/`, or point to existing files with environment variables:

```bash
export FLUX_MODEL=<your model path here>
export FLUX_AE=<your autoencoder path here>
export FLUX_REDUX=<your redux path here>   # for Redux
export FLUX_LORA=<your lora path here>     # for Canny/Depth LoRA variants
```

The gated repositories (`FLUX.1 [dev]` and derivatives) require authentication to Hugging Face. You can set the `HF_TOKEN` environment variable or run `huggingface-cli login` beforehand; if the download fails due to access restrictions, the tooling will prompt for a token interactively.

## Usage

All functionality is exposed through the `python -m flux` command with the subcommands `t2i`, `control`, `fill`, `kontext`, and `redux`.

### Text-to-image

```bash
# Interactive sampling loop
python -m flux t2i --name <name> --loop

# Single sample
python -m flux t2i --name <name> \
  --height <height> --width <width> \
  --prompt "<prompt>"
```

`name` is either `flux-dev` or `flux-schnell`. In interactive mode, the prompt line accepts inline commands: `/w <width>` and `/h <height>` set the resolution, `/s <seed>` sets the seed, `/g <guidance>` sets the guidance (`flux-dev` only), `/n <steps>` sets the number of steps, and `/q` quits. Leaving the prompt empty repeats the previous prompt. By default, 4 steps are used for `flux-schnell` and 50 for `flux-dev`; heights and widths are rounded to multiples of 16. Images are written to `output/` as `img_<idx>.jpg`.

### Structural conditioning (Canny / Depth)

```bash
python -m flux control --name <name> --loop
```

where `name` is one of `flux-dev-canny`, `flux-dev-depth`, `flux-dev-canny-lora`, or `flux-dev-depth-lora`. The LoRA variants require the base `FLUX.1 [dev]` model, which is downloaded automatically alongside the LoRA adapter. A conditioning image is passed with `--img_cond_path` (the default is `assets/robot.webp`).

### Image variation (Redux)

```bash
python -m flux redux --name <name> --loop
```

where `name` is the base model, either `flux-dev` or `flux-schnell`. The conditioning image is passed with `--img_cond_path` (default `assets/robot.webp`).

### Fill (inpainting / outpainting)

```bash
# Interactive sampling loop
python -m flux fill --loop

# Single sample
python -m flux fill \
  --img_cond_path <path_to_input_image> \
  --img_mask_path <path_to_input_mask>
```

The mask must be an image of the same size as the conditioning image containing only black and white pixels; see [`assets/cup_mask.png`](assets/cup_mask.png) for [`assets/cup.png`](assets/cup.png). The conditioning image and mask are expected to have the same shape, with height and width divisible by 32.

### Image editing (Kontext)

```bash
# Interactive sampling loop
python -m flux kontext --loop

# Single sample
python -m flux kontext \
  --img_cond_path <path_to_input_image> \
  --prompt <your_prompt> \
  --num_steps 30 --aspect_ratio "16:9" --guidance 2.5 --seed 1
```

The flags `num_steps`, `aspect_ratio`, `guidance`, and `seed` are optional. See [`src/flux/cli_kontext.py`](src/flux/cli_kontext.py) for all available flags.

### TensorRT inference

TensorRT support requires installing the repository with the `tensorrt` extra. Exports are provided in BF16, FP8, and FP4 precision:

```bash
python -m flux t2i --name=<name> --loop --trt --trt_transformer_precision <precision>
```

`<precision>` can be `bf16`, `fp8`, `fp4`, or `fp4_svd32`. For ONNX exports, `height` and `width` have to be within 768 and 1344. ONNX models are fetched from the `black-forest-labs/*-onnx` Hugging Face repositories and cached in `checkpoints/`; built engines are stored under the directory set by `TRT_ENGINE_DIR` (default `checkpoints/trt_engines`).

### Demos

- Gradio demo for text-to-image and image-to-image:

  ```bash
  python demo_gr.py --name flux-schnell --device cuda
  ```

  Options: `--name` (`flux-schnell` or `flux-dev`), `--device` (default `cuda` if available, otherwise `cpu`), `--offload` (offload models to CPU when not in use), and `--share` (create a public link).

- Streamlit demo for text-to-image and image-to-image (image-to-image is only supported for `flux-dev`):

  ```bash
  streamlit run demo_st.py
  ```

- Streamlit demo for Fill-based inpainting/outpainting:

  ```bash
  streamlit run demo_st_fill.py
  ```

### Diffusers integration

The models are integrated with the [🧨 diffusers](https://github.com/huggingface/diffusers) library, e.g.:

```python
import torch
from diffusers import FluxPipeline

model_id = "black-forest-labs/FLUX.1-schnell"  # you can also use `black-forest-labs/FLUX.1-dev`

pipe = FluxPipeline.from_pretrained(model_id, torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()  # save VRAM by offloading the model to CPU

prompt = "A cat holding a sign that says hello world"
seed = 42
image = pipe(
    prompt,
    output_type="pil",
    num_inference_steps=4,  # use a larger number if you are using [dev]
    generator=torch.Generator("cpu").manual_seed(seed),
).images[0]
image.save("flux-schnell.png")
```

See the [diffusers documentation](https://huggingface.co/docs/diffusers/main/en/api/pipelines/flux) for details, including the Flux Control models.

## Safety, watermarks, and metadata

- Generated images are screened with an NSFW image classifier (`Falconsai/nsfw_image_detection`); outputs above the confidence threshold are not saved.
- Images are embedded with an invisible watermark.
- By default, the prompt is written to the output image's EXIF metadata (`--add_sampling_metadata`).
- All CLI entry points and demos accept a `--track_usage` flag that reports model usage for licensing purposes.

## Repository structure

```
├── assets/               # Example images used by the demos and documentation
├── docs/                 # Per-task usage guides
├── model_cards/          # Model cards for FLUX.1 [dev], [schnell], and Kontext [dev]
├── model_licenses/       # License files for the individual models
├── src/flux/
│   ├── modules/          # Building blocks (autoencoder, conditioner, layers, LoRA, image embedders)
│   ├── trt/              # TensorRT engine building and inference
│   ├── cli.py            # Text-to-image CLI
│   ├── cli_control.py    # Canny / Depth CLI
│   ├── cli_fill.py       # Fill CLI
│   ├── cli_kontext.py    # Kontext CLI
│   ├── cli_redux.py      # Redux CLI
│   ├── model.py          # FLUX transformer implementation
│   ├── sampling.py       # Noise generation, schedules, denoising, packing
│   ├── util.py           # Model configs, checkpoint loading, image saving
│   └── content_filters.py
├── demo_gr.py            # Gradio demo
├── demo_st.py            # Streamlit demo (text-to-image / image-to-image)
└── demo_st_fill.py       # Streamlit demo (Fill)
```

## License

The code in this repository is licensed under the [Apache License 2.0](LICENSE). The model weights are governed by separate licenses: `FLUX.1 [schnell]` is provided under Apache-2.0, while all other models listed above fall under the [FLUX.1-dev Non-Commercial License](model_licenses/LICENSE-FLUX1-dev). See [`model_licenses/`](model_licenses/) for the full license texts and the [model cards](model_cards/) for usage restrictions.

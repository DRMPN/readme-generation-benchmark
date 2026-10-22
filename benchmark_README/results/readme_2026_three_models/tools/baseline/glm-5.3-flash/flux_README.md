# FLUX

This repository is the official inference codebase for the **FLUX** model family, maintained by **Black Forest Labs**. It provides a reference implementation, sampling code, and interactive demos for the open-weight FLUX.1 models, covering text-to-image generation, image editing, inpainting/outpainting, structural conditioning, and image variation.

## Models

The codebase supports the following open-weight models. Weights are downloaded automatically from HuggingFace into `checkpoints/` on first use.

| Model | Code name | HuggingFace repo | License |
| --- | --- | --- | --- |
| FLUX.1 [dev] | `flux-dev` | `black-forest-labs/FLUX.1-dev` | FLUX.1-dev Non-Commercial License |
| FLUX.1 [schnell] | `flux-schnell` | `black-forest-labs/FLUX.1-schnell` | Apache-2.0 |
| FLUX.1 Kontext [dev] | `flux-dev-kontext` | `black-forest-labs/FLUX.1-Kontext-dev` | FLUX.1-dev Non-Commercial License |
| FLUX.1 Fill [dev] | `flux-dev-fill` | `black-forest-labs/FLUX.1-Fill-dev` | FLUX.1-dev Non-Commercial License |
| FLUX.1 Canny [dev] | `flux-dev-canny` | `black-forest-labs/FLUX.1-Canny-dev` | FLUX.1-dev Non-Commercial License |
| FLUX.1 Depth [dev] | `flux-dev-depth` | `black-forest-labs/FLUX.1-Depth-dev` | FLUX.1-dev Non-Commercial License |
| FLUX.1 Canny [dev] LoRA | `flux-dev-canny-lora` | `black-forest-labs/FLUX.1-Canny-dev-lora` | FLUX.1-dev Non-Commercial License |
| FLUX.1 Depth [dev] LoRA | `flux-dev-depth-lora` | `black-forest-labs/FLUX.1-Depth-dev-lora` | FLUX.1-dev Non-Commercial License |
| FLUX.1 Redux [dev] | adapter for `flux-dev`/`flux-schnell` | `black-forest-labs/FLUX.1-Redux-dev` | FLUX.1-dev Non-Commercial License |

Key model characteristics:

- `FLUX.1 [dev]` and `FLUX.1 [schnell]` are 12 billion parameter rectified flow transformers for text-to-image generation. `[dev]` is trained with guidance distillation; `[schnell]` uses latent adversarial diffusion distillation and generates images in 1–4 steps.
- `FLUX.1 Kontext [dev]` edits images from text instructions with robust consistency across successive edits, without finetuning.
- `FLUX.1 Fill [dev]` provides inpainting and outpainting.
- `FLUX.1 Canny [dev]` and `FLUX.1 Depth [dev]` (full models and LoRAs) condition generation on edge or depth maps for structure-preserving, text-guided edits.
- `FLUX.1 Redux [dev]` is an adapter that generates image variations from an input image.

See `model_cards/` for detailed model cards, including limitations and out-of-scope use.

## Setup

### Requirements

- Python **>= 3.10**
- A CUDA GPU is strongly recommended (the code defaults to `cuda` when available and falls back to `cpu`)
- PyTorch 2.6.0 (installed via the `torch` extra)

### Installation

Install from the repository root:

```bash
# Core inference (PyTorch)
pip install -e ".[torch]"

# Everything for demos: torch, Streamlit, and Gradio
pip install -e ".[all]"

# TensorRT-optimized inference (adds to the above as needed)
pip install -e ".[tensorrt]"
```

The base installation pulls in `accelerate`, `einops`, `fire`, `huggingface-hub`, `safetensors`, `sentencepiece`, `transformers` (>= 4.45.2), `tokenizers`, `protobuf`, `requests`, `invisible-watermark`, and `ruff`.

### Model weights and authentication

Weights are downloaded automatically to `checkpoints/` when you start a demo. The `[dev]`-family repositories are gated on HuggingFace, so you must authenticate first:

```bash
export HF_TOKEN=<your huggingface token>
# or
huggingface-cli login
```

Alternatively, download weights manually into `checkpoints/` and point the code at them with environment variables:

```bash
export FLUX_MODEL=<path to flow model>
export FLUX_AE=<path to autoencoder>
export FLUX_REDUX=<path to redux adapter>   # redux only
export FLUX_LORA=<path to LoRA>             # canny/depth LoRAs only
```

## Usage

All commands are dispatched through `python -m flux`, which exposes the subcommands `t2i`, `control`, `fill`, `kontext`, and `redux`.

### Text-to-image

```bash
# Interactive session
python -m flux t2i --name <flux-dev|flux-schnell> --loop

# Single sample
python -m flux t2i --name <name> \
  --height <height> --width <width> \
  --prompt "<prompt>"
```

Defaults: 4 steps for `flux-schnell`, 50 for `flux-dev`; height and width should be multiples of 16.

### Structural conditioning (Canny / Depth)

```bash
python -m flux control --name <flux-dev-canny|flux-dev-depth|flux-dev-canny-lora|flux-dev-depth-lora> \
  --img_cond_path <path_to_input_image> --loop
```

Default guidance is 30.0 for Canny and 10.0 for Depth. The LoRA variants additionally accept `--lora_scale` (default 0.85) and automatically download the base FLUX.1 [dev] model.

### Fill (inpainting / outpainting)

```bash
python -m flux fill \
  --img_cond_path <path_to_input_image> \
  --img_mask_path <path_to_input_mask>
```

The mask must be the same size as the conditioning image and contain only black and white pixels; image dimensions must be divisible by 32.

### Kontext (image editing)

```bash
python -m flux kontext \
  --img_cond_path <path_to_input_image> \
  --prompt "<edit instruction>" \
  --num_steps 30 --aspect_ratio "16:9" --guidance 2.5 --seed 1
```

Kontext was trained on specific preferred resolutions; if no `aspect_ratio` is given, the output matches the input image resolution.

### Redux (image variation)

```bash
python -m flux redux --name <flux-dev|flux-schnell> --img_cond_path <path_to_input_image> --loop
```

### Interactive commands

When running with `--loop`, the prompt input supports slash commands: `/w <width>`, `/h <height>`, `/s <seed>`, `/g <guidance>` (dev models only), `/n <steps>`, and `/q` to quit. Kontext also supports `/ar <width>:<height>` (or `auto`).

### Demos

- **Streamlit (text-to-image / image-to-image):** `streamlit run demo_st.py`
- **Streamlit (Fill inpainting/outpainting with a drawing canvas):** `streamlit run demo_st_fill.py`
- **Gradio:** `python demo_gr.py --name flux-schnell --device cuda` with options `--name`, `--device`, `--offload` (offload models to CPU when idle), and `--share` (create a public link).

### TensorRT inference

Install the `tensorrt` extra, then add `--trt --trt_transformer_precision <precision>` to `t2i`, `control`, or `kontext`:

```bash
python -m flux t2i --name=<name> --loop --trt --trt_transformer_precision bf16
```

- Transformer precisions: `bf16`, `fp8`, or `fp4` (`fp4_svd32` is also accepted); T5 precision is controlled by `TRT_T5_PRECISION` (`bf16` or `fp8`).
- For text-to-image ONNX exports, `height` and `width` must be within 768 and 1344.
- LoRA models are not supported with TRT.
- Engines are built on first run (via `polygraphy`) and cached in `TRT_ENGINE_DIR` (default `checkpoints/trt_engines`). Accessing the gated ONNX repositories requires accepting their licenses on HuggingFace.

### Diffusers integration

`FLUX.1 [schnell]` and `FLUX.1 [dev]` are also usable through 🧨 diffusers' `FluxPipeline`; see the [diffusers documentation](https://huggingface.co/docs/diffusers/main/en/api/pipelines/flux) for details.

## Configuration

Environment variables recognized by the codebase:

| Variable | Purpose |
| --- | --- |
| `HF_TOKEN` | HuggingFace authentication for gated repositories |
| `FLUX_MODEL`, `FLUX_AE`, `FLUX_REDUX`, `FLUX_LORA` | Manual checkpoint paths |
| `BFL_API_KEY` | Required for `--track_usage` (commercial usage reporting) |
| `TRT_ENGINE_DIR` | Directory for TensorRT engines (default `checkpoints/trt_engines`) |
| `TRT_T5_PRECISION` | T5 engine precision (`bf16`/`fp8`) |
| `TRT_TIMING_CACHE_FILE` | TRT timing cache |
| `CUSTOM_ONNX_PATHS` | Custom ONNX paths, formatted `module:path,module:path` |
| `TRT_ALLOCATION_POLICY` | `global` (default) or `dynamic` engine memory policy |

## Safety features and responsible use

- Generated images are checked with an NSFW classifier (threshold 0.85) and an invisible watermark is embedded before saving.
- The Kontext pipeline additionally runs a Pixtral-based content filter on prompts, input images, and outputs to detect copyright or public-figure concerns.
- Saved images carry Exif metadata identifying them as AI-generated, including the model name and (optionally) the prompt.
- Under `--track_usage`, generations of licensed dev models are reported to the BFL licensing API using `BFL_API_KEY`, for commercial-licensing compliance.
- The models must not be used for unlawful content, exploitation of minors, disinformation, harassment, non-consensual nudity, or fully automated decision-making affecting legal rights; see the model cards for the complete out-of-scope-use list.

## Development

- **Formatting and linting:** Ruff (pinned to 0.6.8) with a line length of 110, double quotes, and isort-style import sorting. Run:

  ```bash
  ruff check .
  ruff check --select I .
  ruff format .
  ```

- **Versioning:** handled by `setuptools_scm`, which writes `src/flux/_version.py` (fallback version `0.0.0`).
- **Type checking:** a `pyright` configuration is included, covering `src/` with a `./typings` stub path.
- **pyproject tooling:** `tomlsort` is configured to keep `pyproject.toml` sorted in CI.

## Testing

The repository does not ship a unit-test suite. Correctness of style, imports, and formatting is enforced in CI (`.github/workflows/ci.yaml`, running on every push with Python 3.10), which executes:

```bash
ruff check --output-format=github .
ruff check --select I --output-format=github .
ruff format --check .
```

To smoke-test your installation and GPU setup, generate an image:

```bash
python -m flux t2i --name flux-schnell --prompt "a cat holding a sign that says hello world"
```

## Repository layout

- `src/flux/` — CLI entry points (`cli.py`, `cli_control.py`, `cli_fill.py`, `cli_kontext.py`, `cli_redux.py`), sampling logic, the `Flux` transformer, math utilities, and safety filters.
- `src/flux/modules/` — autoencoder, text conditioners (T5/CLIP), image embedders (Canny, Depth, Redux/SigLIP), transformer layers, and LoRA utilities.
- `src/flux/trt/` — TensorRT engine wrappers and build configurations for CLIP, T5, the transformer, and the VAE.
- `demo_gr.py`, `demo_st.py`, `demo_st_fill.py` — Gradio and Streamlit demos.
- `docs/` — per-capability documentation; `model_cards/` — model cards; `model_licenses/` — weight licenses; `assets/` — example images.

## License

- The **code** in this repository is released under the [Apache License 2.0](LICENSE).
- The **model weights** are governed by their own licenses: `FLUX.1 [schnell]` under Apache-2.0 and all `[dev]`-family models under the FLUX.1 [dev] Non-Commercial License. See `model_licenses/` and the model cards for details.

## Citation

If you use FLUX.1 Kontext, please cite (from `model_cards/FLUX.1-kontext-dev.md`):

```bib
@misc{labs2025flux1kontextflowmatching,
      title={FLUX.1 Kontext: Flow Matching for In-Context Image Generation and Editing in Latent Space},
      author={Black Forest Labs and Stephen Batifol and Andreas Blattmann and Frederic Boesel and Saksham Consul and Cyril Diagne and Tim Dockhorn and Jack English and Zion English and Patrick Esser and Sumith Kulal and Kyle Lacey and Yam Levi and Cheng Li and Dominik Lorenz and Jonas Müller and Dustin Podell and Robin Rombach and Harry Saini and Axel Sauer and Luke Smith},
      year={2025},
      eprint={2506.15742},
      archivePrefix={arXiv},
      primaryClass={cs.GR},
      url={https://arxiv.org/abs/2506.15742},
}
```

# FLUX Inference

This repository contains Black Forest Labs’ reference inference code for FLUX image-generation and image-editing models. It provides a PyTorch implementation, command-line workflows, Streamlit and Gradio demos, and an optional TensorRT backend.

Available workflows include text-to-image generation, image editing with FLUX.1 Kontext, Canny- and depth-conditioned generation, image variation with the Redux adapter, and inpainting or outpainting with FLUX.1 Fill.

## Requirements

- Python 3.10 or later.
- PyTorch for model inference. The declared optional PyTorch dependency is `torch==2.6.0`, with `torchvision`.
- Model weights and text/image encoder files, which are downloaded from Hugging Face when needed unless supplied locally.
- A CUDA-capable GPU is used by default when available. The command-line tools also accept a `--device` setting and support CPU offloading with `--offload`.

The FLUX models are large, so allow for substantial memory and storage requirements. The repository does not specify minimum hardware requirements.

## Installation

Clone the repository, then install it with the inference dependencies:

```bash
git clone https://github.com/black-forest-labs/flux.git
cd flux
python -m pip install -e ".[torch]"
```

Install optional demo dependencies as needed:

```bash
python -m pip install -e ".[streamlit]"
python -m pip install -e ".[gradio]"
```

For both demo frameworks and PyTorch, install the combined extra:

```bash
python -m pip install -e ".[all]"
```

The TensorRT extra is separate:

```bash
python -m pip install -e ".[torch,tensorrt]"
```

TensorRT inference requires CUDA; the TensorRT manager checks that a CUDA device is available.

## Model access and checkpoints

The first run downloads the required model files into `checkpoints/`. Some Hugging Face repositories are gated. If access is required, accept the repository’s terms on Hugging Face and authenticate using either:

```bash
huggingface-cli login
```

or an environment token:

```bash
export HF_TOKEN=<your_hugging_face_token>
```

For manual checkpoint placement or alternate paths, the loaders recognize these environment variables:

- `FLUX_MODEL`: flow model checkpoint.
- `FLUX_AE`: autoencoder checkpoint.
- `FLUX_LORA`: LoRA checkpoint for Canny or depth LoRA variants.
- `FLUX_REDUX`: Redux adapter checkpoint.

For example:

```bash
export FLUX_MODEL=/path/to/model.safetensors
export FLUX_AE=/path/to/ae.safetensors
```

The repository also creates `checkpoints/` and uses it for downloaded files and, by default, TensorRT engines.

## Command-line usage

Run commands through the package module. Its command groups are `t2i`, `control`, `fill`, `kontext`, and `redux`. Use `--help` to inspect available options.

### Text-to-image

Choose `flux-schnell` or `flux-dev`. The default model is `flux-schnell`.

```bash
python -m flux t2i --name flux-schnell \
  --prompt "A cat holding a sign that says hello world" \
  --width 1024 --height 1024 --seed 42
```

Start an interactive session with `--loop`:

```bash
python -m flux t2i --name flux-dev --loop
```

By default, schnell uses 4 sampling steps and dev uses 50. Width and height are adjusted down to multiples of 16. Results are saved as numbered JPEGs under `output/` by default. Sampling prompts can be included in image metadata.

### Image-conditioned workflows

For structural conditioning, select one of `flux-dev-canny`, `flux-dev-depth`, `flux-dev-canny-lora`, or `flux-dev-depth-lora`:

```bash
python -m flux control --name flux-dev-canny \
  --img_cond_path assets/robot.webp \
  --prompt "A robot made of gold"
```

LoRA variants use the FLUX.1 dev base model and do not support TensorRT in this CLI.

For inpainting or outpainting, provide an image and a same-size black-and-white mask. The mask and conditioning image must have matching dimensions divisible by 32:

```bash
python -m flux fill \
  --img_cond_path assets/cup.png \
  --img_mask_path assets/cup_mask.png \
  --prompt "A white paper cup"
```

For instruction-based image editing with Kontext:

```bash
python -m flux kontext \
  --img_cond_path assets/cup.png \
  --prompt "Replace the logo with the text Black Forest Labs" \
  --num_steps 30 --guidance 2.5 --seed 1
```

Kontext accepts an optional `--aspect_ratio`, such as `"16:9"`. If omitted, its output resolution is based on the conditioning image.

For image variations, Redux supports either `flux-dev` or `flux-schnell` as the base model:

```bash
python -m flux redux --name flux-dev \
  --img_cond_path assets/robot.webp
```

Additional flags, including `--device`, `--offload`, `--output_dir`, `--num_steps`, and `--track_usage`, are available on relevant commands. Use `--loop` for repeated interactive sampling. In interactive command-line sessions, prompts and sampling parameters can be updated with slash commands; `/h` displays the available commands and `/q` exits.

## Demos

The text-to-image Streamlit demo also supports image-to-image:

```bash
streamlit run demo_st.py
```

The Fill Streamlit demo provides inpainting and outpainting controls:

```bash
streamlit run demo_st_fill.py
```

Launch the Gradio text-to-image demo with:

```bash
python demo_gr.py --name flux-schnell --device cuda
```

Use `--offload` to offload models to CPU when not in use, or `--share` to create a public demo link.

## TensorRT inference

Install the TensorRT extra before using `--trt`. The CLI builds or loads TensorRT engines and may download ONNX exports from Hugging Face. Some model exports require Hugging Face access and acceptance of the repository’s terms.

For example:

```bash
python -m flux t2i --name flux-schnell --loop \
  --trt --trt_transformer_precision bf16
```

The transformer precision setting supports `bf16`, `fp8`, and FP4 variants as documented for the relevant workflow. TensorRT configuration can also be directed with environment variables:

- `TRT_ENGINE_DIR`: engine output directory (defaults to `checkpoints/trt_engines`).
- `TRT_T5_PRECISION`: T5 precision, `bf16` by default; the TensorRT manager accepts `bf16` or `fp8`.
- `TRT_TIMING_CACHE_FILE`: optional timing-cache path.
- `CUSTOM_ONNX_PATHS`: custom ONNX module paths where supported.

TensorRT options and supported precision variants differ by workflow. For example, the text-to-image documentation specifies image dimensions within 768 and 1344 for its ONNX exports.

## Development and testing

The project uses setuptools and setuptools-scm for packaging and versioning. Install the package in editable mode as described above. The configured Python tooling includes Ruff for linting, import sorting, and formatting; Pyright is configured for the `src` tree.

To run the checks used by continuous integration:

```bash
python -m pip install ruff==0.6.8
ruff check .
ruff check --select I .
ruff format --check .
```

The supplied CI workflow runs these Ruff checks on pushes using Python 3.10. No separate automated test suite is included in the supplied repository files.

## Safety and usage tracking

Generation workflows apply an NSFW image classifier; the demos use a threshold of `0.85`. Kontext additionally checks prompts, input images, and generated images with a content filter. These checks are part of the supplied inference code and should be considered alongside the model’s applicable usage terms.

Usage tracking can be enabled on supported commands or demos with `--track_usage`. It requires the `BFL_API_KEY` environment variable and reports generation counts to the BFL licensing API:

```bash
export BFL_API_KEY=<your_bfl_api_key>
```

## License

The repository’s `LICENSE` file applies the Apache License 2.0 to the software covered by that file. Model weights have separate terms: FLUX.1 schnell is listed under Apache 2.0, while FLUX.1 dev and the listed Fill, Kontext, Redux, Canny, and depth models are associated with the FLUX.1 dev Non-Commercial License. Review the relevant files in `model_licenses/` and model documentation before downloading, using, or redistributing weights.

# FLUX

This repository provides inference code and demos for the FLUX family of image-generation models. It includes command-line tools for text-to-image generation, image editing, filling, structural conditioning, and image variation, as well as optional TensorRT support.

## Features

- Text-to-image inference with FLUX.1 [dev] and FLUX.1 [schnell]
- Image-to-image and image-editing workflows
- Fill and inpainting workflows
- Structural conditioning, including canny and depth examples
- Redux image-variation workflows
- Optional LoRA support
- Streamlit and Gradio demos
- Optional TensorRT engine management and configuration

## Requirements

- Python 3.10 or later
- PyTorch
- A compatible GPU is strongly recommended; CUDA is commonly used for inference
- The model weights required by the workflow you want to run

Model weights are distributed separately from this repository. FLUX.1 model downloads may require accepting the applicable Hugging Face access conditions. Check the model pages and license files before downloading or using the weights.

## Installation

Clone the repository and install its Python package:

```bash
git clone <repository-url>
cd flux-7kn8kxp1

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\activate
```

Install a PyTorch build appropriate for your hardware and CUDA version if it is not already installed. Consult the [official PyTorch installation selector](https://pytorch.org/get-started/locally/) for the correct command.

Some optional features may require additional packages. Refer to `pyproject.toml` and `setup.py` for the project’s declared dependencies.

## Download model weights

Download weights from the relevant model repositories and keep them in a location accessible to the CLI. A typical FLUX.1 setup uses:

- A FLUX model checkpoint, such as `flux1-dev.safetensors` or `flux1-schnell.safetensors`
- The autoencoder checkpoint, commonly `ae.safetensors`
- The CLIP-L text encoder, commonly `clip_l.safetensors`
- The T5 text encoder, commonly `t5xxl_fp16.safetensors` or a supported alternative

For example, after obtaining access to the relevant Hugging Face repositories, you can download their files with the Hugging Face CLI:

```bash
huggingface-cli login
huggingface-cli download black-forest-labs/FLUX.1-dev \
  --local-dir models/flux-dev
```

Repeat for the model variant and files you intend to use. Download commands and available files can change; use the model repository’s current instructions as the source of truth.

Keep the weights in a secure location and do not commit them to version control.

## Text-to-image generation

The package provides a module-based CLI. For example:

```bash
python -m flux --name flux-schnell --prompt "A small robot tending a garden"
```

To try the development model:

```bash
python -m flux --name flux-dev --prompt "A cinematic photograph of a red fox in snow"
```

The CLI provides options for settings such as output dimensions, seed, device, and model location. Check the installed command’s help for the exact options supported by your version:

```bash
python -m flux --help
```

Choose output dimensions supported by the model and workflow. Keeping dimensions divisible by 16 is a useful practical guideline.

## Image workflows

The repository includes separate command-line entry points for several image-to-image tasks. Their available options vary, so start with the relevant help output:

```bash
python -m flux.cli_control --help
python -m flux.cli_fill --help
python -m flux.cli_kontext --help
python -m flux.cli_redux --help
```

### Image editing and variation

Use the appropriate image-editing or variation workflow to provide an input image and a prompt. See `image-editing.md` and `image-variation.md` for examples and guidance.

### Fill and inpainting

The fill workflow supports editing a specified image region using a mask and prompt. See `fill.md` for examples, including inpainting and outpainting.

### Structural conditioning

The control workflow supports structural inputs such as canny edges and depth maps. See `structural-conditioning.md` and the sample assets in the repository.

### Kontext

The Kontext workflow supports image editing guided by a prompt and an input image. See `FLUX.1-kontext-dev.md` for model-specific information and examples.

### Redux

The Redux workflow is intended for image variation and related image-conditioned tasks. See `image-variation.md` and the CLI help for its options.

## Demos

The repository includes both Streamlit and Gradio demos. Run them from the repository root:

```bash
streamlit run demo_st.py
```

```bash
python demo_gr.py
```

The demos need access to the model weights and dependencies used by the selected workflow. Consult their help output or source if you need to customize model paths or runtime settings.

## TensorRT

TensorRT-related configuration and engine-management code is included in the repository. It is an optional inference path and requires a compatible NVIDIA GPU, TensorRT installation, and correctly configured engines.

Relevant files include:

- `trt_manager.py` — engine management
- `base_trt_config.py`, `transformer_trt_config.py`, `vae_trt_config.py`, `clip_trt_config.py`, and `t5_trt_config.py` — component configuration
- `base_engine.py`, `transformer_engine.py`, `vae_engine.py`, `clip_engine.py`, and `t5_engine.py` — inference engines

TensorRT setup is hardware- and environment-dependent. Use the configuration files and CLI help to determine the required settings for your installation.

## Repository contents

| File or group | Purpose |
|---|---|
| `model.py`, `layers.py`, `math.py` | Model and supporting operations |
| `sampling.py`, `util.py` | Sampling and inference utilities |
| `content_filters.py` | Content-filtering utilities |
| `autoencoder.py`, `conditioner.py`, `image_embedders.py` | Autoencoder and conditioning components |
| `cli.py` | General generation CLI |
| `cli_control.py` | Structural-conditioning CLI |
| `cli_fill.py` | Fill and inpainting CLI |
| `cli_kontext.py` | Kontext editing CLI |
| `cli_redux.py` | Redux CLI |
| `lora.py` | LoRA support |
| `demo_st.py`, `demo_gr.py` | Streamlit and Gradio demos |
| `text-to-image.md`, `image-editing.md`, `fill.md`, `structural-conditioning.md`, `image-variation.md` | Workflow guides |
| `FLUX.1-dev.md`, `FLUX.1-schnell.md`, `FLUX.1-kontext-dev.md` | Model-specific documentation |
| `LICENSE*` | Repository and model-license information |

## Performance and troubleshooting

- **Out-of-memory errors:** Reduce output dimensions, close other GPU workloads, or use an appropriate offloading or reduced-precision option if supported by the CLI.
- **Weights not found:** Check the model path and verify that all files required by the selected workflow are present.
- **Access denied when downloading:** Confirm that you have accepted the model’s access conditions and authenticated with Hugging Face.
- **CUDA or dependency errors:** Verify that the installed PyTorch build matches your GPU and CUDA environment.
- **Unknown CLI option:** Run the relevant command with `--help`; options can differ between workflows and versions.
- **Slow first run:** Initial loading or TensorRT engine preparation may take longer than subsequent inference.

## Licensing

This repository includes `LICENSE`, `LICENSE-FLUX1-dev`, and `LICENSE-FLUX1-schnell`. Model weights may have terms separate from the source code. Review the applicable license and model-card terms before using or redistributing code, weights, or generated results.

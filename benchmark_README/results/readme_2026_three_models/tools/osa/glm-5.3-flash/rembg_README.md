# rembg-_n_pawxh

---

[![PyPi](https://badge.fury.io/py/rembg.svg)](https://badge.fury.io/py/rembg)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![numpy](https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white)
![scipy](https://img.shields.io/badge/SciPy-8CAAE6.svg?style=flat&logo=SciPy&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project removes image backgrounds in Python, producing segmentation masks or cutouts from images. It targets developers integrating background removal into applications, as well as ML users who need to select among multiple pretrained segmentation models with CPU or GPU execution. The package offers both a Python API and a command-line interface, with inference running locally. A demo notebook (`rembg.ipynb`) is available in the repository. See Getting Started for installation and runnable steps.

---

## Core Features

- Removes image backgrounds via a single Python API that produces cutouts as bytes, Pillow images, or NumPy arrays, so you can drop results directly into your existing image pipeline.
- Offers multiple pretrained segmentation models (U2Net family, BiRefNet family, DIS, SAM, BRIA RMBG, BEN, and more), letting you pick the model best suited to your images, including custom-model variants.
- Refines cutouts with optional alpha matting and mask post-processing, improving edge quality on soft or fine boundaries.
- Provides a CLI with several commands for batch and single-image processing, enabling background removal without writing code.
- Runs inference locally through ONNX Runtime with automatic CUDA, ROCm, or CPU provider selection, so you can deploy on the hardware you have.

---

## Installation

**Prerequisites:** Python with `pip` available; the repository pins its interpreter version in `.python-version`.

**Note:** The PyPI package name is `rembg`; the repository name (`rembg-_n_pawxh`) differs from the package name.

Install the base package from PyPI:

```sh
pip install rembg
```

Install with the `gpu` and `cli` extras if you need GPU inference support or the command-line interface:

```sh
pip install "rembg[gpu,cli]"
```

---

## Getting Started

**Prerequisites**

- Python with `pip` available (the repository pins its interpreter version in `.python-version`).

**Steps**

1. Install the package with the `gpu` and `cli` extras (see [Installation](#installation) for the base install):

```bash
   pip install "rembg[gpu,cli]"
```

2. Verify the installation:

```bash
   python -c "import rembg; print(rembg.__version__)"
```

3. Remove a background via the Python API. `rembg.remove` (exported from `rembg.bg`) accepts `bytes`, a PIL image, or a NumPy array:

```python
   from rembg import remove
   from PIL import Image

   input_image = Image.open("input.jpg")
   output_image = remove(input_image)
   output_image.save("output.png")
```

4. The first run downloads the ONNX model for the selected session automatically. Weights are cached under `~/.u2net` (or `$XDG_DATA_HOME/.u2net` when `XDG_DATA_HOME` is set); set the `U2NET_HOME` environment variable to override the location. GPU inference (CUDA/ROCm providers) is selected automatically when available.

5. Optional CLI: the click-based command-line app in `rembg/cli.py` registers the subcommands `b`, `d`, `i`, `p`, and `s`. See `USAGE.md` for the exact commands and flags.

See also `USAGE.md` and the `examples/` directory for further usage patterns.

---

## API Reference

### Core library (`rembg`)

| Symbol | Description |
| --- | --- |
| `rembg.remove(data, ...)` | Removes the background from an image. `data` accepts `bytes`, a Pillow image (`PIL.Image.Image`), or a `numpy.ndarray`; alpha matting is controlled with keyword options such as `alpha_matting: bool = False`. Defined in `rembg/bg.py`. |
| `rembg.new_session(...)` | Factory from `rembg.session_factory`; creates a session for a model registered in `rembg.sessions`. |
| `rembg.ReturnType` | Enum in `rembg.bg` with members `BYTES = 0`, `PILLOW = 1`, `NDARRAY = 2` (bytes, Pillow image, and ndarray result formats). |
| `rembg.__version__` | Package version string (versioneer-managed). |

Additional helpers in `rembg/bg.py` (for example `naive_cutout`, `alpha_matting_cutout`, `post_process`) are implementation details and are not exported from the package root.

### Model sessions (`rembg.sessions`)

| Symbol | Description |
| --- | --- |
| `rembg.sessions.sessions` | Registry mapping model name to `BaseSession` subclass (`Dict[str, type[BaseSession]]`). |
| `rembg.sessions.sessions_names` | List of all registered model names. |
| `rembg.sessions.sessions_class` | List of all registered session classes. |
| `rembg.sessions.base.BaseSession` | Base class for model sessions; selects the ONNX Runtime provider (CUDA, ROCm, or CPU), downloads the model, and normalizes inputs. |

`BaseSession` members:

| Member | Description |
| --- | --- |
| `__init__(model_name, sess_opts, ...)` | Builds the `onnxruntime.InferenceSession` from the path returned by `download_models()`, choosing `CUDAExecutionProvider` or `ROCMExecutionProvider` when available and `CPUExecutionProvider` otherwise. |
| `normalize(img, mean, std, size)` | Converts a PIL image (converted to RGB, resized to `size`) into the normalized `float32` input dictionary expected by the model. |
| `predict(img)` | Abstract; subclasses return a `List[PILImage]` result for the input image. |
| `download_models()` | Abstract classmethod; downloads and returns the model file path. |
| `name()` | Abstract classmethod; its return value is used as the registry key in `rembg.sessions.sessions`. |
| `checksum_disabled()` | Classmethod; `True` when the `MODEL_CHECKSUM_DISABLED` environment variable is set. |
| `u2net_home()` | Classmethod; model storage directory, overridable via `U2NET_HOME` (default `~/.u2net`, honoring `XDG_DATA_HOME`). |

Session classes registered in `rembg/sessions/__init__.py`:

- **BiRefNet**: `BiRefNetSessionGeneral`, `BiRefNetSessionGeneralLite`, `BiRefNetSessionPortrait`, `BiRefNetSessionDIS`, `BiRefNetSessionHRSOD`, `BiRefNetSessionCOD`, `BiRefNetSessionMassive` (modules `rembg.sessions.birefnet_*`)
- **DIS**: `DisSession` (imported from both `dis_anime` and `dis_general_use` and registered under each model's name) and `DisCustomSession` (modules `rembg.sessions.dis_*`)
- **U2Net**: `U2netSession`, `U2netpSession`, `U2netHumanSegSession`, `Unet2ClothSession`, `U2netCustomSession` (modules `rembg.sessions.u2net*`)
- **Other models**: `SamSession` (`rembg.sessions.sam`), `SiluetaSession` (`rembg.sessions.silueta`), `BriaRmBgSession` (`rembg.sessions.bria_rmbg`), `BenCustomSession` (`rembg.sessions.ben_custom`)

Model download utility:

- `rembg.bg.download_models(models: tuple[str, ...])` — downloads model files for the given names; an empty tuple downloads every registered model. Exits with status 1 if a name is not registered.

### CLI (`rembg.cli`)

- Entry module `rembg/cli.py` defines a `click` command group and registers the commands collected in `rembg.commands`: `b_command`, `d_command`, `i_command`, `p_command`, `s_command`.
- Supports `--version` reporting the package version.
- Command flags and behavior are defined in `rembg/commands/*.py`; see `USAGE.md` for end-user usage.

---

## Examples

Usage examples are available in the [`examples/`](./examples) directory.

---

## Contributing

- Bug reports and feature requests can be filed through the repository's issue and feature request templates.
- Code changes are validated by the repository's lint CI workflow; ensure your changes pass linting before opening a pull request.

---

## License

License terms were not verified for this README. Consult the repository for the applicable license before reuse.

---

## Citation

If you use this software, please cite it as it is written in the [CITATION](./CITATION.cff) file.

---
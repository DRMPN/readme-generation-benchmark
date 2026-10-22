# rembg-b3l2d0h3

---

[![PyPi](https://badge.fury.io/py/rembg.svg)](https://badge.fury.io/py/rembg)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![scipy](https://img.shields.io/badge/SciPy-8CAAE6.svg?style={0}&logo=SciPy&logoColor=white)
![tqdm](https://img.shields.io/badge/tqdm-FFC107.svg?style={0}&logo=tqdm&logoColor=black)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Testing](#testing)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

rembg removes the background from images by separating the foreground subject from its surroundings. It is intended for developers who need background removal in Python applications and for end users who want to process images from the command line or with a Windows installer. The project provides a command-line interface for interactive use, an importable Python library for integration into code, and container-based deployment, with GPU execution available when the runtime hardware supports it. For runnable setup steps and a first example, see the Getting Started section, and for detailed command usage, see the usage documentation.

---

## Core Features

- Removes backgrounds from images through both a command-line interface and a Python library, so you can process files in scripts or integrate removal into your own code.
- Supports multiple named segmentation models that you select by name, letting you choose a model suited to your use case without changing your code.
- Uses GPU acceleration (CUDA or ROCm) when available and falls back to CPU otherwise, so the same code runs on machines with or without a supported GPU.
- Offers optional alpha matting to refine edges, which can improve cutout quality around fine detail such as hair.
- Returns results as encoded bytes, PIL images, or NumPy arrays, and can apply a solid background color to the output, so results fit into different processing pipelines.

---

## Installation

**Prerequisites:** requires Python >=3.10, <3.14

Install rembg-b3l2d0h3 using one of the following methods:

**Using PyPi:**

```sh
pip install rembg
```

---

## Getting Started

### Prerequisites

- Python, with the version constraints defined in the repository (see `.python-version` and `pyproject.toml`).
- Install the project first by following the Installation section.

### Quickstart

1. Install the package as described in the Installation section.

2. Confirm the CLI loads. `rembg/cli.py` builds a Click command group with a version option, so this should print the version:

```bash
python -m rembg.cli --version
```

3. Remove the background from an image using the library API. `rembg/bg.py` defines `remove()`, which accepts bytes, a PIL image, or a NumPy array:

```python
from PIL import Image

from rembg.bg import remove

input_image = Image.open("input.png")
output = remove(input_image)
```

4. Check the return type in `remove()` in `rembg/bg.py` before saving the result.

Model files are stored under the `U2NET_HOME` environment variable path, which defaults to `~/.u2net` (see `rembg/sessions/base.py`).

---

## Architecture

The project is a Python package that exposes background removal both as a command-line tool and as an importable library. Its structure is modular, with each model implemented as a separate session class selected by name at runtime.

- **CLI layer (`rembg/cli.py`, `rembg/commands/`)**: A Click command group is built in `cli.py`, and subcommands are registered from the `command_functions` list exported by `rembg/commands/`.
- **Library API (`rembg/bg.py`)**: `remove()` is the main entry point for processing image data. The module also provides post-processing and cutout helpers, including alpha matting via `pymatting`, morphological cleanup, and background color application.
- **Session factory (`rembg/session_factory.py`)**: `new_session(model_name)` looks up a session class by name in `sessions_class`, creates ONNX Runtime `SessionOptions` (honoring `OMP_NUM_THREADS`), and returns the instance.
- **Model sessions (`rembg/sessions/`)**: Each model has its own module that subclasses `BaseSession`. `BaseSession` handles ONNX Runtime inference setup, including execution provider selection (CUDA, ROCm, or CPU), input normalization, and model file resolution. Model storage location is controlled by the `U2NET_HOME` environment variable, and checksum verification can be disabled with `MODEL_CHECKSUM_DISABLED`.
- **Delivery and packaging**: The package is published to PyPI, and Docker images are defined in `Dockerfile` and `Dockerfile_nvidia_cuda_cudnn_gpu`. A Windows installer is built from `_setup.iss` and `_build-exe.ps1`.

Details of individual command implementations and the full `remove()` flow were not reviewed, so this overview covers only the structure visible in the provided context.

---

## Testing

Changes are verified with the test artifacts in the repository. Coverage and the specific behaviors tested are not documented here.

- **Test suite:** `tests/test_remove.py`, with supporting `tests/fixtures` and `tests/results` directories.
- **Test configuration:** `pytest.ini` at the repository root.
- **CI workflows:** `.github/workflows/lint_python.yml` (Python linting) and `.github/workflows/test_install.yml` (installation checks). Review these files for the exact commands and triggers used in CI.

The exact local test command is not documented in the reviewed context. Check `pytest.ini` and the CI workflow files before running tests locally.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE.txt) file.

---

## Citation

If you use this software, please cite it as it is written in the [CITATION](./CITATION.cff) file.

---
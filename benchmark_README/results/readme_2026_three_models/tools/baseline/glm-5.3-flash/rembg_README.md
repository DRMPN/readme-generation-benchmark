# rembg

**Remove image background** — a Python library and CLI tool that uses ONNX-based deep learning models to remove the background from images. It supports multiple segmentation models, runs on CPU, GPU (CUDA) and ROCm, and exposes both a programmatic API and a CLI with interactive/server modes.

## Requirements

- Python >= 3.10, < 3.14

## Installation

### CPU

```sh
pip install "rembg[cpu,cli]"
```

### GPU (CUDA)

```sh
pip install "rembg[gpu,cli]"
```

### ROCm

```sh
pip install "rembg[rocm,cli]"
```

The `[cli]` extra installs the dependencies needed for the command-line interface (including Gradio, FastAPI, and Uvicorn). The `[cpu]`, `[gpu]`, and `[rocm]` extras install the appropriate ONNX Runtime backend.

### Google Colab

A ready-to-use notebook (`rembg.ipynb`) is included that demonstrates installation and running the Gradio viewer on Colab with GPU acceleration.

## Models

Models are downloaded automatically on first use (via [pooch](https://github.com/fatiando/pooch)) and cached locally (typically under `~/.u2net/`). The following models are available:

| Model | Description |
|-------|-------------|
| `u2net` | General-purpose segmentation (default) |
| `u2netp` | Lightweight version of u2net |
| `u2net_human_seg` | Human segmentation |
| `u2net_cloth_seg` | Cloth segmentation (upper/lower/full) |
| `silueta` | Silhouette extraction |
| `isnet-general-use` | General-use DIS model |
| `isnet-anime` | Anime image segmentation |
| `birefnet-general` | BiRefNet general segmentation |
| `birefnet-general-lite` | BiRefNet lightweight general |
| `birefnet-portrait` | BiRefNet portrait segmentation |
| `birefnet-dis` | BiRefNet DIS |
| `birefnet-hrsod` | BiRefNet high-resolution salient object detection |
| `birefnet-cod` | BiRefNet camouflaged object detection |
| `birefnet-massive` | BiRefNet massive |
| `bria-rmbg` | Bria RMBG 2.0 |
| `sam` | Segment Anything Model (requires input points) |
| `u2net_custom` | Use a custom U²-Net ONNX model file |
| `dis_custom` | Use a custom DIS ONNX model file |

## Command-line usage

The package installs a `rembg` entry point. Available subcommands:

```
rembg --help
```

- `rembg d` — Download models locally
- `rembg i` — Serve an interactive Gradio-based image viewer
- `rembg p` — Serve an HTTP-based API
- `rembg s` — Serve a Streamlit-based image viewer
- `rembg b` — Process a directory of images

Each subcommand provides its own `--help` output with detailed options.

### Pre-downloading models

You can pre-download a model before use (as done in the Dockerfile):

```sh
rembg d u2net
```

## Python API usage

### Basic usage

```python
from PIL import Image
from rembg import remove

input_path = "input.png"
output_path = "output.png"

input = Image.open(input_path)
output = remove(input)
output.save(output_path)
```

By default, the `u2net` model is used.

### Using a specific model

```python
from rembg import new_session, remove

model_name = "isnet-general-use"
session = new_session(model_name)
output = remove(input, session=session)
```

### Processing multiple images

By default, `remove` initialises a new session every call, which can be a bottleneck when processing multiple images. Initialise a session once and reuse it:

```python
from rembg import new_session, remove

session = new_session(model_name)
for img in images:
    output = remove(img, session=session)
```

### Alpha matting

Alpha matting is a post-processing step that can improve output quality:

```python
output = remove(
    input,
    alpha_matting=True,
    alpha_matting_foreground_threshold=270,
    alpha_matting_background_threshold=20,
    alpha_matting_erode_size=11,
)
```

### Only mask

To return only the segmentation mask:

```python
output = remove(input, only_mask=True)
```

### Post-processing the mask

```python
output = remove(input, post_process_mask=True)
```

### Replacing the background color

```python
output = remove(input, bgcolor=(255, 255, 255, 255))
```

### Using input points (SAM model only)

```python
import numpy as np
from rembg import new_session, remove

session = new_session("sam")

input_points = np.array([[400, 350], [700, 400], [200, 400]])
input_labels = np.array([1, 1, 2])

output = remove(
    image,
    session=session,
    input_points=input_points,
    input_labels=input_labels,
)
```

## Docker

### Building and running

```sh
docker build -t rembg .
docker run -p 7000:7000 rembg
```

The Dockerfile is based on `python:3.10-slim`, installs the package with the `[cpu,cli]` extras, pre-downloads the `u2net` model, exposes port `7000`, and uses `rembg` as the entry point.

### GPU variant

An alternative `Dockerfile_nvidia_cuda_cudnn_gpu` is provided for GPU (CUDA/cuDNN) environments.

### Docker Compose

A `docker-compose.yml` is included. You can configure it via a `.env` file in the root folder:

```env
PUBLIC_PORT=7000:7000
REPLICAS_COUNT=1
```

```sh
docker compose up
```

## Configuration

### Model cache location

Downloaded models are stored in a local cache directory (by default `~/.u2net/`). On first use, each model is retrieved from the project's GitHub releases and verified by checksum (MD5) where available.

### Session options

The `new_session` function accepts additional keyword arguments depending on the model:

- `model_path` — path to a custom ONNX model file (for custom sessions).
- `sam_model` — SAM model variant (e.g. `sam_vit_b_01ec64`, `sam_vit_h_4b8939`).
- `sam_quant` — whether to use quantized SAM model files.
- `cc` / `cloth_category` — for `u2net_cloth_seg`, one of `upper`, `lower`, or `full` (default: all three).
- `sam_prompt` — a list of prompt dictionaries for SAM (point or rectangle prompts), validated with JSON Schema.

## Development

### Setting up a development environment

```sh
git clone https://github.com/danielgatis/rembg.git
cd rembg
pip install -e ".[dev,cpu,cli]"
```

The `[dev]` extra installs linting and testing tools:

- `black`, `isort`, `flake8` — formatting and linting
- `mypy` — static type checking
- `bandit` — security analysis
- `pytest` — testing
- `twine`, `wheel` — packaging

### Versioning

Version numbers are managed with [Versioneer](https://github.com/python-versioneer/python-versioneer). The version is derived from Git tags (prefix `v`), so releases are made by tagging. The generated version file is `rembg/_version.py`.

### Project structure

```
rembg/
├── rembg/
│   ├── bg.py               # Core remove() logic
│   ├── cli.py              # CLI entry point
│   ├── session_factory.py  # Session factory
│   ├── commands/           # CLI subcommands (b, d, i, p, s)
│   └── sessions/           # Model session implementations
├── tests/
│   ├── fixtures/           # Test input images
│   ├── results/            # Expected output masks per model
│   └── test_remove.py      # Test suite
├── examples/               # Example input/output images
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── setup.py
└── setup.cfg
```

## Testing

Tests are run with [pytest](https://pytest.org/):

```sh
pytest
```

The test suite (`tests/test_remove.py`) exercises the `remove` function against a set of fixture images (anime character, car, clothing, plants) and compares the output against pre-computed reference masks (`tests/results/`) for each supported model. Deprecation warnings are suppressed via `pytest.ini`.

## CI/CD

The repository includes GitHub Actions workflows for:

- Python linting (`lint_python.yml`)
- PyPI package publishing (`publish_pypi.yml`)
- Docker image publishing (`publish_docker.yml`)
- Installation testing (`test_install.yml`)
- Windows installer building (`windows_installer.yml`)
- Closing inactive issues (`close_inactive_issues.yml`)

## Examples

The `examples/` directory contains sample input images and corresponding background-removed outputs for animals, anime characters, cars, food, people, and plants.

## Contributing

Bug reports and feature requests are welcome via the GitHub issue templates. When reporting a bug, please include:

- A description of the problem and steps to reproduce
- Input images that demonstrate the issue
- Your OS version and rembg version

Feature requests should describe the problem, the proposed solution, and any alternatives considered.

## Citing

If you use rembg in your research, please cite it using the metadata in `CITATION.cff`.

## License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

Copyright (c) 2020 Daniel Gatis.

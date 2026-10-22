# rembg

rembg removes the background from images. It wraps a set of pretrained ONNX segmentation models behind a Python library, a command-line interface, a FastAPI-based HTTP server with a Gradio web UI, and a Docker image. The package is published on PyPI as `rembg`, and the project is released under the MIT License.

## Overview

The project provides several ways to use the same background-removal pipeline:

- **Python library**: `remove()` and `new_session()` functions that accept bytes, PIL images, or NumPy arrays.
- **Command-line interface**: the `rembg` command with subcommands for single files, byte streams, folders, model downloads, and an HTTP server.
- **HTTP server**: a REST API with interactive documentation at `/api` and a Gradio user interface at `/`.
- **Docker**: a `Dockerfile` and `docker-compose.yml` for running the server in a container.
- **Windows installer**: a PowerShell build script and Inno Setup scripts that produce `rembg-cli-installer.exe`.
- **Google Colab notebook**: `rembg.ipynb` installs the package with GPU and CLI extras and launches a Gradio app.

The package requires Python `>=3.10, <3.14`. Supported Python versions listed in the package metadata are 3.10 through 3.13.

## Installation

Install from PyPI with one of the extras that selects the ONNX Runtime variant:

```bash
pip install "rembg[cpu,cli]"     # CPU runtime plus CLI and server dependencies
pip install "rembg[gpu,cli]"     # onnxruntime-gpu (CUDA)
pip install "rembg[rocm,cli]"    # onnxruntime-rocm
```

The available extras are:

| Extra | Installs |
|-------|----------|
| `cpu` | `onnxruntime` |
| `gpu` | `onnxruntime-gpu` |
| `rocm` | `onnxruntime-rocm` |
| `cli` | `aiohttp`, `asyncer`, `click`, `fastapi`, `filetype`, `gradio`, `python-multipart`, `uvicorn`, `watchdog` |
| `dev` | `bandit`, `black`, `flake8`, `imagehash`, `isort`, `mypy`, `pytest`, `setuptools`, `twine`, `wheel` |

The core dependencies are `jsonschema`, `numpy`, `opencv-python-headless`, `pillow`, `pooch`, `pymatting`, `scikit-image`, `scipy`, and `tqdm`.

The repository includes an `onnxruntime-installation-matrix.png` image, which is intended to help choose the appropriate ONNX Runtime package for a given platform.

To install from a local checkout, run `pip install .[cpu,cli]` from the repository root.

### Docker

The included `Dockerfile` uses `python:3.10-slim`, installs the project with `.[cpu,cli]`, and pre-downloads the `u2net` model during the build. It exposes port 7000 and uses `rembg` as its entrypoint, with `--help` as the default command.

```bash
docker build -t rembg .
docker run -p 7000:7000 rembg s
```

`docker-compose.yml` defines a single service named `app` that builds the image and runs the `s` (server) command. Its ports and replica count are controlled through environment variables (see [Configuration](#configuration)).

```bash
docker compose up
```

The repository also contains a `Dockerfile_nvidia_cuda_cudnn_gpu` file. Its contents are not described in this README.

## Usage

### Command-line interface

The `rembg` command provides five subcommands:

| Command | Purpose |
|---------|---------|
| `rembg i` | Process a single file (input and output may be stdin/stdout) |
| `rembg b WIDTH HEIGHT` | Process a raw RGB byte stream from stdin |
| `rembg p INPUT_DIR OUTPUT_DIR` | Process every file in a folder |
| `rembg d [MODELS...]` | Download models (all models if none are given) |
| `rembg s` | Start the HTTP server |

Examples:

```bash
rembg i input.png output.png
rembg i -m isnet-general-use -a input.png output.png
rembg p -m u2net -ppm inputs/ outputs/
rembg p -w inputs/ outputs/        # watch the input folder for new files
rembg d u2net isnet-general-use
rembg --version
```

Common options for `i`, `b`, and `p`:

- `-m, --model`: model name (default `u2net`).
- `-a, --alpha-matting`: enable alpha matting.
- `-af`, `-ab`, `-ae`: alpha matting foreground threshold (default 240), background threshold (default 10), and erode size (default 10).
- `-om, --only-mask`: output only the mask.
- `-ppm, --post-process-mask`: post-process the mask.
- `-bgc, --bgcolor R G B A`: replace the removed background with a colour.
- `-x, --extras`: extra arguments as a JSON string, passed to the session and `remove()`.

The `p` command also supports `-w, --watch` to monitor the input folder and `-d, --delete_input` to delete source files after processing. The `b` command supports `-o, --output_specifier`, a printf-style pattern for output filenames such as `output-%d.png`.

### HTTP server

Start the server with:

```bash
rembg s --host 0.0.0.0 --port 7000
```

When started, the server attempts to open a browser at `http://localhost:<port>`. It exposes:

- `GET /api/remove?url=<image-url>`: fetches an image from a URL and returns a PNG.
- `POST /api/remove`: accepts an uploaded image file as multipart form data and returns a PNG.
- `/api`: interactive API documentation.
- `/`: a Gradio interface with input image, model dropdown, alpha matting controls, and an extra arguments field.

Shared query parameters are `model`, `a`, `af`, `ab`, `ae`, `om`, `ppm`, `bgc` (formatted as `R,G,B,A`), and `extras` (JSON). In the POST endpoint, the model and processing options are form fields, while `bgc` and `extras` remain query parameters.

### Python API

```python
from PIL import Image
from rembg import new_session, remove

input_image = Image.open("input.png")
output = remove(input_image)
output.save("output.png")
```

To reuse a model across many images, create a session once and pass it in:

```python
session = new_session("isnet-general-use")
for path in paths:
    result = remove(Image.open(path), session=session)
```

`remove()` accepts `bytes`, `PIL.Image.Image`, or `numpy.ndarray` input. Its return type matches the input type, except that `force_return_bytes=True` forces PNG bytes. Other supported keyword arguments include:

- `alpha_matting`, with `alpha_matting_foreground_threshold` (240), `alpha_matting_background_threshold` (10), and `alpha_matting_erode_size` (10).
- `only_mask`, `post_process_mask`, and `bgcolor` (an RGBA tuple).
- `putalpha`, which applies the mask as the image's alpha channel.

Per the code, if no session is given, `remove()` creates one with `new_session("u2net")`. Calling `remove()` without a session therefore reinitialises the model on every call.

### Models

The following model names are registered in `rembg/sessions/__init__.py`:

- BiRefNet: `birefnet-general`, `birefnet-general-lite`, `birefnet-portrait`, `birefnet-dis`, `birefnet-hrsod`, `birefnet-cod`, `birefnet-massive`
- IS-Net: `isnet-general-use`, `isnet-anime`
- U2-Net family: `u2net`, `u2netp`, `u2net_human_seg`, `u2net_cloth_seg`
- Others: `sam`, `silueta`, `bria-rmbg`

Three sessions require a local model file and a `model_path` keyword argument: `u2net_custom`, `dis_custom`, and `ben_custom`. Their `download_models` methods return the expanded path given in `model_path`.

The `sam` session reads a `sam_prompt` keyword argument, a list of prompt items with `type` (`point` or `rectangle`), `label`, and `data`. It also accepts `sam_model` (default `sam_vit_b_01ec64`) and `sam_quant`. When no prompt is provided, it uses the image centre as a single positive point. Note that `USAGE.md` describes `input_points` and `input_labels` arguments for SAM, but the code in `rembg/sessions/sam.py` reads `sam_prompt`.

Model weights are downloaded on first use, or ahead of time with `rembg d`. The CI test workflow shows that some models are fetched from GitHub release assets, and the sessions verify MD5 or SHA-256 checksums unless checksum verification is disabled.

## Configuration

### Environment variables

| Variable | Effect |
|----------|--------|
| `U2NET_HOME` | Directory for model files. Defaults to `$XDG_DATA_HOME/.u2net` if `XDG_DATA_HOME` is set, otherwise `~/.u2net`. |
| `MODEL_CHECKSUM_DISABLED` | When set (to any value), skips checksum verification for downloaded models. |
| `OMP_NUM_THREADS` | Sets ONNX Runtime's inter-op and intra-op thread counts. |
| `PUBLIC_PORT` | Used by `docker-compose.yml` for the port mapping (default `7000:7000`). |
| `REPLICAS_COUNT` | Used by `docker-compose.yml` for the replica count (default `1`). |

Docker Compose reads these values from a `.env` file in the project root, as noted in the file's comments.

### Server options

`rembg s` accepts `-p/--port` (default 7000), `-h/--host` (default `0.0.0.0`), `-l/--log_level` (default `info`), and `-t/--threads` (number of worker threads for the anyio capacity limiter).

## Development

Clone the repository and install in editable mode with the development extras:

```bash
git clone https://github.com/danielgatis/rembg.git
cd rembg
pip install -e ".[cpu,cli,dev]"
```

The package is built with `setuptools`. Versions are computed from git tags by `versioneer` (configured in `setup.cfg` and `pyproject.toml`), using the `v` tag prefix and PEP 440 style. The generated `rembg/_version.py` contains the version lookup logic. Entry point: `rembg = rembg.cli:main`. The top-level `rembg.py` also exposes `main()` for running the module directly.

The lint workflow (`.github/workflows/lint_python.yml`) runs these checks on the `rembg` package:

- `mypy --ignore-missing-imports ./rembg`
- `bandit` with several checks skipped
- `black --check`
- `flake8` with a specific ignore list
- `isort --check-only --profile black`

Markdown linting is configured in `.markdownlint.yaml`, which disables the line-length and inline-HTML rules. Editor settings are in `.editorconfig`.

## Testing

Tests live in `tests/test_remove.py`. They run each supported model against four fixture images (`anime-girl-1`, `car-1`, `cloth-1`, `plants-1`) and compare the perceptual hash (`imagehash.phash`) of each output against the reference PNGs in `tests/results/`. The test file contains commented code showing how to regenerate expected results.

Models must be downloaded first:

```bash
rembg d
pytest
```

`pytest.ini` suppresses `DeprecationWarning` messages. The `test_install.yml` workflow runs on pushes for Python 3.10 through 3.13. It retries `rembg d` up to five times before running `pytest`.

## Continuous integration and releases

The `.github/workflows` directory contains:

- `lint_python.yml`: linting on pushes and pull requests.
- `test_install.yml`: installation and tests on Python 3.10–3.13.
- `publish_pypi.yml`: builds and uploads to PyPI on tags matching `v*.*.*`.
- `publish_docker.yml`: builds and pushes a Docker image for `linux/amd64` on version tags.
- `windows_installer.yml`: runs `_build-exe.ps1`, compiles `_setup.iss` with Inno Setup, and uploads `rembg-cli-installer.exe` to the release.
- `close_inactive_issues.yml`: a scheduled job that marks issues stale after 30 days and closes them 14 days later. Pull requests are not affected.

Issue templates for bug reports and feature requests are in `.github/ISSUE_TEMPLATE/`.

## Examples

The `examples/` directory contains input images (for example `animal-1.jpg`, `car-1.jpg`, `girl-1.jpg`) paired with output PNGs such as `animal-1.out.png`. The `food-1.out.alpha.jpg` file shows a separate alpha output.

## Citation

`CITATION.cff` is included in the repository for citing the project.

## License

rembg is released under the MIT License. The license text is in `LICENSE.txt` and is copyright (c) 2020 Daniel Gatis. The package metadata references this file through `license_files`.

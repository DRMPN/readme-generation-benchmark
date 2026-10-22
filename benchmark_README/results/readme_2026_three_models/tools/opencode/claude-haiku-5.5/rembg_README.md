# rembg

rembg removes the background from images. It wraps several pretrained ONNX segmentation models behind a Python API, a command-line interface, and an HTTP server with a web UI.

| Input | Output |
| --- | --- |
| ![Input](examples/car-1.jpg) | ![Output](examples/car-1.out.png) |
| ![Input](examples/girl-1.jpg) | ![Output](examples/girl-1.out.png) |

## Contents

- [Features](#features)
- [Installation](#installation)
- [Python API](#python-api)
- [Command-line interface](#command-line-interface)
- [HTTP server](#http-server)
- [Docker](#docker)
- [Models](#models)
- [Environment variables](#environment-variables)
- [Development](#development)
- [License](#license)

## Features

- Background removal from file paths, raw bytes, Pillow images, or NumPy arrays.
- Choice of 16 built-in models, plus three options for custom ONNX models (`u2net_custom`, `dis_custom`, and `ben_custom`).
- Optional alpha matting, mask post-processing, mask-only output, and solid background colour replacement.
- Interactive point and rectangle prompts for the SAM model.
- CLI commands for single files, byte streams, and folders (with optional watch mode).
- FastAPI server with a Gradio web UI and an OpenAPI docs page.

## Installation

rembg requires Python 3.10 to 3.13.

Install the package with one ONNX Runtime extra that matches your hardware:

```bash
pip install "rembg[cpu]"        # CPU
pip install "rembg[gpu]"        # NVIDIA GPU (onnxruntime-gpu)
pip install "rembg[rocm]"       # AMD GPU (onnxruntime-rocm)
```

To use the command-line interface and HTTP server, also install the `cli` extra:

```bash
pip install "rembg[cpu,cli]"
```

To install from a local clone:

```bash
pip install ".[cpu,cli]"
```

Model files are downloaded on first use. To download them ahead of time, run:

```bash
rembg d                  # all models
rembg d u2net isnet-general-use   # specific models
```

## Python API

```python
from PIL import Image
from rembg import new_session, remove

input_image = Image.open("input.png")
output = remove(input_image)
output.save("output.png")
```

`remove` accepts `bytes`, a PIL `Image`, or a NumPy `ndarray` and returns the same kind of object. Bytes input returns PNG bytes. Pass `force_return_bytes=True` to get bytes from any input type.

### Reusing a session

By default, `remove` creates a new session on every call. When processing several images, create one session and reuse it:

```python
from rembg import new_session, remove

session = new_session("isnet-general-use")
for path in image_paths:
    with open(path, "rb") as f:
        result = remove(f.read(), session=session)
```

### Options

| Argument | Default | Description |
| --- | --- | --- |
| `alpha_matting` | `False` | Refine edges with alpha matting. |
| `alpha_matting_foreground_threshold` | `240` | Trimap foreground threshold. |
| `alpha_matting_background_threshold` | `10` | Trimap background threshold. |
| `alpha_matting_erode_size` | `10` | Erosion size applied to the trimap. |
| `only_mask` | `False` | Return the mask instead of the cutout. |
| `post_process_mask` | `False` | Smooth the mask with morphological opening and Gaussian blur. |
| `bgcolor` | `None` | RGBA tuple, e.g. `(255, 255, 255, 255)`, used to fill the background. |
| `force_return_bytes` | `False` | Return PNG bytes regardless of input type. |

Example:

```python
output = remove(
    input_image,
    alpha_matting=True,
    alpha_matting_foreground_threshold=270,
    alpha_matting_background_threshold=20,
    alpha_matting_erode_size=11,
)
```

Arguments not listed above are passed to the session when it is created (`new_session`) and to its `predict` method.

### Choosing a model

```python
session = new_session("birefnet-general")
output = remove(input_image, session=session)
```

If no session is given, `remove` uses `u2net`.

### SAM prompts

The `sam` model accepts prompts through the `sam_prompt` argument. Each prompt is a dict with `type`, `label`, and `data`:

- `{"type": "point", "label": 1, "data": [x, y]}`: a point. The `label` is passed to the model as-is.
- `{"type": "rectangle", "data": [x1, y1, x2, y2]}`: a bounding box. Its corners are sent to the model as two points with fixed labels, so `label` is not used.

```python
session = new_session("sam")
output = remove(
    input_image,
    session=session,
    sam_prompt=[{"type": "point", "label": 1, "data": [400, 165]}],
)
```

Without `sam_prompt`, SAM uses a single foreground point at the centre of the image.

The SAM encoder and decoder are selected with `sam_model` (default `sam_vit_b_01ec64`) and quantised variants are enabled with `sam_quant=True`. The `sam_vit_h_4b8939` model is also supported by the download code.

### Custom ONNX models

`u2net_custom`, `dis_custom`, and `ben_custom` load a local ONNX file. Pass its path as `model_path`:

```python
session = new_session("u2net_custom", model_path="/path/to/model.onnx")
```

### Cloth segmentation

The `u2net_cloth_seg` model takes a `cloth_category` argument (or its alias `cc`) with the value `upper`, `lower`, or `full`.

```python
session = new_session("u2net_cloth_seg")
output = remove(input_image, session=session, cloth_category="upper")
```

## Command-line interface

After installing with the `cli` extra, the `rembg` command is available. Each subcommand has its own help:

```bash
rembg --help
rembg i --help
```

| Command | Input | Purpose |
| --- | --- | --- |
| `rembg i INPUT OUTPUT` | One image file | Process a single file. |
| `rembg b WIDTH HEIGHT` | Raw RGB bytes on stdin | Process a stream of fixed-size frames. |
| `rembg p INPUT_DIR OUTPUT_DIR` | A folder | Process every image in a folder. |
| `rembg s` | None | Start the HTTP server. |
| `rembg d [MODELS...]` | None | Download models. |

Input and output for `i` default to stdin and stdout when they are omitted:

```bash
rembg i -m u2net input.png output.png
cat input.png | rembg i > output.png
```

### Shared options

These options apply to `i`, `b`, and `p`:

| Option | Default | Description |
| --- | --- | --- |
| `-m`, `--model` | `u2net` | Model name. |
| `-a`, `--alpha-matting` | off | Use alpha matting. |
| `-af`, `--alpha-matting-foreground-threshold` | `240` | Trimap foreground threshold. |
| `-ab`, `--alpha-matting-background-threshold` | `10` | Trimap background threshold. |
| `-ae`, `--alpha-matting-erode-size` | `10` | Erosion size. |
| `-om`, `--only-mask` | off | Output only the mask. |
| `-ppm`, `--post-process-mask` | off | Post-process the mask. |
| `-bgc`, `--bgcolor R G B A` | `0 0 0 0` | Background colour. |
| `-x`, `--extras` | none | Extra options as a JSON object, e.g. `'{"sam_prompt": [...]}'`. |

### `p`: folders

```bash
rembg p -m isnet-general-use input_dir output_dir
```

Output files are written to `output_dir` with a `.png` extension. Existing outputs are skipped.

- `-w`, `--watch`: keep running and process new files that appear in `input_dir`. To stop watching, create a file named `stop.txt` in `input_dir`.
- `-d`, `--delete_input`: delete each input file after it is processed.

### `b`: byte streams

`b` reads raw 8-bit RGB frames of the given width and height from stdin, one frame after another, and writes a PNG for each frame to stdout. Use `-o` with a printf-style pattern to write files instead, for example `-o 'out/frame-%d.png'`.

### `s`: server options

These are also listed under [HTTP server](#http-server).

## HTTP server

Start the server:

```bash
rembg s --host 0.0.0.0 --port 7000
```

| Option | Default | Description |
| --- | --- | --- |
| `-p`, `--port` | `7000` | Port. |
| `-h`, `--host` | `0.0.0.0` | Host address. |
| `-l`, `--log_level` | `info` | Log level. |
| `-t`, `--threads` | none | Number of worker threads. |

When the server starts, it prints the URLs for the web UI and the API documentation, and it tries to open the web UI in a browser.

- Web UI: `http://localhost:7000/`
- API docs (Swagger UI): `http://localhost:7000/api`

### Endpoints

Both endpoints return a PNG image.

**`POST /api/remove`** uploads an image as multipart form data:

```bash
curl -X POST -F "file=@input.png" "http://localhost:7000/api/remove?model=u2net" -o output.png
```

**`GET /api/remove`** fetches an image from a URL:

```bash
curl "http://localhost:7000/api/remove?url=https://example.com/input.jpg&model=u2net" -o output.png
```

Query parameters for both endpoints:

| Parameter | Default | Description |
| --- | --- | --- |
| `model` | `u2net` | Model name. |
| `a` | `false` | Enable alpha matting. |
| `af` | `240` | Foreground threshold (0 to 255). |
| `ab` | `10` | Background threshold (0 to 255). |
| `ae` | `10` | Erosion size. |
| `om` | `false` | Return only the mask. |
| `ppm` | `false` | Post-process the mask. |
| `bgc` | none | Background colour as `R,G,B,A`. |
| `extras` | none | Extra options as JSON. |

For `POST`, `model`, `a`, `af`, `ab`, `ae`, `om`, and `ppm` are form fields. `bgc` and `extras` remain query parameters. The `GET` endpoint takes the image URL in the `url` parameter.

## Docker

The repository includes a `Dockerfile` (CPU, Python 3.10) and `Dockerfile_nvidia_cuda_cudnn_gpu` (NVIDIA CUDA 12.4 with cuDNN). Both install the package with the `cli` extra, download the `u2net` model at build time, and set `rembg` as the entrypoint.

Build and run the CPU image:

```bash
docker build -t rembg .
docker run -p 7000:7000 rembg s
```

Build and run the GPU image:

```bash
docker build -f Dockerfile_nvidia_cuda_cudnn_gpu -t rembg-gpu .
docker run --gpus all -p 7000:7000 rembg-gpu s
```

`docker-compose.yml` runs the server with `s` as the command. It reads the optional `.env` variables `PUBLIC_PORT` (default `7000:7000`) and `REPLICAS_COUNT` (default `1`).

## Models

rembg can load these model names with `new_session(name)` or `-m name`:

| Name | Notes |
| --- | --- |
| `u2net` | Default model. |
| `u2netp` | U2-Net variant. |
| `u2net_human_seg` | U2-Net trained for human segmentation. |
| `u2net_cloth_seg` | Clothing segmentation; takes `cloth_category` (`upper`, `lower`, `full`). |
| `silueta` | |
| `isnet-general-use` | |
| `isnet-anime` | Anime-style images. |
| `sam` | Promptable segmentation; see [SAM prompts](#sam-prompts). |
| `birefnet-general` | |
| `birefnet-general-lite` | |
| `birefnet-portrait` | |
| `birefnet-dis` | |
| `birefnet-hrsod` | |
| `birefnet-cod` | |
| `birefnet-massive` | |
| `bria-rmbg` | |
| `u2net_custom` | Custom local ONNX model; requires `model_path`. |
| `dis_custom` | Custom local ONNX model; requires `model_path`. |
| `ben_custom` | Custom local ONNX model; requires `model_path`. |

Model files are downloaded from the project's GitHub releases on first use and cached in `~/.u2net` (see `U2NET_HOME` below). The `u2net` model is verified against an MD5 checksum unless `MODEL_CHECKSUM_DISABLED` is set.

The `tests/results` directory contains reference outputs for the test fixtures, one per model and image pair.

## Environment variables

| Variable | Description |
| --- | --- |
| `U2NET_HOME` | Directory for downloaded model files. Defaults to `$XDG_DATA_HOME/.u2net`, or `~/.u2net` when `XDG_DATA_HOME` is unset. |
| `MODEL_CHECKSUM_DISABLED` | When set to any value, skips MD5 verification of downloaded models. |
| `OMP_NUM_THREADS` | When set, sets the ONNX Runtime inter-op and intra-op thread counts for new sessions. |

## Development

Clone the repository and install the development dependencies:

```bash
pip install ".[cpu,cli,dev]"
rembg d
pytest
```

The test suite in `tests/test_remove.py` runs each model on the fixtures in `tests/fixtures` and compares perceptual hashes against the files in `tests/results`. It requires the model files to be downloaded first.

The CI workflows in `.github/workflows` run:

- `lint_python.yml`: mypy, bandit, black, flake8, and isort on `rembg/`.
- `test_install.yml`: installs the package and runs `pytest` on Python 3.10 to 3.13.
- `publish_docker.yml`: builds and pushes the Docker image for version tags.

Windows installer files are also present (`_setup.iss`, `_build-exe.ps1`, `rembg.spec`) for building a `rembg-cli-installer` executable.

## License

rembg is released under the MIT License. See [LICENSE.txt](LICENSE.txt).

The pretrained models are downloaded from the project's release assets; check each model's original license before using it in a commercial product.

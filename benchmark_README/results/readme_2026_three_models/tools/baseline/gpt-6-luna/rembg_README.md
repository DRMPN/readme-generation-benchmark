# rembg

`rembg` is a Python tool for removing image backgrounds. It provides a Python API, command-line tools, and an HTTP server with a web interface. It runs ONNX models through ONNX Runtime and downloads model files when needed.

The repository includes example input and output images, a notebook, and tests with image fixtures and expected results. The package supports Python 3.10–3.13.

## Installation

Install the package with a runtime backend and, if you want the command-line tools or server, the CLI extra:

```bash
python -m pip install "rembg[cpu,cli]"
```

Choose one ONNX Runtime backend:

- `cpu` installs `onnxruntime`.
- `gpu` installs `onnxruntime-gpu`.
- `rocm` installs `onnxruntime-rocm`.

For example, to install the CLI with the GPU backend:

```bash
python -m pip install "rembg[gpu,cli]"
```

The package’s base dependencies include image-processing and numerical libraries. The `cli` extra supplies the dependencies for the command-line and server features; the `dev` extra supplies development and test tools.

## Python API

The main API functions are `remove` and `new_session`. By default, `remove` uses the `u2net` model. It accepts image bytes, a Pillow image, or a NumPy array. Its result matches the input form: bytes, a Pillow image, or an array.

```python
from PIL import Image
from rembg import remove

image = Image.open("input.png")
result = remove(image)
result.save("output.png")
```

To select a model, create a session and pass it to `remove`:

```python
from rembg import new_session, remove

session = new_session("isnet-general-use")
result = remove(image, session=session)
result.save("output.png")
```

Creating a session once and reusing it is useful when processing multiple images, instead of relying on `remove` to create a session for each call.

Optional processing includes alpha matting, mask-only output, mask post-processing, and replacing the background with an RGBA color:

```python
result = remove(
    image,
    alpha_matting=True,
    alpha_matting_foreground_threshold=240,
    alpha_matting_background_threshold=10,
    alpha_matting_erode_size=10,
    post_process_mask=True,
)
```

Use `only_mask=True` to return the mask. Set `bgcolor=(255, 255, 255, 255)` to composite the cutout onto white. See [`USAGE.md`](USAGE.md) for additional examples.

## Models

The model registry includes:

- `u2net`, `u2netp`, `u2net_human_seg`, and `u2net_cloth_seg`
- `isnet-general-use`, `isnet-anime`, and `silueta`
- `birefnet-general`, `birefnet-general-lite`, `birefnet-portrait`, `birefnet-dis`, `birefnet-hrsod`, and `birefnet-cod`, `birefnet-massive`
- `sam` and `bria-rmbg`
- `u2net_custom`, `dis_custom`, and `ben_custom`

Most models are downloaded on demand and cached locally. Custom models require a `model_path` argument when creating a session. `sam` accepts prompts through the `sam_prompt` argument; the test suite and server use prompt data for this model.

## Command line

The installed command is `rembg`. See the available commands and options with:

```bash
rembg --help
rembg i --help
```

The command groups are:

- `d` downloads model files. With no model names, it downloads all registered models; provide names to download selected models.
- `i` processes an image file or byte stream. For example:

  ```bash
  rembg i -m isnet-general-use input.jpg output.png
  ```

  When input and output are omitted in a non-interactive context, the command reads from standard input and writes to standard output.
- `p` processes images in a folder and writes PNGs to an output folder:

  ```bash
  rembg p input_folder output_folder
  ```

  It can watch the input folder for changes and optionally delete input files after processing.
- `b` processes a stream of raw RGB images. Specify the image width and height as arguments; an optional output filename specifier writes individual PNGs to files.
- `s` starts the HTTP server and web UI.

The image-processing commands support options for selecting a model, enabling alpha matting, changing its thresholds and erosion size, returning only the mask, post-processing the mask, and specifying a background color. Some commands also accept extra model arguments as JSON.

## HTTP server

Install the `cli` extra, then start the server:

```bash
rembg s
```

The default host is `0.0.0.0` and the default port is `7000`. The web UI is served at `/`, and API documentation is available at `/api`. The API provides `GET /api/remove` for retrieving an image from a URL and `POST /api/remove` for processing an uploaded image. Both support query parameters for model selection and processing options.

## Configuration and model storage

Model files are stored under `~/.u2net` by default. Set `U2NET_HOME` to choose another model directory. If `U2NET_HOME` is not set, the code uses `$XDG_DATA_HOME/.u2net` when `XDG_DATA_HOME` is set; otherwise it uses `~/.u2net`.

Set `MODEL_CHECKSUM_DISABLED` to disable model checksum verification. When `OMP_NUM_THREADS` is set, `new_session` uses its value to configure ONNX Runtime’s inter-op and intra-op thread counts.

The server accepts `--host`, `--port`, `--log_level`, and `--threads` options. The Docker Compose configuration starts the server on port 7000 by default. Its root `.env` file can set `PUBLIC_PORT` and `REPLICAS_COUNT`.

## Docker

The default `Dockerfile` builds a CPU-based image, installs the CPU and CLI extras, and downloads the `u2net` model during the build. It exposes port 7000. To build and run the server with Compose:

```bash
docker compose up --build
```

Compose starts the `s` server command. The repository also contains a separate NVIDIA CUDA/cuDNN Dockerfile.

## Development

Clone the repository, then install the package in editable mode with CPU, CLI, and development dependencies:

```bash
python -m pip install -e ".[cpu,cli,dev]"
```

The development extra includes pytest, Black, Flake8, isort, mypy, Bandit, and packaging tools. The GitHub lint workflow runs mypy, Bandit, Black, Flake8, and isort against `rembg`.

## Testing

Run the test suite from the repository root:

```bash
pytest
```

`tests/test_remove.py` exercises registered models against image fixtures and compares perceptual hashes with expected output images. Tests may need network access to download model files, and the suite runs inference for multiple model and image combinations.

## License

This project is distributed under the MIT License. See [`LICENSE.txt`](LICENSE.txt) for the complete license text.

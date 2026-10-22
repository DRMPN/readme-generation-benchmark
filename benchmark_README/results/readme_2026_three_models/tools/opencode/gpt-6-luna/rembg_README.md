# rembg

`rembg` is a Python tool and library for removing image backgrounds. It runs ONNX models and can return a transparent cutout or a mask. The package includes a Python API and command implementations for processing files, folders, byte streams, and images through an HTTP server.

## Requirements and installation

Python `>=3.10, <3.14` is required. Install the package with an ONNX Runtime backend that matches your environment:

```bash
pip install "rembg[cpu]"
```

The project also defines `gpu` and `rocm` extras, which install `onnxruntime-gpu` and `onnxruntime-rocm` respectively. Choose one backend appropriate for your system. To install the additional dependencies used by the command implementations, include the `cli` extra:

```bash
pip install "rembg[cpu,cli]"
```

When installing from a source checkout, use `pip install ".[cpu,cli]"` instead. Model files are downloaded when a model session is created; `rembg d` is the explicit model-download command in the CLI implementation. Models are stored under `~/.u2net` by default. Set `U2NET_HOME` to change that location.

## Python API

`remove` accepts image bytes, a Pillow image, or a NumPy array. It returns bytes, a Pillow image, or an array of the corresponding type. Byte input produces PNG bytes.

```python
from pathlib import Path

from rembg import remove

input_bytes = Path("input.jpg").read_bytes()
output_bytes = remove(input_bytes)
Path("output.png").write_bytes(output_bytes)
```

The default model is `u2net`. To select another model, create a session with `new_session` and pass it to `remove`:

```python
from PIL import Image
from rembg import new_session, remove

session = new_session("isnet-general-use")
image = Image.open("input.jpg")
result = remove(image, session=session)
result.save("output.png")
```

Reuse a session when processing multiple images rather than creating one for every call:

```python
session = new_session("u2net")

for input_path in input_paths:
    image = Image.open(input_path)
    result = remove(image, session=session)
    result.save(output_path_for(input_path))
```

Optional arguments include:

| Argument | Default | Purpose |
| --- | --- | --- |
| `alpha_matting` | `False` | Apply alpha matting to the cutout. |
| `alpha_matting_foreground_threshold` | `240` | Foreground threshold for alpha matting. |
| `alpha_matting_background_threshold` | `10` | Background threshold for alpha matting. |
| `alpha_matting_erode_size` | `10` | Erosion size for alpha matting. |
| `only_mask` | `False` | Return the mask instead of a cutout. |
| `post_process_mask` | `False` | Apply mask post-processing. |
| `bgcolor` | `None` | Replace the removed background with an RGBA color tuple, for example `(255, 255, 255, 255)`. |

The `input_points` and `input_labels` arguments are supported by the `sam` model for point-guided masks. See [`USAGE.md`](USAGE.md) for examples of these options and alpha matting.

## Models

The model names registered by this version of the package are:

`ben_custom`, `birefnet-cod`, `birefnet-dis`, `birefnet-general`, `birefnet-general-lite`, `birefnet-hrsod`, `birefnet-massive`, `birefnet-portrait`, `bria-rmbg`, `dis_custom`, `isnet-anime`, `isnet-general-use`, `sam`, `silueta`, `u2net`, `u2net_cloth_seg`, `u2net_custom`, `u2net_human_seg`, and `u2netp`.

For example, download one model explicitly with:

```bash
rembg d u2net
```

With no model names, the download command attempts to download all registered models.

## Command-line interfaces

The source defines these `rembg` subcommands:

| Command | Purpose |
| --- | --- |
| `i` | Process one image file; input and output can also use standard input/output. |
| `p` | Process images in an input folder and write PNGs to an output folder. Supports folder watching. |
| `b` | Read fixed-size RGB images from a byte stream, given the image width and height. |
| `d` | Download one or more model files. |
| `s` | Start the HTTP server and web interface. |

The file and folder commands accept options for model selection, alpha matting, mask-only output, mask post-processing, and background color. For example, the intended file-command form is:

```bash
rembg i -m u2net input.jpg output.png
```

The server command defaults to port `7000`; it provides `POST /api/remove` for uploaded image bytes, `GET /api/remove?url=...` for an image URL, interactive documentation at `/api`, and a web interface at `/`.

**Packaging caveat:** in this checkout, `setup.py` declares the `rembg` console script as `rembg.cli:main`, but `rembg/cli.py` defines `_main` and does not define `main`. The root `rembg.py` also imports `main`. Consequently, the documented console command may fail until that entry-point mismatch is corrected. The command descriptions above reflect the implemented subcommands, not a verified working launcher.

## Development

To install the development dependencies along with the CPU backend and CLI dependencies from a source checkout:

```bash
pip install ".[cpu,cli,dev]"
```

Run the test suite with:

```bash
pytest
```

The tests exercise multiple registered models against image fixtures and expected outputs, so a suitable ONNX Runtime installation and access to the required model files are needed.

## License

This project is distributed under the MIT License. See [`LICENSE.txt`](LICENSE.txt).

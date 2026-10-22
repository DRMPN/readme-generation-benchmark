# rembg

[![PyPI version](https://badge.fury.io/py/rembg.svg)](https://badge.fury.io/py/rembg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

**rembg** is a tool to remove images background.

It bundles several state-of-the-art segmentation models (U²-Net, ISNet/DIS, Segment Anything, BiRefNet, BRIA RMBG, BEN, …), runs them through [ONNX Runtime](https://onnxruntime.ai/) on CPU or CUDA GPU, and exposes them through a simple Python API, a command-line interface and a small HTTP server.

| Input | Output |
| :---: | :---: |
| ![](car-1.jpg) | ![](car-1.out.png) |

> The sample photos and reference results shown above (and used by the test-suite) ship with this repository.

---

## Table of contents

1. [Features](#features)
2. [How it works](#how-it-works)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Quick start](#quick-start)
6. [CLI usage](#cli-usage)
7. [Python usage](#python-usage)
8. [Models](#models)
9. [Docker](#docker)
10. [GPU acceleration](#gpu-acceleration)
11. [Performance tips](#performance-tips)
12. [Running the tests](#running-the-tests)
13. [Repository layout](#repository-layout)
14. [Troubleshooting / FAQ](#troubleshooting--faq)
15. [Citing](#citing)
16. [Acknowledgements](#acknowledgements)
17. [License](#license)

## Features

- Removes backgrounds from photos of people, products, cars, animals, food, plants, clothes and anime characters.
- **Multiple models** to trade off speed vs. quality — from the lightweight `u2netp` (~4 MB) to the massive BiRefNet (~3.5 GB).
- **Python API** (`rembg.remove`), **CLI** (`rembg i|d|p|b|s`) and an **HTTP server** for integration with any language.
- **CPU and GPU (CUDA)** inference via ONNX Runtime.
- **Alpha matting** (via [pymatting](https://github.com/pymatting/pymatting)) for softer, more natural edges.
- **Mask-only output**, mask post-processing and solid background color replacement.
- **Custom ONNX support** — plug in your own fine-tuned weights.
- **Docker images** for CPU and GPU deployments.

## How it works

rembg feeds your image through a pre-trained segmentation network (executed with ONNX Runtime) to obtain a soft foreground mask, then applies that mask as the alpha channel of the image. Models are downloaded on demand and cached locally; a *session* keeps a model loaded in memory so repeated calls stay fast.

## Requirements

- Python **3.8 or newer** (check `setup.cfg` / `pyproject.toml` for the exact supported range of your release).
- `pip`.
- An internet connection on **first use** of each model — weights are downloaded once and cached (see [Models](#models)).

## Installation

**CPU support (default):**

```bash
pip install rembg           # library only
pip install "rembg[cli]"    # library + CLI/server extras
```

Core dependencies (`numpy`, `onnxruntime`, `opencv-python-headless`, `pillow`, `pooch`, `pymatting`, `scipy`, `tqdm`, plus `click`/`aiohttp` for the CLI/server) are installed automatically.

**GPU support (NVIDIA / CUDA):**

GPU inference is provided by `onnxruntime-gpu`. First, check which onnxruntime build is compatible with your CUDA/cuDNN version using the official [support matrix](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html), then install it alongside rembg:

```bash
pip install "rembg[cli]" onnxruntime-gpu
```

**Notebook:**

The repository includes `rembg.ipynb`, a ready-to-run notebook demonstrating the basic API.

## Quick start

**Command line:**

```bash
rembg i car-1.jpg car-1.out.png
```

**Python:**

```python
from rembg import remove
from PIL import Image

input_image = Image.open("car-1.jpg")
result = remove(input_image)        # PIL.Image with alpha channel (RGBA)
result.save("car-1.out.png")
```

> ℹ️ The first call downloads the selected model's weights (e.g. ~170 MB for `u2net`) to the local cache — subsequent runs load them from disk and are fast.

## CLI usage

After installation, verify the `rembg` command is available:

```bash
rembg --version
rembg --help
```

Illustrative help output:

```
Usage: rembg [OPTIONS] COMMAND [ARGS]...

  Rembg is a tool to remove images background.

Commands:
  b  Remove the background from a batch of images
  d  Remove the background from a directory glob
  i  Remove the background from images
  p  HTTP server for removing images background
  s  Download the sample images
```

> Option names can vary slightly between releases — `rembg <command> --help` is always authoritative for the version you have installed.

### `rembg i` — images

```bash
rembg i [OPTIONS] INPUT [OUTPUT]
```

`INPUT`/`OUTPUT` may be `-` (stdin/stdout), local paths, URLs or glob patterns; multiple pairs can be passed in recent versions.

```bash
# local file → local file
rembg i car-1.jpg car-1.out.png

# stdin → stdout (great for pipelines)
curl -s https://example.com/photo.jpg | rembg i > output.png

# pick a model
rembg i -m isnet-anime anime-girl-1.jpg anime-girl-1.out.png
rembg i -m u2net_human_seg girl-1.jpg girl-1.out.png

# alpha matting for finer edges
rembg i -a car-1.jpg car-1.out.png
```

Common options:

| Option | Default | Description |
| ------ | ------- | ----------- |
| `-m, --model` | `u2net` | model to use (see [Models](#models)) |
| `-a, --alpha-matting` | off | enable alpha matting |
| `-af, --alpha-matting-foreground-threshold` | `240` | foreground threshold (0–255) |
| `-ab, --alpha-matting-background-threshold` | `10` | background threshold (0–255) |
| `-ae, --alpha-matting-erode-size` | `10` | erode size for alpha matting |
| `-om, --only-mask` | off | output only the mask |
| `-ppm, --post-process-mask` | off | post-process the mask |
| `-x, --extras` | — | extra session parameters as JSON (custom model paths, SAM prompts) |

### `rembg d` — directories

```bash
rembg d [OPTIONS] INPUT [OUTPUT]
```

Processes every image that matches the input glob and writes the results to the output directory:

```bash
rembg d ./inputs ./outputs
```

### `rembg p` — HTTP server

```bash
rembg p [OPTIONS]
```

Starts an HTTP server (by default on port `5000`) that removes backgrounds. It accepts the usual options (`-m/--model`, alpha-matting flags, …) plus the listening port. This is the easiest way to use rembg from applications written in other languages:

```bash
rembg p -m u2net
```

```bash
curl -sSL -X POST -F "image=@car-1.jpg" "http://localhost:5000"
```

The server replies with JSON containing the base64-encoded result:

```json
{
  "code": 100,
  "output": "iVBORw0KGgoAAAANSUhEUg..."
}
```

### `rembg s` — sample images

```bash
rembg s
```

Downloads the sample images used throughout the documentation and tests (`girl-1.jpg`, `car-1.jpg`, `anime-girl-1.jpg`, `animal-1.jpg`, `cloth-1.jpg`, `food-1.jpg`, `plants-1.jpg`, …).

### `rembg b` — batch

```bash
rembg b [OPTIONS] INPUT [OUTPUT] ...
```

Processes images in batch mode. Run `rembg b --help` for the exact options of your installed version.

## Python usage

### The `remove()` function

`remove()` accepts `bytes`, a `PIL.Image.Image` or a `numpy.ndarray` and returns an image **of the same type** with the background removed (alpha channel applied).

```python
from rembg import remove

# bytes in → PNG bytes out
with open("car-1.jpg", "rb") as i:
    with open("car-1.out.png", "wb") as o:
        output_data = remove(i.read())
        o.write(output_data)
```

```python
import cv2
from rembg import remove

frame = cv2.imread("car-1.jpg")
result = remove(frame)          # np.ndarray (H, W, 4)
```

### Reusing sessions (much faster for batches)

Creating a session downloads/loads the model, so build it once and pass it to every call:

```python
from rembg import remove, new_session

session = new_session("isnet-general-use")

for path in ["car-1.jpg", "plants-1.jpg", "cloth-1.jpg"]:
    with open(path, "rb") as f:
        result = remove(f.read(), session=session)
```

### Options

| Parameter | Default | Description |
| --------- | ------- | ----------- |
| `session` | `None` | session created with `new_session()` — strongly recommended when processing several images |
| `alpha_matting` | `False` | pymatting-based alpha matting for soft edges |
| `alpha_matting_foreground_threshold` | `240` | 0–255 |
| `alpha_matting_background_threshold` | `10` | 0–255 |
| `alpha_matting_erode_size` | `10` | erosion size |
| `only_mask` | `False` | return the segmentation mask instead of the cutout |
| `post_process_mask` | `False` | morphological cleanup of the mask |
| `bgcolor` | `None` | e.g. `(255, 255, 255, 255)` — composite the result over a solid color |
| `sam_prompt` | `None` | prompts for the `sam` model (points / boxes) |

```python
from rembg import remove, new_session

session = new_session("u2net")
result = remove(
    input_image,
    session=session,
    alpha_matting=True,
    alpha_matting_foreground_threshold=240,
    alpha_matting_background_threshold=10,
    alpha_matting_erode_size=10,
    bgcolor=(255, 255, 255, 255),
)
```

### Segment Anything (`sam`) with prompts

The `sam` model needs a prompt telling it which object to keep:

```python
from rembg import remove, new_session

session = new_session("sam")
result = remove(
    input_image,
    session=session,
    sam_prompt=[{"type": "point", "data": [470, 450], "label": 1}],
)
```

See `rembg/sessions/sam.py` and `rembg i --help` for the exact prompt format supported by your version.

## Models

The selected model is downloaded automatically (via [pooch](https://github.com/fatiando/pooch)) on first use and cached in `~/.u2net` — override the location with the `U2NET_HOME` environment variable.

| Model (`-m …`) | Description | Approx. size |
| -------------- | ----------- | ------------ |
| `u2net` *(default)* | General-purpose salient object detection; a good all-rounder | ~176 MB |
| `u2netp` | Lightweight version of u2net — fastest, lower quality | ~4 MB |
| `u2net_human_seg` | Trained for human segmentation | ~170 MB |
| `u2net_cloth_seg` | Extracts clothes from images (upper body, lower body or full body) | ~170 MB |
| `silueta` | Compressed version of u2net | ~43 MB |
| `isnet-general-use` | General-use, high-resolution segmentation | ~174 MB |
| `isnet-anime` | High-accuracy segmentation of anime characters | ~176 MB |
| `sam` | Meta's Segment Anything Model; requires a prompt | ~375 MB |
| `birefnet-general` | BiRefNet trained on a diverse dataset — excellent general quality | ~930 MB |
| `birefnet-general-lite` | BiRefNet with a much smaller footprint | ~190 MB |
| `birefnet-portrait` | BiRefNet fine-tuned on portrait images | ~930 MB |
| `birefnet-dis` | BiRefNet fine-tuned on the DIS dataset | ~930 MB |
| `birefnet-hrsod` | BiRefNet fine-tuned for high-resolution salient object detection | ~930 MB |
| `birefnet-cod` | BiRefNet fine-tuned for camouflaged object detection | ~930 MB |
| `birefnet-massive` | Largest BiRefNet — best quality, slowest | ~3.5 GB |
| `bria-rmbg` | BRIA RMBG 1.4 — **weights are licensed for non-commercial use only** | ~176 MB |
| `dis-general-use` | DIS high-resolution dichotomous segmentation | ~178 MB |
| `dis-anime` | DIS fine-tuned for anime images | ~178 MB |

### Choosing a model

- **Everyday photos:** `u2net` (default) or `birefnet-general` for maximum quality.
- **Speed / low resources:** `u2netp` or `silueta`.
- **People:** `u2net_human_seg`; portraits: `birefnet-portrait`.
- **Anime:** `isnet-anime` or `dis-anime`.
- **Clothes extraction:** `u2net_cloth_seg`.
- **Isolating a specific object:** `sam` with point/box prompts.

### Custom model sessions

The `*_custom` sessions let you run **your own** `.onnx` weights for the supported architectures:

| Session | Purpose |
| ------- | ------- |
| `u2net_custom` | load your own U²-Net ONNX file |
| `dis_custom` | load your own DIS ONNX file |
| `ben_custom` | load your own BEN (Background Erase Network) ONNX file |

```python
from rembg import remove, new_session

session = new_session("u2net_custom", model_path="/path/to/model.onnx")
result = remove(input_image, session=session)
```

From the CLI, pass the same information through the extra-arguments option (see `rembg i --help`).

## Docker

A CPU image is provided:

```bash
docker build -t rembg .
docker run --rm -v "$(pwd)":/app rembg i car-1.jpg car-1.out.png
```

For NVIDIA GPUs, use the CUDA + cuDNN image:

```bash
docker build -f Dockerfile_nvidia_cuda_cudnn_gpu -t rembg-gpu .
docker run --rm --gpus all -v "$(pwd)":/app rembg-gpu i car-1.jpg car-1.out.png
```

Tip: mount a volume for the model cache so weights persist between runs:

```bash
docker run --rm --gpus all -v "$(pwd)":/app -v rembg-models:/root/.u2net rembg-gpu i ...
```

## GPU acceleration

- With `onnxruntime-gpu` installed and a supported GPU available, inference runs on the GPU automatically.
- Verify which execution providers are available in your environment:

  ```python
  import onnxruntime as ort
  print(ort.get_available_providers())
  ```

- `Dockerfile_nvidia_cuda_cudnn_gpu` ships an image with CUDA/cuDNN pre-configured.
- The large BiRefNet models benefit the most from GPU inference.

## Performance tips

- **Reuse sessions** — build one `new_session(...)` and pass it to every `remove()` call.
- **Pick the right model** — `u2netp`/`silueta` for speed, `birefnet-*` for quality.
- **Alpha matting is expensive** — enable it only when you need very soft edges.
- **Use the GPU** for large models and bulk workloads.
- **Batch with the CLI** (`rembg d` / `rembg b`) to avoid repeated model loading.

## Running the tests

The repository ships reference outputs for the sample images (e.g. `car-1.u2net.png`, `anime-girl-1.isnet-anime.png`, `plants-1.birefnet-general-lite.png`, …). The test-suite regenerates these outputs and compares them against the references:

```bash
pip install pytest
pytest test_remove.py
```

> Note: the first run downloads all models used by the tests — it can take a while and a few GB of disk space.

## Repository layout

```
.
├── rembg/                          # the Python package
│   ├── bg.py                       # core remove() logic
│   ├── cli.py                      # CLI entry point
│   ├── *_command.py                # CLI sub-commands (i, d, p, b, s)
│   ├── session_factory.py          # maps a model name to its session class
│   └── sessions/                   # one module per supported model
│       ├── base.py                 # shared session behaviour
│       └── u2net.py, u2netp.py, sam.py, birefnet_*.py, dis_*.py, …
├── test_remove.py                  # pytest suite
├── rembg.ipynb                     # example notebook
├── USAGE.md                        # extended usage documentation
├── Dockerfile                      # CPU container image
├── Dockerfile_nvidia_cuda_cudnn_gpu# GPU container image (CUDA + cuDNN)
├── docker-compose.yml
├── setup.py / setup.cfg / pyproject.toml
├── CITATION.cff
└── LICENSE.txt
```

## Troubleshooting / FAQ

**Where are the models stored?**
In `~/.u2net` by default. Change the location with the `U2NET_HOME` environment variable.

**Can I use rembg offline?**
Yes — after the first download, models are served from the local cache. You can also place your own `.onnx` files in the cache directory or use the `*_custom` sessions.

**The first run is slow.**
The model weights are being downloaded; subsequent runs load them from disk.

**`onnxruntime` fails to load on Windows (DLL errors).**
Install the [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe).

**Alpha matting fails to install/run on Windows.**
Try installing pymatting from conda-forge: `conda install -c conda-forge pymatting`.

**My output looks solid/blank when saved as `.jpg`.**
JPEG has no alpha channel — always save transparent results as `.png`.

## Citing

If rembg was useful for your research, please cite it. The canonical metadata lives in [CITATION.cff](CITATION.cff):

```bibtex
@software{rembg,
  title  = {rembg},
  author = {Gatis, Daniel},
  year   = {2020},
  url    = {https://github.com/danielgatis/rembg}
}
```

## Acknowledgements

rembg stands on the shoulders of these projects and papers:

- [U²-Net](https://github.com/xuebinqin/U-2-Net) — Qin et al., *U²-Net: Going Deeper with Nested U-Structure for Salient Object Detection*
- [DIS / IS-Net](https://github.com/xuebinqin/DIS) — Qin et al., *Highly Accurate Dichotomous Image Segmentation* (ECCV 2022)
- [Segment Anything](https://github.com/facebookresearch/segment-anything) — Kirillov et al., 2023
- [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) — *Bilateral Reference for High-Resolution Dichotomous Image Segmentation*
- [BRIA RMBG](https://huggingface.co/briaai/RMBG-1.4) — BRIA AI
- [BEN](https://github.com/PramaLLC/BEN2) — Background Erase Network
- [ONNX Runtime](https://onnxruntime.ai/), [pooch](https://github.com/fatiando/pooch), [pymatting](https://github.com/pymatting/pymatting), [OpenCV](https://opencv.org/), [Pillow](https://python-pillow.org/)

## License

The rembg source code is released under the [MIT License](LICENSE.txt).

> **Note:** the pre-trained model weights are distributed under their own licenses — in particular, `bria-rmbg` may only be used for **non-commercial** purposes. Check the original projects before using a model in a commercial product.

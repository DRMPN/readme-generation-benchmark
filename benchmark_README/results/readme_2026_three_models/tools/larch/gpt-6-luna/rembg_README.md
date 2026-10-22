# rembg

`rembg` removes image backgrounds using ONNX-based segmentation models. It can process individual images or folders, run as an HTTP service, or be used as a Python library.

The repository includes multiple model implementations and sample images with corresponding output images.

## Features

- Remove an image background and return a transparent PNG.
- Choose from general-purpose, portrait, anime, clothing, and other segmentation models.
- Use the command-line interface, Python API, or HTTP server.
- Reuse model sessions when processing multiple images.
- Optionally refine edges with alpha matting or post-process the mask.

## Installation

Use Python 3.10 or newer. Install `rembg` with a suitable ONNX Runtime backend:

```bash
# CPU
python -m pip install "rembg[cpu]"

# GPU
python -m pip install "rembg[gpu]"
```

The GPU option depends on a compatible GPU, drivers, and CUDA environment. See the [ONNX Runtime installation matrix](onnxruntime-installation-matrix.png) and the [ONNX Runtime documentation](https://onnxruntime.ai/) for compatibility details.

To install the project from a local checkout:

```bash
python -m pip install .
```

## Command-line usage

The command-line interface provides commands for image processing, folders, model downloads, benchmarking, and serving. To see the options available in your installed version:

```bash
rembg --help
rembg i --help
```

### Process one image

```bash
rembg i input.jpg output.png
```

The output should be saved as PNG to preserve transparency. To select a model:

```bash
rembg i -m isnet-general-use input.jpg output.png
```

### Process a folder

Use the folder-processing command to process a directory of images:

```bash
rembg p ./input-images ./output-images
```

Check `rembg p --help` for supported input formats and folder options.

### Download models

Model files are downloaded when needed. The download command can be used to fetch a model ahead of time:

```bash
rembg d u2net
```

See `rembg d --help` for the available model names and options.

### Run the HTTP server

Start the service with:

```bash
rembg s
```

For options such as host and port:

```bash
rembg s --help
```

The server accepts image requests and returns processed images. See the command help for the endpoint and request format supported by your installed version.

### Benchmark

Run the benchmark command to compare processing performance:

```bash
rembg b --help
```

## Python API

### Remove a background from a file

```python
from pathlib import Path

from rembg import remove

input_path = Path("input.jpg")
output_path = Path("output.png")

output = remove(input_path.read_bytes())
output_path.write_bytes(output)
```

### Use a PIL image

```python
from PIL import Image
from rembg import remove

image = Image.open("input.jpg")
result = remove(image)
result.save("output.png")
```

### Reuse a model session

Creating a session once and reusing it is recommended when processing multiple images:

```python
from pathlib import Path

from rembg import new_session, remove

session = new_session("u2net")

for input_path in Path("input-images").glob("*"):
    if not input_path.is_file():
        continue

    result = remove(input_path.read_bytes(), session=session)
    output_path = Path("output-images") / f"{input_path.stem}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(result)
```

### Refine edges with alpha matting

Alpha matting can improve fine edges, such as hair, but may take longer:

```python
from rembg import remove

result = remove(
    open("input.jpg", "rb").read(),
    alpha_matting=True,
    alpha_matting_foreground_threshold=240,
    alpha_matting_background_threshold=10,
    alpha_matting_erode_size=10,
)

with open("output.png", "wb") as output_file:
    output_file.write(result)
```

Thresholds and erosion size may need adjustment for different images.

## Models

The repository contains support for a range of segmentation models. Common model names include:

| Model | Typical use |
|---|---|
| `u2net` | General-purpose background removal |
| `u2netp` | Smaller, lighter U²-Net model |
| `u2net_human_seg` | Human segmentation |
| `u2net_cloth_seg` | Clothing segmentation |
| `silueta` | General-purpose segmentation |
| `isnet-general-use` | General-purpose segmentation |
| `isnet-anime` | Anime-style images |
| `sam` | Segment Anything Model support |
| `birefnet-general` | General-purpose segmentation |
| `birefnet-general-lite` | Lighter general-purpose model |
| `birefnet-portrait` | Portraits |
| `birefnet-dis` | Dichotomous image segmentation |
| `birefnet-hrsod` | High-resolution salient object detection |
| `birefnet-cod` | Concealed object detection |
| `birefnet-massive` | General-purpose segmentation |

The project also includes custom-model support. Consult the command help and model implementation files for the exact model names and configuration supported by your version.

Select a model in the CLI with `-m`, or in Python when creating a session:

```python
from rembg import new_session, remove

session = new_session("isnet-anime")
result = remove(open("anime.jpg", "rb").read(), session=session)
```

Model weights are fetched as needed and cached locally. The first run may therefore require an internet connection and take longer than later runs.

## Output and image formats

Background removal produces an image with an alpha channel. Use PNG or another format that supports transparency when saving the result. Saving as JPEG discards transparency; use PNG if you need to retain the removed-background area.

The output dimensions generally match those of the input. Results vary by image content and model; choosing a model intended for the subject matter can improve results.

## Docker

The repository includes Dockerfiles for building container images, including a GPU-oriented Dockerfile. To build the standard image from the repository root:

```bash
docker build -t rembg .
```

The image can then be used with the CLI. For example, mount local input and output directories and run the image-processing command:

```bash
docker run --rm \
  -v "$PWD:/data" \
  rembg i /data/input.jpg /data/output.png
```

GPU use in Docker requires a compatible host and a container runtime configured for GPU access. See the repository’s Dockerfiles and your container runtime documentation for setup details.

## Development and tests

Install the project and its development dependencies as appropriate for your environment, then run the test suite with:

```bash
pytest
```

The repository contains `test_remove.py` and sample input/output images that can be used when developing or checking image-removal behavior.

## Troubleshooting

- **The first run is slow:** Model weights may need to be downloaded and initialized.
- **No transparency in the saved file:** Save the result as PNG rather than JPEG.
- **Poor edges or missed details:** Try another model, or enable alpha matting and adjust its thresholds.
- **GPU runtime errors:** Check that the installed ONNX Runtime package, CUDA version, drivers, and GPU are compatible.
- **Command options differ:** Use `rembg <command> --help` to see the options provided by your installed release.

## License

See [`LICENSE.txt`](LICENSE.txt) for the license terms.

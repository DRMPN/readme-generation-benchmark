# rembg

A tool to remove image background.

## Features

* High-quality background removal.
* Supports multiple models, including `u2net`, `isnet-general-use`, `sam`, `birefnet-general`, and more.
* Supports alpha matting.
* Provides a simple API and CLI.

## Supported Models

| Model name | Description |
| --- | --- |
| `u2net` | U^2-Net (default) |
| `u2netp` | Lightweight U^2-Net |
| `u2net_human_seg` | Human segmentation |
| `u2net_cloth_seg` | Clothes segmentation |
| `u2net_custom` | Custom U^2-Net |
| `silueta` | Silueta |
| `isnet-general-use` | IS-Net general use |
| `isnet-anime` | IS-Net anime |
| `dis_custom` | Custom DIS |
| `sam` | Segment Anything Model |
| `birefnet-general` | BiRefNet general |
| `birefnet-general-lite` | BiRefNet general lite |
| `birefnet-portrait` | BiRefNet portrait |
| `birefnet-dis` | BiRefNet DIS |
| `birefnet-hrsod` | BiRefNet HRSOD |
| `birefnet-cod` | BiRefNet COD |
| `birefnet-massive` | BiRefNet massive |
| `bria-rmbg` | BriaRmBg |
| `ben_custom` | Ben custom |

## Installation

### Prerequisites

* Python 3.10 or higher.
* [onnxruntime](https://onnxruntime.ai/) for CPU execution.

```bash
pip install rembg
```

To install with the CPU runtime:

```bash
pip install rembg[cpu]
```

To install with the GPU runtime:

```bash
pip install rembg[gpu]
```

To install with the CLI dependencies:

```bash
pip install rembg[cli]
```

## Usage

### As a library

#### Load the Image

```python
from PIL import Image
from rembg import new_session, remove

input_path = 'input.png'
output_path = 'output.png'

input = Image.open(input_path)
```

#### Removing the background

##### Without additional arguments

This defaults to the `u2net` model.

```python
output = remove(input)
output.save(output_path)
```

##### With a specific model

You can use the `new_session` function to create a session with a specific model.

```python
model_name = "isnet-general-use"
session = new_session(model_name)
output = remove(input, session=session)
```

##### For processing multiple image files

By default, `remove` initialises a new session every call. This can be a large bottleneck if you're having to process multiple images. Initialise a session and pass it in to the `remove` function for fast multi-image support

```python
model_name = "u2net"
rembg_session = new_session(model_name)
for img in images:
    output = remove(img, session=rembg_session)
```

##### With alpha matting

Alpha matting is a post processing step that can be used to improve the quality of the output.

```python
output = remove(input, alpha_matting=True, alpha_matting_foreground_threshold=270,alpha_matting_background_threshold=20, alpha_matting_erode_size=11)
```

##### Only mask

If you only want the mask, you can use the `only_mask` argument.

```python
output = remove(input, only_mask=True)
```

##### With post processing

You can use the `post_process_mask` argument to post process the mask to get better results.

```python
output = remove(input, post_process_mask=True)
```

##### Replacing the background color

You can use the `bgcolor` argument to replace the background color.

```python
output = remove(input, bgcolor=(255, 255, 255, 255))
```

##### Using input points

You can use the `input_points` and `input_labels` arguments to specify the points that should be used for the masks. This only works with the `sam` model.

```python
import numpy as np
# Define the points and labels
# The points are defined as [y, x]
input_points = np.array([[400, 350], [700, 400], [200, 400]])
input_labels = np.array([1, 1, 2])

image = remove(image,session=session, input_points=input_points, input_labels=input_labels)
```

#### Save the image

```python
output.save(output_path)
```

### As a CLI

The CLI is available via the `rembg` command. It provides the following subcommands:

| Command | Description |
| --- | --- |
| `b` | for a byte stream as input |
| `d` | download models |
| `i` | for a file as input |
| `p` | for a folder as input |
| `s` | for a http server |

For example, to remove the background from a file:

```bash
rembg i input.png output.png
```

Common options include:

* `-m`, `--model`: the model name (defaults to `u2net`).
* `-a`, `--alpha-matting`: use alpha matting.
* `-om`, `--only-mask`: output only the mask.
* `-ppm`, `--post-process-mask`: post process the mask.
* `-bgc`, `--bgcolor`: background color (R G B A) to replace the removed background with.
* `-x`, `--extras`: additional options in JSON format.

To download the models:

```bash
rembg d u2net
```

To process a folder:

```bash
rembg p input_dir output_dir
```

The `p` command also supports the following options:

* `-w`, `--watch`: watches a folder for changes.
* `-d`, `--delete_input`: delete input file after processing.

To run the HTTP server (which also serves a web UI and API documentation at `/api`):

```bash
rembg s
```

The `s` command also supports the following options:

* `-p`, `--port`: port (defaults to `7000`).
* `-h`, `--host`: host (defaults to `0.0.0.0`).
* `-l`, `--log_level`: log level (defaults to `info`).
* `-t`, `--threads`: number of worker threads.

## Docker

A `Dockerfile` is provided to build an image.

```bash
docker build -t rembg .
```

A `docker-compose.yml` file is also provided.

## License

This project is licensed under the [MIT license](LICENSE.txt).

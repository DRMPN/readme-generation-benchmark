# face_recognition

---

[![PyPi](https://badge.fury.io/py/face_recognition.svg)](https://badge.fury.io/py/face_recognition)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![dlib](https://img.shields.io/badge/Dlib-008000.svg?style=flat&logo=Dlib&logoColor=white)
![numpy](https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project provides a Python library for face detection and recognition, allowing developers and data scientists to locate faces in images, identify facial landmarks, generate face encodings, and compare faces against known individuals. It exposes a high-level Python API for programmatic use, as well as command-line tools for recognizing and detecting faces in images without writing code. The repository also includes usage examples spanning simple scripts and interactive notebook workflows for common recognition tasks. Newcomers can begin with the Getting Started section for installation and first-run instructions.

---

## Core Features

- **Face detection** – Locate faces in images with bounding boxes, using a fast CPU-based model by default or a more accurate GPU-accelerated deep-learning model when accuracy matters.
- **Facial landmark detection** – Identify facial feature points in detected faces, giving you the coordinates needed for alignment, analysis, or image manipulation.
- **Face encoding and recognition** – Convert faces into numeric encodings and compare them against known faces, so you can identify who appears in a photo.
- **Command-line tools** – Run face recognition and face detection directly from the terminal on single images or whole folders, including parallel processing across multiple CPU cores to speed up large batches.
- **Batch GPU processing** – Process multiple images in batches through the CNN detector for much faster results when a GPU is available.

---

## Installation

Install `face_recognition` from PyPI:

```sh
pip install face_recognition
```

---

## Getting Started

Requires Python (see the supported versions declared in `setup.py`) with `pip`. Installing the package pulls in its runtime dependencies (`dlib`, `numpy`, `Pillow`, `Click`, `face_recognition_models`) automatically.

1. **Install the package:**

```console
   $ pip3 install face_recognition
```

2. **Detect faces from the command line.** `face_detection` accepts an image file (or a folder of images) and prints one `filename,top,right,bottom,left` row per face found:

```console
   $ face_detection ./image_to_check.jpg
```

3. **Recognize who is in an image.** `face_recognition` takes a folder of known people's images (the file name without extension is used as the person's name) and an image file or folder to check:

```console
   $ face_recognition ./known_people/ ./unknown.jpg
```

   Useful options: `--cpus` (parallel processing; `-1` uses all cores), `--tolerance` (default 0.6), and `--show-distance`.

4. **Or use the Python API:**

```python
   import face_recognition

   image = face_recognition.load_image_file("your_image.jpg")
   face_locations = face_recognition.face_locations(image)
```

   The package also exports `face_encodings`, `face_landmarks`, `compare_faces`, `face_distance`, and `batch_face_locations` (see `face_recognition/api.py`).

**Troubleshooting:** If the library prints a message asking you to install `face_recognition_models`, run the command shown there:

```console
pip install git+https://github.com/ageitgey/face_recognition_models
```

---

## Architecture

The project is structured as a modular Python SDK, providing core facial analysis capabilities accessed through both a high-level API and specialized command-line interfaces (CLIs).

*   **Core API (`face_recognition`):** This central library handles fundamental tasks including image loading, face detection (using 'hog' or 'cnn' models), generating face encodings, and calculating facial distances.
*   **CLI Tools:** Two distinct CLI entry points simplify usage:
    *   `face_detection`: Dedicated to finding and locating faces within images.
    *   `face_recognition`: Used for full identity verification, allowing users to scan known people and test unknown images against a stored database.
*   **Execution and Integration:** The architecture supports concurrent processing via multiprocessing pools in the CLI layers, supporting various application use cases from simple file processing to complex research integrations (e.g., KNN examples).

---

## API Reference

The public Python interface is defined in `face_recognition/api.py` and re-exported by `face_recognition/__init__.py`, so all functions below are available directly after `import face_recognition`.

### Python API

| Function | Purpose |
| --- | --- |
| `load_image_file(file, mode='RGB')` | Loads an image file (`.jpg`, `.png`, etc.) into a numpy array. Supported modes: `'RGB'` (default) and `'L'` (black and white). |
| `face_locations(img, number_of_times_to_upsample=1, model="hog")` | Finds faces in an image and returns bounding boxes as `(top, right, bottom, left)` tuples. `model` is `"hog"` (faster on CPU, default) or `"cnn"` (more accurate, GPU/CUDA accelerated if available). |
| `batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)` | Runs CNN face detection over a list of images in GPU batches; mainly useful with a GPU. Returns `(top, right, bottom, left)` tuples per image. |
| `face_encodings` | Computes face encodings for faces in an image; also accepts a `known_face_locations` keyword argument (see `examples/face_recognition_knn.py` for usage). |
| `face_distance(face_encodings, face_to_compare)` | Returns the Euclidean distance between each encoding in a list and a known face encoding (smaller means more similar). |

The package also exports `face_landmarks` and `compare_faces` from `face_recognition/api.py`; see the module source for their signatures.

### Command-line tools

Both console scripts are registered in `setup.py`.

**`face_recognition`** (`face_recognition.face_recognition_cli:main`) — recognizes faces in images against a folder of known people.

| Argument / Option | Description |
| --- | --- |
| `known_people_folder` | Folder of images of known people; each file's base name is used as the person's name. |
| `image_to_check` | Image file, or folder of image files, to check. |
| `--cpus` | Number of CPU cores to use in parallel (default `1`; `-1` means use all in system). |
| `--tolerance` | Tolerance for face comparisons (default `0.6`; lower it if you get multiple matches for the same person). |
| `--show-distance` | Also output the face distance (default off); useful for tuning `--tolerance`. |

Results are printed as `filename,name` (or `filename,name,distance` with `--show-distance`); unmatched faces are reported as `unknown_person` and images with no detectable faces as `no_persons_found`.

**`face_detection`** (`face_recognition.face_detection_cli:main`) — prints face bounding-box locations as `filename,top,right,bottom,left`.

| Argument / Option | Description |
| --- | --- |
| `image_to_check` | Image file, or folder of image files, to process. |
| `--cpus` | Number of CPU cores to use in parallel (default `1`; `-1` means use all in system). |
| `--model` | Face detection model: `"hog"` (default) or `"cnn"`. |
| `--upsample` | Number of times to upsample the image when looking for faces (higher numbers find smaller faces; see the CLI source for the default). |

---

## Examples

The [`examples`](./examples) directory contains runnable scripts and Jupyter notebooks covering common workflows
# face_recognition-3ndz68zw

---

[![PyPi](https://badge.fury.io/py/face_recognition.svg)](https://badge.fury.io/py/face_recognition)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![dlib](https://img.shields.io/badge/Dlib-008000.svg?style={0}&logo=Dlib&logoColor=white)
![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![scipy](https://img.shields.io/badge/SciPy-8CAAE6.svg?style={0}&logo=SciPy&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This Python project provides face detection, face encoding, and face comparison for images. It is intended for developers building face-recognition workflows and computer-vision applications. It offers a Python API, command-line tools, and examples; see Getting Started for runnable steps.

---

## Installation

Install face_recognition-3ndz68zw using one of the following methods:

**Using PyPi:**

```sh
pip install face_recognition
```

---

## Getting Started

Prerequisites: Python and `pip3`.

1. Install the package:

```console
   pip3 install face_recognition
```

2. Create a folder of known-person images. The CLI accepts `.jpg`, `.jpeg`, and `.png` files; each filename’s basename is used as that person’s name.

3. Run the CLI with the known-people folder and an image file or folder to check:

```console
   face_recognition ./known_people ./image_to_check.jpg
```

---

## API Reference

- `face_recognition.load_image_file` — Load an image file into a NumPy array.
- `face_recognition.face_locations` — Return face bounding boxes in `(top, right, bottom, left)` order; supports the `hog` and `cnn` models.
- `face_recognition.batch_face_locations` — Return face locations for a batch of images using the CNN detector.
- `face_recognition.face_encodings` — Return face encodings for faces found in an image.
- `face_recognition.compare_faces` — Compare a face encoding with known encodings and return match results.
- `face_recognition.face_distance` — Return Euclidean distances between face encodings.

**Command-line entry points** (registered in `setup.py`):
- `face_recognition` — `face_recognition.face_recognition_cli:main`; compare images against known people.
- `face_detection` — `face_recognition.face_detection_cli:main`; detect faces in an image or directory.

---

## Testing

Test artifacts are in `tests/`, including `tests/test_face_recognition.py` and `tests/test_images/`. `tox.ini` and `.github/workflows/main.yml` are also present; their configuration and exact test commands are not available here.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Documentation

A detailed face_recognition-3ndz68zw description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.rst)**: To learn more about making a contribution to face_recognition-3ndz68zw.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). face_recognition-3ndz68zw repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{face_recognition-3ndz68zw,

        author = {README Benchmark},

        title = {face_recognition-3ndz68zw repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
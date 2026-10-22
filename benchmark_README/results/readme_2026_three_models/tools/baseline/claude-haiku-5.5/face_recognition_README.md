# Face Recognition

Face Recognition is a Python library for recognizing faces, built on dlib's face detection and face encoding models. It provides a Python API and two command-line tools, `face_recognition` and `face_detection`. The package is version 1.4.0 and is released under the MIT License.

## Overview

The library covers these tasks:

- Loading images into NumPy arrays (`load_image_file`)
- Finding faces with a HOG model (default) or a CNN model (`face_locations`, `batch_face_locations`)
- Locating facial features such as eyes, nose, and lips (`face_landmarks`)
- Computing 128-dimension face encodings (`face_encodings`)
- Comparing encodings by Euclidean distance (`face_distance`, `compare_faces`)

The `face_recognition` package is the Python module. Its public functions are exported from `face_recognition/__init__.py`.

## Requirements

The package declares these runtime dependencies in `setup.py`:

- `face_recognition_models>=0.3.0`
- `Click>=6.0`
- `dlib>=19.7`
- `numpy`
- `Pillow`

`requirements.txt` lists the same packages, with `dlib>=19.3.0` and `scipy>=0.17.0` instead of the `setup.py` versions. The package metadata classifiers list Python 3.5 through 3.9. The CI workflow tests Python 3.8, 3.9, and 3.10. `HISTORY.rst` records that Python 2.x support was dropped in 1.4.0 and Python 3.4 support was dropped in 1.3.0.

## Installation

Install the latest stable release from PyPI:

```console
$ pip3 install face_recognition
```

To install from source, clone the repository and run:

```console
$ git clone git://github.com/ageitgey/face_recognition
$ cd face_recognition
$ python setup.py install
```

If `face_recognition_models` is missing, the API module prints this message and exits:

```
pip install git+https://github.com/ageitgey/face_recognition_models
```

### Docker

The repository includes Dockerfiles for CPU and GPU builds, plus a `docker-compose.yml`:

```console
$ docker-compose up
```

The default `docker-compose.yml` builds the image from `Dockerfile` and runs `find_faces_in_picture_cnn.py` from the `examples` directory. To use the GPU, uncomment the `dockerfile: Dockerfile.gpu` and `runtime: nvidia` lines in that file. The GPU option requires Nvidia-Docker.

Prebuilt images are published as `animcogn/face_recognition` on Docker Hub. The tags are listed in `docker/README.md`:

- CPU: `cpu-latest`, `cpu`, `cpu-0.1`, `latest`
- GPU: `gpu-latest`, `gpu`, `gpu-0.1`
- Jupyter (Kubeflow-oriented): `cpu-jupyter-kubeflow-latest` and `gpu-jupyter-kubeflow-latest`, with related version tags

The CPU images need no driver prerequisites. The GPU images require the Nvidia drivers, the Nvidia container runtime, and a Docker configuration that uses that runtime. To check GPU setup inside a container, run:

```python
import dlib
print(dlib.cuda.get_num_devices())
```

## Usage

### Python API

```python
import face_recognition

image = face_recognition.load_image_file("your_file.jpg")

# Find all the faces in the image
face_locations = face_recognition.face_locations(image)

# Find facial features
face_landmarks_list = face_recognition.face_landmarks(image)

# Get a 128-dimension encoding for each face
known_face_encodings = face_recognition.face_encodings(image)
```

Compare an unknown encoding against a list of known encodings:

```python
results = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
```

Key parameters, as documented in `face_recognition/api.py`:

- `face_locations(img, number_of_times_to_upsample=1, model="hog")`: `model` can be `"hog"` or `"cnn"`. Results are `(top, right, bottom, left)` tuples.
- `batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)`: uses the CNN detector on a list of same-sized images.
- `face_landmarks(face_image, face_locations=None, model="large")`: `model` can be `"large"` (68 points) or `"small"` (5 points). The result is a list of dictionaries keyed by feature name.
- `face_encodings(face_image, known_face_locations=None, num_jitters=1, model="small")`: higher `num_jitters` is more accurate but slower.
- `compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)`: returns a list of booleans. Lower tolerance is stricter.

### Command-line tools

The `face_recognition` command compares faces in images against a folder of known people:

```console
$ face_recognition ./pictures_of_people_i_know/ ./unknown_pictures/
```

Each known person is one image file, and the file name (without its extension) is used as the name. Output is written as `filename,name`. Options:

- `--cpus X`: number of CPU cores to use. `-1` uses all cores. Default is 1.
- `--tolerance`: face comparison tolerance. Default is 0.6.
- `--show-distance`: adds the face distance to the output.

The `face_detection` command reports face locations:

```console
$ face_detection ./unknown_pictures/
```

Output is `filename,top,right,bottom,left`. Options:

- `--cpus X`: number of CPU cores.
- `--model`: `"hog"` or `"cnn"`. Default is `"hog"`.
- `--upsample`: how many times to upsample the image. Default is 0.

Both commands accept a single image file or a folder of `.jpg`, `.jpeg`, or `.png` files.

### Examples

The `examples` directory includes scripts that show specific uses:

- `find_faces_in_picture.py` and `find_faces_in_picture_cnn.py`: detect faces and print their locations.
- `find_facial_features_in_picture.py`: draw facial features.
- `identify_and_draw_boxes_on_faces.py`: identify known people and draw labeled boxes.
- `face_recognition_knn.py` and `face_recognition_svm.py`: classifier-based recognition with scikit-learn.
- `facerec_from_webcam.py`, `facerec_from_webcam_faster.py`, `facerec_from_webcam_multiprocessing.py`: live webcam recognition. These require OpenCV.
- `facerec_from_video_file.py` and `find_faces_in_batches.py`: video processing.
- `blink_detection.py` and `blur_faces_on_webcam.py`: webcam demos that require OpenCV.
- `facerec_on_raspberry_pi.py`: runs on a Raspberry Pi with `picamera`.
- `web_service_example.py`: a Flask service that checks uploaded images for a picture of Barack Obama. It runs on port 5001.
- `benchmark.py`: times the main steps on several image sizes.

The `examples/ipynb_examples` folder contains a Jupyter notebook for real-time tracking.

Some examples require extra packages. `face_recognition_knn.py` needs scikit-learn. The webcam, video, and blink demos need OpenCV (`cv2`). `blink_detection.py` also uses scipy. `web_service_example.py` needs Flask.

## Configuration

Configuration is mostly in files:

- **`setup.py`**: package metadata, dependencies, and console script entry points (`face_recognition` and `face_detection`).
- **`setup.cfg`**: bumpversion settings (current version 1.4.0, with commit and tag enabled), wheel settings, and flake8 settings. The flake8 maximum line length is 160, and `examples`, `docs`, and other directories are excluded.
- **`tox.ini`**: test environments for py35 through py38 and flake8. The test command is `python -m unittest discover`.
- **`docs/conf.py`**: Sphinx configuration. It mocks some heavy dependencies during documentation builds.
- **`docker-compose.yml`**: the image name, working directory, startup command, and a volume mapping `./` to `/face_recognition`.

The Dockerfiles use build arguments and environment variables. For example, the CPU image sets `CFLAGS=-static` and the virtual environment at `/opt/venv`. The Jupyter Dockerfiles read `NB_PREFIX` to set the Jupyter base URL.

## Development

Use the steps in `CONTRIBUTING.rst`:

1. Fork the repository and clone your fork.
2. Install your copy into a virtual environment:

   ```console
   $ python setup.py develop
   ```

3. Create a branch for your change.
4. Run checks:

   ```console
   $ flake8 face_recognition tests
   $ python setup.py test
   $ tox
   ```

5. Commit, push, and open a pull request.

The contributing guidelines ask that pull requests include tests, that new functionality be documented with a docstring and added to the README, and that the change work across all supported Python versions.

### Makefile targets

Running `make` with no target shows the help text. The available targets are:

- `clean`, `clean-build`, `clean-pyc`, `clean-test`: remove build, cache, and test artifacts.
- `lint`: runs `flake8 face_recognition tests`.
- `test`: runs `python3 setup.py test`.
- `test-all`: runs `tox`.
- `coverage`: runs tests under `coverage` and generates an HTML report.
- `docs`: runs `sphinx-apidoc` and builds the HTML documentation.
- `servedocs`: rebuilds the docs when `.rst` files change, using `watchmedo`.
- `dist`: builds source and wheel distributions.
- `release`: builds distributions and uploads them with `twine`.
- `install`: installs the package into the active Python environment.

### Documentation

The Sphinx documentation in `docs/` includes the installation guide, usage notes, the contributing guide, the author list, and the history. `docs/face_recognition.rst` uses `automodule` to document `face_recognition.api`. The `docs/requirements_docs.txt` file is empty in the supplied files.

## Testing

Tests are in `tests/test_face_recognition.py` and use Python's `unittest` framework. They cover:

- Image loading, including a 32-bit PNG
- HOG and CNN face detection, including partial faces and batched detection
- Facial landmarks with both models
- Face encodings, face distances, and face comparisons
- The `face_recognition` and `face_detection` command-line interfaces

The test images are in `tests/test_images`. To run the tests:

```console
$ python -m unittest discover
```

or:

```console
$ tox
```

The GitHub Actions workflow in `.github/workflows/main.yml` runs on every push. It sets up Python 3.8, 3.9, and 3.10 on Ubuntu, installs the package, runs `python setup.py check`, and then runs `tox`.

## Authors and Acknowledgments

The author is Adam Geitgey (ageitgey@gmail.com). `AUTHORS.rst` credits Davis King for creating dlib and providing the trained facial feature detection and face encoding models. It also thanks the developers of numpy, scipy, scikit-image, and Pillow, and the Cookiecutter project template.

## Changelog

Release notes are in `HISTORY.rst`. The most recent entry is version 1.4.0 (2020-09-26), which dropped Python 2.x support and added a `--upsample` option to the command-line tool.

## License

This project is licensed under the MIT License. Copyright (c) 2021 Adam Geitgey. See the `LICENSE` file for the full text.

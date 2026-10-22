# face_recognition

`face_recognition` is a Python library and command-line tool for finding faces in images, locating facial landmarks, computing face encodings, and comparing faces to identify people. It is built on [dlib](http://dlib.net/)'s face detection and face recognition models and is published on PyPI as `face_recognition` (version 1.4.0).

- Author: Adam Geitgey (ageitgey@gmail.com)
- License: MIT (see [LICENSE](LICENSE))
- Source: https://github.com/ageitgey/face_recognition

## Features

- Load image files into NumPy arrays (`load_image_file`).
- Find face locations with a fast HOG detector (default) or a more accurate CNN detector (`model="cnn"`), including batched CNN detection (`batch_face_locations`).
- Detect facial landmarks with a 68-point model (`model="large"`) or a 5-point model (`model="small"`).
- Compute 128-dimension face encodings (`face_encodings`).
- Compare encodings with Euclidean distance (`face_distance`) and a tolerance-based match (`compare_faces`).
- Command-line tools `face_recognition` (identify known people in images) and `face_detection` (list face locations).

## Requirements

- Python 3. The package metadata (`setup.py`) lists classifiers for Python 3.5 through 3.9, and the GitHub Actions workflow tests Python 3.8, 3.9, and 3.10.
- Runtime dependencies declared in `setup.py`: `face_recognition_models>=0.3.0`, `Click>=6.0`, `dlib>=19.7`, `numpy`, and `Pillow`.
- `requirements.txt` additionally lists `scipy>=0.17.0` and `dlib>=19.3.0`. The library source does not import scipy.
- dlib must be built or installed successfully on your system. dlib is a native C++ library, so installation can require a compiler and CMake. The repository's Dockerfiles show one working build recipe (dlib v19.9 built from source).
- The `face_recognition_models` package provides the pretrained model files. If it is missing, `api.py` prints an installation hint and exits.

## Installation

Install the stable release from PyPI:

```console
$ pip3 install face_recognition
```

To install from source, clone the repository and install it:

```console
$ git clone https://github.com/ageitgey/face_recognition
$ cd face_recognition
$ pip3 install -r requirements.txt
$ python3 setup.py install
```

If you use the `CNN` model on a GPU, dlib must be compiled with CUDA support. The GPU Dockerfile in this repository builds dlib with `-DDLIB_USE_CUDA=1`. You can check GPU availability with `dlib.cuda.get_num_devices()`.

## Python API

Import the library:

```python
import face_recognition
```

The basic workflow is to load an image, find faces, and compute encodings:

```python
image = face_recognition.load_image_file("your_file.jpg")

# (top, right, bottom, left) tuples for each face
face_locations = face_recognition.face_locations(image)

# Dicts of facial features (chin, eyes, nose, lips, etc.) for each face
face_landmarks_list = face_recognition.face_landmarks(image)

# A 128-dimension encoding for each face
face_encodings = face_recognition.face_encodings(image)
```

To check whether an unknown face matches any known faces:

```python
results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)
# A list of True/False values, one per known encoding
```

To measure how similar faces are, use `face_distance`. Lower distances mean more similar faces:

```python
distances = face_recognition.face_distance(known_face_encodings, unknown_face_encoding)
```

### Functions

| Function | Description |
| --- | --- |
| `load_image_file(file, mode='RGB')` | Loads an image file (or file object) into a NumPy array. `mode` may be `'RGB'`, `'L'`, or `None`. |
| `face_locations(img, number_of_times_to_upsample=1, model="hog")` | Returns a list of `(top, right, bottom, left)` tuples. `model` is `"hog"` or `"cnn"`. Higher upsampling finds smaller faces. |
| `batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)` | Runs the CNN detector on a list of images of the same size. Batching is most useful on a GPU. |
| `face_landmarks(face_image, face_locations=None, model="large")` | Returns a list of dicts with keys such as `chin`, `left_eyebrow`, `right_eyebrow`, `nose_bridge`, `nose_tip`, `left_eye`, `right_eye`, `top_lip`, and `bottom_lip`. `model="small"` returns only `nose_tip`, `left_eye`, and `right_eye`. |
| `face_encodings(face_image, known_face_locations=None, num_jitters=1, model="small")` | Returns a list of 128-dimension NumPy arrays, one per face. Higher `num_jitters` is more accurate but slower. |
| `face_distance(face_encodings, face_to_compare)` | Returns a NumPy array of Euclidean distances between each known encoding and the candidate encoding. |
| `compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)` | Returns a list of booleans indicating whether each known encoding is within `tolerance` distance. Lower tolerance is stricter. |

Each function is documented with a docstring in [`face_recognition/api.py`](face_recognition/api.py).

## Command-line usage

Installing the package provides two commands.

### `face_recognition`: identify known people

```console
$ face_recognition [OPTIONS] KNOWN_PEOPLE_FOLDER IMAGE_TO_CHECK
```

- `KNOWN_PEOPLE_FOLDER` is a folder of images. Each file's base name (without extension) is used as the person's name. Only `.jpg`, `.jpeg`, and `.png` files are scanned. If a file contains no face, it is ignored with a warning. If it contains more than one face, only the first is used.
- `IMAGE_TO_CHECK` is an image file or a folder of images.

Output is one line per match, in the form `filename,name` (or `filename,name,distance` with `--show-distance`). Names are `unknown_person` when no known face matches and `no_persons_found` when no face is detected.

Options:

- `--cpus INTEGER`: number of CPU cores to use when processing a folder. The default is `1`. `-1` uses all cores.
- `--tolerance FLOAT`: face-matching tolerance. The default is `0.6`. Lower values are stricter.
- `--show-distance BOOLEAN`: include the distance in the output. Useful for tuning `--tolerance`.

### `face_detection`: find face locations

```console
$ face_detection [OPTIONS] IMAGE_TO_CHECK
```

Output is one line per face, in the form `filename,top,right,bottom,left`.

Options:

- `--cpus INTEGER`: number of CPU cores to use when processing a folder. The default is `1`. `-1` uses all cores.
- `--model TEXT`: `hog` (default) or `cnn`.
- `--upsample INTEGER`: number of times to upsample the image when searching for faces. The default is `0`. Higher values find smaller faces.

## Examples

The [`examples/`](examples) directory contains runnable scripts. Run them from inside that directory, because several use relative paths to the sample images. Notable examples include:

- `find_faces_in_picture.py` and `find_faces_in_picture_cnn.py`: find faces in an image with the HOG and CNN models and print their locations.
- `find_facial_features_in_picture.py`: find facial landmarks and draw them on the image.
- `identify_and_draw_boxes_on_faces.py`: recognize known people in a single image and draw boxes around them.
- `recognize_faces_in_pictures.py`: compare an unknown face against sample Biden and Obama pictures.
- `face_distance.py`: print the distance between an unknown face and known faces, and show how different tolerances would classify it.
- `face_recognition_knn.py`: train and use a k-nearest-neighbors classifier on a folder of labeled faces (requires scikit-learn). Training data is under `examples/knn_examples/train/`.
- `face_recognition_svm.py`: train an SVM classifier (scikit-learn) on multiple images per person and recognize faces in a test image.
- `find_faces_in_batches.py`: batched CNN detection on video frames (requires OpenCV).
- `facerec_from_webcam.py`, `facerec_from_webcam_faster.py`, `facerec_from_webcam_multiprocessing.py`, `blur_faces_on_webcam.py`: webcam demos (require OpenCV).
- `facerec_from_video_file.py`: recognize faces in a video file and write the annotated result to a new video file (requires OpenCV).
- `facerec_ipcamera_knn.py`: KNN-based recognition on IP camera streams.
- `blink_detection.py`: detects whether the user's eyes are closed using webcam input (requires OpenCV). The script notes that it must be run with sudo for its keyboard handling.
- `digital_makeup.py`: uses facial landmarks to modify facial features in an image.
- `facerec_on_raspberry_pi.py`: runs recognition on a Raspberry Pi camera (requires `picamera`).
- `web_service_example.py`: a Flask app that accepts an uploaded image and reports whether it contains a specific person (requires Flask).
- `benchmark.py`: times face location, landmark, encoding, and end-to-end steps on a single CPU core.
- `*_Simplified_Chinese.py`: Simplified Chinese versions of the Raspberry Pi and web service examples.
- `ipynb_examples/track_faces_on_video_realtime.ipynb`: a Jupyter notebook example.

Example dependencies that are not part of the library, including `cv2`, `flask`, `sklearn`, and `picamera`, must be installed separately to run the corresponding scripts. The `examples/` scripts are not installed with the package.

## Docker

The repository includes several Dockerfiles:

- `Dockerfile`: builds a CPU image on `python:3.10.3-slim-bullseye`, compiles dlib v19.9, installs this package, and runs `recognize_faces_in_pictures.py` by default.
- `Dockerfile.gpu`: a GPU sample based on `nvidia/cuda:9.0-cudnn7-devel` that builds dlib v19.16 with CUDA enabled.
- `docker-compose.yml`: builds the CPU image and runs `find_faces_in_picture_cnn.py` with the repository mounted at `/face_recognition`. The GPU option is commented out and requires the Nvidia container runtime.
- `docker/`: additional Dockerfiles for CPU and GPU images, including Jupyter/Kubeflow variants. See [`docker/README.md`](docker/README.md).

To build and run the default compose service:

```console
$ docker-compose up --build
```

[`docker/README.md`](docker/README.md) states that prebuilt images are published to Docker Hub as `animcogn/face_recognition`, with tags such as `cpu`, `gpu`, and `latest`. For GPU images, the README lists required prerequisites: NVIDIA drivers, the NVIDIA container runtime, and a Docker configuration that uses it. To confirm GPU access inside a container, run `dlib.cuda.get_num_devices()`.

## Testing

Run the test suite with:

```console
$ python3 -m unittest discover
```

The tests live in [`tests/test_face_recognition.py`](tests/test_face_recognition.py) and use the images in `tests/test_images/`. They cover image loading, face detection (HOG and CNN), batched detection, landmarks, and both command-line tools.

The project's `tox.ini` runs the tests and flake8 across several Python versions. Lint with:

```console
$ make lint
```

## Project structure

```
face_recognition/
├── face_recognition/          # Package source
│   ├── __init__.py            # Public API exports and version
│   ├── api.py                 # Detection, landmark, encoding, and comparison functions
│   ├── face_recognition_cli.py  # `face_recognition` command
│   └── face_detection_cli.py    # `face_detection` command
├── examples/                  # Example scripts, sample images, and sample videos
├── tests/                     # Unit tests and test images
├── docs/                      # Sphinx documentation sources
├── docker/                    # Additional Dockerfiles and Docker notes
├── Dockerfile, Dockerfile.gpu, docker-compose.yml
├── setup.py, setup.cfg, requirements*.txt, tox.ini, Makefile
└── HISTORY.rst                # Release history
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.rst](CONTRIBUTING.rst) for the development setup, testing, and pull request guidelines. Bug reports and feature requests can be filed at https://github.com/ageitgey/face_recognition/issues.

## Release history

Release notes are in [HISTORY.rst](HISTORY.rst). The most recent entry is version 1.4.0 (2020-09-26), which dropped Python 2.x support and added the `--upsample` option to the `face_recognition` command.

## Authors

See [AUTHORS.rst](AUTHORS.rst).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

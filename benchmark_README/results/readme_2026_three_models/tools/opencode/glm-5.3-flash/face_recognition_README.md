# face_recognition

Recognize faces from Python or from the command line. This library wraps dlib's state-of-the-art face recognition functionality to provide a simple API for finding faces in images, identifying facial features, computing 128-dimension face encodings, and comparing faces against each other.

- Version: 1.4.0
- Author: Adam Geitgey
- License: MIT

## Features

- **Find faces in images** — locate face bounding boxes in pictures using either a fast HOG-based detector (CPU-friendly) or a more accurate CNN-based deep-learning model (GPU/CUDA accelerated when available).
- **Identify facial features** — find the location of eyes, eyebrows, nose, chin, and lips with either the 68-point ("large") or faster 5-point ("small") pose models.
- **Compute face encodings** — generate a 128-dimension encoding (numerical vector) for each face in an image.
- **Compare faces** — match unknown face encodings against known face encodings using Euclidean distance, with a configurable tolerance (default `0.6`).
- **Batch face detection** — process batches of images through the CNN detector in one call; especially fast when using a GPU.
- **Command line tools** — two CLI commands (`face_recognition` and `face_detection`) installed as console scripts, with multi-core parallel processing support.

## Requirements

Python 3.5 or greater (the classifiers in `setup.py` list Python 3.5–3.9; support for Python 2.x was dropped in version 1.4.0).

Dependencies (installed automatically via `pip`):

- [face_recognition_models](https://github.com/ageitgey/face_recognition_models) (>= 0.3.0) — trained models used by this library
- [dlib](https://github.com/davisking/dlib) (>= 19.7 per `setup.py`; >= 19.3.0 per `requirements.txt`)
- Click (>= 6.0)
- numpy
- Pillow
- scipy (>= 0.17.0, listed in `requirements.txt`)

Note: `dlib` contains C++ code and may require a C++ toolchain (such as `cmake` and build tools) to compile if a pre-built wheel is not available for your platform.

## Installation

### Stable release

```sh
pip3 install face_recognition
```

### From sources

Clone the repository and install locally:

```sh
git clone git://github.com/ageitgey/face_recognition
cd face_recognition
python setup.py install
```

### Docker

Prebuilt CPU, GPU, and Jupyter/Kubeflow images are published on Docker Hub under [`animcogn/face_recognition`](https://hub.docker.com/repository/docker/animcogn/face_recognition). See [`docker/README.md`](docker/README.md) for the available image tags.

The CPU images run out of the box without driver prerequisites. The GPU images require the Nvidia drivers, the Nvidia container toolkit, and Docker configured to use the Nvidia container runtime.

Example Dockerfile using the prebuilt image:

```dockerfile
FROM animcogn/face_recognition:gpu

COPY requirements.txt requirements.txt

RUN pip3 install -r ./requirements.txt

COPY my_app /my_app

CMD [ "python3", "/my_app/my_app.py" ]
```

This repository also includes a sample [`Dockerfile`](Dockerfile) (based on `python:3.10.3-slim-bullseye`) that builds dlib v19.9 from source, installs the package, and runs an example script. You can run it with the included [`docker-compose.yml`](docker-compose.yml), which mounts the repository inside the container and runs an example; the GPU variant (`Dockerfile.gpu` and `runtime: nvidia`) can be enabled by uncommenting the commented lines.

To verify GPU setup inside a container, run:

```python
import dlib
print(dlib.cuda.get_num_devices())
```

## Usage

### Python API

```python
import face_recognition
```

The basic workflow is to load an image into a numpy array, then run operations on it:

```python
import face_recognition

image = face_recognition.load_image_file("your_file.jpg")

# Find all the faces in the image
face_locations = face_recognition.face_locations(image)

# Or maybe find the facial features in the image
face_landmarks_list = face_recognition.face_landmarks(image)

# Or you could get face encodings for each face in the image:
list_of_face_encodings = face_recognition.face_encodings(image)
```

Once you have face encodings, you can compare them to see if faces match:

```python
# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_face_encodings, a_single_unknown_face_encoding)
```

Computing a face encoding is somewhat slow, so consider caching results in a database if you need to refer to them later.

The public API (exported by the `face_recognition` package) consists of:

| Function | Purpose |
|---|---|
| `load_image_file(file, mode='RGB')` | Load an image file (.jpg, .png, etc.) into a numpy array. Supports `'RGB'` and `'L'` (black-and-white) modes. |
| `face_locations(img, number_of_times_to_upsample=1, model="hog")` | Return face bounding boxes as `(top, right, bottom, left)` tuples. `model` is `"hog"` (faster, CPU) or `"cnn"` (more accurate, GPU-accelerated when available). Higher `number_of_times_to_upsample` finds smaller faces. |
| `batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)` | Batched CNN face detection over a list of images. Mainly useful on a GPU; unnecessary when not using a GPU. |
| `face_landmarks(face_image, face_locations=None, model="large")` | Return a list of dicts of facial feature locations (`chin`, `left_eyebrow`, `right_eyebrow`, `nose_bridge`, `nose_tip`, `left_eye`, `right_eye`, `top_lip`, `bottom_lip`). `model="small"` uses a faster 5-point model and only returns `nose_tip`, `left_eye`, and `right_eye`. |
| `face_encodings(face_image, known_face_locations=None, num_jitters=1, model="small")` | Return a list of 128-dimensional face encodings. `model="large"` uses the 68-point pose predictor; higher `num_jitters` is more accurate but slower. |
| `compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)` | Compare a face encoding against a list of known encodings; returns a list of True/False matches. Lower tolerance is more strict; 0.6 is a typical best-performing value. |
| `face_distance(face_encodings, face_to_compare)` | Return the Euclidean distance between a face encoding and a list of encodings — lower means more similar. |

For a look at the full function signatures and parameters, see the docstrings in [`face_recognition/api.py`](face_recognition/api.py).

### Command line

Two commands are installed with the package.

#### `face_recognition` — identify who is in a picture

Compare images against a folder of known people. Each image in the known people folder should be named after the person it depicts (e.g. `obama.jpg`):

```sh
face_recognition ./folder_of_known_people ./image_to_check
```

If `image_to_check` is a directory, every image inside it is checked. Output is one line per detected face in the format `filename,person_name`; unmatched faces are reported as `unknown_person`, and images with no faces are reported as `no_persons_found`.

Options:

- `--cpus` — number of CPU cores to use in parallel (can speed up processing lots of images). `-1` means "use all in system". Default: `1`. (Requires Python 3.4+.)
- `--tolerance` — tolerance for face comparisons. Default is `0.6`. Lower it if you get multiple matches for the same person.
- `--show-distance` — output the face distance, which is useful for tweaking the tolerance setting.

#### `face_detection` — find where faces are in a picture

```sh
face_detection ./image_to_check
```

Output is one line per face in the format `filename,top,right,bottom,left`.

Options:

- `--cpus` — number of CPU cores to use in parallel. `-1` means "use all in system". Default: `1`.
- `--model` — which face detection model to use: `"hog"` (default, faster on CPU) or `"cnn"` (more accurate, GPU-accelerated when available).
- `--upsample` — how many times to upsample the image looking for faces. Higher numbers find smaller faces. Default: `0`.

## Examples

The [`examples/`](examples/) directory contains runnable scripts covering common use cases, including:

- [`recognize_faces_in_pictures.py`](examples/recognize_faces_in_pictures.py) — identify who is in a picture
- [`find_faces_in_picture.py`](examples/find_faces_in_picture.py) and [`find_faces_in_picture_cnn.py`](examples/find_faces_in_picture_cnn.py) — locate faces with HOG and CNN models
- [`find_faces_in_batches.py`](examples/find_faces_in_batches.py) — batched face detection (GPU-friendly)
- [`find_facial_features_in_picture.py`](examples/find_facial_features_in_picture.py) — facial landmarks
- [`identify_and_draw_boxes_on_faces.py`](examples/identify_and_draw_boxes_on_faces.py) — draw boxes and labels on detected faces
- [`facerec_from_webcam.py`](examples/facerec_from_webcam.py), [`facerec_from_webcam_faster.py`](examples/facerec_from_webcam_faster.py), and [`facerec_from_webcam_multiprocessing.py`](examples/facerec_from_webcam_multiprocessing.py) — real-time recognition from a webcam (requires OpenCV)
- [`facerec_from_video_file.py`](examples/facerec_from_video_file.py) — recognize faces in a video file (requires OpenCV)
- [`blur_faces_on_webcam.py`](examples/blur_faces_on_webcam.py) — automatically blur faces in a live webcam feed
- [`facerec_on_raspberry_pi.py`](examples/facerec_on_raspberry_pi.py) — face recognition on a Raspberry Pi
- [`face_recognition_knn.py`](examples/face_recognition_knn.py) and [`face_recognition_svm.py`](examples/face_recognition_svm.py) — classification with KNN and SVM (requires scikit-learn)
- [`blink_detection.py`](examples/blink_detection.py) — detect blinks using the 5-point model
- [`digital_makeup.py`](examples/digital_makeup.py) — apply "digital makeup" using facial landmarks
- [`face_distance.py`](examples/face_distance.py) — measure similarity between faces
- [`benchmark.py`](examples/benchmark.py) — benchmark detection speed on different image sizes
- [`web_service_example.py`](examples/web_service_example.py) — run recognition as a web service (requires Flask)
- [`facerec_ipcamera_knn.py`](examples/facerec_ipcamera_knn.py) — recognize faces from an IP camera stream
- [`ipynb_examples/track_faces_on_video_realtime.ipynb`](examples/ipynb_examples/track_faces_on_video_realtime.ipynb) — Jupyter Notebook example
- Simplified Chinese variants of some examples (`facerec_on_raspberry_pi_Simplified_Chinese.py`, `web_service_example_Simplified_Chinese.py`)

The `examples/knn_examples/` folder includes sample training and test images for the KNN example.

## Development

To set up for local development:

1. Fork the repo on GitHub, then clone your fork locally.
2. Install your local copy into a virtualenv: `python setup.py develop`.
3. Create a branch for your changes: `git checkout -b name-of-your-bugfix-or-feature`.

### Running the tests

Run the full test suite across Python versions with tox:

```sh
tox
```

Or run tests with the default Python (per the `Makefile`):

```sh
python3 setup.py test
```

To run a subset of tests:

```sh
python -m unittest tests.test_face_recognition
```

### Linting

Check style with flake8 (configuration in `setup.cfg`):

```sh
flake8 face_recognition tests
```

### Documentation

Sphinx documentation lives in [`docs/`](docs/). Build it with:

```sh
make docs
```

### Contributing

Contributions are welcome. Please:

- Report bugs at https://github.com/ageitgey/face_recognition/issues, including your operating system name and version, details about your local setup, and detailed steps to reproduce the bug.
- Submit feature requests and feedback via GitHub issues as well.
- Before submitting a pull request, include tests, update the docs when adding functionality, and check that the tests pass.

## Credits

- **Adam Geitgey** — author of this library.
- **Davis King** — creator of [dlib](https://github.com/davisking/dlib) and provider of the trained facial feature detection and face encoding models used here.
- The many Python data science library authors (numpy, scipy, scikit-image, Pillow, etc.).
- This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the `audreyr/cookiecutter-pypackage` project template.

## License

This project is licensed under the MIT License — see the [`LICENSE`](LICENSE) file for details.

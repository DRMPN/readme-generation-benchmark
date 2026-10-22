# face_recognition

Recognize and manipulate faces from Python or from the command line with the world's simplest face recognition library.

**face_recognition** is a Python library (version 1.4.0) built on top of [dlib](https://github.com/davisking/dlib) that lets you:

* Find faces in pictures (using HOG or CNN-based detection models)
* Find and identify facial features such as eyes, eyebrows, nose, mouth, and chin
* Compute 128-dimensional face encodings for faces in images
* Compare face encodings to identify people, or measure how similar two faces are

The library was created by Adam Geitgey and ships with the trained facial feature detection and face encoding models used by dlib (via the `face_recognition_models` package).

## Features

The main `face_recognition` module exposes the following API functions:

* `load_image_file(file, mode='RGB')` — Load an image file (`.jpg`, `.png`, etc.) into a numpy array.
* `face_locations(img, number_of_times_to_upsample=1, model="hog")` — Find all faces in an image and return their bounding boxes as `(top, right, bottom, left)` tuples. The `model` parameter can be `"hog"` (fast on CPU) or `"cnn"` (more accurate, GPU/CUDA accelerated when available).
* `batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)` — Find faces in a list of images using the CNN model in GPU-friendly batches.
* `face_landmarks(face_image, face_locations=None, model="large")` — Return a dict of facial feature locations (chin, eyebrows, eyes, nose bridge, nose tip, lips) for each face. A faster `"small"` 5-point model is also available.
* `face_encodings(face_image, known_face_locations=None, num_jitters=1, model="small")` — Return 128-dimension face encodings for each face in the image.
* `compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)` — Compare a face encoding against a list of known encodings and return a list of True/False matches.
* `face_distance(face_encodings, face_to_compare)` — Compute the Euclidean distance between face encodings to measure similarity. Faces with a distance of 0.6 or less are typically considered a match; use a smaller cutoff (e.g. 0.55) to reduce false positives.

## Installation

Install the stable release with pip:

```bash
$ pip3 install face_recognition
```

Or install from source:

```bash
$ git clone git://github.com/ageitgey/face_recognition
$ cd face_recognition
$ python setup.py install
```

Note: the library depends on `dlib` (>= 19.7), which must be compiled; other dependencies include `face_recognition_models` (>= 0.3.0), `Click` (>= 6.0), `numpy`, and `Pillow`. If you see an error asking for `face_recognition_models`, install it with:

```bash
pip install git+https://github.com/ageitgey/face_recognition_models
```

## Usage

### Python API

The basic workflow is: load an image, find faces, then analyze or compare them.

```python
import face_recognition

image = face_recognition.load_image_file("your_file.jpg")

# Find all the faces in the image
face_locations = face_recognition.face_locations(image)

# Or find the facial features in the image
face_landmarks_list = face_recognition.face_landmarks(image)

# Or get face encodings for each face in the image
list_of_face_encodings = face_recognition.face_encodings(image)
```

Face encodings can be compared against each other to see if the faces match:

```python
# results is an array of True/False telling if the unknown face matched
# anyone in the known_faces array
results = face_recognition.compare_faces(known_face_encodings, a_single_unknown_face_encoding)
```

Finding the encoding for a face is a bit slow, so consider saving the results for each image in a database or cache if you need to refer back to them later.

### Command Line

Two console commands are installed with the package:

**`face_recognition`** — Recognize faces in a photo or folder of photos against a folder of known people:

```bash
$ face_recognition ./folder_of_known_people.jpg ./image_to_check.jpg
```

Options:

* `--cpus` — Number of CPU cores to use in parallel (can speed up processing lots of images). `-1` means "use all in system". Multi-core processing requires Python 3.4 or greater.
* `--tolerance` — Tolerance for face comparisons. Default is 0.6. Lower it if you get multiple matches for the same person.
* `--show-distance` — Output the face distance. Useful for tweaking the tolerance setting.
* `--upsample` — How many times to upsample the image looking for faces (added in 1.4.0). Higher numbers find smaller faces.

Results are printed as `filename,name` (and optionally the distance), with `unknown_person` and `no_persons_found` used when no match or no faces are found.

**`face_detection`** — Find the locations of faces in a photo or folder of photos:

```bash
$ face_detection ./image_to_check.jpg
```

Options:

* `--cpus` — Number of CPU cores to use in parallel (`-1` for all).
* `--model` — Which face detection model to use: `"hog"` (default) or `"cnn"`.
* `--upsample` — How many times to upsample the image looking for faces.

Results are printed as `filename,top,right,bottom,left`.

### Examples

The `examples/` folder contains runnable example scripts covering many use cases, including:

* `recognize_faces_in_pictures.py` — Identify known people in photos.
* `find_faces_in_picture.py` / `find_faces_in_picture_cnn.py` — Locate faces using the HOG or CNN model.
* `find_facial_features_in_picture.py` and `digital_makeup.py` — Work with facial landmarks.
* `face_distance.py` — Measure similarity between faces.
* `facerec_from_webcam.py`, `facerec_from_webcam_faster.py`, and `facerec_from_webcam_multiprocessing.py` — Real-time face recognition from a webcam (requires OpenCV).
* `facerec_from_video_file.py` — Recognize faces in a video file and write labeled output.
* `find_faces_in_batches.py` — Batch face detection across video frames on a GPU.
* `blur_faces_on_webcam.py` — Automatically blur faces in a live video feed.
* `blink_detection.py` — Detect eye closure using facial landmarks.
* `facerec_on_raspberry_pi.py` (also available in Simplified Chinese) — Run face recognition on a Raspberry Pi with the `picamera` module.
* `face_recognition_knn.py` / `face_recognition_svm.py` — Train a classifier (scikit-learn required) to recognize many different people.
* `facerec_ipcamera_knn.py` — Recognize faces from an IP camera stream.
* `web_service_example.py` — A simple Flask web service that reports whether an uploaded photo is a picture of Barack Obama (also available in Simplified Chinese).
* `benchmark.py` — Benchmark face detection, landmark, and encoding speeds at different image resolutions.
* `ipynb_examples/track_faces_on_video_realtime.ipynb` — A Jupyter Notebook demo of realtime face tracking in video.

Most webcam/video examples require OpenCV (`pip3 install opencv-python`), but OpenCV is not required to use the `face_recognition` library itself — it is only needed to read from webcams or video files.

## Docker

Docker images are provided for easy deployment:

* `Dockerfile` — A sample Dockerfile based on `python:3.10.3-slim-bullseye` that installs dlib v19.9 and the library, then runs `recognize_faces_in_pictures.py`.
* `docker/cpu/Dockerfile` — A multi-stage CPU build (based on `animcogn/face_recognition:cpu`).
* `docker/gpu/Dockerfile` — A CUDA 11.2 / cuDNN 8 based GPU build (requires Nvidia drivers and the Nvidia container runtime).
* `docker/cpu-jupyter-kubeflow/` and `docker/gpu-jupyter-kubeflow/` — JupyterLab variants intended for deployment on Kubeflow, exposing Jupyter on port 8888.

A `docker-compose.yml` is included that builds the image and runs an example (`find_faces_in_picture_cnn.py`); uncomment the `Dockerfile.gpu` lines and the `runtime: nvidia` option to run it on the GPU.

Up-to-date prebuilt images are available on Docker Hub under [`animcogn/face_recognition`](https://hub.docker.com/repository/docker/animcogn/face_recognition), with tags such as `cpu`, `gpu`, `cpu-jupyter-kubeflow`, and `gpu-jupyter-kubeflow`. To verify GPU support inside a container, run:

```python
import dlib
print(dlib.cuda.get_num_devices())
```

## Development

To set up `face_recognition` for local development:

1. Fork the repo on GitHub and clone your fork locally.
2. Install your local copy into a virtualenv:
   ```bash
   $ mkvirtualenv face_recognition
   $ cd face_recognition/
   $ python setup.py develop
   ```
3. Create a branch for your bug fix or feature:
   ```bash
   $ git checkout -b name-of-your-bugfix-or-feature
   ```

A `Makefile` provides common development tasks (run `make help` to list them):

* `make test` — Run tests quickly with the default Python (`python3 setup.py test`).
* `make test-all` — Run tests on every Python version with tox.
* `make lint` — Check style with flake8 (max line length 160).
* `make coverage` — Check code coverage with coverage.py and open the HTML report.
* `make docs` — Generate Sphinx HTML documentation, including API docs (`sphinx-apidoc`), and open it in a browser.
* `make dist` / `make release` — Build sdist/wheel packages and upload a release with twine.
* `make clean` — Remove build, test, and Python artifacts.

Version numbers are managed with `bumpversion` (configured in `setup.cfg`, currently at version 1.4.0, updating `setup.py` and `face_recognition/__init__.py`).

To run a subset of tests:

```bash
$ python -m unittest tests.test_face_recognition
```

## Testing

Tests live in `tests/test_face_recognition.py` and use `unittest` plus Click's `CliRunner` to exercise both the Python API and the command-line interfaces. They cover image loading, HOG and CNN face detection (including batched detection and partial faces), facial landmarks (68-point and 5-point models), face encodings, face distances, and face comparison — using test images in `tests/test_images/`.

Continuous integration runs via GitHub Actions (`.github/workflows/main.yml`) on Python 3.8, 3.9, and 3.10, installing the package and running `tox`. The `tox.ini` configuration maps GitHub Actions Python versions to test environments (`py35`–`py38` plus `flake8`) and runs the tests with `python -m unittest discover`.

## Contributing

Contributions are welcome! Bug reports and feature requests can be filed at https://github.com/ageitgey/face_recognition/issues. When reporting a bug, please include your OS name and version, details about your local setup, detailed steps to reproduce the issue, and (if relevant) the picture involved.

Pull requests should include tests, update the docs if new functionality is added, and pass flake8 and the test suite.

## History

Notable releases (see `HISTORY.rst` for the full changelog):

* **1.4.0 (2020-09-26)** — Dropped Python 2.x support; added `--upsample` parameter to the command-line `face_recognition` tool.
* **1.3.0 (2020-02-20)** — Dropped Python 3.4, added 3.8 support; added a blink detection example.
* **1.2.3 (2018-08-21)** — Added `model="small"` support to `face_landmarks()`; Jupyter Notebook example.
* **1.2.2 (2018-04-02)** — Added the `face_detection` CLI command; removed the scipy dependency.
* **1.1.0 (2017-09-23)** — Use dlib's 5-point face pose estimator when possible for speed.
* **1.0.0 (2017-08-29)** — Added CNN face detection and GPU batched face detection support.
* **0.1.13 (2017-04-20)** — Raspberry Pi support.

## Authors

Created and maintained by **Adam Geitgey** (<ageitgey@gmail.com>).

Special thanks to Davis King (@nulhom) for creating dlib and providing the trained facial feature detection and face encoding models, to the maintainers of the Python data science ecosystem (numpy, scipy, scikit-image, Pillow, etc.), and to the Cookiecutter / audreyr/cookiecutter-pypackage project template.

## License

This project is licensed under the **MIT License** — Copyright (c) 2021, Adam Geitgey. See the `LICENSE` file for the full license text.

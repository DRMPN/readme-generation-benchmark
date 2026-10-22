# face_recognition

`face_recognition` is a Python library for detecting faces in images, locating facial features, generating face encodings, and comparing faces. It also provides command-line tools and examples for working with image folders, video, webcams, and other applications.

The library uses dlib and pretrained models supplied by `face_recognition_models`. Its API includes HOG-based face detection, a CNN detector, facial landmarks, 128-dimensional face encodings, and distance-based face comparisons.

## Features

- Load image files into NumPy arrays.
- Find face locations using the default HOG detector or the CNN detector.
- Detect faces in batches with the CNN detector.
- Return facial landmarks using a large (68-point) or small (5-point) model.
- Create and compare face encodings.
- Use command-line tools for face recognition and face detection.
- Explore additional examples for KNN and SVM classification, image processing, video, webcams, and web services.

## Installation

Install the stable package with pip:

```bash
pip3 install face_recognition
```

The package depends on dlib, `face_recognition_models`, Click, NumPy, and Pillow. Installing dlib may require native build tools and libraries, depending on your operating system and Python environment. The repository includes Dockerfiles that install build dependencies and build dlib for CPU or GPU use.

To install from a local checkout:

```bash
git clone https://github.com/ageitgey/face_recognition.git
cd face_recognition
python3 setup.py install
```

For development, see [Development](#development).

## Basic usage

Load an image and find faces, landmarks, or encodings:

```python
import face_recognition

image = face_recognition.load_image_file("your_file.jpg")

face_locations = face_recognition.face_locations(image)
face_landmarks = face_recognition.face_landmarks(image)
face_encodings = face_recognition.face_encodings(image)
```

`load_image_file()` returns a NumPy array. If your image is already an array in a supported format, you can pass it directly to the API.

Compare an encoding against known encodings:

```python
matches = face_recognition.compare_faces(
    known_face_encodings,
    face_encodings[0],
)
```

The result is a list of booleans, one for each known encoding. To examine similarity as a distance rather than a match decision, use:

```python
distances = face_recognition.face_distance(
    known_face_encodings,
    face_encodings[0],
)
```

Face encodings take time to calculate. If you need to compare the same known images repeatedly, consider retaining their encodings rather than recalculating them each time.

See the `examples/` directory and the API reference in `docs/` for more examples and function details.

## Detection models and configuration

`face_locations()` accepts a `model` parameter:

```python
locations = face_recognition.face_locations(image, model="hog")
cnn_locations = face_recognition.face_locations(image, model="cnn")
```

The default `hog` model is faster on CPUs. The `cnn` model is more accurate and can use GPU acceleration when dlib is built with CUDA support. The `number_of_times_to_upsample` parameter controls how many times the image is upsampled while searching; higher values can help find smaller faces. It defaults to `1` in the Python API.

For batches of images, `batch_face_locations()` uses the CNN detector. Its `batch_size` defaults to `128`; batch processing can be useful with a CUDA-enabled GPU. The API documentation describes its parameters and return values.

For facial landmarks, `face_landmarks()` accepts `model="large"` (the default, 68 points) or `model="small"` (5 points). Face comparisons use a default tolerance of `0.6`; lowering the tolerance makes matching stricter. The appropriate setting depends on the application.

## Command-line tools

Installing the package provides two commands.

### Recognize faces

```bash
face_recognition <known_people_folder> <image_or_folder_to_check>
```

Put known-person images directly in `known_people_folder`; each image’s filename, without its extension, is used as the person’s name. The image argument can be one image or a folder of images.

Options include:

- `--tolerance`: comparison threshold; defaults to `0.6`.
- `--cpus`: number of CPU cores for processing a folder; defaults to `1`, and `-1` uses all available cores.
- `--show-distance`: include face distance in output.

For example:

```bash
face_recognition known_people/ unknown_images/ --tolerance 0.55 --show-distance 1
```

### Detect faces

```bash
face_detection <image_or_folder_to_check>
```

The output contains the image filename and face coordinates in `top,right,bottom,left` order. Options include `--model` (`hog` or `cnn`), `--upsample` (default `0` in this command), and `--cpus` for processing folders.

Use `--help` with either command to see its available options.

## Examples and optional dependencies

The `examples/` directory contains scripts for single-image detection, landmarks, face comparison, KNN and SVM classification, batch processing, video files, webcams, Raspberry Pi cameras, and a sample Flask upload service. Some examples need dependencies beyond the core package:

- Webcam and video examples use OpenCV (`cv2`).
- The KNN and SVM examples use scikit-learn.
- The web service example uses Flask.
- The Raspberry Pi example uses `picamera`.

These are example-specific dependencies, not requirements for using the core library.

## Docker

The repository includes a sample root `Dockerfile`, a GPU-oriented Dockerfile, Docker Compose configuration, and CPU/GPU images under `docker/`. The Docker documentation also describes CPU, GPU, and Jupyter images, with prebuilt images published under the `animcogn/face_recognition` Docker Hub repository.

CPU images are described as running without driver prerequisites. GPU images require NVIDIA drivers, the NVIDIA Docker container runtime, and Docker configured to use it. GPU support also depends on dlib being built with CUDA. See [`docker/README.md`](docker/README.md) for image details and GPU checks.

## Development

Contributions are welcome. The project’s contribution guide recommends forking and cloning the repository, then installing the checkout in development mode:

```bash
python setup.py develop
```

Install the development dependencies with:

```bash
pip install -r requirements_dev.txt
```

Create a branch for your change, include tests, and update documentation when adding functionality. Bug reports should include the operating system, Python version, relevant setup details, and steps to reproduce the problem.

## Testing and code quality

Run the test suite with:

```bash
python3 setup.py test
```

Or run unittest discovery:

```bash
python -m unittest discover
```

The Makefile provides shortcuts:

```bash
make test
make lint
make test-all
```

`make lint` runs flake8 on `face_recognition` and `tests`; `make test-all` runs tox. The tox configuration defines test environments and a flake8 environment. GitHub Actions also runs package setup checks and tox on its configured Python matrix.

Build the Sphinx HTML documentation with:

```bash
make docs
```

This generates API documentation and builds the pages under `docs/`.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE) for the full license text.

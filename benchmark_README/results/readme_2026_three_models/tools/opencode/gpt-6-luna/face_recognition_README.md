# face_recognition

`face_recognition` is a Python library for locating faces in images, extracting facial landmarks and face encodings, and comparing encodings to recognize faces. It also provides command-line tools for face detection and for matching faces against a directory of known people.

This repository contains version **1.4.0** of the package. The library uses [dlib](http://dlib.net/) for face detection, facial landmarks, and face encodings.

## Features

- Detect faces with dlib's HOG detector or CNN detector.
- Detect faces in batches with the CNN detector.
- Return facial landmarks using 5-point (`small`) or 68-point (`large`) models.
- Generate 128-dimensional face encodings and compare them using Euclidean distance and a configurable tolerance.
- Use the `face_recognition` and `face_detection` command-line programs.
- Explore additional use cases in the [`examples/`](examples/) directory, including webcam and video examples, K-nearest-neighbors classification, and face blurring.

## Installation

Install the published package with pip:

```bash
python -m pip install face_recognition
```

The package depends on dlib, `face_recognition_models`, Click, NumPy, and Pillow. See [`setup.py`](setup.py) for the package's declared dependencies. dlib's CNN detector can use a GPU when a suitable CUDA-enabled dlib installation is available; the default HOG detector runs without that requirement.

## Quick start

Load an image, find faces, and compare face encodings:

```python
import face_recognition

image = face_recognition.load_image_file("photo.jpg")
locations = face_recognition.face_locations(image)
encodings = face_recognition.face_encodings(image)

print(f"Found {len(locations)} face(s)")

if len(encodings) >= 2:
    print(face_recognition.compare_faces([encodings[0]], encodings[1]))
```

`load_image_file` returns a NumPy array, converted to RGB by default. `face_locations` returns one `(top, right, bottom, left)` tuple per detected face. `face_encodings` returns one 128-dimensional encoding per face; if no face is found, the returned list is empty. To compare an unknown encoding with known encodings, use `compare_faces` or `face_distance`.

## Python API

The public functions are exported from `face_recognition`:

| Function | Purpose |
| --- | --- |
| `load_image_file(file, mode="RGB")` | Load an image file or file object as a NumPy array. `mode` supports `"RGB"` and `"L"`. |
| `face_locations(image, number_of_times_to_upsample=1, model="hog")` | Find faces and return `(top, right, bottom, left)` locations. `model` can be `"hog"` or `"cnn"`. |
| `batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)` | Find face locations for a list of images using the CNN detector. |
| `face_landmarks(image, face_locations=None, model="large")` | Return facial feature points for each face. `model` is `"large"` (68 points) or `"small"` (5 points). |
| `face_encodings(image, known_face_locations=None, num_jitters=1, model="small")` | Return a 128-dimensional encoding for each face. Existing locations can be supplied to avoid detecting faces again. |
| `compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)` | Return a Boolean result for each known encoding; a lower tolerance is stricter. |
| `face_distance(face_encodings, face_to_compare)` | Return the Euclidean distance from the candidate encoding to each supplied encoding. Lower distances indicate more similar encodings. |

See [`docs/`](docs/) and the scripts in [`examples/`](examples/) for further usage. Face encoding generation can take time; if the same images are used repeatedly, the usage documentation recommends saving or caching their encodings.

## Command-line tools

The package installs two commands.

### Recognize faces in images

Provide a directory of known-person images and either an image file or a directory to check:

```bash
face_recognition ./known_people ./unknown.jpg
face_recognition ./known_people ./photos --cpus 2 --tolerance 0.5 --show-distance True
```

For the known-person directory, each image filename (without its extension) is used as the person's name. If an image contains multiple faces, only its first face is used; images without faces are ignored with a warning. When checking images, the command prints comma-separated filename and matching name values. It can print distances with `--show-distance`; images with no detected faces are reported as `no_persons_found`, and unmatched faces as `unknown_person`. The default comparison tolerance is `0.6`. `--cpus -1` uses all available CPUs when processing a directory.

### Detect faces

```bash
face_detection ./photo.jpg
face_detection ./photos --model cnn --upsample 1 --cpus 2
```

The command accepts an image or a directory. It prints comma-separated filename and face coordinates in `(top, right, bottom, left)` order. `--model` selects `hog` (the default) or `cnn`; `--upsample` controls image upsampling for detection, and `--cpus` controls parallel processing of a directory (`-1` uses all available CPUs).

Run either command with `--help` to see its available options.

## Examples

The [`examples/`](examples/) directory contains runnable scripts for still-image face detection, facial landmarks, face comparisons, KNN classification, webcam and video workflows, and other demonstrations. Some examples use additional libraries or hardware beyond the core package dependencies; check each example's imports and comments for its requirements.

## Tests and contributing

The repository includes tests in [`tests/`](tests/). The contribution guide documents the development checks, including:

```bash
python -m unittest tests.test_face_recognition
flake8 face_recognition tests
tox
```

See [`CONTRIBUTING.rst`](CONTRIBUTING.rst) for the contribution workflow and bug-reporting guidance.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE).

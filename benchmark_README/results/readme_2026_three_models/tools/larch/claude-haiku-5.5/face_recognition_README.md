# face_recognition

A Python library for recognizing and manipulating faces, built on top of [dlib](http://dlib.net/)'s state-of-the-art face recognition. You can detect faces, locate facial landmarks, compare faces, and identify people, all with a simple API. The library also ships with command-line tools for batch processing and a set of example scripts for webcams, video files, Raspberry Pi, and web services.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Linux (Ubuntu/Debian)](#linux-ubuntudebian)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Raspberry Pi](#raspberry-pi)
  - [Installing from Source](#installing-from-source)
  - [Docker](#docker)
  - [GPU Support](#gpu-support)
- [Quick Start](#quick-start)
- [Python API](#python-api)
  - [load_image_file](#load_image_file)
  - [face_locations](#face_locations)
  - [batch_face_locations](#batch_face_locations)
  - [face_landmarks](#face_landmarks)
  - [face_encodings](#face_encodings)
  - [compare_faces](#compare_faces)
  - [face_distance](#face_distance)
- [Command-Line Interface](#command-line-interface)
  - [face_recognition](#face_recognition-command)
  - [face_detection](#face_detection-command)
- [Examples](#examples)
- [Tutorials and Recipes](#tutorials-and-recipes)
- [Performance Tips](#performance-tips)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [Authors](#authors)
- [License](#license)

---

## Features

- **Face detection** using either a fast HOG-based model or a more accurate CNN model (requires GPU for good performance).
- **Facial landmark detection** for eyes, eyebrows, nose, lips, and chin (68-point model, plus a 5-point model).
- **Face encoding** that turns each face into a 128-dimensional vector.
- **Face comparison and identification** by measuring the distance between encodings.
- **Batch processing** of multiple images for better throughput on GPUs.
- **Command-line tools** for recognizing and detecting faces in folders of images without writing any code.
- **Image manipulation examples** such as blurring faces, adding digital makeup, and drawing boxes around faces.
- **Real-time examples** for webcams, IP cameras, video files, and Raspberry Pi.
- **Web service example** for exposing face recognition over HTTP.

---

## Project Structure

```
face_recognition/
├── face_recognition/            # Core Python package
│   ├── __init__.py
│   ├── api.py                   # Main public API (face_locations, face_encodings, etc.)
│   ├── face_recognition_cli.py  # `face_recognition` CLI tool
│   ├── face_detection_cli.py    # `face_detection` CLI tool
│   └── test_face_recognition.py # Unit tests
├── examples/                    # Example scripts and sample images/videos
│   ├── find_faces_in_picture.py
│   ├── find_faces_in_picture_cnn.py
│   ├── find_faces_in_batches.py
│   ├── find_facial_features_in_picture.py
│   ├── identify_and_draw_boxes_on_faces.py
│   ├── recognize_faces_in_pictures.py
│   ├── face_recognition_knn.py
│   ├── face_recognition_svm.py
│   ├── facerec_from_webcam.py
│   ├── facerec_from_webcam_faster.py
│   ├── facerec_from_webcam_multiprocessing.py
│   ├── facerec_from_video_file.py
│   ├── facerec_ipcamera_knn.py
│   ├── facerec_on_raspberry_pi.py
│   ├── facerec_on_raspberry_pi_Simplified_Chinese.py
│   ├── blink_detection.py
│   ├── blur_faces_on_webcam.py
│   ├── digital_makeup.py
│   ├── face_distance.py
│   ├── benchmark.py
│   ├── track_faces_on_video_realtime.ipynb
│   ├── web_service_example.py
│   ├── web_service_example_Simplified_Chinese.py
│   └── ...                      # Sample images and videos
├── docs/                        # Sphinx documentation sources
│   ├── conf.py
│   ├── index.rst
│   ├── installation.rst
│   ├── usage.rst
│   ├── face_recognition.rst
│   ├── modules.rst
│   ├── contributing.rst
│   ├── authors.rst
│   ├── history.rst
│   ├── Makefile
│   └── make.bat
├── Dockerfile                   # CPU Docker image
├── Dockerfile.gpu               # GPU Docker image
├── Dockerfile-python-example    # Docker image for running the Python examples
├── docker-compose.yml
├── setup.py
├── setup.cfg
├── pyproject.toml
├── requirements.txt
├── requirements_dev.txt
├── requirements_docs.txt
├── tox.ini
├── MANIFEST.in
├── Makefile
├── README.md
├── HISTORY.rst
├── AUTHORS.rst
├── CONTRIBUTING.rst
└── LICENSE
```

---

## Requirements

- **Python** 3.x (3.3 or newer; a recent 3.8+ version is recommended)
- **dlib** (built with C++ support, and optionally CUDA for GPU acceleration)
- **numpy**
- **Pillow**
- **Click** (used by the command-line tools)
- **CMake** (required to build dlib)
- For examples: **OpenCV** (`opencv-python`) and other packages listed in the examples

Dependencies are listed in `requirements.txt`, `setup.py`, and `pyproject.toml`.

---

## Installation

The easiest way to install is with pip:

```bash
pip install face_recognition
```

This compiles dlib during installation, which can take a while and requires a C++ compiler and CMake. Platform-specific instructions follow.

### Linux (Ubuntu/Debian)

```bash
# Install build tools and dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake
sudo apt-get install -y libopenblas-dev liblapack-dev
sudo apt-get install -y libx11-dev libgtk-3-dev   # Only needed for the dlib GUI features / some examples

# Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install face_recognition
pip install face_recognition
```

### macOS

```bash
# Install CMake using Homebrew
brew install cmake

# Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

pip install face_recognition
```

### Windows

1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) with the "Desktop development with C++" workload.
2. Install [CMake](https://cmake.org/download/) and make sure it is on your `PATH`.
3. Install the package:

```bash
python -m venv venv
venv\Scripts\activate
pip install face_recognition
```

Prebuilt dlib wheels for Windows are sometimes available, which can avoid compiling from source. If `pip install dlib` fails, search for a wheel matching your Python version.

### Raspberry Pi

Building dlib on a Raspberry Pi is slow. Expect it to take a long time, and make sure you have adequate swap space.

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake libopenblas-dev liblapack-dev
pip3 install face_recognition
```

The file `examples/facerec_on_raspberry_pi.py` demonstrates real-time recognition on a Pi camera. A Simplified Chinese version of the same tutorial is also included.

### Installing from Source

```bash
git clone https://github.com/ageitgey/face_recognition.git
cd face_recognition
pip install -r requirements.txt
python setup.py install
```

To install in editable/development mode:

```bash
pip install -e .
```

### Docker

The repository includes Dockerfiles so you can run the library without configuring a local environment.

**Build the CPU image:**

```bash
docker build -t face_recognition .
```

**Run an interactive container:**

```bash
docker run -ti --rm face_recognition
```

**Run an example with your local images mounted:**

```bash
docker run -ti --rm -v $(pwd):/mnt face_recognition face_recognition /mnt/known /mnt/unknown
```

**Using docker-compose:**

```bash
docker-compose up --build
```

**Python examples container:** `Dockerfile-python-example` builds an image that includes the example scripts and their dependencies.

### GPU Support

To use the CNN face detector and dlib with CUDA acceleration, you need:

- An NVIDIA GPU with CUDA installed
- cuDNN
- dlib compiled with CUDA support

`Dockerfile.gpu` provides a container with these pieces configured:

```bash
docker build -f Dockerfile.gpu -t face_recognition_gpu .
docker run --gpus all -ti --rm face_recognition_gpu
```

---

## Quick Start

Recognize a face in an unknown image using a known image of a person:

```python
import face_recognition

# Load known image and compute its face encoding
known_image = face_recognition.load_image_file("obama.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Load an unknown image
unknown_image = face_recognition.load_image_file("unknown.jpg")
unknown_encodings = face_recognition.face_encodings(unknown_image)

for unknown_encoding in unknown_encodings:
    results = face_recognition.compare_faces([known_encoding], unknown_encoding)
    print("Match!" if results[0] else "Not a match.")
```

Find all faces in a picture:

```python
import face_recognition

image = face_recognition.load_image_file("two_people.jpg")
face_locations = face_recognition.face_locations(image)

print(f"Found {len(face_locations)} face(s) in this photograph.")
for top, right, bottom, left in face_locations:
    print(f"Face at top={top}, right={right}, bottom={bottom}, left={left}")
```

---

## Python API

All public functions live in `face_recognition/api.py` and are exposed at the package level via `import face_recognition`.

### load_image_file

```python
face_recognition.load_image_file(file, mode='RGB')
```

Loads an image file (JPEG, PNG, etc.) into a NumPy array.

| Parameter | Type | Description |
|-----------|------|-------------|
| `file` | str or file-like | Path or file object for the image. |
| `mode` | str | `'RGB'` (default) or `'L'` (grayscale). |

**Returns:** `numpy.ndarray` of shape `(height, width, 3)` for RGB.

### face_locations

```python
face_recognition.face_locations(img, number_of_times_to_upsample=1, model="hog")
```

Finds all faces in an image.

| Parameter | Type | Description |
|-----------|------|-------------|
| `img` | numpy.ndarray | Image to search. |
| `number_of_times_to_upsample` | int | How many times to upsample the image before searching. Higher values find smaller faces but run slower. |
| `model` | str | `"hog"` (CPU, fast, default) or `"cnn"` (more accurate, GPU recommended). |

**Returns:** A list of tuples `(top, right, bottom, left)` in pixel coordinates.

```python
image = face_recognition.load_image_file("biden.jpg")
locations = face_recognition.face_locations(image, model="cnn")
```

### batch_face_locations

```python
face_recognition.batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)
```

Finds faces in a list of images in a single batch. Requires the CNN model and benefits greatly from a GPU.

| Parameter | Type | Description |
|-----------|------|-------------|
| `images` | list of numpy.ndarray | Images to process. All must have the same dimensions. |
| `number_of_times_to_upsample` | int | Upsampling count. |
| `batch_size` | int | Number of images processed per GPU batch. |

**Returns:** A list, one entry per image, each containing a list of face location tuples.

### face_landmarks

```python
face_recognition.face_landmarks(face_image, face_locations=None, model="large")
```

Finds facial features such as eyes, nose, lips, and chin.

| Parameter | Type | Description |
|-----------|------|-------------|
| `face_image` | numpy.ndarray | Image containing faces. |
| `face_locations` | list | Optional pre-computed face locations. If omitted, they are detected automatically. |
| `model` | str | `"large"` (68 points) or `"small"` (5 points). |

**Returns:** A list of dictionaries, one per face, mapping feature names to lists of `(x, y)` points. Feature names include `chin`, `left_eyebrow`, `right_eyebrow`, `nose_bridge`, `nose_tip`, `left_eye`, `right_eye`, `top_lip`, and `bottom_lip`. The `small` model returns only `nose_tip`, `left_eye`, and `right_eye`.

```python
landmarks = face_recognition.face_landmarks(image)
print(landmarks[0]["left_eye"])
```

### face_encodings

```python
face_recognition.face_encodings(face_image, known_face_locations=None, num_jitters=1, model="small")
```

Computes a 128-dimensional encoding for each face. These encodings are used for comparison.

| Parameter | Type | Description |
|-----------|------|-------------|
| `face_image` | numpy.ndarray | Image containing faces. |
| `known_face_locations` | list | Optional pre-computed face locations. |
| `num_jitters` | int | Number of times to re-sample the face when computing the encoding. Higher values are more accurate but slower. |
| `model` | str | `"small"` (default, faster) or `"large"`. |

**Returns:** A list of 128-element NumPy arrays, one per face.

### compare_faces

```python
face_recognition.compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)
```

Compares a face encoding against a list of known encodings.

| Parameter | Type | Description |
|-----------|------|-------------|
| `known_face_encodings` | list | List of known face encodings. |
| `face_encoding_to_check` | numpy.ndarray | Encoding to compare. |
| `tolerance` | float | Maximum distance for a match. Lower is stricter. `0.6` is the default and works well in most cases. |

**Returns:** A list of booleans, one per known encoding.

### face_distance

```python
face_recognition.face_distance(face_encodings, face_to_compare)
```

Computes the Euclidean distance between a face encoding and a list of encodings. Lower distances mean more similar faces.

**Returns:** A NumPy array of distances. A distance below about `0.6` is generally considered a match.

```python
distances = face_recognition.face_distance(known_encodings, unknown_encoding)
best_match_index = distances.argmin()
```

---

## Command-Line Interface

Installing the package also installs two command-line tools.

### face_recognition Command

Identifies people in a folder of images using a folder of known faces. Each subfolder inside the known folder is named after a person and contains images of them.

```
known_people/
├── alice/
│   ├── alice1.jpg
│   └── alice2.jpg
└── bob/
    └── bob1.jpg
```

Run it against a folder of unknown images:

```bash
face_recognition ./known_people ./unknown_pictures
```

Output is one line per detected face in the form `filename,person_name`, with `unknown_person` for unmatched faces.

**Options:**

| Option | Description |
|--------|-------------|
| `--show-distance true` | Shows the face distance alongside each result. |
| `--tolerance 0.6` | Sets the match threshold. |
| `--cpus 4` | Number of CPU cores to use in parallel. Use `-1` for all cores. |

Example:

```bash
face_recognition --tolerance 0.5 --show-distance true --cpus -1 ./known_people ./unknown_pictures
```

### face_detection Command

Detects faces in a single image or a folder of images and prints the file name and face location.

```bash
face_detection ./pictures
face_detection --model cnn --cpus 4 ./pictures
```

**Options:**

| Option | Description |
|--------|-------------|
| `--model hog` or `--model cnn` | Detection model. Default is `hog`. |
| `--upsample N` | Number of upsampling passes. |
| `--cpus N` | Number of CPU cores to use. |

Output format: `filename,top,right,bottom,left`.

---

## Examples

The `examples/` directory contains runnable scripts. Install any extra dependencies they need (for example, `opencv-python` for webcam examples).

| Script | Purpose |
|--------|---------|
| `find_faces_in_picture.py` | Detect faces in a picture and print their locations. |
| `find_faces_in_picture_cnn.py` | Same as above using the CNN model. |
| `find_faces_in_batches.py` | Batch face detection with the CNN model on GPU. |
| `find_facial_features_in_picture.py` | Find and print facial landmarks. |
| `identify_and_draw_boxes_on_faces.py` | Recognize known people and draw labeled boxes. |
| `recognize_faces_in_pictures.py` | Recognize faces across a set of pictures. |
| `face_recognition_knn.py` | Face recognition using a k-nearest neighbors classifier. |
| `face_recognition_svm.py` | Face recognition using a support vector machine. |
| `facerec_from_webcam.py` | Real-time recognition from a webcam. |
| `facerec_from_webcam_faster.py` | Faster webcam recognition by processing every other frame. |
| `facerec_from_webcam_multiprocessing.py` | Webcam recognition using multiple processes. |
| `facerec_from_video_file.py` | Recognize faces in a video file and write annotated output. |
| `facerec_ipcamera_knn.py` | Recognition from an IP camera stream using KNN. |
| `facerec_on_raspberry_pi.py` | Recognition optimized for a Raspberry Pi. |
| `facerec_on_raspberry_pi_Simplified_Chinese.py` | Raspberry Pi example with Simplified Chinese comments. |
| `blink_detection.py` | Detect eye blinks using facial landmarks. |
| `blur_faces_on_webcam.py` | Blur detected faces in a live webcam feed. |
| `digital_makeup.py` | Apply digital makeup effects using landmarks. |
| `face_distance.py` | Demonstrate computing face distances. |
| `benchmark.py` | Measure performance of detection and encoding. |
| `track_faces_on_video_realtime.ipynb` | Jupyter notebook for real-time face tracking on video. |
| `web_service_example.py` | Expose face recognition through a simple web service. |
| `web_service_example_Simplified_Chinese.py` | Web service example with Simplified Chinese comments. |

**Example usage:**

```bash
cd examples
python find_faces_in_picture.py
python identify_and_draw_boxes_on_faces.py
python facerec_from_webcam.py
```

The directory also contains sample images (such as `obama.jpg`, `biden.jpg`, `two_people.jpg`, and `obama-1080p.jpg`) and videos (`hamilton_clip.mp4`, `short_hamilton_clip.mp4`) that the scripts use.

### Example: Blurring Faces

```python
import face_recognition
from PIL import Image, ImageFilter

image = face_recognition.load_image_file("two_people.jpg")
locations = face_recognition.face_locations(image)

pil_image = Image.fromarray(image)
for top, right, bottom, left in locations:
    region = pil_image.crop((left, top, right, bottom))
    blurred = region.filter(ImageFilter.GaussianBlur(20))
    pil_image.paste(blurred, (left, top, right, bottom))

pil_image.save("blurred.jpg")
```

---

## Tutorials and Recipes

- **Finding faces in pictures:** Start with `find_faces_in_picture.py`.
- **Recognizing a known person:** See the Quick Start above and `recognize_faces_in_pictures.py`.
- **Building a classifier:** `face_recognition_knn.py` and `face_recognition_svm.py` train a classifier on labeled encodings instead of comparing against each known face individually.
- **Real-time video:** Start with `facerec_from_webcam.py`, then try `facerec_from_webcam_faster.py` for better frame rates.
- **Web APIs:** `web_service_example.py` shows how to wrap recognition in an HTTP endpoint.

---

## Performance Tips

- **Scale down images.** Processing a smaller version of each frame is often the single biggest speedup. The webcam example resizes frames to a quarter of their original size.
- **Process every other frame** in video streams. Faces rarely change identity between consecutive frames.
- **Use the HOG model on CPU and the CNN model on GPU.** CNN detection on a CPU is very slow.
- **Use `batch_face_locations`** with the CNN model to exploit GPU parallelism.
- **Use `--cpus` with the CLI** to parallelize across cores.
- **Use multiprocessing** for webcam pipelines (`facerec_from_webcam_multiprocessing.py`) to separate capture from recognition.
- **Lower `num_jitters`** if encoding speed matters more than accuracy.
- **Avoid unnecessary upsampling.** Each upsample pass increases processing time significantly.

Run `benchmark.py` to measure performance on your hardware.

---

## Testing

Unit tests are in `face_recognition/test_face_recognition.py`.

Run them with the standard library:

```bash
python -m unittest discover -s face_recognition -p "test_*.py"
```

Or with pytest:

```bash
pip install pytest
pytest face_recognition/test_face_recognition.py
```

To run the full test matrix across Python versions, use tox:

```bash
pip install tox
tox
```

`tox.ini` defines environments for supported Python versions. The `Makefile` also provides shortcuts, so check it for available targets.

---

## Documentation

The Sphinx documentation lives in `docs/`. To build it locally:

```bash
pip install -r requirements_docs.txt
cd docs
make html        # On Windows: make.bat html
```

The generated HTML is placed in `docs/_build/html/`. Open `index.html` in a browser to view it.

The docs cover installation, usage, the API reference (`face_recognition.rst`, `modules.rst`), contributing guidelines, and the changelog (`history.rst`).

---

## Contributing

Contributions are welcome. A typical workflow is:

1. Fork the repository.
2. Create a feature branch: `git checkout -b my-feature`.
3. Install development dependencies: `pip install -r requirements_dev.txt`.
4. Make your changes and add tests where appropriate.
5. Run the test suite: `python -m unittest` or `tox`.
6. Commit and push your branch, then open a pull request.

See `CONTRIBUTING.rst` for the full guidelines, including coding style and how to report bugs.

---

## Troubleshooting

**`ERROR: Failed building wheel for dlib`**
Make sure CMake and a C++ compiler are installed and available on your `PATH`. On Windows, install the Visual Studio C++ build tools. On macOS, install Xcode command-line tools and CMake.

**`ImportError: libopenblas.so` or similar**
Install BLAS/LAPACK libraries, for example `sudo apt-get install libopenblas-dev liblapack-dev` on Debian-based systems.

**Very slow face detection**
You are probably using the CNN model on a CPU. Switch to `model="hog"`, or install dlib with CUDA support and use a GPU.

**Faces not detected in small or distant faces**
Increase `number_of_times_to_upsample`, though this will slow processing.

**Too many false matches**
Lower the `tolerance` value (for example, `0.5`). For too many missed matches, raise it slightly. Also ensure the known images show clear, front-facing faces.

**Webcam examples fail to open the camera**
Confirm that OpenCV can access the camera index (usually `0`) and that no other application is using it.

**Out of memory during dlib build on Raspberry Pi**
Increase swap space temporarily before running `pip install`.

---

## Authors

See [AUTHORS.rst](AUTHORS.rst) for the full list of contributors.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

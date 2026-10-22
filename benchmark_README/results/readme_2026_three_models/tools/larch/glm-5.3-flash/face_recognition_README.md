# face_recognition

**Face Recognition** — Recognize and manipulate faces from Python or from the command line with

> the world's simplest face recognition library.

Built using **dlib**'s state-of-the-art face recognition model, which achieves an accuracy of **99.38%** on the *Labeled Faces in the Wild* benchmark.

This project also provides a simple `face_recognition` command line tool that lets you do face recognition on a folder of images from the command line!

![Face Recognition](https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/obama_biden_face_recognition.jpg)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Use as a CLI Tool](#use-as-a-cli-tool)
- [Use in Python](#use-in-python)
  - [Find faces in a picture](#find-faces-in-a-picture)
  - [Locate facial features in a picture](#locate-facial-features-in-a-picture)
  - [Identify faces in pictures](#identify-faces-in-pictures)
- [Face Recognition API Reference](#face-recognition-api-reference)
- [Automatically Blur Faces in Images or Videos](#automatically-blur-faces-in-images-or-videos)
- [Python Code Examples](#python-code-examples)
- [Deployment / Docker](#deployment--docker)
- [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
- [Thanks](#thanks)
- [License](#license)

---

## Features

Find faces in pictures:

![Find faces](https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/find_faces_in_picture.jpg)

Find and manipulate facial features in pictures:

![Facial features](https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/find_facial_features.jpg)

Identify who appears in each photo:

![Identify faces](https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/obama_biden_face_recognition.jpg)

You can even use this library with other Python libraries to do real-time face recognition — see this example:

![Real-time webcam recognition](https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/facerec_from_webcam_faster_demo.gif)

---

## Installation

### Requirements

* Python 3.3+ or Python 2.7
* macOS or Linux (Windows is *not* officially supported, but might work)
* The `dlib` library (installed automatically as a dependency)

### Installing on macOS or Linux

First, make sure you have `dlib` with Python bindings installed. Then simply:

```bash
pip3 install face_recognition
```

If you don't already have `dlib` installed, it will be compiled from source — this requires **CMake** and a working C++ compiler:

```bash
# On macOS
brew install cmake

# On Ubuntu/Debian
sudo apt-get install cmake build-essential
```

Then install:

```bash
pip3 install face_recognition
```

> 💡 **Tip:** Compiling `dlib` from source can take a while. If you're having trouble installing, follow the detailed instructions below or check the [Troubleshooting](#common-issues-and-troubleshooting) section.

### Installing on a Raspberry Pi

The `face_recognition` library works great on a Raspberry Pi! See the `facerec_on_raspberry_pi.py` example for a working demo.

### Installing pre-configured Docker images

Docker images with `face_recognition` and its dependencies are pre-configured for you:

```bash
# CPU-only image
docker build -f Dockerfile -t facerecognition .

# GPU image (requires nvidia-docker)
docker build -f Dockerfile.gpu -t facerecognition-gpu .
```

There is also a simplified Python example Dockerfile in `Dockerfile-python-example`.

---

## Use as a CLI Tool

Once installed, you can use the `face_recognition` command directly from your terminal.

### Show faces found in an image

```bash
face_recognition --show-models --show-faces obama.jpg
```

### Compare faces in two images

Find out if the same person appears in two pictures:

```bash
$ face_recognition obama.jpg obama2.jpg

# Output:
obama.jpg,obama2.jpg,0.32321
```

A distance of **0.36 or less** generally means the pictures are of the same person. Values closer to 0 mean a better match.

### Recognize faces in a folder of images

Given a folder of known people (`people/`) and a folder of unknown images (`unknown_pics/`), identify everyone:

```bash
$ face_recognition people/ unknown_pics/

# Output:
obama,unknown_pics/obama-1080p.jpg
biden,unknown_pics/biden2.jpg
unknown_person,unknown_pics/johnsnow_test1.jpg
```

Results are printed as CSV: `person_name,image_filename` (run with `--tolerance` to adjust the match strictness).

For full CLI usage:

```bash
face_recognition --help
```

---

## Use in Python

You can also import and use the `face_recognition` Python module.

### Find faces in a picture

```python
import face_recognition

image = face_recognition.load_image_file("obama.jpg")

# Find all the faces in the image using a pretrained HOG model.
face_locations = face_recognition.face_locations(image)
```

**See the full example:** [`find_faces_in_picture.py`](examples/find_faces_in_picture.py)

To use a CNN (deep-learning based) face detector for more accurate results (requires GPU for speed):

```python
face_locations = face_recognition.face_locations(image, model="cnn")
```

**See:** [`find_faces_in_picture_cnn.py`](examples/find_faces_in_picture_cnn.py)

### Locate facial features in a picture

Find important parts of faces — eyes, nose, mouth, chin, etc.:

```python
import face_recognition

image = face_recognition.load_image_file("obama.jpg")

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)
```

**See the full example:** [`find_facial_features_in_picture.py`](examples/find_facial_features_in_picture.py)

You can even apply "digital makeup" using the landmark points:

```python
# See digital_makeup.py for the full example
```

**See:** [`digital_makeup.py`](examples/digital_makeup.py)

### Identify faces in pictures

Recognize who is in each photo:

```python
import face_recognition

# Load images
obama_image = face_recognition.load_image_file("obama.jpg")
biden_image = face_recognition.load_image_file("biden.jpg")
unknown_image = face_recognition.load_image_file("obama_and_biden.jpg")

# Get 128-dimension face encodings for each person
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

known_faces = [
    obama_face_encoding,
    biden_face_encoding
]

# Compare the unknown face against the known faces
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

print("Is the unknown face Obama? {}".format(results[0]))
print("Is the unknown face Biden? {}".format(results[1]))
print("Is the unknown face a new person? {}".format(not True in results))
```

**See the full example:** [`recognize_faces_in_pictures.py`](examples/recognize_faces_in_pictures.py)

---

## Face Recognition API Reference

After installing, you can view the full API documentation with:

```bash
pydoc face_recognition
```

or build the Sphinx docs from the `docs/` directory:

```bash
cd docs
make html
```

### Main API functions

| Function | Description |
|---|---|
| `face_recognition.api.load_image_file(file, mode='RGB')` | Load an image file into a numpy array |
| `face_recognition.api.face_locations(img, number_of_times_to_upsample=0, model='hog')` | Find all faces in an image. Models: `hog` (fast, CPU) or `cnn` (accurate, GPU) |
| `face_recognition.api.face_encodings(face_image, known_face_locations=None, num_jitters=1)` | Return 128-dimensional face encodings of all faces in an image |
| `face_recognition.api.compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)` | Compare a face encoding against a list of known encodings. Returns list of `True`/`False` |
| `face_recognition.api.face_distance(face_encodings, face_to_compare)` | Compute the euclidean distance between face encodings — lower is more similar |
| `face_recognition.api.face_landmarks(face_image, face_locations=None)` | Return a dictionary of facial feature locations (eyes, nose, mouth, etc.) |
| `face_recognition.api.batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)` | Find faces in a batch of images using the CNN model (GPU recommended) |

### Key parameters

* **`model`** — `"hog"` (default) is fast but less accurate; `"cnn"` is a deep-learning model that is more accurate and works well on GPUs.
* **`tolerance`** — How much distance between faces to consider them a match. Lower is stricter. `0.6` is a good default.
* **`num_jitters`** — How many times to re-sample the face when computing encodings. Higher values are slower but more accurate.

### A note on face matching accuracy

The face recognition model gives you a *distance* between face encodings. This is how the comparison works:

* **Distance < 0.6** → probably the same person
* **Distance > 0.6** → probably different people

Use the `face_distance` function directly if you want to build custom matching logic (e.g., picking the *closest* match instead of just the first match). See [`face_distance.py`](examples/face_distance.py) for an example.

For even more accuracy, see the K-Nearest Neighbors classifier example in [`face_recognition_knn.py`](examples/face_recognition_knn.py) and the SVM classifier in [`face_recognition_svm.py`](examples/face_recognition_svm.py).

---

## Automatically Blur Faces in Images or Videos

If you need to anonymize faces in photos or videos (for privacy reasons), see the [`blur_faces_on_webcam.py`](examples/blur_faces_on_webcam.py) example which shows how to automatically detect and blur faces in real time from a webcam.

---

## Python Code Examples

All example code is in the [`examples/`](examples/) folder. To run any of them, you need `OpenCV` installed for the video examples:

```bash
pip3 install opencv-python
```

| Example | Description |
|---|---|
| `find_faces_in_picture.py` | Find faces in a picture using the default HOG model |
| `find_faces_in_picture_cnn.py` | Find faces in a picture using the deep-learning CNN model |
| `find_faces_in_batches.py` | Find faces in multiple images at once using a GPU |
| `find_facial_features_in_picture.py` | Locate eyes, nose, mouth, chin and other facial features |
| `identify_and_draw_boxes_on_faces.py` | Detect faces and draw boxes around them with names |
| `digital_makeup.py` | Apply "digital makeup" using facial landmarks |
| `recognize_faces_in_pictures.py` | Identify who is in each photo |
| `face_recognition_knn.py` | Use a K-Nearest Neighbors classifier for improved accuracy |
| `face_recognition_svm.py` | Use an SVM classifier for recognition |
| `face_distance.py` | Compare face encodings numerically |
| `benchmark.py` | Benchmark detection speed on your hardware |
| `facerec_from_webcam.py` | Real-time face recognition from your webcam |
| `facerec_from_webcam_faster.py` | Faster, optimized real-time webcam recognition |
| `facerec_from_webcam_multiprocessing.py` | Multi-process webcam recognition |
| `blink_detection.py` | Detect eye blinks using facial landmarks |
| `facerec_from_video_file.py` | Recognize faces in a video file |
| `blur_faces_on_webcam.py` | Automatically blur faces from a live webcam |
| `facerec_ipcamera_knn.py` | Face recognition from an IP camera stream |
| `facerec_on_raspberry_pi.py` | Run face recognition on a Raspberry Pi |
| `web_service_example.py` | Wrap the API in a simple Flask web service |
| `web_service_example_Simplified_Chinese.py` | Flask web service example (Simplified Chinese) |

The `hamilton_clip.mp4` and `short_hamilton_clip.mp4` video files and associated Jupyter notebooks (like `track_faces_on_video_realtime.ipynb`) can be used to test real-time face tracking on video.

---

## Deployment / Docker

Several `Dockerfile`s are included to make deployment easy:

* **`Dockerfile`** — standard CPU-based deployment image
* **`Dockerfile.gpu`** — GPU-accelerated image using `nvidia-docker`
* **`Dockerfile-python-example`** — minimal Python example

A `docker-compose.yml` is also provided for running multi-service deployments.

---

## Common Issues and Troubleshooting

### `ImportError: No module named 'face_recognition'`

Make sure the library was installed for the Python version you are using (`pip3` vs `pip`).

### `AttributeError: 'module' object has no attribute 'face_recognition_model_v1'` or dlib errors

This usually means you have a very old version of `dlib`. Upgrade it:

```bash
pip3 install --upgrade dlib
```

### Installation fails when compiling dlib

Compiling `dlib` requires **CMake** and a C++ compiler:

```bash
# macOS
brew install cmake

# Ubuntu / Debian
sudo apt-get install build-essential cmake

# Fedora
sudo dnf install cmake
```

Then retry `pip3 install face_recognition`.

### Face detection is slow

* The default `hog` model is CPU-based and reasonably fast.
* The `cnn` model is much more accurate, but is only fast on a CUDA-enabled GPU.
* For real-time webcam performance, see `facerec_from_webcam_faster.py` which uses various optimization tricks.
* Reduce image resolution before processing (e.g., use `obama-240p.jpg` instead of `obama-1080p.jpg`) — detection time scales with image size.

### Partial faces are not detected

Faces that are partially cut off in an image may not be detected. Try increasing `number_of_times_to_upsample` when calling `face_locations()`.

### Low accuracy

* Use higher-resolution images.
* Increase `num_jitters` when calling `face_encodings()`.
* Use the CNN model for face detection.
* Tune the `tolerance` parameter — lower it if you get false positives, raise it if you get false negatives.

---

## Thanks

* **[dlib](https://github.com/davisking/dlib)** — This project would not be possible without Davis King's incredible dlib library, including its deep metric learning face recognition model.
* **[Openface](https://cmusatyalab.github.io/openface/)** — An open source face recognition project that inspired this one and provided documentation on the face recognition model used.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Free, forever, for commercial or personal use. 🎉

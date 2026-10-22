# face_recognition

A Python library for detecting and recognizing faces in images and video. It wraps [dlib](http://dlib.net/)’s state-of-the-art face-recognition model in a simple API, so you can locate faces, turn them into numeric encodings, and compare those encodings to identify likely matches.

> **Important:** Face recognition is probabilistic. A match is not proof of identity. Choose an appropriate threshold for your use case, and use additional safeguards for decisions that affect people.

## Features

- Find faces in images using a HOG-based CPU detector or a CNN-based detector.
- Generate 128-dimensional face encodings.
- Compare faces and calculate the distance between encodings.
- Locate facial landmarks, including eyes, nose, eyebrows, and lips.
- Use command-line tools to recognize faces or report face locations.
- Explore examples for image, webcam, video, batch, and web-service workflows.

## Installation

Install the package from PyPI:

```bash
pip install face_recognition
```

The package depends on [dlib](http://dlib.net/). Installing dlib may require a C++ compiler and CMake; consult the [dlib installation instructions](http://dlib.net/). If installation fails, install the required system build tools for your operating system and try again.

For example, on many Debian- or Ubuntu-based systems:

```bash
sudo apt-get update
sudo apt-get install build-essential cmake
pip install face_recognition
```

The CNN face detector can take advantage of CUDA-enabled GPUs when dlib is built with CUDA support. The HOG detector works on a CPU and is a good starting point.

### Docker

The repository includes Dockerfiles and a `docker-compose.yml` for container-based workflows. See those files for the available image configurations.

## Quick start

```python
import face_recognition

# Load images as RGB arrays.
known_image = face_recognition.load_image_file("obama.jpg")
unknown_image = face_recognition.load_image_file("biden.jpg")

# Generate an encoding for each image.
known_encodings = face_recognition.face_encodings(known_image)
unknown_encodings = face_recognition.face_encodings(unknown_image)

if not known_encodings:
    raise ValueError("No face found in obama.jpg")
if not unknown_encodings:
    raise ValueError("No face found in biden.jpg")

# Compare the first face in each image.
matches = face_recognition.compare_faces(
    known_encodings,
    unknown_encodings[0],
)
print(matches)
```

`compare_faces` returns one Boolean for each known encoding. In this example, `matches[0]` indicates whether the two faces are considered a match at the default tolerance.

## Recognize faces in an image

Use `face_recognition` to compare faces in one or more images against a directory of known people.

Organize known images so each filename identifies the person:

```text
known_people/
├── alice.jpg
├── bob.jpg
└── bob_at_work.png
```

Then run:

```bash
face_recognition known_people/ pictures_to_check/
```

The command prints the image being checked and the name of each recognized person. When a face does not match a known encoding, it is reported as `unknown`.

The command-line tool also supports options for adjusting the recognition tolerance, detector model, and CPU usage. Run it with `--help` to see the options available in your installation:

```bash
face_recognition --help
```

## Find faces and draw boxes

A typical image workflow is to locate faces, then use the returned coordinates to draw boxes or crop the image:

```python
import face_recognition
from PIL import Image, ImageDraw

image = face_recognition.load_image_file("obama.jpg")
locations = face_recognition.face_locations(image)

pil_image = Image.fromarray(image)
draw = ImageDraw.Draw(pil_image)

for top, right, bottom, left in locations:
    draw.rectangle(
        (left, top, right, bottom),
        outline="red",
        width=3,
    )

del draw
pil_image.save("faces_found.jpg")
```

`face_locations` returns a list of `(top, right, bottom, left)` tuples, in pixels. These coordinates can also be used to crop a face from the original image:

```python
top, right, bottom, left = locations[0]
face_crop = image[top:bottom, left:right]
```

## Find facial landmarks

Use `face_landmarks` to find points describing facial features:

```python
import face_recognition

image = face_recognition.load_image_file("obama.jpg")
landmarks = face_recognition.face_landmarks(image)

for face in landmarks:
    print(face["left_eye"])
    print(face["nose_tip"])
```

Each face is represented as a dictionary of feature names and point coordinates. The default `"large"` landmark model returns detailed features; the `"small"` model returns a reduced set.

## Use face encodings directly

Face encodings are numeric representations of faces. You can save encodings and compare them later:

```python
import face_recognition

image = face_recognition.load_image_file("obama.jpg")
encodings = face_recognition.face_encodings(image)

if encodings:
    encoding = encodings[0]
    print(encoding.shape)  # (128,)
```

Compare an unknown encoding with a collection of known encodings:

```python
import face_recognition

# known_encodings is a list of 128-dimensional face encodings.
# unknown_encoding is one 128-dimensional face encoding.
distances = face_recognition.face_distance(
    known_encodings,
    unknown_encoding,
)

best_match_index = distances.argmin()
print("Closest distance:", distances[best_match_index])
```

A smaller distance means the encodings are more similar. You can set the matching threshold yourself:

```python
tolerance = 0.50
is_match = distances[best_match_index] <= tolerance
```

The default tolerance used by `compare_faces` is `0.6`. Lower values require a closer match and generally reduce false matches, but may also cause genuine matches to be missed. Test and tune the threshold on data representative of your application.

## Python API

The main functions are:

| Function | Description |
| --- | --- |
| `load_image_file(file, mode="RGB")` | Load an image file as a NumPy array. |
| `face_locations(img, number_of_times_to_upsample=1, model="hog")` | Return face bounding boxes. Use `"hog"` for CPU detection or `"cnn"` for the CNN detector. |
| `batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)` | Find faces in a batch of images; most useful with a CUDA-enabled CNN detector. |
| `face_landmarks(face_image, face_locations=None, model="large")` | Return facial feature landmarks. |
| `face_encodings(face_image, known_face_locations=None, num_jitters=1, model="small")` | Return 128-dimensional encodings for detected faces. |
| `compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)` | Compare one encoding against known encodings and return match results. |
| `face_distance(face_encodings, face_to_compare)` | Return distances between an encoding and a collection of encodings. |

If no face is found, the location, landmark, and encoding functions return empty lists. Check their results before indexing into them.

## Command-line tools

The package installs two command-line programs:

### `face_recognition`

Compare faces in images against a directory of known people:

```bash
face_recognition <known_people_directory> <images_to_check>
```

Use `face_recognition --help` for available options.

### `face_detection`

Print face locations for an image or images:

```bash
face_detection <image_file>
```

Use `face_detection --help` for available options.

## Examples in this repository

The repository includes scripts and notebooks showing different ways to use the library:

- `find_faces_in_picture.py` — locate faces in an image.
- `identify_and_draw_boxes_on_faces.py` — identify faces and draw boxes around them.
- `find_facial_features_in_picture.py` — find facial landmarks.
- `recognize_faces_in_pictures.py` — recognize known people in pictures.
- `face_distance.py` — compare face encodings using distances.
- `find_faces_in_batches.py` — process images in batches.
- `face_recognition_knn.py` and `face_recognition_svm.py` — recognition examples using classifiers.
- `facerec_from_webcam.py`, `facerec_from_webcam_faster.py`, and `facerec_from_webcam_multiprocessing.py` — webcam examples.
- `facerec_from_video_file.py` and `track_faces_on_video_realtime.ipynb` — video examples.
- `blur_faces_on_webcam.py` and `digital_makeup.py` — examples of effects using face locations and landmarks.
- `web_service_example.py` — a web-service example.

Some webcam, video, and image-processing examples require additional packages such as OpenCV. Install the dependencies required by the specific example before running it.

## Performance and detector choice

The default HOG detector is CPU-friendly and suitable for many images. The CNN detector can be more accurate in some situations, but is typically slower without a CUDA-enabled GPU.

```python
locations = face_recognition.face_locations(image, model="cnn")
```

For small faces, try increasing the number of times the image is upsampled:

```python
locations = face_recognition.face_locations(
    image,
    number_of_times_to_upsample=2,
)
```

Upsampling can improve detection of small faces, but increases processing time.

## Development and tests

The repository includes test and development configuration, including `test_face_recognition.py`, `tox.ini`, and `requirements_dev.txt`. To set up a development environment, install the development requirements and run the test suite with your preferred test runner.

Documentation-related dependencies are listed in `requirements_docs.txt`.

## Limitations and responsible use

- Results depend on image quality, face size, lighting, pose, and other conditions.
- Encodings and similarity thresholds do not establish a person’s identity with certainty.
- Detection and recognition performance can vary across demographic groups and image conditions.
- Store face images and encodings securely, and obtain appropriate consent before collecting or processing biometric data.
- Do not use this library as the sole basis for consequential decisions.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE) for the full license text.

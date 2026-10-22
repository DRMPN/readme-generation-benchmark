# EmotiEffLib

EmotiEffLib is a library for facial emotion recognition, facial attribute analysis, and engagement estimation from face images and video. It provides pretrained lightweight CNN and transformer models that run on PyTorch, ONNX Runtime, and TensorFlow Lite. The repository also includes C++ and Android bindings, a Flask-style server example, a Python video pipeline, and the notebooks used to train and evaluate the models.

> **Note:** This README was written from the repository's file listing. Where it describes APIs, command-line options, or folder contents, it reflects the typical layout of the EmotiEffLib project. Check the code and the per-folder READMEs for exact signatures before relying on them.

---

## Table of Contents

1. [Features](#features)
2. [Repository Structure](#repository-structure)
3. [Pretrained Models](#pretrained-models)
4. [Installation](#installation)
5. [Quick Start (Python)](#quick-start-python)
6. [Inference Engines](#inference-engines)
7. [Emotion and Attribute Recognition on Video](#emotion-and-attribute-recognition-on-video)
8. [Engagement Estimation](#engagement-estimation)
9. [C++ Library](#c-library)
10. [Android Application](#android-application)
11. [Server Example](#server-example)
12. [Model Conversion](#model-conversion)
13. [Training and Experiments](#training-and-experiments)
14. [Testing](#testing)
15. [Documentation](#documentation)
16. [Citation](#citation)
17. [License](#license)

---

## Features

- **Facial expression recognition (FER)** into the standard categories (for example, AffectNet-style labels such as anger, disgust, fear, happiness, neutral, sadness, surprise, plus contempt where supported).
- **Valence–arousal (VA) regression** and multi-task models that jointly predict emotions and continuous affect.
- **Engagement estimation** from face features, with a user-independent model and a user-adaptation pipeline.
- **Multiple inference backends**: PyTorch, ONNX Runtime, and TensorFlow Lite.
- **Face detection and alignment** via MTCNN (TensorFlow protobuf and TFLite versions).
- **Age, gender, and ethnicity estimation** using a TensorFlow/Keras model.
- **Video processing** with frame-level prediction, temporal smoothing, and summary visualization.
- **Cross-platform deployment**: Python package, C++ library with CMake, and an Android app with PyTorch Lite and TFLite classifiers.
- **Reproducible training** through Jupyter notebooks for AffectNet, AFEW, VGAF, ABAW challenge tasks, RAMAS, and more.

---

## Repository Structure

The repository is organized into several main components. Folder names are inferred from the file listing.

| Component | Purpose |
|---|---|
| **Python package** (`emotiefflib/`, with `setup.py` and `pyproject.toml`) | Core library: `facial_analysis.py`, `mobilefacenet.py`, `engagement_classification_model.py`, `utils.py`, and related modules. |
| **Pretrained weights** (`*.pt`, `*.onnx`, `*.h5`, `*.pb`) | Models for PyTorch, ONNX, Keras, and TensorFlow. |
| **Engagement** (`engagement_single_attention.h5`, `engagement_single_attention_converter.py`, `requirements-engagement.txt`) | Engagement model and converter script. |
| **Binder / notebooks** (`requirements-binder*.txt`, `*.ipynb`) | Interactive demos runnable on Binder: image emotion recognition, video emotion prediction, and engagement prediction. |
| **Tests** (`test_facial_analysis.py`, `test_module_loading.py`, `check_installed_libs.sh`, `download_test_data.sh`) | Python test suite and environment checks. |
| **C++ library** (`facial_analysis.h`, `facial_analysis.cpp`, `CMakeLists.txt`, `Doxyfile*`) | Native implementation, C++ tests, and Doxygen documentation config. |
| **Android app** (`build.gradle`, `AndroidManifest.xml`, `MainActivity.java`, `MTCNN.java`, `EmotionPyTorchClassifier.java`, `EmotionTfLiteClassifier.java`, `AgeGenderEthnicityTfLiteClassifier.java`, and so on) | Mobile app with on-device face detection and emotion classification. Includes `.ptl` and `.tflite` models. |
| **Server** (`server.py`, `ServerProcessor.java`) | Example server that processes frames sent from a client. |
| **Model conversion** (`prepare_models_for_emotieffcpplib.py`, `convert_pt_to_onnx.py`, `to_pytorchlite.py`, `to_tflite.py`) | Scripts that convert PyTorch models to ONNX, TorchScript Lite, and TFLite. |
| **Training and experiments** (`*.ipynb`, `robust_optimization.py`, `generate_exp_preproc_results.py`) | Notebooks and scripts for training, evaluation, and result generation. |
| **Video tools** (`recognize_emotions_video.py`, `video_summarizer.ipynb`, `display_emotions.ipynb`) | Command-line and notebook tools for video analysis. |
| **Sample data** (`20180720_174416.jpg`, `download_test_data.sh`) | Sample image and script to download test datasets. |

---

## Pretrained Models

### Emotion recognition (PyTorch, ONNX)

| Model name | Backbone | Training data / task | Formats |
|---|---|---|---|
| `enet_b0_8_best_afew` | EfficientNet-B0 | AFEW (emotion) | `.pt`, `.onnx` |
| `enet_b0_8_best_vgaf` | EfficientNet-B0 | VGAF (emotion) | `.pt`, `.onnx` |
| `enet_b0_8_va_mtl` | EfficientNet-B0 | Multi-task: emotion + valence/arousal | `.pt`, `.onnx`, `.ptl` (mobile) |
| `enet_b2_7` | EfficientNet-B2 | AffectNet, 7 classes | `.pt`, `.onnx` |
| `enet_b2_8` | EfficientNet-B2 | AffectNet, 8 classes | `.pt`, `.onnx` |
| `mbf_va_mtl` | MobileFaceNet | Multi-task: emotion + valence/arousal | `.pt`, `.onnx` |
| `mobilevit_va_mtl` | MobileViT | Multi-task: emotion + valence/arousal | `.pt`, `.onnx` |

### Engagement

| File | Description |
|---|---|
| `engagement_single_attention.h5` | Keras model for engagement classification with a single attention block. |

### Face analysis and detection

| File | Description |
|---|---|
| `mtcnn.pb`, `mtcnn_model.pb` | MTCNN face detector (TensorFlow protobuf). |
| `pnet.tflite`, `rnet.tflite`, `onet.tflite` | MTCNN stages in TFLite format for mobile use. |
| `state_vggface2_enet0_new.pt`, `state_vggface2_enet2.pt`, `state_vggface2_rexnet_150.pt` | Face recognition backbones (VGGFace2-trained) used as feature extractors. |
| `mobilenet_7.h5` | MobileNet-based emotion model in Keras format. |
| `age_gender_tf2_224_deep-03-0.13-0.97.h5`, `age_gender_ethnicity_224_deep-03-0.13-0.97-0.88.pb` | Age, gender, and ethnicity models (Keras and TensorFlow protobuf). |

### Labels

- `affectnet_labels.txt` lists the emotion class names used by the Android app and the models.

---

## Installation

### Requirements

- Python 3.8 or newer (check `setup.py` or `pyproject.toml` for the exact minimum)
- pip
- Optional: CUDA-capable GPU for PyTorch inference or training
- For C++: CMake 3.x and a C++17 compiler
- For Android: Android Studio and an SDK matching `build.gradle`

### Install the Python package

From the repository root:

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

### Optional requirement sets

| File | Use case |
|---|---|
| `requirements.txt` | Core runtime dependencies. |
| `requirements-torch.txt` | PyTorch-based inference and training. |
| `requirements-engagement.txt` | Engagement model dependencies (TensorFlow/Keras). |
| `requirements-binder.txt`, `requirements-binder-torch.txt` | Binder environment for the demo notebooks. |
| `requirements-ci.txt` | Continuous integration. |
| `setup.cfg`, `pyproject.toml` | Packaging metadata. |

### Verify the environment

```bash
bash check_installed_libs.sh
```

This script checks that the required libraries are installed and importable.

---

## Quick Start (Python)

The examples below show the typical usage pattern. Confirm names against the code in `facial_analysis.py`.

### Recognize emotions in an image

```python
import cv2
from emotiefflib.facial_analysis import EmotiEffLibRecognizer, get_model_list

print(get_model_list())  # list available model names

img = cv2.cvtColor(cv2.imread("20180720_174416.jpg"), cv2.COLOR_BGR2RGB)

fer = EmotiEffLibRecognizer(
    engine="onnx",                 # "torch" or "onnx" (or "tflite" where supported)
    model_name="enet_b0_8_best_vgaf",
    device="cpu",
)

# Face bounding boxes (x, y, w, h) from a detector, or a pre-cropped face
faces = [...]

for face in faces:
    emotion, scores = fer.predict_emotions(face, logits=True)
    print(emotion, scores)
```

### Predict valence and arousal with a multi-task model

```python
fer = EmotiEffLibRecognizer(engine="torch", model_name="mbf_va_mtl", device="cpu")
emotion, scores = fer.predict_emotions(face, logits=True)
```

### Run the bundled example notebooks

Launch Jupyter and open one of the demos:

- `One image emotion recognition.ipynb`
- `Predict emotions on video.ipynb`
- `Predict engagement and emotions on video.ipynb`

---

## Inference Engines

EmotiEffLib supports three backends. Choose based on deployment needs.

| Engine | Best for | Notes |
|---|---|---|
| **PyTorch** (`.pt`) | Research, training, GPU inference | Full flexibility; largest dependency footprint. |
| **ONNX Runtime** (`.onnx`) | Production servers, CPU speed, portability | Good default for CPU inference. |
| **TensorFlow Lite** (`.tflite`) | Mobile and embedded devices | Used in the Android app and MTCNN stages. |
| **TorchScript Lite** (`.ptl`) | Android PyTorch Mobile | Used by `EmotionPyTorchClassifier.java`. |

To convert models between formats, see [Model Conversion](#model-conversion).

---

## Emotion and Attribute Recognition on Video

### Command line

```bash
python recognize_emotions_video.py --input input.mp4 --output output.mp4 \
    --model enet_b0_8_va_mtl --engine onnx
```

Check `python recognize_emotions_video.py --help` for the exact arguments. Typical options include the input and output paths, model name, inference engine, and frame sampling rate.

### Notebooks

- `Predict emotions on video.ipynb`: frame-by-frame emotion prediction with overlays.
- `display_emotions.ipynb`: visualization of emotion timelines.
- `video_summarizer.ipynb`: selects key frames and summarizes a video.

---

## Engagement Estimation

Engagement estimation uses face features extracted by the emotion models and a classifier trained on engagement labels.

### Pipeline

1. **Feature extraction**: `01 - Features-extractor.ipynb` extracts per-frame features.
2. **User-independent training**: `02 - Engagement user-independent model training.ipynb` trains a general model.
3. **Custom dataset features**: `03 - Custom dataset features extractor.ipynb` processes your own data.
4. **User adaptation**: `04 - Engagement user-adaptation.ipynb` fine-tunes the model for a specific user.

### Inference

Install the engagement requirements and use `engagement_classification_model.py`, or open `Predict engagement and emotions on video.ipynb`.

### Converting the engagement model

```bash
python engagement_single_attention_converter.py
```

This converts `engagement_single_attention.h5` to another format if needed.

---

## C++ Library

The C++ implementation lives alongside the Python package and exposes the same core functionality through `facial_analysis.h` and `facial_analysis.cpp`.

### Build

```bash
mkdir build && cd build
cmake ..
cmake --build . --config Release
```

### Run tests

The C++ test suite includes `tests_facial_analisys.cpp`, `tests_internal_methods.cpp`, and helper utilities in `test_utils.h` and `test_utils.cpp`. After building, run the test executable generated by CMake, for example:

```bash
./build/tests_facial_analysis
```

### Generate documentation

Doxygen configuration files are provided for both C++ and Python:

```bash
doxygen Doxyfile-cpp
doxygen Doxyfile-python
```

### Preprocessing parity check

`generate_exp_preproc_results.py` generates preprocessing outputs so the C++ implementation can be checked against Python results.

---

## Android Application

The Android app performs face detection and emotion classification on device.

### Components

- `MainActivity.java`: camera UI and main flow.
- `MTCNN.java`, `Box.java`, `Align.java`: face detection and alignment.
- `EmotionPyTorchClassifier.java`: runs `enet_b0_8_va_mtl.ptl` with PyTorch Mobile.
- `EmotionTfLiteClassifier.java`, `TfLiteClassifier.java`: TFLite-based classification.
- `AgeGenderEthnicityTfLiteClassifier.java`: demographic estimation.
- `ServerProcessor.java`: sends frames to a remote server when configured.
- `Utils.java`, `EmotionData.java`, `FaceData.java`, `ClassifierResult.java`: helpers and data models.

### Build and run

1. Open the Android project in Android Studio.
2. Let Gradle sync using `build.gradle`, `settings.gradle`, and `gradle.properties`.
3. Connect a device or start an emulator with a camera.
4. Build and run the app.

Model files (`.ptl`, `.tflite`, `.pb`, `affectnet_labels.txt`) are bundled under the app's assets.

---

## Server Example

`server.py` implements a server that receives frames (for example, from the Android app via `ServerProcessor.java`), runs emotion recognition, and returns results.

```bash
python server.py
```

Check the file for the host, port, and model settings. Ensure the required Python dependencies are installed first.

---

## Model Conversion

| Script | Purpose |
|---|---|
| `prepare_models_for_emotieffcpplib.py` | Prepares PyTorch models for the C++ library (exports weights and ONNX models). |
| `convert_pt_to_onnx.py` | Converts a PyTorch `.pt` model to `.onnx`. |
| `to_pytorchlite.py` | Converts a PyTorch model to TorchScript Lite (`.ptl`) for Android. |
| `to_tflite.py` | Converts a model to TensorFlow Lite (`.tflite`). |
| `engagement_single_attention_converter.py` | Converts the engagement Keras model. |

Example:

```bash
python convert_pt_to_onnx.py --help
```

---

## Training and Experiments

The `*.ipynb` notebooks reproduce the training and evaluation experiments. They cover:

| Notebook group | Topic |
|---|---|
| `train_affectnet_march2021_pytorch.ipynb`, `evaluate_affectnet_march2021_pytorch.ipynb` | AffectNet training and evaluation (PyTorch). |
| `train_emotions.ipynb`, `train_emotions-pytorch.ipynb`, `train_emotions-pytorch-afew-vgaf.ipynb` | Emotion model training on several datasets. |
| `AFEW_train.ipynb`, `VGAF_train.ipynb` | Training on AFEW and VGAF. |
| `abaw3_train.ipynb` through `abaw8_expr.ipynb`, `abaw4_mtl_train.ipynb`, `abaw5_expr_va_au_train.ipynb`, `abaw6_affwild2.ipynb` | Experiments for the ABAW (Affective Behavior Analysis in-the-wild) challenges: expression, valence–arousal, action units, and multi-task learning. |
| `emi.ipynb`, `bah.ipynb`, `mtl.ipynb`, `cexpr.ipynb`, `eri.ipynb` | Additional experiments for EMI, BAH, MTL, C-EXPR, and ERI tasks. |
| `train_ramas.ipynb`, `abaw4_lsd_train.ipynb` | RAMAS and LSD experiments. |
| `emotions_experiments.ipynb` | Comparative emotion experiments. |
| `robust_optimization.py` | Robust optimization utilities for training. |
| `train_faces_torch.ipynb` | Face model training in PyTorch. |

Most notebooks expect datasets to be downloaded and placed in paths set at the top of each notebook. Dataset licenses and access terms apply and must be followed.

---

## Testing

### Python tests

```bash
pytest test_facial_analysis.py test_module_loading.py
```

- `test_facial_analysis.py` checks inference output shapes and label handling.
- `test_module_loading.py` checks that the package and its modules import correctly.

### Sample data

Download test data with:

```bash
bash download_test_data.sh
```

### C++ tests

Build with CMake and run the generated test binaries (see [C++ Library](#c-library)).

### Continuous integration

`requirements-ci.txt` lists CI dependencies. Use it to set up a CI environment that runs the Python and C++ tests.

---

## Documentation

- **API reference**: generate with Doxygen using `Doxyfile-cpp` (C++) and `Doxyfile-python` (Python). Layouts are in `DoxygenLayout*.xml`.
- **Per-folder READMEs**: several subfolders include their own README files with specific instructions (for example, the Android app, the engagement pipeline, and the notebook collections).

---

## Citation

If you use EmotiEffLib in your research, please cite the associated papers by the author, Andrey V. Savchenko. Two commonly referenced works are:

```bibtex
@inproceedings{savchenko2021facial,
  title     = {Facial expression recognition with adaptive frame rate based on multiple testing},
  author    = {Savchenko, Andrey V.},
  booktitle = {Neural Networks},
  year      = {2022}
}

@article{savchenko2021emotieffnet,
  title   = {Efficient facial representations for age, gender and identity recognition in organizing photo albums using multi-output CNN},
  author  = {Savchenko, Andrey V.},
  journal = {arXiv preprint},
  year    = {2021}
}
```

Please verify the exact citation details against the project's published references before using them in a paper.

---

## License

This project is distributed under the terms in the [LICENSE](LICENSE) file. Pretrained models and third-party datasets may carry separate licenses or usage restrictions. Check those before commercial use.

---

## Acknowledgements

EmotiEffLib builds on open-source work including PyTorch, ONNX Runtime, TensorFlow, TensorFlow Lite, OpenCV, and MTCNN. Datasets referenced by the notebooks (AffectNet, AFEW, VGAF, Aff-Wild2, and others) belong to their respective owners.

# README

# EmotiEffLib — Emotion & Engagement Recognition Library

**EmotiEffLib** is a cross-platform (**Python / C++ / Android**) library and model zoo for **real-time facial emotion recognition**, **valence–arousal estimation**, and **engagement (attentiveness) detection** from face images and video. It consolidates pretrained models (EfficientNet, MobileFaceNet, MobileViT and RexNet backbones pre-trained on VGGFace2), a high-level Python package, a high-performance C++ core, ready-to-build Android demo apps, and training notebooks for public datasets (AffectNet, AFEW, VGAF, Aff-Wild2 / ABAW, RAMAS, EngageWild, …).

---

## Table of Contents

1. [Overview](#overview)
2. [Key features](#key-features)
3. [Processing pipeline](#processing-pipeline)
4. [Pretrained models](#pretrained-models)
5. [Installation](#installation)
6. [Quick start](#quick-start)
7. [C++ library](#c-library)
8. [Android demos](#android-demos)
9. [Model conversion & preparation](#model-conversion--preparation)
10. [Training your own models](#training-your-own-models)
11. [Repository structure](#repository-structure)
12. [Testing & CI](#testing--ci)
13. [Documentation](#documentation)
14. [Notebooks in the cloud (Binder)](#notebooks-in-the-cloud-binder)
15. [Datasets](#datasets)
16. [Which model should I use?](#which-model-should-i-use)
17. [Contributing](#contributing)
18. [License](#license)
19. [Acknowledgments & citation](#acknowledgments--citation)

---

## Overview

EmotiEffLib turns the research code and checkpoints of the *face-emotion-recognition* project into a reusable, production-friendly library:

* **Frame-level emotion recognition** — 7-class (Aff-Wild2 style) and 8-class (AffectNet style) classifiers built on top of VGGFace2-pretrained backbones.
* **Video-level prediction** — per-frame embeddings are aggregated (averaging, attention, or your own temporal model) into a decision for the whole clip.
* **Multi-task (MTL) models** — joint prediction of 8 emotions and continuous **valence/arousal** in `[-1, 1]`.
* **Engagement recognition** — an attention-based temporal model over sequences of frame embeddings, with a user-independent checkpoint and notebooks for **user adaptation**.
* **Auxiliary face analysis** — MTCNN face detection (TF and TensorFlow-Lite), and age/gender(/ethnicity) estimation models.

The same models are exposed through three stacks:

| Stack | Backends | Typical use |
|---|---|---|
| **Python package** (`emotiefflib`) | PyTorch (`.pt`), ONNX Runtime (`.onnx`), Keras/TF (`.h5`) | research, notebooks, servers |
| **C++ core** (`emotieffcpplib`) | ONNX Runtime, LibTorch | desktop / embedded, real-time apps |
| **Android demos** (Gradle projects) | PyTorch Mobile (`.ptl`), TensorFlow Lite (`.tflite`) | on-device mobile inference |

---

## Key features

* 😀 Emotion recognition from a **single image** or a **video** (7 or 8 classes)
* 💞 **Valence/arousal** estimation with multi-task heads
* 🎓 **Engagement detection** from sliding windows of frame embeddings, incl. user adaptation
* ⚡ Choice of runtimes: **PyTorch**, **ONNX Runtime**, **Keras/TF**, **TensorFlow Lite**, **PyTorch Mobile**
* 🔍 **MTCNN** face detection & alignment helpers
* 👤 Auxiliary **age / gender (/ethnicity)** models
* 📓 Jupyter notebooks to **reproduce training** and experiment on custom data
* 🧪 Python and C++ (CTest) **test suites**, CI dependency sets
* 📚 **Doxygen** documentation for both the C++ and the Python API

---

## Processing pipeline

```
 video / image          MTCNN              face crops          VGGFace2 backbone                task heads
┌─────────────┐     ┌──────────┐      ┌───────────────┐    ┌────────────────────────┐    ┌────────────────────┐
│ frames ────►│────►│ detector │─────►│ 224×224, RGB  │───►│ ENet-B0/B2 · MBF ·     │───►│ 7/8 emotions ·     │
└─────────────┘     └──────────┘      └───────────────┘    │ MobileViT · RexNet-150 │    │ valence / arousal  │
                                                           └───────────┬────────────┘    └────────────────────┘
                                                                       │ frame embeddings
                                                                       ▼
                                                          ┌────────────────────────┐
                                                          │ temporal aggregation   │
                                                          │ (mean / attention over │
                                                          │  an 80-frame window)   │
                                                          └───────────┬────────────┘
                                                                      ▼
                                                       ┌──────────────────────────────┐
                                                       │ video-level emotions &       │
                                                       │ engagement prediction        │
                                                       └──────────────────────────────┘
```

1. Detect faces in every frame (MTCNN).
2. Crop and resize the face to `224×224` (RGB).
3. Extract a per-frame embedding with a VGGFace2-pretrained backbone.
4. Classify emotions and/or estimate valence–arousal.
5. Aggregate frame-level outputs over the sequence (or feed embeddings to the engagement model).

---

## Pretrained models

### Emotion / valence–arousal models

| Checkpoint | Backbone | Output | Trained / fine-tuned on | Formats |
|---|---|---|---|---|
| `enet_b0_8_best_afew` | EfficientNet-B0 (VGGFace2) | 8 emotions | AFEW | `.pt`, `.onnx` |
| `enet_b0_8_best_vgaf` | EfficientNet-B0 (VGGFace2) | 8 emotions | VGAF | `.pt`, `.onnx` |
| `enet_b2_7` | EfficientNet-B2 (VGGFace2) | 7 emotions | affect datasets (see notebooks) | `.pt`, `.onnx`, `.h5` |
| `enet_b2_8` | EfficientNet-B2 (VGGFace2) | 8 emotions | affect datasets (see notebooks) | `.pt`, `.onnx` |
| `enet_b0_8_va_mtl` | EfficientNet-B0 | 8 emotions **+** valence/arousal | multi-task (ABAW-style) | `.pt`, `.onnx` |
| `mbf_va_mtl` | MobileFaceNet | valence/arousal (+ emotion head), MTL | multi-task (ABAW-style) | `.pt`, `.onnx` |
| `mobilevit_va_mtl` | MobileViT | valence/arousal (+ emotion head), MTL | multi-task (ABAW-style) | `.pt`, `.onnx` |
| `mobilenet_7.h5` | MobileNet (Keras/TF) | 7 emotions | AffectNet-style data | `.h5` |

**Label sets** (the label order used by the mobile apps is stored in `affectnet_labels.txt`):

* **8 classes (AffectNet):** anger, contempt, disgust, fear, happiness, neutral, sadness, surprise
* **7 classes (Aff-Wild2):** anger, disgust, fear, happiness, neutral, sadness, surprise

### Feature extractors (backbones)

| Checkpoint | Architecture | Purpose |
|---|---|---|
| `state_vggface2_enet0_new.pt` | EfficientNet-B0 | frame embedding extractor (fastest) |
| `state_vggface2_enet2.pt` | EfficientNet-B2 | frame embedding extractor (more accurate) |
| `state_vggface2_rexnet_150.pt` | RexNet-150 | alternative embedding extractor |

### Engagement model

| Checkpoint | Architecture | Output | Trained on | Formats |
|---|---|---|---|---|
| `engagement_single_attention.h5` | frame embeddings + single-head attention pooling | engaged / not engaged (binary) | EngageWild | `.h5` (+ converter script) |

The model consumes a **sliding window of 80 consecutive frame embeddings** and is **user-independent**; a personalized (user-adapted) workflow is provided in the notebooks.

### Auxiliary models

| Checkpoint | Purpose |
|---|---|
| `mtcnn.pb`, `mtcnn_model.pb` | MTCNN face detector (TensorFlow frozen graph) |
| `pnet.tflite`, `rnet.tflite`, `onet.tflite` | MTCNN stages for mobile (TFLite) |
| `age_gender_tf2_224_deep-03-0.13-0.97.h5` | age + gender estimation (Keras/TF2, 224×224 input) |
| `age_gender_ethnicity_224_deep-03-0.13-0.97-0.88.pb` | age + gender + ethnicity (TF frozen graph) |

---

## Installation

### Python

```bash
git clone <repository-url>
cd EmotiEffLib

# create an environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# choose ONE inference backend
pip install -r requirements.txt            # ONNX Runtime backend (lightweight)
pip install -r requirements-torch.txt      # PyTorch backend

# install the library
pip install .                              # or: pip install -e . for development
```

Optional extras:

| File | When to use |
|---|---|
| `requirements-engagement.txt` | run the Keras engagement / age-gender models |
| `requirements-binder.txt` | Binder/Colab environment for the example notebooks (ONNX) |
| `requirements-binder-torch.txt` | Binder/Colab environment for the example notebooks (PyTorch) |
| `requirements-ci.txt` | CI pipeline dependencies |

Sanity-check your environment:

```bash
bash check_installed_libs.sh
```

### C++ (`emotieffcpplib`)

Requirements: CMake (≥ 3.x), OpenCV, GoogleTest, and either **ONNX Runtime** or **LibTorch**.

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
ctest --test-dir build --output-on-failure
```

Use the helper script to stage model files for the C++ side:

```bash
python prepare_models_for_emotieffcpplib.py
```

### Android

Open the demo Gradle projects in **Android Studio** (see [Android demos](#android-demos)). The model assets are committed with the apps or can be regenerated with the conversion scripts.

---

## Quick start

The bundled test image `20180720_174416.jpg` is used throughout the examples and tests.

### 1. Emotions from a single image

```python
import cv2
from emotiefflib.facial_analysis import EmotiEffLib, get_model_names

# list all available checkpoints
print(get_model_names())

# load a model (PyTorch or ONNX Runtime depending on the backend/format)
model = EmotiEffLib(model_name="enet_b0_8_best_vgaf", device="cpu")

frame = cv2.cvtColor(cv2.imread("20180720_174416.jpg"), cv2.COLOR_BGR2RGB)

# per-frame embeddings and class scores
features = model.extract_features([frame])
scores   = model.classify_emotions(features, logits=True)
```

> For the best accuracy, crop the face first (e.g., with the provided MTCNN helpers — see `utils.py` and the example notebooks).

### 2. Emotions from video

```python
import cv2
import numpy as np

cap = cv2.VideoCapture("video.mp4")
crops = []
while True:
    ok, bgr = cap.read()
    if not ok:
        break
    crops.append(detect_and_crop_face(bgr))   # MTCNN crop → RGB 224×224 (see notebooks)

features = np.asarray(model.extract_features(crops))          # (T, D)
scores   = np.asarray(model.classify_emotions(features))      # (T, n_classes)

video_prediction = scores.mean(axis=0).argmax()               # simple temporal aggregation
```

### 3. Engagement recognition

```python
import numpy as np
from tensorflow.keras.models import load_model

engagement = load_model("engagement_single_attention.h5")

# features: (T, D) frame embeddings produced by any EmotiEff feature extractor
window  = features[-80:]                                       # last 80 frames
prob    = engagement.predict(window[np.newaxis])[0]
print(f"Engagement probability: {prob:.3f}")
```

For personalized (user-adapted) engagement models, see `04 - Engagement user-adaptation.ipynb`.

### 4. Valence / arousal

Load a `*_va_mtl` checkpoint (e.g., `enet_b0_8_va_mtl`): the multi-task heads return emotion logits **together with** valence and arousal values in `[-1, 1]`.

### 5. Command-line demo

```bash
python recognize_emotions_video.py --help
```

`recognize_emotions_video.py` recognizes emotions in a video file or from a webcam and renders the predictions on top of the frames.

### 6. Example notebooks

* `One image emotion recognition.ipynb` — end-to-end pipeline for photos
* `Predict emotions on video.ipynb` — frame- and video-level emotion prediction
* `Predict engagement and emotions on video.ipynb` — joint engagement + emotions pipeline

---

## C++ library

The `emotieffcpplib` core mirrors the Python API:

* `facial_analysis.h` / `facial_analysis.cpp` — public facade with implementations for the **ONNX Runtime** and **LibTorch** backends;
* CMake-based build with the two test targets (`tests_facial_analisys`, `tests_internal_methods`);
* the same pretrained checkpoints, prepared by `prepare_models_for_emotieffcpplib.py`.

Illustrative usage:

```cpp
#include <opencv2/opencv.hpp>
#include "facial_analysis.h"

int main() {
    // Load a pretrained model (ONNX Runtime or LibTorch backend)
    EmotiEffLib engine("enet_b0_8_va_mtl" /*, backend, device */);

    std::vector<cv::Mat> faceCrops = /* 224×224 RGB MTCNN crops */;

    auto features = engine.extractFeatures(faceCrops);
    auto scores   = engine.classifyEmotions(features);
}
```

Refer to the C++ README and the generated Doxygen reference for the exact signatures.

---

## Android demos

Two Gradle demo applications show how to run the pipeline on a phone with **CameraX** preview (`fragment_camera2_basic.xml`):

1. **PyTorch Mobile demo** — `EmotionPyTorchClassifier.java` runs `enet_b0_8_va_mtl.ptl` (produced by `to_pytorchlite.py`) on-device; when on-device compute is not enough, `ServerProcessor.java` streams face crops to the Python helper `server.py` and receives predictions back. MTCNN runs locally via TFLite (`pnet/rnet/onet.tflite`, `mtcnn_model.pb`).
2. **Fully on-device TF Lite demo** — `EmotionTfLiteClassifier.java` plus `AgeGenderEthnicityTfLiteClassifier.java` (age, gender and ethnicity from `age_gender_ethnicity_224_deep-…pb`), with `EmotionData` / `FaceData` / `ClassifierResult` UI helpers and the `Align` / `MTCNN` / `Box` / `Utils` utilities shared with the first app.

Both apps display the predicted emotion labels (from `affectnet_labels.txt`) over the live camera preview.

---

## Model conversion & preparation

| Script | Direction |
|---|---|
| `convert_pt_to_onnx.py` | PyTorch `.pt` → ONNX `.onnx` |
| `prepare_models_for_emotieffcpplib.py` | package the checkpoints for the C++ library |
| `to_tflite.py` | TF/Keras models → TensorFlow Lite for Android |
| `to_pytorchlite.py` | PyTorch models → PyTorch Mobile `.ptl` |
| `engagement_single_attention_converter.py` | port the Keras engagement model to other runtimes |

---

## Training your own models

### Engagement workflow (`engagement-training/`)

1. `01 - Features-extractor.ipynb` — set up the feature extractor and prepare embeddings.
2. `02 - Engagement user-independent model training.ipynb` — train the attention-based, user-independent engagement classifier.
3. `03 - Custom dataset features extractor.ipynb` — extract features from **your own** dataset.
4. `04 - Engagement user-adaptation.ipynb` — adapt the model to a specific user.
5. `train_faces_torch.ipynb` — fine-tune the face backbones (PyTorch) on custom data.

### Emotion / valence–arousal training & experiments (`model-training/`)

* **Emotions:** `train_emotions.ipynb` (Keras), `train_emotions-pytorch.ipynb`, `train_emotions-pytorch-afew-vgaf.ipynb`
* **AffectNet:** `train_affectnet_march2021_pytorch.ipynb`, `evaluate_affectnet_march2021_pytorch.ipynb`
* **Video datasets:** `AFEW_train.ipynb`, `VGAF_train.ipynb`
* **ABAW / Aff-Wild2 challenge pipelines:** `abaw3_train.ipynb`, `abaw4_lsd_train.ipynb`, `abaw4_mtl_train.ipynb`, `abaw5_expr_va_au_train.ipynb`, `abaw6_affwild2.ipynb`, `abaw8_expr.ipynb`, `mtl.ipynb`
* **Additional studies:** `cexpr.ipynb` (compound expressions), `emi.ipynb`, `bah.ipynb`, `eri.ipynb`, `train_ramas.ipynb`
* **Utilities & demos:** `emotions_experiments.ipynb` (model comparison), `display_emotions.ipynb`, `video_summarizer.ipynb`, `robust_optimization.py`, `recognize_emotions_video.py`

---

## Repository structure

Logical layout of the project (file names as in the repository):

```
EmotiEffLib/
├── README.md, LICENSE
├── setup.py / setup.cfg / pyproject.toml          # Python packaging
├── requirements*.txt                              # backend-specific dependency sets
├── check_installed_libs.sh                        # environment sanity check
├── download_test_data.sh                          # fetch test images/videos
├── test_module_loading.py                         # import / backend tests
├── test_facial_analysis.py                        # end-to-end model tests
├── prepare_models_for_emotieffcpplib.py           # stage models for the C++ library
├── 20180720_174416.jpg                            # bundled test image
│
├── emotiefflib/                                   # Python package
│   ├── __init__.py
│   ├── facial_analysis.py                         # main entry point (models, embeddings, classifiers)
│   ├── mobilefacenet.py                           # MobileFaceNet backbone
│   ├── engagement_classification_model.py
│   ├── utils.py
│   ├── engagement_single_attention.h5
│   └── engagement_single_attention_converter.py
│
├── examples/                                      # end-user notebooks (+ Binder setup)
├── engagement-training/                           # notebooks 01–04, train_faces_torch.ipynb
├── model-training/                                # emotion / VA training & research notebooks
│
├── emotieffcpplib/                                # C++ core
│   ├── facial_analysis.h / facial_analysis.cpp    # common facade + LibTorch + ONNX backends
│   ├── tests/                                     # tests_facial_analisys.cpp,
│   │                                              # tests_internal_methods.cpp,
│   │                                              # test_utils.{h,cpp},
│   │                                              # generate_exp_preproc_results.py
│   └── CMakeLists.txt
│
├── android/                                       # two Gradle demo apps (see above)
│
└── docs/                                          # Doxygen configuration
    ├── Doxyfile, Doxyfile-cpp, Doxyfile-python
    └── DoxygenLayout.xml, DoxygenLayout-cpp.xml, DoxygenLayout-python.xml
```

Pretrained checkpoints (`.pt`, `.onnx`, `.h5`, `.ptl`, `.tflite`, `.pb`) ship with the repository/package or are fetched by `download_test_data.sh` where applicable.

---

## Testing & CI

**Python**

```bash
bash download_test_data.sh        # fetch the test images/videos
python test_module_loading.py     # verify imports and available backends
python test_facial_analysis.py    # end-to-end predictions on the test data
```

**C++**

```bash
cmake -S . -B build && cmake --build build
ctest --test-dir build --output-on-failure
```

* `tests_facial_analisys.cpp` — end-to-end checks of model outputs against reference results;
* `tests_internal_methods.cpp` — unit tests of preprocessing/alignment internals;
* `generate_exp_preproc_results.py` — regenerates the expected outputs used by the tests;
* `test_utils.{h,cpp}` — shared test helpers.

Continuous integration installs `requirements-ci.txt` and calls `check_installed_libs.sh` to validate the environment.

---

## Documentation

API references are generated with **Doxygen**:

```bash
doxygen Doxyfile            # combined documentation
doxygen Doxyfile-cpp        # C++ API only
doxygen Doxyfile-python     # Python API only
```

The layout files (`DoxygenLayout.xml`, `DoxygenLayout-cpp.xml`, `DoxygenLayout-python.xml`) customize the generated HTML. Output is written to the `html/` directory — open `html/index.html` in a browser.

---

## Notebooks in the cloud (Binder)

The example notebooks can be run without a local installation (e.g., in Binder or Colab). The environments are defined by:

* `requirements-binder.txt` — ONNX-based environment;
* `requirements-binder-torch.txt` — PyTorch-based environment.

---

## Datasets

The models and notebooks rely on the following public datasets:

* **AffectNet** — 8-class static emotion classification;
* **AFEW (EmotiW)** and **VGAF** — video-based emotion recognition;
* **Aff-Wild2 / ABAW challenges (3–8)** — expression recognition, valence–arousal, action units;
* **EngageWild** — engagement (attentiveness) recognition;
* **RAMAS** and additional datasets explored in the experiment notebooks (e.g., compound expressions).

---

## Which model should I use?

| Goal | Recommendation |
|---|---|
| Fast CPU / mobile inference | `enet_b0_8_best_vgaf`, `mbf_va_mtl`, `mobilevit_va_mtl` |
| Highest frame-level accuracy | `enet_b2_8` / `enet_b2_7` |
| Video-level emotion (aggregated) | `enet_b0_8_best_vgaf` / `enet_b0_8_best_afew` |
| Emotions + valence/arousal | `enet_b0_8_va_mtl` (or the MBF/MobileViT MTL models) |
| Engagement detection | `engagement_single_attention.h5` over ENet embeddings |
| Custom emotion taxonomy / data | fine-tune with the provided training notebooks |

---

## Contributing

Contributions are welcome! Please open an issue to discuss proposed changes, add tests for new functionality, and make sure `check_installed_libs.sh` and the test suites pass.

---

## License

The code, notebooks, and pretrained models are distributed under the terms of the [LICENSE](LICENSE) file included in this repository. The pretrained models are intended primarily for **research purposes**; check the licenses of the underlying datasets before any commercial use.

---

## Acknowledgments & citation

EmotiEffLib packages the models and experiments originally developed in the *face-emotion-recognition* research project (HSE University), and builds on MTCNN, EfficientNet/`timm`, ONNX Runtime, LibTorch, TensorFlow/TFLite and OpenCV.

If you use EmotiEffLib in your research, please cite the library and the underlying publications on video-based emotion, engagement, and multi-task recognition (see the upstream repository for the full list):

```bibtex
@software{emotiefflib,
  title  = {EmotiEffLib: a cross-platform library for facial emotion and engagement recognition},
  author = {Savchenko, Andrey V.},
  year   = {2024},
  note   = {https://github.com/HSE-asavchenko/EmotiEffLib}
}
```

**See also**

* Upstream research repository with training details: `face-emotion-recognition`
* ABAW / Aff-Wild2 challenge materials, AffectNet, AFEW, VGAF and EngageWild dataset pages

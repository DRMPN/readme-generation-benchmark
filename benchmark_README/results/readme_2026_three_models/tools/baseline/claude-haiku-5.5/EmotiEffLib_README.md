# EmotiEffLib

EmotiEffLib is a library for facial emotion and engagement recognition in images and videos. It provides a Python package (`emotiefflib`) and a C++ library (`emotieffcpplib`). The Python package supports PyTorch and ONNX Runtime inference, and the C++ library supports Libtorch and ONNX Runtime. The package description refers to "Facial Emotion and Engagement Recognition," and the project is authored by Andrey Savchenko and Egor Churaev.

## Overview

The repository contains:

- **`emotiefflib/`**: the Python package, installable via `setup.py` or pip.
- **`emotieffcpplib/`**: the C++ library, built with CMake. It uses OpenCV and xtensor, and is configurable as a static or shared library.
- **`models/`**: pre-trained emotion models (PyTorch, ONNX, and Keras `.h5`), an engagement classification model, and face detection models.
- **`docs/`**: Doxygen configuration files and tutorials for Python and C++.
- **`tests/`**: pytest tests for the Python package.
- **`training_and_examples/`**: Jupyter notebooks for training and experiments, plus two Android demo applications and an emotional dialogue web server.

### Supported models

The Python package exposes the following models through `get_model_list()`:

- `enet_b0_8_best_vgaf`
- `enet_b0_8_best_afew`
- `enet_b2_8`
- `enet_b0_8_va_mtl`
- `enet_b2_7`
- `mbf_va_mtl`
- `mobilevit_va_mtl`

Model names ending in `_7` predict 7 emotion classes (Anger, Disgust, Fear, Happiness, Neutral, Sadness, Surprise). Other models predict 8 classes, which add Contempt. Models containing `_mtl` are multi-task models; the classifier drops the last two outputs when computing emotion predictions.

Engagement is predicted as one of two classes: `Distracted` or `Engaged`.

## Setup

### Python package

Install from source:

```sh
python setup.py install
```

Or install from PyPI with one of the following extras:

```sh
pip install emotiefflib            # ONNX support
pip install emotiefflib[torch]     # ONNX and PyTorch support
pip install emotiefflib[engagement] # ONNX and TensorFlow support (needed for engagement prediction)
pip install emotiefflib[all]       # all dependencies
```

The base dependencies are `numpy`, `onnx`, `onnxruntime`, `opencv-python`, and `pillow`. The `torch` extra adds `timm==0.9.*`, `torch`, and `torchvision`. The `engagement` extra adds `tensorflow` and `tf2onnx==1.16.0`.

### C++ library

Clone the repository with its submodules, since the CMake configuration expects `3rdparty/xtl` and `3rdparty/xtensor`:

```sh
git clone https://github.com/sb-ai-lab/EmotiEffLib.git
cd EmotiEffLib
git submodule update --init --recursive
```

Requirements:

- C++17 or later
- CMake 3.10.2 or later
- OpenCV
- At least one inference engine: Libtorch or ONNX Runtime

Download Libtorch from the PyTorch website or ONNX Runtime from its GitHub releases, unpack each archive, and pass the unpacked paths to CMake. The README notes that the latest Libtorch for x86 macOS is unavailable, and that version 2.2.2 can be downloaded instead.

Basic build:

```sh
mkdir build && cd build
cmake .. -DWITH_TORCH=/path/to/libtorch -DWITH_ONNX=/path/to/onnxruntime
make -j$(nproc)
```

Build with tests:

```sh
cmake .. -DWITH_TORCH=/path/to/libtorch -DWITH_ONNX=/path/to/onnxruntime -DBUILD_TESTS=ON
make -j$(nproc)
```

### Pre-trained models

Model weights are downloaded automatically on first use. `emotiefflib/utils.py` stores them in `~/.emotiefflib` and fetches them from the repository on GitHub if they are not already cached. The engagement model `engagement_single_attention.h5` is downloaded the same way.

For the C++ library, prepare models with the helper script:

```sh
python3 models/prepare_models_for_emotieffcpplib.py
```

The script writes its output to `models/emotieffcpplib_prepared_models`. It processes the ONNX and PyTorch models listed above, splits each into a feature extractor and a classifier, and exports the engagement classifier in ONNX and TorchScript formats.

## Usage

### Python

The main entry point is `EmotiEffLibRecognizer`, which takes `engine`, `model_name`, and `device` arguments. The supported engines are `torch` and `onnx`. The default engine is `torch`, the default model is `enet_b0_8_best_vgaf`, and the default device is `cpu`.

Methods available on the returned recognizer:

- `predict_emotions(face_img, logits=True)`: accepts one face image or a list of face images. Returns predicted labels and scores (logits, or softmax probabilities when `logits=False`).
- `extract_features(face_img)`: returns feature vectors for one or more face images.
- `classify_emotions(features, logits=True)`: classifies previously extracted features.
- `predict_engagement(face_imgs, sliding_window_width=128)`: predicts engagement over a sequence of face images. It raises `ValueError` if there are fewer frames than the window width.
- `classify_engagement(features, sliding_window_width=128)`: classifies engagement from extracted features.

Face images are NumPy arrays in RGB order. The test suite crops faces with `facenet_pytorch.MTCNN`; face detection is not part of the library itself.

A minimal sketch based on these signatures:

```python
from emotiefflib.facial_analysis import EmotiEffLibRecognizer

fer = EmotiEffLibRecognizer(engine="onnx", model_name="enet_b0_8_best_vgaf", device="cpu")
labels, scores = fer.predict_emotions(face_rgb, logits=False)
```

Tutorials are provided as notebooks in [docs/tutorials/python](docs/tutorials/python/README.md). They cover single-image emotion recognition, emotion prediction on video, and engagement plus emotion prediction on video.

### C++

To use the C++ library in another CMake project, add the repository as a subdirectory and link against the `emotiefflib` target:

```cmake
set(WITH_TORCH "/path/to/libtorch")
set(WITH_ONNX "/path/to/ONNXRuntime")
add_subdirectory("${PROJECT_SOURCE_DIR}/path/to/emotiefflib/emotieffcpplib")
include_directories(
    "${PROJECT_SOURCE_DIR}/path/to/emotiefflib/emotieffcpplib/include"
)
target_link_libraries(your_project PRIVATE emotiefflib)
```

Public headers are in `emotieffcpplib/include/emotiefflib/`, including `facial_analysis.h` and backend-specific headers for ONNX and Torch. Examples are in [docs/tutorials/cpp](docs/tutorials/cpp/README.md). Running them requires the `xcpp17` Jupyter kernel from xeus-cling, a C++ build with `-DBUILD_TESTS=ON -DBUILD_SHARED_LIBS=ON`, and the prepared models.

## Configuration

### CMake options (C++)

| Option | Default | Purpose |
|---|---|---|
| `WITH_TORCH` | OFF | Path to the Libtorch directory |
| `WITH_ONNX` | OFF | Path to the ONNX Runtime directory |
| `BUILD_TESTS` | OFF | Build unit tests with GoogleTest |
| `BUILD_SHARED_LIBS` | OFF | Build a shared library instead of a static one |

At least one of `WITH_TORCH` or `WITH_ONNX` must be set, or configuration fails with an error.

### Python runtime options

- **`engine`**: `"torch"` or `"onnx"`. Any other value raises `ValueError`.
- **`device`**: `"cpu"` or `"cuda"`. The ONNX backend always uses `CPUExecutionProvider`.
- **Cache location**: downloaded models are stored in `~/.emotiefflib`.

### Test environment variables

- `EMOTIEFFLIB_ROOT`: root of the repository, used by the C++ tests to locate inputs.
- `WITHOUT_TORCH` and `WITHOUT_ONNX`: when set, the corresponding module-loading tests run and check for the expected `ImportError` messages.

## Development

### Repository layout

- `emotiefflib/`: Python sources (`facial_analysis.py`, `engagement_classification_model.py`, `utils.py`, and `backbones/`).
- `emotieffcpplib/`: C++ sources, with separate ONNX and Torch backends under `src/backends/`.
- `models/`: model files and conversion scripts.
- `training_and_examples/`: training notebooks and mobile applications.

### Code quality

The `.pre-commit-config.yaml` file defines these hooks:

- `pre-commit-hooks` (v4.1.0): merge-conflict check, YAML check, end-of-file fixer, requirements sorting, and trailing-whitespace removal.
- `black` (25.1.0)
- `pylint` (v3.1.0), run on `training_and_examples` with import errors disabled
- `isort` (v5.10.1)
- `clang-format` (v19.1.7) for C and C++ files

`pyproject.toml` sets Black's line length to 100 and target version to Python 3.10. It configures isort with the Black profile and sets Pylint's maximum line length to 100. Pylint ignores `training_and_examples/`, `mobile_app/`, and `emotiefflib/backbones/`.

`requirements-ci.txt` lists `black==25.1.0`, `isort`, `pre-commit`, and `pylint` for continuous integration.

### Documentation

Doxygen configuration files are in `docs/`. From that directory, run:

```sh
doxygen
doxygen Doxyfile-cpp
doxygen Doxyfile-python
```

The generated documentation is written to an `html` folder. Custom layouts are provided in `DoxygenLayout*.xml`.

### Continuous integration

The `.github/workflows/` directory contains workflows for `binder.yml`, `generate_documentation.yml`, `lint.yml`, and `tests.yml`. The `.binder/` directory defines a Binder environment with Python 3.10, CMake, and xeus-cling 0.15.0. Its `apt.txt` lists `cmake`, `g++`, `make`, `wget`, and `libopencv-dev`.

## Testing

### Python

Install the test dependencies (`facenet-pytorch`, `gdown`, `pytest`), download the test data, and run pytest:

```sh
pip install -r tests/requirements.txt
cd tests
./download_test_data.sh
tar -xzf data.tar.gz
cd ..
pytest tests
```

`download_test_data.sh` uses `gdown` to fetch an archive from Google Drive. The tests in `tests/test_facial_analysis.py` cover:

- single-image and multi-image emotion predictions for every model and both engines
- feature extraction comparisons between ONNX and Torch
- an accuracy check on AffectNet validation images (requires accuracy above 0.55 on a subset)
- emotion and engagement predictions on sample videos

`tests/test_module_loading.py` checks the unsupported-engine error and optional missing-library errors. `tests/check_installed_libs.sh` verifies which libraries are installed for a given extras configuration, such as `[torch]` or `[engagement]`.

### C++

Build with `-DBUILD_TESTS=ON`, which fetches GoogleTest during configuration. Then:

```sh
export EMOTIEFFLIB_ROOT="/path/to/root/of/emotiefflib_repo"
cd <emotiefflib_root>/tests
./download_test_data.sh
tar -xzf data.tar.gz
cd -
./<build_dir>/bin/unit_tests
```

## Training and examples

The `training_and_examples/` directory contains Jupyter notebooks and scripts. The main notebooks are:

- `affectnet/train_emotions-pytorch.ipynb`, described as the main training file for EmotiEffNet models
- `affectnet/train_emotions.ipynb`, for the TensorFlow MobileNet model
- `AFEW_train.ipynb` and `VGAF_train.ipynb`, for dataset preprocessing and classifier training
- `train_faces_torch.ipynb`, for facial recognition pre-training on VGGFace2
- `display_emotions.ipynb`, which visualizes predictions with GradCAM
- `video_summarizer.ipynb`, for conference video processing
- `ABAW/` and `personalized_models/`, for challenge-specific and personalized engagement models

`convert_pt_to_onnx.py` exports PyTorch models to ONNX. The `mobile_apps/` directory contains an Android demo (`demo`) and an emotional dialogue application (`emotional_dialogue`) with a Python `web_server/server.py`. The README asks users to run `to_tflite.py` and `to_pytorchlite.py` before using the mobile application.

## License

The code is released under the Apache License, Version 2.0. The `LICENSE` file contains the full text. `setup.py` also declares `Apache-2.0` as the license for the Python package.

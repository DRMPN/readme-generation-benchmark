# EmotiEffLib

**EmotiEffLib** is a library for facial emotion and engagement recognition in images and videos. It provides efficient and accurate implementations of models for recognizing emotions and engagement from facial images, available in both **Python** (`emotiefflib`) and **C++** (`emotieffcpplib` / EmotiEffCppLib).

- Repository: <https://github.com/sb-ai-lab/EmotiEffLib>
- License: Apache-2.0
- Authors: Andrey Savchenko, Egor Churaev

## Overview

The repository is organized around two main library packages plus a rich set of supporting materials:

| Component | Description |
|---|---|
| `emotiefflib/` | Python library for facial emotion and engagement recognition |
| `emotieffcpplib/` | C++ library (EmotiEffCppLib) with Libtorch and ONNX Runtime backends |
| `models/` | Pretrained models (AffectNet-based emotion recognition, engagement classification, face preprocessing) |
| `docs/` | Doxygen configuration and Jupyter tutorials (Python and C++) |
| `training_and_examples/` | Training notebooks, examples, and Android mobile app demos |
| `tests/` | Python test suite |

### Python library

The `emotiefflib` package includes:

- `facial_analysis.py` — facial analysis functionality for emotion recognition
- `engagement_classification_model.py` — engagement classification models
- `backbones/mobilefacenet.py` — MobileFaceNet backbone
- `utils.py` — utility helpers

The library supports two backends: **PyTorch** (via the `torch` extra) and **ONNX Runtime** (available with the base installation). Engagement classification additionally requires TensorFlow and tf2onnx (the `engagement` extra).

### C++ library

EmotiEffCppLib is designed for emotion and engagement recognition in images and videos. Key features:

- Multiple inference engines: **Libtorch** and **ONNX Runtime**
- **OpenCV** for image processing
- **xtensor** for working with tensors
- Configurable as a static or shared library
- Separate backend implementations (`backends/torch`, `backends/onnx`) behind a common `facial_analysis` interface

## Requirements

### Python

- Python 3.10 is used for the Binder environment and linting configuration
- Core dependencies: `numpy`, `onnx`, `onnxruntime`, `opencv-python`, `pillow`
- Optional extras:
  - `torch`: `torch`, `torchvision`, `timm==0.9.*`
  - `engagement`: `tensorflow`, `tf2onnx==1.16.0`
  - `all`: both of the above

### C++

- C++17 or later
- CMake 3.10.2 or later
- OpenCV
- At least one of the inference engines: Libtorch or ONNX Runtime

## Setup

### Installing the Python library

Install from the repository root:

```sh
pip install .
```

To include optional dependencies, install with extras:

```sh
# PyTorch backend
pip install .[torch]

# Engagement classification
pip install .[engagement]

# Everything
pip install .[all]
```

### Building the C++ library

1. **Clone the repository**

   ```sh
   git clone https://github.com/sb-ai-lab/EmotiEffLib.git
   cd EmotiEffLib
   git submodule update --init --recursive
   ```

2. **Prepare inference engines**

   *Libtorch*: download a build for your OS from <https://pytorch.org/get-started/locally/> and unpack it. Note that the newest Libtorch for x86 macOS is not available; the latest available version, 2.2.2, can be downloaded from <https://download.pytorch.org/libtorch/cpu/libtorch-macos-x86_64-2.2.2.zip>. The unpacked folder path is passed via `-DWITH_TORCH`.

   *ONNX Runtime*: download the latest release for your OS from <https://github.com/microsoft/onnxruntime/releases> and unpack it. The unpacked folder path is passed via `-DWITH_ONNX`.

3. **Configure and build**

   ```sh
   mkdir build && cd build
   cmake .. -DWITH_TORCH=/path/to/libtorch -DWITH_ONNX=/path/to/onnxruntime
   make -j$(nproc)
   ```

   At least one of `WITH_TORCH` or `WITH_ONNX` must be enabled.

### CMake options

| Option | Default | Description |
|---|---|---|
| `WITH_TORCH` | `OFF` | Path to the directory containing Libtorch |
| `WITH_ONNX` | `OFF` | Path to the directory containing ONNX Runtime |
| `BUILD_TESTS` | `OFF` | Enable building unit tests using GoogleTest |
| `BUILD_SHARED_LIBS` | `OFF` | Build as a shared library instead of a static library |

## Usage

### Python

Examples of using `emotiefflib` are provided as Jupyter tutorials in `docs/tutorials/python`:

- *One image emotion recognition*
- *Predict emotions on video*
- *Predict engagement and emotions on video*

To run the tutorials, install the tutorial requirements:

```sh
pip install -r docs/tutorials/python/requirements.txt
```

### C++

To use EmotiEffCppLib in your own project, add this repository as a submodule and reference it from your `CMakeLists.txt`:

```cmake
# At least one of these variables should be specified
set(WITH_TORCH "/path/to/libtorch")
set(WITH_ONNX "/path/to/ONNXRuntime")
add_subdirectory("${PROJECT_SOURCE_DIR}/path/to/emotiefflib/emotieffcpplib")
include_directories(
    "${PROJECT_SOURCE_DIR}/path/to/emotiefflib/emotieffcpplib/include"
)
target_link_libraries(your_project PRIVATE emotiefflib)
```

C++ tutorials are located in `docs/tutorials/cpp` and mirror the Python ones (single-image emotion recognition, emotions on video, engagement and emotions on video). They require `jupyter`/`notebook` (see `docs/tutorials/cpp/requirements.txt`) and are designed to run with the C++ kernel provided by the Binder environment (`xeus-cling`).

### Pretrained models

The `models/` directory contains pretrained models used by the library and examples:

- `models/affectnet_emotions/` — emotion recognition models trained on AffectNet-related setups, including:
  - `enet_b0_8_best_afew`, `enet_b0_8_best_vgaf`, `enet_b0_8_va_mtl`, `enet_b2_7`, `enet_b2_8`, `mbf_va_mtl`, `mobilevit_va_mtl` (PyTorch `.pt` files)
  - corresponding ONNX versions in `models/affectnet_emotions/onnx/`
  - `mobilenet_7.h5` (TensorFlow/Keras 7-emotion model)
  - See `models/affectnet_emotions/README.md` for details
- `models/engagement_classification/` — engagement classification model (`engagement_single_attention.h5`) and its converter script
- `models/pretrained_faces/` — face-related preprocessing models (e.g., `mtcnn.pb` for MTCNN face detection, VGGFace2-based feature extractors, an age/gender model)

The script `models/prepare_models_for_emotieffcpplib.py` prepares models for use with the C++ library. PyTorch models can be converted to ONNX with `training_and_examples/convert_pt_to_onnx.py` (input size is 260 for `_b2_` models, 224 otherwise).

## Documentation

Doxygen is used to generate the project documentation. Configuration files are located in `docs/` (`Doxyfile`, `Doxyfile-cpp`, `Doxyfile-python`). To build the documentation, run the following commands in the `docs/` directory:

```sh
doxygen
doxygen Doxyfile-cpp
doxygen Doxyfile-python
```

The generated documentation is written to the `html` folder.

## Binder

The repository includes a Binder configuration (`.binder/`) so the tutorials can be launched in an executable online environment. The environment is based on:

- Python 3.10 (conda-forge)
- `cmake`
- `xeus-cling=0.15.0` (C++ kernel for Jupyter, used by the C++ tutorials)

Additional dependencies for Binder runs are listed in `requirements-binder.txt` (CPU TensorFlow/tf2onnx/ONNX stack) and `requirements-binder-torch.txt` (CPU PyTorch 2.2.0 build). A Binder workflow is set up via `.github/workflows/binder.yml`.

## Testing

### Python tests

The Python test suite lives in `tests/` and uses `pytest`:

- `tests/test_facial_analysis.py` — tests for the facial analysis functionality
- `tests/test_module_loading.py` — tests for model module loading
- `tests/download_test_data.sh` — script to download test data
- `tests/check_installed_libs.sh` — script to check installed libraries
- `tests/README.md` — additional details about testing

Install test requirements and run the tests:

```sh
pip install -r tests/requirements.txt
```

### C++ tests

The C++ library uses **GoogleTest** for unit testing (`emotieffcpplib/tests/`):

1. Build EmotiEffCppLib with the option `-DBUILD_TESTS=ON`.
2. Define the `EMOTIEFFLIB_ROOT` environment variable pointing to the root of the EmotiEffLib repository:

   ```sh
   export EMOTIEFFLIB_ROOT="/path/to/root/of/emotiefflib"
   ```

Test targets include `tests_facial_analisys.cpp` and `tests_internal_methods.cpp`, with helper utilities in `tests/test_utils.cpp` / `tests/include/test_utils.h`. Expected preprocessing results used by the tests are generated with `tests/generate_exp_preproc_results.py`.

## Development

### Code style and linting

- Python code is formatted with **black** (line length 100, target Python 3.10) and imports sorted with **isort** (black profile), configured in `pyproject.toml`.
- **pylint** is configured in `pyproject.toml` (max line length 100; `training_and_examples/`, `mobile_app/`, and `emotiefflib/backbones/` are excluded from some checks).
- A **pre-commit** configuration is provided in `.pre-commit-config.yaml`.
- Lint requirements are in `requirements-ci.txt` (`black`, `isort`, `pre-commit`, `pylint`).
- An `.editorconfig` file is included for consistent editor settings.

Install and enable the linting tools:

```sh
pip install -r requirements-ci.txt
pre-commit install
```

### CI

GitHub Actions workflows are defined in `.github/workflows/`:

- `lint.yml` — code linting
- `tests.yml` — running tests
- `generate_documentation.yml` — generating documentation
- `binder.yml` — Binder-related checks

### C++ code style

The C++ library includes a `.clang-format` file (`emotieffcpplib/.clang-format`) for consistent C++ formatting.

## Examples and training

The `training_and_examples/` directory contains a broad collection of Jupyter notebooks and scripts:

- **Emotion model training**: notebooks for training on AffectNet (`affectnet/train_emotions*.ipynb`, `train_affectnet_march2021_pytorch.ipynb`), AFEW (`AFEW_train.ipynb`), and VGAF (`VGAF_train.ipynb`).
- **ABAW challenges**: notebooks for ABAW3–ABAW8 (expression recognition, valence–arousal, action units, multi-task learning, engagement).
- **Engagement**: `personalized_models/` notebooks covering feature extraction, user-independent engagement model training, custom dataset feature extraction, and user adaptation.
- **Utilities and demos**: `display_emotions.ipynb`, `video_summarizer.ipynb`, `train_faces_torch.ipynb`, `train_ramas.ipynb`, `facial_analysis.py` (MTCNN-based face processing), emotion-LLM experiments (`emotions_llm/`), and ONNX conversion (`convert_pt_to_onnx.py`).

Additional requirements for running the examples are listed in `training_and_examples/requirements.txt`.

### Mobile apps

Two Android demo applications are provided under `training_and_examples/mobile_apps/`:

- **demo** (`com.asav.facialprocessing`) — real-time facial processing demo using TensorFlow Lite and PyTorch Lite, with MTCNN face detection.
- **emotional_dialogue** (`com.asav.facialprocessing.insideout`) — emotion recognition with a dialogue component, connecting to a companion web server (`web_server/server.py`).

Both are Gradle-based Android projects (Kotlin, CameraX, TensorFlow Lite, PyTorch Lite) targeting arm64-v8a devices, and include model conversion scripts (`to_tflite.py`, `to_pytorchlite.py`).

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for the full license text.

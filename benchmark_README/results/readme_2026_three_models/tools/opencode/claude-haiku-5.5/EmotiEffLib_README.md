# EmotiEffLib

EmotiEffLib is a library for facial emotion recognition and, for video sequences, engagement recognition. It is provided in two implementations:

- **Python** (`emotiefflib/`), with Torch and ONNX Runtime inference engines.
- **C++** (`emotieffcpplib/`), with LibTorch and ONNX Runtime inference backends.

The project also contains pre-trained models, tutorials, training notebooks, and example mobile applications.

License: Apache-2.0 (see [LICENSE](LICENSE)).

## Contents

- [Features](#features)
- [Repository layout](#repository-layout)
- [Pre-trained models](#pre-trained-models)
- [Python: installation](#python-installation)
- [Python: usage](#python-usage)
- [C++: requirements](#c-requirements)
- [C++: building](#c-building)
- [C++: usage](#c-usage)
- [Running tests](#running-tests)
- [Documentation and tutorials](#documentation-and-tutorials)
- [Training and examples](#training-and-examples)
- [License](#license)

## Features

- Emotion recognition on face images, with labels from 7- or 8-class models.
- Emotion recognition on sequences of face images (for example, video frames).
- Engagement recognition (`Distracted` / `Engaged`) on a sequence of face images, using a sliding window of 128 frames.
- Access to raw scores (logits) or softmax probabilities for emotion predictions.
- Feature extraction separated from classification, so features can be extracted once and then classified with emotion or engagement heads.
- Python package with optional Torch and TensorFlow extras.
- C++17 library that can be built as a static or shared library.

Face detection is not part of the library. The test suite and tutorials use an external face detector (MTCNN) to crop faces before passing them to EmotiEffLib.

## Repository layout

| Path | Contents |
| --- | --- |
| `emotiefflib/` | Python package: `facial_analysis.py` (public API), `engagement_classification_model.py`, `utils.py` (model download and caching), `backbones/` |
| `emotieffcpplib/` | C++ library: CMake project, public header in `include/emotiefflib/`, sources in `src/` (with `src/backends/torch` and `src/backends/onnx`), and GoogleTest tests in `tests/` |
| `models/` | Pre-trained model files (`affectnet_emotions/`, `engagement_classification/`, `pretrained_faces/`) and `prepare_models_for_emotieffcpplib.py`, which prepares models for the C++ library |
| `tests/` | Python pytest suite, test-data download script, and test images |
| `docs/` | Doxygen configuration and tutorials (`docs/tutorials/python`, `docs/tutorials/cpp`) |
| `training_and_examples/` | Training notebooks, example scripts, personalized engagement models, and Android example apps |
| `.github/workflows/` | CI: unit tests, lint (Black, isort, Pylint, clang-format), documentation build, and Binder |

## Pre-trained models

The following models are available through `get_model_list()` in Python and `getSupportedModels()` in C++.

| Model name | Emotion classes | Input size | Python Torch | Python ONNX | C++ LibTorch | C++ ONNX |
| --- | --- | --- | --- | --- | --- | --- |
| `enet_b0_8_best_vgaf` | 8 | 224 | Yes | Yes | Yes | Yes |
| `enet_b0_8_best_afew` | 8 | 224 | Yes | Yes | Yes | Yes |
| `enet_b2_8` | 8 | 260 | Yes | Yes | Yes | Yes |
| `enet_b0_8_va_mtl` | 8 | 224 | Yes | Yes | Yes | Yes |
| `enet_b2_7` | 7 | 260 | Yes | Yes | Yes | Yes |
| `mbf_va_mtl` | 8 | 112 | Yes | Yes | No | Yes |
| `mobilevit_va_mtl` | 8 | 224 | Yes | Yes | No | Yes |

Notes:

- Model names containing `_mtl` are multi-task models. For these, the last two outputs are not emotion scores and are excluded from emotion classification.
- Model names containing `_7` use 7 emotion classes. All other models use 8 classes.
- The C++ `LibTorch` column reflects `getSupportedModels("torch")` in `emotieffcpplib/src/facial_analysis.cpp`. `mbf_va_mtl` and `mobilevit_va_mtl` are only listed for ONNX.
- The Python ONNX engine runs on the CPU execution provider only.

Emotion labels:

- 8-class models: `Anger`, `Contempt`, `Disgust`, `Fear`, `Happiness`, `Neutral`, `Sadness`, `Surprise`.
- 7-class models: `Anger`, `Disgust`, `Fear`, `Happiness`, `Neutral`, `Sadness`, `Surprise`.

Engagement labels: `Distracted`, `Engaged`.

### Model download and cache

On first use, the Python library downloads the requested model from this GitHub repository into `~/.emotiefflib/` (see `emotiefflib/utils.py`). Later calls reuse the cached file. The engagement classifier weights (`engagement_single_attention.h5`) are cached the same way.

The engagement classifier expects 2560-dimensional features. The test suite runs engagement tests only for `enet_b0` models and marks other models as expected failures.

## Python: installation

The Python package is named `emotiefflib` and requires Python 3.10 in CI.

Install from PyPI:

```sh
pip install emotiefflib            # ONNX Runtime engine
pip install emotiefflib[torch]     # ONNX and Torch engines
pip install emotiefflib[engagement] # ONNX and TensorFlow (needed for engagement prediction)
pip install emotiefflib[all]       # All of the above
```

Or install from a clone of this repository (run from the repository root, because `setup.py` reads the requirements files from the current directory):

```sh
python setup.py install
```

Base dependencies (`requirements.txt`): `numpy`, `onnx`, `onnxruntime`, `opencv-python`, `pillow`.

Extra dependencies:

- `torch` extra (`requirements-torch.txt`): `timm==0.9.*`, `torch`, `torchvision`.
- `engagement` extra (`requirements-engagement.txt`): `tensorflow`, `tf2onnx==1.16.0`.

## Python: usage

Import the factory function and create a recognizer:

```python
import cv2
from emotiefflib.facial_analysis import EmotiEffLibRecognizer, get_model_list

print(get_model_list())

fer = EmotiEffLibRecognizer(engine="onnx", model_name="enet_b0_8_best_vgaf", device="cpu")

# Face crops must be RGB NumPy arrays (OpenCV loads BGR, so convert first).
face_bgr = cv2.imread("face.jpg")
face_rgb = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB)

labels, scores = fer.predict_emotions(face_rgb, logits=False)
print(labels[0], scores)
```

Signatures used in the code:

- `EmotiEffLibRecognizer(engine="torch", model_name="enet_b0_8_best_vgaf", device="cpu")`. `engine` is `"torch"` or `"onnx"`. `device` is passed to Torch (for example, `"cuda"`); the ONNX engine ignores it.
- `predict_emotions(face_img, logits=True)`: `face_img` is one face image or a list of face images. Returns `(labels, scores)`. With `logits=False`, scores are softmax probabilities.
- `predict_engagement(face_imgs, sliding_window_width=128)`: `face_imgs` is a list of face images in temporal order. Returns `(labels, scores)`. It raises `ValueError` if there are fewer frames than the window width.
- `extract_features(face_img)`: returns feature vectors. `classify_emotions(features, logits=True)` and `classify_engagement(features, sliding_window_width=128)` classify previously extracted features.

Example for video:

```python
frames = []  # list of RGB face crops, one per frame where a face was detected

labels, scores = fer.predict_emotions(frames, logits=True)
_, eng_scores = fer.predict_engagement(frames, sliding_window_width=128)
```

Requirements for engagement: install the `engagement` extra, use a model whose features are 2560-dimensional (see above), and provide at least 128 face frames.

The tutorial notebooks in [docs/tutorials/python](docs/tutorials/python) show complete examples.

## C++: requirements

- C++17 compiler.
- CMake 3.10.2 or later.
- OpenCV (`find_package(OpenCV REQUIRED)`).
- At least one inference engine: LibTorch (`WITH_TORCH`) or ONNX Runtime (`WITH_ONNX`).
- The `xtl` and `xtensor` git submodules under `emotieffcpplib/3rdparty/`.

Other dependencies declared in `.gitmodules`: `opencv-mtcnn` (used by the tutorials) and `nlohmann/json` (used by `docs/tutorials/cpp`).

## C++: building

Clone the repository with submodules:

```sh
git clone https://github.com/sb-ai-lab/EmotiEffLib.git
cd EmotiEffLib
git submodule update --init --recursive
```

Download the engines:

- **LibTorch**: download from [pytorch.org](https://pytorch.org/get-started/locally/). For x86 macOS, the note in the C++ README points to LibTorch 2.2.2.
- **ONNX Runtime**: download a release from [github.com/microsoft/onnxruntime/releases](https://github.com/microsoft/onnxruntime/releases).

Configure and build (from the repository root):

```sh
cmake -S emotieffcpplib -B build -DWITH_TORCH=/path/to/libtorch -DWITH_ONNX=/path/to/onnxruntime
cmake --build build -- -j$(nproc)
```

CMake options:

| Option | Default | Description |
| --- | --- | --- |
| `WITH_TORCH` | `OFF` | Path to the LibTorch directory. |
| `WITH_ONNX` | `OFF` | Path to the ONNX Runtime directory. |
| `BUILD_TESTS` | `OFF` | Build GoogleTest unit tests (fetched by CMake). |
| `BUILD_SHARED_LIBS` | `OFF` | Build a shared library instead of a static one. |

At least one of `WITH_TORCH` or `WITH_ONNX` must be set; otherwise configuration fails.

To use the library in another CMake project, add the directory as a subdirectory and link the `emotiefflib` target:

```cmake
set(WITH_ONNX "/path/to/onnxruntime")
add_subdirectory("path/to/EmotiEffLib/emotieffcpplib")
include_directories("path/to/EmotiEffLib/emotieffcpplib/include")
target_link_libraries(your_project PRIVATE emotiefflib)
```


## C++: usage

The public API is in `emotieffcpplib/include/emotiefflib/facial_analysis.h`, namespace `EmotiEffLib`.

```cpp
#include <emotiefflib/facial_analysis.h>

// backend is "torch" or "onnx"; modelPath is the path to the prepared model file.
auto fer = EmotiEffLib::EmotiEffLibRecognizer::createInstance("onnx", modelPath);

std::vector<cv::Mat> faces; // RGB face crops
auto res = fer->predictEmotions(faces, true); // res.labels, res.scores

auto eng = fer->predictEngagement(faces); // requires at least 128 faces
```

Other entry points:

- `EmotiEffLibRecognizer::createInstance(const EmotiEffLibConfig&)` for explicit configuration (backend, model paths, model name).
- `getAvailableBackends()` returns the backends compiled into the library (`"torch"`, `"onnx"`).
- `getSupportedModels(backend)` returns the models supported by a backend.
- `predictEmotions(const cv::Mat&, bool logits)`, `extractFeatures(...)`, `classifyEmotions(...)`, and `classifyEngagement(...)`.

C++ models must be prepared before use. Run this from the repository root:

```sh
python3 models/prepare_models_for_emotieffcpplib.py
```

The script writes the prepared models to `models/emotieffcpplib_prepared_models/`. It requires Python with `onnx` and/or `torch` installed, and the `engagement_classification` converter module that the script imports. The script skips the `mbf_va_mtl` and `mobilevit_va_mtl` Torch models.

## Running tests

### Python tests

```sh
pip install -r tests/requirements.txt
cd tests
./download_test_data.sh      # downloads data.tar.gz with gdown from Google Drive
tar -xzf data.tar.gz
cd ..
pytest tests/
```

`tests/requirements.txt` installs `facenet-pytorch` (MTCNN face detection), `gdown`, and `pytest`. The tests also need the Torch and TensorFlow extras (see [Python: installation](#python-installation)); CI installs all of them. The engagement tests call `predict_engagement` and need TensorFlow.

The test module `tests/test_module_loading.py` checks error messages when Torch or ONNX is missing. It runs without those packages (`WITHOUT_TORCH` and `WITHOUT_ONNX` environment variables).

### C++ tests

Build with `-DBUILD_TESTS=ON`, then run the GoogleTest binary. The tests read their inputs from `EMOTIEFFLIB_ROOT`.

```sh
cmake -S emotieffcpplib -B build -DWITH_TORCH=/path/to/libtorch -DWITH_ONNX=/path/to/onnxruntime -DBUILD_TESTS=ON
cmake --build build -- -j$(nproc)
python3 models/prepare_models_for_emotieffcpplib.py
cd tests && ./download_test_data.sh && tar -xzf data.tar.gz && cd ..
EMOTIEFFLIB_ROOT=$PWD ./build/bin/unit_tests
```

CI runs the Python tests on Python 3.10 and the C++ tests on Linux with LibTorch 2.6.0 (CPU) and ONNX Runtime 1.20.1 (`.github/workflows/tests.yml`).

## Documentation and tutorials

- [docs/README.md](docs/README.md) describes how to generate Doxygen documentation (`doxygen`, `doxygen Doxyfile-cpp`, `doxygen Doxyfile-python`). The output goes to `docs/html/`. On pushes to `main`, `.github/workflows/generate_documentation.yml` builds it and deploys it to GitHub Pages.
- [Python tutorials](docs/tutorials/python/README.md): one-image emotion recognition, emotions on video, and engagement and emotions on video.
- [C++ tutorials](docs/tutorials/cpp/README.md): the same three topics in C++. These run as Jupyter notebooks with the `xcpp17` kernel from [xeus-cling](https://github.com/jupyter-xeus/xeus-cling). Building them requires the C++ library built with `-DBUILD_TESTS=ON -DBUILD_SHARED_LIBS=ON`.

## Training and examples

[training_and_examples/README.md](training_and_examples/README.md) lists the training and example material, including:

- `affectnet/`: training notebooks for the EmotiEffNet models and evaluation scripts, including `robust_optimization.py`.
- `ABAW/`: classifiers built on the emotional features for ABAW challenges.
- `personalized_models/`: notebooks for personalized engagement models.
- `emotions_llm/`: code for a demo of an emotional multi-agent multimodal dialogue system, published at IJCAI 2024.
- `mobile_apps/`: Android example apps (`demo` and `emotional_dialogue`). To prepare models for the `demo` app, run `to_tflite.py` and `to_pytorchlite.py` in `mobile_apps/demo/`.

Pre-trained models are in [models/](models/). [models/affectnet_emotions/README.md](models/affectnet_emotions/README.md) notes that some other models are available on Google Drive.

## License

The code is released under the Apache License, Version 2.0. See [LICENSE](LICENSE).

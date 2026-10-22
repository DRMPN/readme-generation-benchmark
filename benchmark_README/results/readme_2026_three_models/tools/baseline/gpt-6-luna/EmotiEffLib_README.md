# EmotiEffLib

EmotiEffLib is a Python and C++ library for facial emotion recognition and engagement recognition from images and videos. Both implementations support ONNX Runtime; the Python implementation also supports PyTorch, while the C++ implementation can be built with Libtorch, ONNX Runtime, or both. OpenCV is used for image processing.

The recognizers take face images as input. Face detection and cropping are separate steps: the tutorials and tests show pipelines that detect faces before passing the resulting crops to EmotiEffLib.

## Repository contents

- `emotiefflib/`: Python library, including emotion recognition, feature extraction, and engagement classification.
- `emotieffcpplib/`: C++ library and its unit tests.
- `models/`: emotion and engagement models, including ONNX and PyTorch model files.
- `docs/tutorials/`: Jupyter notebooks for image and video recognition in Python and C++.
- `training_and_examples/`: model-training notebooks, conversion utilities, personalized engagement examples, and Android application projects.
- `tests/`: Python tests, a sample image, and scripts for retrieving additional test data.
- `docs/`: Doxygen configuration and documentation instructions.

## Python setup

The basic Python installation provides the ONNX dependencies:

```bash
python -m pip install emotiefflib
```

To install from a local checkout instead:

```bash
git clone https://github.com/sb-ai-lab/EmotiEffLib.git
cd EmotiEffLib
python -m pip install .
```

The package defines optional dependency groups:

```bash
# ONNX support and PyTorch support
python -m pip install "emotiefflib[torch]"

# ONNX support and TensorFlow, used for engagement prediction
python -m pip install "emotiefflib[engagement]"

# Both optional groups
python -m pip install "emotiefflib[all]"
```

The base requirements include NumPy, ONNX, ONNX Runtime, OpenCV, and Pillow. The `torch` extra adds `timm`, Torch, and TorchVision. The `engagement` extra adds TensorFlow and `tf2onnx`. The `all` extra combines the Torch and engagement dependencies. Alternatively, install the project’s requirements directly with `python -m pip install -r requirements.txt`, `requirements-torch.txt`, or `requirements-engagement.txt`.

## Python usage

Create a recognizer with `EmotiEffLibRecognizer`, specifying an inference engine and model. The default engine is `torch`; use `onnx` when relying on the base installation.

```python
import numpy as np
from PIL import Image

from emotiefflib.facial_analysis import EmotiEffLibRecognizer

# Supply a face crop represented as an RGB NumPy array.
face = np.asarray(Image.open("face.jpg").convert("RGB"))

recognizer = EmotiEffLibRecognizer(
    engine="onnx",
    model_name="enet_b0_8_best_vgaf",
)

labels, scores = recognizer.predict_emotions(face, logits=False)
print(labels)
print(scores)
```

`predict_emotions` accepts one NumPy image or a list of NumPy images. It returns predicted labels and model scores; with `logits=False`, emotion scores are softmax-normalized. By default, the method returns logits. For applications that already have feature vectors, use `extract_features` and `classify_emotions` separately.

The available model names are:

- `enet_b0_8_best_vgaf`
- `enet_b0_8_best_afew`
- `enet_b2_8`
- `enet_b0_8_va_mtl`
- `enet_b2_7`
- `mbf_va_mtl`
- `mobilevit_va_mtl`

Use `get_model_list()` to retrieve this list and `get_supported_engines()` to retrieve the supported engine names. The recognizer’s `device` parameter defaults to `"cpu"` and is used by the Torch engine; the factory also accepts `"cuda"` for Torch inference.

For a sequence of face crops, `predict_engagement` extracts features and classifies engagement. You can instead call `classify_engagement` on extracted features. The default sliding-window width is 128 frames; the number of frames must be at least the chosen window width. Engagement prediction uses the TensorFlow-backed classifier and therefore requires the `engagement` extra.

The library downloads model files on demand when needed and stores them in `~/.emotiefflib`. The Python tutorials include notebooks for recognizing emotions in one image, predicting emotions on video, and predicting engagement and emotions on video. See `docs/tutorials/python/README.md` for instructions to install the tutorial dependencies.

## C++ build

The C++ library requires C++17, CMake 3.10.2 or later, OpenCV, and at least one inference engine. Obtain and unpack Libtorch and/or ONNX Runtime for your platform. Then configure and build from the C++ library directory:

```bash
cd emotieffcpplib
mkdir build
cd build
cmake .. \
  -DWITH_TORCH=/path/to/libtorch \
  -DWITH_ONNX=/path/to/onnxruntime
make -j"$(nproc)"
```

Use at least one of `WITH_TORCH` or `WITH_ONNX`; both are optional individually but the CMake configuration fails if neither is set. Other options are `BUILD_TESTS` (default `OFF`) and `BUILD_SHARED_LIBS` (default `OFF`). For example, to build a shared library with tests enabled:

```bash
cmake .. \
  -DWITH_TORCH=/path/to/libtorch \
  -DWITH_ONNX=/path/to/onnxruntime \
  -DBUILD_TESTS=ON \
  -DBUILD_SHARED_LIBS=ON
make -j"$(nproc)"
```

The CMake project builds the `emotiefflib` library. To link it into another CMake project, add the `emotieffcpplib` directory with `add_subdirectory`, include its `include` directory, and link your target to `emotiefflib`. The C++ tutorials cover image, video, and engagement examples. Their setup additionally requires Python notebook dependencies, `xeus-cling` with an `xcpp17` kernel, models prepared for the C++ runtime, and test data. Follow `docs/tutorials/cpp/README.md` for those steps.

## Configuration and models

Choose `engine` as `"torch"` or `"onnx"` when constructing a Python recognizer. Choose `model_name` from the available list above. Emotion model class labels depend on the selected model: for example, the seven-class models use a different label set from the eight-class models. The default emotion output is logits; pass `logits=False` to `predict_emotions` for normalized probabilities.

The repository includes model files under `models/affectnet_emotions/` and ONNX files under its `onnx/` subdirectory. `models/prepare_models_for_emotieffcpplib.py` prepares model files for C++ inference, subject to the installed conversion dependencies. The repository also contains additional pretrained face models and engagement assets.

## Development

Install development tools with:

```bash
python -m pip install -r requirements-ci.txt
pre-commit install
```

The pre-commit configuration runs checks for merge conflicts, YAML formatting, trailing whitespace, and end-of-file formatting, as well as Black, isort, Pylint, and clang-format. Black and Pylint use a 100-character line limit. The CI requirements file lists Black, isort, pre-commit, and Pylint.

Training notebooks and auxiliary scripts are in `training_and_examples/`. Their dependencies are listed separately in `training_and_examples/requirements.txt`; this set includes packages for notebooks, computer vision, and model training and is not required for the basic Python installation.

## Testing

For Python tests, install the test requirements and retrieve the test archive:

```bash
python -m pip install -r tests/requirements.txt
cd tests
./download_test_data.sh
tar -xzf data.tar.gz
cd ..
pytest tests
```

The test requirements include pytest, `gdown`, and `facenet-pytorch`. The tests exercise image, video, model-loading, and engagement functionality; the data-dependent cases use files from the downloaded archive.

For C++ tests, configure with `-DBUILD_TESTS=ON`, set `EMOTIEFFLIB_ROOT` to the repository root, download and extract test data from `tests/`, and run the resulting executable:

```bash
export EMOTIEFFLIB_ROOT="/path/to/EmotiEffLib"
cd tests
./download_test_data.sh
tar -xzf data.tar.gz
cd ..
./emotieffcpplib/build/bin/unit_tests
```

## Documentation

The `docs/tutorials/` directory contains Python and C++ Jupyter notebooks. To generate Doxygen documentation, install Doxygen, change to `docs/`, and run:

```bash
doxygen
doxygen Doxyfile-cpp
doxygen Doxyfile-python
```

The generated HTML is placed in `docs/html`.

## License

The repository includes the Apache License, Version 2.0, in `LICENSE`. Review that file for the terms governing use, reproduction, and distribution. Check the terms applicable to third-party dependencies and model assets separately where relevant.

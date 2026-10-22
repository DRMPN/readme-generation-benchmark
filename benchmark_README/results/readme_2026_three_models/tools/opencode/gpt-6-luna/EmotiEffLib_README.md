# EmotiEffLib

EmotiEffLib is a library for facial emotion and engagement recognition in images and videos. The repository contains a Python API and a C++ library (`emotieffcpplib`). Both provide emotion inference with Torch/LibTorch and ONNX Runtime backends; engagement prediction is also available through the APIs.

The recognizers process **face images**. Face detection and tracking are not part of the Python recognizer API, so detect and crop faces in your application before passing them in. The tutorials demonstrate image and video workflows.

## Python

### Install

The base installation includes ONNX Runtime support. Install from the repository root:

```sh
pip install .
```

Optional dependencies add other features:

```sh
pip install '.[torch]'        # Torch inference
pip install '.[engagement]'    # TensorFlow-based engagement inference
pip install '.[all]'           # Both optional dependency groups
```

The `torch` extra installs Torch and torchvision. The `engagement` extra installs TensorFlow and tf2onnx. Use a compatible framework build for your hardware if you need a specific accelerator configuration.

### Predict emotion

```python
import cv2
from emotiefflib.facial_analysis import EmotiEffLibRecognizer

# Supply a cropped face as an RGB NumPy image.
face_bgr = cv2.imread("face.jpg")
face_rgb = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB)

recognizer = EmotiEffLibRecognizer(
    engine="torch",  # or "onnx"
    model_name="enet_b0_8_best_vgaf",
    device="cpu",    # Torch can also use "cuda" when available
)
labels, scores = recognizer.predict_emotions(face_rgb, logits=False)
print(labels[0], scores)
```

`predict_emotions` accepts one NumPy image or a list of NumPy images and returns predicted label(s) and a NumPy array of scores. By default, `logits=True` returns raw scores; with `logits=False`, emotion scores are softmax-normalized. `extract_features` and `classify_emotions` are available when feature extraction and classification need to be performed separately.

The built-in model names are:

- `enet_b0_8_best_vgaf`
- `enet_b0_8_best_afew`
- `enet_b2_8`
- `enet_b0_8_va_mtl`
- `enet_b2_7`
- `mbf_va_mtl`
- `mobilevit_va_mtl`

The implementation downloads selected model files on first use and caches them under `~/.emotiefflib`.

### Predict engagement

Engagement prediction operates on a sequence of face images or extracted features. It requires the `engagement` extra (TensorFlow), and the default sliding-window width is 128 frames. For example:

```python
labels, scores = recognizer.predict_engagement(face_frames)
```

`face_frames` should be a list of face-image NumPy arrays. The model expects 2560-dimensional features; the current engagement tests exercise `enet_b0` models. Engagement is not a single-image prediction.

### Python tests and tutorials

Tests use pytest. Install `tests/requirements.txt`, download and unpack the test data, then run pytest from the repository root:

```sh
pip install -r tests/requirements.txt
cd tests
./download_test_data.sh
tar -xzf data.tar.gz
cd ..
pytest tests
```

The test dataset is downloaded separately. Python notebooks for single-image emotion recognition, video emotion recognition, and video emotion-and-engagement prediction are in [`docs/tutorials/python`](docs/tutorials/python/README.md).

## C++ library

The C++ implementation is in [`emotieffcpplib`](emotieffcpplib/README.md). It requires C++17, CMake 3.10.2 or later, OpenCV, and at least one of LibTorch or ONNX Runtime. The CMake options `WITH_TORCH` and `WITH_ONNX` take the respective library directory paths; `BUILD_TESTS` enables unit tests and `BUILD_SHARED_LIBS` selects a shared library instead of the default static library.

Initialize the repository's submodules, then configure and build from the C++ library directory. Provide at least one inference backend:

```sh
git submodule update --init --recursive
cmake -S emotieffcpplib -B build \
  -DWITH_TORCH=/path/to/libtorch \
  -DWITH_ONNX=/path/to/onnxruntime
cmake --build build --parallel
```

The C++ API is declared in `emotieffcpplib/include/emotiefflib/facial_analysis.h`. Model preparation utilities are in `models/prepare_models_for_emotieffcpplib.py`; see the [C++ library README](emotieffcpplib/README.md) and [C++ tutorials](docs/tutorials/cpp/README.md) for setup and usage details. The C++ tests require `-DBUILD_TESTS=ON` and test data; see the library README.

## More resources

- [Python tutorials](docs/tutorials/python/README.md)
- [C++ tutorials](docs/tutorials/cpp/README.md)
- [Training and examples](training_and_examples/README.md)
- [Doxygen documentation instructions](docs/README.md)

## License

This repository is released under the [Apache License 2.0](LICENSE).

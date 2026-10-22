# EmotiEffLib

EmotiEffLib is a library for facial emotion recognition and engagement recognition in images and
videos. It provides implementations in **Python** ([`emotiefflib`](emotiefflib)) and **C++**
([`emotieffcpplib`](emotieffcpplib)), and supports multiple inference engines: ONNX Runtime and
PyTorch in Python, ONNX Runtime and Libtorch in C++.

The library extracts features from cropped face images and classifies them into emotions
(7 or 8 classes, depending on the model) and engagement (`Engaged` / `Distracted`).

## Features

- **Two implementations**: Python package `emotiefflib` and C++ library `emotieffcpplib`
- **Two inference engines** in each implementation (PyTorch/Libtorch and ONNX Runtime)
- **Seven pre-trained models** for facial emotion recognition (`get_model_list()`)
- **Engagement recognition** over a video sequence using a sliding window of feature vectors
- **Automatic model download**: weights are fetched from this repository on first use and cached in
  `~/.emotiefflib`
- Face detection is *not* included: the recognizers expect cropped face images (the bundled
  tutorials and tests crop faces with MTCNN before calling the library)

## Installation

### Python

Install from PyPI with one of the following variants:

```sh
pip install emotiefflib                    # ONNX Runtime support only
pip install emotiefflib[torch]             # ONNX Runtime + PyTorch
pip install emotiefflib[engagement]        # ONNX Runtime + TensorFlow (needed for engagement)
pip install emotiefflib[all]               # everything
```

Or install from a clone of this repository:

```sh
python setup.py install
```

Python 3.10 is used in the CI and Binder environments.

### C++

The C++ library requires C++17, CMake 3.10.2 or later, OpenCV, and at least one inference engine
(Libtorch or ONNX Runtime). To build it, clone the repository with submodules, download one of the
engines, and configure CMake:

```sh
git clone https://github.com/sb-ai-lab/EmotiEffLib.git
cd EmotiEffLib
git submodule update --init --recursive

mkdir build && cd build
cmake .. -DWITH_TORCH=/path/to/libtorch -DWITH_ONNX=/path/to/onnxruntime
make -j$(nproc)
```

CMake options: `WITH_TORCH`, `WITH_ONNX` (at least one is required), `BUILD_TESTS` (GoogleTest),
`BUILD_SHARED_LIBS`. Full details are in [`emotieffcpplib/README.md`](emotieffcpplib/README.md).

## Usage

### Python

```python
from emotiefflib.facial_analysis import EmotiEffLibRecognizer, get_model_list

model_name = get_model_list()[0]

# engine: "torch" or "onnx"; device: "cpu" or "cuda" (torch engine only)
fer = EmotiEffLibRecognizer(engine="onnx", model_name=model_name, device="cpu")

# face_img is a NumPy RGB image (H, W, 3) or a list of such images
emotions, scores = fer.predict_emotions(face_img, logits=True)

# For a video sequence of face images (needs at least 128 frames by default):
engagement, scores = fer.predict_engagement(face_imgs)
```

### C++

The C++ API (`EmotiEffLibRecognizer::createInstance` in
[`emotieffcpplib/include/emotiefflib/facial_analysis.h`](emotieffcpplib/include/emotiefflib/facial_analysis.h))
mirrors the Python one; usage examples are in the
[C++ tutorials](docs/tutorials/cpp/README.md).

## Available models

| Model name          | Emotion classes | Input size | Notes                                   |
| ------------------- | --------------- | ---------- | --------------------------------------- |
| `enet_b0_8_best_vgaf` | 8               | 224        | default model in the Python API         |
| `enet_b0_8_best_afew` | 8               | 224        |                                         |
| `enet_b2_8`           | 8               | 260        |                                         |
| `enet_b0_8_va_mtl`    | 8               | 224        | multi-task (`_mtl`): 2 extra output scores |
| `enet_b2_7`           | 7               | 260        |                                         |
| `mbf_va_mtl`          | 8               | 112        | multi-task (`_mtl`): 2 extra output scores |
| `mobilevit_va_mtl`    | 8               | 224        | multi-task (`_mtl`): 2 extra output scores |

The 7-class set is: Anger, Disgust, Fear, Happiness, Neutral, Sadness, Surprise. The 8-class set
adds Contempt. In multi-task (`_mtl`) models the output scores include two additional values that
are excluded from emotion classification.

The pre-trained weights live in [`models/affectnet_emotions`](models/affectnet_emotions) (Torch and
ONNX formats) and are downloaded automatically at runtime; some additional models are available on
[Google Drive](https://drive.google.com/drive/folders/1eBIIooLKnHoHYfbnJmNZlEHyOkckFif1?usp=sharing).

## Tutorials

Jupyter notebooks that demonstrate the library step by step are available for both languages:

- [Python tutorials](docs/tutorials/python/README.md): one-image emotion recognition, emotions on
  video, engagement and emotions on video
- [C++ tutorials](docs/tutorials/cpp/README.md): the same examples run with the C++ implementation
  through the xeus-cling kernel

The notebooks can also be run interactively via Binder (the `.binder/` directory contains the
environment definition, and MyBinder builds are triggered from `main` by CI).

## Training and examples

The [`training_and_examples`](training_and_examples) directory contains Jupyter notebooks and
scripts used to train and evaluate the models, including:

- training of the EmotiEffNet models and AFEW/VGAF emotion classifiers
  ([`affectnet`](training_and_examples/affectnet)), and ABAW challenge experiments
  ([`ABAW`](training_and_examples/ABAW))
- personalized engagement models ([`personalized_models`](training_and_examples/personalized_models))
- an emotional multiagent dialogue demo ([`emotions_llm`](training_and_examples/emotions_llm))

## Running tests

**Python** (pytest):

```sh
pip install -r tests/requirements.txt
cd tests && ./download_test_data.sh && tar -xzf data.tar.gz && cd -
pytest tests
```

**C++** (GoogleTest): build with `-DBUILD_TESTS=ON`, download the test data as above, and run
`./<build_dir>/bin/unit_tests` with `EMOTIEFFLIB_ROOT` pointing to the repository root. Details are
in [`emotieffcpplib/README.md`](emotieffcpplib/README.md).

## Documentation

Doxygen configuration files (`Doxyfile`, `Doxyfile-cpp`, `Doxyfile-python`) are located in
[`docs`](docs). Run `doxygen`, `doxygen Doxyfile-cpp` and `doxygen Doxyfile-python` in that
directory to generate HTML documentation.

## License

The code of EmotiEffLib is released under the [Apache-2.0 License](LICENSE). There is no limitation
for both academic and commercial usage.

## Authors

Andrey Savchenko and Egor Churaev
([sb-ai-lab/EmotiEffLib](https://github.com/sb-ai-lab/EmotiEffLib))
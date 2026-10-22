# EmotiEffLib-x3pex2ph

---

[![PyPi](https://badge.fury.io/py/emotiefflib.svg)](https://badge.fury.io/py/emotiefflib)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

EmotiEffLib is a software development kit for facial emotion recognition in images and video, providing both a Python package and a C++ library with a common interface. Pre-trained model weights are bundled, and inference can run through pluggable backends based on PyTorch or ONNX Runtime, with additional support for engagement (distracted/engaged) classification on video sequences. The repository targets ML and computer-vision researchers, application developers integrating emotion recognition into C++ or Android projects, and data scientists studying the training flows. Alongside the two core libraries, the repository offers tutorial notebooks, training and evaluation workflows, and mobile demo applications. Newcomers should consult the Getting Started section for runnable steps and pointers to tutorials for both languages.

---

## Core Features

* **Dual-Language Core:** Provides a unified library interface supporting both Python and C++, enabling seamless integration into data science pipelines and high-performance native applications.
* **Pluggable Inference Backends:** Offers deployment flexibility by supporting multiple runtimes, including PyTorch and ONNX Runtime, for optimized operation in diverse environments.
* **Facial Affect Recognition:** Facilitates the accurate identification of facial emotions and continuous assessment of viewer engagement using bundled pre-trained model weights.
* **Comprehensive Development Ecosystem:** Includes detailed training notebooks, examples, and mobile application demos to accelerate research, testing, and practical implementation of the library.

---

## Installation

Install EmotiEffLib-x3pex2ph using one of the following methods:

**Using PyPi:**

```sh
pip install emotiefflib
```

---

## Getting Started

### Prerequisites

Before starting, ensure you have the necessary environment set up. The primary interfaces support both Python (PyTorch/ONNX) and C++17.

**Python:**
*   Python 3.10+ is recommended.
*   Install the package via pip (refer to setup documentation for specifics).

**C++:**
*   CMake (3.10.2+) is required.
*   OpenCV and at least one inference backend (LibTorch or ONNX Runtime) must be available.

### Quickstart (Python)

To run a minimal inference pipeline, install the package and execute a tutorial notebook. The library exposes model functions like `classify_emotions`.

1.  **Installation:**
```bash
pip install emotiefflib # Assuming standard install command
```
2.  **Execution:**
    Refer to the Jupyter notebooks located in `docs/tutorials/python` to see step-by-step usage examples.

### Quickstart (C++) 

For C++ integration, you must configure the build to include a supported inference engine.

1.  **Configure Build:**
    Use CMake and specify either the `--WITH_TORCH` or `--WITH_ONNX` flag, pointing to the respective engine directory.
```bash
cmake -B build -DWITH_TORCH=/path/to/libtorch 
# OR 
cmake -B build -DWITH_ONNX=/path/to/onnxruntime
```
2.  **Build the Library:**
```bash
cmake --build build
```
3.  **Tutorials:**
    Use the examples in `docs/tutorials/cpp` to understand the C++ factory pattern and model loading.

---

## API Reference

This library exposes several APIs across Python (`emotiefflib`) and C++ (`emotieffcpplib`) to handle facial emotion and engagement recognition.

**Python Module API (emotiefflib)**

*   **`EmotiEffLibRecognizerBase`** (Abstract Class)
    *   `extract_features(face_img)`: Extracts visual features from a single or list of facial images.
    *   `classify_emotions(features, logits)`: Classifies emotions based on extracted feature vectors. Returns labels and model scores (logits or probabilities).
    *   `classify_engagement(features, sliding_window_width)`: Classifies engagement levels from a video sequence using a sliding window approach.
*   **`get_engagement_model(feature_vector_dim, number_of_frames)`**: Loads and returns the Keras model instance for engagement classification.

**C++ Core API (emotieffcpplib)**

*   **`EmotiEffLibRecognizer::createInstance(backend, path)` / `createInstance(config)`**: Factory methods used to create recognizer instances, supporting different inference backends (e.g., Torch, ONNX).
*   **`EmotiEffLibRecognizer::extractFeatures(faceImgs)`**: Extracts features from a vector of input OpenCV face images.
*   **`EmotiEffLibRecognizer::predictEmotions(faceImgs, logits)`**: Predicts emotions for a vector of input face images.
*   **`EmotiEffLibRecognizer::processEmotionScores(score, logits)`**: Post-processes raw emotion scores to determine final predictions (including softmax normalization if required).
*   **`EmotiEffLibRecognizer::processEngagementScores(score)`**: Processes raw engagement scores into prediction labels.

---

## Examples

Examples of how this should work and how it should be used are available [here](./docs/tutorials).

---

## Documentation

A detailed EmotiEffLib-x3pex2ph description is available [here](./docs).

---

## Contributing

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). EmotiEffLib-x3pex2ph repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{EmotiEffLib-x3pex2ph,

        author = {README Benchmark},

        title = {EmotiEffLib-x3pex2ph repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
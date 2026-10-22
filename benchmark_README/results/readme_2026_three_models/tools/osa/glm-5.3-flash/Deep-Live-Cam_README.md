# Deep-Live-Cam-tpzyno3v

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![onnx](https://img.shields.io/badge/ONNX-005CED.svg?style={0}&logo=ONNX&logoColor=white)
![tensorflow](https://img.shields.io/badge/TensorFlow-FF6F00.svg?style={0}&logo=TensorFlow&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Deep-Live-Cam-tpzyno3v is a Python-based media processing tool for real-time and offline face swapping in images, videos, and live camera streams. It targets developers, researchers, and data scientists who need configurable, machine-learning-driven face processing workflows. The project provides both a command-line interface for headless, parameter-driven runs and a graphical interface for interactive use, including a live webcam mode. Newcomers should consult the Getting Started section for installation and runnable steps.

---

## Core Features

- **Real-time face swap from webcam or files** — swap a face from a source image onto live camera feeds, images, or videos, enabling instant previews and batch media processing.
- **Configurable frame processing pipeline** — combine processors such as face swapping and face enhancement to tailor output quality per run.
- **Multi-face and face mapping support** — detect and swap every face in a frame, or map specific source faces to specific target faces for precise control in crowded scenes.
- **Mouth masking and color correction** — preserve natural mouth movement with adjustable mask region controls, and correct color spaces for more accurate results.
- **CLI and GUI with flexible output options** — run headless via command-line arguments or through a desktop interface, with control over encoders, quality, FPS, audio, execution providers, and memory limits.

---

## Installation

Install Deep-Live-Cam-tpzyno3v using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/Deep-Live-Cam-tpzyno3v
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

**Prerequisites**

- A Python 3 environment with the project's dependencies installed (the code imports PyTorch, TensorFlow, ONNX Runtime, `insightface`, OpenCV (`cv2`), and `customtkinter`).
- A source image containing a face.
- A target image (`*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.bmp`) or video (`*.mp4`, `*.mkv`).

**Steps**

1. Verify the installation (prints the application name and version):

```bash
   python run.py -v
```

2. Start the graphical interface — the default when no `-s`/`-t`/`-o` arguments are given:

```bash
   python run.py
```

   Select a source face and a target image or video in the window, then start.

3. Alternatively, run headless from the command line by passing source, target, and output:

```bash
   python run.py -s <source_image> -t <target_image_or_video> -o <output_path>
```

4. Tune the run with optional flags (full set defined in `modules/core.py`):

   - `--frame-processor face_swapper face_enhancer` — processor pipeline (default: `face_swapper`).
   - `--execution-provider cuda` — execution provider (default: `cpu`).
   - `--many-faces` — process every face in the target.

The face swapper requires the `inswapper_128_fp16.onnx` model, downloaded from HuggingFace via `conditional_download` (see `modules/processors/frame/face_swapper.py`).

---

## Architecture

The application is a modular Python pipeline with a thin entry point and clearly separated subsystems:

- **Entry point (`run.py`)**: Delegates immediately to `modules.core.run()`, which parses CLI arguments, populates shared settings, and orchestrates execution.
- **Shared state (`modules/globals.py`)**: A central module holding runtime configuration (paths, frame processors, execution providers/threads, encoder settings, toggles) read by all other components.
- **Core orchestration (`modules/core.py`)**: Handles argument parsing (including deprecated-arg translation), headless vs. GUI mode selection, and drives the overall image/video workflow using utilities for frame extraction, video creation, audio restoration, and temp-file management (`modules/utilities.py`).
- **Frame processors (`modules/processors/frame/`)**: A pluggable pipeline selected via `--frame-processor` (e.g., `face_swapper`, `face_enhancer`), resolved by `modules/processors/frame/core.get_frame_processors_modules`. Each processor implements a common interface (pre-check, pre-start, per-frame processing).
- **Face analysis & mapping (`modules/face_analyser.py`, `modules/cluster_analysis.py`)**: Detects source/target faces and, in mapped mode, matches multiple faces using embedding centroid comparison.
- **UI (`modules/ui.py`, `modules/video_capture.py`, `modules/capturer.py`)**: A CustomTkinter GUI providing source/target selection, previews, live webcam mode, and face mapping popups; it shares the same `modules.globals` state as the CLI path.
- **Inference backends**: Models (e.g., `inswapper_128_fp16.onnx` under `models/`) run through insightface/ONNX Runtime with configurable execution providers (CPU, CUDA, ROCm, CoreML, DirectML), with PyTorch/TensorFlow used by supporting components.

Control flow: user input (CLI or GUI) → validated settings in `modules.globals` → target media split into temp frames → frame processors applied per frame (multi-threaded) → frames reassembled into output video/audio via utilities.

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to Deep-Live-Cam-tpzyno3v.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Deep-Live-Cam-tpzyno3v repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Deep-Live-Cam-tpzyno3v,

        author = {README Benchmark},

        title = {Deep-Live-Cam-tpzyno3v repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
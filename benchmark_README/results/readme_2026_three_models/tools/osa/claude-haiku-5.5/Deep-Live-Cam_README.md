# Deep-Live-Cam-33zc4mp2

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

Deep-Live-Cam is a Python application for swapping faces in images and videos, using face analysis and a face-swap model to replace a face in a target image or video with a face from a source image. It is aimed at developers and technically capable end-users who are comfortable configuring Python dependencies, model files, and GPU or other execution backends. The project offers both a command-line interface for scripted or headless processing and a graphical user interface for interactive use. For runnable setup and usage steps, see the Getting Started section.

---

## Core Features

- **Image and video face swapping:** Swaps a source face onto faces in a target image or video, so developers can produce face-swapped media from a single command.
- **Command-line and UI operation:** Runs headless from command-line arguments for source, target, and output paths, or interactively through a graphical interface, which suits both scripted and manual workflows.
- **Selectable execution providers:** Lets developers choose the compute backend (such as CPU, CUDA, CoreML, or ROCm) to match their hardware.
- **Frame-based video processing:** Processes video frames in parallel on a thread pool and reports progress, which speeds up work on longer videos.
- **Pluggable frame processors:** Loads frame processors dynamically through a fixed interface, so developers can add or swap processing steps without changing the core pipeline.

---

## Installation

Install Deep-Live-Cam-33zc4mp2 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/Deep-Live-Cam-33zc4mp2
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

### Prerequisites

- Python with the dependencies listed in `requirements.txt`. Exact versions are not specified in the provided context.
- The face swap model `inswapper_128_fp16.onnx`. The face swapper loads it from the `models/` directory.

### Steps

1. Install the Python dependencies listed in `requirements.txt`.
2. Confirm the CLI is available and review the available options:

```bash
python run.py --help
```

3. Run a headless face swap by supplying a source image, a target image or video, and an output path:

```bash
python run.py -s source.jpg -t target.mp4 -o output.mp4
```

Supplying `-s`, `-t`, or `-o` enables headless mode. Replace the file names with your own inputs.

4. To select an execution provider, add `--execution-provider` with one of the values accepted by the CLI, for example:

```bash
python run.py -s source.jpg -t target.mp4 -o output.mp4 --execution-provider cpu
```

### Windows

The repository includes Windows batch launchers `run-cuda.bat` and `run-directml.bat` as existing entry points.

---

## Architecture

The application is a Python command-line and UI tool with a modular, plugin-style frame processing pipeline.

- **Entry point:** `run.py` imports `modules/core.py` and calls `core.run()`. `core.py` parses CLI arguments and sets shared options. If source, target, or output paths are provided, the tool runs in headless mode. Otherwise, it uses the UI in `modules/ui.py`.
- **Shared state:** Runtime options are stored in `modules/globals.py` and read by the core, processor, and analysis modules.
- **Frame processor plugins:** `modules/processors/frame/core.py` loads processors with `importlib` from `modules/processors/frame/`. Each processor must expose `pre_check`, `pre_start`, `process_frame`, `process_image`, and `process_video`. Processors include `face_swapper` and `face_enhancer`.
- **Face analysis and swapping:** `modules/face_analyser.py` uses insightface `FaceAnalysis` (`buffalo_l`). `modules/processors/frame/face_swapper.py` loads `inswapper_128_fp16.onnx` from the `models` directory through insightface `model_zoo`.
- **Execution backends:** The `--execution-provider` option sets the providers passed to insightface and ONNX Runtime. The `--execution-threads` option sets the worker count for frame processing.
- **Frame processing flow:** Video frames are extracted to temporary files and processed in parallel with `ThreadPoolExecutor` in `multi_process_frame`. Progress is reported with `tqdm`. Frames are then reassembled into the output video with OpenCV-based utilities in `modules/utilities.py`.

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to Deep-Live-Cam-33zc4mp2.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Deep-Live-Cam-33zc4mp2 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Deep-Live-Cam-33zc4mp2,

        author = {README Benchmark},

        title = {Deep-Live-Cam-33zc4mp2 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
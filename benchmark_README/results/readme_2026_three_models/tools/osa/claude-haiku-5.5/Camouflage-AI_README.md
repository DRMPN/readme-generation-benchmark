# Camouflage-AI-y6jmr6rk

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Camouflage AI is a desktop application that removes video backgrounds using AI-based person segmentation. It replaces everything behind the detected person with a solid color, a selected image, or a blur effect, and saves the result as an MP4 video. The primary audience is end users on Windows who want a graphical tool for this task, with developers as a secondary audience. It is a standalone graphical application rather than a hosted service, so for installation and running steps, see the Getting Started section.

---

## Core Features

- **Automatic person segmentation:** Detects and isolates people in each video frame using YOLOv8 segmentation, so no manual masking is required.
- **Flexible background replacement:** Replaces the detected background with a solid color, a custom image, or a blur effect, letting you adjust the look without external editing tools.
- **MP4 video output:** Writes the processed frames to an MP4 file, providing a ready-to-use result after each run.
- **Non-blocking processing with progress reporting:** Runs video processing on a background thread and reports progress through a callback, keeping the desktop interface responsive during long jobs.
- **GPU acceleration with CPU fallback:** Uses CUDA when available and falls back to CPU otherwise, allowing the tool to run on machines without a compatible GPU.

---

## Installation

**Prerequisites:** requires Python >=3.8

Install Camouflage-AI-y6jmr6rk using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/Camouflage-AI-y6jmr6rk
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

### Prerequisites

- Windows (the project metadata lists Microsoft Windows as the operating system)
- Python 3.8 or later (`python_requires='>=3.8'` in `setup.py`)
- Dependencies, installed as described in the [Installation](#installation) section

### Steps

1. **Install the core dependencies.** See the [Installation](#installation) section. `requirements.txt` lines are prefixed with `pip install`, which is not standard requirements-file syntax. Review that file before using it.
2. **Install `ultralytics` and `torch`.** Both are imported by `process_video.py` but are not listed in `setup.py` or `requirements.txt`. Follow the [Installation](#installation) section for this step.
3. **Model.** `process_video.py` loads the model by name, `YOLO('yolov8n-seg.pt')`, and uses the person class (`classes=[0]`). A code comment notes that `yolov8x-seg.pt` can be used on a powerful GPU for higher accuracy.
4. **Start the application** from the repository directory:

```bash
python "Camouflage AI.py"
```

5. **Process a video** in the window:
   - Click **Select Video**.
   - Choose a background type: **Color**, **Image**, or **Blur**. For **Image**, click **Select Image**.
   - Click **Start Processing**.
   - Click **Show Output Folder** to open the output location.

### Output

Each processed video is written as an MP4 file named `<input_name>_<bg_type>_bg.mp4` in the output folder passed to `run_yolo_background_removal`. The default output folder is not specified in the repository evidence.

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Camouflage-AI-y6jmr6rk repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Camouflage-AI-y6jmr6rk,

        author = {README Benchmark},

        title = {Camouflage-AI-y6jmr6rk repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
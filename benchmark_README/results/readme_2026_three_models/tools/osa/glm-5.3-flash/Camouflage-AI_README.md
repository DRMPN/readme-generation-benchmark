# Camouflage-AI-x8kz7kp_

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

Camouflage AI is a Windows desktop application that removes and replaces video backgrounds automatically. It applies AI-based person segmentation to each frame of a video, allowing the detected person to be composited onto a solid color, a custom image, or a blurred version of the original scene. The tool is written in Python and runs on a GPU when one is available, falling back to CPU otherwise. It targets users and developers who want a simple, GUI-driven way to change video backgrounds without manual editing. See Getting Started for installation and first-run instructions.

---

## Core Features

- **AI-powered background removal** — Segments people in each frame with YOLOv8 so the original video background is removed automatically.
- **Three background replacement modes** — Swap in a solid color picked in-app, a custom image scaled to the video's resolution, or a blurred version of the original scene.
- **One-window workflow** — Select a video, choose the background style, start processing, and open the output folder from a single desktop interface.
- **Non-blocking processing** — Video processing runs in a background thread with live progress updates, keeping the interface responsive while a video renders.
- **Automatic device selection** — Processing uses a CUDA GPU when available and falls back to CPU, so it runs on machines without dedicated graphics hardware.

---

## Installation

**Prerequisites:** requires Python >=3.8

Install Camouflage-AI-x8kz7kp_ using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/Camouflage-AI-x8kz7kp_
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

### Prerequisites

- Python 3.8 or later. The packaging metadata targets Windows, so Windows is the expected platform.
- The dependencies listed in `requirements.txt`. Packages imported by the code but not listed in that file — such as `torch` and `ultralytics` — may need to be installed separately.
- A CUDA-capable GPU is optional: the processing device (GPU or CPU) is selected automatically at runtime.

### Steps

1. Install the dependencies from `requirements.txt` (the file contains one `pip install <package>` line per package).

2. Launch the desktop GUI from the repository root:

```bash
   python "Camouflage AI.py"
```

3. Select an input video in the application window.

4. Choose a background type — solid color, image, or blur — and pick a color or a background image if the selected type requires one.

5. Start processing. The video is processed in a background thread using the `yolov8n-seg.pt` segmentation model, automatically on a CUDA GPU when available and on CPU otherwise. Status updates are shown in the application window.

6. When processing completes, open the output folder from the application to view the result: an `.mp4` video named after the input file and the chosen background type, e.g. `<video-name>_color_bg.mp4`.

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Camouflage-AI-x8kz7kp_ repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Camouflage-AI-x8kz7kp_,

        author = {README Benchmark},

        title = {Camouflage-AI-x8kz7kp_ repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
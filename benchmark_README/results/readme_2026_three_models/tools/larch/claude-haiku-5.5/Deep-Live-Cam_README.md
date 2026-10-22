# Deep-Live-Cam

> Real-time face swap and video deepfake tool that needs only a single source image.

Deep-Live-Cam lets you replace the face of a person in a live webcam feed, or in a target image or video, using one reference photo. It includes a graphical interface, command-line execution, optional face enhancement, and support for GPU acceleration on NVIDIA (CUDA) and Windows (DirectML) hardware.

---

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Ethical Use and Disclaimer](#ethical-use-and-disclaimer)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Downloading the Models](#downloading-the-models)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Command-Line Options](#command-line-options)
- [Hardware Acceleration](#hardware-acceleration)
- [Localization](#localization)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Demo

The repository includes several demonstration animations:

| File | Description |
|------|-------------|
| `demo.gif` | General overview of the face swap in action |
| `live_show.gif` | Live webcam face swapping |
| `streamers.gif` | Use case for streamers |
| `movie.gif` | Swapping faces in video footage |
| `ludwig.gif` | Example of the swap on a target video |
| `meme.gif` | Example of a meme-style use |
| `avgpcperformancedemo.gif` | Performance on an average PC |
| `deepwarebench.gif` | Benchmark results |

---

## Features

- **Real-time face swapping** from a webcam feed, with a single source image.
- **Offline swapping** on images and videos, with output saved to disk.
- **Multi-face support**, including swapping all detected faces or mapping specific faces to specific sources.
- **Face enhancement** with a GFPGAN-based enhancer to improve output sharpness.
- **Mouth mask** option to better preserve the original mouth and teeth.
- **Frame processors** as pluggable modules (face swapper, face enhancer).
- **Hardware acceleration** through CUDA (NVIDIA), DirectML (Windows), and CPU fallback.
- **Graphical user interface** for selecting sources, targets, and options, with live preview.
- **Multilingual interface** with translations in German, Spanish, Finnish, Russian, Chinese, Korean, Brazilian Portuguese, Khmer, and Thai.
- **Content filtering** through an optional NSFW predictor module.
- **Audio preservation** when processing videos.
- **Windows launch scripts** for CUDA and DirectML.

---

## Ethical Use and Disclaimer

This software can create realistic synthetic media of real people. Misuse can cause serious harm, including fraud, harassment, non-consensual imagery, and disinformation.

**By using this software, you agree to:**

- Obtain explicit consent from anyone whose face you use.
- Never create sexual, defamatory, or harassing content using someone's likeness without consent.
- Clearly label generated or manipulated content when sharing it publicly.
- Comply with all applicable laws, including those on deepfakes, privacy, and likeness rights.
- Not use the software to deceive people in political, financial, or legal contexts.

The developers and contributors take no responsibility for misuse. Use this software responsibly.

---

## Project Structure

The project is organized as follows (inferred from the repository contents):

```
Deep-Live-Cam/
├── run.py                    # Main entry point
├── requirements.txt          # Python dependencies
├── run-cuda.bat              # Windows launcher for NVIDIA CUDA
├── run-directml.bat          # Windows launcher for DirectML
├── mypi.ini                  # Mypy type-checking configuration
├── instructions.txt          # Short setup/usage notes
├── ui.json                   # UI layout/text configuration
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # Project license
│
├── *.json                    # Translation files (de, es, fi, ru, zh, ko,
│                             #   pt-br, km, th)
│
├── modules/                  # Core application logic
│   ├── core.py               # Main processing pipeline and startup logic
│   ├── globals.py            # Shared global settings and state
│   ├── ui.py                 # Graphical user interface
│   ├── capturer.py           # Frame capture helpers
│   ├── video_capture.py      # Webcam/video input handling
│   ├── face_analyser.py      # Face detection and recognition
│   ├── cluster_analysis.py   # Face clustering for multi-face handling
│   ├── predicter.py          # Optional content filter (NSFW prediction)
│   ├── gettext.py            # Translation/localization handling
│   ├── metadata.py           # Application name, version, and metadata
│   ├── typing.py             # Shared type definitions
│   ├── utilities.py          # General helper functions
│   │
│   └── processors/
│       └── frame/
│           ├── core.py           # Frame processor loader/base logic
│           ├── face_swapper.py   # Face swapping processor
│           └── face_enhancer.py  # Face enhancement processor (GFPGAN)
│
├── models/                   # Downloaded model files (you must add these)
│
└── *.gif                     # Demo animations
```

**Key files:**

- **`run.py`**: Parses command-line arguments and launches the GUI or headless processing.
- **`modules/globals.py`**: Stores configuration such as selected source, target, output path, execution providers, and option flags.
- **`modules/face_analyser.py`**: Detects faces and extracts embeddings used for matching.
- **`modules/processors/frame/face_swapper.py`**: Performs the swap using the inswapper model.
- **`modules/processors/frame/face_enhancer.py`**: Optionally refines the swapped face.
- **`modules/ui.py`** and **`ui.json`**: Build the GUI and define its labels and layout.

> **Note:** The exact directory layout is inferred from the file listing. Check the repository for the precise paths if they differ.

---

## Requirements

### Software

- **Python 3.10** (recommended). Newer versions may have dependency incompatibilities.
- **Git** (to clone the repository).
- **FFmpeg** (required for video processing and audio handling).
- **Visual C++ Redistributable** (Windows, if you encounter DLL errors).

### Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Modern quad-core | 8+ cores |
| GPU | Any (CPU fallback) | NVIDIA GPU with 6+ GB VRAM |
| RAM | 8 GB | 16 GB+ |
| Storage | 5 GB free | 10 GB+ free (for video output) |

Real-time performance depends heavily on GPU availability. Without a supported GPU, expect significantly lower frame rates.

### Python Dependencies

All dependencies are listed in `requirements.txt`. They typically include:

- `insightface` (face analysis and swapping)
- `onnxruntime` / `onnxruntime-gpu` / `onnxruntime-directml`
- `opencv-python`
- `numpy`
- `customtkinter` or a similar UI library
- `torch` and `torchvision` (for the enhancer and related features)
- `pillow`
- `tqdm`
- `psutil`

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/hacksider/Deep-Live-Cam.git
cd Deep-Live-Cam
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For GPU acceleration, install the matching runtime after the base requirements:

- **NVIDIA CUDA:** `pip install onnxruntime-gpu`
- **Windows DirectML:** `pip install onnxruntime-directml`

Make sure only one ONNX Runtime variant is installed, or the wrong provider may load.

### 4. Install FFmpeg

- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` folder to your `PATH`. Or use `winget install ffmpeg`.
- **macOS:** `brew install ffmpeg`
- **Linux (Debian/Ubuntu):** `sudo apt install ffmpeg`

Verify the installation:

```bash
ffmpeg -version
```

---

## Downloading the Models

The face swap and enhancement models are not included in the repository. Download them and place them in the `models/` directory.

| Model | Purpose | File name |
|-------|---------|-----------|
| Inswapper | Face swapping | `inswapper_128_fp16.onnx` (or `inswapper_128.onnx`) |
| GFPGAN | Face enhancement (optional) | `GFPGANv1.4.pth` (or the ONNX variant) |
| Face analysis | Detection and recognition | Downloaded automatically by InsightFace on first run |

After downloading, your folder should look like this:

```
models/
├── inswapper_128_fp16.onnx
└── GFPGANv1.4.pth
```

Only download models from sources you trust, and verify their checksums where available.

---

## Running the Application

### Windows (recommended)

Use the provided batch files:

- **NVIDIA GPU:** double-click `run-cuda.bat`
- **Any DirectX 12 GPU (AMD, Intel, NVIDIA):** double-click `run-directml.bat`

### Command line

```bash
python run.py
```

Running without arguments opens the graphical interface.

---

## Usage Guide

### Using the graphical interface

1. **Select a source image.** Choose a clear, front-facing photo of the face you want to apply.
2. **Select a target.** Choose either a webcam (for live mode) or an image/video file (for offline mode).
3. **Choose options** such as face enhancer, mouth mask, keep FPS, keep audio, or many-faces mode.
4. **Click Preview** to check the result before processing.
5. **Click Start (Live)** for real-time webcam swapping, or **Start** to process a file and save the output.

### Tips for better results

- Use a **well-lit, high-resolution, front-facing** source image.
- Make sure the target face is **not too small** or heavily occluded.
- Enable **Face Enhancer** for sharper output, at the cost of speed.
- Enable **Mouth Mask** if the mouth or teeth look distorted during speech.
- Close other GPU-heavy applications to free VRAM.
- For live mode, lower the webcam resolution if the frame rate is too low.

---

## Command-Line Options

Run `python run.py --help` to see the full list for your version. Common options include:

| Option | Description |
|--------|-------------|
| `-s, --source` | Path to the source face image |
| `-t, --target` | Path to the target image or video |
| `-o, --output` | Path for the output file |
| `--frame-processor` | Processors to use, e.g. `face_swapper face_enhancer` |
| `--keep-fps` | Keep the original video frame rate |
| `--keep-audio` | Keep the original audio track |
| `--keep-frames` | Keep intermediate frames on disk |
| `--many-faces` | Swap all detected faces |
| `--mouth-mask` | Preserve the original mouth region |
| `--video-encoder` | Video codec, e.g. `libx264`, `libx265` |
| `--video-quality` | Output quality setting |
| `--execution-provider` | Hardware backend: `cpu`, `cuda`, `dml`, `coreml` |
| `--execution-threads` | Number of worker threads |
| `--max-memory` | Maximum RAM/VRAM to use (GB) |

### Example commands

Swap a face in an image:

```bash
python run.py -s source.jpg -t target.jpg -o output.jpg --frame-processor face_swapper
```

Swap a face in a video, keeping FPS and audio, with enhancement:

```bash
python run.py -s source.jpg -t video.mp4 -o result.mp4 \
    --frame-processor face_swapper face_enhancer \
    --keep-fps --keep-audio
```

Use CUDA with four threads:

```bash
python run.py -s source.jpg --execution-provider cuda --execution-threads 4
```

---

## Hardware Acceleration

Choose the execution provider that matches your hardware.

| Provider | Hardware | Platform | Setup |
|----------|----------|----------|-------|
| `cuda` | NVIDIA GPUs | Windows, Linux | Install CUDA Toolkit and cuDNN, plus `onnxruntime-gpu` |
| `dml` | AMD, Intel, NVIDIA | Windows | Install `onnxruntime-directml` |
| `coreml` | Apple Silicon | macOS | Install standard `onnxruntime` |
| `cpu` | Any | Any | No extra setup, but slowest |

If the requested provider is unavailable, the application falls back to the CPU.

### Verifying GPU use

Check the console log at startup. It should list the active execution provider. If it reports `CPUExecutionProvider` when you expected a GPU, check your CUDA/cuDNN versions or your ONNX Runtime installation.

---

## Localization

The interface is translated into several languages. Translation files are stored as JSON in the repository root:

| Code | Language | File |
|------|----------|------|
| `en` | English (default) | Built-in |
| `de` | German | `de.json` |
| `es` | Spanish | `es.json` |
| `fi` | Finnish | `fi.json` |
| `ru` | Russian | `ru.json` |
| `zh` | Chinese | `zh.json` |
| `ko` | Korean | `ko.json` |
| `pt-br` | Portuguese (Brazil) | `pt-br.json` |
| `km` | Khmer | `km.json` |
| `th` | Thai | `th.json` |

The `modules/gettext.py` module handles string lookup. To add a language, copy an existing file, translate the values, and keep the keys unchanged.

---

## Configuration

- **`modules/globals.py`** holds default runtime settings. Editing it changes default behavior for all sessions.
- **`ui.json`** controls interface text and layout.
- **`mypi.ini`** holds mypy settings for static type checking.

Example of checking types:

```bash
pip install mypy
mypy --config-file mypi.ini .
```

---

## Troubleshooting

**`ffmpeg` not found**
Install FFmpeg and confirm it is on your `PATH` by running `ffmpeg -version` in a new terminal.

**Model file not found**
Confirm that `inswapper_128_fp16.onnx` (or `inswapper_128.onnx`) is in the `models/` folder.

**Very low frame rate in live mode**
Use a GPU execution provider, reduce webcam resolution, disable the face enhancer, or lower the thread count.

**CUDA errors or the CPU provider is used instead**
Check that your CUDA and cuDNN versions match the `onnxruntime-gpu` requirements. Make sure only one ONNX Runtime package is installed.

**DLL load errors on Windows**
Install the latest Microsoft Visual C++ Redistributable.

**Webcam not detected**
Close other applications using the camera and try a different camera index in the settings.

**Dependency conflicts**
Use a clean virtual environment with Python 3.10 and reinstall from `requirements.txt`.

**Out of memory**
Reduce `--max-memory`, lower the video resolution, or process fewer frames at once.

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

General workflow:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes and run type checks with `mypy`.
4. Commit with a clear message.
5. Open a pull request describing the change and how you tested it.

When adding translations, keep the JSON keys identical to the English source.

---

## License

This project is distributed under the license in the [LICENSE](LICENSE) file. Read it before using, modifying, or redistributing the software. Model files may be subject to separate licenses from their original authors.

---

## Acknowledgements

- [InsightFace](https://github.com/deepinsight/insightface) for face analysis and the inswapper model.
- [GFPGAN](https://github.com/TencentARC/GFPGAN) for face restoration.
- [ONNX Runtime](https://onnxruntime.ai/) for hardware-accelerated inference.
- [FFmpeg](https://ffmpeg.org/) for video processing.
- All contributors and translators who have helped improve the project.

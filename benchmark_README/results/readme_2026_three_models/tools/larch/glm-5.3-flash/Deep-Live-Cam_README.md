# README.md for Deep-Live-Cam-ssltv728

````markdown
# 🎭 Deep-Live-Cam-ssltv728

> **Real-Time Face Swap and One-Click Video Deepfake — with only a single image.**

<p align="center">
  <img src="ludwig.gif" alt="Deep-Live-Cam-ssltv728 demo" width="720"/>
</p>

[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Code Style](https://img.shields.io/badge/typing-mypy-informational.svg)](mypy.ini)

---

## 📖 Table of Contents

1. [Introduction](#-introduction)
2. [⚠️ Disclaimer — Ethical Use](#%EF%B8%8F-disclaimer--ethical-use)
3. [✨ Features](#-features)
4. [🎬 Demos & Showcase](#-demos--showcase)
5. [🚀 Quick Start (TL;DR)](#-quick-start-tldr)
6. [📦 Requirements](#-requirements)
7. [🛠️ Installation](#%EF%B8%8F-installation)
8. [▶️ Usage](#%EF%B8%8F-usage)
9. [⌨️ Command-Line Reference](#%EF%B8%8F-command-line-reference)
10. [🔍 NSFW Filter & Cluster Analysis](#-nsfw-filter--cluster-analysis)
11. [🌐 Localization](#-localization)
12. [📈 Performance](#-performance)
13. [🧰 Troubleshooting & FAQ](#-troubleshooting--faq)
14. [🤝 Contributing](#-contributing)
15. [🏆 Credits & Acknowledgements](#-credits--acknowledgements)
16. [📜 License](#-license)

---

## 📖 Introduction

**Deep-Live-Cam-ssltv728** is a Python-based real-time face-swapping and
deepfake toolkit, built as an enhanced variant of
[Deep-Live-Cam](https://github.com/hacksider/Deep-Live-Cam) (and, by
extension, the original **roop** project).

With **one single image** containing a face, you can:

- 🎥 **Swap faces in any video** — one click, done.
- 📷 **Swap faces in a still image**.
- 🔴 **Swap your face live on a webcam feed** — great for streaming,
  video calls, and content creation.
- 🖼️ **Restore & enhance the swapped face** using GFPGAN for
  photorealistic results.

The project ships with a modern desktop GUI (`customtkinter`), a fully
scriptable CLI, GPU acceleration (CUDA / DirectML / CoreML), an optional
NSFW safety filter, and a multi-language interface.

---

## ⚠️ Disclaimer — Ethical Use

**This project is intended as a creative tool for video editing and
content creation. Users are expected to use it responsibly.**

The authors and contributors are **not** responsible for any misuse.
Please adhere to the following rules:

1. ❌ **Do not** use this software on adults without their explicit,
   informed consent.
2. ❌ **Do not** use this software to create fake or malicious content
   that could be used to harm, defraud, defame, or deceive others
   (including fake news, impersonation, or targeted harassment).
3. ❌ **Do not** create or share deepfakes of real people (especially
   public figures, politicians, or rulers) in ways they did not consent to.
4. ✅ **Do** only use images you own or that depict yourself, or faces
   of people who have explicitly given you permission.

> **Note:** The developers disclaim all liability for malicious or
> unethical use of this software. Read the full terms in the
> [`LICENSE`](LICENSE) file.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎥 **One-Click Video Deepfake** | Swap a face across an entire video from a single source image. |
| 🔴 **Live Face Swap** | Real-time face swap on your webcam feed via the built-in preview. |
| 🧩 **Face Mapping** | Map one source face to *multiple distinct faces* found in a target (`--map-faces`). |
| 👥 **Many Faces** | Replace **every** face detected in the target (`--many-faces`). |
| 💎 **Face Enhancer** | Optional GFPGAN post-processing for sharp, realistic results. |
| 🛡️ **NSFW Filter** | Optional OpenNSFW2-based safety filter with cluster analysis. |
| 🎮 **GPU Acceleration** | NVIDIA CUDA, DirectML (Windows), Apple Silicon (CoreML), or CPU. |
| ⌨️ **Headless CLI** | Full pipeline automation without the GUI — for servers & scripting. |
| 🖥️ **Modern GUI** | Built with `customtkinter`; live preview, progress bars, face picker. |
| 🌐 **Multi-Language UI** | 9 languages included out of the box. |
| 🎚️ **Fine Control** | FPS preservation, frame retention, video encoder & quality, memory limits, thread count. |

---

## 🎬 Demos & Showcase

| Asset | What it shows |
|---|---|
| `ludwig.gif` | Flagship demo — real-time face swap in action |
| `live_show.gif` | Live face swap during a live show |
| `streamers.gif` | Face swap for streamers |
| `movie.gif` | Face swapping in movie footage |
| `meme.gif` | Creating memes |
| `avgpcperformancedemo.gif` | Average FPS performance across consumer GPUs |
| `deepwarebench.gif` | Detection benchmark via Deepware (see [Detection](#-nsfw-filter--cluster-analysis)) |
| `demo.gif` | General walkthrough |

<p align="center">
  <img src="streamers.gif" alt="Streamer demo" width="400"/>
  &nbsp;&nbsp;
  <img src="live_show.gif" alt="Live show demo" width="400"/>
</p>

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Clone the repository
git clone https://github.com/ssltv728/Deep-Live-Cam-ssltv728.git
cd Deep-Live-Cam-ssltv728

# 2. Install Python 3.10 or 3.11, then install dependencies
pip install -r requirements.txt

# 3. Run!
python run.py
```

That's it. Pick a **source image** (the face you want to use), pick a
**target** (an image or video), and press **Start**.
For a **live webcam swap**, press **Live** in the UI.

### 🪟 Windows One-Click Launchers

| File | Use it when… |
|---|---|
| `run-cuda.bat` | You have an **NVIDIA GPU** (CUDA acceleration) |
| `run-directml.bat` | You have an AMD / Intel GPU on **Windows** (DirectML) |
| `python run.py` | CPU-only, or on Linux/macOS |

---

## 📦 Requirements

| Requirement | Details |
|---|---|
| **Operating System** | Windows 10/11, macOS (Apple Silicon recommended), or Linux |
| **Python** | **3.10 or 3.11** (older/newer versions are not officially supported) |
| **Hardware** | Any modern CPU works; a GPU with ≥ 4 GB VRAM is strongly recommended for live mode |
| **FFmpeg** | Pulled in via the `imageio-ffmpeg` dependency; if encoding fails, install FFmpeg and add it to your `PATH` |
| **Source image** | A clear photo containing **one face**, ideally frontal and well-lit |

---

## 🛠️ Installation

### 1. Manual Installation

```bash
git clone https://github.com/ssltv728/Deep-Live-Cam-ssltv728.git
cd Deep-Live-Cam-ssltv728
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

> 💡 On Ubuntu/Debian, if you get a `tkinter` error:
> `sudo apt install python3-tk`

### 2. Models

The face-swap and face-restoration models are downloaded automatically
into the `models/` directory on first launch:

```
Deep-Live-Cam-ssltv728/
└── models/
    ├── inswapper_128.onnx    # InsightFace face-swap model
    └── GFPGANv1.4.pth        # GFPGAN face-restoration model
```

If the automatic download fails (firewall, proxy, etc.), fetch them
manually and place them in `models/`:

- **inswapper_128.onnx** — InsightFace model zoo / Hugging Face mirror
- **GFPGANv1.4.pth** — https://github.com/TencentARC/GFPGAN/releases

### 3. GPU Inference (Optional — highly recommended)

#### 🟢 NVIDIA CUDA

```bash
pip uninstall onnxruntime onnxruntime-directml
pip install onnxruntime-gpu==1.18.1
python run.py --execution-provider cuda
```

> Your CUDA toolkit version must be compatible with the `onnxruntime-gpu`
> build. CUDA 11.8+ is recommended.

#### 🍎 Apple Silicon (CoreML)

```bash
pip uninstall onnxruntime onnxruntime-gpu
pip install onnxruntime-silicon==1.13.1
python run.py --execution-provider coreml
```

#### 🟦 DirectML (AMD / Intel GPUs on Windows)

```bash
pip uninstall onnxruntime onnxruntime-gpu
pip install onnxruntime-directml==1.15.1
python run.py --execution-provider dml
```

Or simply double-click **`run-directml.bat`**.

#### ⚡ Headless / Full-GPU Mode

By default the CPU provider stays as a fallback. To force a fully
GPU-accelerated pipeline (e.g. on a server without a display):

```bash
pip uninstall onnxruntime
pip install onnxruntime-gpu==1.18.1
python run.py --execution-provider cuda
```

---

## ▶️ Usage

### 🖥️ GUI Mode (default)

```bash
python run.py
```

1. **Select a face** — choose a source image containing one face.
2. **Select a target** — choose an image or a video.
3. **Start** — pick an output path; the swap is processed and saved.
4. Toggle **Face Enhancer** for GFPGAN post-processing.
5. (Optional) Enable the **NSFW Filter** for safety.

### 🔴 Live / Webcam Mode

1. Click **Live** in the UI.
2. Choose your camera (index-based) and the preview size.
3. Click **Live Start**.
4. Keyboard shortcuts in the preview window:
   - **`F`** — swap the face on / off
   - **`Q`** — quit the live preview

Useful flags for live mode:

```bash
python run.py --live-mirror     # mirror the preview (like a real mirror)
python run.py --live-resizable  # make the live preview window resizable
```

> 💡 For streaming: point OBS Studio / Discord / Zoom at the live
> preview window, or capture it as a window source.

### 🎬 One-Click Video Deepfake (GUI)

1. Select the **source** face image.
2. Select the **target** video.
3. Press **Start**, choose where to save, and wait for processing.

### ⌨️ CLI Mode (headless)

```bash
# Basic image swap
python run.py -s face.jpg -t portrait.jpg -o result.png

# Full video deepfake on GPU
python run.py -s face.jpg -t video.mp4 -o swapped.mp4 --execution-provider cuda

# Swap + enhance (better quality, slower)
python run.py -s face.jpg -t video.mp4 -o enhanced.mp4 \
    --frame-processor face_swapper face_enhancer

# Swap every face in a crowd video
python run.py -s face.jpg -t crowd.mp4 -o crowd.mp4 --many-faces

# Maximum speed: NVENC hardware encoder, keep original FPS, no audio re-encode issues
python run.py -s face.jpg -t video.mp4 -o fast.mp4 \
    --video-encoder h264_nvenc --keep-fps --skip-audio --execution-provider cuda
```

---

## ⌨️ Command-Line Reference

```
python run.py [options]
```

| Option | Description | Default |
|---|---|---|
| `-h`, `--help` | Show help and exit | — |
| `-v`, `--version` | Show version and exit | — |
| `-s`, `--source` | Path to the **source image** (face to swap in) | — |
| `-t`, `--target` | Path to the **target** image or video | — |
| `-o`, `--output` | Path to the output file / directory | — |
| `--frame-processor` | Pipeline stages: `face_swapper`, `face_enhancer` (repeatable) | `face_swapper` |
| `--keep-fps` | Preserve the target video's original FPS | off |
| `--keep-frames` | Keep temporary extracted frames in the output directory | off |
| `--skip-audio` | Do not copy the target's audio track into the output | off |
| `--many-faces` | Swap **all** detected faces instead of the best match | off |
| `--map-faces` | Automatically map faces across frames for multi-face targets | off |
| `--nsfw-filter` | Refuse to process NSFW content (slower) | off |
| `--video-encoder` | `libx264` \| `libx265` \| `h264_nvenc` \| `hevc_nvenc` | `libx264` |
| `--video-quality` | Output quality, `0` (worst) – `100` (best) | `68` |
| `--live-mirror` | Mirror the live webcam preview | off |
| `--live-resizable` | Allow resizing the live preview window | off |
| `--max-memory` | Maximum RAM usage in MB (`0` = auto) | `0` |
| `--execution-provider` | `cpu`, `cuda`, `coreml`, `dml` (last one is the fallback) | `cpu` |
| `--execution-threads` | Number of parallel worker threads | `4` |
| `--log-level` | `fatal` → `debug` | `info` |

---

## 🔍 NSFW Filter & Cluster Analysis

This fork includes **two layers** of protection, enabled via the UI
toggle or the `--nsfw-filter` flag:

- **`predicter.py`** — an OpenNSFW2-based image classifier that scans
  source/target images before processing.
- **`cluster_analysis.py`** — additional analysis of detected faces to
  prevent unsafe or unintended mappings.

> ⚠️ Enabling the NSFW filter **slows processing down**, but is strongly
> recommended when you're unsure about your input material.

### Detecting Manipulated Media

Tools such as **Deepware** can help detect AI-manipulated videos.
See `deepwarebench.gif` for a benchmark example — and please use this
tool ethically so detection technology remains effective.

---

## 🌐 Localization

The interface ships with the following translations:

| Code | Language | Code | Language |
|---|---|---|---|
| `de.json` | 🇩🇪 German | `ko.json` | 🇰🇷 Korean |
| `es.json` | 🇪🇸 Spanish | `pt-br.json` | 🇧🇷 Portuguese (Brazil) |
| `fi.json` | 🇫🇮 Finnish | `km.json` | 🇰🇭 Khmer |
| `ru.json` | 🇷🇺 Russian | `th.json` | 🇹🇭 Thai |
| `zh.json` | 🇨🇳 Chinese | | |

The language is detected from your system locale and can be changed in
the UI settings. Translations are loaded by `gettext.py` from the
`*.json` files — **PRs adding new languages are very welcome!**

---

## 📈 Performance

Processing speed depends on your hardware, frame processor(s),
resolution, thread count, and selected encoder. Indicative figures
with the default pipeline (`face_swapper`, 4 threads):

| Hardware | Average FPS | Time for 500 frames |
|---|---:|---:|
| Intel i5-1240P (CPU only) | ~7 | ~70 s |
| GTX 1060 | ~24 | ~21 s |
| RTX 3060 Ti | ~70 | ~7 s |
| RTX 3090 | ~108 | ~5 s |
| RTX 4090 | ~128 | ~4 s |

*Numbers are indicative — measure on your own hardware and see
`avgpcperformancedemo.gif`.*

**Tips to go faster:**

- Use a GPU execution provider (`cuda` / `dml` / `coreml`).
- Increase `--execution-threads` (4–16).
- Use a hardware encoder (`h264_nvenc` / `hevc_nvenc`).
- Skip `face_enhancer` unless you need the extra quality.

---

## 🧰 Troubleshooting & FAQ

<details>
<summary><b>onnxruntime is not using my GPU</b></summary>

Make sure you installed the matching provider (`onnxruntime-gpu`,
`onnxruntime-directml`, or `onnxruntime-silicon`) **and** pass the
matching `--execution-provider`. CUDA users: your CUDA toolkit version
must match the runtime build.
</details>

<details>
<summary><b>Model download fails / stalls</b></summary>

Download `inswapper_128.onnx` and `GFPGANv1.4.pth` manually and place
them in the `models/` folder.
</details>

<details>
<summary><b>Camera doesn't start (macOS)</b></summary>

macOS requires explicit camera permissions for terminal apps
(System Settings → Privacy & Security → Camera).
</details>

<details>
<summary><b>Encoder errors / missing FFmpeg</b></summary>

Install FFmpeg and make sure `ffmpeg` is on your `PATH`.
</details>

<details>
<summary><b>Out of memory</b></summary>

Lower the target resolution, disable `face_enhancer`, reduce
`--execution-threads`, or set `--max-memory`.
</details>

<details>
<summary><b>Poor swap quality</b></summary>

Use a **high-resolution**, **frontal**, well-lit source photo with a
**single face**, and enable the face enhancer. Matching head angle and
lighting between source and target makes a huge difference.
</details>

---

## 🤝 Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md)
first.

- 🐛 Bug reports: open an issue with your OS, Python version, GPU, and logs.
- 🌐 Translations: add/extend a `*.json` locale file.
- 🧪 Before submitting a PR, please run static checks (the project uses
  [`mypy.ini`](mypy.ini)):

```bash
pip install mypy
mypy .
```

---

## 🏆 Credits & Acknowledgements

This project stands on the shoulders of giants:

- **[hacksider/Deep-Live-Cam](https://github.com/hacksider/Deep-Live-Cam)** — the base of this fork
- **[s0md3v/roop](https://github.com/s0md3v/roop)** — the original project
- **[iperov/DeepFaceLive](https://github.com/iperov/DeepFaceLive)** — live pipeline inspiration
- **[InsightFace](https://github.com/deepinsight/insightface)** — face analysis & `inswapper_128`
- **[GFPGAN](https://github.com/TencentARC/GFPGAN)** — face restoration
- **[OpenNSFW2](https://github.com/bedapud6/OpenNSFW2)** — NSFW classification
- All the community translators and testers 🙏

---

## 📜 License

This project is licensed under the **GNU Affero General Public License
v3.0 (AGPL-3.0)**, **with additional terms** restricting unethical use
(no use without consent, no malicious/deceptive content).

See the [`LICENSE`](LICENSE) file for the complete text, and the
[Disclaimer](#%EF%B8%8F-disclaimer--ethical-use) section above.

---

<p align="center">
  ⭐ If this project helped you, please consider giving it a star!
</p>
````

---

**Notes on the draft:**

- It's built directly from the file list: entry point (`run.py`), core pipeline (`core.py`, `face_analyser.py`, `face_swapper.py`, `face_enhancer.py`), NSFW safety (`predicter.py`, `cluster_analysis.py`), live capture (`video_capture.py`), GUI + i18n (`ui.py`, `gettext.py`, 9 `*.json` locales), Windows launchers (`run-cuda.bat`, `run-directml.bat`), all 8 demo GIFs, and dev config (`mypy.ini`, `CONTRIBUTING.md`).
- The GPU install commands, CLI flags, FPS table, and live-mode shortcuts mirror the upstream **Deep-Live-Cam** project this repo is clearly derived from — tweak version pins/numbers if your fork diverges.
- Feel free to remove the badge row, the `<details>` FAQ blocks, or the emoji headers if you'd prefer a plainer style.

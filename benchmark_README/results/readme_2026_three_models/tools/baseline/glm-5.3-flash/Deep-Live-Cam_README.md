# Deep-Live-Cam

Deep-Live-Cam is a real-time and one-click face-swapping tool for images and video. It lets you take a single source image and swap that face onto a target image, a target video, or live webcam footage — all from a desktop application built with Python and a CustomTkinter UI.

## Features

- **Image and video face swap** — process a single photo or an entire video (frames are extracted, processed, and reassembled with FFmpeg, and the original audio can be preserved).
- **Real-time webcam face swap** — swap your face live from any connected camera, with selectable camera devices and frame previews.
- **Face enhancer** — optional GFPGAN-based enhancement of the swapped face for improved quality.
- **Many faces mode** — detect and swap multiple faces in the target.
- **Source × Target Mapper** — manually map specific source faces to specific target faces, including per-face mapping across video frames (using face-embedding cluster analysis to match faces).
- **Mouth mask** — preserve or blend the target's mouth region using landmark-based masking with configurable size, down-size, and feathering options, plus an optional visualization box.
- **Fix Blueish Cam** — color correction for cameras that produce a blueish output.
- **Keep fps / Keep frames** — control whether the original frame rate is preserved and whether intermediate frames are kept.
- **Show FPS** — display the real-time frame rate during live processing.
- **Multi-language UI** — interface translations for German, Spanish, Finnish, Khmer, Korean, Brazilian Portuguese, Russian, Thai, and Chinese.
- **NSFW filter** — an optional check using OpenNSFW2/TensorFlow to prevent processing inappropriate content.

## Demo

The repository includes several demo animations in the `media/` directory:

| File | Description |
| --- | --- |
| `media/demo.gif` | General face swap demonstration |
| `media/live_show.gif` | Live webcam face swap |
| `media/streamers.gif` | Use case for streamers |
| `media/movie.gif` | Swapping faces in a movie scene |
| `media/meme.gif` | Meme creation example |
| `media/ludwig.gif` | Example with a public figure |
| `media/avgpcperformancedemo.gif` | Performance on an average PC |
| `media/deepwarebench.gif` | Benchmark example |

## How It Works

1. **Face detection and analysis** — faces in the source and target are detected and analyzed with InsightFace.
2. **Frame processing** — for video, FFmpeg extracts frames into a temporary directory; each frame is processed by one or more *frame processors*.
3. **Frame processors** — the project ships with two pluggable frame processors:
   - **Face Swapper** (`modules/processors/frame/face_swapper.py`) — swaps faces using the `inswapper_128_fp16.onnx` model, with optional mouth masking and multi-face/mapped-face handling.
   - **Face Enhancer** (`modules/processors/frame/face_enhancer.py`) — enhances faces with GFPGAN (`GFPGANv1.4.pth`).
4. **Reassembly** — processed frames are encoded back into a video with the configured video encoder and quality (CRF), the original audio track is restored if "Keep audio" is enabled, and temporary files are cleaned up.

Models are downloaded automatically on first use to the `models/` directory (see `models/instructions.txt`).

## Requirements

- Python 3
- `ffmpeg` (must be available on your `PATH`; used for frame extraction, video creation, and audio restoration)
- An internet connection for the initial model download
- A webcam (for live mode)

Core Python dependencies (see `requirements.txt`) include:

- `numpy`, `opencv-python`, `pillow`, `tqdm`
- `insightface`, `onnx`, `onnxruntime-gpu` (or `onnxruntime-silicon` on Apple Silicon Macs)
- `torch` / `torchvision` (with a CUDA 12.8 extra index for GPU acceleration on Windows/Linux)
- `tensorflow`, `opennsfw2` (NSFW detection; not installed on macOS)
- `customtkinter`, `tk` (GUI)
- `psutil`, `cv2_enumerate_cameras`, `typing-extensions`, `protobuf`

The PyTorch wheel index `https://download.pytorch.org/whl/cu128` is used as an extra index for CUDA-enabled builds.

## Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd deep-live-cam

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make sure ffmpeg is installed and available on your PATH
```

Models (`inswapper_128_fp16.onnx` and `GFPGANv1.4.pth`) are downloaded automatically to the `models/` folder when the corresponding frame processor first runs.

### Platform-Specific Setup

- **Windows with NVIDIA CUDA** — run `run-cuda.bat`, which installs/uses the CUDA-enabled PyTorch build (`cu128`).
- **Windows with DirectML** — run `run-directml.bat` for DirectML-based acceleration on compatible GPUs.
- **macOS (Apple Silicon)** — requirements resolve to `onnxruntime-silicon` and PyTorch with MPS support automatically via the platform markers in `requirements.txt`.
- **Linux / CPU-only** — install `requirements.txt` as-is; execution providers can be selected at runtime (e.g., `cpu`).

## Usage

### GUI Mode

```bash
python run.py
```

The graphical interface provides:

1. **Source image selection** — pick the image containing the face you want to use.
2. **Target selection** — pick a target image or video.
3. **Start** — process the target and save the output.
4. **Live** — start real-time webcam face swapping, with camera selection and a "Destroy" button to stop.

Optional toggles in the UI include Keep audio, Face Enhancer, Many faces, Map faces, Show FPS, Keep fps, Keep frames, Fix Blueish Cam, Mouth Mask, and Show Mouth Mask Box.

### Source × Target Mapper

When "Map faces" is enabled, a mapper window opens that lets you:

- Select multiple source images and target images,
- Detect unique faces in the target (including faces across video frames),
- Pair each source face with a specific target face,
- Add, clear, and submit mappings.

Mappings are matched at processing time using face-embedding centroid analysis (`modules/cluster_analysis.py`), so the correct source face is applied to each detected target face.

### Command Line

The application is started via `run.py`, which calls `modules.core.run()`. Runtime settings (source/target paths, output path, execution providers, thread count, memory limit, video encoder and quality, log level, and all feature toggles) are managed through `modules.globals`.

## Configuration

Key configurable behaviors (managed through the UI and `modules.globals`):

| Option | Effect |
| --- | --- |
| Execution providers | Choose ONNX Runtime providers (e.g., CUDA, CPU, TensorRT if available) |
| Execution threads | Number of worker threads for parallel frame processing |
| Max memory | Memory limit for processing |
| Video encoder / quality | FFmpeg encoder and CRF quality used when creating output video |
| Log level | Verbosity of FFmpeg/status logging |
| Mask size / Mask down size / Mask feather ratio | Tuning for the mouth mask feature |
| Frame processors | Enable/disable Face Swapper and Face Enhancer, including dynamically from the UI |

Temporary frames are stored in a `temp/` directory next to the target file and cleaned up automatically unless "Keep frames" is enabled.

## Development

### Project Structure

```
run.py                        # Entry point
modules/
  core.py                     # Application orchestration and CLI handling
  globals.py                  # Global runtime settings
  ui.py, ui.json              # CustomTkinter GUI
  face_analyser.py            # Face detection/extraction helpers
  capturer.py, video_capture.py  # Camera capture (DirectShow-aware on Windows)
  processors/frame/           # Pluggable frame processors (face_swapper, face_enhancer)
  cluster_analysis.py         # Face-embedding centroid matching
  predicter.py                # NSFW prediction
  gettext.py, locales/        # Localization
  utilities.py                # FFmpeg helpers, downloads, temp file management
  typing.py                   # Shared type definitions
models/                       # Model weights and instructions
media/                        # Demo animations
locales/                      # UI translation files (JSON)
```

### Frame Processor Interface

Custom frame processors can be added under `modules/processors/frame/`. Each processor module must implement the required interface methods: `pre_check`, `pre_start`, `process_frame`, `process_image`, and `process_video`. They are loaded dynamically via `modules.processors.frame.core`.

### Type Checking

The repository includes a `mypi.ini` with a strict mypy configuration (`check_untyped_defs`, `disallow_untyped_defs`, `disallow_untyped_calls`, `disallow_any_generics`). Run mypy against the codebase to verify type correctness before submitting changes.

### Localization

UI strings are translated via JSON files in `locales/`. To add a language, create a new locale file following the existing format (e.g., `locales/de.json`).

## Contributing

See `CONTRIBUTING.md` for the full guidelines. Summary:

### Branching Strategy

- **`premain`** — all changes should be pushed to `premain` first. All tests are performed there; changes are merged into `main` only after rigorous testing (hours to days).
- **`experimental`** — use for large or potentially disruptive changes requiring thorough discussion and review.

### Pre-Pull Request Checklist

Before opening a PR, verify:

- **Functionality**
  - Realtime faceswap works with the face enhancer both enabled and disabled.
  - Map Faces works with both options (enabled and disabled).
  - All cameras are listed accurately.
- **Stability**
  - No drop in real-time FPS.
  - No negative impact on boot time (application or real-time faceswap).
  - At least 15 minutes of testing with no GPU overloading or crashes.
  - The application remains responsive with no lag.

## Testing

There is no dedicated automated test suite in the repository. Testing is performed manually on the `premain` branch following the checklist above. Type checking with mypy (using `mypi.ini`) is part of the development workflow.

## Reporting Bugs

Use the bug report issue template (`.github/ISSUE_TEMPLATE/bug_report.md`) and include:

- A clear description of the bug
- Screenshots, if applicable
- The exact error message from the terminal
- Your OS, version, GPU, and CPU
- The mandatory confirmations: the template was followed, the issue is not a performance question, and it is not a duplicate

Issues that do not follow the template may be closed without notice.

## Ethics and Responsible Use

This software manipulates faces in images and video. You are responsible for using it lawfully and ethically — do not use it to create deceptive, defamatory, or non-consensual content, and always respect the rights and likeness of the people whose faces you process.

## License

This project is licensed under the **GNU Affero General Public License v3.0** (see `LICENSE`). This is a free, copyleft license: you are free to use, modify, and distribute the software, provided that derivatives — including software offered over a network — remain licensed under the AGPLv3 with full source availability. The program is provided **without warranty of any kind**; see sections 15 and 16 of the license for details.

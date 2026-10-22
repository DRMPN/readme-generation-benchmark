# Deep-Live-Cam

Deep-Live-Cam is a Python application that swaps a face from a source image onto a target face in images, in videos, and in a live webcam feed. It provides a desktop GUI (built with CustomTkinter) and a command-line mode for batch processing.

![Demo](media/demo.gif)

> **Responsible use:** Face swapping can be used to impersonate real people. Only use this software on faces you have permission to use, and follow the laws that apply where you live. The project is licensed under AGPL-3.0 (see [License](#license)).

## Features

- **Image face swap:** Swap a face from a source image onto a target image.
- **Video face swap:** Swap faces frame by frame in a target video, with options to keep the original FPS and audio.
- **Live mode:** Run the swap on a webcam feed from the GUI, with options for a mirrored view and an FPS display.
- **Face mapping (`--map-faces`):** Choose which source face replaces which target face when a frame contains several people. Mapping is set up in the GUI.
- **Many faces (`--many-faces`):** Process every detected face instead of only one.
- **Face enhancer:** An optional GFPGAN-based pass that enhances the swapped face (`--frame-processor face_enhancer`).
- **Mouth mask (`--mouth-mask`):** Keeps the lower-mouth region of the original target face.
- **Optional NSFW filter (`--nsfw-filter`):** Checks images and videos with the `opennsfw2` model before processing.
- **Multiple execution providers:** Runs on whichever ONNX Runtime execution providers are available on your system (for example CPU, CUDA, DirectML, or CoreML).
- **Localized GUI:** Translation files are included for several languages (see [Language](#language)).

## Requirements

- **Python 3.9 or newer.** The app checks this at startup.
- **ffmpeg** (with `ffprobe`) available on your `PATH`. The app checks for `ffmpeg` at startup and exits if it is missing.
- **Model files** placed in the `models/` folder (see [Models](#models)).
- **Python packages** listed in `requirements.txt`. The key ones are:
  - `insightface==0.7.3` (face detection, analysis, and the swapper model loader)
  - `onnx==1.16.0` and `onnxruntime-gpu==1.21.0` (or `onnxruntime-silicon==1.21.0` on Apple Silicon)
  - `opencv-python==4.10.0.84`
  - `customtkinter==5.2.2` (GUI)
  - `torch`, `torchvision`, and `tensorflow` (used by the GFPGAN enhancer and by resource setup)
  - `opennsfw2==0.10.2` (NSFW filter)
  - `numpy>=1.23.5,<2`

A GPU is optional. Without one, the app runs with the CPU execution provider by default.

## Installation

The repository does not include a separate install guide, so the steps below are based on `requirements.txt` and the code. They have not been verified on every platform.

1. Clone the repository and enter its folder.
2. Create and activate a virtual environment (the `.gitignore` already excludes `venv/` and `.venv/`):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` adds the PyTorch CUDA 12.8 wheel index (`https://download.pytorch.org/whl/cu128`) and pins `onnxruntime-gpu` on non-macOS systems. On macOS it uses `onnxruntime-silicon` for Apple Silicon (arm64) and `torch==2.5.1` / `torchvision==0.20.1`.

4. Install ffmpeg and make sure `ffmpeg` and `ffprobe` run from a terminal.
5. Download the model files (see [Models](#models)).

## Models

The app loads two model files from the `models/` folder:

| File | Used by | Download |
| --- | --- | --- |
| `inswapper_128_fp16.onnx` | Face swapper (required) | https://huggingface.co/hacksider/deep-live-cam/resolve/main/inswapper_128_fp16.onnx?download=true |
| `GFPGANv1.4.pth` | Face enhancer (only used with `--frame-processor face_enhancer` or the GUI Face Enhancer switch) | https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth |

Put both files in the `models/` folder. Face-analysis models (`buffalo_l`) are loaded by `insightface` and are handled by that library.

> **Note:** The face swapper's `pre_check()` tries to download `inswapper_128_fp16.onnx` using a Hugging Face page URL (`/blob/main/`) and saves it to `modules/processors/frame/`, not `models/`. The code loads the model from `models/`. Downloading the file manually from the `/resolve/` URL above into `models/` is the reliable option.

## Usage

### GUI mode

Run the app with no source or target arguments:

```bash
python run.py
```

The window lets you:

1. Select a source face image and a target image or video (the **↔** button swaps them).
2. Toggle options such as **Keep fps**, **Keep frames**, **Keep audio**, **Many faces**, **Map faces**, **Face Enhancer**, **Fix Blueish Cam**, **Show FPS**, **Mouth Mask**, and **Show Mouth Mask Box**.
3. Click **Start** to process the target, or **Preview** to see a swapped frame first.
4. Choose a camera and click **Live** to run the swap on a webcam feed.
5. Click **Destroy** to stop and clean up temporary files.

The NSFW filter switch is commented out in the GUI code. The NSFW filter is available only through the `--nsfw-filter` command-line flag.

Toggling a switch in the GUI saves the current switch states to `switch_states.json` in the working directory, and those states are loaded the next time the GUI starts.

### Command-line mode

Passing any of `-s/--source`, `-t/--target`, or `-o/--output` runs in headless mode, which processes the target without opening the GUI. In headless mode, pass `-o` with the output file path (or directory when used with `-s` and `-t`).

```bash
# Swap a face in an image
python run.py -s source.jpg -t target.jpg -o output.jpg

# Swap a face in a video, keep the original FPS, and use the face enhancer
python run.py -s source.jpg -t target.mp4 -o output.mp4 --keep-fps --frame-processor face_swapper face_enhancer

# Process every face in the target
python run.py -s source.jpg -t group.mp4 -o output.mp4 --many-faces
```

When `-s` and `-t` are both given and `-o` is an existing directory, the output is named `<source>-<target><ext>` inside that directory.

### Command-line options

| Option | Default | Description |
| --- | --- | --- |
| `-s, --source` | none | Source face image. |
| `-t, --target` | none | Target image or video. |
| `-o, --output` | none | Output file, or a directory when source and target are also given. |
| `--frame-processor` | `face_swapper` | One or more of `face_swapper`, `face_enhancer`. Run in the order given. |
| `--keep-fps` | off | Keep the target video's original frame rate. Without it, the output is written at 30 FPS. |
| `--keep-audio` | on | Keep the target's audio track. The flag is defined as `store_true` with a default of `True`, so audio is kept unless the code is changed. |
| `--keep-frames` | off | Keep the extracted temporary frames. |
| `--many-faces` | off | Process every detected face instead of only one. |
| `--map-faces` | off | Enable source/target face mapping. |
| `--mouth-mask` | off | Apply the mouth mask. |
| `--nsfw-filter` | off | Check the target with the NSFW model before processing. |
| `--video-encoder` | `libx264` | One of `libx264`, `libx265`, `libvpx-vp9`. |
| `--video-quality` | `18` | Constant rate factor for the video encoder, from `0` to `51`. |
| `--execution-provider` | `cpu` | One or more execution providers. Choices come from the ONNX Runtime providers installed on your system. Names are lowercase, such as `cpu`, `cuda`, `dml`, `coreml`, or `rocm`. |
| `--execution-threads` | `8` | Number of worker threads. The default is fixed at `8` when the arguments are defined, so it does not change with the chosen provider. Set it explicitly (for example `1`) when using DirectML or ROCm. |
| `--max-memory` | `16` GB (`4` on macOS) | Memory limit in GB. |
| `--live-mirror` | off | Mirror the live camera view. |
| `--live-resizable` | off | Make the live camera window resizable. |
| `-l, --lang` | `en` | GUI language code (see [Language](#language)). |
| `-v, --version` | | Print the version. |

Deprecated options `-f/--face`, `--cpu-cores`, `--gpu-vendor`, and `--gpu-threads` still work but print a warning and map to the newer options.

### Windows launchers

Two batch files start the app with a preset execution provider:

- `run-cuda.bat`: runs `python run.py --execution-provider cuda`. Requires an NVIDIA GPU and a working CUDA setup.
- `run-directml.bat`: runs `python run.py --execution-provider dml`. Uses DirectML.

## How it works

1. **Startup:** `run.py` calls `modules/core.py`, which parses arguments, checks Python and ffmpeg, and calls each selected frame processor's `pre_check()`.
2. **Face analysis:** `modules/face_analyser.py` uses `insightface` (`buffalo_l` model) to detect faces and their embeddings.
3. **Face swap:** `modules/processors/frame/face_swapper.py` loads `inswapper_128_fp16.onnx` and swaps the source face onto each target face. The mouth mask and color transfer are applied here when enabled.
4. **Enhancement:** `modules/processors/frame/face_enhancer.py` runs GFPGAN (`GFPGANv1.4.pth`) on frames where a face is detected.
5. **Video handling:** `modules/utilities.py` extracts frames with ffmpeg into a `temp/<video-name>/` folder next to the target, processes them, rebuilds the video with ffmpeg, and restores the original audio. The temp folder is deleted unless `--keep-frames` is set.
6. **Live mode:** `modules/ui.py` reads frames from the selected camera with OpenCV and runs the same frame processors on each frame.

## Project structure

```
run.py                       Entry point
run-cuda.bat / run-directml.bat   Windows launchers with preset execution providers
requirements.txt             Python dependencies
models/                      Model files (download separately; see Models)
locales/                     GUI translation files (*.json)
media/                       Demo images and GIFs
modules/
  core.py                    Argument parsing, startup checks, main flow
  ui.py                      CustomTkinter GUI and live webcam mode
  globals.py                 Shared runtime settings
  face_analyser.py           Face detection and mapping (insightface)
  predicter.py               NSFW detection (opennsfw2)
  utilities.py               ffmpeg helpers, file and temp-folder handling
  cluster_analysis.py        Face-embedding clustering for mapping
  processors/frame/
    face_swapper.py          Face swap and mouth mask
    face_enhancer.py         GFPGAN face enhancement
    core.py                  Frame-processor loader and parallel processing
```

## Language

The GUI uses the `-l/--lang` option. Translation files are included for: `de`, `es`, `fi`, `km`, `ko`, `pt-br`, `ru`, `th`, and `zh`. The default is `en`. Strings without a translation are shown in English.

## Troubleshooting

- **"ffmpeg is not installed."** Install ffmpeg and make sure `ffmpeg` is on your `PATH`.
- **"Python version is not supported."** Use Python 3.9 or newer.
- **"No face in source path detected."** Use a source image where a face is clearly visible.
- **"No cameras found"** in the GUI. Check that the camera is connected and not in use by another app. On Linux, the app checks the first 10 camera indices.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first. It describes the `premain` and `experimental` branch workflow and the pre-pull-request checks (face swap with and without the face enhancer, map faces, camera listing, real-time FPS, boot time, and GPU stability). Bug reports can use the template in `.github/ISSUE_TEMPLATE/bug_report.md`.

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See [LICENSE](LICENSE) for the full text.

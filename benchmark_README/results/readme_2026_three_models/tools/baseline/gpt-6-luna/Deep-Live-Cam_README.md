# Deep-Live-Cam

Deep-Live-Cam is a Python desktop application for processing images and videos with face-swapping and face-enhancement processors. It also provides a live-camera preview, face mapping, and options for video output and frame processing. The application is named **Deep-Live-Cam 1.8 (GitHub Edition)** in its metadata.

The graphical interface is built with CustomTkinter. You can also run image or video processing from the command line by supplying source, target, and output paths.

## Features

- Swap a source face into a target image or video.
- Enhance detected faces with the optional face-enhancer processor.
- Process multiple detected faces, or map source faces to faces found in a target.
- Preview processed frames and use an available camera for live preview.
- Choose whether to preserve video frame rate and audio, and whether to retain temporary frames.
- Configure video encoder and quality, execution provider and thread count, memory limit, and interface language.
- Use a mouth mask, show its visualization, mirror the live preview, or display its FPS.

The interface has translation files for German (`de`), Spanish (`es`), Finnish (`fi`), Khmer (`km`), Korean (`ko`), Brazilian Portuguese (`pt-br`), Russian (`ru`), Thai (`th`), and Chinese (`zh`). English is the default language.

## Requirements

- Python 3.9 or later.
- FFmpeg available on `PATH`. The application checks for it at startup and uses FFmpeg and FFprobe for video processing.
- The Python packages listed in [`requirements.txt`](requirements.txt).
- Model files required by the processors you use. The repository’s `models/instructions.txt` lists the model download locations.

The requirements file includes platform-specific PyTorch and ONNX Runtime entries. It also configures a PyTorch CUDA 12.8 package index. GPU execution depends on an available ONNX Runtime execution provider and suitable system support; CPU is the command-line default.

## Setup

Clone or download the repository, then create and activate a virtual environment. For example, on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows, create the environment with `py -m venv .venv` and activate it with `.venv\Scripts\activate` before installing requirements.

Download the models listed in `models/instructions.txt` and place them in the `models/` directory:

- `inswapper_128_fp16.onnx` for face swapping.
- `GFPGANv1.4.pth` for face enhancement.

The face-enhancer code also checks for and downloads its GFPGAN model during its pre-check. The face-swapper code has its own model pre-check; consult the model instructions and ensure the swapper model is available in `models/`.

Start the application from the repository root:

```bash
python run.py
```

FFmpeg must be installed separately from the Python dependencies. If startup reports that FFmpeg is missing, install it and ensure both `ffmpeg` and `ffprobe` can be found on `PATH`.

## Using the application

In the desktop interface, choose a source image and a target image or video. The source must contain a detectable face for regular face swapping. Choose an output file when prompted, then start processing. The preview window can show a processed target frame; for video targets, use its slider to select a frame.

The interface includes switches for preserving FPS and audio, retaining temporary frames, enabling the face enhancer, processing many faces, mapping faces, correcting a blueish camera image, showing FPS, and applying a mouth mask. Camera selection and the **Live** control open a camera preview when a camera is available. With face mapping enabled, the application provides a mapper for associating source and target faces.

Interface switch settings are saved to `switch_states.json` in the current working directory. If that file does not exist, the application uses its defaults.

## Command-line usage

Run `python run.py --help` to see the available options. A basic headless example is:

```bash
python run.py \
  --source source.jpg \
  --target target.mp4 \
  --output result.mp4 \
  --execution-provider cpu
```

The main options include:

| Option | Purpose |
| --- | --- |
| `-s`, `--source` | Source image. |
| `-t`, `--target` | Target image or video. |
| `-o`, `--output` | Output file or directory. |
| `--frame-processor` | One or more processors: `face_swapper` or `face_enhancer`. Defaults to `face_swapper`. |
| `--keep-fps` | Preserve the target video’s frame rate. Without it, output video is created at 30 FPS. |
| `--keep-audio` | Preserve target audio; enabled by default in the argument configuration. |
| `--keep-frames` | Retain temporary video frames. |
| `--many-faces` | Process every detected face. |
| `--map-faces` | Enable source-to-target face mapping. |
| `--mouth-mask` | Mask the mouth region during face swapping. |
| `--nsfw-filter` | Enable filtering that can ignore an image or video classified above the configured threshold. |
| `--video-encoder` | Select `libx264`, `libx265`, or `libvpx-vp9`. Defaults to `libx264`. |
| `--video-quality` | Set encoder quality from 0 to 51; defaults to 18. |
| `-l`, `--lang` | Set the interface language code; defaults to `en`. |
| `--execution-provider` | Select from providers available in the installed ONNX Runtime. Defaults to `cpu`. |
| `--execution-threads` | Set execution thread count. |
| `--max-memory` | Set the RAM limit in GB; the suggested default is 4 on macOS and 16 elsewhere. |
| `--live-mirror`, `--live-resizable` | Configure live-preview mirroring and resizing. |

The application normalizes an output path when the supplied output is a directory and both source and target paths are provided. Temporary video frames are stored under a `temp` directory alongside the target; they are removed unless `--keep-frames` is enabled.

## Configuration and project layout

Command-line arguments configure processing for a run. The desktop interface persists its switch settings in `switch_states.json`. UI styling is defined in `modules/ui.json`; translations are stored in `locales/`. Processor implementations live under `modules/processors/frame/`, and shared processing, face analysis, camera capture, and video utilities are in `modules/`.

The repository includes `run-cuda.bat` and `run-directml.bat`, but their contents are not provided here; refer to those files before relying on their behavior.

## Development and testing

Install the project dependencies in a Python 3.9+ environment and ensure FFmpeg is available before running the application. The repository includes `mypy.ini`, which enables strict checks for untyped definitions and calls, while ignoring missing imports. No automated test suite or test command is included in the supplied files.

Before submitting a pull request, [`CONTRIBUTING.md`](CONTRIBUTING.md) asks contributors to test realtime face swapping with the enhancer both enabled and disabled, face mapping in both states, and camera listing. It also calls for checking realtime FPS, application and live-feature startup time, responsiveness, and GPU stability over at least 15 minutes. The contribution guide directs changes to `premain` initially and recommends `experimental` for large or potentially disruptive work.

For bug reports, use the repository’s issue template and include a clear description, relevant screenshots, the terminal error message, operating system and version, GPU, and CPU. The template asks reporters to confirm that they followed it, checked for duplicates, and are not submitting a performance-improvement query.

## License

This project is distributed under the **GNU Affero General Public License, version 3 (AGPL-3.0)**, as stated in [`LICENSE`](LICENSE). Consult that file for the complete terms, including conditions for distributing modified versions and network use.

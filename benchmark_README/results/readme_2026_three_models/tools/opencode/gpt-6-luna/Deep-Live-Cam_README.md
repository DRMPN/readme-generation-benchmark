# Deep-Live-Cam

Deep-Live-Cam is a Python desktop application for face swapping and face enhancement in images, videos, and a live camera preview. The application is identified in the code as version **1.8**, **GitHub Edition**.

## Features

- Swap a face from a source image into a target image or video.
- Preview a processed target before saving it.
- Run a live preview from a detected camera.
- Optionally process multiple faces, map source faces to target faces, enhance faces, mask the mouth region, and show live-preview FPS.
- Configure video frame rate and audio retention, and select an ONNX Runtime execution provider from those available in the installed runtime.
- Use the GUI or run image/video jobs from the command line.
- UI translations are provided for German, Spanish, Finnish, Khmer, Korean, Brazilian Portuguese, Russian, Thai, and Chinese, in addition to English.

## Requirements

- Python 3.9 or newer.
- FFmpeg available on `PATH` (the application checks for `ffmpeg`; video frame-rate detection also invokes `ffprobe`).
- The Python packages in [`requirements.txt`](requirements.txt).
- Model files required by the selected frame processors; see [Models](#models).

The face-enhancer module imports `gfpgan`, but `gfpgan` is not listed in `requirements.txt`; the requirements file alone therefore does not establish that the enhancer's Python dependency is installed.

The requirements file includes platform-specific PyTorch and ONNX Runtime entries, including separate entries for macOS and Apple silicon. Camera availability and execution providers depend on the host system and installed runtime.

## Installation

1. Install Python and FFmpeg. Make sure both `ffmpeg` and `ffprobe` can be run from a terminal.
2. Clone or download this repository and change to its directory.
3. (Recommended) Create and activate a virtual environment.
4. Install the Python dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Download and place the model files as described below.

## Models

The face swapper looks for `models/inswapper_128_fp16.onnx`. The face enhancer looks for `models/GFPGANv1.4.pth`. The repository's [`models/instructions.txt`](models/instructions.txt) lists the download sources:

- `inswapper_128_fp16.onnx`: [Hugging Face model file](https://huggingface.co/hacksider/deep-live-cam/resolve/main/inswapper_128_fp16.onnx?download=true)
- `GFPGANv1.4.pth`: [GFPGAN v1.4 release](https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth)

Place each downloaded file in the repository's `models/` directory, keeping the exact filenames above. The face enhancer model is only needed when using the face-enhancer processor. These model files are not included in the repository.

## Run the application

Start the graphical interface with:

```bash
python run.py
```

In the GUI, choose a source face image and a target image or video, configure the available options, then choose **Start** and a destination file. **Preview** shows a processed preview; choose a camera and **Live** to open the live camera preview. When face mapping is enabled, the application presents a mapping dialog before processing.

On Windows, the repository also provides these convenience launchers:

```bat
run-cuda.bat
run-directml.bat
```

They invoke `run.py` with `--execution-provider cuda` and `--execution-provider dml`, respectively. They require the corresponding provider to be available in the installed ONNX Runtime environment.

## Command-line use

Supplying any of `--source`, `--target`, or `--output` selects headless processing instead of opening the GUI. For example:

```bash
python run.py --source path/to/source.jpg --target path/to/target.mp4 --output path/to/result.mp4
```

For an image target, use an image output path instead:

```bash
python run.py --source path/to/source.jpg --target path/to/target.jpg --output path/to/result.jpg
```

Run `python run.py --help` for the full argument list. The main options are:

| Option | Description |
| --- | --- |
| `-s`, `--source` | Source face image. |
| `-t`, `--target` | Target image or video. |
| `-o`, `--output` | Output file path (or output directory when supported by path normalization). |
| `--frame-processor` | One or more processors: `face_swapper` and/or `face_enhancer`. The default is `face_swapper`. |
| `--execution-provider` | One or more ONNX Runtime providers available in the environment. The default is `cpu`. |
| `--execution-threads` | Number of processing threads. |
| `--keep-fps` | Keep the target video's original frame rate; without it, output video is created at 30 fps. |
| `--keep-audio` | Retain target video audio. This is enabled by default in the CLI. |
| `--keep-frames` | Keep temporary extracted video frames. |
| `--many-faces` | Process every detected face rather than only one. |
| `--map-faces` | Enable source-to-target face mapping. |
| `--mouth-mask` | Apply the mouth-region mask during face swapping. |
| `--nsfw-filter` | Enable the optional NSFW filter. It is off by default. |
| `--video-encoder` | Output video encoder: `libx264` (default), `libx265`, or `libvpx-vp9`. |
| `--video-quality` | Video quality value from 0 to 51; the default is 18. |
| `--live-mirror`, `--live-resizable` | Configure live camera preview display. |
| `--max-memory` | Set the maximum memory amount in GB. |
| `-l`, `--lang` | UI language code; English is the default. |
| `-v`, `--version` | Print the application version. |

Provider names are derived from ONNX Runtime's available providers, so the choices differ by installation. The repository's `--help` output is the authoritative list for the current environment.

## Repository layout

```text
run.py                         Application entry point
requirements.txt               Python dependencies
run-cuda.bat                   Windows CUDA launcher
run-directml.bat               Windows DirectML launcher
modules/core.py                CLI, startup checks, and processing orchestration
modules/ui.py                  Desktop interface and live camera preview
modules/face_analyser.py       Face analysis and face mapping
modules/processors/frame/       Face swapper and face enhancer processors
models/instructions.txt        Model download sources
locales/                       UI translation files
media/                         GIF media files
CONTRIBUTING.md                Collaboration and pull-request guidance
LICENSE                        GNU Affero General Public License v3
```

Video processing extracts frames to a temporary directory alongside the target video. Temporary frames are removed when processing finishes unless **Keep frames** / `--keep-frames` is enabled.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the repository's branch guidance and suggested checks for realtime face swapping, face mapping, camera listing, performance, and stability.

## License

This repository includes the **GNU Affero General Public License, version 3** in [`LICENSE`](LICENSE). Refer to that file for the complete license terms.

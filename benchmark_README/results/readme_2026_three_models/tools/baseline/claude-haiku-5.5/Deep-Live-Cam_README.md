# Deep-Live-Cam

Deep-Live-Cam is a Python application for real-time face swapping and face swapping on image and video files. It is distributed as the "GitHub Edition" of version 1.8 (see `modules/metadata.py`). It provides a Tkinter/CustomTkinter desktop interface and a headless command-line mode.

## Overview

The application can:

- Swap a face from a source image onto a target image or video. Processing for video extracts frames with FFmpeg, processes each frame, and reassembles the video.
- Run a live webcam preview that swaps faces in real time (the **Live** button).
- Enhance faces with GFPGAN through an optional Face Enhancer processor.
- Map multiple source faces to multiple target faces, using the **Map faces** option. Video mapping clusters face embeddings to identify unique people.
- Apply an optional mouth mask, with an optional visualization box.
- Filter NSFW content through the `--nsfw-filter` option, which uses `opennsfw2`.
- Keep or drop the original audio and frame rate, and choose the output video encoder and quality.
- Display its interface in several languages. Translation files are provided for German, Spanish, Finnish, Khmer, Korean, Brazilian Portuguese, Russian, Thai, and Chinese.

The project's README images in `media/` include demo GIFs, but their contents are not described here.

## Requirements

- **Python 3.9 or higher.** The application checks this at startup and exits if the version is older.
- **FFmpeg** available on the system `PATH`. The application checks for `ffmpeg` at startup and reports an error if it is missing. It also calls `ffprobe` to detect frame rates.
- **Python dependencies** listed in `requirements.txt`. The file includes `insightface`, `onnx`, `onnxruntime-gpu` (or `onnxruntime-silicon` on Apple Silicon), `opencv-python`, `customtkinter`, `torch`, `torchvision`, `tensorflow`, `opennsfw2`, and `protobuf`. It also points to the PyTorch CUDA 12.8 package index.
- **Optional hardware acceleration.** The execution provider is selected at runtime. Available options depend on the ONNX Runtime build installed.

## Setup

1. **Clone the repository** and enter its directory.

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download the models** and place them in the `models/` directory. `models/instructions.txt` lists the two files:

   - `inswapper_128_fp16.onnx` from `https://huggingface.co/hacksider/deep-live-cam/resolve/main/inswapper_128_fp16.onnx?download=true`
   - `GFPGANv1.4.pth` from `https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth`

   The Face Enhancer's `pre_check()` downloads `GFPGANv1.4.pth` into `models/` automatically if it is missing. The face swapper's `pre_check()` attempts a download as well, but it saves the file to the `modules/processors/frame/` directory, while the model is loaded from `models/`. Placing the file in `models/` manually is therefore the reliable approach.

4. **Launch the application** using `run.py` or one of the Windows batch files:

   - `run-cuda.bat`
   - `run-directml.bat`

   The contents of the batch files are not described in this README. Their names suggest CUDA and DirectML execution providers.

## Usage

### Graphical interface

Start the application without arguments:

```bash
python run.py
```

The main window provides the following controls:

- **Select a face** chooses the source image. The **↔** button swaps the source and target when both are images.
- **Select a target** chooses a target image or video.
- **Switches** control Keep fps, Keep frames, Face Enhancer, Keep audio, Many faces, Fix Blueish Cam, Map faces, Show FPS, Mouth Mask, and Show Mouth Mask Box.
- **Start** runs processing. If **Map faces** is enabled, a mapper window opens first. Otherwise, a save dialog asks for an output file.
- **Preview** shows a preview of the current frame, or of the first frame for a video. For videos, a slider selects the frame.
- **Live** opens a webcam preview. You choose the camera from the **Select Camera** menu.
- **Destroy** closes the application and cleans up temporary files.

UI preferences are saved to `switch_states.json` in the working directory.

### Headless mode

Passing `-s`, `-t`, or `-o` runs processing without the GUI:

```bash
python run.py -s source.jpg -t target.mp4 -o output.mp4
```

If `-o` names an existing directory, the output file is named `<source>-<target><extension>`. Images are processed directly. Videos are extracted to frames, processed, encoded, and then cleaned up.

### Command-line options

| Option | Description |
|---|---|
| `-s, --source` | Source image path |
| `-t, --target` | Target image or video path |
| `-o, --output` | Output file or directory |
| `--frame-processor` | Processors to run: `face_swapper`, `face_enhancer` (default: `face_swapper`) |
| `--keep-fps` | Keep the original frame rate |
| `--keep-audio` | Keep the original audio (default: on) |
| `--keep-frames` | Keep temporary frames |
| `--many-faces` | Process every face in the frame |
| `--nsfw-filter` | Filter NSFW images or videos |
| `--map-faces` | Map source and target faces |
| `--mouth-mask` | Apply the mouth mask |
| `--video-encoder` | `libx264` (default), `libx265`, or `libvpx-vp9` |
| `--video-quality` | Constant rate factor from 0 to 51 (default: 18) |
| `-l, --lang` | UI language code, such as `de`, `es`, or `ko` (default: `en`) |
| `--live-mirror` | Mirror the live camera display |
| `--live-resizable` | Make the live camera window resizable |
| `--max-memory` | Maximum RAM in GB (default: 16, or 4 on macOS) |
| `--execution-provider` | One or more providers. Choices come from the installed ONNX Runtime. Default: `cpu` |
| `--execution-threads` | Number of worker threads (default: 8, or 1 for DirectML and ROCm) |
| `-v, --version` | Print the name and version |

The options `-f/--face`, `--cpu-cores`, `--gpu-vendor`, and `--gpu-threads` are deprecated. The program still accepts them, prints a warning, and maps them to the newer options.

Press Ctrl+C to exit. The application handles `SIGINT` and cleans up temporary files for the target.

## Configuration

Configuration comes from three sources:

1. **Command-line arguments**, described above.
2. **Global defaults** in `modules/globals.py`. These include `keep_fps`, `keep_audio`, `video_encoder`, `mask_feather_ratio` (8), `mask_down_size` (0.50), and `mask_size` (1).
3. **Saved UI states** in `switch_states.json`, which the interface reads at startup.

Other settings:

- **Language:** Translation files live in `locales/` as JSON. Each file maps English strings to translated strings. The `-l` option selects one. The `en` code uses the built-in strings. Unrecognized codes print a "Language file not found" message.
- **Theme:** `modules/ui.json` defines the CustomTkinter theme colors and fonts for macOS, Windows, and Linux.
- **Metadata:** `modules/metadata.py` defines the application name, version, and edition shown in the window title.

## Development

### Project layout

- `run.py`: Entry point. It calls `modules.core.run()`.
- `modules/core.py`: Argument parsing, startup checks, resource limits, and the processing pipeline.
- `modules/ui.py`: The CustomTkinter interface and the source-target mapper windows.
- `modules/face_analyser.py`: Face detection using InsightFace `buffalo_l`. It also handles mapping and clustering for video frames.
- `modules/cluster_analysis.py`: K-means clustering for face embeddings.
- `modules/capturer.py` and `modules/video_capture.py`: Video frame reading and webcam capture. On Windows, the webcam module uses `pygrabber` to list devices.
- `modules/utilities.py`: FFmpeg wrappers, temporary directory management, and model download helpers.
- `modules/predicter.py`: NSFW prediction through `opennsfw2`.
- `modules/processors/frame/`: Frame processors. `face_swapper.py` uses InsightFace's `inswapper` model. `face_enhancer.py` uses GFPGAN. Both expose a shared interface that `core.py` checks at load time: `pre_check`, `pre_start`, `process_frame`, `process_image`, and `process_video`.
- `modules/gettext.py`: Loads locale JSON files.

### Temporary files

For a video target, frames are written to `temp/<target-name>/` next to the target file. The directory is removed after processing unless `--keep-frames` is set.

### Contributing

`CONTRIBUTING.md` describes the workflow:

- Push changes to the **`premain`** branch first. Tests run there. Changes move to **`main`** only after several hours or days of testing.
- Use the **`experimental`** branch for large or disruptive changes that need discussion before a merge into `main`.

The bug report template in `.github/ISSUE_TEMPLATE/bug_report.md` asks for a description, screenshots, the terminal error message, OS, GPU, and CPU. It also asks reporters to confirm that the issue is not a duplicate and is not a performance question.

### Type checking

`mypi.ini` contains mypy settings, including `disallow_untyped_defs`, `disallow_untyped_calls`, and `check_untyped_defs`. The file name is spelled `mypi.ini`, and mypy looks for `mypy.ini` by default, so you may need to pass the config file explicitly, for example `mypy --config-file mypi.ini`.

## Testing

No automated test suite is included in the supplied files. `CONTRIBUTING.md` defines a manual pre-pull-request checklist:

- **Functionality:** Test real-time face swap with the face enhancer enabled and disabled. Test Map faces with the option enabled and disabled. Confirm that all cameras are listed correctly.
- **Stability:** Confirm that real-time FPS does not drop. Confirm that boot time is not worse for the application or the real-time feature. Run for at least 15 minutes to check for GPU overload. Confirm that the interface stays responsive.

## Known gaps

The supplied files show a few dependency issues:

- `requirements.txt` does not list `gfpgan`, `scikit-learn`, `tqdm`, or `pygrabber`. These packages are imported by the code. `pygrabber` is used only on Windows.
- `tensorflow` is listed in `requirements.txt`, and `core.py` imports it.

Check these before you install on a fresh environment.

## License

This project is licensed under the **GNU Affero General Public License, version 3 (AGPL-3.0)**. The full text is in `LICENSE`. Under this license, you may run, modify, and redistribute the software. If you modify it and make it available to users over a network, you must offer those users the corresponding source code of your modified version.

The `LICENSE` file is the standard FSF text. It does not name the project's copyright holder, and the supplied files do not contain copyright notices for the project itself.

## Contact

The supplied files do not include contact details for the maintainers, either by email or by postal mail. For questions and bug reports, use the project's issue tracker, following the bug report template. The application's window also contains a "Deep Live Cam" link that opens `https://deeplivecam.net`.

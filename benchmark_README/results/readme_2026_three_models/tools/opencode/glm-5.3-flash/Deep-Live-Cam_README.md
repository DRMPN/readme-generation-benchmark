# Deep-Live-Cam

Real-time face swapping and one-click video face swaps using only a single source image. Deep-Live-Cam is an open-source deepfake tool built on [insightface](https://github.com/deepinsight/insightface) and [ONNX Runtime](https://github.com/microsoft/onnxruntime): pick a face, pick a target image, video, or webcam, and the selected face is swapped onto it — live or offline.

This is the **GitHub Edition**, version 1.8. The upstream project lives at [hacksider/Deep-Live-Cam](https://github.com/hacksider/Deep-Live-Cam).

![demo](media/demo.gif)
![live show](media/live_show.gif)

## Features

- **Image and video processing** — swap a face from a source image onto a target image or video.
- **Real-time camera preview** — apply the face swap to a live webcam feed from the GUI (*Live* mode, with camera selection).
- **Face Enhancer** — optional GFPGAN-based quality enhancement of swapped faces.
- **Many faces** — process every face found in the target, not just the most prominent one.
- **Map faces** — select specific source images for each individual face detected in the target.
- **Mouth mask** — keep the original mouth region of the target face (with an optional debug overlay).
- **NSFW filter** — refuse to process NSFW source/target content using OpenNSFW2.
- **Keep FPS / audio / frames** — preserve the original frame rate and audio track, and optionally keep the temporary extracted frames.
- **Color correction** — fix a blueish tint in the live camera feed (*Fix Blueish Cam*).
- **Output control** — choose the video encoder (`libx264`, `libx265`, `libvpx-vp9`) and quality (0–51).
- **Live options** — mirror the camera feed and/or make the live window resizable; show FPS in the preview.
- **GUI and headless mode** — a [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) desktop interface, or a fully command-line-driven mode.
- **Multilingual UI** — English (default), German, Spanish, Finnish, Khmer, Korean, Portuguese (Brazil), Russian, Thai, and Chinese.
- **Cross-platform** — Windows, macOS (including Apple Silicon), and Linux.

## Disclaimer

This software is intended as a productive contribution to the AI-generated media industry, helping artists with tasks like animating custom characters or using them as storyboards.

Users of this software are asked to use it responsibly and ethically:

- Do not use the software to create content that promotes violence, hatred, or defamation.
- Do not create misleading or fraudulent content of any kind.
- Do not use the software to harm or deceive other people.

The developers of this project are not responsible for users' actions or for any malicious use of the software. Users must ensure they comply with applicable local laws and obtain consent from the people whose likeness they use.

## Requirements

- **Python 3.9 or higher**
- **ffmpeg** (and `ffprobe`) — required and verified at startup
- The Python packages listed in [`requirements.txt`](requirements.txt)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hacksider/Deep-Live-Cam.git
   cd Deep-Live-Cam
   ```

2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Download the required models and place them in the [`models/`](models/) folder (see [`models/instructions.txt`](models/instructions.txt)); the application also attempts to download missing models on startup:

   - [`inswapper_128_fp16.onnx`](https://huggingface.co/hacksider/deep-live-cam/resolve/main/inswapper_128_fp16.onnx) (face swapper)
   - [`GFPGANv1.4.pth`](https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth) (face enhancer)

### Platform notes

- **Windows** — helper scripts are included: [`run-cuda.bat`](run-cuda.bat) launches with NVIDIA CUDA support and [`run-directml.bat`](run-directml.bat) with DirectML.
- **macOS** — `requirements.txt` automatically selects Apple Silicon–optimized packages (`onnxruntime-silicon`, pinned `torch`/`torchvision`) on ARM Macs.
- **GPU acceleration** — execution providers are provided by your installed ONNX Runtime build (e.g. `cpu`, `cuda`, `rocm`, `coreml`, `dml`).

## Usage

Launch the graphical interface:

```bash
python run.py
```

Typical GUI workflow:

1. Click **Select a face** and choose a source image containing a face.
2. Choose a mode:
   - **Image/video**: click **Select a target**, pick an image or video, then click **Start**.
   - **Live**: pick a camera under **Select Camera**, then click **Live** to run the swap on your webcam feed in real time.
3. Toggle features such as *Face Enhancer*, *Many faces*, *Map faces*, *Mouth Mask*, or *NSFW filter* as needed. Switch states are remembered between sessions.

You can also run the tool headlessly by passing a source and/or target on the command line:

```bash
# Face swap on an image
python run.py -s source.jpg -t target.jpg -o output.jpg

# Face swap on a video, keeping the original frame rate and audio
python run.py -s source.jpg -t target.mp4 -o output.mp4 --keep-fps --keep-audio

# Force a specific execution provider (NVIDIA CUDA example)
python run.py --execution-provider cuda
```

### Command-line options

| Option | Description | Default |
| --- | --- | --- |
| `-s`, `--source` | Source image path | — |
| `-t`, `--target` | Target image or video path | — |
| `-o`, `--output` | Output file or directory | — |
| `--frame-processor` | Pipeline of frame processors (`face_swapper`, `face_enhancer`) | `face_swapper` |
| `--keep-fps` | Keep the original frame rate | off |
| `--keep-audio` | Keep the original audio track | on |
| `--keep-frames` | Keep the temporary extracted frames | off |
| `--many-faces` | Process every face in the target | off |
| `--nsfw-filter` | Filter NSFW images/videos | off |
| `--map-faces` | Map source faces to target faces | off |
| `--mouth-mask` | Mask the mouth region | off |
| `--video-encoder` | Output video encoder (`libx264`, `libx265`, `libvpx-vp9`) | `libx264` |
| `--video-quality` | Output video quality (0–51) | `18` |
| `-l`, `--lang` | UI language | `en` |
| `--live-mirror` | Mirror the live camera display | off |
| `--live-resizable` | Make the live camera window resizable | off |
| `--max-memory` | Maximum RAM in GB | `16` (4 on macOS) |
| `--execution-provider` | Core execution provider(s); choices depend on the installed ONNX Runtime | `cpu` |
| `--execution-threads` | Number of execution threads | `8` (1 for `dml`/`rocm`) |
| `-v`, `--version` | Show the program version | — |

Passing `-s`/`-t`/`-o` switches the application into headless (no-GUI) mode.

## How It Works

- Faces in the source and target are detected and analysed with [insightface](https://github.com/deepinsight/insightface); the swap itself is performed by the `inswapper_128_fp16` ONNX model.
- For videos, frames are extracted with **ffmpeg**, processed by the selected frame processor pipeline (`face_swapper`, optionally `face_enhancer`), and reassembled with ffmpeg; the original audio track is then restored.
- For live mode, webcam frames are captured and swapped on the fly.
- The face enhancer uses [GFPGAN](https://github.com/TencentARC/GFPGAN) and, when `torch_tensorrt` is installed, can accelerate enhancement with TensorRT on CUDA devices.

### Project structure

```
.
├── run.py                     # Entry point
├── modules/                   # Core application code
│   ├── core.py                # CLI parsing, orchestration, headless mode
│   ├── ui.py                  # CustomTkinter GUI
│   ├── globals.py             # Shared runtime options
│   ├── utilities.py           # ffmpeg helpers, downloads, temp files
│   ├── face_analyser.py       # Face detection/mapping helpers
│   ├── video_capture.py       # Webcam capture abstraction
│   ├── predicter.py           # NSFW detection (OpenNSFW2)
│   ├── gettext.py             # UI translations
│   └── processors/frame/      # face_swapper.py, face_enhancer.py
├── models/                    # Place model files here
├── locales/                   # UI translations (JSON)
└── media/                     # Demo assets
```

## Localization

The UI language can be selected with `-l/--lang` (e.g. `python run.py -l de`). English is built in; additional languages are loaded from JSON files in [`locales/`](locales/): German (`de`), Spanish (`es`), Finnish (`fi`), Khmer (`km`), Korean (`ko`), Portuguese — Brazil (`pt-br`), Russian (`ru`), Thai (`th`), and Chinese (`zh`). Pull requests adding translations are welcome.

## Contributing

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request. In short: work targets the `premain` branch (large or disruptive changes go to `experimental`), and PRs must pass the listed functionality and stability checks (realtime FPS, boot time, GPU load, camera listing, etc.).

## Credits

Deep-Live-Cam builds on the work of many open-source projects, including:

- [insightface](https://github.com/deepinsight/insightface) and the `inswapper_128` model
- [GFPGAN](https://github.com/TencentARC/GFPGAN) (face enhancement)
- [OpenNSFW2](https://github.com/nateraw/opennsfw2) (NSFW filtering)
- [ONNX Runtime](https://github.com/microsoft/onnxruntime), [PyTorch](https://github.com/pytorch/pytorch), and [TensorFlow](https://github.com/tensorflow/tensorflow)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), [OpenCV](https://opencv.org/), and [ffmpeg](https://ffmpeg.org/)

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).

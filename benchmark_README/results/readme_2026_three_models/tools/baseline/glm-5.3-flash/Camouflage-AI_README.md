# Camouflage AI 🎥🤖

**AI-powered desktop tool for removing video backgrounds using YOLOv8 segmentation.**

Camouflage AI is a desktop application that replaces the background of any video using YOLOv8 instance segmentation. Select a video, choose a new background — a solid color, a custom image, or a blurred version of the original scene — and Camouflage AI composites the detected person onto it, frame by frame.

Built with Python, CustomTkinter, OpenCV, and Ultralytics YOLOv8.

## Features

- 🖥️ **Modern desktop GUI** — a clean CustomTkinter interface launched in dark mode with the blue color theme.
- 🎯 **Person-only segmentation** — uses the `yolov8n-seg` model, filtered to the `person` class (`classes=[0]`) with a confidence threshold of `0.4`.
- 🎨 **Three background modes**:
  - **Color** — pick any color with the native color chooser (default green, `#00FF00`, with a live color swatch preview).
  - **Image** — use any `.jpg` / `.jpeg` / `.png` image; it is automatically resized to match the video's frame dimensions.
  - **Blur** — apply a heavy Gaussian blur (99×99 kernel) to the original background while keeping the person sharp.
- ⚡ **Automatic GPU acceleration** — processing runs on CUDA if a compatible GPU is available, otherwise on CPU.
- 📊 **Live progress tracking** — a modal progress window with a progress bar updated for every processed frame.
- 🧵 **Non-blocking processing** — video processing runs on a background thread so the main window stays responsive.
- 📁 **Convenient output handling** — results are saved to the `output_videos/` folder, and a single click opens it in Windows Explorer, macOS Finder, or the Linux file manager.
- ⚠️ **Large-file warning** — videos larger than 200 MB trigger a warning that processing may be slow.

## Sample Files

The repository ships with a demonstration pair you can use to see the tool in action:

| File | Description |
|---|---|
| `Input video/sample video.mp4` | Sample input video |
| `Output video/sample video_color_bg.mp4` | Result produced with the **color** background mode |

## How It Works

The core pipeline lives in `process_video.py`:

1. The video is opened with OpenCV (`cv2.VideoCapture`), and its FPS, frame size, and frame count are read.
2. The YOLOv8n-seg model predicts segmentation masks for each frame, restricted to the `person` class.
3. The mask is binarized, resized to the frame dimensions if needed (`INTER_NEAREST`), and split into foreground/inverse masks.
4. The foreground person is isolated with a bitwise `AND`, then composited onto the chosen background:
   - **Color/Image** — the background layer is masked with the inverse mask and added to the foreground.
   - **Blur** — the frame is Gaussian-blurred, masked with the inverse mask, and added to the foreground.
5. Frames are written to an `.mp4` file using the `mp4v` codec via `cv2.VideoWriter`.

> **Note:** If no person is detected in a frame, the frame is copied through to the output unchanged. Per frame, the first returned mask (`masks.data[0]`) is used for compositing.

## Requirements

- **Python 3.8+** (`python_requires='>=3.8'` in `setup.py`)
- **Windows** is the primary target platform per the package classifiers, though the "Show Output Folder" action also includes macOS (`open`) and Linux (`xdg-open`) fallbacks.
- A **CUDA-capable GPU** is optional but strongly recommended for faster processing.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Vishnu-tppr/Camouflage-AI.git
   cd Camouflage-AI
   ```

2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   ```

3. Install the declared dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. **Important:** `process_video.py` also imports `torch` and `ultralytics` (the YOLOv8 framework), which are **not** listed in `requirements.txt`. Install them additionally:

   ```bash
   pip install torch ultralytics
   ```

   The `yolov8n-seg.pt` weights are loaded by the Ultralytics framework when processing starts.

Alternatively, install the project as a package (name `Camouflage-AI`, version `1.0.0`) via its `setup.py`:

```bash
pip install .
```

## Usage

Launch the GUI:

```bash
python "Camouflage AI.py"
```

Then follow this workflow:

1. **Select Video** — choose an input file (`.mp4`, `.avi`, `.mov`, `.mkv`, or any file). The selected file name and size are shown, with a warning for files over 200 MB.
2. **Choose a Background Type**:
   - **Color** — click *Choose Color* to open the color picker; the swatch shows the current color.
   - **Image** — click *Select Image* to choose a `.jpg`/`.jpeg`/`.png` background.
   - **Blur** — no extra configuration needed.
3. **Start Processing** — a modal progress window appears with a live progress bar. The main controls are disabled until processing finishes. The progress dialog is intentionally non-closable while work is in progress.
4. **Show Output Folder** — after completion, open `output_videos/` directly from the app.

The output file is saved as:

```
output_videos/<original-video-name>_<color|image|blur>_bg.mp4
```

Success and error outcomes are reported both in the status label and via message boxes.

## Configuration

There is no external config file; tuning is done in the source:

| Setting | Location | Default |
|---|---|---|
| YOLO model weights | `process_video.py` | `yolov8n-seg.pt` (the code notes you can switch to `yolov8x-seg.pt` for maximum accuracy on a powerful GPU) |
| Confidence threshold | `process_video.py` | `0.4` |
| Detected classes | `process_video.py` | `[0]` (person only) |
| Gaussian blur kernel | `process_video.py` | `(99, 99)` |
| Default background color | `Camouflage AI.py` | Green, `(0, 255, 0)` / `#00FF00` |
| Output folder | `Camouflage AI.py` | `output_videos/` |
| Output codec | `process_video.py` | `mp4v` |
| Appearance/theme | `Camouflage AI.py` | dark mode, blue theme |

## Project Structure

```
Camouflage-AI/
├── Camouflage AI.py          # CustomTkinter GUI application
├── process_video.py          # YOLOv8 background-removal pipeline
├── requirements.txt          # Declared dependencies
├── setup.py                  # Package metadata and install config
├── LICENSE                   # MIT license
├── Input video/
│   └── sample video.mp4      # Sample input
└── Output video/
    └── sample video_color_bg.mp4   # Sample result (color mode)
```

## Development

The GUI and the processing pipeline are cleanly separated, so the core function can be reused programmatically:

```python
from process_video import run_yolo_background_removal

success = run_yolo_background_removal(
    input_video="path/to/video.mp4",
    output_folder="output_videos",
    bg_type="color",            # "color" | "image" | "blur"
    bg_color=(0, 255, 0),       # RGB tuple (converted to BGR internally)
    bg_image_path=None,         # required when bg_type="image"
    progress_callback=None,     # callable receiving a 0–1 progress fraction
)
```

Behavior notes for contributors:

- The function returns `True` on success and `False` on failure, printing `[ERROR]`/`[INFO]` diagnostics to the console.
- It validates that the video opens, that frame dimensions are positive, and that the `VideoWriter` initializes; on failure it releases all OpenCV resources.
- The GUI calls this function from a daemon thread and marshals completion back to the UI thread via `after(0, ...)`.
- `requirements.txt` declares several packages that are not imported by the two core modules (e.g., `rembg`, `moviepy`, `matplotlib`, `scikit-image`, `tqdm`, `pyperclip`); they are available for additional or experimental functionality.

## Testing

This repository does not include an automated test suite, so verification is manual. A reasonable checklist:

1. Run the app and process the bundled `Input video/sample video.mp4` in each of the three background modes, confirming that three distinct outputs are produced in `output_videos/`.
2. Compare your color-mode result against the provided `Output video/sample video_color_bg.mp4`.
3. Confirm error handling:
   - Clicking *Start Processing* with no video selected shows an error dialog.
   - Selecting the **Image** mode without choosing an image shows an error dialog.
   - An unreadable/invalid video file results in a failure message and the UI re-enabling.
4. Select a file over 200 MB and confirm the large-file warning appears.
5. Verify that output videos open correctly and match the input's resolution and frame rate.

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright © 2025 Vishnu.

---

Built by 💖 Vishnu | Camouflage AI · Repository: [github.com/Vishnu-tppr/Camouflage-AI](https://github.com/Vishnu-tppr/Camouflage-AI) · Contact: vishnu.tppr@gmail.com

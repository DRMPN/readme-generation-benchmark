# Camouflage AI

Camouflage AI is a desktop application that removes or replaces the background of a video. It uses a YOLOv8 segmentation model to find people in each frame, keeps the person, and fills the rest of the frame with a solid color, a user-supplied image, or a blurred version of the original frame.

## Overview

The project has two main parts:

- **`Camouflage AI.py`** is a CustomTkinter graphical interface. It lets the user select a video, choose a background type, start processing, and open the output folder.
- **`process_video.py`** contains `run_yolo_background_removal()`, which reads the video frame by frame with OpenCV, runs YOLO segmentation, composites the result, and writes a new MP4 file.

The repository includes a sample input video (`Input video/sample video.mp4`) and a sample output (`Output video/sample video_color_bg.mp4`), which was produced with the color background option.

### Features

- Background options: solid color, custom image, or blur.
- Color selection through the system color chooser (default green, `#00FF00`).
- Image backgrounds in JPG, JPEG, or PNG format, resized to match the video frame size.
- Support for MP4, AVI, MOV, and MKV input files in the file picker.
- A progress window that updates while frames are processed.
- A warning in the status bar when the selected video is larger than 200 MB.
- A button that opens the output folder in Windows Explorer, macOS Finder, or the Linux `xdg-open` handler.

## Repository Structure

```
.
├── Camouflage AI.py        # CustomTkinter GUI (entry point)
├── process_video.py        # Video processing and segmentation logic
├── requirements.txt        # Dependency list
├── setup.py                # Packaging metadata
├── LICENSE                 # MIT License
├── Input video/
│   └── sample video.mp4
└── Output video/
    └── sample video_color_bg.mp4
```

## Requirements

The application imports the following packages:

- `customtkinter`
- `opencv-python`
- `numpy`
- `rembg`
- `pillow`
- `moviepy`
- `matplotlib`
- `scikit-image`
- `tqdm`
- `pyperclip`

`process_video.py` also imports `torch` and `ultralytics`. These two packages are not listed in `requirements.txt` or `setup.py`, so they must be installed separately. The code loads the model with `YOLO('yolov8n-seg.pt')`, and the weight file is not included in this repository.

The `setup.py` file declares `python_requires='>=3.8'` and classifiers for Python 3 and Microsoft Windows.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Vishnu-tppr/Camouflage-AI.git
   cd Camouflage-AI
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   ```

3. Install the dependencies. The `requirements.txt` file contains lines written as `pip install <package>`, so the most reliable approach is to install each package directly. Then install the packages used by `process_video.py` that are missing from the list:

   ```bash
   pip install customtkinter opencv-python numpy rembg pillow moviepy matplotlib scikit-image tqdm pyperclip
   pip install torch ultralytics
   ```

   Alternatively, `setup.py` can be used to install the declared dependencies with `pip install .`. This does not install `torch` or `ultralytics`.

4. Make sure the YOLOv8 segmentation weights (`yolov8n-seg.pt`) are available to Ultralytics when the program runs.

## Usage

Start the application from the project directory:

```bash
python "Camouflage AI.py"
```

The window is titled **Camouflage AI** and has a fixed size of 600×650 pixels. Follow these steps:

1. Click **Select Video** and choose a video file.
2. Choose a background type using the **Color**, **Image**, or **Blur** radio buttons.
   - **Color:** Click **Choose Color** to pick a color. The default is green.
   - **Image:** Click **Select Image** and choose a JPG, JPEG, or PNG file.
   - **Blur:** No extra input is needed. The background is blurred.
3. Click **Start Processing**. A progress window appears while frames are processed. The controls are disabled until processing finishes.
4. When processing completes, a success or error message is shown. Click **Show Output Folder** to open the results.

Processed videos are saved to an `output_videos` folder, which is created in the current working directory. The application does not create the `Output video` folder shown in the repository tree.

### Output File Naming

Output files use this pattern:

```
<input file name without extension>_<background type>_bg.mp4
```

For example, processing `sample video.mp4` with the color background produces `sample video_color_bg.mp4`.

## Configuration

Most settings are fixed in the source code. The table below lists the values that can be changed.

| Setting | Location | Default | Notes |
|---|---|---|---|
| Model weights | `process_video.py`, `YOLO('yolov8n-seg.pt')` | `yolov8n-seg.pt` | A code comment suggests `yolov8x-seg.pt` for higher accuracy on a powerful GPU. |
| Detection confidence | `process_video.py`, `conf=0.4` | `0.4` | Minimum confidence for a detection. |
| Detected class | `process_video.py`, `classes=[0]` | `0` (person) | Only the `person` class is segmented. |
| Blur strength | `process_video.py`, `cv2.GaussianBlur(frame, (99, 99), 0)` | 99×99 kernel | Larger odd values produce stronger blur. |
| Default color | `Camouflage AI.py`, `bg_color_rgb` and `bg_color_hex` | Green (`#00FF00`) | Changed through the **Choose Color** button. |
| Output folder | `Camouflage AI.py` and `process_video.py` | `output_videos` | Relative to the current working directory. |
| Large-file warning | `Camouflage AI.py` | 200 MB | Displays a warning in the status bar only. |
| Window size | `Camouflage AI.py` | 600×650 | The window is not resizable. |
| Appearance | `Camouflage AI.py`, `__main__` block | Dark mode, blue theme | Set with `ctk.set_appearance_mode` and `ctk.set_default_color_theme`. |

The code selects a CUDA device when `torch.cuda.is_available()` returns true and uses the CPU otherwise.

## How Processing Works

For each frame of the input video, `run_yolo_background_removal()` performs the following steps:

1. Runs YOLO segmentation on the frame, keeping only detections of the `person` class with confidence of at least 0.4.
2. Uses the first detected person mask. Other detected people are not included in the output.
3. Resizes the mask to the frame size if needed and converts it to a 3-channel image.
4. Keeps the pixels inside the mask from the original frame.
5. Fills the remaining area with the background:
   - **Color:** a solid fill with the chosen color.
   - **Image:** the selected image, resized to the frame size.
   - **Blur:** the original frame blurred with a Gaussian kernel.
6. Writes the composited frame to an MP4 file using the `mp4v` codec. The output uses the input video's frame rate and dimensions.

The function reports progress through a callback as a value from 0 to 1. The GUI uses this value to update the progress bar.

## Development

The project uses a flat layout. `Camouflage AI.py` contains the `CamouflageApp` class, which extends `customtkinter.CTk`. Processing logic is separate in `process_video.py` and can be called from other code. Its signature is:

```python
run_yolo_background_removal(
    input_video: str,
    output_folder: str,
    bg_type: str,              # 'color', 'image', or 'blur'
    bg_color: tuple = (0, 255, 0),   # RGB
    bg_image_path: str = None,
    progress_callback=None
) -> bool
```

The function returns `True` on success and `False` on failure. Errors are printed to the console.

Processing runs in a background thread so the GUI remains responsive. The GUI reads the video path, background type, color, and image path from its own state before starting the thread.

## Testing

The repository does not include a test suite or test files. Testing is currently manual. To check the processing pipeline, run the GUI with `Input video/sample video.mp4` and compare the result with `Output video/sample video_color_bg.mp4`, or call `run_yolo_background_removal()` directly with the sample file.

## Known Limitations

- Only the first detected person in each frame is kept. Other people are removed along with the background.
- The `setup.py` file reads `README.md` when building package metadata, but `README.md` was not part of the supplied files.
- `requirements.txt` uses `pip install` lines, so it cannot be passed directly to `pip install -r`.
- `torch` and `ultralytics` are used but not declared in `requirements.txt` or `setup.py`.
- The `setup.py` classifiers list Windows only, although the GUI code also handles macOS and Linux when opening the output folder.
- The video processing function reads the entire video frame by frame, so large files take a long time to process. The application warns about files over 200 MB.

## License

This project is licensed under the MIT License. Copyright (c) 2025 Vishnu. See the [LICENSE](LICENSE) file for the full text.

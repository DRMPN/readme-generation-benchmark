# Camouflage AI

Camouflage AI is a small desktop application that removes the background from a video and replaces it with a solid color, a custom image, or a blurred version of the original background. It uses a YOLOv8 segmentation model (via the Ultralytics library) to find people in each frame.

## Features

- Graphical interface built with CustomTkinter.
- Select an input video (`.mp4`, `.avi`, `.mov`, `.mkv`).
- Choose one of three background types:
  - **Color**: a solid fill. The default is green (`#00FF00`); you can pick another color.
  - **Image**: a `.jpg`, `.jpeg`, or `.png` file, resized to the video's frame size.
  - **Blur**: a Gaussian blur (99×99 kernel) of the original frame, used as the background.
- Progress bar while processing. Processing runs in a background thread so the window stays responsive.
- "Show Output Folder" button that opens the output folder in the system file browser.
- Warning in the status bar when the selected video is larger than 200 MB.

## How it works

For each frame of the input video, `process_video.py`:

1. Runs the YOLOv8 segmentation model `yolov8n-seg.pt` with a confidence threshold of 0.4, restricted to the COCO `person` class (class 0).
2. Takes the mask of the **first** detected person. Only one person's mask is used per frame.
3. Keeps the masked pixels from the original frame as the foreground.
4. Fills the remaining pixels with the chosen background (color, image, or blurred frame).
5. Writes the composited frame to the output video.

If no person is detected in a frame, the original frame is written unchanged.

The model runs on CUDA if PyTorch reports a GPU; otherwise it runs on CPU. The code prints which device it uses.

## Requirements

- Python 3.8 or newer (per `setup.py`).
- A Python environment with the packages listed below.
- Model weights: the code loads `yolov8n-seg.pt` by name. The weights are not included in this repository. Ultralytics normally downloads them automatically on first use, but this was not verified here.

### Python dependencies

The packages the code imports directly are:

- `customtkinter` (GUI)
- `opencv-python` (`cv2`, video reading/writing and image operations)
- `numpy`
- `Pillow` (`PIL`, background image loading)
- `torch` (PyTorch; used to choose CPU or CUDA)
- `ultralytics` (provides `YOLO` for segmentation)

`tkinter` is also required. It ships with most standard Python installs.

Note that `requirements.txt` and `setup.py` do not list every import. `torch` and `ultralytics` are used by `process_video.py` but are not declared in either file. `setup.py` also lists `rembg`, `moviepy`, `matplotlib`, `scikit-image`, `tqdm`, and `pyperclip`, which the current source files do not import. `requirements.txt` contains `pip install ...` lines rather than a list that `pip install -r` can read.

## Installation

Clone the repository and install the packages you need. At minimum:

```bash
git clone https://github.com/Vishnu-tppr/Camouflage-AI.git
cd Camouflage-AI
pip install customtkinter opencv-python numpy pillow torch ultralytics
```

Installing the repository with `pip install .` uses `setup.py`, which does not declare `torch` or `ultralytics`; you will need to install those separately.

## Usage

Run the application from the repository root, so that `process_video.py` can be imported:

```bash
python "Camouflage AI.py"
```

Then:

1. Click **Select Video** and choose an input video.
2. Choose a background type: **Color**, **Image**, or **Blur**.
   - For **Color**, click **Choose Color**.
   - For **Image**, click **Select Image**. Processing will not start without an image.
3. Click **Start Processing** and wait for the progress window to close.
4. Click **Show Output Folder** to open the results.

## Output

Results are written to an `output_videos` folder, created in the directory from which the application was started. Output files are named:

```
<input name>_<background type>_bg.mp4
```

For example, `sample video` processed with the Color background becomes `sample video_color_bg.mp4`. Output is always `.mp4`, encoded with the `mp4v` codec. The audio track of the input is not copied: the code writes only video frames with OpenCV.

## Project structure

```
Camouflage-AI/
├── Camouflage AI.py      # Tkinter/CustomTkinter GUI and entry point
├── process_video.py      # Frame-by-frame segmentation and compositing
├── setup.py              # setuptools packaging script
├── requirements.txt      # Dependency list written as pip install commands
├── LICENSE               # MIT License
├── Input video/
│   └── sample video.mp4  # Sample input
└── Output video/
    └── sample video_color_bg.mp4  # Sample output
```

The application writes to `output_videos/` (with an underscore), which is separate from the `Output video/` folder in the repository.

## Limitations

- Only people are segmented (COCO class 0). Other objects are not treated as foreground.
- Only the first detected person per frame is kept. If several people appear, the others are removed along with the background.
- Frames with no detection are passed through unchanged, so the original background appears in those frames.
- Segmentation is run independently on each frame with no temporal smoothing, so mask edges may flicker between frames.
- Audio is not preserved.
- Processing speed depends on hardware. No benchmarks are included.
- `setup.py` lists Windows as the only operating system classifier. The code also has macOS and Linux branches for opening the output folder, but no platform testing is documented in this repository.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Vishnu (vishnu.tppr@gmail.com)

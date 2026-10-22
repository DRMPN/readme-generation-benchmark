# Camouflage AI

Camouflage AI is a desktop application for replacing or blurring the background in a video while keeping the detected person in the foreground. It uses a YOLOv8 segmentation model to identify people, OpenCV to process video frames, and a CustomTkinter interface to select videos and backgrounds.

You can choose a solid color, an image, or a blurred version of the original background. Processing runs in a background thread, and the application displays progress and reports whether the task completed successfully.

## Features

- Select a video file in MP4, AVI, MOV, or MKV format.
- Replace the background with a chosen color or an image.
- Blur the video background.
- Use GPU acceleration when CUDA is available; otherwise, processing uses the CPU.
- View processing progress and open the output folder from the application.

The segmentation code filters for the person class and uses a confidence threshold of `0.4`. When multiple people are detected, it uses the first mask returned for a frame. The output is written as an MP4 video. The processing code does not mux the original audio into the output.

## Repository contents

- `Camouflage AI.py` — desktop application entry point.
- `process_video.py` — video segmentation and background replacement.
- `requirements.txt` — dependency installation commands.
- `setup.py` — Python package metadata and declared dependencies.
- `Input video/sample video.mp4` — sample input video.
- `Output video/sample video_color_bg.mp4` — sample output video.
- `LICENSE` — MIT License.

## Requirements

The package metadata specifies Python 3.8 or later. The project is classified for Windows, though the application includes platform-specific logic for opening the output folder on Windows, macOS, and Linux.

The project uses CustomTkinter, OpenCV, NumPy, rembg, Pillow, MoviePy, Matplotlib, scikit-image, tqdm, and pyperclip. The video-processing module also imports **PyTorch** and **Ultralytics**, which are not listed in `requirements.txt` or `setup.py`; install them separately so video processing can run.

## Setup

Create and activate a virtual environment using your preferred Python environment tool. For example, on Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies declared by the project and the additional video-processing dependencies:

```bash
python -m pip install .
python -m pip install torch ultralytics
```

Alternatively, install the packages listed in `requirements.txt` individually. That file contains `pip install ...` command lines rather than the usual package-per-line format accepted by `pip install -r requirements.txt`, and it does not include `torch` or `ultralytics`.

The processing code requests the `yolov8n-seg.pt` model when it starts. Ensure the model is available to the Ultralytics installation when processing a video.

## Usage

From the repository root, launch the graphical application:

```bash
python "Camouflage AI.py"
```

The application opens in dark mode. To process a video:

1. Click **Select Video** and choose a video file. The picker offers MP4, AVI, MOV, and MKV files.
2. Select a background type: **Color**, **Image**, or **Blur**.
3. For **Color**, click **Choose Color**. The default color is green (`#00FF00`).
4. For **Image**, click **Select Image** and choose a JPG, JPEG, or PNG file.
5. Click **Start Processing**. The application requires a video, and it also requires an image when the Image background is selected.
6. Wait for processing to finish. A progress window appears while the video is being processed.
7. Click **Show Output Folder** to open the output directory.

Generated files are written to `output_videos/` in the current working directory. The filename follows the pattern `<input-name>_<background-type>_bg.mp4`; for example, processing `sample video.mp4` with the color background produces `sample video_color_bg.mp4`. An image background is resized to the input video’s frame dimensions. The blur option applies a Gaussian blur to the original frame’s background.

The supplied example output is in `Output video/`, while the application writes new files to `output_videos/`.

## Configuration and implementation notes

The desktop interface lets you select the input video, background type, background color, and background image. The background color is selected through the system color chooser and passed to the processing function as RGB values. The processing code converts those values for OpenCV before creating the color background.

`process_video.py` exposes `run_yolo_background_removal`, which accepts an input video path, output folder, background type, optional RGB color, optional image path, and optional progress callback. It creates the output directory if needed and chooses CUDA when PyTorch reports that CUDA is available. The application itself uses `output_videos` as its output directory.

The model is initialized as `yolov8n-seg.pt`. The source also comments that `yolov8x-seg.pt` could be used instead, but changing the model may require greater computing resources. The application warns when a selected video is larger than 200 MB; this is an informational warning, not a processing limit.

## Development and testing

The application and processing logic are in separate Python files. When changing the interface, keep the call to `run_yolo_background_removal` aligned with that function’s parameters. When changing video processing, retain the expected Boolean success result because the interface uses it to display completion or failure messages.

No automated test suite or test configuration is included in the supplied repository. For a manual smoke test, launch the application, process the supplied sample video with each background type, and confirm that a corresponding MP4 appears in `output_videos/`. Also test an invalid or unreadable input and verify that the application reports failure rather than showing a success message.

## License

This project is distributed under the MIT License. See `LICENSE` for the complete license text. The license permits use, modification, distribution, sublicensing, and sale, subject to including the copyright and permission notice. The software is provided without warranty.

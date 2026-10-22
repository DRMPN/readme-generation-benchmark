# Camouflage AI

Camouflage AI is an AI-powered desktop tool for removing video backgrounds using YOLOv8 segmentation. It provides a graphical interface to replace the background of a video with a solid color, a custom image, or a blur effect.

## Features

- **Video Selection**: Supports common video formats such as `.mp4`, `.avi`, `.mov`, and `.mkv`.
- **AI-Powered Segmentation**: Uses YOLOv8 segmentation (`yolov8n-seg.pt`) to detect and isolate people in videos.
- **Background Options**:
  - **Color**: Replace the background with a solid color using a built-in color picker.
  - **Image**: Replace the background with a custom image, which is automatically resized to match the video dimensions.
  - **Blur**: Apply a Gaussian blur effect to the original background.
- **GPU Acceleration**: Automatically uses CUDA (if available) for faster processing, falling back to CPU otherwise.
- **Real-time Progress**: Displays a progress bar and status updates during video processing.
- **Output Management**: Saves processed videos to an `output_videos` folder, with a button to open it directly.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Vishnu-tppr/Camouflage-AI.git
   cd Camouflage-AI
   ```

2. **Install dependencies:**

   The core application requires the following packages (including `ultralytics` and `torch`, which are used by the processing logic):

   ```bash
   pip install customtkinter opencv-python numpy ultralytics torch pillow
   ```

   *Note: The `requirements.txt` file also lists additional packages such as `rembg`, `moviepy`, `matplotlib`, `scikit-image`, `tqdm`, and `pyperclip`.*

3. **Optional: GPU support**

   For faster performance, ensure CUDA is installed and configured for PyTorch.

## Usage

1. **Run the application:**

   ```bash
   python "Camouflage AI.py"
   ```

2. **Workflow:**
   - Click **Select Video** to choose a video file.
   - Select the background type (**Color**, **Image**, or **Blur**) and configure the option (pick a color or choose an image).
   - Click **Start Processing**. A progress window will track the processing status.
   - Once complete, the processed video will be saved in the `output_videos` folder with a suffix indicating the background type (e.g., `myvideo_color_bg.mp4`).

## Tech Stack

- **Language**: Python 3.8+
- **GUI**: CustomTkinter (Tkinter-based dark-mode interface)
- **AI/ML**: Ultralytics YOLOv8 (segmentation), PyTorch
- **Video/Image Processing**: OpenCV, NumPy, Pillow

## License

This project is licensed under the [MIT License](LICENSE).

Copyright (c) 2025 Vishnu

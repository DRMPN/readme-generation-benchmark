# Camouflage AI

Camouflage AI is a desktop application for replacing or blurring the background in a video. It uses YOLOv8 person segmentation to separate a person from each frame and offers three background treatments: a solid color, an image, or a blur of the original frame.

## Features

- Select a video and choose a background color, image, or blur effect.
- Process videos in a graphical interface with a progress indicator.
- Use a CUDA-capable GPU when PyTorch detects one; otherwise, processing uses the CPU.
- Save processed videos in the `output_videos` directory.

## Requirements

- Python 3.8 or newer (as declared in `setup.py`).
- The Python packages used by the application: CustomTkinter, OpenCV, NumPy, Pillow, PyTorch, and Ultralytics.
- A graphical desktop environment to run the GUI. A CUDA-enabled PyTorch installation is optional; without one, the application selects the CPU.

Install the runtime packages from the repository directory:

```bash
python -m pip install customtkinter opencv-python numpy pillow torch ultralytics
```

PyTorch installation options can vary by operating system and hardware. If you need CUDA support, follow the [official PyTorch installation instructions](https://pytorch.org/get-started/locally/) to choose a suitable command.

## Run

From the repository directory, launch the application with:

```bash
python "Camouflage AI.py"
```

## Use the application

1. Select a video. The file picker filters for MP4, AVI, MOV, and MKV files.
2. Choose **Color**, **Image**, or **Blur** as the background type.
   - **Color:** Choose a replacement color.
   - **Image:** Select a JPG, JPEG, or PNG image. The image is resized to the video's frame dimensions.
   - **Blur:** Blur the original frame behind the segmented person.
3. Select **Start Processing** and wait for the progress indicator to complete.
4. Find the result in `output_videos` in the current working directory. **Show Output Folder** opens that directory.

The output filename is `<input-name>_<background-type>_bg.mp4`. For example, processing `sample video.mp4` with the color background creates `sample video_color_bg.mp4`.

## Processing details and limitations

- The application loads the `yolov8n-seg.pt` segmentation model and runs person-class prediction with a confidence threshold of `0.4`.
- For each frame, it composites the first detected person mask. If no person mask is detected, that frame is written unchanged.
- Output is written as MP4 using OpenCV's `mp4v` codec, with the source video's frame dimensions and reported frame rate.
- Processing time depends on the video and available hardware. Large videos may take longer, especially when running on the CPU.

## Repository files

- `Camouflage AI.py` — desktop application and user interface.
- `process_video.py` — video segmentation and background compositing.
- `Input video/sample video.mp4` — sample input video included in the repository.
- `Output video/sample video_color_bg.mp4` — sample output video included in the repository.
- `requirements.txt` and `setup.py` — package and project metadata. The runtime install command above includes `torch` and `ultralytics`, which are imported by the processing code but are not listed in `requirements.txt`.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for the license text.

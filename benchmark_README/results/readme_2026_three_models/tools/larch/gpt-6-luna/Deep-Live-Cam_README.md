# Deep-Live-Cam

Deep-Live-Cam is a Python application for swapping a face in an image, video, or live camera feed. It includes a graphical interface, optional face enhancement, and support for different execution backends. Performance and available features depend on your hardware, installed dependencies, and model files.

> **Use responsibly.** Only use images and video you have the right to use, and get consent from anyone whose likeness you process. Do not use generated or altered media to mislead, harass, or impersonate people. Follow applicable laws and the project’s license.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Launch](#launch)
- [Using the application](#using-the-application)
- [Performance and execution providers](#performance-and-execution-providers)
- [Troubleshooting](#troubleshooting)
- [Project files](#project-files)
- [License](#license)

## Features

- Swap a face from a source image into a target image or video.
- Process a live camera feed, where supported by the selected backend and hardware.
- Use the optional face-enhancement processor.
- Choose between available CPU and GPU execution options.
- Use localized interface text. Translation files in the repository include German, Spanish, Finnish, Russian, Chinese, Korean, Brazilian Portuguese, Khmer, and Thai.

## Requirements

- A supported Python installation. Check the project’s dependency versions in `requirements.txt` if you encounter compatibility issues.
- A camera for live use.
- Model files required by the application. On first launch, the application may download required files or indicate where they should be placed; follow the messages shown by the application.
- For GPU execution, compatible hardware, drivers, and the corresponding runtime are required. CPU execution may work without a supported GPU, but can be substantially slower.

## Installation

### 1. Get the project

If you have Git installed:

```bash
git clone <repository-url>
cd Deep-Live-Cam-t4pxr3xc
```

Alternatively, download and extract the project, then open a terminal in the project directory.

### 2. Create a virtual environment

Using a virtual environment keeps the project’s Python packages separate from other projects.

**Windows (Command Prompt):**

```bat
py -m venv .venv
.venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS or Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If your system has multiple Python versions installed, use the version supported by the dependencies in `requirements.txt`.

### 3. Install dependencies

With the virtual environment active, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Some dependencies may require platform-specific GPU runtimes or system libraries. If installation fails, see [Troubleshooting](#troubleshooting).

## Launch

From the project directory, start the application with:

```bash
python run.py
```

On Windows, the repository also includes launcher scripts:

- `run-cuda.bat` — intended for systems configured for CUDA.
- `run-directml.bat` — intended for Windows systems using DirectML.

Choose the launcher that matches your setup. These scripts do not replace the need for compatible hardware, drivers, Python dependencies, or model files.

## Using the application

The exact controls may vary by version, but the usual workflow is:

1. **Start the application** using `python run.py` or a suitable Windows launcher.
2. **Choose a source face** — the image containing the face you want to use.
3. **Choose a target** — an image or video to process, or a camera for live use.
4. **Select processors and settings.** The face swapper performs the swap; the face enhancer is optional and may increase processing time.
5. **Preview and process** the target. For file-based processing, select an output destination if prompted.
6. **Review the result** before sharing it, and clearly disclose that it has been altered where appropriate.

Use clear, well-lit source images with a visible, unobstructed face for best results. Results can vary with pose, lighting, resolution, occlusion, and the number of faces in the target.

### Live camera use

Select the appropriate camera in the interface and start the live preview or processing session. Close other applications that may be using the camera if it is unavailable. Live performance depends heavily on the selected execution provider and the computer’s capabilities.

## Performance and execution providers

The application’s backend and available execution providers are determined by the installed dependencies and local hardware.

- **CPU:** A fallback option on many systems, but often slower for live processing.
- **CUDA:** For compatible NVIDIA GPUs with suitable drivers and runtime components.
- **DirectML:** A Windows option for supported graphics hardware.
- Other provider options may be available depending on the project version and installed packages.

If the application reports that a provider is unavailable, use a supported provider or install the matching runtime and dependencies. Do not assume that installing a GPU driver alone is sufficient.

## Troubleshooting

### The application does not start

- Run it from a terminal with the project’s virtual environment activated so you can see the full error message.
- Confirm that dependencies installed successfully:

  ```bash
  pip install -r requirements.txt
  ```

- Check that you are using a Python version supported by those dependencies.

### A model or weight file is missing

Follow any download or setup instructions printed at startup. If the application cannot retrieve a required file, check your network connection and consult the project’s instructions and release materials for the expected model files and locations.

### CUDA or DirectML is unavailable

- Confirm that your hardware supports the chosen provider.
- Check that the relevant drivers and runtime components are installed.
- Try launching with another available provider if the application offers one.
- Use the terminal output to identify the specific package or runtime error.

### Processing is slow or the preview is choppy

- Try a supported GPU provider.
- Close other GPU-intensive applications.
- Use smaller or lower-resolution input media where possible.
- Disable optional enhancement processing if speed is more important than output refinement.

### The camera is not detected

- Check operating-system camera permissions.
- Close video-call or recording applications that may be using the camera.
- Reconnect the camera and restart the application.

### Poor or inconsistent results

Use a clear source image, make sure the target face is visible, and try different source images when pose or lighting differs substantially. Face swapping is not guaranteed to work well for every image or video.

## Project files

Some notable files in the repository:

- `run.py` — application entry point.
- `ui.py`, `ui.json` — user-interface code and related UI data.
- `face_analyser.py`, `face_swapper.py`, `face_enhancer.py` — face analysis and processing components.
- `video_capture.py`, `capturer.py` — video and capture-related code.
- `utilities.py`, `globals.py`, `metadata.py`, `typing.py` — supporting code and shared definitions.
- `requirements.txt` — Python dependencies.
- `run-cuda.bat`, `run-directml.bat` — Windows launch scripts.
- `instructions.txt` — additional project instructions.
- `de.json`, `es.json`, `fi.json`, `ru.json`, `zh.json`, `ko.json`, `pt-br.json`, `km.json`, `th.json` — interface translations.
- GIF files in the project root — demonstrations and examples.

## License

See [`LICENSE`](LICENSE) for the terms that apply to this project. Check the licenses and usage terms for any separately downloaded models or other assets as well.

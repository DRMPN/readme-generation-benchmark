# Python Weather Info App

A Python desktop application for viewing weather information. The repository includes the application, a configuration module, and image assets used by the interface.

## Contents

- `weather_app.py` — application entry point
- `config.py` — application configuration
- `requirements.txt` — Python dependencies
- `background.png`, `search_icon.png`, `weather.ico` — interface assets
- `screenshot.png` — application screenshot
- `LICENSE` — license terms

## Preview

![Weather app screenshot](screenshot.png)

## Requirements

- Python 3
- The packages listed in `requirements.txt`

The project does not specify a minimum Python version. If you encounter compatibility issues, check the versions supported by the installed dependencies.

## Installation

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Activate it with:

   - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
   - **macOS/Linux:** `source .venv/bin/activate`

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the application

From the project directory, run:

```bash
python weather_app.py
```

If your system uses `python3` to invoke Python, run:

```bash
python3 weather_app.py
```

## Configuration

Review `config.py` before running the app. It contains the project’s configuration settings. If the application requires an API key or other external-service credentials, configure them there according to the comments and settings in that file. Do not publish private credentials in a public repository.

## Troubleshooting

- **A dependency is missing:** Make sure the virtual environment is active and run `python -m pip install -r requirements.txt` again.
- **An image or icon does not appear:** Run the app from the project directory so its relative asset paths can resolve.
- **The app cannot retrieve weather information:** Check the configuration and any credentials or network requirements documented in `config.py` or the application source.

## License

See the [`LICENSE`](LICENSE) file for the terms governing use, modification, and distribution.

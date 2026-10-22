# Python Weather Info App

A desktop weather application that lets you search for any city and view its current weather conditions, with a custom icon, background image, and search button graphic.

> **Note:** This README was written from the file list alone. Sections marked with ⚠️ describe likely behavior and should be checked against `weather_app.py`, `config.py`, and `requirements.txt` before publishing.

![Screenshot](screenshot.png)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🔍 Search weather by city name
- 🌡️ Display current temperature, humidity, wind speed, and general conditions ⚠️
- 🖼️ Custom graphical interface with a background image and search icon
- 🪟 Custom window icon (`weather.ico`)
- ⚙️ Centralized settings (API key, units, default city) in `config.py` ⚠️

## Project Structure

```
Python-Weather-Info-App-drt3c9m5/
├── weather_app.py     # Main application: GUI and weather logic
├── config.py          # Configuration settings (API key, units, etc.)
├── requirements.txt   # Python package dependencies
├── weather.ico        # Window/taskbar icon
├── background.png     # Background image for the GUI
├── search_icon.png    # Icon used on the search button
├── screenshot.png     # Application screenshot (used in this README)
└── LICENSE            # Project license
```

| File | Description |
|------|-------------|
| `weather_app.py` | Entry point. Builds the user interface, handles user input, requests weather data, and displays results. |
| `config.py` | Stores configurable values such as the API key and measurement units. Keep private values out of version control. |
| `requirements.txt` | Lists the third-party packages needed to run the app. |
| `weather.ico` | Icon shown in the window title bar and taskbar. |
| `background.png` | Background image rendered behind the weather information. |
| `search_icon.png` | Image displayed on the search button. |
| `screenshot.png` | Preview of the application. |
| `LICENSE` | Terms under which the software may be used and distributed. |

## Prerequisites

- **Python 3.8 or higher** ⚠️
- **pip** (Python package installer)
- An active internet connection
- A weather data API key (for example, from [OpenWeatherMap](https://openweathermap.org/api)) ⚠️

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/Python-Weather-Info-App-drt3c9m5.git
   cd Python-Weather-Info-App-drt3c9m5
   ```

   Or download and extract the ZIP archive from GitHub.

2. **Create and activate a virtual environment** (recommended)

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Open `config.py` and set your values. A typical configuration looks like this:

```python
# config.py
API_KEY = "your_api_key_here"   # Your weather service API key
UNITS = "metric"                # "metric" (°C), "imperial" (°F), or "standard" (K)
DEFAULT_CITY = "London"         # City shown on startup
```

⚠️ **Security tip:** Do not commit a real API key to a public repository. Consider one of these approaches:

- Add `config.py` to `.gitignore` and provide a `config.example.py` template instead.
- Load the key from an environment variable:

  ```python
  import os
  API_KEY = os.getenv("WEATHER_API_KEY", "")
  ```

## Usage

Start the application from the project directory:

```bash
python weather_app.py
```

Then:

1. Type a city name into the search field (for example, `Paris` or `New York`).
2. Click the search button (magnifying glass icon) or press **Enter**.
3. View the current weather conditions for that city.

If a city cannot be found, the app displays an error message instead of crashing.

## How It Works

1. **Startup:** `weather_app.py` loads settings from `config.py` and creates the main window using the custom icon and background image.
2. **User input:** The search field accepts a city name, and the search button triggers a lookup.
3. **API request:** The app sends an HTTP request to the weather service with the city name, API key, and units. ⚠️
4. **Parsing:** The JSON response is parsed to extract temperature, humidity, wind speed, and conditions. ⚠️
5. **Display:** The results are rendered on top of the background image in the GUI.

## Customization

- **Change the default city or units:** Edit `DEFAULT_CITY` or `UNITS` in `config.py`.
- **Change the look:** Replace `background.png`, `search_icon.png`, or `weather.ico` with your own images. Keep the same filenames, or update the references in `weather_app.py`.
- **Adjust the window size or colors:** Modify the layout and style settings in `weather_app.py`. ⚠️

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|----------------|----------|
| `ModuleNotFoundError` | Dependencies are not installed | Run `pip install -r requirements.txt` inside your virtual environment. |
| "Invalid API key" or 401 error | API key is missing or incorrect | Check `API_KEY` in `config.py`. New keys may take a few hours to activate. |
| "City not found" | Misspelled city name or unsupported location | Check the spelling, or try adding the country code (for example, `London,GB`). |
| Images do not load | Image files are missing or the path is wrong | Run the app from the project folder, and confirm the image filenames are unchanged. |
| Window icon does not change | Icon files are not supported on this OS | `.ico` files work best on Windows. Use a different format on macOS or Linux. ⚠️ |
| No internet connection error | Network or firewall is blocking requests | Check your connection and firewall settings. |

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request.

Please keep changes focused and describe what you changed and why.

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.

---

*Made with Python.*

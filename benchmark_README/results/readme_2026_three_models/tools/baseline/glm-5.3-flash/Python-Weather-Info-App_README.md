# ☂ Weather Info — Python Weather App

A lightweight desktop weather application built with **Python**, **Tkinter**, and the **OpenWeatherMap API**. The app provides a simple graphical interface where users can search for any city worldwide and view current weather details, including temperature, humidity, pressure, wind speed, and sunrise/sunset times.

## Overview

Weather Info is a GUI-based weather application that fetches real-time weather data from the OpenWeatherMap API. When the app launches, it automatically loads the weather for a default city (New Delhi by default). Users can search for any other city by typing its name into the search bar and pressing Enter or clicking the Search button.

Key features:

- **Real-time weather data** — Fetches current conditions from the OpenWeatherMap API in metric units.
- **Detailed weather information** — Displays city, country, temperature, weather description, pressure, humidity, wind speed, sunrise, and sunset times.
- **Default city loading** — Shows weather for a configurable default city on startup.
- **Responsive background image** — The background image dynamically resizes with the window.
- **Threading** — Weather fetching runs in a background thread so the UI stays responsive while data loads.
- **Customizable UI** — Colors, fonts, borders, images, and the default city are all configurable via a single configuration file.

## Screenshots & Assets

The repository includes the following assets used by the application:

| File | Purpose |
|------|---------|
| `assets/background.png` | Default window background image |
| `assets/search_icon.png` | Icon displayed on the search button |
| `assets/weather.ico` | Application window icon |
| `assets/screenshot.png` | Screenshot of the running application |

## Project Structure

```
.
├── weather_app.py      # Main application (GUI + weather fetching logic)
├── config.py           # API keys and UI configuration settings
├── requirements.txt    # Python dependencies
├── assets/
│   ├── background.png  # Background image
│   ├── screenshot.png  # App screenshot
│   ├── search_icon.png # Search button icon
│   └── weather.ico     # Window icon
└── LICENSE             # MIT License
```

## Requirements

- Python 3.x
- Internet connection (to reach the OpenWeatherMap API)

Python dependencies (from `requirements.txt`):

- `requests` — used to call the OpenWeatherMap API
- `Pillow` (PIL) — used to load, resize, and display images in the Tkinter GUI

## Setup

1. **Clone the repository** (or download the source files):

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **(Optional but recommended) Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key:**

   The app uses the OpenWeatherMap Current Weather API. An API key placeholder is included in `config.py`:

   ```python
   API_KEY = "47abd6fca9faad069da778f0cdbb0b9c"
   BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
   ```

   For production use, obtain your own free API key from [OpenWeatherMap](https://openweathermap.org/api) and replace the value of `API_KEY` in `config.py`. The key in the repository is provided for demonstration and may be rate-limited or revoked.

5. **Run the application:**

   ```bash
   python weather_app.py
   ```

## Usage

1. Launch the app with `python weather_app.py`. A 500×400 window titled **"Weather Info"** opens, showing the weather for the default city (New Delhi).
2. Type a city name into the search box (placeholder: *"Enter city name here"*).
3. Press **Enter** or click the **Search** button.
   - While fetching, the button is disabled and displays *"Searching"*, and the info box shows a *"Loading"* message.
   - Once data arrives, the info box displays:
     - City and country
     - Temperature (°C)
     - Weather description
     - Pressure (hPa) and Humidity (%)
     - Wind speed (m/s)
     - Sunrise and sunset times (formatted as `HH:MM:SS`)
4. If the city is not found, the message *"Not Found. Please provide a valid city name."* is shown. If the request fails entirely, the app prompts you to provide a valid city name.

## Configuration

All user-adjustable settings live in **`config.py`**:

### API settings

| Setting | Description |
|---------|-------------|
| `API_KEY` | Your OpenWeatherMap API key |
| `BASE_URL` | Base URL for the OpenWeatherMap weather endpoint |

### Header (title) settings

| Setting | Description | Default |
|---------|-------------|---------|
| `HEADER_TOP_TEXT_SIZE` | Font size of the header text | `20` |
| `HEADER_TOP_TEXT_COLOR` | Color of the header text | `#000000` |
| `HEADER_TEXT_TOP_BORDER_THICKNESS` | Thickness of the header border | `2.5` |

### Search bar and button

| Setting | Description | Default |
|---------|-------------|---------|
| `SEARCH_BAR_BORDER_COLOR` | Border color of the city input box | `#FFFFFF` |
| `SEARCH_BUTTON_COLOR` | Background color of the search button | `#0068E5` |
| `SEARCH_BUTTON_TEXT_COLOR` | Text color of the search button | `#FFFFFF` |

### Images

| Setting | Description | Default |
|---------|-------------|---------|
| `DEFAULT_BACKGROUND_IMAGE` | Path to the background image | `assets/background.png` |
| `SEARCH_ICON_IMAGE` | Path to the search button icon | `assets/search_icon.png` |

### Weather info box

| Setting | Description | Default |
|---------|-------------|---------|
| `INFO_TEXT_COLOR` | Text color in the weather info box | `#000000` |
| `INFO_BORDER_THICKNESS` | Border thickness of the info box | `3` |

### Default city

| Setting | Description | Default |
|---------|-------------|---------|
| `DEFAULT_CITY` | City shown automatically at startup | `New Delhi` |

## Development Notes

- **GUI framework:** The app is built with Tkinter (`tk.Tk` main window, `Label`, `Entry`, and `Button` widgets placed with `place()` using relative positioning).
- **Threading:** Each search spawns a background thread (`threading.Thread`) running `get_weather()`, keeping the Tkinter event loop responsive during network calls. A simulated 3-second delay is included before the API request.
- **Image handling:** Pillow (`PIL.Image`, `PIL.ImageTk`) loads and resizes the background and search icon images. The background is re-rendered with LANCZOS resampling whenever the window is resized via the `resize_bg` handler bound to window resize events.
- **Error handling:** API failures and missing image files are handled gracefully — errors are shown in the info box or via a `messagebox` dialog rather than crashing the app.
- **Startup behavior:** `show_default_info()` is called before the main loop, so the default city's weather loads immediately on launch.

### Ideas for contributions/improvements

- Increase/adjust the simulated delay or remove it for faster lookups.
- Add forecast support, unit switching, or saved favorites.
- Move the API key to an environment variable instead of hard-coding it.

## Testing

This repository does not include an automated test suite. To verify the app manually:

1. Run `python weather_app.py` and confirm the window opens with the default city's weather.
2. Search for a known city (e.g., `London`) and confirm data appears.
3. Search for an invalid string (e.g., `xyzzy123`) and confirm the "Not Found" message is shown.
4. Resize the window and confirm the background image resizes accordingly.
5. Press Enter in the search box and click the Search button to confirm both trigger a search.

## License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Vishal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

*Code With ♥ By Vishal Sharma*

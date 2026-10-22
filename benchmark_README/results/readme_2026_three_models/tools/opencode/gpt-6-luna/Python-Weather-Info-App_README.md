# Weather Info

Weather Info is a Python desktop application built with Tkinter. It looks up current weather for a city through the OpenWeatherMap current-weather endpoint and displays the result in a small window.

![Weather Info application screenshot](assets/screenshot.png)

## Features

- Fetches weather for the default city, **New Delhi**, when the application starts.
- Search for another city with the **Search** button or by pressing **Enter** in the city field.
- Displays the city and country, temperature in °C, weather description, pressure in hPa, humidity in percent, wind speed in m/s, and sunrise and sunset times.
- Uses a bundled background image, search icon, and window icon.
- Allows several appearance options and the default city to be changed in `config.py`.

## Requirements

- Python with Tkinter available. Tkinter is part of many Python installations; on some Linux distributions it must be installed separately through the operating system's package manager.
- The Python packages listed in `requirements.txt`: `requests` and `Pillow`.
- An OpenWeatherMap API key with access to the configured current-weather endpoint.
- Internet access while retrieving weather data.

## Setup and run

Run these commands from the repository directory (the directory containing `weather_app.py`):

```bash
python -m venv .venv
```

Activate the virtual environment, then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Set `API_KEY` in `config.py` to an OpenWeatherMap API key, then start the application:

```bash
python weather_app.py
```

The application loads its images using paths relative to the current working directory, so run it from the repository directory. The existing `config.py` contains a hard-coded key; replace it with your own key, and rotate the existing key if you control it and it may have been exposed.

## Configuration

`config.py` contains the following settings:

| Setting | Purpose |
| --- | --- |
| `API_KEY` | OpenWeatherMap API key used for requests. |
| `BASE_URL` | Current-weather API URL. |
| `DEFAULT_CITY` | City queried when the application starts. |
| `HEADER_TOP_TEXT_SIZE`, `HEADER_TOP_TEXT_COLOR`, `HEADER_TEXT_TOP_BORDER_THICKNESS` | Header text size, color, and border thickness. |
| `SEARCH_BAR_BORDER_COLOR` | City-entry border highlight color. |
| `SEARCH_BUTTON_COLOR`, `SEARCH_BUTTON_TEXT_COLOR` | Search button background and text colors. |
| `DEFAULT_BACKGROUND_IMAGE`, `SEARCH_ICON_IMAGE` | Paths to the background and search icon images. |
| `INFO_TEXT_COLOR`, `INFO_BORDER_THICKNESS` | Weather information text color and border thickness. |

The request uses metric units. Sunrise and sunset values are formatted as `HH:MM:SS` using the computer's local time zone.

## Project files

- `weather_app.py` — Tkinter interface and weather request/display logic.
- `config.py` — API, default-city, image-path, and appearance settings.
- `requirements.txt` — Python package dependencies.
- `assets/` — Application background, search icon, window icon, and screenshot.
- `LICENSE` — MIT License.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE) for the license text.

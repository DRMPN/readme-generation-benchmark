# Weather Info

Weather Info is a desktop weather viewer written in Python with Tkinter. You type a city name, and the app queries the OpenWeatherMap current weather API and shows the temperature, conditions, pressure, humidity, wind speed, country, and sunrise and sunset times in a single window. On startup, it shows the weather for a configurable default city.

## Features

- Search for weather by city name, either with the **Search** button or the Enter key.
- Display of temperature (°C), weather description, pressure (hPa), humidity (%), wind speed (m/s), country code, sunrise time, and sunset time.
- A default city (`New Delhi` by default) that is loaded when the app starts.
- A "Loading" status message while a request is in progress, and a disabled, "Searching" search button during a lookup.
- Error messages for empty input, unknown cities, and failed requests.
- A background image that fills the window, plus a search icon on the button.
- Visual settings (colors, font sizes, border thicknesses, image paths) that can be changed in a single configuration file.

## Screenshot

![Weather Info screenshot](assets/screenshot.png)

## Project Structure

```
.
├── LICENSE              # MIT License
├── assets/
│   ├── background.png   # Default background image
│   ├── screenshot.png   # Screenshot of the application
│   ├── search_icon.png  # Icon shown on the Search button
│   └── weather.ico      # Window icon
├── config.py            # API settings and UI customization values
├── requirements.txt     # Python package dependencies
└── weather_app.py       # Main application script
```

## Requirements

- Python 3
- The Python packages listed in `requirements.txt`:
  - `requests`
  - `Pillow`
- Tkinter, which is used for the GUI. It is not listed in `requirements.txt`, so it must be available in your Python installation.
- An internet connection and an OpenWeatherMap API key.

No specific Python version is specified in the repository.

## Setup

1. Clone or download the repository and change into its directory.

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add your OpenWeatherMap API key. The repository's `config.py` contains an `API_KEY` value. Replace it with your own key, as the code comments indicate (`# Your OpenWeatherMap API Key`).

5. Run the application:

   ```bash
   python weather_app.py
   ```

The app must be run from the project directory, because image and icon paths such as `assets/background.png` are relative.

## Usage

1. When the window opens, the weather for the city in `DEFAULT_CONFIG.DEFAULT_CITY` (`New Delhi` by default) is loaded and displayed.
2. Click the city entry box, type a city name, and then either:
   - click the **Search** button, or
   - press **Enter**.
3. The app shows a "Loading" message, then displays the weather details. The city entry is updated to the city name returned by the API.
4. If the search box is empty, the info box displays "Enter city name to get weather info."
5. If the city is not found, the info box displays "Not Found. Please provide a valid city name."
6. If any other error occurs while fetching or parsing the data, the info box displays "Provide a valid city name to get info."

Note that the city entry is prefilled with the placeholder text "Enter city name here" when the app starts. You need to replace this text with a city name before searching.

## Configuration

All configurable values are in `config.py`. Changes take effect the next time you run the app.

| Setting | Default | Description |
|---|---|---|
| `API_KEY` | (a key is present in the file) | Your OpenWeatherMap API key |
| `BASE_URL` | `http://api.openweathermap.org/data/2.5/weather?` | Base URL of the current weather endpoint |
| `HEADER_TOP_TEXT_SIZE` | `20` | Font size of the title label |
| `HEADER_TOP_TEXT_COLOR` | `#000000` | Color of the title text |
| `HEADER_TEXT_TOP_BORDER_THICKNESS` | `2.5` | Border thickness of the title label |
| `SEARCH_BAR_BORDER_COLOR` | `#FFFFFF` | Border color of the city entry box |
| `SEARCH_BUTTON_COLOR` | `#0068E5` | Background color of the Search button |
| `SEARCH_BUTTON_TEXT_COLOR` | `#FFFFFF` | Text color of the Search button |
| `DEFAULT_BACKGROUND_IMAGE` | `assets/background.png` | Path to the background image |
| `SEARCH_ICON_IMAGE` | `assets/search_icon.png` | Path to the icon on the Search button |
| `INFO_TEXT_COLOR` | `#000000` | Text color of the weather info box |
| `INFO_BORDER_THICKNESS` | `3` | Border thickness of the weather info box |
| `DEFAULT_CITY` | `New Delhi` | City shown when the app starts |

The API request uses metric units (`units=metric`), so temperatures are shown in Celsius and wind speed in meters per second.

## How It Works

`weather_app.py` contains the following main parts:

- **`get_weather(city_name)`** shows a "Loading" message, waits for three seconds (`time.sleep(3)`), and requests `BASE_URL` with the city name, `API_KEY`, and `units=metric`. It reads the response fields (main, wind, weather, sys, and name) and updates the info label. Sunrise and sunset values are converted from Unix timestamps to `HH:MM:SS` local times.
- **`search_city()`** reads the city entry, disables the Search button, and runs `get_weather` in a background thread so the window stays responsive during the request.
- **`on_enter_press(event)`** calls `search_city()` when Enter is pressed in the city entry.
- **`set_background(image_path)`** opens the background image and sizes it to 500×400 pixels to match the default window size.
- **`show_default_info()`** calls `get_weather` with `DEFAULT_CITY` at startup.

The window is created with the title "Weather Info", a fixed initial geometry of 500×400, and the icon `assets/weather.ico`. Widgets are positioned with relative coordinates so they are centered horizontally.

## Development

- The application is a single script, `weather_app.py`, that builds the GUI at import time and runs `app.mainloop()` at the end.
- Visual and API settings belong in `config.py`, so you can adjust appearance without changing the logic.
- The code includes a `resize_bg(event)` function that resizes the background image to the window size, but no event binding in the current code calls it. The background therefore stays at the size set by `set_background`.
- The `requests` library is used for HTTP calls, and `Pillow` is used for image loading and resizing.

If you contribute changes, keep the configuration values in `config.py`, and keep the dependencies in `requirements.txt` up to date.

## Testing

The repository does not include any test files, test framework configuration, or test instructions. Testing is currently manual: run `python weather_app.py` and try valid city names, invalid city names, an empty search, and the Enter key.

## Known Limitations

- The API key is stored in plain text in `config.py`. If you publish a fork, consider replacing it with your own key and keeping it out of version control.
- `get_weather` calls `time.sleep(3)` before every request, which adds a three-second delay to each lookup, including the startup lookup. The startup lookup runs on the main thread, so the window may be unresponsive during that delay.
- The app depends on the OpenWeatherMap API and its response format. The code treats the response as successful unless `cod` is `404`, and most errors are reported with a generic message.
- The window icon is set with `iconbitmap` using a `.ico` file, which is a Tk method that is typically used with Windows icon files.

## License

This project is licensed under the MIT License. Copyright (c) 2024 Vishal. See the [LICENSE](LICENSE) file for the full text.

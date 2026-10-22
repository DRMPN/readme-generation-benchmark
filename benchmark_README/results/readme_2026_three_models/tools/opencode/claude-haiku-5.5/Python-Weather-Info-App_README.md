# Python Weather Info App

A simple desktop weather app written in Python with Tkinter. Enter a city name and the app fetches current weather conditions from the [OpenWeatherMap](https://openweathermap.org/) Current Weather API and displays them in a small graphical window.

![Screenshot of the Weather Info app](assets/screenshot.png)

## Features

- Search for current weather by city name, either with the **Search** button or the Enter key.
- Displays the following for the searched city:
  - City and country code
  - Temperature (°C)
  - Weather description
  - Pressure (hPa)
  - Humidity (%)
  - Wind speed (m/s)
  - Sunrise and sunset times (local time of the machine running the app)
- Loads weather for a default city (`New Delhi`) when the app starts.
- Shows a "Loading" message while data is fetched and disables the Search button during the request.
- Shows messages for an empty search, an unrecognized city, or a failed request.
- Uses a background image and a search icon from the `assets/` folder.

## Requirements

- Python 3
- An internet connection
- An OpenWeatherMap API key
- The Python packages listed in `requirements.txt`:
  - [`requests`](https://pypi.org/project/requests/) for HTTP calls to the API
  - [`Pillow`](https://pypi.org/project/Pillow/) for loading and resizing images
- Tkinter, which is included with most standard Python installations. On some Linux distributions it must be installed separately (for example, the `python3-tk` package).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/Python-Weather-Info-App.git
   cd Python-Weather-Info-App
   ```

   Replace the URL with the actual location of your copy of the repository.

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

All settings are in `config.py`.

### API key

The app reads its API key from `API_KEY` in `config.py`. The file in this repository contains a key value, but you should replace it with your own OpenWeatherMap key:

```python
API_KEY = "your_openweathermap_api_key"
```

Keep in mind that a key stored in a source file is visible to anyone who can access that file. If you publish your own copy of this project, do not commit a personal key.

### Other settings

| Setting | Default | Purpose |
| --- | --- | --- |
| `BASE_URL` | `http://api.openweathermap.org/data/2.5/weather?` | Base URL of the OpenWeatherMap current weather endpoint |
| `DEFAULT_CITY` | `"New Delhi"` | City shown when the app starts |
| `DEFAULT_BACKGROUND_IMAGE` | `"assets/background.png"` | Background image path |
| `SEARCH_ICON_IMAGE` | `"assets/search_icon.png"` | Icon shown on the Search button |
| `HEADER_TOP_TEXT_SIZE` | `20` | Font size of the title |
| `HEADER_TOP_TEXT_COLOR` | `"#000000"` | Title text color |
| `HEADER_TEXT_TOP_BORDER_THICKNESS` | `2.5` | Title border thickness |
| `SEARCH_BAR_BORDER_COLOR` | `"#FFFFFF"` | Search box border color |
| `SEARCH_BUTTON_COLOR` | `"#0068E5"` | Search button background color |
| `SEARCH_BUTTON_TEXT_COLOR` | `"#FFFFFF"` | Search button text color |
| `INFO_TEXT_COLOR` | `"#000000"` | Weather info text color |
| `INFO_BORDER_THICKNESS` | `3` | Weather info box border thickness |

Image paths are relative, so run the app from the project directory.

## Usage

Start the app from the project directory:

```bash
python weather_app.py
```

Then:

1. Type a city name in the search box (the box initially contains the text `Enter city name here`; replace it).
2. Click **Search** or press **Enter**.
3. Read the weather details in the info box. When the search succeeds, the search box is updated to the city name returned by the API.

If the city name is empty, the app asks you to enter one. If the city is not found, it shows `Not Found. Please provide a valid city name.` If the request fails for any other reason (for example, no connection or an invalid API key), it shows `Provide a valid city name to get info`.

## Project structure

```
.
├── assets/
│   ├── background.png     # Window background image
│   ├── search_icon.png    # Icon for the Search button
│   ├── screenshot.png     # Screenshot used in this README
│   └── weather.ico        # Window icon
├── config.py              # API key, URLs, default city, and display settings
├── LICENSE                # MIT License
├── requirements.txt       # Python dependencies
└── weather_app.py         # Main application (Tkinter GUI and API calls)
```

## How it works

- `weather_app.py` builds the Tkinter window, places the widgets, and runs the main loop.
- When you search, the app starts a background thread that requests `BASE_URL` with the city name, the API key, and `units=metric`.
- The response is parsed and the results are written to the info box.
- Before each request, the app waits 3 seconds (`time.sleep(3)`), a delay that is built into the code.

## Known limitations

- The API key is stored in plain text in `config.py`.
- The API URL uses plain `http://`, not `https://`.
- Every request includes a fixed 3-second delay.
- Any error, including an invalid API key, is shown with the generic "Provide a valid city name" message. Only a 404 response shows the "Not Found" message.
- The background image is scaled to 500×400 when loaded. A resize handler (`resize_bg`) is defined in `weather_app.py`, but it is not connected to any window event, so the background does not rescale when the window is resized.
- The app is not tested with an automated test suite. No tests are included in this repository.
- Weather data is only shown for the city name you type; the app does not use location services or store history.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

# Weather Info

Weather Info is a desktop weather application built with Python and Tkinter. It looks up current conditions for a city using the OpenWeatherMap weather endpoint and displays the results in a small graphical window. Weather values are requested in metric units.

The application loads weather information for **New Delhi** when it starts. You can search for another city using the text field and the **Search** button, or press Enter while the field is focused.

![Weather Info application screenshot](assets/screenshot.png)

## Features

- Search for a city by name.
- Display the city and country, temperature, weather description, pressure, humidity, wind speed, sunrise, and sunset.
- Show temperature in degrees Celsius and wind speed in metres per second.
- Load a background image, search icon, and application icon from the `assets/` directory.
- Customize the default city and a selection of interface text, colors, borders, and image paths in `config.py`.

## Requirements

- Python installed on your computer.
- The Python packages listed in `requirements.txt`:
  - `requests` for HTTP requests to the weather service.
  - `Pillow` for loading, resizing, and displaying images.
- Tkinter, used for the graphical interface. Tkinter is included with many Python installations, but may need to be installed separately on some systems.
- An internet connection to retrieve weather data.
- A valid OpenWeatherMap API key configured in `config.py`.

## Setup

1. Clone or download this repository, then open a terminal in the project directory. The directory should contain `weather_app.py`, `config.py`, `requirements.txt`, and the `assets/` folder.
2. Install the Python dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

   Depending on your system, you may need to use `python3` instead of `python`.

3. Open `config.py` and set `API_KEY` to an OpenWeatherMap API key you can use. The repository contains an API key directly in this file; configure your own key rather than relying on a key committed to a repository.
4. Confirm that the image files referenced in `config.py` exist under `assets/`. The application also loads `assets/weather.ico` directly when creating its window.
5. Start the application:

   ```bash
   python weather_app.py
   ```

   Use `python3 weather_app.py` if that is the command for your Python installation.

## Usage

When the window opens, the application requests weather data for the configured default city. Enter a city name in the input field and click **Search**, or press Enter. The button changes to **Searching** and is disabled while the application fetches data. After a successful lookup, the entry field is updated with the city name returned by the service, and the weather details appear in the information box.

If the city is not found, the information box displays a message asking for a valid city name. If the input is empty, the application prompts you to enter a city name. Other exceptions during lookup are handled with a general message asking for a valid city name.

The application includes a three-second delay before making the weather request. The weather endpoint URL and API key are used to form the request, with `units=metric` included.

## Configuration

Edit the values in `config.py` to adjust the application. The file currently provides these settings:

| Setting | Purpose |
| --- | --- |
| `API_KEY` | OpenWeatherMap API key used for requests. |
| `BASE_URL` | Base URL for the OpenWeatherMap current-weather endpoint. |
| `DEFAULT_CITY` | City requested when the application starts. |
| `HEADER_TOP_TEXT_SIZE` | Font size for the header text. |
| `HEADER_TOP_TEXT_COLOR` | Header text color. |
| `HEADER_TEXT_TOP_BORDER_THICKNESS` | Header border thickness. |
| `SEARCH_BAR_BORDER_COLOR` | Search field highlight and border color. |
| `SEARCH_BUTTON_COLOR` | Search button background color. |
| `SEARCH_BUTTON_TEXT_COLOR` | Search button text color. |
| `DEFAULT_BACKGROUND_IMAGE` | Path to the background image. |
| `SEARCH_ICON_IMAGE` | Path to the search button icon. |
| `INFO_TEXT_COLOR` | Text color for the weather information. |
| `INFO_BORDER_THICKNESS` | Border thickness for the information box. |

Image paths are relative to the project’s working directory when the application is launched. Keep the referenced assets available at those paths, or update the configuration to point to replacement images. The window icon path is set directly in `weather_app.py` to `assets/weather.ico`.

The API key is stored as a plain-text value in `config.py`. Do not publish a real key in a public copy of the project. If a key has been exposed, replace it with a key you control.

## Project layout

```text
.
├── LICENSE
├── assets/
│   ├── background.png
│   ├── screenshot.png
│   ├── search_icon.png
│   └── weather.ico
├── config.py
├── requirements.txt
└── weather_app.py
```

- `weather_app.py` defines the Tkinter interface, search behavior, weather request, and display of results.
- `config.py` contains the API and interface settings.
- `requirements.txt` lists the third-party Python dependencies.
- `assets/` contains the images used by the interface and the screenshot.
- `LICENSE` contains the project’s license terms.

## Development and testing

There is no automated test suite or test command included in the supplied project files. To check a change manually, install the dependencies, configure a valid API key, and run the application using the command above. Try the default-city lookup, a valid city search, an invalid city name, an empty search, and pressing Enter to submit a search. If changing image paths or styling, relaunch the application and verify that the window loads and displays the updated appearance.

Keep image files in place when testing: the background, search icon, and window icon are referenced by the application. The background-loading function displays an error dialog if its configured image cannot be found.

## License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for the complete terms. The license notice identifies Vishal as the copyright holder for 2024.

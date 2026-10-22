# Weather Info App

A lightweight desktop weather application built with Python and Tkinter. It fetches real-time weather data from the [OpenWeatherMap API](https://openweathermap.org/api) and displays it in a clean, customizable graphical interface.

## Features

- **Real-time Weather Data**: Fetches current weather details for any city worldwide using the OpenWeatherMap API.
- **Detailed Weather Information**: Displays the city, country, temperature (°C), weather description, pressure (hPa), humidity (%), wind speed (m/s), as well as sunrise and sunset times.
- **Responsive UI**: Uses threading to fetch data without freezing the GUI, and dynamically resizes the background image to fit the window.
- **Keyboard Support**: Search by pressing the Enter key or clicking the Search button.
- **Customizable Interface**: Configure colors, fonts, borders, background images, icons, and the default city through a simple configuration file.

## Screenshot

![App Screenshot](assets/screenshot.png)

## Requirements

- Python 3.x
- The following Python packages (listed in `requirements.txt`):
  - `requests`
  - `Pillow`

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd Python-Weather-Info-App
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application using Python:

```bash
python weather_app.py
```

Upon launching, the app automatically displays the weather for the default city (New Delhi). You can then enter any city name in the search bar and press **Enter** or click **Search** to fetch its weather data.

## Configuration

All customizable settings are located in `config.py`:

| Setting | Description |
| :--- | :--- |
| `API_KEY` | Your OpenWeatherMap API key |
| `BASE_URL` | The base URL for the OpenWeatherMap API |
| `DEFAULT_CITY` | The default city displayed on startup (e.g., `"New Delhi"`) |
| `HEADER_TOP_TEXT_SIZE` | Font size for the header text |
| `HEADER_TOP_TEXT_COLOR` | Color of the header text |
| `HEADER_TEXT_TOP_BORDER_THICKNESS` | Border thickness for the header |
| `SEARCH_BAR_BORDER_COLOR` | Border color for the search bar |
| `SEARCH_BUTTON_COLOR` | Background color of the search button |
| `SEARCH_BUTTON_TEXT_COLOR` | Text color of the search button |
| `DEFAULT_BACKGROUND_IMAGE` | Path to the background image (default: `assets/background.png`) |
| `SEARCH_ICON_IMAGE` | Path to the search button icon (default: `assets/search_icon.png`) |
| `INFO_TEXT_COLOR` | Text color for the weather info box |
| `INFO_BORDER_THICKNESS` | Border thickness for the weather info box |

> **Note:** To use the application with your own account, replace the `API_KEY` in `config.py` with your personal OpenWeatherMap API key.

## Project Structure

```
Python-Weather-Info-App/
│
├── assets/
│   ├── background.png       # Background image
│   ├── search_icon.png      # Search button icon
│   ├── screenshot.png       # App screenshot
│   └── weather.ico          # Window icon
├── config.py                # Configuration settings
├── weather_app.py           # Main application file
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Made with ♥ by **Vishal Sharma**

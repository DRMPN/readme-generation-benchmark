# Python-Weather-Info-App-5p4wuhkn

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project is a Python desktop application that retrieves current weather data for a user-specified city from the OpenWeatherMap API and displays it in a Tkinter-based graphical interface. It is aimed primarily at end users who want a simple desktop weather viewer, and secondarily at hobbyist developers who can adjust appearance and defaults through centralized configuration settings. Weather requests run in a background thread so the interface stays responsive while data is fetched. For setup and run instructions, see the Getting Started section.

---

## Core Features

- **Current weather lookup by city name**: search any city and instantly see temperature, weather description, pressure, humidity, wind speed, and sunrise/sunset times fetched from the OpenWeatherMap API.
- **Non-blocking weather fetches**: data is retrieved in a background thread, so the window stays responsive and shows a "Searching" state instead of freezing.
- **Customizable appearance and defaults**: central settings control header text, colors, fonts, background image, search bar style, and the default city shown at startup.
- **Polished desktop interface**: a Tkinter window with a resizable background image, search bar with Enter-key support, and an icon-enabled search button.
- **Graceful error handling**: invalid city names, API failures, and missing background images are reported through clear in-app messages instead of crashes.

---

## Installation

Install Python-Weather-Info-App-5p4wuhkn using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/Python-Weather-Info-App-5p4wuhkn
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

## Prerequisites

- Python 3 installed (the app uses the standard-library Tkinter GUI toolkit)
- The Python packages listed in `requirements.txt`: `requests` and `Pillow`
- Internet access, since the app fetches live data from the OpenWeatherMap API

## Setup and Run

1. **Install the dependencies** from the repository root:

```bash
   pip install -r requirements.txt
```

2. **Check the API configuration** in `config.py`. The app uses the `API_KEY` and `BASE_URL` values defined there to call the OpenWeatherMap current-weather API. If you use your own OpenWeatherMap account, replace the existing `API_KEY` value with your key.

3. **(Optional) Adjust defaults in `config.py`.** You can change the startup city via `DEFAULT_CITY` (currently `"New Delhi"`), as well as colors, font sizes, and the image paths for the background (`DEFAULT_BACKGROUND_IMAGE`) and search icon (`SEARCH_ICON_IMAGE`).

4. **Run the app** from the repository root:

```bash
   python weather_app.py
```

## Notes

- The window expects the icon and images referenced in `config.py` (e.g., `assets/weather.ico`, `assets/background.png`, `assets/search_icon.png`) to exist; a missing background image triggers an error dialog.
- In the app window, type a city name in the search box and press **Enter** (or use the search button). If the city is not found, the app shows a "Not Found" message.

---

## Architecture

The application is a simple monolithic desktop app built with Python and Tkinter.

- **Single main script (`weather_app.py`)**: Contains both the GUI (main window, title label, city entry, search button, background image) and the application logic, with no separation into layers or modules beyond configuration.
- **Centralized configuration (`config.py`)**: Holds user-adjustable settings such as the OpenWeatherMap API key and base URL, colors, fonts, image paths (e.g., `DEFAULT_BACKGROUND_IMAGE`, `SEARCH_ICON_IMAGE`), and the default city (`DEFAULT_CITY`). The UI code reads these values at startup.
- **Assets directory (`assets/`)**: Stores static resources used by the UI, including the background image, search icon, and window icon (`weather.ico`).

**Data and control flow:**
1. The user types a city name into the entry field and presses Enter or clicks the Search button, which triggers `search_city()`.
2. The search button is disabled while a background `threading.Thread` runs `get_weather()`, keeping the window responsive during the fetch.
3. `get_weather()` builds a request URL from `config.BASE_URL`, the city name, and `config.API_KEY`, then calls the OpenWeatherMap current-weather REST API via the `requests` library (metric units).
4. The JSON response is parsed to extract temperature, weather description, pressure, humidity, wind speed, and sunrise/sunset times, which are displayed in the info label.
5. Errors (city not found, network/parse failures) are handled by updating the info label with a message and re-enabling the search button.

Note: The API key is stored in plaintext in `config.py`; there is no additional service layer, database, or external component beyond the OpenWeatherMap API.

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Python-Weather-Info-App-5p4wuhkn repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Python-Weather-Info-App-5p4wuhkn,

        author = {README Benchmark},

        title = {Python-Weather-Info-App-5p4wuhkn repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
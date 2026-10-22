# Python-Weather-Info-App-b0dwopk7

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Python-Weather-Info-App is a desktop application that shows current weather conditions for a city entered by the user, using data from the OpenWeatherMap web service. It is intended for developers and end users who want a simple graphical weather viewer. Lookups run in a background thread so the window remains responsive while data is retrieved. The project provides a single graphical desktop interface; for runnable steps, see the Getting Started section.

---

## Core Features

- **City weather lookup:** Fetches current weather conditions from the OpenWeatherMap API for a city name entered by the user, so developers can check conditions without leaving the app.
- **Desktop GUI:** Provides a Tkinter window with a city search field, a search button, and a background image, giving a simple, self-contained way to view weather results.
- **Responsive lookups:** Runs each weather request in a background thread so the window is not blocked while data is fetched.
- **Centralized settings:** Keeps the API settings, default city, colors, sizes, and image paths in one configuration module, making them easy to change without editing the GUI code.

---

## Installation

Install Python-Weather-Info-App-b0dwopk7 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/Python-Weather-Info-App-b0dwopk7
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

**Prerequisites**

- Python 3
- An OpenWeatherMap API key
- The dependencies listed in `requirements.txt` (`requests` and `Pillow`). See `requirements.txt` for the full list.

**Steps**

1. Install the dependencies listed in `requirements.txt`.
2. Open `config.py` and set `API_KEY` to your OpenWeatherMap API key. `BASE_URL` is already set to the OpenWeatherMap weather endpoint.
3. Keep the `assets/` folder next to `weather_app.py`. The paths in `config.py` (`assets/background.png`, `assets/search_icon.png`) are relative, and `weather_app.py` loads `assets/weather.ico` directly.
4. Run `weather_app.py` to open the Weather Info window. The default city is set by `DEFAULT_CITY` in `config.py`.

> **Security note:** `config.py` currently contains a hardcoded API key. Before sharing or publishing this repository, remove the key from the file, replace it with a placeholder, and rotate the key if it has been exposed.

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Python-Weather-Info-App-b0dwopk7 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Python-Weather-Info-App-b0dwopk7,

        author = {README Benchmark},

        title = {Python-Weather-Info-App-b0dwopk7 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
# Python Weather Info App

A desktop weather application built with Python that provides real-time weather information with a clean, modern graphical user interface. Users can search for any city worldwide and instantly view current weather conditions, including temperature, humidity, wind speed, and more.

![App Screenshot](screenshot.png)

## ✨ Features

- 🔍 **City Search** — Look up current weather conditions for any city in the world
- 🌡️ **Temperature Display** — View current temperature in Celsius (or Fahrenheit)
- 💧 **Weather Details** — Includes humidity, wind speed, pressure, and weather descriptions
- 🖼️ **Graphical User Interface** — Modern, user-friendly interface with custom background and icons
- ⚙️ **Configurable** — API keys and settings are stored in a separate configuration file
- 🪟 **Native Desktop Icon** — Ships with a custom `weather.ico` application icon

## 📋 Requirements

- Python 3.7+
- An API key from [OpenWeatherMap](https://openweathermap.org/api) (free tier available)

## 🚀 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/Python-Weather-Info-App-w5oh191c.git
   cd Python-Weather-Info-App-w5oh191c
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key:**

   Open `config.py` and add your OpenWeatherMap API key:

   ```python
   API_KEY = "your_api_key_here"
   ```

   > 💡 Sign up at [openweathermap.org](https://openweathermap.org/api) to get a free API key.

## ▶️ Usage

Run the application:

```bash
python weather_app.py
```

1. Enter a city name in the search field.
2. Click the search icon (or press Enter).
3. View the current weather information displayed on the screen.

## 📁 Project Structure

```
Python-Weather-Info-App-w5oh191c/
├── weather_app.py      # Main application entry point and GUI
├── config.py           # Configuration (API key, settings)
├── requirements.txt    # Python dependencies
├── weather.ico         # Application window icon
├── search_icon.png     # Search button icon
├── background.png      # Application background image
├── screenshot.png      # App screenshot for documentation
└── LICENSE             # License information
```

## 🛠️ Built With

- **Python** — Core programming language
- **Tkinter / CustomTkinter** — GUI framework
- **Requests** — HTTP requests to the weather API
- **OpenWeatherMap API** — Weather data provider
- **Pillow (PIL)** — Image handling for icons and background

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the terms found in the [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather data API
- The Python community for excellent GUI and networking libraries

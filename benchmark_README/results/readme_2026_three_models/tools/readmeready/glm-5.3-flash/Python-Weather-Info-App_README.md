# Python-Weather-Info-App<h2>Description</h2>

<p>Python-Weather-Info-App is a desktop weather application built in Python using Tkinter. It provides a simple graphical interface where users can view current weather information for a city.</p>

<p>Key features:</p>

<ul>
<li><strong>Live weather data</strong>: Fetches current weather conditions from the <a href="https://openweathermap.org/api">OpenWeatherMap API</a>.</li>
<li><strong>City search</strong>: Users can enter any city name in a search bar and press the search button to retrieve its weather.</li>
<li><strong>Default city</strong>: On startup, the app displays weather information for a default city (<code>New Delhi</code>), which can be changed.</li>
<li><strong>Customizable UI</strong>: Appearance options such as text colors, border thickness, header font size, search bar/button styling, and background image paths are defined as configurable constants.</li>
<li><strong>Branding footer</strong>: A footer at the bottom of the window displays credit text ("Code With ♥ By Vishal Sharma").</li>
</ul>

<p>The app uses a single main window with a header, a search bar with a search button, a weather info box, and a footer. The main event loop (<code>app.mainloop()</code>) keeps the window running, and default weather info is shown as soon as the application loads.</p>
<h2>Requirements</h2>

<p>To run the Python-Weather-Info-App, you will need the following:</p>

<ul>
<li><strong>Python 3</strong> installed on your system.</li>
<li>An <strong>OpenWeatherMap API key</strong> — the app uses the OpenWeatherMap API (<code>http://api.openweathermap.org/data/2.5/weather?</code>) to fetch weather data. The API key is configured in the project's configuration file (<code>API_KEY</code> setting).</li>
<li><strong>Tkinter</strong> — the app's graphical user interface is built with Tkinter, which is included with standard Python installations.</li>
<li><strong>Internet connection</strong> — required to fetch live weather data from the OpenWeatherMap API.</li>
<li><strong>Asset files</strong> — the app expects the following image assets to be present:
<ul>
<li><code>assets/background.png</code> — the default background image.</li>
<li><code>assets/search_icon.png</code> — the icon used for the search button.</li>
</ul></li>
</ul>
<h2>Installation</h2>

<p>To get started with the Python-Weather-Info-App, follow these steps:</p>

<h3>1. Clone the Repository</h3>

<p><code>bash
git clone https://github.com/your-username/Python-Weather-Info-App.git
cd Python-Weather-Info-App
</code></p>

<h3>2. Install Dependencies</h3>

<p>The app uses Python with a Tkinter-based GUI. Tkinter is included with most standard Python installations. If it is not available on your system, install it using your package manager:</p>

<p>```bash</p>

<h1>Debian/Ubuntu</h1>

<p>sudo apt-get install python3-tk
```</p>

<h3>3. Configure the API Key</h3>

<p>The application uses the <a href="https://openweathermap.org/">OpenWeatherMap</a> API to fetch weather data. The API configuration is located in the project's configuration file:</p>

<p><code>python
API_KEY = "47abd6fca9faad069da778f0cdbb0b9c"  # Your OpenWeatherMap API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"  # Base URL for OpenWeather API
</code></p>

<p>You can use the included key or replace <code>API_KEY</code> with your own OpenWeatherMap API key. You can obtain a free API key by signing up at <a href="https://openweathermap.org/">OpenWeatherMap</a>.</p>

<h3>4. Run the Application</h3>

<p><code>bash
python main.py
</code></p>

<p>The app will launch and display weather information for the default city (<code>New Delhi</code>, configurable via the <code>DEFAULT_CITY</code> setting in the configuration file). You can then search for the weather of any other city using the search bar.</p>
<h2>Usage</h2>

<p>Once you have installed the dependencies and configured your API key, you can run the application:</p>

<p><code>bash
python main.py
</code></p>

<p>When the app launches, it will display the weather information for the default city (<code>New Delhi</code>, as configured in the code). You can enter any city name in the search bar and click the search button to fetch and display the current weather for that city.</p>

<p>The application runs in a Tkinter window and keeps running until you close it.</p>
<h2>Contributing</h2>

<p>Contributions are welcome! Since this project is released under the <a href="LICENSE">MIT License</a>, you are free to use, modify, and distribute the code.</p>

<p>If you'd like to contribute:</p>

<ol>
<li>Fork the repository.</li>
<li>Create a new branch for your feature or bug fix.</li>
<li>Make your changes and test them locally (the project depends on <code>requests</code> and <code>Pillow</code>).</li>
<li>Submit a pull request describing your changes.</li>
</ol>

<p>Please note that the <code>API_KEY</code> in the configuration is for personal use — do not commit or share your own OpenWeatherMap API key publicly.</p>
<h2>License</h2>

<p>This project is licensed under the MIT License.</p>

<p>Copyright (c) 2024 Vishal</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.</p>

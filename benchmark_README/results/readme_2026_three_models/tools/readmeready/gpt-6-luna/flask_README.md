# flask<h2>Description</h2>

<p>Flask is a lightweight WSGI web application framework for Python. It provides the foundations for building web applications, including request handling, routing, and template rendering, while allowing applications to add functionality through extensions. Its core dependencies include Werkzeug and Jinja.</p>
<h2>Requirements</h2>

<p>Flask requires Python 3.9 or newer. Its runtime dependencies are:</p>

<ul>
<li>Blinker 1.9.0 or newer</li>
<li>Click 8.1.3 or newer</li>
<li>ItsDangerous 2.2.0 or newer</li>
<li>Jinja 3.1.2 or newer</li>
<li>MarkupSafe 2.1.1 or newer</li>
<li>Werkzeug 3.1.0 or newer</li>
</ul>

<p>Optional dependencies are available through extras:</p>

<ul>
<li><code>async</code> installs <code>asgiref</code> 3.2 or newer.</li>
<li><code>dotenv</code> installs <code>python-dotenv</code>.</li>
</ul>
<h2>Installation</h2>

<p>Install Flask with pip:</p>

<p><code>bash
python -m pip install Flask
</code></p>

<p>Optional extras are available for async support and loading environment variables from <code>.env</code> files:</p>

<p><code>bash
python -m pip install "Flask[async]"
python -m pip install "Flask[dotenv]"
</code></p>
<p>I’ll inspect the repository’s README and application code to determine the project’s documented usage and supported commands.</p>

<h2>Usage</h2>

<p>Create a file named <code>hello.py</code> with a Flask application:</p>

<p>```python
from flask import Flask</p>

<p>app = Flask(<strong>name</strong>)</p>

<p>@app.route("/")
def hello():
    return "Hello, World!"
```</p>

<p>Start Flask’s development server from the same directory:</p>

<p><code>console
flask --app hello run
</code></p>
<h2>Contributing</h2>

<p>See the Pallets contributing documentation for ways to contribute, including reporting issues, requesting features, asking or answering questions, and making pull requests.</p>
<h2>License</h2>

<p>Flask is distributed under the BSD-3-Clause License. Copyright 2010 Pallets. See <code>LICENSE.txt</code> for the license terms.</p>

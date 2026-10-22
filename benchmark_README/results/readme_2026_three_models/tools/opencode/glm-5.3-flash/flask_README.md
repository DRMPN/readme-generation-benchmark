# Flask

A simple framework for building complex web applications.

Flask is a lightweight [WSGI](https://wsgi.readthedocs.io/) web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around [Werkzeug](https://werkzeug.palletsprojects.com/) and [Jinja](https://jinja.palletsprojects.com/), and has become one of the most popular Python web application frameworks.

Flask offers suggestions, but doesn't enforce any dependencies or project layout. It is up to the developer to choose the tools and libraries they want to use. There are community-maintained extensions that add more functionality.

## Installation

Install Flask with `pip` inside a virtual environment:

```sh
pip install Flask
```

Flask supports Python 3.10 and newer.

### Dependencies

These distributions are installed automatically when installing Flask:

- [Werkzeug](https://palletsprojects.com/p/werkzeug/) implements WSGI, the standard Python interface between applications and servers.
- [Jinja](https://palletsprojects.com/p/jinja/) is a template language that renders the pages your application serves.
- [MarkupSafe](https://palletsprojects.com/p/markupsafe/) comes with Jinja. It escapes untrusted input when rendering templates to avoid injection attacks.
- [ItsDangerous](https://palletsprojects.com/p/itsdangerous/) securely signs data to ensure its integrity. This is used to protect Flask's session cookie.
- [Click](https://palletsprojects.com/p/click/) is a framework for writing command line applications. It provides the `flask` command and allows adding custom management commands.
- [Blinker](https://blinker.readthedocs.io/) provides support for signals.

### Optional dependencies

These distributions will not be installed automatically. Flask will detect and use them if you install them:

- [asgiref](https://asgi.readthedocs.io/) is required for `async def` views (`pip install Flask[async]`).
- [python-dotenv](https://github.com/theskumar/python-dotenv#readme) enables support for environment variables from `.env` files when running `flask` commands (`pip install Flask[dotenv]`).
- [Watchdog](https://pythonhosted.org/watchdog/) provides a faster, more efficient reloader for the development server.
- [greenlet](https://greenlet.readthedocs.io/) is required when using gevent or eventlet with your application.

## A Simple Example

Save this as `hello.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

Run it with the `flask` command:

```sh
$ flask --app hello run
 * Serving Flask app 'hello'
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

Then visit http://127.0.0.1:5000/ in your browser to see the hello world greeting. This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production.

## Documentation

The full documentation is available at [flask.palletsprojects.com](https://flask.palletsprojects.com/), including a user's guide, a tutorial that shows how to create a small but complete application, common patterns, a deployment guide, and the full API reference.

## Contributing

See the contributing guide in the documentation for how to set up a development environment and submit changes. Development is managed with `tox` (tests, style, typing, and docs environments), and the test suite uses `pytest`. The development dependencies are managed with [uv](https://docs.astral.sh/uv/).

## Links

- Documentation: <https://flask.palletsprojects.com/>
- Changes: <https://flask.palletsprojects.com/page/changes/>
- Source code: <https://github.com/pallets/flask/>
- Pallets chat: <https://discord.gg/pallets>
- Donate: <https://palletsprojects.com/donate>

## License

Flask is licensed under the BSD-3-Clause license. See the `LICENSE.txt` file for details.

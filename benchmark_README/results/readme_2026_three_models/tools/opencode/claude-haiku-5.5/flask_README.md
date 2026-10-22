# Flask

Flask is a lightweight WSGI web application framework for Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

- Documentation: <https://flask.palletsprojects.com/>
- Changes: <https://flask.palletsprojects.com/page/changes/>
- Source code: <https://github.com/pallets/flask/>
- Discord chat: <https://discord.gg/pallets>

Flask is maintained by [Pallets](https://palletsprojects.com/) and licensed under the BSD-3-Clause license.

## Requirements

Flask supports Python 3.10 and newer.

Installing Flask also installs these required dependencies:

- [Werkzeug](https://palletsprojects.com/p/werkzeug/): WSGI toolkit.
- [Jinja](https://palletsprojects.com/p/jinja/): template engine.
- [MarkupSafe](https://palletsprojects.com/p/markupsafe/): escapes untrusted input in templates.
- [ItsDangerous](https://palletsprojects.com/p/itsdangerous/): signs data, including the session cookie.
- [Click](https://palletsprojects.com/p/click/): command line interface, provides the `flask` command.
- [Blinker](https://blinker.readthedocs.io/): signal support.

Optional extras:

- `async`: installs `asgiref`, for running async views.
- `dotenv`: installs `python-dotenv`, for loading `.env` and `.flaskenv` files with the `flask` command.

## Installation

Create and activate a virtual environment, then install Flask.

macOS/Linux:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install Flask
```

Windows:

```bat
py -3 -m venv .venv
.venv\Scripts\activate
pip install Flask
```

To install the optional extras:

```sh
pip install "Flask[async,dotenv]"
```

## Quick start

Save this as `hello.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

Run the development server:

```sh
flask --app hello run
```

Then open <http://127.0.0.1:5000/> in a browser.

If you name your file `app.py` or `wsgi.py`, you can omit `--app`. You can also run Flask with `python -m flask`.

The built-in server is intended for development and testing, not production. See the [deployment options](https://flask.palletsprojects.com/deploying/) in the documentation.

### Debug mode

Use `--debug` to enable the reloader and the interactive debugger:

```sh
flask --app hello run --debug
```

The debugger allows running arbitrary Python code from the browser. Do not use the development server or debugger in production.

By default the server listens only on `127.0.0.1`. To make it reachable from other machines on your network, pass `--host=0.0.0.0`, and only do so when the debugger is disabled or you trust the network.

## Command line

The `flask` command provides subcommands, including:

- `flask run`: start the development server.
- `flask shell`: open an interactive shell within the application context.
- `flask routes`: list the application's routes.

Custom commands can be added with Click. See the [CLI documentation](https://flask.palletsprojects.com/cli/).

## Documentation

The full documentation covers:

- A [tutorial](https://flask.palletsprojects.com/tutorial/) that builds a small complete application.
- [Templating](https://flask.palletsprojects.com/templating/), [configuration](https://flask.palletsprojects.com/config/), [views](https://flask.palletsprojects.com/views/), [blueprints](https://flask.palletsprojects.com/blueprints/), [signals](https://flask.palletsprojects.com/signals/), and [error handling](https://flask.palletsprojects.com/errorhandling/).
- [Testing](https://flask.palletsprojects.com/testing/), [logging](https://flask.palletsprojects.com/logging/), and [debugging](https://flask.palletsprojects.com/debugging/).
- [Common patterns](https://flask.palletsprojects.com/patterns/) and [web security](https://flask.palletsprojects.com/web-security/).
- [Deployment](https://flask.palletsprojects.com/deploying/) guides.
- The [API reference](https://flask.palletsprojects.com/api/).

Examples in this repository:

- [`examples/javascript`](examples/javascript/): posting form data and handling JSON responses with `fetch`, `XMLHttpRequest`, and `jQuery.ajax`.

## Development

Clone the repository and install the development environment with [uv](https://docs.astral.sh/uv/), which uses the committed `uv.lock`:

```sh
git clone https://github.com/pallets/flask.git
cd flask
uv sync
```

Run the test suite:

```sh
pytest
```

The project uses [tox](https://tox.wiki/) for its test, style, typing, and documentation environments. Some of the configured environments are:

- `tox -e py3.13` (or another supported `py3.x`): run the tests on a specific Python version.
- `tox -e style`: run all pre-commit hooks.
- `tox -e typing`: run mypy and pyright.
- `tox -e docs`: build the documentation into `docs/_build/dirhtml`.
- `tox -e docs-auto`: rebuild the documentation continuously and serve it locally.

Continuous integration runs the tests on Linux, Windows, and macOS across the supported Python versions, plus PyPy, minimum dependency versions, and development versions of dependencies, along with a typing check.

Contributions are welcome. See the [contributing guide](https://palletsprojects.com/contributing/) for reporting issues, requesting features, and submitting pull requests. Report security vulnerabilities privately through a [GitHub security advisory](https://github.com/pallets/flask/security/advisories/new), not in a public issue.

## License

Flask is licensed under the BSD-3-Clause license. See [LICENSE.txt](LICENSE.txt) for details.

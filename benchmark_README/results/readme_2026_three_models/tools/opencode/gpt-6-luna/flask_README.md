# Flask

Flask is a lightweight WSGI web application framework for Python. It provides
the essentials for building web applications while leaving project structure
and many technology choices to the developer. It can be used for small
applications and extended for more complex ones.

Flask is maintained by Pallets. It builds on Werkzeug for WSGI and HTTP
utilities, Jinja for templates, and Click for its command-line interface.

## Requirements

Flask supports Python 3.10 and newer. Installing Flask also installs its
required dependencies: Werkzeug, Jinja, MarkupSafe, ItsDangerous, Click, and
Blinker.

## Installation

Install Flask from PyPI, preferably in a virtual environment:

```console
python -m pip install Flask
```

Optional dependencies can be installed with extras:

```console
python -m pip install 'Flask[async]'   # async view support
python -m pip install 'Flask[dotenv]'  # .env support for the Flask CLI
```

## Quick start

Save the following as `hello.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "<p>Hello, World!</p>"
```

Run it locally with Flask's development server:

```console
flask --app hello run
```

Open <http://127.0.0.1:5000/> to see the response. The `flask` command can
also discover applications named `app.py` or `wsgi.py` without an explicit
`--app` option. See the [Quickstart](https://flask.palletsprojects.com/quickstart/)
for routing, templates, request data, JSON responses, sessions, and more.

The built-in server and interactive debugger are for local development only;
do not use them in production. Use a production WSGI server or hosting platform
to deploy an application. See the [deployment documentation](https://flask.palletsprojects.com/deploying/).

## Documentation

- [Flask documentation](https://flask.palletsprojects.com/)
- [Installation guide](https://flask.palletsprojects.com/installation/)
- [Tutorial](https://flask.palletsprojects.com/tutorial/)
- [API reference](https://flask.palletsprojects.com/api/)
- [Changes](https://flask.palletsprojects.com/changes/)

The tutorial builds a small blog application and introduces application
factories, database access, views, templates, testing, and deployment. Flask
also supports community-maintained extensions for additional functionality.

## Development

This repository uses `uv` and includes a `uv.lock` file. With `uv` installed,
set up the project environment and run the test suite with:

```console
uv sync
uv run pytest
```

The tests are in `tests/`. The project also defines tox environments for
style checks, type checks, and documentation builds; see `pyproject.toml` for
the available commands and dependencies.

For contribution guidance, see the [Pallets contributing documentation](https://palletsprojects.com/contributing/).

## License

Flask is distributed under the BSD-3-Clause license. See [LICENSE.txt](LICENSE.txt)
for the full license text.

# Flask

Flask is a Python web application framework for building web applications. It provides a WSGI application object, URL routing, request and application contexts, template rendering with Jinja, sessions, JSON support, error handling, and a command-line interface. Blueprints help organize reusable application components, and extensions can add functionality.

This repository contains Flask’s source code, documentation, tests, and example applications. The project metadata identifies this checkout as version `3.2.0.dev` and requires Python 3.10 or newer.

- **Documentation:** https://flask.palletsprojects.com/
- **Source:** https://github.com/pallets/flask/
- **Changes:** https://flask.palletsprojects.com/page/changes/
- **Community chat:** https://discord.gg/pallets
- **Contributing guidance:** https://palletsprojects.com/contributing/

## Installation

Install Flask from a package index in your project’s virtual environment:

```console
python -m pip install Flask
```

To work with the source checkout, create and activate a virtual environment, then install the project in editable mode:

```console
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

On Windows, activate the environment with the appropriate script under `.venv\Scripts\`.

Flask’s required dependencies are Blinker, Click, ItsDangerous, Jinja, MarkupSafe, and Werkzeug. Optional extras are available:

```console
python -m pip install "Flask[async]"
python -m pip install "Flask[dotenv]"
```

The `async` extra enables coroutine-based views and related handlers. The `dotenv` extra installs `python-dotenv`, which Flask can use to load `.env` and `.flaskenv` files.

## Quick start

Create an application module, for example `hello.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"
```

Start Flask’s development server from the same environment:

```console
flask --app hello run
```

Open the address printed by the command, typically `http://127.0.0.1:5000/`. For automatic reload and the interactive debugger during development, enable debug mode:

```console
flask --app hello run --debug
```

The CLI can discover an application in a module or file. It looks for an application named `app` or `application`, or a factory named `create_app` or `make_app`. To select a different object or call a factory, use an import path such as `flask --app 'hello:create_app("dev")' run`. Run `flask --help` for command and option details.

The built-in server and interactive debugger are for development only. **Do not use them in production.** See the [deployment documentation](https://flask.palletsprojects.com/en/stable/deploying/) for production deployment guidance and server options.

## Application structure and features

A Flask application is an explicit `Flask` instance. The name passed to its constructor helps Flask locate application resources, including templates and static files. Applications can be created directly or through a factory function. For larger projects, use [blueprints](https://flask.palletsprojects.com/en/stable/blueprints/) to group routes and other application components, then register them with the application.

Routes connect URLs to view functions. Flask exposes the active request through `request`, the current application through `current_app`, and context-scoped storage through `g`. Templates can be rendered with Jinja, and Flask provides support for sessions, JSON responses, redirects, file responses, and custom error handlers.

The `flask` command includes `run`, `shell`, and `routes`, and can also expose commands registered by an application, blueprint, or installed plugin. Use `flask shell` to open an interactive shell with an application context, or `flask routes` to list registered routes.

## Configuration

Application settings are available through `app.config`, a dictionary-like object. Set configuration early in application setup so extensions can use it when initialized:

```python
app.config.update(
    TESTING=True,
    SECRET_KEY="replace-with-a-long-random-value",
)
```

Do not commit real secrets or expose them in logs or support requests. Flask uses `SECRET_KEY` to sign its default session cookies. The default is unset, so applications that use sessions should configure a suitably random secret.

Configuration can also be loaded from Python objects or files, and `Config.from_file` supports data files when supplied with a loader. For environment-based configuration, `app.config.from_prefixed_env()` reads variables with the `FLASK_` prefix by default and parses values as JSON. See the [configuration documentation](https://flask.palletsprojects.com/en/stable/config/) for available settings and loading patterns.

The CLI can load `.flaskenv` and `.env` files when `python-dotenv` is installed. By convention, `.flaskenv` is suitable for public development settings, while `.env` should hold private values and should not be committed. An explicit `--env-file` can also be provided. Values already set in the process environment take precedence over dotenv values.

## Development

The project uses `uv`, `tox`, Ruff, pre-commit, pytest, mypy, and Pyright. The default `uv` development groups include development tools, pre-commit tools, tests, and typing tools. To install the locked development environment:

```console
uv sync
```

The documentation dependencies are in the `docs` group. Install them with:

```console
uv sync --group docs
```

Source code is under `src/flask/`; the main test suite is under `tests/`; documentation sources are under `docs/`; and runnable examples are under `examples/`. The repository includes a Flask tutorial application, a JavaScript request example, and a Celery background-task example.

Before submitting a change, add or update tests and relevant documentation. The pull request template also asks contributors to add a `CHANGES.rst` entry summarizing the change and linking to the related issue, and to update relevant version notes in code documentation. See the [contributing documentation](https://flask.palletsprojects.com/en/stable/contributing/) and the repository’s pull request template for additional guidance.

## Testing and checks

Run the main test suite with pytest:

```console
pytest
```

Pytest is configured to discover tests in `tests/` and to treat warnings as errors. The tox configuration provides test environments for supported Python versions, minimum dependency versions, and development dependency versions. For example:

```console
tox -e py3.10
tox -e tests-min
```

Run the project’s style hooks across all files with:

```console
tox -e style
```

Run both configured static type checkers with:

```console
tox -e typing
```

Build the documentation with the tox documentation environment:

```console
tox -e docs
```

Alternatively, after installing documentation dependencies, build it directly:

```console
sphinx-build -E -W -b dirhtml docs docs/_build/dirhtml
```

## License

Flask is distributed under the **BSD 3-Clause License**. See [`LICENSE.txt`](LICENSE.txt) for the license text.

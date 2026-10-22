# flask-kpi6q5gk

A snapshot of the [Flask](https://flask.palletsprojects.com/) web framework source tree, including its test suite, documentation, and example applications.

> **Note:** The project name `flask-kpi6q5gk` suggests this is a copy or fork of the upstream Flask repository. Check `pyproject.toml` and the git history for the exact version and origin.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Examples](#examples)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Type Checking](#type-checking)
- [Building the Documentation](#building-the-documentation)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Overview

Flask is a lightweight WSGI web application framework for Python. It is designed to make getting started quick and simple, with the ability to scale up to complex applications. It is built on:

- **[Werkzeug](https://werkzeug.palletsprojects.com/)** for WSGI routing, request and response objects, and the development server.
- **[Jinja](https://jinja.palletsprojects.com/)** for HTML templating.
- **[Click](https://click.palletsprojects.com/)** for the command-line interface.
- **[ItsDangerous](https://itsdangerous.palletsprojects.com/)** for cryptographically signed session cookies.
- **[Blinker](https://blinker.readthedocs.io/)** for signals.

Flask does not impose a database, form library, or authentication system. Those are provided by extensions or by your own code.

---

## Features

- **Routing** with decorators (`@app.route`) and URL variables with converters.
- **Blueprints** for organizing an application into reusable components.
- **Jinja2 templating** with auto-escaping, template inheritance, and macros.
- **Request and response handling** via Werkzeug, including JSON support.
- **Sessions** stored in signed cookies, with a pluggable session interface.
- **Configuration** from Python objects, files (`.py`, `.toml`, `.json`), and environment variables.
- **Request, application, and template contexts** through `flask.g`, `current_app`, `request`, and `session`.
- **Application factories** for creating configured app instances.
- **Async views** (`async def`) with the `[async]` extra installed.
- **Signals** for hooking into framework events (such as template rendering or request lifecycle events).
- **Command-line interface** via `flask run`, `flask shell`, and custom commands registered with `@app.cli.command()`.
- **Logging** integration with the standard `logging` module.
- **Testing utilities** including a test client (`app.test_client()`) and a CLI test runner.
- **Error handling** with custom error handlers and debugging helpers.
- **Type annotations** shipped with the package (`py.typed`).

---

## Repository Structure

```
.
├── src/flask/            # Framework source code
│   ├── __init__.py       # Public API exports
│   ├── app.py            # Flask application class
│   ├── blueprints.py     # Blueprint support
│   ├── cli.py            # Command-line interface (flask command)
│   ├── config.py         # Configuration handling
│   ├── ctx.py            # Application and request contexts
│   ├── debughelpers.py   # Helpers for debugging errors
│   ├── globals.py        # Context-local proxies (request, session, g, ...)
│   ├── helpers.py        # Utility functions (url_for, flash, send_file, ...)
│   ├── logging.py        # Logging setup
│   ├── json/             # JSON provider and tagged JSON support
│   ├── sansio/           # I/O-independent base classes
│   ├── sessions.py       # Session interface and implementation
│   ├── signals.py        # Signal definitions
│   ├── templating.py     # Jinja2 integration
│   ├── testing.py        # Test client and CLI runner
│   ├── typing.py         # Type aliases
│   ├── views.py          # Class-based views
│   └── wrappers.py       # Request and Response classes
├── tests/                # Test suite (pytest)
│   ├── test_*.py         # Tests for each module
│   ├── typing_*.py       # Static type-checking test cases
│   ├── static/           # Static files used by tests
│   └── templates/        # Templates used by tests
├── docs/                 # Sphinx documentation (reStructuredText)
│   ├── conf.py           # Sphinx configuration
│   ├── quickstart.rst
│   ├── tutorial/         # Step-by-step tutorial
│   ├── config.rst
│   ├── blueprints.rst
│   ├── deploying/       # Deployment guides (gunicorn, nginx, uWSGI, ...)
│   └── ...
├── examples/
│   ├── tutorial/         # "flaskr" blog application (the official tutorial)
│   ├── javascript/       # Calling Flask endpoints from JavaScript
│   └── celery/           # Integrating Flask with Celery tasks
├── pyproject.toml        # Project metadata and tool configuration
├── uv.lock               # Locked dependency versions (uv)
├── CHANGES.rst           # Changelog
├── LICENSE.txt           # BSD-3-Clause license
└── README.md             # This file
```

---

## Requirements

- Python 3.9 or newer (check `pyproject.toml` for the exact supported range).
- Runtime dependencies are installed automatically: Werkzeug, Jinja2, itsdangerous, click, blinker, and markupsafe.

---

## Installation

### From PyPI

```bash
pip install Flask
```

Optional extras, if defined in `pyproject.toml`, can be installed with:

```bash
pip install "Flask[async                                                                                                                                       ]"
```

### From this repository

Create and activate a virtual environment, then install in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

---

## Quick Start

Create a file named `hello.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
```

Run the development server:

```bash
flask --app hello run --debug
```

Open `http://127.0.0.1:5000/` in your browser.

The `--debug` flag enables the interactive debugger and automatic reloading. Do not use it in production.

### Routing with variables

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/users/<int:user_id>")
def show_user(user_id: int):
    return jsonify(id=user_id, name=f"User {user_id}")

@app.post("/items")
def create_item():
    return {"status": "created"}, 201
```

### Rendering templates

Place templates in a `templates/` directory next to your application module:

```
hello.py
templates/
└── index.html
```

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/greet/<name>")
def greet(name):
    return render_template("index.html", name=name)
```

```html
<!-- templates/index.html -->
<h1>Hello, {{ name }}!</h1>
```

Jinja2 escapes variables automatically, which protects against cross-site scripting (XSS).

---

## Core Concepts

### Application object

`Flask(__name__)` creates the WSGI application. It holds configuration, routes, error handlers, and extensions. The `__name__` argument tells Flask where to find resources such as templates and static files.

### Request and context locals

Flask exposes request-scoped objects as context-aware proxies:

| Name              | Purpose                                              |
|-------------------|------------------------------------------------------|
| `request`         | The current incoming request                         |
| `session`         | A dictionary-like object for per-user data           |
| `g`               | A namespace for storing data during one request      |
| `current_app`    | The application handling the current request        |

```python
from flask import request, session, g

@app.before_request
def load_user():
    g.user = session.get("user_id")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    return f"You searched for {query}"
```

### Configuration

```python
app.config.from_mapping(
    SECRET_KEY="change-me",
    SESSION_COOKIE_SECURE=True,
)
app.config.from_prefixed_env()       # reads FLASK_* environment variables
app.config.from_file("config.toml", load=tomllib.load, text=False)
```

Configuration can also be loaded from a Python object with `app.config.from_object()`. Set `SECRET_KEY` to a strong, random value before using sessions.

### Blueprints

Blueprints group related routes so they can be reused or mounted at a URL prefix:

```python
from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    ...

# In the application factory:
app.register_blueprint(bp)
```

### Application factories

A factory function creates and configures an app instance, which is useful for testing and for running multiple configurations:

```python
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev")
    if test_config:
        app.config.from_mapping(test_config)

    from . import auth
    app.register_blueprint(auth.bp)
    return app
```

Run it with `flask --app "myapp:create_app" run`.

### Command-line interface

Custom commands are registered with the app's CLI group:

```python
import click

@app.cli.command("init-db")
def init_db_command():
    """Create the database tables."""
    click.echo("Initialized the database.")
```

```bash
flask --app myapp init-db
```

### Async views

With async support installed (`pip install "Flask[async]"`), views can be coroutines:

```python
@app.route("/slow")
async def slow():
    await asyncio.sleep(1)
    return "done"
```

### Signals

Signals let you react to framework events without modifying core code:

```python
from flask import template_rendered

def log_template(sender, template, context, **extra):
    sender.logger.debug("Rendered %s", template.name)

template_rendered.connect(log_template, app)
```

---

## Examples

The `examples/` directory contains complete applications. Each includes its own `pyproject.toml` and, in most cases, a README with detailed instructions.

### Tutorial: `examples/tutorial/` (flaskr)

A blog application with user registration, login, and post creation, editing, and deletion. It uses SQLite via Python's `sqlite3` module and includes an application factory, blueprints, templates, static files, and tests.

```bash
cd examples/tutorial
pip install -e .
flask --app flaskr init-db
flask --app flaskr run --debug
```

Run its tests:

```bash
pip install -e ".[test]"
pytest
```

The tutorial's source is also the basis of the Flask documentation's "Tutorial" section.

### JavaScript: `examples/javascript/`

Demonstrates calling Flask endpoints from the browser using `fetch`, `XMLHttpRequest`, and jQuery. Includes a JavaScript-enabled test using Playwright or a similar browser driver (see the example's `conftest.py`).

```bash
cd examples/javascript
pip install -e .
flask --app js_example run --debug
```

### Celery: `examples/celery/`

Shows how to configure Celery with a Flask application context so that background tasks can access the app's configuration and extensions. The `make_celery.py` module creates the Celery instance, and `tasks.py` defines the tasks.

```bash
cd examples/celery
pip install -r requirements.txt
```

Start a Celery worker and the Flask development server in separate terminals, following the instructions in the example's README.

---

## Development Setup

This repository uses [uv](https://docs.astral.sh/uv/) for dependency management, as indicated by `uv.lock`.

```bash
# Install uv (see https://docs.astral.sh/uv/getting-started/installation/)
uv sync --all-extras
```

Activate the environment or prefix commands with `uv run`:

```bash
uv run pytest
uv run flask --help
```

If the project includes pre-commit hooks, install them with:

```bash
uv run pre-commit install
```

---

## Running Tests

The test suite uses [pytest](https://docs.pytest.org/). Shared fixtures live in `tests/conftest.py`.

```bash
# Run the full suite
pytest

# Run one file
pytest tests/test_basic.py

# Run one test
pytest tests/test_blueprints.py::test_name

# Run with coverage (if pytest-cov is installed)
pytest --cov=flask
```

Test modules are organized by feature, for example:

| File                        | Covers                                 |
|-----------------------------|----------------------------------------|
| `test_basic.py`             | Core routing and request handling      |
| `test_blueprints.py`        | Blueprint registration and behavior    |
| `test_cli.py`               | The `flask` command-line tool          |
| `test_config.py`            | Configuration loading                  |
| `test_templating.py`        | Jinja2 integration                     |
| `test_json.py`              | JSON provider and responses            |
| `test_session_interface.py` | Session handling                       |
| `test_signals.py`           | Signal dispatch                        |
| `test_testing.py`           | The test client and CLI runner         |
| `test_async.py`             | Async views                            |

---

## Type Checking

The package includes type annotations and a `py.typed` marker. The `tests/typing_*.py` files are checked with a static type checker (such as mypy or pyright) to ensure the public API types correctly:

```bash
mypy tests/typing_app_decorators.py tests/typing_route.py
```

Consult `pyproject.toml` for the configured type checker and its settings.

---

## Building the Documentation

The documentation uses [Sphinx](https://www.sphinx-doc.org/) with reStructuredText sources in `docs/`.

```bash
cd docs
make html          # Linux/macOS
make.bat html      # Windows
```

The output is written to `docs/_build/html/`. Open `index.html` in a browser to view it.

The documentation covers:

- **Getting started:** installation, quickstart, and the tutorial.
- **Concepts:** application setup, routing, templates, blueprints, configuration, request and response objects, sessions, signals, and the CLI.
- **Guides:** async, testing, logging, error handling, and debugging.
- **Deployment:** Gunicorn, uWSGI, mod_wsgi, Gevent, Eventlet, Waitress, Nginx, Apache HTTPD, and ASGI servers.
- **Extending:** extension development and subclassing.
- **Reference:** API documentation generated from docstrings.

---

## Contributing

Contributions are welcome. A typical workflow:

1. Fork the repository and create a feature branch.
2. Set up the development environment (see [Development Setup](#development-setup)).
3. Make your changes and add or update tests in `tests/`.
4. Update `docs/` and `CHANGES.rst` if the change affects users.
5. Run the test suite and any linters or type checkers.
6. Open a pull request describing the change and its motivation.

Please keep changes focused, follow the existing code style, and include tests for bug fixes and new features.

For security issues, follow the process described in the project's security policy rather than opening a public issue.

---

## Changelog

Release history and notable changes are recorded in [`CHANGES.rst`](CHANGES.rst).

---

## License

Flask is released under the BSD 3-Clause License. See [`LICENSE.txt`](LICENSE.txt) for the full text.

---

## Acknowledgments

Flask is developed by the [Pallets](https://palletsprojects.com/) project and its contributors. Its dependencies, Werkzeug, Jinja, Click, ItsDangerous, and Blinker, are also Pallets projects.

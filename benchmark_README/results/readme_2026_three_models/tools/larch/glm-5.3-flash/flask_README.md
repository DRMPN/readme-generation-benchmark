# README

```markdown
# Flask

[![Tests](https://github.com/pallets/flask/workflows/Tests/badge.svg)](https://github.com/pallets/flask/actions?query=workflow%3ATests)
[![Python Version](https://img.shields.io/pypi/pyversions/flask)](https://pypi.org/project/flask/)
[![PyPI](https://img.shields.io/pypi/v/flask)](https://pypi.org/project/flask/)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-green)](https://github.com/pallets/flask/blob/main/LICENSE.txt)

Flask is a lightweight [WSGI](https://wsgi.readthedocs.io/) web application framework. It is
designed to make getting started quick and easy, with the ability to scale up to complex
applications. It began as a simple wrapper around [Werkzeug](https://werkzeug.palletsprojects.com/)
and [Jinja](https://jinja.palletsprojects.com/), and has become one of the most popular Python
web application frameworks.

Flask offers suggestions, but doesn't enforce any dependencies or project layout. It is up to
the developer to choose the tools and libraries they want to use. There are many extensions
provided by the community that make adding new functionality easy.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Project Structure](#project-structure)
- [Running the Test Suite](#running-the-test-suite)
- [Building the Documentation](#building-the-documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [Links](#links)
- [License](#license)

---

## Features

- **Simple, lightweight core** — a minimal API with sensible defaults that stays out of your way.
- **Built-in development server and debugger** — with hot reloading and interactive tracebacks.
- **Integrated unit testing support** — test clients and helpers for simulating requests.
- **RESTful request dispatching** — clean, expressive URL routing with converters.
- **Jinja2 templating** — powerful HTML templating with template inheritance, macros, and filters.
- **Secure cookies (sessions)** — cryptographically signed session support out of the box.
- **100% WSGI 1.0 compliant** — works with any WSGI server or middleware.
- **Unicode-based** — full Unicode support throughout the framework.
- **Extensive documentation** — tutorials, API reference, and design notes.
- **Type annotated** — ships a `py.typed` marker for full static typing support.
- **Async support** — `async`/`await` view functions are supported.
- **CLI support** — a built-in command-line interface with custom command support via Click.
- **Signals** — integration with Blinker for decoupled event handling.
- **Blueprints** — organize large applications into reusable components.
- **Application and Request Contexts** — thread-safe access to globals like `request` and `g`.

---

## Installation

Python 3.8 or later is required. Install Flask from [PyPI](https://pypi.org/project/flask/)
using `pip`:

```sh
pip install Flask
```

Or, to work on Flask itself from this repository (using [uv](https://docs.astral.sh/uv/)):

```sh
# create a virtualenv and install dependencies
uv sync

# activate the virtualenv
. .venv/bin/activate    # Linux / macOS
.venv\Scripts\activate  # Windows
```

Dependencies include:

| Package      | Role                                      |
|--------------|-------------------------------------------|
| Werkzeug     | WSGI toolkit: request/response objects    |
| Jinja        | Template engine                           |
| Click        | Command-line interface                    |
| itsdangerous | Securely signing data (sessions, cookies) |
| Blinker      | Signals support                           |

---

## Quick Start

### Hello, World!

Create a file called `hello.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"
```

Run the development server:

```sh
flask run
```

Or make the file executable:

```sh
python hello.py
```

Visit `http://127.0.0.1:5000/` in your browser — that's it!

### A More Complete Example

```python
from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"


@app.route("/")
def index():
    return render_template("index.html", name=session.get("user"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        flash("Logged in successfully.")
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/user/<int:user_id>")
def profile(user_id):
    # URL converters: int, string, path, uuid, float
    return f"Profile for user {user_id}"


if __name__ == "__main__":
    app.run(debug=True)
```

---

## Core Concepts

### Routing

Map URLs to view functions with the `route` decorator. Variables are captured from the URL
and passed as keyword arguments:

```python
@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post {post_id}"
```

### Templates

Flask uses [Jinja](https://jinja.palletsprojects.com/) for rendering templates from a
`templates/` directory. Templates support inheritance, macros, filters, and automatic
escaping:

```python
from flask import render_template

@app.route("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name)
```

### Configuration

Applications carry configuration via `app.config`, which supports loading from Python
objects, files, environment variables, and dictionaries:

```python
app = Flask(__name__)
app.config.from_object("yourapplication.default_config")
app.config.from_envvar("YOURAPPLICATION_SETTINGS")
app.config.from_file("config.json", load=json.load)
```

### Sessions

Sessions are stored in cryptographically signed cookies, backed by `itsdangerous`:

```python
from flask import session

@app.route("/counter")
def counter():
    session["count"] = session.get("count", 0) + 1
    return str(session["count"])
```

### Blueprints

Split large applications into reusable, nestable components:

```python
from flask import Blueprint

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/")
def index():
    return "Admin dashboard"

app.register_blueprint(bp)
```

### Class-Based Views

Reusable views via `flask.views.View` and `flask.views.MethodView`:

```python
from flask.views import MethodView

class UserAPI(MethodView):
    def get(self, user_id):
        return f"User {user_id}"

    def delete(self, user_id):
        return f"Deleted {user_id}"

app.add_url_rule(
    "/users/<int:user_id>", view_func=UserAPI.as_view("user_api")
)
```

### Application & Request Contexts

Flask uses context locals so that views can access `request`, `session`, `g`, and
`current_app` without being passed as arguments — safely across threads and async tasks.

### Error Handling & Signals

Register handlers for exceptions and HTTP codes, and hook into framework lifecycle events
via signals (`request_started`, `request_finished`, `app_error`, etc.):

```python
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
```

### JSON Support

Flask provides first-class JSON support with provider-level customization:

```python
from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    sort_keys = False

app.json = CustomJSONProvider(app)
```

### Command-Line Interface

The `flask` command runs the development server, opens a shell, and exposes commands
defined in your app:

```python
import click
from flask import Flask

app = Flask(__name__)

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    click.echo("Initialized the database.")
```

```sh
flask init-db
```

### Testing

The built-in test client simulates full requests without a running server:

```python
import pytest
from myapp import create_app

@pytest.fixture()
def app():
    return create_app(testing=True)

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data
```

---

## Project Structure

This repository contains the framework source, tests, documentation, and examples:

```
.
├── src/flask/              # Framework source code
│   ├── __init__.py         # Public API exports
│   ├── app.py              # Flask application class
│   ├── blueprint*.py       # Blueprint support
│   ├── scaffold.py         # Shared application/behavior base
│   ├── ctx.py              # Request & application contexts
│   ├── wrappers.py         # Request and Response subclasses
│   ├── config.py           # Configuration handling
│   ├── routing helpers / globals.py   # Context globals (request, g, ...)
│   ├── helpers.py          # Utility functions (url_for, flash, ...)
│   ├── templating.py       # Jinja integration
│   ├── sessions.py         # Session interfaces & cookie sessions
│   ├── json/               # JSON provider and tag serialization
│   ├── signals.py          # Blinker signal definitions
│   ├── cli.py              # Command-line interface
│   ├── logging.py          # Logging integration
│   ├── testing.py          # Test client and CLI runner
│   ├── views.py            # Class-based views
│   ├── typing.py           # Type aliases for decorators
│   ├── debughelpers.py     # Helpful errors for common mistakes
│   └── py.typed            # PEP 561 type marker
├── tests/                  # Comprehensive pytest test suite
│   ├── test_basic.py       # Core behavior
│   ├── test_appctx.py      # Application context
│   ├── test_reqctx.py      # Request context
│   ├── test_blueprints.py  # Blueprints
│   ├── test_async.py       # Async view support
│   ├── test_cli.py         # CLI
│   ├── test_config.py      # Configuration
│   ├── test_json.py        # JSON encoding
│   ├── test_templating.py  # Jinja integration
│   ├── test_testing.py     # Test client
│   └── ...                 # plus test_apps/ fixtures
├── docs/                   # Sphinx documentation
│   ├── quickstart.rst      # Getting started guide
│   ├── tutorial/           # Flaskr tutorial
│   ├── api.rst             # API reference
│   └── ...
├── examples/
│   ├── flaskr/             # Official blog tutorial application
│   ├── javascript/         # JavaScript integration patterns
│   └── celery/             # Background tasks with Celery
├── artwork/                # Logos and artwork
├── pyproject.toml          # Build & tool configuration
├── CHANGES.rst             # Release changelog
├── LICENSE.txt             # BSD-3-Clause license
└── README.rst              # This file (reStructuredText original)
```

---

## Running the Test Suite

Install the development dependencies, then run `pytest`:

```sh
uv sync --dev
pytest
```

Individual test modules can be run for faster iteration:

```sh
pytest tests/test_basic.py
pytest tests/test_blueprints.py -v
```

The suite covers application context, request context, routing, sessions, templating,
signals, async behavior, the CLI, typing annotations, error handling, and known
regressions.

---

## Building the Documentation

The documentation is built with [Sphinx](https://www.sphinx-doc.org/):

```sh
cd docs
make html        # Linux / macOS
.\make.bat html  # Windows
```

The output is written to `docs/_build/html/`.

---

## Examples

### Flaskr — The Tutorial Blog App

The [flaskr](examples/flaskr) example is the complete application from the official
tutorial: a small blogging application with registration, authentication, and SQLite
persistence.

```sh
cd examples/flaskr
pip install -e .
flask init-db
flask run
```

Key files:

- `flaskr/__init__.py` — application factory
- `flaskr/db.py` — SQLite connection management
- `flaskr/auth.py` — registration and login blueprints
- `flaskr/blog.py` — blog posts blueprint
- `tests/` — end-to-end tests with `pytest` fixtures

### JavaScript Integration

Patterns for using Flask with client-side JavaScript, including jQuery, XHR,
and the modern `fetch` API:

```javascript
fetch("/api/data")
  .then((response) => response.json())
  .then((data) => console.log(data));
```

### Celery

Using Celery task queues with Flask application factories:

```python
from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config["RESULT_BACKEND"], broker=app.config["BROKER_URL"])
    celery.conf.update(app.config)
    return celery
```

---

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting
pull requests:

1. Fork the repository and create a feature branch.
2. Run the test suite and ensure all tests pass: `pytest`.
3. Ensure code passes formatting and lint checks (`ruff`).
4. Update `CHANGES.rst` with a description of your change.
5. Add or update tests for any behavior changes.
6. Open a pull request with a clear description.

---

## Links

- **Documentation:** https://flask.palletsprojects.com/
- **Source Code:** https://github.com/pallets/flask
- **Issue Tracker:** https://github.com/pallets/flask/issues
- **PyPI:** https://pypi.org/project/flask/
- **Chat:** [Discord](https://discord.gg/pallets)
- **Werkzeug:** https://werkzeug.palletsprojects.com/
- **Jinja:** https://jinja.palletsprojects.com/

---

## License

Flask is distributed under the terms of the **BSD-3-Clause** license. See
[LICENSE.txt](LICENSE.txt) for the full text.

Copyright © Pallets
```

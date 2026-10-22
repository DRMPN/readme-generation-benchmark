# Flask

A simple framework for building complex web applications.

Flask is a lightweight WSGI web application framework written in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.

Flask offers suggestions, but doesn't enforce any dependencies or project layout. It is up to the developer to choose the tools and libraries they want to use. There are many community-provided extensions that provide common functionality such as authentication, database integration, and form handling.

## Features

- **Simple, explicit API** — create an application object, register routes, and serve requests.
- **Routing** — powered by Werkzeug's routing system, with converters for `string`, `int`, `float`, `path`, `any`, and `uuid` variable parts, plus support for custom converters, subdomain matching, and host matching.
- **Templating** — built-in Jinja2 integration with automatic autoescaping for `.html`, `.htm`, `.xml`, `.xhtml`, and `.svg` files, template inheritance, and streaming templates.
- **Blueprints** — organize larger applications into reusable components, with support for nested blueprints, blueprint-specific static files, templates, CLI commands, and error handlers.
- **CLI** — the `flask` command (built with Click) provides a development server, interactive shell, route listing, and support for custom commands, command groups, and plugins via entry points.
- **Configuration** — load configuration from Python files, TOML/JSON data files, environment variables (including `Config.from_prefixed_env()` with JSON parsing and nested keys), and instance folders.
- **Sessions** — secure, signed cookie-based sessions with extensive cookie options (`Secure`, `HttpOnly`, `SameSite`, `Partitioned`) and key rotation support via `SECRET_KEY_FALLBACKS`.
- **Async support** — views, error handlers, and hooks can be defined with `async def` when installed with the `async` extra.
- **JSON support** — customizable via a `JSONProvider` class, so you can swap in a different JSON library.
- **Signals** — lifecycle signals (via Blinker) such as `request_started`, `request_finished`, `got_request_exception`, `template_rendered`, and `message_flashed`.
- **Testing** — built-in test client (`app.test_client()`) and CLI test runner (`app.test_cli_runner()`).
- **Type hints** — the codebase is fully typed (`py.typed` included).

## Installation

Flask requires Python >= 3.10.

```console
$ pip install flask
```

Optional extras:

```console
$ pip install "flask[async]"     # async view support (asgiref)
$ pip install "flask[dotenv]"    # .env and .flaskenv support (python-dotenv)
```

## Quick Start

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
```

Or run it with the `flask` command:

```console
$ flask --app hello run --debug
 * Serving Flask app "hello"
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

The `--app` option accepts a module name, file path, or factory, e.g. `--app hello`, `--app hello:app2`, or `--app 'hello:create_app("dev")'`. If omitted, the CLI looks for `wsgi.py` or `app.py` in the current directory and auto-detects an `app`/`application` instance or a `create_app`/`make_app` factory.

> **Warning:** Do not use the development server (`flask run` or `app.run()`) in production. It is not designed for the stability, security, or performance requirements of a production deployment. See the deployment documentation for WSGI server recommendations (Gunicorn, uWSGI, Waitress, Apache, nginx, etc.).

## CLI

Installing Flask installs the `flask` script, which provides:

- `flask run` — start the development server, with `--debug` to enable the debugger and reloader, `--cert`/`--key` for HTTPS, `--extra-files` and `--exclude-patterns` for reloader control.
- `flask shell` — an interactive Python shell with an active application context.
- `flask routes` — list all registered routes, sortable by endpoint, methods, domain, rule, or match order.
- `flask --version` — show Python, Flask, and Werkzeug versions.

Custom commands can be registered with `@app.cli.command()`, organized into groups with `AppGroup`, attached to blueprints, loaded from `flask.commands` entry points in installed packages, or exposed through a custom script using `FlaskGroup`:

```python
import click
from flask import Flask
from flask.cli import FlaskGroup

def create_app():
    app = Flask("wiki")
    return app

@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Wiki application."""
```

Environment variables from `.env` and `.flaskenv` files are loaded automatically if `python-dotenv` is installed. Options can also be set via environment variables named `FLASK_COMMAND_OPTION`, e.g. `FLASK_RUN_PORT`.

## Configuration

Configuration is stored on `app.config`, a dictionary subclass. Key built-in values include:

| Key | Description | Default |
| --- | --- | --- |
| `DEBUG` | Enable debug mode (debugger, reloader) | `False` |
| `TESTING` | Propagate exceptions for testing | `False` |
| `SECRET_KEY` | Key for signing session cookies | `None` |
| `SECRET_KEY_FALLBACKS` | Old keys for key rotation (added in 3.1) | `None` |
| `SESSION_COOKIE_*` | Cookie name, domain, path, security options | varies |
| `PERMANENT_SESSION_LIFETIME` | Permanent session lifetime | 31 days |
| `MAX_CONTENT_LENGTH` | Max bytes read per request | `None` |
| `MAX_FORM_MEMORY_SIZE` | Max size per non-file form field | `500_000` |
| `MAX_FORM_PARTS` | Max fields in multipart body | `1_000` |
| `TRUSTED_HOSTS` | Host validation during routing (added in 3.1) | `None` |
| `SERVER_NAME` | Host/port for external URL generation | `None` |
| `TEMPLATES_AUTO_RELOAD` | Reload changed templates | `None` (debug) |

Config can be loaded from Python objects/files (`from_object`, `from_pyfile`), data files (`from_file` with TOML, JSON, etc.), or environment variables (`from_prefixed_env` with `FLASK_` prefix, JSON parsing, and `__`-separated nested keys). Instance folders provide a deployment-specific location for configuration and data outside version control.

## Async Support

With the `async` extra installed, routes, error handlers, before/after request functions, teardown functions, and class-based view handlers can be coroutine functions. Flask runs async views on an event loop in a thread; each request still ties up one worker, so async is most beneficial for concurrent IO-bound work within a view. For heavily async codebases, consider [Quart](https://github.com/pallets/quart), an ASGI-based Flask reimplementation.

## Examples

The repository includes runnable examples:

- **tutorial** (`examples/tutorial/`) — the "Flaskr" blog application built in the documentation's tutorial, with authentication, database (SQLite), and a full test suite.
- **javascript** (`examples/javascript/`) — demonstrates making AJAX requests to Flask using Fetch, jQuery, and XMLHttpRequest.
- **celery** (`examples/celery/`) — a Flask application with Celery background tasks (Redis broker).

Each example is a standalone package with its own `pyproject.toml` and tests.

## Development

### Setting Up

```console
$ git clone https://github.com/pallets/flask/
$ cd flask
$ uv sync --all-groups
```

The project uses [uv](https://docs.astral.sh/uv/) for dependency management (`uv.lock` is included) and defines dependency groups: `dev`, `pre-commit`, `tests`, `typing`, and `docs`. A dev container configuration is also available in `.devcontainer/`.

### Running Tests

Tests use pytest:

```console
$ pytest -v --tb=short
```

Or run the full matrix with tox:

```console
$ tox
```

The tox environment list includes `py3.10`–`py3.13`, `pypy3.11`, `tests-min` (minimum pinned dependency versions), `tests-dev` (git main branches of Pallets dependencies), `style`, `typing`, and `docs`.

Test configuration in `pyproject.toml` treats warnings as errors (`filterwarnings = ["error"]`), and coverage is configured with branch coverage over `flask` and `tests`.

### Style and Type Checking

- **Ruff** — linting with `flake8-bugbear`, `pycodestyle`, `pyflakes`, `isort` (force-single-line), and `pyupgrade` rules.
- **pre-commit** — hooks run via `tox -e style` or `pre-commit run --all-files`.
- **mypy** (strict mode) and **pyright** (basic mode) — run via `tox -e typing`.

### Building Documentation

Documentation is built with Sphinx:

```console
$ tox -e docs            # build once
$ tox -e docs-auto       # continuous rebuild with local server
```

Or directly:

```console
$ sphinx-build -E -W -b dirhtml docs docs/_build/dirhtml
```

Docs cover the quickstart, tutorial, API reference, configuration, CLI, blueprints, testing, deployment guides, design patterns, and more. They are hosted at <https://flask.palletsprojects.com/> and published with Read the Docs (`.readthedocs.yaml` included).

### Continuous Integration

GitHub Actions workflows run pre-commit checks, tests, and the publish process; a lock workflow manages stale issues/PRs.

### Contributing

See the Pallets [contributing documentation](https://palletsprojects.com/contributing/) for how to report issues, request features, and submit PRs. Pull requests should link to an issue, include tests demonstrating correct behavior, update relevant docs, and add an entry in `CHANGES.rst`. Issue templates for bug reports and feature requests are provided.

## Release Notes

Notable recent changes (from `CHANGES.rst`):

- **3.2.0 (unreleased)** — drops Python 3.9 support; removes the deprecated `__version__` attribute.
- **3.1.0** — drops Python 3.8; updated minimum dependencies (Werkzeug >= 3.1, ItsDangerous >= 2.2, Blinker >= 1.9); adds `SECRET_KEY_FALLBACKS` key rotation, `SESSION_COOKIE_PARTITIONED` (CHIPS), `TRUSTED_HOSTS`, `MAX_FORM_MEMORY_SIZE`/`MAX_FORM_PARTS` resource limits, `encoding` parameter for `open_resource`, and `PROVIDE_AUTOMATIC_OPTIONS` config.
- **3.0.0** — removed deprecated code; Sans-IO base classes for `Flask` and `Blueprint`; requires Werkzeug >= 3.0.

## License

Flask is licensed under the BSD-3-Clause license, described in `LICENSE.txt`.

## Links

- Documentation: <https://flask.palletsprojects.com/>
- Changes: <https://flask.palletsprojects.com/page/changes/>
- Source: <https://github.com/pallets/flask/>
- Chat: <https://discord.gg/pallets>
- Donate: <https://palletsprojects.com/donate>

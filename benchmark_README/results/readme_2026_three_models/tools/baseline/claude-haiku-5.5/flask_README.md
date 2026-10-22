# Flask

Flask is a lightweight WSGI web application framework for Python, distributed as the `flask` package by Pallets. The project's package metadata describes it as "A simple framework for building complex web applications." It is licensed under BSD-3-Clause.

This repository contains the Flask source code (`src/flask`), the test suite (`tests`), the Sphinx documentation (`docs`), three example applications (`examples`), and the project's build, tooling, and CI configuration.

## Overview

Flask is built around a central `Flask` application object. The application object acts as a registry for view functions, URL rules, template configuration, and other settings. Within the source tree, the main modules include:

- `app.py` and `sansio/app.py`: the `Flask` application class and its sans-I/O base.
- `blueprints.py` and `sansio/blueprints.py`: blueprints for organizing an application into modular components.
- `cli.py`: the `flask` command-line interface, built on Click.
- `config.py`: the configuration object.
- `ctx.py` and `globals.py`: application and request contexts and their proxies (such as `current_app`, `request`, `session`, and `g`).
- `json/`: the pluggable JSON provider system.
- `templating.py`: Jinja2 integration.
- `testing.py`: the test client and CLI runner.
- `sessions.py`: the session interface and secure cookie session implementation.
- `signals.py`: signal support, which relies on Blinker.

The package includes a `py.typed` marker, and the project is configured for static type checking.

## Requirements

- Python 3.10 or later (`requires-python = ">=3.10"`). `CHANGES.rst` notes that Python 3.9 support is dropped in the unreleased 3.2.0 version.
- Required dependencies:
  - `blinker>=1.9.0`
  - `click>=8.1.3`
  - `itsdangerous>=2.2.0`
  - `jinja2>=3.1.2`
  - `markupsafe>=2.1.1`
  - `werkzeug>=3.1.0`

Optional extras:

- `async`: installs `asgiref>=3.2`, required for `async def` views.
- `dotenv`: installs `python-dotenv`, which enables loading `.env` and `.flaskenv` files.

## Installation

Install Flask from PyPI with pip:

```bash
pip install flask
```

To include async view support:

```bash
pip install "flask[async]"
```

To include dotenv support:

```bash
pip install "flask[dotenv]"
```

The project uses `flit_core` as its build backend. The source distribution includes `docs/`, `examples/`, `tests/`, `CHANGES.rst`, and `uv.lock`.

## Quick Start

Create a minimal application in a file named `hello.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"
```

Run the development server:

```bash
flask --app hello run --debug
```

The `flask` command is installed as a console script that points to `flask.cli:main`. The `--app` option tells it where to find the application. Without `--app`, the command looks for `wsgi.py` or `app.py` in the current directory.

## Usage

### Application discovery

The `--app` (`-A`) option accepts a module or file path, optionally followed by a colon and an attribute name or factory call:

- `--app hello`: imports `hello` and looks for an application named `app` or `application`, or a factory named `create_app` or `make_app`.
- `--app hello:app2`: uses the `app2` instance in `hello`.
- `--app 'hello:create_app("dev")'`: calls the `create_app` factory with the literal argument `"dev"`.
- `--app src/hello`: sets the working directory to `src`, then imports `hello`.

The `FLASK_APP` environment variable can supply the same value.

### Built-in commands

| Command | Description |
| --- | --- |
| `flask run` | Starts the development server. |
| `flask shell` | Opens an interactive shell with an application context active. |
| `flask routes` | Lists registered routes, with endpoints and methods. Supports `--sort` and `--all-methods`. |

Global options include `--app`/`-A`, `--debug/--no-debug`, `-e/--env-file`, and `--version`, which prints the Python, Flask, and Werkzeug versions.

### Running the development server

`flask run` accepts these options, among others:

- `--host`/`-h` (default `127.0.0.1`) and `--port`/`-p` (default `5000`)
- `--cert` and `--key` for HTTPS, including ad-hoc certificates when `cryptography` is installed
- `--reload/--no-reload` and `--debugger/--no-debugger`, both enabled by default in debug mode
- `--with-threads/--without-threads`
- `--extra-files` and `--exclude-patterns` for reloader behavior

The development server is intended only for development. The documentation and the `run` command's help text state that it is not designed for production use. The `deploying/` documentation covers production WSGI servers, including Gunicorn, uWSGI, Waitress, mod_wsgi, Apache, and nginx.

### Custom commands

Commands registered on `app.cli` run with an application context active:

```python
import click
from flask import Flask

app = Flask(__name__)

@app.cli.command("create-user")
@click.argument("name")
def create_user(name):
    ...
```

Flask also loads commands from the `flask.commands` entry point group, which allows extensions to add commands when installed.

## Configuration

### Configuration keys

Flask stores configuration in `app.config`, which behaves like a dictionary. The built-in defaults include keys such as:

- `DEBUG`, `TESTING`, `PROPAGATE_EXCEPTIONS`
- `SECRET_KEY` and `SECRET_KEY_FALLBACKS` (for key rotation)
- `SESSION_COOKIE_NAME`, `SESSION_COOKIE_DOMAIN`, `SESSION_COOKIE_PATH`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_PARTITIONED`, `SESSION_COOKIE_SAMESITE`
- `PERMANENT_SESSION_LIFETIME` (default 31 days)
- `SERVER_NAME`, `APPLICATION_ROOT`, `PREFERRED_URL_SCHEME`
- `MAX_CONTENT_LENGTH`, `MAX_FORM_MEMORY_SIZE`, `MAX_FORM_PARTS`
- `TEMPLATES_AUTO_RELOAD`, `EXPLAIN_TEMPLATE_LOADING`
- `TRUSTED_HOSTS`, `MAX_COOKIE_SIZE`, `PROVIDE_AUTOMATIC_OPTIONS`

### Loading configuration

Configuration can be loaded from several sources:

```python
app.config.from_object("yourapplication.default_settings")
app.config.from_envvar("YOURAPPLICATION_SETTINGS")
app.config.from_file("config.toml", load=tomllib.load, text=False)
app.config.from_prefixed_env()  # FLASK_ prefix by default
```

Values loaded with `from_prefixed_env()` are parsed as JSON by default. Double underscores (`__`) set keys in nested dictionaries.

### Instance folders

Flask supports an instance folder, exposed as `app.instance_path`, for deployment-specific files that should not be under version control. Pass `instance_path` as an absolute path, or set `instance_relative_config=True` to resolve config file paths relative to it.

### Environment variables and dotenv

Command options can be set through environment variables named `FLASK_<OPTION>` or `FLASK_<COMMAND>_<OPTION>`, for example `FLASK_RUN_PORT`. When python-dotenv is installed, `flask` loads `.flaskenv` and `.env` files found by scanning upward from the current directory. Variables already set in the environment take precedence over file values. Setting `FLASK_SKIP_DOTENV=1` disables automatic loading.

Debug mode is best controlled with the `--debug` option rather than by setting `DEBUG` in code.

## Examples

The `examples/` directory contains three standalone projects, each with its own `pyproject.toml` and README:

- **`examples/tutorial`** (`flaskr`): the basic blog application from the Flask tutorial, with authentication, blog posts, SQLite schema, templates, and tests.
- **`examples/javascript`** (`js_example`): demonstrates making AJAX requests to Flask using `fetch`, XHR, and jQuery, with tests.
- **`examples/celery`** (`flask-example-celery`): an example application with Celery background tasks, using Redis as a broker in its dependencies.

These example projects are marked `Private :: Do Not Upload`.

## Development

### Setting up a development environment

The project uses `uv` for dependency management. The `[tool.uv]` section sets the default dependency groups to `dev`, `pre-commit`, `tests`, and `typing`. The lock file is `uv.lock`. A `.devcontainer/` configuration is also included.

Development dependency groups include:

- `dev`: `ruff`, `tox`, `tox-uv`
- `tests`: `asgiref`, `greenlet`, `pytest`, `python-dotenv`
- `typing`: `mypy`, `pyright`, and related stubs
- `docs`: `sphinx`, `pallets-sphinx-themes`, `sphinx-tabs`, `sphinxcontrib-log-cabinet`
- `pre-commit`: `pre-commit`, `pre-commit-uv`

### Code style and linting

Ruff is configured in `pyproject.toml` with the `B`, `E`, `F`, `I`, `UP`, and `W` rule sets. Imports are sorted with one import per line. Pre-commit hooks are configured in `.pre-commit-config.yaml`. EditorConfig settings are in `.editorconfig`.

### Type checking

- **mypy** runs in strict mode over `src` and `tests/type_check`.
- **pyright** runs in basic mode over the same paths.

## Testing

Tests live in `tests/` and are run with pytest. The pytest configuration sets `filterwarnings = ["error"]`, so warnings are treated as errors. Coverage is configured with branch coverage for `flask` and `tests`.

The `tox` configuration defines these environments:

| Environment | Purpose |
| --- | --- |
| `py3.10` through `py3.13`, `pypy3.11` | Tests on the locked dependency versions |
| `tests-min` | Tests with the minimum supported dependency versions |
| `tests-dev` | Tests against development branches of Pallets dependencies |
| `style` | Runs all pre-commit hooks on all files |
| `typing` | Runs mypy and pyright |
| `docs` | Builds the documentation with warnings as errors |
| `docs-auto` | Rebuilds documentation continuously and serves it locally |

To run the test suite directly:

```bash
pytest
```

To run the full tox matrix:

```bash
tox
```

Example projects include their own `tests/` directories, configured with pytest.

## Documentation

The documentation is written in reStructuredText under `docs/` and built with Sphinx using the `dirhtml` builder. Topics include quickstart, the application context, blueprints, configuration, CLI, debugging, deployment, templating, testing, signals, and a step-by-step tutorial. Read the Docs is configured via `.readthedocs.yaml`.

To build the docs locally with tox:

```bash
tox -e docs
```

The published documentation is at https://flask.palletsprojects.com/.

## Contributing

Pull requests should follow the checklist in `.github/pull_request_template.md`. It asks contributors to open an issue first for code changes, add tests that fail without the change, update documentation and `CHANGES.rst`, and add `.. versionchanged::` entries where relevant. Issue templates for bug reports and feature requests are in `.github/ISSUE_TEMPLATE/`. The documentation refers to the Pallets contributing guide at https://palletsprojects.com/contributing/.

Continuous integration is configured with GitHub Actions workflows for tests, pre-commit checks, publishing, and lock maintenance under `.github/workflows/`.

## Changelog

Release notes are maintained in `CHANGES.rst`, which is included in the documentation. The current unreleased 3.2.0 entries include dropping Python 3.9 support and removing the previously deprecated `__version__` attribute.

## Community and Links

- Documentation: https://flask.palletsprojects.com/
- Changes: https://flask.palletsprojects.com/page/changes/
- Source: https://github.com/pallets/flask/
- Chat: https://discord.gg/pallets
- Donate: https://palletsprojects.com/donate

## License

Flask is licensed under the BSD-3-Clause license. See `LICENSE.txt` for the full text. The package is maintained by Pallets (contact@palletsprojects.com).

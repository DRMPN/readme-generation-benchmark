# Flask

Flask is a lightweight Python web application framework. It provides the essentials for building web applications—request handling, routing, templates, sessions, and more—while leaving many architectural and tooling choices to the developer. That makes it suitable for small applications as well as larger projects built with extensions.

Flask is based on the [Werkzeug](https://werkzeug.palletsprojects.com/) WSGI toolkit and the [Jinja](https://jinja.palletsprojects.com/) template engine.

## Features

- URL routing and request/response handling
- Jinja templates with automatic escaping
- Session support and signed cookies
- Application and request contexts
- Blueprints for organizing applications
- A command-line interface for common development tasks
- Error handling, logging, and signals
- Support for asynchronous view functions when the async extra is installed
- An extension ecosystem for features such as database access and authentication

## Installation

Install Flask from PyPI:

```bash
python -m pip install Flask
```

To install this checkout for local development:

```bash
python -m pip install -e .
```

The project’s `pyproject.toml` and `uv.lock` contain its packaging and dependency configuration.

## Quick start

Create a file named `hello.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, Flask!"
```

Start the development server:

```bash
flask --app hello run --debug
```

Then open <http://127.0.0.1:5000/> in a browser. The debug server is intended for local development; use a production WSGI server when deploying an application.

### A route with a template

Flask looks for templates in a `templates` directory next to the application module:

```text
myapp/
├── app.py
└── templates/
    └── index.html
```

```python
# app.py
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Welcome")
```

```html
<!-- templates/index.html -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
  </head>
  <body>
    <h1>{{ title }}</h1>
  </body>
</html>
```

Jinja escapes template values by default, which helps protect pages from unsafe HTML.

## Application organization

A Flask application can be as simple as a single module. As it grows, you can organize related routes into **blueprints**, create an application factory, and use extensions for additional functionality. Flask does not require one particular project layout.

A typical larger application might look like this:

```text
myapp/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── blog.py
│   └── templates/
├── tests/
└── pyproject.toml
```

The documentation and examples in this repository include application factories, blueprints, database-backed applications, and other patterns.

## Repository contents

- **Flask package:** the framework implementation, including routing, contexts, sessions, templating, the CLI, and JSON support.
- **Tests:** automated tests for framework behavior, including requests, views, blueprints, configuration, sessions, and templates.
- **Documentation:** Sphinx documentation covering application development, deployment, extensions, and Flask’s APIs.
- **Examples:** sample applications and patterns, including a tutorial application, JavaScript examples, and a Celery integration example.

## Development and tests

Run the test suite from the repository’s development environment:

```bash
pytest
```

Project and test dependencies are configured in `pyproject.toml`. Consult the contributing documentation for the complete development setup and contribution guidelines.

## Documentation

The documentation source is in the `docs/` directory. It covers topics such as:

- Application setup, configuration, and application factories
- Routing, views, requests, and responses
- Templates, static files, and error handling
- Blueprints, signals, and application extensions
- Testing Flask applications
- Deployment and security considerations

The published documentation is available at <https://flask.palletsprojects.com/>.

## License

Flask is distributed under the BSD-3-Clause license. See [`LICENSE.txt`](LICENSE.txt) for the full license text.

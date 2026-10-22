# TagGenerator

A Django application for generating QR-code tags. The project includes a Django web interface, QR-code generation code, database models and migrations, and a frontend template.

## Contents

- [Requirements](#requirements)
- [Getting started](#getting-started)
- [Running the application](#running-the-application)
- [Using the application](#using-the-application)
- [Docker](#docker)
- [Tests and checks](#tests-and-checks)
- [Project structure](#project-structure)
- [Configuration and deployment](#configuration-and-deployment)
- [License](#license)

## Requirements

- Python 3
- `pip`
- The packages listed in `requirements.txt`

## Getting started

Clone or download the project, then open a terminal in the project directory.

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Apply the database migrations:

```bash
python manage.py migrate
```

## Running the application

Start Django’s development server:

```bash
python manage.py runserver
```

Then open the local address shown in the terminal, usually:

```text
http://127.0.0.1:8000/
```

The available pages and routes are defined in the project’s `urls.py` files.

## Using the application

Open the application in a browser and follow the available form or page to generate a QR-code tag. The project’s `qr_code_frontend.html` provides the frontend template, while `qrcode_tags.py` contains QR-tag-related code.

The exact fields, output format, and available routes depend on the implementation in the project.

## Docker

A `Dockerfile` is included. Build an image from the project directory:

```bash
docker build -t taggenerator .
```

Run the container using the port configured by the Dockerfile. If the application listens on port `8000` inside the container, for example:

```bash
docker run --rm -p 8000:8000 taggenerator
```

If the image requires environment variables or a different port, provide those according to the project’s Docker and Django configuration.

## Tests and checks

Run the Django test suite with:

```bash
python manage.py test
```

Run Django’s configuration checks with:

```bash
python manage.py check
```

## Project structure

The repository includes:

- `manage.py` — Django command-line utility.
- `settings.py` — Django project settings.
- `urls.py` — URL routing for the project and application.
- `wsgi.py`, `asgi.py` — WSGI and ASGI application entry points.
- `apps.py` — Django application configuration.
- `models.py` — database model definitions.
- `admin.py` — Django admin configuration.
- `views.py` — request handling and page logic.
- `qrcode_tags.py` — QR-code tag functionality.
- `qr_code_frontend.html` — frontend template.
- `0001_initial.py` — initial database migration.
- `tests.py` — automated tests.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — container build instructions.
- `setup.py`, `setup.cfg` — Python package and tool configuration.
- `LICENSE` — project license.

## Configuration and deployment

The project’s Django settings are in `settings.py`. Before deploying, review the settings for the target environment. In particular:

- Set a secure `SECRET_KEY` through an environment variable or other secret-management mechanism.
- Set `DEBUG = False` in production.
- Configure `ALLOWED_HOSTS` for the deployment’s hostnames.
- Configure the production database and static-file handling as needed.
- Serve the application through a production-ready WSGI or ASGI server rather than Django’s development server.

## License

See the [`LICENSE`](LICENSE) file for licensing terms.

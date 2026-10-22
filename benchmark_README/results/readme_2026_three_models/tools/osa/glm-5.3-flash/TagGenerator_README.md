# TagGenerator-mrnberwk

---

[![PyPi](https://badge.fury.io/py/TagGenerator.svg)](https://badge.fury.io/py/TagGenerator)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

TagGenerator is a Python web application built with Django that generates styled QR code images over HTTP. It provides a web form for interactive generation, an HTTP endpoint that returns QR code images on request, and a reusable template tag for embedding generated QR codes directly into Django templates. The project is aimed primarily at Django developers who want to serve or integrate QR code generation within their own projects, and secondarily at users of the bundled web interface. See Getting Started for setup and runnable steps.

---

## Core Features

- **HTTP QR code generation** — request styled QR code images as PNG over a simple GET endpoint, so any client (browser, template, script) can generate codes on the fly.
- **Styled image rendering** — QR codes are drawn with rounded modules and a radial gradient color mask, producing visually polished codes instead of plain black-and-white grids.
- **Django template tag integration** — embed QR codes in any Django template with a single tag that returns a ready-to-use image URL.
- **Bundled web frontend** — a built-in form page lets users enter text or a URL and instantly preview the generated QR code.
- **Reusable Django app packaging** — the app ships with models, migrations, and packaging metadata, making it straightforward to drop into other Django projects.

---

## Installation

**Prerequisites:** requires Python >=3.9

Install TagGenerator-mrnberwk using one of the following methods:

**Using PyPi:**

```sh
pip install TagGenerator
```

**Using Docker:**

The repository includes a `Dockerfile` for containerized deployment:

```sh
docker build -t taggenerator .
docker run -p 8000:8000 taggenerator
```

> Note: adjust the image tag and port mapping (assumed here as Django's default port 8000) to match the `Dockerfile`.

---

## Getting Started

## Prerequisites

- Python with Django 5.1.7 (see `requirements.txt` for the full dependency list, including the `qrcode` library used to generate styled images).
- The included SQLite database requires no additional setup.

## Quickstart

1. Clone or download the repository to your local machine.
2. Install the dependencies:

```bash
   pip install -r requirements.txt
```

3. Apply the database migrations:

```bash
   python manage.py migrate
```

4. Start the development server:

```bash
   python manage.py runserver
```

5. Open `http://127.0.0.1:8000/qrcode/` in your browser to use the QR code generator form, or request an image directly, e.g. `http://127.0.0.1:8000/qrcode/generate/?data=Hello` (PNG response).

> Note: The bundled `settings.py` uses `DEBUG = True` and a hardcoded development secret key, so this setup is intended for local development only.

---

## API Reference

This project is a Django web application rather than a Python library with a callable API. Its public usage surface consists of HTTP endpoints, Django views, a model, and a template tag, all defined in the `QrCode` app.

### HTTP Endpoints

Defined in `QrCode/urls.py` (namespace `qrcode`, mounted at `qrcode/` via `TagGenerator/urls.py`):

| Endpoint | View | Purpose |
| --- | --- | --- |
| `GET /qrcode/` | `QRCodeHomeView` | Renders the QR code generator frontend (`templates/qr_code_frontend.html`). |
| `GET /qrcode/generate/?data=<text>` | `GenerateQRCodeView` | Returns a styled QR code image as a `image/png` response. The `data` query parameter supplies the text/URL to encode (default: `"Hello, Beautiful QR Code!"`). |

### Views (`QrCode/views.py`)

| Symbol | Purpose |
| --- | --- |
| `QRCodeHomeView` (`TemplateView`) | Serves the generator page. |
| `GenerateQRCodeView` (`View`) | Builds a QR code (high error correction, rounded modules, radial gradient mask) and returns it as a PNG. |

### Template Tag (`QrCode/templatetags/qrcode_tags.py`)

Load with `{% load qrcode_tags %}`:

- `{% qrcode_url data %}` — Returns the URL to the QR code generation endpoint for the given data. Example:

```html
  <img src="{% qrcode_url 'Some text to encode' %}" alt="QR Code">
```

### Model (`QrCode/models.py`)

| Symbol | Purpose |
| --- | --- |
| `QRCode` | Stores encoded payload (`data` `TextField`) and creation timestamp (`created`, auto-set). Its `__str__` returns the first 50 characters of `data`. |

No programmatic Python API (e.g., importable functions for direct QR generation) is exposed beyond the Django views above; reuse happens through the endpoints or the template tag.

---

## Testing

Tests for the `QrCode` app live in `QrCode/tests.py`. As a standard Django project, tests can be run with Django's test runner via `manage.py` (e.g., `python manage.py test`), which discovers tests in the installed apps.

Continuous integration is configured through GitHub Actions in `.github/workflows/django.yml`, which — based on its filename — appears to handle automated test runs. The repository also includes `publish-docker.yml` and `python-publish.yml` workflows; their purposes (likely Docker image and PyPI publishing, respectively) are inferred from their filenames only.

---

## Contributing

Contributions are welcome:

1. Clone or download the repository and install the dependencies (see [Getting Started](#getting-started)).
2. Make your changes in the `QrCode` app.
3. Run the test suite in `QrCode/tests.py` with `python manage.py test` and ensure it passes.
4. Submit your changes via a pull request, and make sure the CI workflow (`.github/workflows/django.yml`) completes successfully.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

> **Note:** The citation below contains placeholder values (`README Benchmark`, year `2026`, and `REPOSITORY_URL`). Replace them with the actual author, year, and canonical repository URL before publishing.

### APA format:

    README Benchmark (2026). TagGenerator-mrnberwk repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{TagGenerator-mrnberwk,

        author = {README Benchmark},

        title = {TagGenerator-mrnberwk repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
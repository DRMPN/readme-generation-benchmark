# TagGenerator

A reusable Django app for QR code generation.

TagGenerator ships a self-contained Django app (`QrCode`) that renders styled PNG QR codes on the fly from any URL, plus a small demo project so you can run the whole thing locally. It also ships a Django template tag so you can embed generated QR codes directly into your own templates with a single tag.

- **Package name:** `TagGenerator` (version 1.0.2 on PyPI packaging metadata)
- **Reusable app:** `QrCode`
- **Author:** Dada Nanjesha
- **License:** MIT
- **Repository:** https://github.com/DadaNanjesha/TagGenerator

---

## Features

- **Reusable Django app** — drop `QrCode` into any Django project's `INSTALLED_APPS` and include its URLconf.
- **Styled QR code images** — QR codes are generated as PNG images with rounded module drawers and a radial gradient color mask, using high (`H`) error correction.
- **Arbitrary data support** — pass any text or URL via the `data` query parameter; a friendly default ("Hello, Beautiful QR Code!") is used when none is provided.
- **QR code model** — a `QRCode` model stores the encoded data and its creation timestamp, with a ready-to-use admin registration.
- **Template tag** — the `qrcode_url` tag builds the correct image URL for any data string inside your templates.
- **Demo frontend** — a simple HTML page with a form to generate QR codes interactively.
- **Docker support** — a `Dockerfile` is included for containerized deployment.
- **CI/CD** — GitHub Actions workflows for running tests, publishing Docker images to GHCR, and publishing the Python package to PyPI on releases.

---

## Requirements

- Python **3.9+**
- **Django 4.0+** (the bundled demo project was generated with Django 5.1)
- [qrcode](https://pypi.org/project/qrcode/)
- [Pillow](https://pypi.org/project/Pillow/) (used for the styled PIL-based QR images)

Dependencies are declared both in `requirements.txt` and in `setup.py`'s `install_requires`.

---

## Installation

### From source

```bash
git clone https://github.com/DadaNanjesha/TagGenerator.git
cd TagGenerator

# Recommended: create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### As a package

The project is packaged for PyPI (`TagGenerator`), so once installed you can use the `QrCode` app in your own Django project:

```bash
pip install TagGenerator
```

---

## Quick Start (demo project)

The repository contains a complete Django project (`TagGenerator`) that demonstrates the app:

```bash
# Apply migrations (creates the SQLite database)
python manage.py migrate

# Optionally create a superuser for the admin site
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Then visit:

| URL | Description |
| --- | --- |
| `http://127.0.0.1:8000/qrcode/` | Demo home page with a QR code generator form |
| `http://127.0.0.1:8000/qrcode/generate/?data=https://example.com` | Direct QR code image (PNG) for the given data |
| `http://127.0.0.1:8000/admin/` | Django admin (QRCode entries are registered there) |

---

## Using the `QrCode` app in your own Django project

1. **Install the package** (or copy the `QrCode` app into your project).

2. **Add the app** to `INSTALLED_APPS` in your `settings.py`:

   ```python
   INSTALLED_APPS = [
       # ...
       'QrCode',
   ]
   ```

3. **Include the URLconf** in your project's `urls.py`:

   ```python
   from django.urls import path, include

   urlpatterns = [
       # ...
       path("qrcode/", include("QrCode.urls", namespace="qrcode")),
   ]
   ```

4. **Run migrations** (the app includes a `QRCode` model):

   ```bash
   python manage.py migrate
   ```

### Endpoints

Once wired up, the app exposes two URLs under your chosen prefix (namespace `qrcode`):

| Name | Path | Description |
| --- | --- | --- |
| `qrcode:home` | `qrcode/` | Renders the demo template `qr_code_frontend.html` |
| `qrcode:generate` | `qrcode/generate/` | Returns a PNG QR code image |

### Generating a QR code

Request the generate endpoint with an optional `data` query parameter:

```
/qrcode/generate/?data=https://example.com
```

- If `data` is omitted, the default text `"Hello, Beautiful QR Code!"` is encoded.
- The response is always a PNG image (`Content-Type: image/png`).

QR codes are generated with the following characteristics (see `QrCode/views.py`):

- **Version:** 1
- **Error correction:** `ERROR_CORRECT_H` (high)
- **Box size:** 10, border: 4
- **Styling:** `RoundedModuleDrawer` and `RadialGradiantColorMask` (white background, black center gradient)

### Template tag

The app provides a `qrcode_url` template tag (defined in `QrCode/templatetags/qrcode_tags.py`) that builds the image URL for any data string. Load it and use it in your templates:

```django
{% load qrcode_tags %}

<img src="{% qrcode_url 'Some text to encode' %}" alt="QR Code">
```

This resolves the `qrcode:generate` URL and appends the properly URL-encoded `data` query string, so the image can be embedded directly in any page.

### Model

The `QRCode` model (`QrCode.models`) provides simple persistence for generated data:

| Field | Type | Notes |
| --- | --- | --- |
| `data` | `TextField` | The text encoded into the QR code |
| `created` | `DateTimeField` | Set automatically on creation (`auto_now_add`) |

The model is registered with the Django admin, listing `data` and `created` columns.

---

## Configuration

The `QrCode` app requires no special configuration beyond being installed and having its URLs included. A few project-level notes from the bundled demo settings (`TagGenerator/settings.py`):

- **Database:** SQLite (`db.sqlite3`) by default. The Dockerfile installs `libpq-dev`, so switching to PostgreSQL via the `DATABASES` setting is straightforward if desired.
- **Templates:** the demo project's `TEMPLATES` setting includes the project-level `templates/` directory, where `qr_code_frontend.html` lives. If you reuse only the `QrCode` app package (per `setup.py`'s `packages=["QrCode"]`), package data handling via `MANIFEST.in` includes project files as appropriate.
- **Debug/secret key:** the bundled `settings.py` uses a development-oriented configuration (`DEBUG = True`, a hard-coded insecure `SECRET_KEY`, empty `ALLOWED_HOSTS`). **Do not use these settings in production** — follow Django's deployment checklist to set a real secret key, disable debug, and configure allowed hosts.

---

## Docker

A `Dockerfile` is included. It builds an image based on `python:3.9-slim-buster`, installs dependencies from `requirements.txt`, exposes port **8000**, and starts the Django development server bound to `0.0.0.0:8000`:

```bash
docker build -t taggenerator .
docker run -p 8000:8000 taggenerator
```

Then open `http://localhost:8000/qrcode/`.

A Docker image is automatically built and pushed to the GitHub Container Registry (`ghcr.io/dadananjesha/taggenerator:latest`) on pushes to `main` via the `publish-docker.yml` workflow.

---

## Development

### Project layout

```
├── QrCode/                  # The reusable Django app
│   ├── admin.py             # Admin registration for the QRCode model
│   ├── apps.py              # AppConfig (QrcodeConfig)
│   ├── migrations/          # Database migrations
│   ├── models.py            # QRCode model
│   ├── templatetags/
│   │   └── qrcode_tags.py   # qrcode_url template tag
│   ├── tests.py             # Test suite
│   ├── urls.py              # App URL routes (namespace "qrcode")
│   └── views.py             # Home (template) and Generate (image) views
├── TagGenerator/            # Demo Django project
│   ├── settings.py          # Project settings
│   ├── urls.py              # Root URL configuration
│   ├── asgi.py / wsgi.py    # ASGI/WSGI entry points
├── templates/
│   └── qr_code_frontend.html  # Demo generator page
├── Dockerfile
├── manage.py
├── requirements.txt
├── setup.py / setup.cfg / MANIFEST.in
└── LICENSE
```

### Running locally

Standard Django development commands apply:

```bash
python manage.py runserver        # development server
python manage.py migrate          # apply migrations
python manage.py makemigrations   # create new migrations after model changes
```

---

## Testing

The test suite lives in `QrCode/tests.py` and covers:

- **`GenerateQRCodeViewTest`**
  - Generating a QR code with no `data` parameter returns HTTP 200, `Content-Type: image/png`, and non-empty content.
  - Generating a QR code with a specific `data` parameter (e.g. `https://example.com`) behaves the same.
- **`QRCodeHomeViewTest`**
  - The home view returns HTTP 200 and contains key HTML elements (`<form>` and the "QR Code Generator" heading).

Run the tests with:

```bash
python manage.py test
```

Tests are executed automatically by the **Django CI** GitHub Actions workflow on pushes to `main`/`dev` and pull requests targeting `main`, using Python 3.9 on Ubuntu.

---

## CI/CD

The repository includes three GitHub Actions workflows under `.github/workflows/`:

| Workflow | Trigger | What it does |
| --- | --- | --- |
| `django.yml` (Django CI) | Push to `main`/`dev`, PRs to `main` | Installs dependencies and runs `python manage.py test` |
| `publish-docker.yml` | Push to `main` | Builds and pushes the Docker image to `ghcr.io/dadananjesha/taggenerator:latest` |
| `python-publish.yml` | GitHub release published | Builds the distribution with `python -m build` and publishes it to PyPI via trusted publishing |

---

## Packaging

The project is distributed as the `TagGenerator` package (see `setup.py`):

- Packages: `QrCode`
- Dependencies: `Django>=4.0`, `qrcode`, `Pillow`
- Python requirement: `>=3.9`
- Classifiers: Django framework, Python 3, MIT license, OS-independent

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 DADA NANJESHA

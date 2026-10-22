# TagGenerator-beh2_7un

A Django-based web application for generating QR-code tags. Users can create tags through a web interface, and the application generates downloadable QR codes for each tag, with an admin backend for management.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
  - [Docker Installation](#docker-installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [License](#license)

---

## Overview

**TagGenerator** is a Django application that allows users to generate tags with associated QR codes. Each tag is stored in the database (via Django models), a QR code is generated for it, and a frontend page (`qr_code_frontend.html`) renders the tags and their QR codes. The Django admin interface provides convenient management of tags out of the box.

The project is packaged with `setup.py` / `setup.cfg` and ships with a `Dockerfile` for containerized deployment, as well as ASGI/WSGI entry points for flexible hosting.

---

## Features

- 🏷️ **Tag creation & management** — create, edit, and delete tags backed by Django models.
- 📱 **QR code generation** — automatic QR code generation for every tag (`qrcode_tags.py`).
- 🖥️ **Web frontend** — a dedicated HTML template for viewing/scanning generated QR codes.
- 🛠️ **Django admin integration** — manage tags through the built-in admin site.
- 🐳 **Docker support** — containerized deployment via the included `Dockerfile`.
- 🧪 **Test suite** — Django tests included in `tests.py`.
- ⚙️ **ASGI & WSGI support** — ready for both sync and async deployment targets.

---

## Tech Stack

| Component   | Technology |
|-------------|------------|
| Language    | Python 3   |
| Framework   | Django     |
| QR Codes    | `qrcode` library |
| Frontend    | HTML (Django templates) |
| Container   | Docker     |
| Packaging   | setuptools (`setup.py`, `setup.cfg`, `MANIFEST.in`) |

See [`requirements.txt`](requirements.txt) for the exact dependency list.

---

## Project Structure

```
TagGenerator-beh2_7un/
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker build configuration
├── LICENSE                    # Project license
├── MANIFEST.in                # Packaging manifest
├── setup.py                   # Package installation script
├── setup.cfg                  # Packaging configuration
│
├── <project>/                 # Django project package
│   ├── __init__.py
│   ├── settings.py            # Django settings
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI entry point
│   └── asgi.py                # ASGI entry point
│
└── tags/                      # Main application
    ├── __init__.py
    ├── apps.py                # App configuration
    ├── models.py              # Tag data models
    ├── views.py               # Request handlers
    ├── urls.py                # App URL routes
    ├── admin.py               # Admin site registration
    ├── qrcode_tags.py         # QR code generation logic
    ├── tests.py               # Test suite
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py    # Initial database migration
    └── templates/
        └── qr_code_frontend.html   # QR code frontend page
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- (Optional) Docker & Docker Compose

### Local Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/TagGenerator-beh2_7un.git
   cd TagGenerator-beh2_7un
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. Open your browser at:

   - Application: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

### Docker Installation

1. **Build the image**

   ```bash
   docker build -t taggenerator .
   ```

2. **Run the container**

   ```bash
   docker run -d -p 8000:8000 taggenerator
   ```

3. Access the app at `http://localhost:8000/`.

> **Note:** For production, migrate inside the container or run migrations as part of your entrypoint:
> ```bash
> docker run -it taggenerator python manage.py migrate
> ```

---

## Configuration

All Django settings live in `settings.py`. Key areas you may want to adjust:

| Setting | Purpose |
|---------|---------|
| `DATABASES` | Switch from the default SQLite to PostgreSQL/MySQL for production. |
| `ALLOWED_HOSTS` | Add your domain/IP when deploying. |
| `DEBUG` | Set to `False` in production. |
| `SECRET_KEY` | Load from an environment variable — never commit a production key. |
| `INSTALLED_APPS` | The `tags` app is registered here. |
| `STATIC_URL` / `STATIC_ROOT` | Static file handling for deployment. |

Example environment-based secret key setup:

```python
import os
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-key")
```

---

## Usage

1. **Start the server** (`python manage.py runserver`).
2. **Log in to the admin panel** at `/admin/` and create tags, or use the app's frontend.
3. **View generated QR codes** on the frontend page — each tag renders with its scannable QR code.
4. **Scan a QR code** with any mobile device to retrieve the tag's encoded target (e.g., a URL or identifier).

### QR Code Generation

The QR generation logic is isolated in `qrcode_tags.py`, making it easy to reuse:

```python
from tags.qrcode_tags import generate_qr

# Example: generate a QR code image for a tag
image = generate_qr("https://example.com/tag/123")
```

---

## Running Tests

Run the full Django test suite with:

```bash
python manage.py test
```

Or for a specific app:

```bash
python manage.py test tags
```

For coverage reporting (optional):

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Deployment

The project includes both **WSGI** and **ASGI** entry points:

- **WSGI** (`wsgi.py`) — for classic deployments with Gunicorn/uWSGI + Nginx:

  ```bash
  gunicorn <project>.wsgi:application --bind 0.0.0.0:8000
  ```

- **ASGI** (`asgi.py`) — for async-capable servers such as Daphne or Uvicorn:

  ```bash
  daphne -b 0.0.0.0 -p 8000 <project>.asgi:application
  ```

**Production checklist:**

- [ ] `DEBUG = False`
- [ ] Set a strong `SECRET_KEY` via environment variables
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use a production database (PostgreSQL recommended)
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Serve behind a reverse proxy (Nginx) with HTTPS
- [ ] Run `python manage.py migrate` before starting the server

---

## Installing as a Package

Because the project ships with `setup.py` and `setup.cfg`, it can also be installed as a reusable Python package:

```bash
pip install .
```

---

## License

This project is licensed under the terms found in the [`LICENSE`](LICENSE) file.

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

Please make sure tests pass before submitting:

```bash
python manage.py test
```

# TagGenerator

TagGenerator is a Django project built around a reusable Django app, **QrCode**, that generates QR code images over HTTP. It ships with a small web frontend for interactive generation, a direct image endpoint, a `{% qrcode_url %}` template tag for use in your own templates, and an optional `QRCode` model that can be managed through the Django admin.

Generated QR codes are styled with rounded modules and a radial gradient color mask, using the [`qrcode`](https://pypi.org/project/qrcode/) library with a Pillow-backed styled image factory.

## Features

- **HTTP image endpoint** — `GET /qrcode/generate/?data=<text>` returns a PNG QR code image.
- **Web frontend** — a demo page at `/qrcode/` with a form to enter text or a URL and preview the resulting QR code.
- **Template tag** — `{% qrcode_url 'some text' %}` builds the image URL for any data, ready to drop into an `<img>` tag.
- **Optional model** — a `QRCode` model (`data`, `created`) registered in the Django admin (the generation views do not use the database).
- **Tests** — unit tests covering both the image endpoint and the frontend page.

## Requirements

- Python >= 3.9
- Django >= 4.0 (the included project was generated with Django 5.1.7)
- qrcode
- Pillow

Pinned versions for the bundled dependencies are listed in `requirements.txt`.

## Getting Started

### 1. Clone and install dependencies

```bash
git clone https://github.com/DadaNanjesha/TagGenerator
cd TagGenerator
pip install -r requirements.txt
```

### 2. Apply migrations

```bash
python manage.py migrate
```

### 3. Run the development server

```bash
python manage.py runserver
```

Then open <http://127.0.0.1:8000/qrcode/>.

## URLs

| URL | Name | Description |
| --- | --- | --- |
| `/qrcode/` | `qrcode:home` | Frontend page with a form for entering text/URL to encode |
| `/qrcode/generate/?data=<text>` | `qrcode:generate` | Returns the QR code as a PNG image (`image/png`) |
| `/admin/` | — | Django admin, including the `QRCode` model |

If the `data` query parameter is omitted on the generate endpoint, the text `Hello, Beautiful QR Code!` is used.

Example direct image request:

```
http://127.0.0.1:8000/qrcode/generate/?data=https://example.com
```

## Using the Template Tag

In any Django template:

```django
{% load qrcode_tags %}

<img src="{% qrcode_url 'Some text to encode' %}" alt="QR Code">
```

The tag returns the URL of the generate endpoint with the data passed as a query string.

## Installing as a Reusable App

`QrCode` is packaged as an installable Django app (see `setup.py`). To use it in your own project:

1. Install the package or copy the `QrCode` app into your project.
2. Add `"QrCode"` to `INSTALLED_APPS`.
3. Include its URLs under a namespace:

   ```python
   from django.urls import path, include

   urlpatterns = [
       ...
       path("qrcode/", include("QrCode.urls", namespace="qrcode")),
   ]
   ```

4. If you want the `QRCode` model, run `python manage.py migrate` (the generation views themselves do not require the database).

Note that the demo frontend template, `templates/qr_code_frontend.html`, lives in the project-level `templates/` directory, which is on the project's `DIRS` template path.

## Running Tests

```bash
python manage.py test
```

The tests in `QrCode/tests.py` verify that:

- `/qrcode/generate/` responds with `200` and `image/png`, both with and without a `data` parameter.
- `/qrcode/` renders the form and the "QR Code Generator" heading.

## Docker

A `Dockerfile` is included for running the project in a container:

```bash
docker build -t taggenerator .
docker run -p 8000:8000 taggenerator
```

The container listens on port 8000 and starts Django's development server (`python manage.py runserver 0.0.0.0:8000`).

## Project Structure

```
TagGenerator/
├── QrCode/                     # Reusable QR code app
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── templatetags/
│   │   └── qrcode_tags.py      # {% qrcode_url %} template tag
│   ├── admin.py                # QRCode model admin
│   ├── apps.py
│   ├── models.py               # QRCode model (data, created)
│   ├── tests.py
│   ├── urls.py
│   └── views.py                # Home and image-generating views
├── TagGenerator/               # Django project (settings, root URLconf, WSGI/ASGI)
├── templates/
│   └── qr_code_frontend.html   # Demo frontend page
├── Dockerfile
├── manage.py
├── requirements.txt
├── setup.py                    # Packaging metadata (TagGenerator 1.0.2)
└── setup.cfg
```

## License

This project is licensed under the [MIT License](LICENSE). Copyright (c) 2025 Dada Nanjesha.

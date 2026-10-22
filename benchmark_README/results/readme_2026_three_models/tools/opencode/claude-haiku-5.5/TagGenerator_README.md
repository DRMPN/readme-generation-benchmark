# TagGenerator

TagGenerator is a Django project and reusable Django app (`QrCode`) for generating styled QR code images. A browser form takes text or a URL, and the app returns a PNG QR code. The app also provides a template tag that builds the image URL for use in your own templates.

The repository is [DadaNanjesha/TagGenerator](https://github.com/DadaNanjesha/TagGenerator) and is released under the MIT License.

## Features

- A simple HTML page with a text field and a **Generate** button (`/qrcode/`).
- An image endpoint (`/qrcode/generate/?data=...`) that returns a PNG QR code.
- Styled output: rounded modules and a radial gradient mask (black at the center, white background), using the `qrcode` library's styled image support.
- Error correction level H (the highest level in the `qrcode` library).
- A `qrcode_url` template tag for embedding QR codes in templates.
- A `QRCode` model (stores `data` and a `created` timestamp) registered in the Django admin.
- Basic tests for the image endpoint and the home page.

## Requirements

- Python 3.9 or later (from `setup.py`)
- Dependencies listed in `requirements.txt`:
  - `Django` (unpinned)
  - `qrcode==8.0`
  - `pillow==11.1.0`
  - `asgiref==3.8.1`
  - `sqlparse==0.5.3`
  - `tzdata==2025.1`
  - `colorama==0.4.6`

## Quick start (from source)

```bash
git clone https://github.com/DadaNanjesha/TagGenerator.git
cd TagGenerator

python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Then open:

- http://127.0.0.1:8000/qrcode/ for the QR code generator page
- http://127.0.0.1:8000/admin/ for the Django admin (requires a superuser, created with `python manage.py createsuperuser`)

The project uses SQLite, stored in `db.sqlite3` in the project root.

## Usage

### Web page

Go to `/qrcode/`, type text or a URL into the field, and click **Generate**. The page shows the QR code for the entered value. If no value is given, the page encodes the default text shown in its input field.

### Image endpoint

`GET /qrcode/generate/` returns a `image/png` response.

- `data` (query parameter): the text to encode. If omitted, the default text `Hello, Beautiful QR Code!` is encoded.

Example:

```
http://127.0.0.1:8000/qrcode/generate/?data=https://example.com
```

### Template tag

Load the tag library and use `qrcode_url` to build an image URL:

```django
{% load qrcode_tags %}
<img src="{% qrcode_url 'Some text to encode' %}" alt="QR Code">
```

The tag reverses the `qrcode:generate` URL name and URL-encodes the data.

## Running with Docker

The repository includes a `Dockerfile` based on `python:3.9-slim-buster`. It installs the requirements and runs the development server on port 8000.

```bash
docker build -t taggenerator .
docker run -p 8000:8000 taggenerator
```

Then open http://localhost:8000/qrcode/.

A GitHub Actions workflow (`.github/workflows/publish-docker.yml`) builds and pushes an image to GitHub Container Registry as `ghcr.io/dadananjesha/taggenerator:latest` on pushes to `main`.

## Using the app in another Django project

`setup.py` packages the `QrCode` app (name `TagGenerator`, version `1.0.2`). To use it in your own project:

1. Install the `qrcode` package and Pillow, along with Django 4.0 or later.
2. Add `"QrCode"` to `INSTALLED_APPS`.
3. Include its URLs under the `qrcode` namespace:

   ```python
   from django.urls import include, path

   urlpatterns = [
       path("qrcode/", include("QrCode.urls", namespace="qrcode")),
   ]
   ```

4. Run migrations: `python manage.py migrate`.

**Note:** The home page template, `templates/qr_code_frontend.html`, lives in this repository's project-level `templates/` directory and is not inside the `QrCode` package. In another project, the home view (`qrcode:home`) needs a template with that name. The image endpoint and the template tag do not depend on it.

## Project structure

```
.
├── manage.py                     # Django management entry point
├── TagGenerator/                 # Project settings and root URL configuration
│   ├── settings.py
│   └── urls.py                   # Mounts /admin/ and /qrcode/
├── QrCode/                       # Reusable Django app
│   ├── models.py                 # QRCode model (data, created)
│   ├── views.py                  # QRCodeHomeView, GenerateQRCodeView
│   ├── urls.py                   # "generate/" and "" routes (namespace "qrcode")
│   ├── admin.py                  # Registers QRCode in the admin
│   ├── templatetags/qrcode_tags.py  # qrcode_url template tag
│   ├── migrations/0001_initial.py
│   └── tests.py
├── templates/qr_code_frontend.html  # Home page template
├── requirements.txt
├── setup.py
├── Dockerfile
└── .github/workflows/            # CI and publishing workflows
```

## Configuration

Settings are in `TagGenerator/settings.py`. The current values are development defaults:

- `DEBUG = True`
- `ALLOWED_HOSTS = []`
- `SECRET_KEY` is hardcoded in the file.
- The database is SQLite (`db.sqlite3`).
- `TIME_ZONE = 'UTC'` and `LANGUAGE_CODE = 'en-us'`.

Before deploying, you should move the secret key out of the source, set `DEBUG = False`, and configure `ALLOWED_HOSTS`. The Docker image runs `manage.py runserver`, which is Django's development server and is not intended for production.

## Running tests

```bash
python manage.py test
```

The tests in `QrCode/tests.py` check that:

- the generate endpoint returns HTTP 200 with a `image/png` content type and non-empty content, both with and without `data`;
- the home page loads and contains a `<form` element and the heading "QR Code Generator".

The GitHub Actions workflow `.github/workflows/django.yml` runs these tests on pushes to `main` and `dev` and on pull requests to `main`, using Python 3.9.

## Continuous integration and releases

- **Django CI** (`django.yml`): installs `requirements.txt` and runs `python manage.py test` on Python 3.9.
- **Upload Python Package** (`python-publish.yml`): when a GitHub release is published, builds the distribution with `python -m build` and publishes it to PyPI through the `pypi` environment using trusted publishing.
- **Publish Docker Image** (`publish-docker.yml`): described in the Docker section above.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

# TagGenerator

TagGenerator is a Django project containing a reusable `QrCode` app for generating QR code images. It provides a simple web page and an HTTP endpoint that returns a styled QR code as a PNG. The app also defines a Django model for QR code data and registers it in the admin.

## Features

- Generate a QR code image from text supplied in a request.
- Return generated images as `image/png`.
- Apply rounded modules and a radial color mask to generated QR codes.
- Provide a home page at `/qrcode/`.
- Include a `QRCode` model with a text field and creation timestamp.
- Register QR code records in the Django admin.

## Requirements

The project supports Python 3.9 and later. Its package metadata declares Django 4.0 or later, `qrcode`, and Pillow as installation requirements. The Docker image uses Python 3.9.

The project settings use SQLite by default, with the database stored in `db.sqlite3` in the project directory.

## Setup

Clone the repository and move into its directory. Create and activate a virtual environment, then install the project dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\activate
```

Apply the database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

By default, Django serves the project at `http://127.0.0.1:8000/`. The QR code home page is at `http://127.0.0.1:8000/qrcode/`.

## Usage

### Generate an image

The generation endpoint is:

```text
GET /qrcode/generate/
```

Pass the text to encode in the `data` query parameter. For example:

```text
http://127.0.0.1:8000/qrcode/generate/?data=https%3A%2F%2Fexample.com
```

The endpoint responds with a PNG image. If `data` is omitted, the default content is `Hello, Beautiful QR Code!`. The generated QR code uses high error correction, rounded modules, and a radial color mask with a white background and black center.

The application also provides a home page at `/qrcode/`. Its template is `templates/qr_code_frontend.html`; the project’s tests check that the page loads and contains a form and the heading “QR Code Generator.”

### Use the app’s template tag

The `QrCode` app includes a `qrcode_url` template tag for building a generation URL from a value:

```django
{% load qrcode_tags %}

<img src="{% qrcode_url 'Some text to encode' %}" alt="QR Code">
```

The tag URL-encodes the supplied value and reverses the `qrcode:generate` route, so it works with the app’s configured URL namespace.

### Admin

The project mounts Django’s admin at `/admin/`. The `QRCode` model is registered there, with its `data` and `created` fields displayed in the list view. To create an admin account locally:

```bash
python manage.py createsuperuser
```

The model defines a text field for `data` and an automatically populated `created` timestamp. The generation endpoint itself returns an image; it does not create a model record.

## Configuration

Project settings are in `TagGenerator/settings.py`. The configured database is SQLite, templates are loaded from the top-level `templates` directory as well as installed apps, and the `QrCode` app is enabled in `INSTALLED_APPS`.

The checked-in settings are intended for development: `DEBUG` is enabled, `ALLOWED_HOSTS` is empty, and the secret key is a development value. Before deploying, configure an appropriate secret key, disable debug mode, and set allowed hosts for the deployment environment. The repository does not define environment-variable-based settings, so any production-specific configuration must be supplied separately.

## Development

The Django project package is `TagGenerator`; the reusable Django application is `QrCode`. URL routing is configured in `TagGenerator/urls.py`, which includes the app under the `/qrcode/` prefix. The app’s named routes are `qrcode:home` and `qrcode:generate`.

After changing models, create and apply migrations as needed:

```bash
python manage.py makemigrations
python manage.py migrate
```

The package metadata is in `setup.py`. It identifies the distribution as `TagGenerator`, version `1.0.2`, and includes the `QrCode` package. The repository also contains GitHub Actions workflows for running Django tests, building and publishing a Docker image on pushes to `main`, and building and publishing Python distributions when a release is published.

### Docker

The supplied `Dockerfile` builds an image from `python:3.9-slim-buster`, installs `libpq-dev` and the Python requirements, exposes port `8000`, and starts Django’s development server on `0.0.0.0:8000`.

Build and run the image with:

```bash
docker build -t taggenerator .
docker run --rm -p 8000:8000 taggenerator
```

This container command uses Django’s `runserver`; it is not presented in the repository as a production server configuration.

## Testing

Run the Django test suite from the repository root:

```bash
python manage.py test
```

The tests cover the home page response and check that it includes a form and the “QR Code Generator” heading. They also verify that the generation endpoint returns a non-empty PNG both when using its default data and when given a `data` query parameter.

The Django CI workflow runs this same command with Python 3.9 after installing dependencies from `requirements.txt`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full license text.

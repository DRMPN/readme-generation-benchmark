# TagGenerator

TagGenerator is a Django project containing the `QrCode` app. It provides a small web page for entering text or a URL and generates a styled QR code PNG from that value. The app also exposes a URL that can be used directly as an image source.

## Features

- A QR code page at `/qrcode/` with a text input and generated image.
- A PNG generation endpoint at `/qrcode/generate/`, accepting the content in the `data` query parameter.
- QR codes rendered with rounded modules, a radial color mask, a white background, and high error correction.
- A Django template tag, `{% qrcode_url %}`, for building generation URLs in templates.

The QR code view responds to GET requests and does not save generated data. The project also defines a `QRCode` model with `data` and `created` fields; the generation view does not use that model.

## Requirements

- Python 3.9 or later
- Django 4.0 or later
- `qrcode`
- Pillow

The repository's `requirements.txt` provides the project dependencies. The package metadata in `setup.py` declares Django, `qrcode`, and Pillow as install requirements.

## Run the project

From the repository root, create and activate a virtual environment, then install dependencies:

```sh
python -m venv .venv
```

On macOS or Linux:

```sh
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies, apply migrations, and start Django's development server:

```sh
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/qrcode/> to use the page. The project includes a development configuration with `DEBUG = True` and a development secret key; configure secure settings before deploying it.

## Generate a QR code

Pass the text or URL as the `data` query parameter:

```text
http://127.0.0.1:8000/qrcode/generate/?data=https%3A%2F%2Fexample.com
```

The response is an `image/png`. If `data` is omitted, the endpoint encodes `Hello, Beautiful QR Code!`. On the web page, the form submits its `data` value with GET, and the image is generated from that value. When the page is first opened without a value, its template uses `Input your text here` for the displayed QR code.

In a Django template, load and use the provided tag to make an image URL:

```django
{% load qrcode_tags %}
<img src="{% qrcode_url 'Some text to encode' %}" alt="QR Code">
```

## Use the app in another Django project

The repository declares a Python distribution named `TagGenerator`, which can be built/installed from its checkout with:

```sh
python -m pip install .
```

There is a packaging limitation in the current `setup.py`: it explicitly lists only the `QrCode` package. As a result, the `QrCode.templatetags` and `QrCode.migrations` subpackages are not included by that package list. To use those features from an installed distribution, the package configuration needs to include the subpackages; otherwise, keep the repository source available to the Django project.

Add `QrCode` to `INSTALLED_APPS`, and include its URL configuration with the `qrcode` namespace. For example, in the host project's URL configuration:

```python
from django.urls import include, path

urlpatterns = [
    path("qrcode/", include("QrCode.urls", namespace="qrcode")),
]
```

The namespace is used by the `qrcode_url` template tag to reverse the generation route. The app's home page uses the `qr_code_frontend.html` template from the repository's top-level `templates/` directory; configure the host project's template directories to include that template if you want to use the included page. The generation endpoint itself returns the PNG response.

## Tests

Run the Django test suite from the repository root:

```sh
python manage.py test
```

The tests cover the home page and generation endpoint, including PNG responses with and without a supplied `data` parameter.

## License

This project is provided under the MIT License. See [LICENSE](LICENSE).

# httpx-j22he5t3

---

[![PyPi](https://badge.fury.io/py/httpx.svg)](https://badge.fury.io/py/httpx)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![mkdocs-material](https://img.shields.io/badge/Material%20for%20MkDocs-526CFE.svg?style=flat&logo=Material-for-MkDocs&logoColor=white)
![pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat&logo=Pytest&logoColor=white)
![ruff](https://img.shields.io/badge/Ruff-FCC21B.svg?style=flat&logo=Ruff&logoColor=black)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

httpx is a Python HTTP client library for sending HTTP requests from applications and services, offering both synchronous and asynchronous client APIs alongside a top-level convenience API for common request methods. It is primarily aimed at Python developers integrating HTTP requests into their code, as well as library authors who can build on its pluggable transport layer (including ASGI, WSGI, and mock transports). An optional command-line client is also available for making requests from the terminal. Newcomers can start with the quickstart documentation, which includes usage snippets covering basic and streaming requests.

---

## Core Features

- Provides both sync (`Client`) and async (`AsyncClient`) HTTP request APIs with a consistent interface, letting developers choose the concurrency model that fits their application.
- Includes a top-level convenience API for common verbs (`get`, `post`, `put`, `patch`, `delete`, `head`, `options`) plus `request` and `stream`, enabling one-off requests without manually managing a client, and streaming responses without loading the full body into memory.
- Supports a pluggable transport layer with default HTTP, ASGI, WSGI, and Mock transports, so applications and tests can route requests against ASGI/WSGI apps or simulated responses without a live server.
- Offers built-in request configuration for authentication, proxies, timeouts, redirects, cookies, headers, query parameters, and SSL verification, covering typical client behavior in one place.
- Ships an optional command-line client (installed via the `httpx[cli]` extra) for sending requests from the terminal with formatted output.

---

## Installation

Install httpx-j22he5t3 using pip:

```sh
pip install httpx
```

To include the optional command-line client dependencies, install with the `cli` extra:

```sh
pip install 'httpx[cli]'
```

---

## Usage

After installation, use HTTPX either as a Python library or via the optional command-line client.

### Python API

Top-level convenience functions for one-off requests:

```pycon
>>> import httpx
>>> response = httpx.request('GET', 'https://httpbin.org/get')
>>> response
<Response [200 OK]>
```

Shorthands such as `httpx.get(...)`, `httpx.post(...)`, and `httpx.stream(...)` are also available (see `httpx/_api.py`).

For anything beyond one-off scripts, use a `Client` instance, ideally as a context manager so connections are cleaned up:

```python
with httpx.Client() as client:
    response = client.get("https://www.example.com/")
```

Clients reuse connections via pooling and support cookie persistence, shared configuration, proxies, and HTTP/2.

Authentication can be configured per request or on the client:

```pycon
>>> auth = httpx.BasicAuth(username="finley", password="secret")
>>> client = httpx.Client(auth=auth)
>>> response = client.get("https://httpbin.org/basic-auth/finley/secret")
```

For asynchronous code, use `httpx.AsyncClient`.

### CLI

If installed with the `httpx[cli]` extra, a command-line client is available (implemented in `httpx/_main.py` using `click`, `rich`, and `pygments`):

```
httpx <URL> [OPTIONS]
```

Supported options include `-m/--method`, `-p/--params`, `-d/--data`, `-j/--json`, `-h/--headers`, `--auth <USER PASS>`, `--proxy URL`, `--timeout FLOAT`, `--follow-redirects`, `--no-verify`, `--http2`, `--download FILE`, and `-v/--verbose`. Run `httpx --help` for the full list.

If the CLI dependencies are missing, invoking `httpx.main()` prints a message directing you to reinstall with `pip install 'httpx[cli]'`.

---

## Architecture

httpx is a single-package, modular Python HTTP client library with clear layering:

- **Top-level convenience API** (`httpx/_api.py`): module-level `get`, `post`, `request`, `stream`, and related functions that spin up a `Client` for one-off requests.
- **Client layer** (`httpx/_client.py`): `Client` (sync) and `AsyncClient` (async) manage request lifecycle, cookies, headers, auth, redirects, event hooks, and timeouts. They share configuration and behavior via a common `BaseClient` base class.
- **Request/Response models** (`httpx/_models.py`, `_urls.py`, `_multipart.py`, `_content.py`): `Request`, `Response`, `URL`, `QueryParams`, `Headers`, and `Cookies` objects representing HTTP messages and URL state.
- **Transport layer** (`httpx/_transports/`): pluggable `BaseTransport`/`AsyncBaseTransport` interfaces with concrete implementations — `HTTPTransport`/`AsyncHTTPTransport` (default, delegating to the low-level `httpcore` layer), plus `ASGITransport`, `WSGITransport`, and `MockTransport` for in-process ASGI/WSGI apps and testing.
- **Supporting modules**: authentication (`_auth.py`), configuration such as timeouts, limits, and proxies (`_config.py`), content decoders (`_decoders.py`), URL parsing (`_urlparse.py`), typed exceptions (`_exceptions.py`), and type aliases (`_types.py`).
- **Optional CLI** (`httpx/_main.py`): a command-line client built with `click`, `rich`, and `pygments`, installed via the `httpx[cli]` extra; it delegates to `Client` to send requests.

Control flow is straightforward: convenience functions and the CLI construct a `Client`, the client builds a `Request` from models, selects a transport, sends the request (handling auth, redirects, and decoding via the support modules), and returns a `Response`.

---

## Testing

The test suite lives in the `tests/` directory, covering client behavior (`tests/client/`), models (`tests/models/`), and top-level functionality such as auth, content, decoders, exceptions, multipart, timeouts, and the ASGI/WSGI transports. Shared fixtures and helpers are in `tests/conftest.py`, `tests/common.py`, and `tests/concurrency.py`, with fixture files under `tests/fixtures/`.

To run the tests locally, use the repository's `scripts/test` script. Coverage can be checked with `scripts/coverage`.

Continuous integration runs the test suite via the GitHub Actions workflow in `.github/workflows/test-suite.yml`. Related maintenance scripts include `scripts/check` and `scripts/lint` for pre-submission validation. See `docs/contributing.md` and `.github/CONTRIBUTING.md` for contribution workflow details.

---

## Documentation

A detailed httpx-j22he5t3 description is available [here](./docs). The documentation site, built with Material for MkDocs
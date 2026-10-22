# httpx-khdjoj31

A Python HTTP client library with a sync and async API, built on the same interface as [Requests](https://docs.python-requests.org/), with support for HTTP/1.1, HTTP/2, and modern networking features.

This repository, `httpx-khdjoj31`, contains the HTTPX source code, documentation, test suite, and build tooling.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Making Requests](#making-requests)
  - [Async Support](#async-support)
  - [Clients](#clients)
  - [Request and Response Data](#request-and-response-data)
  - [Authentication](#authentication)
  - [Timeouts](#timeouts)
  - [Proxies](#proxies)
  - [SSL and Certificates](#ssl-and-certificates)
  - [HTTP/2](#http2)
  - [Resource Limits](#resource-limits)
  - [Event Hooks](#event-hooks)
  - [Transports](#transports)
  - [Exceptions](#exceptions)
  - [Command-Line Interface](#command-line-interface)
  - [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Development](#development)
  - [Setting Up a Development Environment](#setting-up-a-development-environment)
  - [Running Tests](#running-tests)
  - [Linting and Type Checking](#linting-and-type-checking)
  - [Coverage](#coverage)
  - [Building and Publishing](#building-and-publishing)
  - [Documentation](#documentation)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Overview

HTTPX is a fully featured HTTP client for Python 3. It provides:

- A **synchronous** API, similar to `requests`
- An **asynchronous** API, compatible with `asyncio` and `trio`
- **HTTP/1.1** and optional **HTTP/2** support
- Strict **timeouts** on every operation by default
- Support for **WSGI** and **ASGI** applications, useful for testing without a network connection
- Fully type-annotated public API

The library is designed to be a drop-in replacement for most `requests` use cases while adding async support and modern protocol features.

---

## Features

- **Familiar API**: Client methods (`get`, `post`, `put`, `patch`, `delete`, `head`, `options`, `request`, `stream`) match `requests`.
- **Sync and async clients**: `httpx.Client` and `httpx.AsyncClient`.
- **HTTP/2 support**: Opt-in via the `http2` extra.
- **Connection pooling** and configurable **resource limits**.
- **Granular timeouts**: separate connect, read, write, and pool timeouts.
- **Authentication**: Basic, Digest, and custom auth flows.
- **Proxy support**: HTTP, HTTPS, and SOCKS proxies (SOCKS via extra).
- **Streaming**: Stream request and response bodies.
- **Multipart uploads** and file uploads.
- **Event hooks** for inspecting or modifying requests and responses.
- **Redirect handling** with configurable limits.
- **Cookie persistence** across requests within a client.
- **Content decoding**: gzip, deflate, and Brotli (via extra), plus Zstandard where supported.
- **Custom transports** and **mock transports** for testing.
- **ASGI and WSGI transports** for calling applications directly.
- **Command-line tool** for making requests from the terminal.
- **Strict URL and header parsing** aligned with WHATWG URL standards.

---

## Installation

Install from PyPI:

```bash
pip install httpx
```

### Optional Extras

HTTPX provides optional dependencies for additional features:

| Extra | Installs | Purpose |
|-------|----------|---------|
| `httpx[http2]` | `h2` | HTTP/2 support |
| `httpx[brotli]` | `brotli` / `brotlicffi` | Brotli content decoding |
| `httpx[zstd]` | `zstandard` | Zstandard content decoding |
| `httpx[socks]` | `socksio` | SOCKS proxy support |
| `httpx[cli]` | `rich`, `click`, `pygments` | Command-line interface |

Install several at once:

```bash
pip install "httpx[http2,brotli,socks,cli]"
```

### Requirements

- A supported Python 3 version (see `pyproject.toml` for the current minimum).

---

## Quick Start

```python
import httpx

response = httpx.get("https://www.example.org/")
print(response.status_code)   # 200
print(response.headers["content-type"])
print(response.text)
```

Async version:

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.example.org/")
        print(response.status_code)

asyncio.run(main())
```

---

## Usage

### Making Requests

HTTPX supports all standard HTTP methods at the top level:

```python
import httpx

r = httpx.get("https://httpbin.org/get", params={"q": "httpx"})
r = httpx.post("https://httpbin.org/post", json={"key": "value"})
r = httpx.put("https://httpbin.org/put", data={"field": "value"})
r = httpx.patch("https://httpbin.org/patch", content=b"raw bytes")
r = httpx.delete("https://httpbin.org/delete")
r = httpx.head("https://httpbin.org/get")
r = httpx.options("https://httpbin.org/get")
r = httpx.request("GET", "https://httpbin.org/get")
```

Passing query parameters, headers, and bodies:

```python
r = httpx.get(
    "https://httpbin.org/get",
    params={"page": 2, "sort": "name"},
    headers={"User-Agent": "my-app/1.0", "Accept": "application/json"},
)

r = httpx.post(
    "https://httpbin.org/post",
    data={"username": "alice"},          # form-encoded
)

r = httpx.post(
    "https://httpbin.org/post",
    json={"username": "alice"},          # JSON-encoded
)

r = httpx.post(
    "https://httpbin.org/post",
    files={"upload": ("report.csv", open("report.csv", "rb"), "text/csv")},
)
```

### Async Support

The async API mirrors the sync API but uses `await`:

```python
import asyncio
import httpx

async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        return await asyncio.gather(*tasks)

responses = asyncio.run(fetch_all([
    "https://www.example.org/",
    "https://www.python.org/",
]))
```

HTTPX's async client works with `asyncio` and `trio` backends.

### Clients

For multiple requests, use a `Client` instance. It reuses connections, persists cookies, and applies shared configuration.

```python
import httpx

with httpx.Client(
    base_url="https://api.example.com",
    headers={"Authorization": "Bearer TOKEN"},
    timeout=10.0,
) as client:
    users = client.get("/users").json()
    client.post("/users", json={"name": "Alice"})
```

Client options include:

- `base_url`: prepended to relative URLs
- `headers`: default headers
- `cookies`: default cookies
- `params`: default query parameters
- `auth`: default authentication
- `timeout`: default timeout configuration
- `limits`: connection pool limits
- `follow_redirects`: whether to follow redirects (default `False` for the client)
- `max_redirects`: redirect limit
- `verify`: SSL verification settings
- `proxy` / `mounts`: proxy configuration
- `http1` / `http2`: protocol selection
- `event_hooks`: request and response hooks
- `transport`: custom transport
- `trust_env`: whether to read environment variables

Always close clients when finished, or use a context manager.

### Request and Response Data

**Response attributes:**

```python
r = httpx.get("https://httpbin.org/get")

r.status_code        # int
r.reason_phrase      # str, e.g. "OK"
r.headers            # Headers (case-insensitive mapping)
r.cookies            # Cookies
r.text               # decoded body as str
r.content            # body as bytes
r.json()             # parsed JSON
r.url                # final URL
r.history            # list of redirect responses
r.elapsed            # timedelta
r.request            # the Request object
r.is_success         # True for 2xx
r.is_redirect        # True for redirect status codes
r.raise_for_status() # raises HTTPStatusError on 4xx/5xx
```

**Streaming responses:**

```python
with httpx.stream("GET", "https://example.org/large-file") as response:
    for chunk in response.iter_bytes():
        process(chunk)

    # Other iterators:
    # response.iter_text()
    # response.iter_lines()
    # response.iter_raw()
```

Async streaming:

```python
async with httpx.AsyncClient() as client:
    async with client.stream("GET", url) as response:
        async for chunk in response.aiter_bytes():
            process(chunk)
```

**Headers and cookies:**

```python
headers = httpx.Headers({"Content-Type": "application/json"})
headers["content-type"]   # case-insensitive lookup

cookies = httpx.Cookies()
cookies.set("session", "abc123", domain="example.org")
r = httpx.get("https://example.org/", cookies=cookies)
```

**Query parameters:**

```python
params = httpx.QueryParams({"tag": ["python", "http"]})
```

**Text encodings:**

When decoding `response.text`, HTTPX uses the charset from `Content-Type` when available, and falls back to charset detection otherwise. You can override the encoding:

```python
r.encoding = "utf-8"
print(r.text)
```

### Authentication

Basic authentication:

```python
r = httpx.get("https://example.com", auth=("user", "password"))
```

Digest authentication:

```python
r = httpx.get("https://example.com", auth=httpx.DigestAuth("user", "password"))
```

Custom authentication by subclassing `httpx.Auth`:

```python
class BearerAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request

r = httpx.get("https://api.example.com", auth=BearerAuth("secret"))
```

Auth flows can yield multiple requests, which allows challenge-response schemes.

### Timeouts

HTTPX applies a default timeout of 5 seconds to all operations. You can configure each phase separately:

```python
httpx.get("https://example.org", timeout=10.0)

httpx.get(
    "https://example.org",
    timeout=httpx.Timeout(connect=2.0, read=10.0, write=5.0, pool=1.0),
)

httpx.get("https://example.org", timeout=None)  # disable timeouts
```

See [`timeouts.md`](https://www.python-httpx.org/advanced/timeouts/) in the docs for details.

### Proxies

```python
# Single proxy for all requests
with httpx.Client(proxy="http://localhost:8030") as client:
    client.get("https://example.org")

# Proxy with authentication
with httpx.Client(proxy="http://user:pass@localhost:8030") as client:
    client.get("https://example.org")

# Per-scheme routing with mounts
mounts = {
    "http://": httpx.HTTPTransport(proxy="http://localhost:8030"),
    "https://": httpx.HTTPTransport(proxy="http://localhost:8031"),
}
with httpx.Client(mounts=mounts) as client:
    client.get("https://example.org")
```

SOCKS proxies require the `socks` extra:

```python
with httpx.Client(proxy="socks5://localhost:1080") as client:
    client.get("https://example.org")
```

### SSL and Certificates

By default, HTTPX verifies certificates using the `certifi` CA bundle.

```python
# Custom CA bundle
httpx.get("https://internal.example", verify="/path/to/ca-bundle.pem")

# Client certificate
httpx.get("https://example.org", cert="/path/to/client.pem")
httpx.get("https://example.org", cert=("/path/to/client.crt", "/path/to/client.key"))

# Disable verification (not recommended in production)
httpx.get("https://example.org", verify=False)
```

Custom `ssl.SSLContext` objects are also accepted for `verify`.

### HTTP/2

HTTP/2 is opt-in. Install the extra, then enable it:

```bash
pip install "httpx[http2]"
```

```python
with httpx.Client(http2=True) as client:
    r = client.get("https://www.google.com")
    print(r.http_version)  # "HTTP/2"
```

HTTP/1.1 remains available by default. You can enable both with `http1=True, http2=True`.

### Resource Limits

Control connection pool size:

```python
limits = httpx.Limits(
    max_connections=100,
    max_keepalive_connections=20,
    keepalive_expiry=5.0,
)

with httpx.Client(limits=limits) as client:
    ...
```

### Event Hooks

Event hooks run before a request is sent and after a response is received. They are useful for logging, tracing, and metrics.

```python
def log_request(request):
    print(f"Request: {request.method} {request.url}")

def log_response(response):
    print(f"Response: {response.status_code}")
    response.raise_for_status()

with httpx.Client(
    event_hooks={"request": [log_request], "response": [log_response]}
) as client:
    client.get("https://example.org")
```

Async clients accept async hooks as well.

### Transports

Transports handle the low-level sending of requests. HTTPX provides several:

- `httpx.HTTPTransport` / `httpx.AsyncHTTPTransport`: default network transports
- `httpx.WSGITransport`: call a WSGI application directly
- `httpx.ASGITransport`: call an ASGI application directly
- `httpx.MockTransport`: return canned responses for tests

**Testing a WSGI app (e.g., Flask) without a server:**

```python
import httpx
from myapp import app

with httpx.Client(transport=httpx.WSGITransport(app=app), base_url="http://testserver") as client:
    r = client.get("/")
    assert r.status_code == 200
```

**Testing an ASGI app (e.g., FastAPI, Starlette):**

```python
import httpx
from myapp import app

async def test_root():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        r = await client.get("/")
        assert r.status_code == 200
```

**Mocking responses:**

```python
def handler(request):
    return httpx.Response(200, json={"mocked": True})

with httpx.Client(transport=httpx.MockTransport(handler)) as client:
    r = client.get("https://anything.example")
    assert r.json() == {"mocked": True}
```

### Exceptions

HTTPX exceptions form a hierarchy rooted at `httpx.HTTPError`:

- `RequestError`: network-level errors
  - `TransportError`: connection, timeout, and protocol errors
    - `TimeoutException` (`ConnectTimeout`, `ReadTimeout`, `WriteTimeout`, `PoolTimeout`)
    - `NetworkError` (`ConnectError`, `ReadError`, `WriteError`, `CloseError`)
    - `ProtocolError`, `ProxyError`, `UnsupportedProtocol`
  - `DecodingError`
  - `TooManyRedirects`
- `HTTPStatusError`: raised by `response.raise_for_status()`

```python
try:
    r = httpx.get("https://example.org", timeout=1.0)
    r.raise_for_status()
except httpx.TimeoutException:
    print("Request timed out")
except httpx.HTTPStatusError as exc:
    print(f"Bad status: {exc.response.status_code}")
except httpx.RequestError as exc:
    print(f"Request failed: {exc.request.url}")
```

### Command-Line Interface

If installed with the `cli` extra, the `httpx` command is available:

```bash
pip install "httpx[cli]"

httpx https://www.example.org
httpx https://httpbin.org/post -m POST -j '{"key": "value"}'
httpx https://www.example.org --headers "Accept" "application/json"
```

Run `httpx --help` for the full set of options.

### Environment Variables

When `trust_env=True` (the default), HTTPX reads standard environment variables:

| Variable | Purpose |
|----------|---------|
| `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY` | Proxy URLs |
| `NO_PROXY` | Hosts to exclude from proxying |
| `SSL_CERT_FILE` / `SSL_CERT_DIR` | CA certificate locations |
| `SSLKEYLOGFILE` | Write TLS keys for debugging (e.g., Wireshark) |

See `environment_variables.md` in the documentation for the complete reference.

---

## Project Structure

```
httpx-khdjoj31/
├── httpx/                      # Library source code
│   ├── __init__.py             # Public API exports
│   ├── __version__.py          # Version string
│   ├── _api.py                 # Top-level get/post/... functions
│   ├── _client.py              # Client and AsyncClient
│   ├── _models.py              # Request, Response, Headers, Cookies
│   ├── _auth.py                # Authentication classes
│   ├── _config.py              # Timeout, Limits, SSL configuration
│   ├── _content.py             # Request body encoding
│   ├── _multipart.py           # Multipart form encoding
│   ├── _decoders.py            # Content-Encoding decoders
│   ├── _exceptions.py          # Exception hierarchy
│   ├── _main.py                # Command-line interface
│   ├── _status_codes.py        # HTTP status code constants
│   ├── _types.py               # Type aliases
│   ├── _urls.py                # URL class
│   ├── _urlparse.py            # URL parsing (WHATWG-compliant)
│   ├── _utils.py               # Internal helpers
│   ├── py.typed                # PEP 561 type marker
│   ├── wsgi.py                 # WSGI transport
│   ├── asgi.py                 # ASGI transport
│   ├── mock.py                 # Mock transport
│   └── _transports/
│       ├── __init__.py
│       ├── base.py             # Base transport classes
│       ├── default.py          # Default HTTP transports
│       ├── asgi.py             # ASGI transport implementation
│       └── mock.py             # Mock transport implementation
├── tests/                      # Test suite
│   ├── conftest.py
│   ├── common.py
│   ├── concurrency.py
│   ├── test_api.py
│   ├── test_async_client.py
│   ├── test_auth.py
│   ├── test_client.py
│   ├── test_content.py
│   ├── test_decoders.py
│   ├── test_exceptions.py
│   ├── test_multipart.py
│   ├── test_proxies.py
│   ├── test_redirects.py
│   ├── test_timeouts.py
│   ├── test_url.py
│   ├── test_whatwg.py          # Tests against WHATWG URL test data
│   ├── whatwg.json
│   └── ...                     # Additional tests for each module
├── docs/                       # MkDocs documentation source
│   ├── index.md
│   ├── quickstart.md
│   ├── async.md
│   ├── clients.md
│   ├── authentication.md
│   ├── http2.md
│   ├── proxies.md
│   ├── timeouts.md
│   ├── ssl.md
│   ├── transports.md
│   ├── event-hooks.md
│   ├── exceptions.md
│   ├── troubleshooting.md
│   ├── compatibility.md
│   ├── third_party_packages.md
│   ├── environment_variables.md
│   ├── resource-limits.md
│   ├── text-encodings.md
│   ├── logging.md
│   ├── extensions.md
│   ├── api.md
│   ├── contributing.md
│   ├── code_of_conduct.md
│   ├── custom.css
│   ├── nav.html
│   ├── CNAME
│   └── img/                    # Images and demo GIFs
├── scripts/                    # Development scripts
│   ├── check
│   ├── clean
│   ├── build
│   ├── publish
│   ├── test
│   ├── lint
│   ├── coverage
│   ├── docs
│   ├── install
│   └── sync-version
├── requirements.txt            # Development dependencies
├── pyproject.toml              # Project metadata and build configuration
├── mkdocs.yml                  # Documentation site configuration
├── CHANGELOG.md                # Release history
├── LICENSE.md                  # BSD 3-Clause license
└── README.md
```

> Note: The directory layout above is inferred from the file listing. Some files may be located slightly differently in your checkout.

---

## Development

### Setting Up a Development Environment

Clone the repository and run the install script, which sets up a virtual environment and installs development dependencies:

```bash
git clone <repository-url> httpx-khdjoj31
cd httpx-khdjoj31
scripts/install
```

Or manually:

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### Running Tests

```bash
scripts/test
```

Or with pytest directly:

```bash
pytest tests/
pytest tests/test_client.py::test_name -v   # single test
```

Async tests are run with the configured async backend; `conftest.py` provides shared fixtures.

### Linting and Type Checking

```bash
scripts/lint
scripts/check
```

`lint` runs code formatting and style checks. `check` runs static type checking and related verification.

### Coverage

```bash
scripts/coverage
```

Generates a coverage report for the `httpx` package.

### Building and Publishing

```bash
scripts/clean      # remove build artifacts
scripts/build      # build sdist and wheel
scripts/publish    # upload to PyPI (requires credentials)
```

Version management is handled by:

```bash
scripts/sync-version
```

This keeps the version string in `httpx/__version__.py` consistent with `pyproject.toml`.

### Documentation

Documentation is built with [MkDocs](https://www.mkdocs.org/) using the configuration in `mkdocs.yml`.

```bash
scripts/docs       # build and/or serve the docs locally
mkdocs serve       # live-reloading local preview
mkdocs build       # static build to site/
```

---

## Contributing

Contributions are welcome. Before opening a pull request:

1. Read [`docs/contributing.md`](docs/contributing.md) and [`docs/code_of_conduct.md`](docs/code_of_conduct.md).
2. Fork the repository and create a feature branch.
3. Add or update tests for any behavior change.
4. Run `scripts/lint`, `scripts/check`, and `scripts/test` locally.
5. Update documentation and `CHANGELOG.md` where relevant.
6. Open a pull request with a clear description of the change.

Bug reports and feature requests should be filed as issues with a minimal reproducible example, the Python version, and the HTTPX version (`httpx.__version__`).

---

## Changelog

Release notes are maintained in [`CHANGELOG.md`](CHANGELOG.md).

---

## License

HTTPX is released under the **BSD 3-Clause License**. See [`LICENSE.md`](LICENSE.md) for the full text.

---

## Acknowledgements

HTTPX builds on ideas from [Requests](https://github.com/psf/requests) and is designed to interoperate with the wider Python async ecosystem, including `asyncio`, `trio`, ASGI, and WSGI.

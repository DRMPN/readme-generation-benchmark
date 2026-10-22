# HTTPX

[![Test Suite](https://github.com/encode/httpx/workflows/Test%20Suite/badge.svg)](https://github.com/encode/httpx/actions)
[![Package version](https://badge.fury.io/py/httpx.svg)](https://pypi.org/project/httpx/)

HTTPX is a fully featured HTTP client for Python 3. It provides both synchronous and asynchronous APIs and supports HTTP/1.1 and HTTP/2. The package is described as "The next generation HTTP client" and is documented at [python-httpx.org](https://www.python-httpx.org).

## Overview

HTTPX builds on the usability of `requests` and offers:

* A broadly `requests`-compatible API (see the Requests Compatibility Guide in the docs).
* A standard synchronous interface, with async support when you need it.
* HTTP/1.1 and HTTP/2 support (HTTP/2 is optional).
* The ability to send requests directly to WSGI and ASGI applications.
* Timeouts enabled by default for network operations.
* Type annotations (the package ships a `py.typed` marker).
* Connection pooling, cookie persistence through `Client` instances, automatic decompression and content decoding, multipart file uploads, HTTP(S) and SOCKS proxy support, streaming downloads, `.netrc` support, and chunked requests.

HTTPX uses [HTTPCore](https://github.com/encode/httpcore) as its networking layer, and it depends on `certifi`, `httpcore`, `anyio`, and `idna`.

The project is released under the BSD-3-Clause license and currently has version `0.28.1`, as defined in `httpx/__version__.py`. It supports Python 3.9 and later. The changelog lists support for Python 3.8 as removed in the unreleased section.

## Installation

Install the latest release from PyPI:

```shell
$ pip install httpx
```

Optional features are available as extras:

| Extra | Purpose |
| --- | --- |
| `httpx[http2]` | HTTP/2 support (installs `h2`) |
| `httpx[socks]` | SOCKS proxy support (installs `socksio`) |
| `httpx[brotli]` | Decoding of `brotli` responses |
| `httpx[zstd]` | Decoding of `zstd` responses (installs `zstandard`) |
| `httpx[cli]` | The command-line client (installs `click`, `pygments`, and `rich`) |

Extras can be combined:

```shell
$ pip install 'httpx[brotli,zstd]'
```

## Usage

### Top-level functions

The top-level API sends one request per call, without connection reuse:

```pycon
>>> import httpx
>>> r = httpx.get('https://www.example.org/')
>>> r
<Response [200 OK]>
>>> r.status_code
200
>>> r.headers['content-type']
'text/html; charset=UTF-8'
```

The module also provides `post`, `put`, `patch`, `delete`, `head`, `options`, `request`, and `stream`.

Query parameters, headers, cookies, and form data are passed as keyword arguments:

```python
r = httpx.get("https://httpbin.org/get", params={"key1": "value1"}, headers={"user-agent": "my-app/0.0.1"})
r = httpx.post("https://httpbin.org/post", data={"key": "value"})
r = httpx.post("https://httpbin.org/post", json={"integer": 123, "list": ["a", "b"]})
r = httpx.post("https://httpbin.org/post", content=b"Hello, world")
```

Files are uploaded in binary mode:

```python
with open("report.xls", "rb") as report_file:
    files = {"upload-file": report_file}
    r = httpx.post("https://httpbin.org/post", files=files)
```

### Clients

For more than a handful of requests, use a `Client`. It provides connection pooling, cookie persistence, and shared configuration:

```python
with httpx.Client(headers={"user-agent": "my-app/0.0.1"}) as client:
    r = client.get("https://example.com")
    print(r.request.headers["User-Agent"])
```

### Async

Use `AsyncClient` with `async`/`await`:

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.example.com/")
        print(response)

asyncio.run(main())
```

The async docs show examples for asyncio, Trio (which requires the `trio` package to be installed), and AnyIO.

### Responses

Responses expose `.text`, `.content`, `.json()`, `.headers`, `.cookies`, and `.history`. Streaming is available via `httpx.stream()` and `client.stream()`:

```python
with httpx.stream("GET", "https://www.example.com") as r:
    for chunk in r.iter_bytes():
        print(chunk)
```

Use `response.raise_for_status()` to raise `httpx.HTTPStatusError` for non-2xx responses. The base class `httpx.HTTPError` covers both request errors and status errors.

### Command-line client

When installed with the `cli` extra, the `httpx` command is available:

```shell
$ pip install 'httpx[cli]'
$ httpx --help
```

## Configuration

### Redirects

HTTPX does **not** follow redirects by default. Enable them per request or per client:

```python
response = client.get(url, follow_redirects=True)
client = httpx.Client(follow_redirects=True)
```

### Timeouts

The default timeout is five seconds. You can override it per request, per client, or with fine-grained settings:

```python
httpx.get("https://example.com/", timeout=10.0)
httpx.get("https://example.com/", timeout=None)  # Disable timeouts.

timeout = httpx.Timeout(10.0, connect=60.0)
client = httpx.Client(timeout=timeout)
```

The four timeout types are `connect`, `read`, `write`, and `pool`.

### Connection limits

Pool sizes are controlled with `httpx.Limits`. The documented defaults are 20 keep-alive connections, 100 maximum connections, and a 5-second keep-alive expiry:

```python
limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
client = httpx.Client(limits=limits)
```

### Proxies

Pass a `proxy` to a client or top-level function. Use `mounts` for routing by scheme, domain, or port:

```python
with httpx.Client(proxy="http://localhost:8030") as client:
    ...

proxy_mounts = {
    "http://": httpx.HTTPTransport(proxy="http://localhost:8030"),
    "https://": httpx.HTTPTransport(proxy="http://localhost:8031"),
}
with httpx.Client(mounts=proxy_mounts) as client:
    ...
```

The docs note that the proxy URL for the `https://` key usually uses the `http://` scheme. Proxy credentials can be placed in the URL's userinfo section.

### Transports

Low-level behaviour is configured through transports, such as `httpx.HTTPTransport(retries=1)`, `httpx.HTTPTransport(local_address=...)`, and `httpx.HTTPTransport(uds=...)`. `httpx.WSGITransport` and `httpx.ASGITransport` route requests into Python web applications. `httpx.MockTransport` supports mocked responses in tests.

### SSL

Verification is enabled by default and uses the certifi CA bundle. You can pass `verify=False`, an `ssl.SSLContext`, or configure client certificates with `ctx.load_cert_chain()`.

### Environment variables

Unless `trust_env=False` is set, HTTPX reads these variables:

* `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`: proxy URLs for HTTP, HTTPS, or all requests.
* `NO_PROXY`: a comma-separated list of hosts or URLs that bypass the proxy.

The `NETRC` variable can be used with `httpx.NetRCAuth(file=os.environ.get("NETRC"))`.

### Logging

HTTPX uses Python's standard `logging`. The `httpx` logger emits request lines at INFO level, and the `httpcore` logger emits network-level DEBUG output. The two loggers can be configured separately. The exact debug format may change between versions.

### Authentication

Pass a `(username, password)` tuple, `httpx.BasicAuth`, `httpx.DigestAuth`, or `httpx.NetRCAuth` as `auth`. Custom schemes can subclass `httpx.Auth` and implement `auth_flow()`, or override `sync_auth_flow()` and `async_auth_flow()`.

### HTTP/2

HTTP/2 is disabled by default. Install the `http2` extra and enable it:

```python
client = httpx.AsyncClient(http2=True)
```

Check `response.http_version` to see which protocol was used.

## Development

Clone your fork and install the project in editable mode with the provided scripts:

```shell
$ git clone https://github.com/YOUR-USERNAME/httpx
$ cd httpx
$ scripts/install
```

The `scripts/` directory contains:

* `scripts/install`: installs the project and its dependencies.
* `scripts/test`: runs the test suite. Extra arguments are passed to `pytest`.
* `scripts/lint`: runs code auto-formatting.
* `scripts/check`: runs code checks (also run by `scripts/test`).
* `scripts/docs`: serves the documentation locally.
* `scripts/build`, `scripts/clean`, `scripts/coverage`, `scripts/publish`, and `scripts/sync-version`.

Linting and type checking are configured in `pyproject.toml`. Ruff selects the `E`, `F`, `I`, `B`, and `PIE` rule sets. Mypy runs in strict mode, with relaxed checks for the `tests.*` modules.

Dependencies for tooling are pinned in `requirements.txt`. Runtime dependencies are intentionally left unpinned, so tests must pass against current package versions.

### Code layout

* `httpx/`: the package source, including `_client.py`, `_models.py`, `_auth.py`, `_config.py`, and the `_transports/` package.
* `tests/`: the test suite, organised into `client/` and `models/` subpackages.
* `docs/`: the MkDocs documentation, configured by `mkdocs.yml`.
* `CHANGELOG.md`: the release history, following Keep a Changelog.

## Testing

Run the full suite with:

```shell
$ scripts/test
```

The test suite starts local servers on ports **8000** and **8001**, so those ports must be free. Run a single file with:

```shell
$ scripts/test tests/test_multipart.py
```

Pytest is configured in `pyproject.toml`. Warnings are treated as errors. Two custom markers are defined:

* `network`: marks tests that need a network connection, for build environments where networking is disabled.
* `copied_from`: marks tests copied from elsewhere, with a description of changes.

Coverage is configured for `httpx/*` and `tests/*`. The contributing guide states that the required coverage threshold is 100%.

Continuous integration is defined in `.github/workflows/test-suite.yml`. The contributing guide describes separate check, docs, and Python test jobs.

### Debugging with a proxy

The contributing guide describes using [mitmproxy](https://mitmproxy.org/) with certificates generated by `trustme-cli` to inspect HTTPX traffic during development.

## Documentation

The documentation source lives in `docs/` and is built with MkDocs and the Material theme. Build and preview it locally with `scripts/docs`. The site is published at [https://www.python-httpx.org](https://www.python-httpx.org).

## Releasing

Releases are prepared by maintainers. A release pull request updates `CHANGELOG.md` and the version in `httpx/__version__.py`. After the pull request is merged, a GitHub release is created with a tag such as `0.13.3`. According to the contributing guide, the release is then uploaded to PyPI automatically. If that job fails, `scripts/publish` can be used.

## Contributing

Contributions are welcome, including bug reports, features, reviews, and documentation. The contributing guide asks that contributions start as a discussion at [github.com/encode/httpx/discussions](https://github.com/encode/httpx/discussions). Bug reports should include the OS, Python version, installed dependencies, a minimal code snippet, and the traceback.

Pull requests use a template that asks for a summary, tests for each change, and documentation updates. The project follows the [Python Software Foundation Code of Conduct](https://www.python.org/psf/conduct/).

## License

HTTPX is licensed under the BSD-3-Clause license. The copyright is held by Encode OSS Ltd. See [LICENSE.md](LICENSE.md) for the full text.

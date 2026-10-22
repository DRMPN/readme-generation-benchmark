# HTTPX

<p align="center">
  <img width="350" height="208" src="https://raw.githubusercontent.com/encode/httpx/master/docs/img/butterfly.png" alt="HTTPX">
</p>

<div align="center">
<p>
<a href="https://github.com/encode/httpx/actions">
    <img src="https://github.com/encode/httpx/workflows/Test%20Suite/badge.svg" alt="Test Suite">
</a>
<a href="https://pypi.org/project/httpx/">
    <img src="https://badge.fury.io/py/httpx.svg" alt="Package version">
</a>
</p>

<em>A next-generation HTTP client for Python.</em>
</div>

---

HTTPX is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.

- **Requires:** Python 3.9+
- **License:** BSD-3-Clause
- **Documentation:** <https://www.python-httpx.org>
- **Source:** <https://github.com/encode/httpx>

## Features

HTTPX builds on the well-established usability of `requests`, and gives you:

* A broadly [requests-compatible API](https://www.python-httpx.org/compatibility/).
* Standard synchronous interface, but with async support if you need it.
* HTTP/1.1 and HTTP/2 support.
* Ability to make requests directly to WSGI applications or ASGI applications.
* Strict timeouts everywhere.
* Fully type annotated.
* 100% test coverage.

Plus all the standard features of `requests`...

* International Domains and URLs
* Keep-Alive & Connection Pooling
* Sessions with Cookie Persistence
* Browser-style SSL Verification
* Basic/Digest Authentication
* Elegant Key/Value Cookies
* Automatic Decompression
* Automatic Content Decoding
* Unicode Response Bodies
* Multipart File Uploads
* HTTP(S) Proxy Support
* Connection Timeouts
* Streaming Downloads
* .netrc Support
* Chunked Requests

## Installation

Install with pip:

```shell
$ pip install httpx
```

Or, to include one of the optional extras:

```shell
$ pip install httpx[http2]      # HTTP/2 support (h2)
$ pip install httpx[cli]        # Command line client (click, pygments, rich)
$ pip install httpx[socks]      # SOCKS proxy support (socksio)
$ pip install httpx[brotli]     # Brotli decoding (brotli / brotlicffi)
$ pip install httpx[zstd]       # Zstd decoding (zstandard)
```

Multiple extras may be combined, e.g. `pip install httpx[brotli,zstd]`.

## Quickstart

Import HTTPX and start making requests:

```pycon
>>> import httpx
>>> r = httpx.get('https://www.example.org/')
>>> r
<Response [200 OK]>
>>> r.status_code
200
>>> r.headers['content-type']
'text/html; charset=UTF-8'
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

All the standard HTTP methods are available on the top-level API: `httpx.get()`, `httpx.post()`, `httpx.put()`, `httpx.patch()`, `httpx.delete()`, `httpx.head()`, `httpx.options()`, and the generic `httpx.request()`. Request bodies can be sent as form data (`data=...`), multipart file uploads (`files=...`), JSON (`json=...`), or raw binary content (`content=...`).

### Using a Client

If you do anything more than experimentation, one-off scripts, or prototypes, you should use a `Client` instance. Clients use HTTP connection pooling, provide cookie persistence across requests, allow configuration to be shared across outgoing requests, and unlock features such as HTTP/2 and proxying.

The recommended way to use a `Client` is as a context manager, ensuring connections are properly cleaned up:

```python
with httpx.Client() as client:
    r = client.get('https://example.com')
```

Client-level configuration—such as headers, query parameters, cookies, authentication, and timeouts—is merged into each outgoing request.

### Async Support

HTTPX offers a standard synchronous API by default, but also provides an async client:

```python
async with httpx.AsyncClient() as client:
    r = await client.get('https://www.example.com/')
```

Both `asyncio` and `trio` are supported as async environments, and are auto-detected. Streaming responses use `aiter_bytes()`, `aiter_text()`, `aiter_lines()`, and `aiter_raw()` inside an async context block.

### Streaming Responses

For large downloads, stream the response body instead of loading it into memory at once:

```python
with httpx.stream("GET", "https://www.example.com") as r:
    for line in r.iter_lines():
        print(line)
```

### Command Line Client

The command line client is an optional dependency:

```shell
$ pip install 'httpx[cli]'
$ httpx http://httpbin.org/json
```

The CLI displays connection and server certificate information with `-v/--verbose`.

## Configuration

### Timeouts

HTTPX defaults to a five-second timeout for all network operations, so that a request should always raise an error rather than hanging indefinitely:

```python
httpx.get('https://github.com/', timeout=0.001)  # Stricter timeout
httpx.get('https://github.com/', timeout=None)   # Disable timeouts
```

Fine-grained configuration is available with `httpx.Timeout(10.0, connect=60.0)`, covering **connect**, **read**, **write**, and **pool** timeouts.

### Proxies

Route traffic through an HTTP proxy with the `proxy` argument:

```python
with httpx.Client(proxy="http://localhost:8030") as client:
    ...
```

For more advanced routing, use the `mounts` argument to map URL patterns—by scheme, domain, port, or wildcards—onto different transports. SOCKS proxy support (`socks5://...`) is available with the `httpx[socks]` extra.

### Authentication

Basic and Digest authentication are supported out of the box:

```python
httpx.get("https://example.com", auth=("my_user", "password123"))

auth = httpx.DigestAuth("my_user", "password123")
httpx.get("https://example.com", auth=auth)
```

`.netrc` files can be used via `httpx.NetRCAuth()`, and custom authentication schemes can be implemented by subclassing `httpx.Auth` and providing an `auth_flow()` method.

### Environment Variables

HTTPX can be configured via the `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and `NO_PROXY` environment variables. Environment variables are used by default; set `trust_env=False` on a client or top-level request to ignore them.

### SSL

By default HTTPS connections are verified using the `certifi` CA bundle. Verification can be disabled with `verify=False`, or a custom `ssl.SSLContext` can be passed with `verify=<ssl_context>` for more complex cases, such as client-side certificates or alternative certificate stores.

## Documentation

A run-through of all the basics is available in the [QuickStart](https://www.python-httpx.org/). For more advanced topics see the **Advanced** section (clients, authentication, SSL, proxies, timeouts, resource limits, event hooks, transports, text encodings, and extensions), the [async support](https://www.python-httpx.org/async/) guide, or the [HTTP/2](https://www.python-httpx.org/http2/) guide. The [Developer Interface](https://www.python-httpx.org/api/) provides a comprehensive API reference, and a [Requests compatibility guide](https://www.python-httpx.org/compatibility/) outlines the differences from `requests`.

If you need to mock HTTPX in tests, see the third-party packages [RESPX](https://lundberg.github.io/respx/) and [pytest-httpx](https://colin-b.github.io/pytest_httpx/). For HTTP caching, see [Hishel](https://hishel.com/).

## Dependencies

HTTPX relies on these core libraries:

* `httpcore` – The underlying transport implementation for `httpx`.
* `certifi` – SSL certificates.
* `idna` – Internationalized domain name support.
* `anyio` – Async library autodetection across `asyncio` and `trio`.

Optional installs:

* `h2` – HTTP/2 support. *(Optional, with `httpx[http2]`)*
* `socksio` – SOCKS proxy support. *(Optional, with `httpx[socks]`)*
* `rich`, `click`, `pygments` – Command line client. *(Optional, with `httpx[cli]`)*
* `brotli` / `brotlicffi` – Brotli decoding. *(Optional, with `httpx[brotli]`)*
* `zstandard` – Zstd decoding. *(Optional, with `httpx[zstd]`)*

A huge amount of credit is due to `requests` for the API layout that much of this work follows, as well as to `urllib3` for plenty of design inspiration around the lower-level networking details.

## Development

To start developing HTTPX, create a **fork** of the [HTTPX repository](https://github.com/encode/httpx) on GitHub, then clone your fork:

```shell
$ git clone https://github.com/YOUR-USERNAME/httpx
$ cd httpx
$ scripts/install
```

The project uses custom shell scripts to automate the testing, linting, and documentation workflow. Pinned tooling versions are listed in `requirements.txt` and include `pytest`, `ruff`, `mypy` (run in strict mode), `coverage`, `mkdocs`, and `trio`.

### Testing

Run the full test suite with:

```shell
$ scripts/test
```

> **Warning**
> The test suite spawns testing servers on ports **8000** and **8001**. Make sure these are not in use, so the tests can run properly.

Additional arguments are passed to `pytest`, so a single test module can be run like this:

```shell
$ scripts/test tests/test_multipart.py
```

The project maintains a **100% test coverage** requirement, so tests fail if any code paths are untested. Coverage is measured over both the `httpx/` and `tests/` packages, and can be inspected using the `scripts/coverage` script.

### Linting and Checks

Code auto-formatting is run with:

```shell
$ scripts/lint
```

The code checks (formatting and type annotations, also run as part of `scripts/test`) can be run separately with:

```shell
$ scripts/check
```

### Documentation

Documentation pages are located under the `docs/` folder and built with MkDocs. To run the documentation site locally (useful for previewing changes), use:

```shell
$ scripts/docs
```

### Continuous Integration

Once a pull request is submitted, the test suite runs automatically on GitHub Actions. Common failures include the *check* job (formatting or type-annotation issues—run `scripts/check`, and try `scripts/lint` to auto-format), the *docs* job (invalid markdown or missing configuration in `mkdocs.yml`), and the *Python 3.X* test jobs (failing tests or coverage below 100%).

## Contributing

There are many ways you can contribute to the project:

* Try HTTPX and [report bugs/issues you find](https://github.com/encode/httpx/issues/new)
* [Implement new features](https://github.com/encode/httpx/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
* [Review Pull Requests of others](https://github.com/encode/httpx/pulls)
* Write documentation
* Participate in discussions

Contributions should generally start out with [a discussion](https://github.com/encode/httpx/discussions)—possible bugs may be raised as a "Potential Issue" discussion, and feature requests as an "Ideas" discussion—so that the issues list properly reflects ongoing work. When reporting a bug, please include your OS platform, Python version, installed dependency versions (`python -m pip freeze`), a code snippet, and an error traceback, reduced to the simplest possible case that demonstrates the issue.

Pull requests should include a test for each change, aim to be a single atomic change, and update the documentation accordingly. See the [contribution guidelines](.github/CONTRIBUTING.md) for full details, including notes on local proxy debugging with `mitmproxy`.

## Releasing

*This section is targeted at HTTPX maintainers.*

Before releasing a new version, create a pull request that includes an update to the [changelog](CHANGELOG.md)—which follows the format from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)—and a version bump in `httpx/__version__.py`. Once the release PR is merged, create a [new GitHub release](https://github.com/encode/httpx/releases/new) with a tag version, title, and description copied from the changelog. The release is then automatically uploaded to PyPI; if the PyPI job fails, it can be published using the `scripts/publish` script.

## Code of Conduct

We expect contributors to our projects and online spaces to follow [the Python Software Foundation's Code of Conduct](https://www.python.org/psf/conduct/). Reports may be raised privately by email, or [made to the Python Software Foundation](https://www.python.org/psf/conduct/reporting/), and will be treated confidentially.

## License

Copyright © 2019, [Encode OSS Ltd](https://www.encode.io/). All rights reserved.

Licensed under the [BSD-3-Clause License](LICENSE.md). Redistribution and use in source and binary forms, with or without modification, are permitted provided that the copyright notice, disclaimer, and conditions in the license file are met. This software is provided "AS IS", without warranty of any kind.

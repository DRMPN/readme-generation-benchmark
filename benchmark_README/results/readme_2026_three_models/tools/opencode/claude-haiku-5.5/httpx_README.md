# HTTPX

A next-generation HTTP client for Python.

HTTPX is a fully featured HTTP client for Python 3. It provides both sync and async APIs and supports HTTP/1.1 and HTTP/2. Its API is modeled on `requests`, so most `requests` code translates directly.

## Features

- A broadly `requests`-compatible API.
- A standard synchronous interface, plus async support via `AsyncClient` (works with `asyncio` and `trio`).
- HTTP/1.1 and HTTP/2 support (HTTP/2 is opt-in; see below).
- Direct requests to WSGI and ASGI applications through `WSGITransport` and `ASGITransport`.
- Timeouts on all operations, with the default set to 5 seconds.
- Type annotations throughout the package (ships with a `py.typed` marker).
- Other `requests`-style features, including connection pooling, cookie persistence in sessions, Basic and Digest authentication, `.netrc` support, proxy support (HTTP, SOCKS), multipart file uploads, streaming downloads, chunked request bodies, and automatic decompression.

## Requirements

- Python 3.9 or newer.

## Installation

Install from PyPI:

```shell
pip install httpx
```

Optional extras add functionality:

| Extra | Installs | Purpose |
| --- | --- | --- |
| `http2` | `h2` | HTTP/2 support |
| `socks` | `socksio` | SOCKS proxy support |
| `brotli` | `brotli` (CPython) or `brotlicffi` (other) | Decoding `br` responses |
| `zstd` | `zstandard` | Decoding `zstd` responses |
| `cli` | `click`, `pygments`, `rich` | The `httpx` command-line client |

Install several at once with a comma-separated list, for example:

```shell
pip install "httpx[http2,brotli,zstd]"
```

## Quick start

```pycon
>>> import httpx
>>> r = httpx.get("https://www.example.org/")
>>> r
<Response [200 OK]>
>>> r.status_code
200
>>> r.headers["content-type"]
'text/html; charset=UTF-8'
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

Other top-level helpers follow the same style: `httpx.post()`, `httpx.put()`, `httpx.patch()`, `httpx.delete()`, `httpx.head()`, `httpx.options()`, and `httpx.request()`.

```pycon
>>> r = httpx.post("https://httpbin.org/post", data={"key": "value"})
>>> params = {"key1": "value1", "key2": ["value2", "value3"]}
>>> r = httpx.get("https://httpbin.org/get", params=params)
>>> r.url
URL('https://httpbin.org/get?key1=value1&key2=value2&key2=value3')
```

### Clients

For multiple requests, use a `Client`, which provides connection pooling and shared configuration:

```python
import httpx

with httpx.Client() as client:
    r = client.get("https://httpbin.org/get")
    print(r.status_code)
```

### Async

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://httpbin.org/get")
        print(r.status_code)

asyncio.run(main())
```

### JSON

```pycon
>>> r = httpx.get("https://api.github.com/events")
>>> r.json()
```

## Command-line client

With the `cli` extra installed, the `httpx` command sends requests from the terminal:

```shell
pip install "httpx[cli]"
httpx --help
httpx http://httpbin.org/json
```

The CLI accepts options including `--method`/`-m`, `--params`/`-p`, `--content`/`-c`, `--data`/`-d`, `--files`/`-f`, `--json`/`-j`, `--headers`/`-h`, `--cookies`, `--auth`, `--proxy`, `--timeout`, `--follow-redirects`, `--no-verify`, `--download`, and `--verbose`/`-v`. Run `httpx --help` for the full list and usage.

## HTTP/2

HTTP/2 is not enabled by default. To use it, install the `http2` extra and create a client with `http2=True`:

```shell
pip install "httpx[http2]"
```

```python
import httpx

with httpx.Client(http2=True) as client:
    r = client.get("https://www.example.org/")
    print(r.http_version)
```

See the [HTTP/2 guide](docs/http2.md) for details.

## Documentation

Full documentation is available at [python-httpx.org](https://www.python-httpx.org). The source is in the [`docs/`](docs/) directory:

- [QuickStart](docs/quickstart.md)
- [Async support](docs/async.md)
- [HTTP/2](docs/http2.md)
- Advanced topics: [clients](docs/advanced/clients.md), [authentication](docs/advanced/authentication.md), [SSL](docs/advanced/ssl.md), [proxies](docs/advanced/proxies.md), [timeouts](docs/advanced/timeouts.md), [resource limits](docs/advanced/resource-limits.md), [event hooks](docs/advanced/event-hooks.md), [transports](docs/advanced/transports.md), [text encodings](docs/advanced/text-encodings.md), and [extensions](docs/advanced/extensions.md)
- [Requests compatibility](docs/compatibility.md)
- [Logging](docs/logging.md) and [troubleshooting](docs/troubleshooting.md)
- [Developer interface (API reference)](docs/api.md) and [exceptions](docs/exceptions.md)
- [Environment variables](docs/environment_variables.md)
- [Third-party packages](docs/third_party_packages.md)

## Development

Clone the repository and install the development dependencies:

```shell
git clone https://github.com/encode/httpx
cd httpx
scripts/install
```

`scripts/install` creates a `venv/` directory and installs `requirements.txt`, which includes the package with all extras.

The project uses these scripts in `scripts/`:

| Script | Purpose |
| --- | --- |
| `scripts/install` | Create the virtual environment and install dependencies |
| `scripts/test` | Run the test suite with `pytest` under `coverage` (runs `scripts/check` first unless in GitHub Actions) |
| `scripts/check` | Run `ruff format --diff`, `mypy`, and `ruff check` on `httpx` and `tests` |
| `scripts/lint` | Auto-format code |
| `scripts/coverage` | Require 100% test coverage |
| `scripts/docs` | Serve the documentation locally with `mkdocs serve` |
| `scripts/build` | Build the package and documentation |
| `scripts/publish` | Publish a release |

For example, to run a single test file:

```shell
scripts/test tests/test_multipart.py
```

The test suite starts local test servers on ports **8000** and **8001**, so these ports must be free. Tests marked `network` require a network connection.

Before opening a pull request, read [CONTRIBUTING.md](.github/CONTRIBUTING.md) and the [contributing guide](docs/contributing.md).

## Contributing

Contributions are welcome. Bug reports, feature requests, and questions should generally begin as a [discussion](https://github.com/encode/httpx/discussions). Please also read the [Code of Conduct](docs/code_of_conduct.md).

## Changelog

Release history is in [CHANGELOG.md](CHANGELOG.md).

## License

HTTPX is licensed under the BSD 3-Clause License. See [LICENSE.md](LICENSE.md).

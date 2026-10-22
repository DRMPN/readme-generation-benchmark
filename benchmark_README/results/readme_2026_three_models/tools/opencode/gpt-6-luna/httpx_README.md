# HTTPX

HTTPX is a Python HTTP client with synchronous and asynchronous APIs. It supports HTTP/1.1 and optional HTTP/2, and provides a broadly Requests-compatible API.

## Installation

HTTPX requires Python 3.9 or later. Install the base package with pip:

```shell
python -m pip install httpx
```

Optional dependencies enable additional features:

```shell
python -m pip install 'httpx[http2]'       # HTTP/2 support
python -m pip install 'httpx[socks]'       # SOCKS proxies
python -m pip install 'httpx[cli]'         # `httpx` command-line client
python -m pip install 'httpx[brotli,zstd]' # Brotli and Zstandard decoding
```

These extras can be combined, for example `httpx[cli,http2]`.

## Quick start

Make a one-off synchronous request with the top-level API:

```python
import httpx

response = httpx.get("https://www.example.org/")
print(response.status_code)
print(response.text)
```

For multiple requests, use a client so connections can be pooled and configuration or cookies can be shared. Use it as a context manager to close its resources:

```python
with httpx.Client() as client:
    response = client.get("https://www.example.org/")
    print(response.status_code)
```

HTTPX also provides an async API through `AsyncClient`:

```python
import asyncio
import httpx


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.example.org/")
        print(response.status_code)


asyncio.run(main())
```

The async API supports asyncio and Trio; install Trio separately if you use the Trio backend.

## Features

- Synchronous and asynchronous requests, including streaming request and response bodies.
- HTTP/1.1, with HTTP/2 available by installing `httpx[http2]` and enabling it on a client with `http2=True`.
- Query parameters, headers, cookies, JSON and form bodies, and multipart file uploads.
- Connection pooling, configurable timeouts, authentication, TLS verification, and HTTP proxies.
- Transports for calling WSGI and ASGI applications directly, as well as custom and mock transports.
- Typed public APIs and automatic response content decoding. Brotli and Zstandard decoding require their optional extras.

Redirects are not followed by default. Set `follow_redirects=True` on a request or client to enable them. Network operations use timeouts by default; pass `timeout=None` to disable them.

## Command-line client

Install the CLI extra, then pass a URL to the `httpx` command:

```shell
python -m pip install 'httpx[cli]'
httpx https://www.example.org/
```

Use `httpx --help` to see supported options, including request methods, headers, request bodies, proxies, redirects, HTTP/2, verbose output, and downloading a response to a file.

## Documentation

- [QuickStart](https://www.python-httpx.org/quickstart/)
- [Async support](https://www.python-httpx.org/async/)
- [HTTP/2](https://www.python-httpx.org/http2/)
- [Advanced usage](https://www.python-httpx.org/advanced/clients/)
- [API reference](https://www.python-httpx.org/api/)
- [Requests compatibility guide](https://www.python-httpx.org/compatibility/)
- [Full documentation](https://www.python-httpx.org/)

## Contributing

Development and testing instructions are in the [contributing guide](docs/contributing.md). To run the test suite from a development checkout, use:

```shell
scripts/install
scripts/test
```

## License

HTTPX is distributed under the [BSD 3-Clause License](LICENSE.md).

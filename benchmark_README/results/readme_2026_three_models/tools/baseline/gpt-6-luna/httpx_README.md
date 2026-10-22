# HTTPX

HTTPX is a fully featured HTTP client for Python 3, with synchronous and asynchronous APIs and support for HTTP/1.1 and optional HTTP/2. It provides a broadly `requests`-compatible interface, connection pooling through client instances, and a typed API.

- **Documentation:** [python-httpx.org](https://www.python-httpx.org)
- **Source and issues:** [github.com/encode/httpx](https://github.com/encode/httpx)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

## Features

HTTPX includes:

- Sync and async clients, with async support for `asyncio` and Trio.
- HTTP/1.1, plus optional HTTP/2.
- Connection pooling and persistent client cookies.
- Request and response streaming, multipart uploads, and automatic content decoding.
- SSL verification, authentication, timeouts, connection limits, and proxy support.
- WSGI and ASGI transports for calling Python applications directly.
- Custom and mock transports, event hooks, and structured logging.
- Type annotations and a `py.typed` marker.

## Requirements and installation

HTTPX requires **Python 3.9 or later**. Install the core package with pip:

```shell
python -m pip install httpx
```

Optional features are installed separately:

```shell
python -m pip install "httpx[http2]"          # HTTP/2
python -m pip install "httpx[cli]"            # Command-line client
python -m pip install "httpx[socks]"          # SOCKS proxies
python -m pip install "httpx[brotli,zstd]"    # Brotli and zstd decoding
```

The available extras are `http2`, `cli`, `socks`, `brotli`, and `zstd`. The `cli` extra provides the `httpx` command; the other extras add their respective protocol or decoding dependencies.

## Quick start

The top-level functions are useful for experiments and one-off requests:

```python
import httpx

response = httpx.get("https://www.example.org/")
print(response.status_code)
print(response.headers["content-type"])
print(response.text)
```

Send form data, JSON, or raw content with the corresponding argument:

```python
httpx.post("https://httpbin.org/post", data={"key": "value"})
httpx.post("https://httpbin.org/post", json={"enabled": True})
httpx.post("https://httpbin.org/post", content=b"raw bytes")
```

Use `params` for query parameters and `files` for multipart file uploads. Open files in binary mode when uploading them.

For repeated requests, prefer a client instance. It reuses connections and can share configuration across requests:

```python
with httpx.Client(base_url="https://httpbin.org") as client:
    response = client.get("/get", params={"page": 1})
    response.raise_for_status()
    print(response.json())
```

A client should generally be used as a context manager so that its connections are closed when the block exits. You can also call `client.close()` explicitly.

## Asynchronous requests

Use `AsyncClient` in async applications. Requests and response streaming methods must be awaited or iterated asynchronously:

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.example.org/")
        print(response.status_code)

asyncio.run(main())
```

HTTPX supports `asyncio` and Trio as async environments. Trio must be installed to use its backend. Reuse a scoped client where possible rather than creating clients repeatedly in a hot loop.

## Streaming

For large responses, stream the body instead of loading it all into memory:

```python
with httpx.stream("GET", "https://www.example.org/large-file") as response:
    for chunk in response.iter_bytes():
        process(chunk)
```

The stream context closes the response on exit. Streaming clients also provide `iter_text()`, `iter_lines()`, and `iter_raw()`. For async requests, use `AsyncClient.stream()` with `async with` and iterate using methods such as `aiter_bytes()`.

## Configuration

HTTPX can be configured per request or on a client. Common options include headers, query parameters, cookies, authentication, a base URL, timeouts, connection limits, transports, and proxy routing. Client-level headers, parameters, and cookies can be combined with request-level values.

### Timeouts and redirects

HTTPX applies a default timeout of five seconds of network inactivity. Set `timeout` on a request or client to change it; use `timeout=None` to disable timeouts. Fine-grained configurations can set separate connect, read, write, and pool timeouts:

```python
timeout = httpx.Timeout(10.0, connect=60.0)
client = httpx.Client(timeout=timeout)
```

Redirects are **not followed by default**. Enable them for a request with `follow_redirects=True`, or set that option when creating a client.

### TLS and HTTP/2

HTTPS certificate verification is enabled by default. Supply an `ssl.SSLContext` using `verify` for custom trust stores or client certificates; `verify=False` disables verification and should be used with care.

HTTP/2 support is optional and disabled by default. Install `httpx[http2]`, then enable it on a client:

```python
client = httpx.Client(http2=True)
```

A server must also support HTTP/2 for a connection to use it. Check `response.http_version` to see the negotiated protocol.

### Proxies and environment

Configure a proxy with the `proxy` argument, or use `mounts` for routing different URL patterns through different transports. SOCKS proxy support requires `httpx[socks]`.

By default, HTTPX uses proxy-related environment variables when available. Set `trust_env=False` on a client or top-level request to ignore environment configuration. Recognized variables include `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and `NO_PROXY`.

### Connection limits

Use `httpx.Limits` with a client’s `limits` argument to configure connection-pool bounds and keep-alive expiry:

```python
limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
client = httpx.Client(limits=limits)
```

See the [advanced documentation](https://www.python-httpx.org/advanced/) for authentication, SSL, proxies, timeouts, resource limits, event hooks, transports, and text encodings. The [quickstart](https://www.python-httpx.org/quickstart/) and [API reference](https://www.python-httpx.org/api/) cover the rest of the public interface.

## Command-line usage

The command-line client is an optional install:

```shell
python -m pip install "httpx[cli]"
httpx --help
```

## Development

To work on HTTPX, fork the repository and clone your fork:

```shell
git clone https://github.com/YOUR-USERNAME/httpx
cd httpx
scripts/install
```

The project’s development requirements are listed in `requirements.txt`. The install script sets up the project and its development dependencies.

## Testing and checks

Run the test suite with:

```shell
scripts/test
```

The tests start local servers on ports **8000** and **8001**; make sure those ports are available. You can pass test arguments through the script to run a specific test file:

```shell
scripts/test tests/test_multipart.py
```

Run code checks separately, or apply linting and formatting with:

```shell
scripts/check
scripts/lint
```

To preview the documentation locally, run:

```shell
scripts/docs
```

Documentation sources are in `docs/`. Contributions should generally start with a [GitHub discussion](https://github.com/encode/httpx/discussions). For bug reports, include a minimal example, traceback, Python version, operating system, and installed dependency versions. Pull requests should include tests for changes and documentation updates where appropriate. See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) for project guidance.

## License

HTTPX is distributed under the **BSD 3-Clause License**. See [LICENSE.md](LICENSE.md) for the full terms.

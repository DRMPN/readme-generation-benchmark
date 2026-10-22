# HTTPX

> A next-generation HTTP client for Python.

<div align="center">

**HTTP/1.1 · HTTP/2 · Sync & Async · Type-Annotated · Requests-Compatible**

[![Python Versions](https://img.shields.io/pypi/pyversions/httpx.svg)](https://pypi.org/project/httpx/)
[![Version](https://img.shields.io/pypi/v/httpx.svg)](https://pypi.org/project/httpx/)
[![License](https://img.shields.io/pypi/l/httpx.svg)](LICENSE.md)

</div>

---

HTTPX is a fully featured HTTP client library for Python 3. It includes:

* **A widely known and loved API** — if you've used `requests`, you already know most of HTTPX.
* **Standard synchronous interface**, but with **async support** if you need it.
* **HTTP/1.1 and HTTP/2** support.
* **The ability to make requests directly against WSGI or ASGI applications** — ideal for testing.
* **Strict timeout handling** by default.
* **Fully type annotated** code, shipped with a `py.typed` marker.
* **An integrated command line client** (`python -m httpx`).
* **100% test coverage**.

---

## Table of Contents

* [Installation](#installation)
* [Quickstart](#quickstart)
* [Streaming Responses](#streaming-responses)
* [Async Support](#async-support)
* [HTTP/2 Support](#http2-support)
* [Advanced Usage](#advanced-usage)
* [Command Line Interface](#command-line-interface)
* [Environment Variables](#environment-variables)
* [Exceptions](#exceptions)
* [Documentation](#documentation)
* [Third-Party Packages](#third-party-packages)
* [Contributing](#contributing)
* [Changelog & License](#changelog--license)

---

## Installation

Install with `pip`:

```shell
pip install httpx
```

HTTPX requires **Python 3.8+** (see `pyproject.toml` for the exact supported range of your release) and depends on:

* `httpcore` — the low-level transport layer
* `anyio` — async/concurrency primitives
* `certifi` — SSL certificates
* `idna` — internationalized domain names

### Optional Extras

Some functionality requires additional dependencies, available as extras:

```shell
pip install httpx[http2]    # HTTP/2 support (h2)
pip install httpx[brotli]   # Brotli response decoding
pip install httpx[zstd]     # Zstandard response decoding
pip install httpx[socks]    # SOCKS proxy support
```

---

## Quickstart

### Sending a Request

Start by importing HTTPX and making a request:

```pycon
>>> import httpx
>>> r = httpx.get('https://httpbin.org/get')
>>> r
<Response [200 OK]>
>>> r.status_code
200
>>> r.headers['content-type']
'application/json'
>>> r.text
'{"args": {}, "data": "", "files": {}, "form": {}, "headers": {...}}'
>>> r.json()['url']
'https://httpbin.org/get'
```

The following top-level request functions are available:

* `httpx.get(url, ...)`
* `httpx.post(url, ...)`
* `httpx.put(url, ...)`
* `httpx.patch(url, ...)`
* `httpx.delete(url, ...)`
* `httpx.head(url, ...)`
* `httpx.options(url, ...)`
* `httpx.request(method, url, ...)`
* `httpx.stream(method, url, ...)`

### Response Content

A `Response` exposes the response body in several ways:

```pycon
>>> r.text                # Decoded text
>>> r.content             # Raw bytes
>>> r.encoding            # Character encoding used to decode `r.text`
>>> r.json()              # Parsed JSON body
```

### Query Parameters

Include parameters in the URL via the `params` keyword:

```pycon
>>> params = {'key1': 'value1', 'key2': ['value2', 'value3']}
>>> r = httpx.get('https://httpbin.org/get', params=params)
>>> r.url
URL('https://httpbin.org/get?key1=value1&key2=value2&key2=value3')
```

### Request Headers

Use a dictionary with the `headers` keyword:

```pycon
>>> headers = {'User-Agent': 'my-app/1.0.0', 'X-Custom': 'value'}
>>> r = httpx.get('https://httpbin.org/get', headers=headers)
```

### Sending Request Bodies

**Form-encoded data:**

```python
data = {'name': 'World'}
r = httpx.post('https://httpbin.org/post', data=data)
```

**JSON-encoded data:**

```python
data = {'name': 'World'}
r = httpx.post('https://httpbin.org/post', json=data)
```

**Multipart file uploads:**

```python
files = {'file': ('report.csv', open('report.csv', 'rb'), 'text/csv')}
r = httpx.post('https://httpbin.org/post', files=files)
```

**Raw binary content:**

```python
content = b'Hello, world!'
r = httpx.post(
    'https://httpbin.org/post',
    content=content,
    headers={'Content-Type': 'text/plain'},
)
```

### Response Headers

Response headers behave like a case-insensitive, multi-valued dictionary:

```pycon
>>> r.headers
<Headers[('server', 'nginx'), ('content-type', 'application/json'), ...]>
>>> r.headers['Content-Type']
'application/json'
>>> r.headers.get('content-type')
'application/json'
```

### Cookies

Send cookies with a request:

```pycon
>>> r = httpx.get('https://httpbin.org/cookies', cookies={'session': 'abc123'})
```

Read cookies returned by a server:

```pycon
>>> r = httpx.get('https://httpbin.org/cookies/set?chocolate=chip')
>>> r.cookies['chocolate']
'chip'
```

### Redirection and History

By default, HTTPX does **not** follow redirects. Enable them with `follow_redirects`:

```pycon
>>> r = httpx.get('https://httpbin.org/redirect/2', follow_redirects=True)
>>> r.url
URL('https://httpbin.org/get')
>>> r.history
[<Response [302 Found]>, <Response [302 Found]>]
```

### Timeouts

HTTPX applies a **default timeout of 5 seconds** to every request:

```python
r = httpx.get('https://httpbin.org/delay/10', timeout=2.0)  # raises httpx.ReadTimeout
```

Fine-grained timeouts are supported via `httpx.Timeout`:

```python
timeout = httpx.Timeout(timeout=5.0, connect=10.0)
r = httpx.get('https://httpbin.org/get', timeout=timeout)
```

Pass `timeout=None` to disable timeouts entirely (not recommended).

### Authentication

Basic authentication with a two-tuple:

```python
r = httpx.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
```

Or explicitly with an auth class:

```python
r = httpx.get('https://httpbin.org/basic-auth/user/pass', auth=httpx.BasicAuth('user', 'pass'))
```

Digest authentication is also built in:

```python
r = httpx.get('https://httpbin.org/digest-auth/auth/user/pass', auth=httpx.DigestAuth('user', 'pass'))
```

Custom authentication schemes can be implemented by subclassing `httpx.Auth` — see [`docs/authentication.md`](docs/authentication.md).

### Status Codes and `raise_for_status()`

```pycon
>>> httpx.codes.NOT_FOUND == 404
True
>>> r.is_success
False
>>> r.raise_for_status()
Traceback (most recent call last):
    ...
httpx.HTTPStatusError: 404 Not Found for url 'https://httpbin.org/status/404'
```

---

## Streaming Responses

For large responses, use the streaming API and avoid loading the whole body into memory:

```python
with httpx.stream('GET', 'https://httpbin.org/bytes/8192') as r:
    r.raise_for_status()
    with open('download.bin', 'wb') as f:
        for chunk in r.iter_bytes():
            f.write(chunk)
```

Available iteration methods:

* `r.iter_bytes()` — raw response chunks
* `r.iter_text()` — decoded text chunks
* `r.iter_lines()` — line-by-line iteration
* `r.iter_raw()` — untouched transport chunks

---

## Async Support

HTTPX provides a full async API via `httpx.AsyncClient`:

```python
import asyncio
import httpx


async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get('https://httpbin.org/get')
        print(r.status_code)


asyncio.run(main())
```

The async API mirrors the sync one, including streaming:

```python
async with httpx.AsyncClient() as client:
    async with client.stream('GET', 'https://httpbin.org/bytes/8192') as r:
        async for chunk in r.aiter_bytes():
            ...
```

AnyIO is used under the hood, so the async client works with `asyncio`, `trio`, and other supported backends.

---

## HTTP/2 Support

Enable HTTP/2 (requires `pip install httpx[http2]`):

```python
with httpx.Client(http2=True) as client:
    r = client.get('https://httpbin.org/get')
    print(r.http_version)  # 'HTTP/2'
```

HTTP/2 is used automatically when the server supports it; otherwise the connection gracefully falls back to HTTP/1.1.

---

## Advanced Usage

### Client Instances

The recommended interface for real-world usage is a `Client` instance, which manages connection pooling, cookies, and configuration:

```python
with httpx.Client() as client:
    r = client.get('https://httpbin.org/get')
```

Clients also support a `base_url`, for working against a single host:

```python
client = httpx.Client(base_url='https://httpbin.org')
client.get('/get')
```

The async equivalent is `httpx.AsyncClient`. Defaults such as headers, cookies, auth, timeouts, and query parameters can be set once on the client and applied to every request.

### Connection Pooling

Control connection behaviour with `httpx.Limits`:

```python
limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
client = httpx.Client(limits=limits)
```

See [`docs/resource-limits.md`](docs/resource-limits.md).

### Proxies

```python
client = httpx.Client(proxy='http://127.0.0.1:8080')

# SOCKS proxies (requires `pip install httpx[socks]`)
client = httpx.Client(proxy='socks5://user:pass@127.0.0.1:1080')
```

Route different traffic through different proxies using `mounts`:

```python
mounts = {
    'https://': httpx.HTTPTransport(proxy='http://127.0.0.1:8080'),
    'all://': httpx.HTTPTransport(),
}
client = httpx.Client(mounts=mounts)
```

See [`docs/proxies.md`](docs/proxies.md).

### SSL Certificates

```python
# Use a custom CA bundle
client = httpx.Client(verify='/path/to/cert.pem')

# Client-side certificates
client = httpx.Client(cert=('/path/client.crt', '/path/client.key'))

# Disable verification (NOT recommended in production)
client = httpx.Client(verify=False)
```

See [`docs/ssl.md`](docs/ssl.md).

### Event Hooks

Hooks allow arbitrary logic to be attached to each request/response cycle:

```python
def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    print(f"Response event hook: {response.status_code}")

client = httpx.Client(
    event_hooks={'request': [log_request], 'response': [log_response]},
)
```

Hooks on `AsyncClient` instances must be `async` functions. See [`docs/event-hooks.md`](docs/event-hooks.md).

### Custom Transports

Transports determine how a request is actually sent:

```python
transport = httpx.HTTPTransport(retries=1)   # Retry once on connection failures
client = httpx.Client(transport=transport)
```

Implement your own by subclassing `httpx.BaseTransport` (or `httpx.AsyncBaseTransport`):

```python
class HelloTransport(httpx.BaseTransport):
    def handle_request(self, request):
        return httpx.Response(200, json={'message': 'Hello, world!'})
```

See [`docs/transports.md`](docs/transports.md).

### Mock Transports (Testing)

`httpx.MockTransport` lets you stub out responses entirely — great for unit tests:

```python
def handler(request):
    return httpx.Response(200, json={'url': str(request.url)})

transport = httpx.MockTransport(handler)
client = httpx.Client(transport=transport)
r = client.get('https://example.com/test')  # {'url': 'https://example.com/test'}
```

### WSGI and ASGI Transports

HTTPX can send requests directly against local WSGI or ASGI applications — perfect for testing your own web apps without a running server:

```python
transport = httpx.WSGITransport(app=wsgi_app)
client = httpx.Client(transport=transport)
r = client.get('http://testserver/')
```

```python
transport = httpx.ASGITransport(app=asgi_app)
client = httpx.Client(transport=transport)
r = client.get('http://testserver/')
```

---

## Command Line Interface

HTTPX ships with an integrated command line client:

```shell
python -m httpx https://httpbin.org/get
python -m httpx --method POST https://httpbin.org/post --json '{"name": "World"}'
python -m httpx https://httpbin.org/basic-auth/user/pass --auth user:pass
python -m httpx https://httpbin.org/get --timeout 10 --verbose
```

Common options include `--method`, `--json`, `--form`, `--auth`, `--header`, `--params`, `--timeout`, and `--verbose`.

---

## Environment Variables

HTTPX respects the following standard environment variables:

| Variable | Purpose |
|---|---|
| `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY` | Proxy configuration |
| `SSL_CERT_FILE`, `SSL_CERT_DIR` | Custom SSL certificate locations |

Environment-based behavior can be disabled per-client:

```python
client = httpx.Client(trust_env=False)
```

See [`docs/environment_variables.md`](docs/environment_variables.md).

---

## Exceptions

All HTTPX exceptions inherit from `httpx.HTTPError`:

```
httpx.HTTPError
├── httpx.RequestError
│   ├── httpx.TransportError
│   │   ├── httpx.TimeoutException   → ConnectTimeout, ReadTimeout, WriteTimeout, PoolTimeout
│   │   ├── httpx.NetworkError       → ConnectError, ReadError, WriteError, CloseError
│   │   └── httpx.ProtocolError      → LocalProtocolError, RemoteProtocolError, ProxyError, ...
│   ├── httpx.TooManyRedirects
│   ├── httpx.DecodingError
│   ├── httpx.InvalidURL
│   ├── httpx.CookieConflict
│   └── httpx.StreamError            → StreamClosed, ResponseNotRead, StreamConsumed, ...
└── httpx.HTTPStatusError
```

A typical error-handling pattern:

```python
try:
    r = httpx.get('https://httpbin.org/get')
    r.raise_for_status()
except httpx.HTTPStatusError as exc:
    print(f"Error response {exc.response.status_code} while requesting {exc.request.url}")
except httpx.RequestError as exc:
    print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
```

See [`docs/exceptions.md`](docs/exceptions.md).

---

## Documentation

Full documentation lives in the `docs/` directory (also published via `mkdocs` — see `mkdocs.yml`):

| Topic | Documentation |
|---|---|
| Quickstart | [`docs/quickstart.md`](docs/quickstart.md) |
| API Reference | [`docs/api.md`](docs/api.md) |
| Async | [`docs/async.md`](docs/async.md) |
| Clients | [`docs/clients.md`](docs/clients.md) |
| HTTP/2 | [`docs/http2.md`](docs/http2.md) |
| Authentication | [`docs/authentication.md`](docs/authentication.md) |
| Event Hooks | [`docs/event-hooks.md`](docs/event-hooks.md) |
| Exceptions | [`docs/exceptions.md`](docs/exceptions.md) |
| Proxies | [`docs/proxies.md`](docs/proxies.md) |
| Timeouts | [`docs/timeouts.md`](docs/timeouts.md) |
| Resource Limits | [`docs/resource-limits.md`](docs/resource-limits.md) |
| Transports | [`docs/transports.md`](docs/transports.md) |
| SSL | [`docs/ssl.md`](docs/ssl.md) |
| Text Encodings | [`docs/text-encodings.md`](docs/text-encodings.md) |
| Environment Variables | [`docs/environment_variables.md`](docs/environment_variables.md) |
| Compatibility with `requests` | [`docs/compatibility.md`](docs/compatibility.md) |
| Troubleshooting | [`docs/troubleshooting.md`](docs/troubleshooting.md) |
| Third-Party Packages | [`docs/third_party_packages.md`](docs/third_party_packages.md) |

---

## Third-Party Packages

A growing ecosystem of libraries builds on HTTPX, including:

* **respx** — mock/patch HTTPX traffic in tests
* **pytest-httpx** — pytest fixture for mocking responses
* **hishel** — HTTP caching for HTTPX
* **httpx-cache** — request/response caching
* **httpx-auth** — additional authentication schemes
* **httpx-ntlm** — NTLM authentication support

---

## Contributing

Contributions are very welcome! To set up a development environment:

```shell
git clone https://github.com/encode/httpx.git
cd httpx
make install
```

The project includes a `Makefile` with the following targets:

| Target | Description |
|---|---|
| `make install` | Set up the development environment |
| `make test` | Run the test suite with pytest |
| `make coverage` | Run tests with coverage reporting |
| `make lint` | Run static checks (ruff, mypy) |
| `make check` | Run the complete lint/format/test check suite |
| `make docs` | Build the documentation with mkdocs |
| `make build` | Build distributable packages |
| `make publish` | Publish the package to PyPI |
| `make clean` | Remove build artifacts |
| `make sync-version` | Synchronize version strings across files |

Pinned development dependencies are listed in [`requirements.txt`](requirements.txt), and project configuration (build system, tool settings) is in [`pyproject.toml`](pyproject.toml).

Guidelines:

* Maintain **100% test coverage** — the test suite in `tests/` covers the client, models, transports, decoders, auth, timeouts, proxies, redirects, and more.
* Keep the public API strictly type-annotated (`py.typed` is included in the distribution).
* Run `make check` before submitting a pull request.

---

## Changelog & License

* **Changelog** — see [`CHANGELOG.md`](CHANGELOG.md) for release history.
* **License** — HTTPX is released under the BSD 3-Clause license. See [`LICENSE.md`](LICENSE.md) for details.

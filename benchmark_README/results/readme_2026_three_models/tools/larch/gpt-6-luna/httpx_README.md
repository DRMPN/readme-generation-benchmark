# HTTPX

HTTPX is a Python HTTP client for making synchronous and asynchronous HTTP requests. It provides a familiar, high-level API while supporting features such as connection pooling, streaming, HTTP/2, and custom transports.

## Features

- Synchronous and asynchronous clients
- HTTP/1.1 and optional HTTP/2 support
- Connection pooling and persistent cookies
- Request and response streaming
- Timeouts, redirects, authentication, and proxy support
- JSON, form, and multipart file uploads
- Custom transports, including WSGI and ASGI transports
- A broadly familiar API for users of `requests`

## Installation

Install HTTPX with pip:

```bash
pip install httpx
```

HTTP/2 support is available as an optional dependency:

```bash
pip install "httpx[http2]"
```

## Quickstart

Make a request with the top-level API:

```python
import httpx

response = httpx.get("https://httpbin.org/get")

print(response.status_code)
print(response.json())
```

HTTPX also provides methods for other common HTTP verbs:

```python
httpx.post("https://httpbin.org/post", json={"name": "Ada"})
httpx.put("https://httpbin.org/put", data={"active": "true"})
httpx.delete("https://httpbin.org/delete")
```

Pass query parameters, headers, or form data as keyword arguments:

```python
response = httpx.get(
    "https://httpbin.org/headers",
    params={"page": 2},
    headers={"X-Client": "example"},
)
```

For JSON responses, use `response.json()`. For text or binary content, use `response.text` or `response.content`:

```python
response = httpx.get("https://httpbin.org/json")

data = response.json()
text = response.text
raw_bytes = response.content
```

Check the status code or raise an exception for unsuccessful responses:

```python
response = httpx.get("https://httpbin.org/status/404")
response.raise_for_status()
```

## Using a client

For multiple requests to the same service, use a `Client`. Clients reuse connections and can share configuration such as headers, authentication, and cookies.

```python
import httpx

with httpx.Client(base_url="https://httpbin.org") as client:
    response = client.get("/get", params={"q": "httpx"})
    print(response.json())
```

A client can also be configured with default headers, timeouts, and redirect behavior:

```python
with httpx.Client(
    headers={"User-Agent": "my-application"},
    timeout=10.0,
    follow_redirects=True,
) as client:
    response = client.get("https://example.com")
```

Redirects are not followed by default. Set `follow_redirects=True` on a request or client to follow them.

## Asynchronous requests

Use `AsyncClient` in asynchronous applications. Its request methods must be awaited, and the client should be closed when it is no longer needed.

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        print(response.json())

asyncio.run(main())
```

The asynchronous client supports the same general configuration and request options as the synchronous client.

## Request data and file uploads

Use `json=` to send JSON, `data=` to send form data, and `files=` to upload files:

```python
import httpx

response = httpx.post(
    "https://httpbin.org/post",
    json={"message": "hello"},
)

with open("report.txt", "rb") as report:
    upload_response = httpx.post(
        "https://httpbin.org/post",
        files={"file": report},
    )
```

## Timeouts

HTTPX applies a timeout by default. Set a different timeout on a request or client:

```python
response = httpx.get("https://example.com", timeout=20.0)
```

For more control, configure connect, read, write, and connection-pool timeouts separately:

```python
timeout = httpx.Timeout(10.0, connect=2.0)

with httpx.Client(timeout=timeout) as client:
    response = client.get("https://example.com")
```

See the [timeouts guide](https://www.python-httpx.org/advanced/timeouts/) for details.

## Streaming

For large responses, stream the body instead of loading it all into memory at once:

```python
import httpx

with httpx.stream("GET", "https://example.com/large-file") as response:
    response.raise_for_status()
    for chunk in response.iter_bytes():
        process(chunk)
```

The same pattern is available on clients with `client.stream(...)`. Async clients provide asynchronous streaming methods such as `aiter_bytes()`.

## HTTP/2

Install the HTTP/2 extra, then enable HTTP/2 on a client:

```python
import httpx

with httpx.Client(http2=True) as client:
    response = client.get("https://example.com")
```

HTTPX can negotiate the protocol with the server; enabling HTTP/2 does not guarantee that every connection will use it.

## Documentation

The full documentation is available at **[www.python-httpx.org](https://www.python-httpx.org/)**. It includes guides for clients, authentication, proxies, SSL, timeouts, streaming, transports, and more.

## Contributing

Contributions are welcome. See the repository’s `contributing.md` for development guidance, and consult the documentation and tests when making changes.

## License

See [`LICENSE.md`](LICENSE.md) for the license terms.

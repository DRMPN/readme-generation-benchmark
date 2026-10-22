# httpx<h2>Description</h2>

<p>HTTPX is a fully featured HTTP client for Python. It provides both synchronous and asynchronous APIs, with support for HTTP/1.1 and optional HTTP/2. Its features include connection pooling, timeouts, redirects, authentication, proxies, and streaming requests and responses.</p>
<h2>Requirements</h2>

<p>HTTPX requires Python 3.8 or later.</p>
<h2>Installation</h2>

<p>Install HTTPX using pip:</p>

<p><code>shell
pip install httpx
</code></p>

<p>For HTTP/2 support, install the <code>http2</code> extra:</p>

<p><code>shell
pip install "httpx[http2]"
</code></p>
<h2>Usage</h2>

<p>Use the top-level functions for a simple request:</p>

<p>```python
import httpx</p>

<p>response = httpx.get("https://www.example.org/")</p>

<p>print(response.status_code)
print(response.headers["content-type"])
print(response.text)
```</p>

<p>For multiple requests, use a client:</p>

<p><code>python
with httpx.Client() as client:
    response = client.get("https://www.example.org/")
    print(response.status_code)
</code></p>

<p>HTTPX also supports asynchronous requests with <code>AsyncClient</code>:</p>

<p>```python
import asyncio
import httpx</p>

<p>async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.example.org/")
        print(response.status_code)</p>

<p>asyncio.run(main())
```</p>
<h2>Contributing</h2>

<p>For information on contributing to HTTPX, see <code>contributing.md</code> in the Community documentation.</p>
<h2>License</h2>

<p>HTTPX is released under the BSD 3-Clause license.</p>

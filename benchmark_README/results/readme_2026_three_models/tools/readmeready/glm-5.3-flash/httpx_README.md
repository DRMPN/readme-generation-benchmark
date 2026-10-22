# httpx<h2>Description</h2>

<p>HTTPX is a fully featured HTTP client library for Python. It includes an intuitive API, support for both synchronous and asynchronous code styles, and support for both HTTP/1.1 and HTTP/2.</p>

<p>Key features include:</p>

<ul>
<li><strong>Synchronous and asynchronous API</strong> — Use the same client interface whether your application is blocking or async.</li>
<li><strong>HTTP/1.1 and HTTP/2 support</strong> — HTTP/2 support is available via the optional <code>http2</code> extra.</li>
<li><strong>Proxies, timeouts, SSL, and connection pooling</strong> — Fine-grained control over how requests are made, including resource limits and configurable transports.</li>
<li><strong>Rich built-in tooling</strong> — Event hooks, authentication flows, and text encoding handling.</li>
<li><strong>Command line interface</strong> — An <code>httpx</code> command is included for making requests directly from the terminal.</li>
<li><strong>Optional compression support</strong> — Brotli and Zstandard decompression via the <code>brotli</code> and <code>zstd</code> extras, plus SOCKS proxy support via the <code>socks</code> extra.</li>
</ul>

<p>The full documentation, including a QuickStart guide, advanced usage guides, and API reference, is available at <a href="https://www.python-httpx.org">https://www.python-httpx.org</a>.</p>

<p>For release information and recent changes, see the <a href="https://github.com/encode/httpx/blob/master/CHANGELOG.md">Full changelog</a>.</p>
<h2>Requirements</h2>

<p>httpx requires the following:</p>

<ul>
<li>Python 3.9+</li>
</ul>

<p>httpx also relies on a small number of core dependencies to handle the low-level details of HTTP:</p>

<ul>
<li><code>httpcore</code> — The underlying HTTP transport implementation, which handles connection pooling, the HTTP/1.1 and HTTP/2 protocols, and asynchronous support.</li>
<li><code>anyio</code> — Used to provide the async API.</li>
<li><code>certifi</code> — SSL certificate bundle, used for verifying HTTPS connections.</li>
<li><code>idna</code> — Internationalized domain name support.</li>
</ul>

<h3>Optional extras</h3>

<p>Some functionality is provided through optional dependency groups, which can be installed using the <code>extras</code> syntax:</p>

<p>```bash</p>

<h1>HTTP/2 support</h1>

<p>pip install httpx[http2]</p>

<h1>Brotli response compression support</h1>

<p>pip install httpx[brotli]</p>

<h1>SOCKS proxy support</h1>

<p>pip install httpx[socks]</p>

<h1>Zstandard response compression support</h1>

<p>pip install httpx[zstandard]
```</p>

<ul>
<li>The <code>http2</code> extra installs the <code>h2</code> library, enabling you to use the HTTP/2 protocol with your requests.</li>
<li>The <code>brotli</code> and <code>zstandard</code> extras install libraries for decoding Brotli- and Zstandard-compressed responses.</li>
<li>The <code>socks</code> extra installs the <code>socksio</code> library, enabling requests to be made through a SOCKS proxy.</li>
</ul>
<h2>Installation</h2>

<p>Install with <code>pip</code>:</p>

<p><code>shell
pip install httpx
</code></p>

<p>Or add httpx directly to your project's dependencies if you're using a <code>requirements.txt</code> file:</p>

<p><code>
httpx
</code></p>

<p>If you plan to use HTTP/2 support, you'll also need to install the optional <code>http2</code> extra, which pulls in the required dependencies:</p>

<p><code>shell
pip install httpx[http2]
</code></p>
<h2>Usage</h2>

<h3>Making a Request</h3>

<p>The simplest way to use <code>httpx</code> is to call one of the top-level request functions, such as <code>httpx.get()</code>:</p>

<p>```python</p>

<blockquote>
  <blockquote>
    <blockquote>
      <p>import httpx
      response = httpx.get('https://example.com')
      response
      <Response [200 OK]&gt;
      response.status_code
      200
      response.text
      '<!doctype html>...'
      ```</p>
    </blockquote>
  </blockquote>
</blockquote>

<p>You can also send <code>POST</code>, <code>PUT</code>, <code>DELETE</code>, <code>HEAD</code>, and <code>OPTIONS</code> requests:</p>

<p>```python</p>

<blockquote>
  <blockquote>
    <blockquote>
      <p>response = httpx.post('https://example.com', json={'key': 'value'})
      response = httpx.put('https://example.com', data={'key': 'value'})
      response = httpx.delete('https://example.com')
      response = httpx.head('https://example.com')
      response = httpx.options('https://example.com')
      ```</p>
    </blockquote>
  </blockquote>
</blockquote>

<h3>Using a Client</h3>

<p>For making multiple requests, or for more advanced configuration, use a <code>Client</code> instance:</p>

<p>```python</p>

<blockquote>
  <blockquote>
    <blockquote>
      <p>import httpx
      with httpx.Client() as client:
      ...     response = client.get('https://example.com')
      ...     print(response.status_code)
      200
      ```</p>
    </blockquote>
  </blockquote>
</blockquote>

<p>A <code>Client</code> instance can be configured with various options, such as:</p>

<p>```python</p>

<blockquote>
  <blockquote>
    <blockquote>
      <p>client = httpx.Client(
      ...     auth=('username', 'password'),
      ...     headers={'X-Custom': 'value'},
      ...     timeout=5.0,
      ... )
      ```</p>
    </blockquote>
  </blockquote>
</blockquote>

<p>Available options include:</p>

<ul>
<li><strong>auth</strong> - <em>(optional)</em> An authentication class to use when sending requests.</li>
<li><strong>params</strong> - <em>(optional)</em> Query parameters to include in request URLs, as a string, dictionary, or sequence of two-tuples.</li>
<li><strong>headers</strong> - <em>(optional)</em> Dictionary of HTTP headers to include when sending requests.</li>
<li><strong>cookies</strong> - <em>(optional)</em> Dictionary of Cookie items to include when sending requests.</li>
<li><strong>verify</strong> - <em>(optional)</em> Either <code>True</code> to use an SSL context with the default CA bundle, <code>False</code> to disable verification, or an instance of <code>ssl.SSLContext</code> to use a custom context.</li>
<li><strong>http2</strong> - <em>(optional)</em> A boolean indicating if HTTP/2 support should be enabled. Defaults to <code>False</code>.</li>
<li><strong>proxy</strong> - <em>(optional)</em> A proxy URL where all the traffic should be routed.</li>
<li><strong>timeout</strong> - <em>(optional)</em> The timeout configuration to use when sending requests.</li>
<li><strong>limits</strong> - <em>(optional)</em> The limits configuration to use.</li>
</ul>

<h3>Async Requests</h3>

<p><code>httpx</code> also supports asynchronous request handling with <code>AsyncClient</code>:</p>

<p>```python
import asyncio
import httpx</p>

<p>async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://example.com')
        print(response.status_code)</p>

<p>asyncio.run(main())
```</p>
<h2>Contributing</h2>

<p>For guidance on setting up a development environment, and how to make a
contribution to HTTPX, see
<a href="https://github.com/encode/httpx/blob/master/docs/contributing.md">Contributing to HTTPX</a>.</p>

<p>If you're looking to get involved with the HTTPX project, the community
section of the documentation is a good place to start:</p>

<ul>
<li><a href="https://github.com/encode/httpx/blob/master/docs/contributing.md">Contributing</a> — how to set up a development environment and submit a contribution.</li>
<li><a href="https://github.com/encode/httpx/blob/master/docs/code_of_conduct.md">Code of Conduct</a> — the community guidelines for participating in the project.</li>
<li><a href="https://github.com/encode/httpx/blob/master/docs/third_party_packages.md">Third Party Packages</a> — a listing of packages built by the community on top of HTTPX.</li>
</ul>

<p>We'd love to see your contributions — whether that's code, documentation, or feedback on how the project can be improved.</p>
<h2>License</h2>

<p>This project is licensed under the terms of the BSD 3-Clause License.</p>

<p>Copyright (c) Encode OSS Ltd.</p>

<p>For the full license text, see the <code>LICENSE</code> file included in the repository.</p>

# httpx<h2>Description</h2>

<p>httpx is a Python HTTP client library. The project's packaging configuration defines optional extras for additional features:</p>

<ul>
<li><strong><code>brotli</code></strong>: Brotli content decoding. Installs <code>brotli</code> on CPython and <code>brotlicffi</code> on other Python implementations.</li>
<li><strong><code>cli</code></strong>: Command-line support, using <code>click</code>, <code>pygments</code>, and <code>rich</code>.</li>
<li><strong><code>http2</code></strong>: HTTP/2 support, using <code>h2</code>.</li>
<li><strong><code>socks</code></strong>: SOCKS proxy support, using <code>socksio</code>.</li>
<li><strong><code>zstd</code></strong>: Zstandard content decoding, using <code>zstandard</code>.</li>
</ul>

<p>The package also provides an <code>httpx</code> command-line entry point that runs <code>httpx:main</code>.</p>

<p>Project links:</p>

<ul>
<li><a href="https://www.python-httpx.org">Documentation</a></li>
<li><a href="https://github.com/encode/httpx">Source</a></li>
<li><a href="https://github.com/encode/httpx/blob/master/CHANGELOG.md">Changelog</a></li>
</ul>
<h2>Requirements</h2>

<p>The build system for this project uses <a href="https://github.com/pypa/hatch">Hatchling</a> as the build backend, together with the <code>hatch-fancy-pypi-readme</code> plugin. Both are declared in <code>pyproject.toml</code>.</p>

<p>The provided context does not specify the Python version or the runtime dependencies needed to use the package, so those details are not listed here.</p>

<p>For related information, see:</p>

<ul>
<li><strong>Environment Variables:</strong> <code>environment_variables.md</code></li>
<li><strong>Third Party Packages:</strong> <code>third_party_packages.md</code></li>
<li><strong>Contributing:</strong> <code>contributing.md</code></li>
<li><strong>Code of Conduct:</strong> <code>code_of_conduct.md</code></li>
</ul>
<h2>Installation</h2>

<p>Install HTTPX from PyPI using pip:</p>

<p><code>bash
pip install httpx
</code></p>
<h2>Usage</h2>

<p>Send a request with the top-level helper:</p>

<p>```python
import httpx</p>

<p>response = httpx.get("https://www.example.org/")
print(response.status_code)
print(response.text)
```</p>

<p>To share settings across several requests, create a <code>Client</code> instance and use it to send requests:</p>

<p>```python
import httpx</p>

<p>with httpx.Client(
    headers={"User-Agent": "my-app/1.0"},
    timeout=10.0,
) as client:
    response = client.get("https://www.example.org/")
```</p>

<p>The <code>Client</code> accepts the following optional arguments:</p>

<ul>
<li><strong>auth</strong>: An authentication class to use when sending requests.</li>
<li><strong>params</strong>: Query parameters to include in request URLs, as a string, dictionary, or sequence of two-tuples.</li>
<li><strong>headers</strong>: Dictionary of HTTP headers to include when sending requests.</li>
<li><strong>cookies</strong>: Dictionary of Cookie items to include when sending requests.</li>
<li><strong>verify</strong>: Either <code>True</code> to use an SSL context with the default CA bundle, <code>False</code> to disable verification, or an instance of <code>ssl.SSLContext</code> to use a custom context.</li>
<li><strong>http2</strong>: A boolean indicating whether HTTP/2 support should be enabled. Defaults to <code>False</code>.</li>
<li><strong>proxy</strong>: A proxy URL where all the traffic should be routed.</li>
<li><strong>timeout</strong>: The timeout configuration to use when sending requests.</li>
<li><strong>limits</strong>: The limits configuration to use.</li>
</ul>
<h2>Contributing</h2>

<p>Contribution guidelines are in <code>contributing.md</code>. The project's expectations for community conduct are in <code>code_of_conduct.md</code>.</p>
<h2>License</h2>

<!-- Intentionally left blank: the provided context does not include the project's license terms or a license file link. -->

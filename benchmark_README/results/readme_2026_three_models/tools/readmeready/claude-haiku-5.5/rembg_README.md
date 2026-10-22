# rembg<h2>Description</h2>

<p>rembg is a Python project for removing backgrounds from images. It can be installed with optional extras: <code>cli</code> for a command-line interface and <code>gpu</code> for GPU acceleration through <code>onnxruntime-gpu</code>. The web API is built with FastAPI and served with Uvicorn, and its interactive API documentation is available at <code>/api</code>. The project also depends on Gradio, which is used for a web interface.</p>

<p>rembg is released under the <a href="https://github.com/danielgatis/rembg/blob/main/LICENSE.txt">MIT License</a>.</p>
<h2>Requirements</h2>

<p>Dependencies are declared in <code>requirements.txt</code> and <code>requirements-gpu.txt</code>, and the package metadata is in <code>pyproject.toml</code> and <code>setup.py</code>.</p>

<p>rembg has optional extras:</p>

<ul>
<li><strong><code>cli</code></strong>: adds the command-line and web-server dependencies (for example, FastAPI, Uvicorn, and Gradio).</li>
<li><strong><code>gpu</code></strong>: adds GPU support through <code>onnxruntime-gpu</code>.</li>
</ul>

<p>To install rembg with both extras:</p>

<p><code>bash
pip install "rembg[cli,gpu]"
</code></p>
<h2>Installation</h2>

<p>Install rembg with pip:</p>

<p><code>bash
pip install rembg
</code></p>

<p>rembg provides optional extras that add dependencies for specific runtimes and features:</p>

<p>| Extra | Installs | Purpose |
|-------|----------|---------|
| <code>cpu</code> | <code>onnxruntime</code> | Run models on the CPU |
| <code>gpu</code> | <code>onnxruntime-gpu</code> | Run models on NVIDIA GPUs |
| <code>rocm</code> | <code>onnxruntime-rocm</code> | Run models on AMD GPUs (ROCm) |
| <code>cli</code> | <code>aiohttp</code>, <code>asyncer</code>, <code>click</code>, <code>fastapi</code>, <code>filetype</code>, <code>gradio</code>, <code>python-multipart</code>, <code>uvicorn</code>, <code>watchdog</code> | Command-line interface, web server, and Gradio UI |
| <code>dev</code> | <code>bandit</code>, <code>black</code>, <code>flake8</code>, <code>imagehash</code>, <code>isort</code>, <code>mypy</code>, <code>pytest</code>, <code>setuptools</code>, <code>twine</code>, <code>wheel</code> | Development and testing tools |</p>

<p>To install one or more extras, add them in square brackets:</p>

<p>```bash</p>

<h1>CPU runtime with the command-line interface</h1>

<p>pip install "rembg[cpu,cli]"</p>

<h1>GPU runtime with the command-line interface</h1>

<p>pip install "rembg[gpu,cli]"
```</p>
<h2>Usage</h2>

<p>The context provided for this section is limited, so this covers only what the repository code and packaging files show.</p>

<h3>Command-line interface (Windows installer)</h3>

<p>The repository includes an Inno Setup script that packages rembg's command-line tool as a Windows installer (<code>rembg-cli-installer</code>). The installer:</p>

<ul>
<li>Installs <code>rembg.exe</code> and its supporting files into the Program Files directory under a <code>Rembg</code> folder.</li>
<li>Offers an optional <strong>"Add to PATH variable"</strong> task, which adds the install location to your <code>PATH</code> so <code>rembg</code> can be run from any terminal.</li>
</ul>

<p>The installer is built into the <code>dist</code> output folder.</p>

<h3>Optional dependency extras</h3>

<p>The dependency metadata refers to the <code>cli</code> and <code>gpu</code> extras of the <code>rembg</code> package (for example, <code>rembg[cli,gpu]</code>). The <code>cli</code> extra brings in packages such as <code>uvicorn</code> and <code>gradio-client</code>, and the <code>gpu</code> extra brings in <code>onnxruntime-gpu</code>.</p>

<h3>Web API documentation</h3>

<p>The FastAPI application is configured with its interactive API documentation served at <code>/api</code>. Once the server is running, you can open that path in a browser to view the API docs.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>rembg is released under the MIT License. Copyright (c) 2020 Daniel Gatis.</p>

<p>The full license text is available in <a href="https://github.com/danielgatis/rembg/blob/main/LICENSE.txt">LICENSE.txt</a>.</p>

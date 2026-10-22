# rembg<h2>Description</h2>

<p>rembg is a tool to remove the background from images. It can be used as a Python library, a command-line tool, and as a server (FastAPI-based HTTP service). Under the hood, it uses ONNX Runtime models to perform image segmentation, producing images where the background is made transparent.</p>

<p>If this project has helped you, please consider giving it a ⭐.</p>

<h3>License</h3>

<p>This project is licensed under the MIT License - see the <a href="https://github.com/danielgatis/rembg/blob/main/LICENSE.txt">LICENSE.txt</a> file for details.</p>
<h2>Requirements</h2>

<ul>
<li>Python 3.x</li>
<li><a href="https://github.com/danielgatis/rembg">onnxruntime</a> — for CPU inference</li>
<li>For GPU support, install the GPU requirements (<code>requirements-gpu.txt</code>), which use <code>onnxruntime-gpu</code> instead of the CPU runtime</li>
</ul>

<p>All other dependencies (such as <code>pooch</code>, <code>numpy</code>, <code>opencv-python-headless</code>, <code>pymatting</code>, <code>fastapi</code>, <code>gradio</code>, and <code>typer</code> for the CLI/web server extras) are listed in <code>requirements.txt</code> and are installed automatically when you install rembg via pip:</p>

<p><code>bash
pip install rembg           # basic install
pip install "rembg[cli]"    # CLI support
pip install "rembg[gpu]"    # GPU (onnxruntime-gpu) support
</code></p>
<h2>Installation</h2>

<p>To install <code>rembg</code>, use <code>pip</code> with one of the following options depending on your needs:</p>

<h3>CPU</h3>

<p><code>bash
pip install rembg[cpu]
</code></p>

<h3>GPU (NVIDIA CUDA)</h3>

<p><code>bash
pip install rembg[gpu]
</code></p>

<h3>ROCm (AMD)</h3>

<p><code>bash
pip install rembg[rocm]
</code></p>

<h3>Command-line interface (CLI) and web server extras</h3>

<p>The CLI and the built-in FastAPI/Gradio server require additional dependencies (such as <code>fastapi</code>, <code>gradio</code>, <code>uvicorn</code>, <code>click</code>, etc.). You can combine extras, for example to install the CLI together with GPU support:</p>

<p><code>bash
pip install rembg[cli,gpu]
</code></p>

<h3>Development installation</h3>

<p>If you want to contribute or run the test suite, install the development dependencies:</p>

<p><code>bash
pip install rembg[dev]
</code></p>

<h3>Core dependencies</h3>

<p>The base installation includes the following core dependencies:</p>

<ul>
<li><code>jsonschema</code></li>
<li><code>numpy</code></li>
<li><code>opencv-python-headless</code></li>
<li><code>pillow</code></li>
<li><code>pooch</code></li>
<li><code>pymatting</code></li>
<li><code>scikit-image</code></li>
<li><code>scipy</code></li>
<li><code>tqdm</code></li>
</ul>

<p>The inference backend (<code>onnxruntime</code>) is not installed by default — you must select it via the <code>cpu</code>, <code>gpu</code>, or <code>rocm</code> extras as shown above.</p>
<h2>Usage</h2>

<p>rembg can be used in three main ways: as a command-line tool, as a Python library, and as an HTTP server.</p>

<h3>As a CLI</h3>

<p>After installing rembg, you can remove the background from an image directly from your terminal:</p>

<p><code>bash
rembg i path/to/input.png path/to/output.png
</code></p>

<p>Useful options include:</p>

<ul>
<li><code>-m</code> to specify a different model, for example:</li>
</ul>

<p><code>bash
rembg i -m isnet-general-use path/to/input.png path/to/output.png
</code></p>

<ul>
<li><code>-a</code> to enable alpha matting for better edge quality.</li>
<li><code>-om</code> to output only the mask instead of the full image.</li>
</ul>

<p>Processing a whole directory:</p>

<p><code>bash
rembg p path/to/input-dir path/to/output-dir
</code></p>

<h3>As a library</h3>

<p>In your Python code, use the <code>remove</code> function from the <code>rembg</code> package:</p>

<p>```python
from rembg import remove, new_session
from PIL import Image</p>

<p>session = new_session("isnet-general-use")</p>

<p>input<em>image = Image.open("input.png")
output</em>image = remove(input<em>image, session=session)
output</em>image.save("output.png")
```</p>

<p>The <code>session</code> can be reused across multiple calls so the model is loaded only once.</p>

<h3>As an HTTP server</h3>

<p>rembg also ships with a server mode that exposes the background removal functionality over HTTP:</p>

<p><code>bash
rembg s --host 0.0.0.0 --port 7000
</code></p>

<p>Once running, you can send images to the endpoints described in the auto-generated API docs available at <code>/api</code> on the running server.</p>
<h2>Contributing</h2>

<p>Contributions are welcome! If you'd like to help improve rembg, please feel free to open issues or submit pull requests on the project's GitHub repository.</p>

<p>Before contributing, please:</p>

<ol>
<li>Fork the repository and create your branch from the main branch.</li>
<li>Make sure your changes follow the existing code style.</li>
<li>Test your changes locally before submitting a pull request.</li>
</ol>

<p>rembg is licensed under the MIT License (Copyright (c) 2020 Daniel Gatis), so by contributing you agree that your contributions will be licensed under the same license.</p>
<h2>License</h2>

<p>The code of this project is released under the <a href="https://github.com/danielgatis/rembg/blob/main/LICENSE.txt">MIT License</a>.</p>

<p>Copyright (c) 2020 Daniel Gatis</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>
<h2>Description</h2>

<p>rembg is a Python library and tool suite for removing the background from images. It uses machine learning models (via ONNX Runtime) to segment the foreground subject of an image and produce a version of the image with a transparent background.</p>

<p>The project offers multiple ways to use it:</p>

<ul>
<li><strong>As a Python library</strong> — import <code>rembg</code> and use its <code>remove</code> function (and session classes) directly in your own code.</li>
<li><strong>As a command-line tool</strong> — a <code>rembg</code> CLI is provided (installed via the <code>cli</code> extra) for processing single images or batches of images.</li>
<li><strong>As an HTTP server</strong> — rembg ships a FastAPI-based server (installed via the <code>server</code> extra) exposing endpoints over HTTP, with OpenAPI docs served at <code>/api</code> and MIT licensing metadata.</li>
<li><strong>As a Docker image</strong> — for easy deployment of the server.</li>
</ul>

<p>Different segmentation models are available (e.g., <code>u2net</code>, <code>isnet-general-use</code>, and others), and GPU acceleration is supported through the optional <code>gpu</code> extra using <code>onnxruntime-gpu</code>. Model weights are downloaded automatically and cached locally.</p>

<p>Licensed under the <a href="https://github.com/danielgatis/rembg/blob/main/LICENSE.txt">MIT License</a>.</p>
<h2>Requirements</h2>

<ul>
<li>Python 3.8 or later</li>
<li>The dependencies listed in <a href="https://github.com/danielgatis/rembg/blob/main/requirements.txt"><code>requirements.txt</code></a>, which include:
<ul>
<li>numpy</li>
<li>onnxruntime (CPU) — or <code>onnxruntime-gpu</code> for GPU support via <a href="https://github.com/danielgatis/rembg/blob/main/requirements-gpu.txt"><code>requirements-gpu.txt</code></a></li>
<li>opencv-python-headless</li>
<li>pillow</li>
<li>pooch</li>
<li>pymatting</li>
<li>scipy</li>
<li>tqdm</li>
</ul></li>
</ul>

<p>Depending on the extras you install, additional packages are pulled in automatically:</p>

<ul>
<li><code>[cpu]</code> — CPU inference with <code>onnxruntime</code></li>
<li><code>[gpu]</code> — GPU inference with <code>onnxruntime-gpu</code> (requires a CUDA-capable device and appropriate NVIDIA/CUDA drivers)</li>
<li><code>[cli]</code> — command-line interface dependencies (<code>typer</code>, <code>gradio</code>, <code>fastapi</code>, <code>uvicorn</code>, etc.)</li>
</ul>

<p>All of these are installed automatically when you install rembg with <code>pip</code>, so in most cases you only need to pick the appropriate extra:</p>

<p><code>bash
pip install rembg              # base install
pip install "rembg[cpu]"       # CPU runtime
pip install "rembg[gpu]"       # GPU runtime
pip install "rembg[cli,gpu]"   # CLI + GPU
</code></p>
<h2>Installation</h2>

<p>rembg can be installed from PyPI using pip. Depending on your hardware, choose one of the following installation options:</p>

<h3>CPU</h3>

<p>To install rembg with CPU support:</p>

<p><code>bash
pip install "rembg[cpu]"
</code></p>

<h3>GPU (NVIDIA)</h3>

<p>To install rembg with NVIDIA GPU support:</p>

<p><code>bash
pip install "rembg[gpu]"
</code></p>

<h3>ROCm (AMD)</h3>

<p>To install rembg with AMD ROCm support:</p>

<p><code>bash
pip install "rembg[rocm]"
</code></p>

<h3>CLI / Server</h3>

<p>To install rembg with the command-line interface and HTTP server dependencies (which includes <a href="https://github.com/dmitryrck/TODO">gradio</a>, FastAPI, and uvicorn):</p>

<p><code>bash
pip install "rembg[cli]"
</code></p>

<p>You can also combine extras, for example:</p>

<p><code>bash
pip install "rembg[cli,gpu]"
</code></p>

<h3>Requirements</h3>

<p>rembg depends on the following core packages, which will be installed automatically:</p>

<ul>
<li>jsonschema</li>
<li>numpy</li>
<li>opencv-python-headless</li>
<li>pillow</li>
<li>pooch</li>
<li>pymatting</li>
<li>scikit-image</li>
<li>scipy</li>
<li>tqdm</li>
</ul>
<h2>Usage</h2>

<h3>As a CLI</h3>

<p>After installing rembg, you can use it from the command line:</p>

<p>```bash</p>

<h1>Remove the background from an image</h1>

<p>rembg i input.png output.png</p>

<h1>Process a whole directory of images</h1>

<p>rembg p input<em>directory output</em>directory
```</p>

<p>Run the following command to see all available commands and options:</p>

<p><code>bash
rembg --help
</code></p>

<h3>As a Python library</h3>

<p>You can also use rembg programmatically:</p>

<p>```python
from rembg import remove
from PIL import Image</p>

<p>input<em>image = Image.open("input.png")
output</em>image = remove(input<em>image)
output</em>image.save("output.png")
```</p>

<h3>As a HTTP server</h3>

<p>Rembg can also run as a server exposing a REST API (with docs available at <code>/api</code>):</p>

<p><code>bash
rembg s
</code></p>
<h2>Contributing</h2>

<p>rembg is licensed under the <a href="https://github.com/danielgatis/rembg/blob/main/LICENSE.txt">MIT License</a>, Copyright (c) 2020 Daniel Gatis.</p>

<p>Contributions are welcome! If you would like to contribute to the project:</p>

<ol>
<li>Fork the repository and create a new branch for your changes.</li>
<li>Make your changes, including tests or documentation where appropriate.</li>
<li>Submit a pull request describing the changes you have made.</li>
</ol>

<p>If you run into any issues or have questions, please open an issue on the <a href="https://github.com/danielgatis/rembg">GitHub repository</a>.</p>
<h2>License</h2>

<p>The rembg project is licensed under the MIT License.</p>

<p>Copyright (c) 2020 Daniel Gatis</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>

<p>The full license text is available in the <a href="https://github.com/danielgatis/rembg/blob/main/LICENSE.txt">LICENSE.txt</a> file in the repository.</p>

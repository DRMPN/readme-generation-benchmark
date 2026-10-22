# rembg<h2>Description</h2>

<p><code>rembg</code> removes backgrounds from images. It can be used as a command-line tool, a Python library, or an HTTP server.</p>
<h2>Requirements</h2>

<p>Install the dependencies listed in <code>requirements.txt</code>. For GPU support, use the dependencies in <code>requirements-gpu.txt</code> instead.</p>
<h2>Installation</h2>

<p>Install the package with pip:</p>

<p><code>bash
pip install rembg
</code></p>

<p>Choose an ONNX Runtime provider by installing an extra:</p>

<p><code>bash
pip install "rembg[cpu]"
pip install "rembg[gpu]"
pip install "rembg[rocm]"
</code></p>

<p>To include the CLI dependencies, add the <code>cli</code> extra. Extras can be combined:</p>

<p><code>bash
pip install "rembg[cpu,cli]"
</code></p>
<h2>Usage</h2>

<h3>Command line</h3>

<p>Remove the background from an image:</p>

<p><code>bash
rembg i input.png output.png
</code></p>

<p>Process images in a folder:</p>

<p><code>bash
rembg p input_folder output_folder
</code></p>

<h3>Python</h3>

<p><code>remove</code> accepts a Pillow image and returns the processed image:</p>

<p>```python
from PIL import Image
from rembg import remove</p>

<p>input<em>image = Image.open("input.png")
output</em>image = remove(input<em>image)
output</em>image.save("output.png")
```</p>

<p>You can also pass image bytes and write the returned bytes to a file:</p>

<p>```python
from rembg import remove</p>

<p>with open("input.png", "rb") as input<em>file:
    output = remove(input</em>file.read())</p>

<p>with open("output.png", "wb") as output<em>file:
    output</em>file.write(output)
```</p>

<h3>HTTP server</h3>

<p>Start the server, then send an image to its remove endpoint:</p>

<p><code>bash
rembg s --host 0.0.0.0 --port 7000
</code></p>

<p><code>bash
curl -F file=@input.png http://localhost:7000/api/remove -o output.png
</code></p>
<h2>Contributing</h2>
<h2>License</h2>

<p>rembg is distributed under the <a href="https://github.com/danielgatis/rembg/blob/main/LICENSE.txt">MIT License</a>.</p>

# flux<h2>Description</h2>

<!-- No information about the flux project's structure, purpose, or modules was provided in the available context. Please refer to the repository documentation or add a description of the project here. -->
<h2>Requirements</h2>

<!-- No information about the specific requirements of this project is available in the provided context. -->
<h2>Installation</h2>

<p><code>flux</code> is a Python package and can be installed from source using <code>pip</code>.</p>

<h3>Requirements</h3>

<ul>
<li>Python 3.10 or later</li>
<li><code>pip</code></li>
</ul>

<h3>Installing from source</h3>

<p>Clone the repository and install the package with <code>pip</code>:</p>

<p><code>bash
git clone &lt;repository-url&gt;
cd flux
pip install .
</code></p>

<p>The project uses <code>setuptools</code> as its build backend (with <code>setuptools_scm</code> for automatic versioning from git tags), so a standard <code>pip install .</code> will build and install the package along with its build dependencies (<code>setuptools&gt;=64</code>, <code>wheel</code>, and <code>setuptools_scm&gt;=8</code>).</p>

<h3>For development</h3>

<p>If you plan to work on the code, install the package in editable mode so your changes take effect without reinstalling:</p>

<p><code>bash
pip install -e .
</code></p>

<h3>Verifying the installation</h3>

<p>Installing the package provides a <code>flux</code> command-line entry point (defined in <code>src/flux/cli.py</code>). You can verify the installation by running:</p>

<p><code>bash
flux --help
</code></p>
<h2>Usage</h2>

<p>The repo is meant to be used with:</p>

<p><code>shell
pip install -e .[dev]
</code></p>

<p>The demos can be found in <code>demo_gr.py</code>. To try it you will need a Hugging Face token that has access to the FLUX.1 [dev] model. There are two demos, one text-to-image and one image-to-image. To try the text-to-image demo run:</p>

<p><code>shell
python demo_gr.py --name flux-schnell --mode turbo
</code></p>

<p>To try the image-to-image demo run:</p>

<p><code>shell
python demo_gr.py --name flux-dev --mode azimuthal
</code></p>

<p>To run the API demo run:</p>

<p><code>shell
python api_demo.py --name flux-schnell
</code></p>

<p>To run the API demo with flux-dev:</p>

<p><code>shell
python api_demo.py --name flux-dev
</code></p>
<h2>Contributing</h2>

<p>(This section is intentionally left blank, as no contribution guidelines or instructions specific to this repository were found in the provided context.)</p>
<h2>License</h2>

<p>The code in this repository is licensed under the <strong>Apache License, Version 2.0</strong>. You may use, reproduce, and distribute the source code in accordance with the terms of that license. A copy of the license text is included in the repository (see the <code>LICENSE</code> file).</p>

<p>Please note that the <strong>model weights</strong> are <strong>not</strong> covered by the Apache License. The weights are provided under the separate <strong>FLUX.1 [dev] Non-Commercial License</strong>, which restricts their use to non-commercial purposes. If you intend to use the model weights, make sure you review and comply with the terms of that license.</p>

<p>In summary:</p>

<ul>
<li><strong>Code</strong>: Apache License, Version 2.0</li>
<li><strong>Model weights</strong>: FLUX.1 [dev] Non-Commercial License (non-commercial use only)</li>
</ul>

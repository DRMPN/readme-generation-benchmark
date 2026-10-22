# face_recognition<h2>Description</h2>

<p>I could not find enough information in the provided context to write this section. The context contains only Sphinx configuration (<code>conf.py</code>) and a Makefile help listing. The project description lives in <code>../README.rst</code>, which is referenced but not included. The only related text is a placeholder ("One line description of project.") in the Texinfo settings, which doesn't describe the project.</p>
<h2>Requirements</h2>

<p>The build system requires <code>setuptools</code> and <code>wheel</code>, as declared in <code>pyproject.toml</code>:</p>

<p><code>toml
[build-system]
requires = ["setuptools", "wheel"]
</code></p>

<p>The provided context does not list the runtime dependencies or supported Python versions, so this section does not cover them.</p>
<h2>Installation</h2>

<p>The repository includes a <code>Makefile</code> target that installs the package into the active Python environment's <code>site-packages</code>:</p>

<p><code>bash
make install
</code></p>

<p>This target removes build artifacts with <code>clean</code> and then runs <code>python3 setup.py install</code>.</p>

<p>To build distributable packages instead of installing directly, use:</p>

<p><code>bash
make dist
</code></p>

<p>This creates a source distribution and a wheel in the <code>dist/</code> directory.</p>
<h2>Usage</h2>

<p>The provided context doesn't include the usage information for this project. It only contains Sphinx documentation build settings (a Makefile help snippet and <code>conf.py</code> options) and <code>.. include::</code> directives pointing to <code>../README.rst</code> and <code>../CONTRIBUTING.rst</code>. Neither included file's contents are shown, so this section is left blank.</p>
<h2>Contributing</h2>

<p>Contribution guidelines are in <code>CONTRIBUTING.rst</code> at the root of the repository. The project's documentation includes this file.</p>
<h2>License</h2>

<p>This project is licensed under the MIT License. Copyright (c) 2021, Adam Geitgey.</p>

<p>The full license text is included in the repository's <code>LICENSE</code> file.</p>

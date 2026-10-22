# mkdocs<h2>Description</h2>

<p>MkDocs is a fast, simple and downright gorgeous static site generator that's geared towards building project documentation. Documentation source files are written in Markdown, and configured with a single YAML configuration file. It is licensed under the BSD-2-Clause license and requires Python 3.8+.</p>

<p>Key features include:</p>

<ul>
<li><strong>Markdown-based authoring</strong> — write your documentation in plain Markdown files, and MkDocs converts them into a complete static documentation website.</li>
<li><strong>Theming</strong> — ships with a built-in theme (the <code>mkdocs</code> theme) and supports custom themes for full control over the look and feel of your site.</li>
<li><strong>Plugins</strong> — extend MkDocs's behavior with a plugin system (e.g., the built-in <code>search</code> plugin).</li>
<li><strong>Live-reload development server</strong> — preview your documentation locally with automatic rebuilding as you save changes.</li>
<li><strong>Configuration validation</strong> — your <code>mkdocs.yml</code> settings (such as <code>site_url</code>, <code>site_description</code>, <code>theme</code>, navigation-related options, etc.) are validated with helpful error messages.</li>
<li><strong>Production/Stable status</strong> — a mature project intended for developers and widely used for project documentation.</li>
</ul>

<p>MkDocs works on any operating system with Python installed, and runs on both CPython and PyPy.</p>
<h2>Requirements</h2>

<p>MkDocs requires <strong>Python 3.8 or newer</strong> (it supports CPython and PyPy) along with the following Python packages, which are installed automatically when you install MkDocs:</p>

<ul>
<li><code>click</code></li>
<li><code>Jinja2</code></li>
<li><code>markdown</code></li>
<li><code>markupsafe</code></li>
<li><code>mergedeep</code></li>
<li><code>packaging</code></li>
<li><code>pathspec</code></li>
<li><code>PyYAML</code></li>
<li><code>pyyaml-env-tag</code></li>
<li><code>watchdog</code></li>
<li><code>ghp-import</code></li>
<li><code>importlib-metadata</code> (Python &lt; 3.10 only)</li>
</ul>

<p>The complete and authoritative list of dependencies and supported Python versions is defined in the project's <code>pyproject.toml</code> file in the <a href="https://github.com/mkdocs/mkdocs">mkdocs repository</a>.</p>
<h2>Installation</h2>

<p>MkDocs requires Python 3.x and can be installed with pip:</p>

<p><code>bash
python -m pip install mkdocs
</code></p>

<p>Note: Installation using <code>setup.py</code> is no longer supported. To install from a local copy of the source code, use:</p>

<p><code>bash
python -m pip install .
</code></p>
<h2>Usage</h2>

<p>MkDocs provides a simple command-line interface to create, preview, and build your documentation project.</p>

<h3>Creating a new project</h3>

<p>To scaffold a new documentation project, run:</p>

<p><code>bash
mkdocs new my-project
</code></p>

<p>This creates a <code>my-project</code> directory containing a <code>mkdocs.yml</code> configuration file and a <code>docs/</code> folder with an initial <code>index.md</code> page.</p>

<h3>Previewing your documentation</h3>

<p>To start the built-in development server with live reloading:</p>

<p><code>bash
mkdocs serve
</code></p>

<p>This builds your documentation and serves it locally at <code>localhost:8000</code> (default). Any changes you make to your docs or configuration are automatically rebuilt and reloaded in the browser. Useful options include:</p>

<ul>
<li><code>--dev-addr</code> — IP address and port to serve documentation locally (default: <code>localhost:8000</code>)</li>
<li><code>--no-livereload</code> — disable the live reloading in the development server</li>
<li><code>--dirtyreload</code> — only re-build files that have changed</li>
<li><code>--open</code> / <code>-o</code> — open the website in a web browser after the initial build finishes</li>
</ul>

<h3>Building your documentation</h3>

<p>To build a static site from your documentation:</p>

<p><code>bash
mkdocs build
</code></p>

<p>The generated static site is written to the output directory (by default <code>site/</code>). Useful options include:</p>

<ul>
<li><code>--clean</code> — remove old files from the site directory before building (this is the default)</li>
<li><code>--site-dir</code> — the directory to output the result of the documentation build</li>
<li><code>--config</code> — provide a specific MkDocs config file, or <code>-</code> to read the configuration from stdin</li>
<li><code>--strict</code> — enable strict mode, which causes MkDocs to abort the build on any warnings</li>
<li><code>--theme</code> — the theme to use when building your documentation</li>
</ul>

<p>Run <code>mkdocs --help</code> or <code>mkdocs &lt;command&gt; --help</code> to see all available commands and options.</p>
<h2>Contributing</h2>

<p>Contributions to MkDocs are welcome! Whether you want to report a bug, suggest a feature, or submit a code change, here's how to get started:</p>

<h3>Reporting Issues</h3>

<p>If you find a bug or have a feature request, please open an issue on the <a href="https://github.com/mkdocs/mkdocs/issues">GitHub issue tracker</a>. Before opening a new issue, please search existing issues to avoid duplicates.</p>

<h3>Setting Up a Development Environment</h3>

<p>To work on MkDocs itself, clone the repository and install the project in editable mode along with its development dependencies:</p>

<p><code>bash
git clone https://github.com/mkdocs/mkdocs.git
cd mkdocs
pip install -e . -r requirements/requirements-project.txt
</code></p>

<h3>Running the Tests</h3>

<p>MkDocs has a comprehensive test suite. You can run the tests locally to verify your changes:</p>

<p><code>bash
pytest mkdocs
</code></p>

<h3>Submitting Changes</h3>

<ol>
<li>Fork the repository and create a new branch for your work.</li>
<li>Make your changes, and add tests where appropriate.</li>
<li>Ensure the test suite passes and any documentation is updated.</li>
<li>Open a pull request against the <code>main</code> branch of the <a href="https://github.com/mkdocs/mkdocs">MkDocs repository</a>.</li>
</ol>

<h3>Code of Conduct</h3>

<p>Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.</p>
<h2>License</h2>

<p>MkDocs is released under the BSD 2-Clause License.</p>

<p>Copyright © 2015, Waylan Limberg. All rights reserved.</p>

<p>Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:</p>

<ol>
<li>Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.</li>
<li>Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.</li>
<li>Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.</li>
</ol>

<p>Note that some bundled dependencies (such as the ReadTheDocs theme used for styling, and other vendored assets) carry their own licenses — for example, portions of the shipped theme CSS are distributed under the MIT license with their respective copyright holders. Please refer to the license headers in the individual files for details.</p>

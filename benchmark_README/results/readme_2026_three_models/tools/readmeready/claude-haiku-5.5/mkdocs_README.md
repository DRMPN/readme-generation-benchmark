# mkdocs<h2>Description</h2>

<p>MkDocs is a tool for building project documentation with Markdown. It is licensed under BSD-2-Clause and was created by Tom Christie.</p>

<p>The project is configured through settings such as:</p>

<ul>
<li><strong><code>site_url</code></strong>: the full URL where the documentation will be hosted.</li>
<li><strong><code>site_description</code> / <code>site_author</code></strong>: values added to the HTML meta tags.</li>
<li><strong><code>theme</code></strong>: the MkDocs theme used for the documentation, defaulting to <code>mkdocs</code>.</li>
<li><strong><code>plugins</code></strong>: extensions such as <code>search</code>, <code>redirects</code>, <code>autorefs</code>, <code>literate-nav</code>, and <code>mkdocstrings</code>, which can generate API reference pages from Python docstrings.</li>
<li><strong><code>hooks</code></strong>: custom Python scripts that run during the build.</li>
<li><strong><code>draft_docs</code> / <code>not_in_nav</code></strong>: patterns for marking pages as drafts or for pages that are intentionally left out of the navigation.</li>
</ul>

<p>The package supports Python 3.8 through 3.12.</p>
<h2>Requirements</h2>

<p>MkDocs supports Python 3.8, 3.9, 3.10, 3.11, and 3.12, on CPython and PyPy.</p>
<h2>Installation</h2>

<p>Installing with <code>setup.py</code> directly is no longer supported. From the root of the repository, install the project with pip:</p>

<p><code>bash
python -m pip install .
</code></p>

<p>pip installs the project's runtime dependencies along with it. These include <code>packaging</code>, <code>mergedeep</code>, <code>pathspec</code>, <code>mkdocs-get-deps</code>, and <code>babel</code>. On Windows, <code>colorama</code> is also installed.</p>
<h2>Usage</h2>

<p>The command-line interface provides options for building and serving the documentation. The options below are described by their help text in the source code.</p>

<p><strong>Building the documentation</strong></p>

<ul>
<li>Remove old files from the output directory before building. This is the default.</li>
<li>Provide a specific MkDocs configuration. This can be a file name, or <code>-</code> to read the configuration from stdin.</li>
<li>Set the directory where the built documentation is written.</li>
<li>Use directory URLs when building pages. This is the default.</li>
<li>Enable strict mode, which makes the build abort on any warning.</li>
<li>Choose the theme to use. Available theme names are read from the installed themes.</li>
</ul>

<p><strong>Serving the documentation locally</strong></p>

<ul>
<li>Set the IP address and port for the development server. The default is <code>localhost:8000</code>.</li>
<li>Open the website in a web browser after the initial build finishes.</li>
<li>Enable live reloading in the development server. This is the default.</li>
<li>Disable live reloading in the development server.</li>
<li>Only rebuild files that have changed.</li>
<li>Remove old files before building. This is the counterpart of the clean-build option above.</li>
</ul>

<p>Run the command with <code>--help</code> to see the exact option names for your installed version.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project includes third-party components that are distributed under their own license terms. The license notices for these components are:</p>

<ul>
<li><strong>sphinx<em>rtd</em>theme</strong> (versions 1.0.0 and 1.2.0): licensed under the <strong>MIT license</strong>.</li>
<li><strong>Copyright © 2014-present, Tom Christie.</strong> The bundled code carries a BSD-style notice permitting redistribution and use in source and binary forms, with or without modification, provided that the copyright notice, the list of conditions, and the disclaimer are retained in source redistributions and reproduced in binary redistributions.</li>
<li><strong>Copyright (c) 2015, Waylan Limberg.</strong> This notice is under a BSD 3-clause style license. It permits redistribution and use in source and binary forms, with or without modification, subject to the following:
<ol>
<li>Source redistributions must retain the copyright notice and the list of conditions.</li>
<li>Binary redistributions must reproduce the copyright notice, the list of conditions, and the disclaimer in the documentation or other materials provided with the distribution.</li>
<li>The name of the copyright holder and its contributors may not be used to endorse or promote products derived from this software without specific prior written permission.</li>
</ol></li>
</ul>

<p>Refer to the license notices in the corresponding source files for the complete license text.</p>

# flask<h2>Description</h2>

<p>Flask is a Python web application framework. Its core runtime dependencies are:</p>

<ul>
<li><strong>Werkzeug</strong> (&gt;= 3.1.0)</li>
<li><strong>Jinja2</strong> (&gt;= 3.1.2)</li>
<li><strong>Click</strong> (&gt;= 8.1.3)</li>
<li><strong>Blinker</strong> (&gt;= 1.9.0)</li>
<li><strong>itsdangerous</strong> (&gt;= 2.2.0)</li>
<li><strong>MarkupSafe</strong> (&gt;= 2.1.1)</li>
</ul>

<p>It also provides two optional extras:</p>

<ul>
<li><strong><code>async</code></strong>: installs <code>asgiref</code> (&gt;= 3.2) to support async views.</li>
<li><strong><code>dotenv</code></strong>: installs <code>python-dotenv</code> to load environment variables from <code>.env</code> files.</li>
</ul>

<p>Development, testing, documentation, and typing tools are grouped separately as development dependencies (<code>dev</code>, <code>docs</code>, <code>docs-auto</code>, <code>pre-commit</code>, <code>tests</code>, <code>typing</code>, and <code>gha-update</code>).</p>
<h2>Requirements</h2>

<p>Flask requires the following packages, which are installed automatically with it:</p>

<ul>
<li><code>blinker</code> &gt;= 1.9.0</li>
<li><code>click</code> &gt;= 8.1.3</li>
<li><code>itsdangerous</code> &gt;= 2.2.0</li>
<li><code>jinja2</code> &gt;= 3.1.2</li>
<li><code>markupsafe</code> &gt;= 2.1.1</li>
<li><code>werkzeug</code> &gt;= 3.1.0</li>
</ul>

<p>Flask also has two optional extras:</p>

<ul>
<li><strong>async</strong>: installs <code>asgiref</code> (&gt;= 3.2) to support async views.</li>
<li><strong>dotenv</strong>: installs <code>python-dotenv</code> to load environment variables from <code>.env</code> and <code>.flaskenv</code> files.</li>
</ul>

<p>To install Flask with an extra, use:</p>

<p><code>bash
pip install flask[async]
pip install flask[dotenv]
</code></p>
<h2>Installation</h2>

<p>Install Flask with pip:</p>

<p><code>bash
pip install flask
</code></p>

<p>Flask installs these required dependencies automatically:</p>

<ul>
<li><code>blinker</code> (&gt;= 1.9.0)</li>
<li><code>click</code> (&gt;= 8.1.3)</li>
<li><code>itsdangerous</code> (&gt;= 2.2.0)</li>
<li><code>jinja2</code> (&gt;= 3.1.2)</li>
<li><code>markupsafe</code> (&gt;= 2.1.1)</li>
<li><code>werkzeug</code> (&gt;= 3.1.0)</li>
</ul>

<p>Flask also has two optional extras:</p>

<ul>
<li><p><strong><code>async</code></strong> adds <code>asgiref</code> (&gt;= 3.2) for async view support:</p>

<p><code>bash
pip install "flask[async]"
</code></p></li>
<li><p><strong><code>dotenv</code></strong> adds <code>python-dotenv</code> for loading environment variables from <code>.env</code> files:</p>

<p><code>bash
pip install "flask[dotenv]"
</code></p></li>
</ul>

<p>You can install both extras at once:</p>

<p><code>bash
pip install "flask[async,dotenv]"
</code></p>
<h2>Usage</h2>

<p>Flask declares two optional extras that you can install alongside the core package:</p>

<ul>
<li><code>async</code> installs <code>asgiref</code> (version 3.2 or later).</li>
<li><code>dotenv</code> installs <code>python-dotenv</code>.</li>
</ul>

<p><code>bash
pip install "flask[async]"
pip install "flask[dotenv]"
</code></p>
<h2>Contributing</h2>

<p>Contributions are welcome. For the many ways to get involved, including reporting issues, requesting features, asking or answering questions, and submitting pull requests, see the <a href="https://palletsprojects.com/contributing/">Pallets contributing documentation</a>.</p>
<h2>License</h2>

<p>Flask is licensed under the BSD-3-Clause License. Copyright 2010 Pallets.</p>

<p>Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:</p>

<ol>
<li><p>Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.</p></li>
<li><p>Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.</p></li>
<li><p>Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.</p></li>
</ol>

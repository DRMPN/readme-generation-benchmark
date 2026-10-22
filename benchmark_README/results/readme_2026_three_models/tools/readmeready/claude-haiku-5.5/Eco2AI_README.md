# Eco2AI<h2>Description</h2>

<p>Eco2AI is a Python package (<code>eco2ai</code>) for working with the energy use and carbon footprint of AI and machine learning workloads. It is distributed as a standard Python package with a <code>setup.py</code> file.</p>

<p>The package depends on:</p>

<ul>
<li><strong>APScheduler</strong> for scheduling periodic tasks.</li>
<li><strong>pynvml</strong> (5.6.2 or newer) for querying NVIDIA GPU information.</li>
<li><strong>psutil</strong> for system resource information.</li>
<li><strong>py-cpuinfo</strong> for CPU details.</li>
</ul>

<p>It also ships three data files with the package: <code>cpu_names.csv</code>, <code>config.txt</code>, and <code>carbon_index.csv</code>.</p>

<p>The project is authored by Vladimir Lazarev, Nikita Zakharenko, Alexey Korovin, Semyon Budyonny, and Leonid Zhukov, and is licensed under the Apache License, Version 2.0.</p>
<h2>Requirements</h2>

<p>Eco2AI installs the following Python packages automatically through <code>setup.py</code>:</p>

<ul>
<li><code>APScheduler</code></li>
<li><code>pynvml&gt;=5.6.2</code></li>
<li><code>psutil</code></li>
<li><code>py-cpuinfo</code></li>
</ul>
<h2>Installation</h2>

<p>Eco2AI is packaged with <code>setuptools</code> and declares the following runtime dependencies, which are installed automatically:</p>

<ul>
<li><code>APScheduler</code></li>
<li><code>pynvml</code> (version 5.6.2 or newer)</li>
<li><code>psutil</code></li>
<li><code>py-cpuinfo</code></li>
</ul>

<p>To install from a local copy of the repository, run the following from the project root:</p>

<p><code>bash
pip install .
</code></p>

<p>The package also ships data files used at runtime (<code>data/cpu_names.csv</code>, <code>data/config.txt</code>, and <code>data/carbon_index.csv</code>).</p>
<h2>Usage</h2>

<p>The provided context does not contain enough information to write this section. It includes license text, a parameter description, and dependency lock-file entries, but no usage examples or instructions.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the Apache License, Version 2.0. You can use, reproduce, modify, and distribute the software, including in derivative works, provided you follow the license conditions. These include giving other recipients a copy of the license, marking modified files as changed, and keeping the relevant copyright, patent, trademark, and attribution notices.</p>

<p>The software is provided "AS IS," without warranties or conditions of any kind. See the full license text in the repository's <code>LICENSE</code> file for the complete terms.</p>

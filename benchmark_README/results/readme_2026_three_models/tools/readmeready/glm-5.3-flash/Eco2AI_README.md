# Eco2AI<h2>Description</h2>

<p>Eco2AI is a Python library for estimating the energy consumption and CO2 emissions produced by machine learning workloads. It monitors the hardware used during model training or inference and translates the consumed energy into an equivalent carbon footprint, taking into account the regional carbon index where the computations are performed.</p>

<p>Under the hood, Eco2AI gathers hardware information (CPU model, GPU state, and other system metrics) using libraries such as <code>pynvml</code>, <code>psutil</code>, and <code>py-cpuinfo</code>, and periodically collects consumption data with the help of <code>APScheduler</code>. The package ships with supporting data files — a CPU names database (<code>data/cpu_names.csv</code>), a regional carbon index table (<code>data/carbon_index.csv</code>), and a configuration file (<code>data/config.txt</code>) — which are used to compute accurate energy and emissions estimates.</p>

<p>The project is licensed under the Apache License 2.0 and is developed by Vladimir Lazarev, Nikita Zakharenko, Alexey Korovin, Semyon Budyonny, and Leonid Zhukov.</p>
<h2>Requirements</h2>

<p>Eco2AI requires the following dependencies to be installed:</p>

<ul>
<li><strong>APScheduler</strong> – used for scheduling periodic tracking tasks</li>
<li><strong>pynvml>=5.6.2</strong> – NVIDIA Management Library Python bindings, used to collect GPU metrics</li>
<li><strong>psutil</strong> – used for retrieving system and CPU utilization information</li>
<li><strong>py-cpuinfo</strong> – used to gather CPU model details</li>
</ul>

<p>You can install all of these dependencies automatically by installing the package via pip:</p>

<p><code>bash
pip install eco2ai
</code></p>

<p>This will install the package together with its dependencies, as well as the required data files (<code>cpu_names.csv</code>, <code>config.txt</code>, and <code>carbon_index.csv</code>) bundled with the <code>eco2ai</code> package.</p>
<h2>Installation</h2>

<p>Eco2AI is available as a Python package and can be installed directly with <code>pip</code>:</p>

<p><code>bash
pip install eco2ai
</code></p>

<p>This will install the <code>eco2ai</code> package along with all of its required dependencies:</p>

<ul>
<li><code>APScheduler</code></li>
<li><code>pynvml&gt;=5.6.2</code> (NVIDIA Management Library Python bindings, used for GPU monitoring)</li>
<li><code>psutil</code> (system and process utilities)</li>
<li><code>py-cpuinfo</code> (CPU information retrieval)</li>
</ul>

<p>The package also ships with the data files it needs to operate, including the CPU names database, configuration file, and carbon index data.</p>

<h3>Installing from source</h3>

<p>Alternatively, you can install Eco2AI directly from the source code of this repository:</p>

<p><code>bash
git clone https://github.com/sustainable-computing-io/eco2ai.git
cd eco2ai
pip install .
</code></p>

<h3>Requirements</h3>

<ul>
<li>A Python environment (Python 3.x)</li>
<li>NVIDIA GPU drivers (required for GPU-related tracking, since Eco2AI relies on <code>pynvml</code> to access GPU metrics)</li>
</ul>
<h2>Usage</h2>

<p>Eco2AI tracks the electricity consumption and corresponding CO2 emissions of your Python code with a simple tracker interface: create a tracker, call <code>start()</code> before your workload, and call <code>stop()</code> afterwards.</p>

<h3>Basic example</h3>

<p>```python
from eco2ai import EmissionTracker</p>

<p>tracker = EmissionTracker(
    project<em>name="MNIST classification",
    experiment</em>description="Simple CNN training",
    file<em>name="results.csv",
    measure</em>period=10,
)</p>

<p>tracker.start()</p>

<h1>... train your model here ...</h1>

<p>tracker.stop()
```</p>

<p>Once <code>tracker.stop()</code> is called, the measured energy consumption and CO2 emissions are written to the file specified via <code>file_name</code>.</p>

<h3>Tracker parameters</h3>

<p>The <code>EmissionTracker</code> constructor accepts the following parameters:</p>

<p>| Parameter | Type | Description | Default |
|---|---|---|---|
| <code>project_name</code> | <code>str</code> | Specified by user project name. | <code>None</code> |
| <code>experiment_description</code> | <code>str</code> | Specified by user experiment description. | <code>None</code> |
| <code>file_name</code> | <code>str</code> | Name of file to save the results of calculations. | <code>None</code> |
| <code>measure_period</code> | <code>float</code> | Period of power consumption measurements in seconds. The larger the period, the more time between measurements. | <code>10</code> |
| <code>emission_level</code> | <code>float</code> | The mass of CO2 in kilos, which is produced per every MWh of consumed energy. | <code>None</code> |
| <code>alpha_2_code</code> | <code>str</code> | User specified country code. You can search for your country code here: <a href="https://www.iban.com/country-codes">https://www.iban.com/country-codes</a> | <code>None</code> |
| <code>region</code> | <code>str</code> | User specified country region/state/district. | <code>None</code> |</p>

<h3>Specifying the emission level or location</h3>

<p>If you know the exact emission level of your energy source, you can pass it directly:</p>

<p><code>python
tracker = EmissionTracker(
    project_name="MNIST classification",
    emission_level=350.0,  # kg of CO2 per MWh
)
</code></p>

<p>Otherwise, you can specify your location, and emissions will be estimated for your country (and region, where applicable):</p>

<p><code>python
tracker = EmissionTracker(
    project_name="MNIST classification",
    alpha_2_code="RU",
    region="Moscow",
)
</code></p>

<p>The <code>alpha_2_code</code> parameter must be a two-letter country code from the <a href="https://www.iban.com/country-codes">ISO country codes list</a>.</p>
<h2>Contributing</h2>

<p>Contributions to Eco2AI are welcome. Since the project is distributed under the Apache License 2.0, any work you submit for inclusion in the project is licensed under the same terms. This means that by contributing code, documentation, or other materials, you grant the project maintainers a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute your contributions as part of the Work, in both source and object form.</p>

<p>If you would like to contribute, you can get involved by:</p>

<ul>
<li>Submitting bug reports or feature requests through the project's issue tracking system.</li>
<li>Submitting patches or improvements via the project's source code control system.</li>
</ul>

<p>Please note that only work that is intentionally submitted to the project maintainers for inclusion in Eco2AI is considered a contribution — communication that is explicitly marked as "Not a Contribution" by the copyright owner is excluded.</p>
<h2>License</h2>

<p>Eco2AI is licensed under the <a href="http://www.apache.org/licenses/">Apache License 2.0</a>.</p>

<p>You are free to use, reproduce, and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications, and in Source or Object form, provided that you meet the following conditions:</p>

<ul>
<li>You must give any other recipients of the Work or Derivative Works a copy of this License;</li>
<li>You must cause any modified files to carry prominent notices stating that you changed the files;</li>
<li>You must retain, in the Source form of any Derivative Works that you distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work, excluding those notices that do not pertain to any part of the Derivative Works.</li>
</ul>

<p>The Work is provided on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with your exercise of permissions under this License.</p>

<p>For the full terms and conditions, see the Apache License, Version 2.0: http://www.apache.org/licenses/</p>
<h2>Description</h2>

<p><strong>Eco2AI</strong> is a Python library for tracking the equivalent CO2 emissions produced by running your code (in particular, ML/DL model training). The library monitors the power consumption of the CPU and GPU devices during the program runtime and, based on the consumed energy and the carbon intensity of the regional power grid, calculates the equivalent amount of CO2 emissions.</p>

<p>All measurements are performed in real time and are summed up and recorded to a <code>.csv</code> log file, so after each session you get cumulative statistics on the carbon footprint of your computations, including device usage, power consumption, energy consumed, and CO2 emissions.</p>

<p>The library is designed to be as simple to use as possible: once installed, you just import <code>eco2ai</code> and add a single <code>track()</code> call before the training starts — from that moment on, every run of the script automatically appends its energy and emissions statistics to the log file.</p>

<p>Key features:</p>

<ul>
<li>Tracks power consumption of CPU and NVIDIA GPU devices during runtime</li>
<li>Calculates equivalent CO2 emissions using the carbon intensity of the region where the code is executed</li>
<li>Records the results of every tracking session to a <code>.csv</code> log file</li>
<li>Requires only a couple of lines of code to start tracking</li>
</ul>

<p>The package is distributed under the Apache License 2.0.</p>
<h2>Requirements</h2>

<p>Eco2AI has a small set of external dependencies, all of which are declared in the project's <code>setup.py</code>. They are installed automatically together with the package, for example via <code>pip install eco2ai</code>.</p>

<h3>Python dependencies</h3>

<ul>
<li><strong>APScheduler</strong> — used to schedule periodic measurements of power consumption during the tracked session;</li>
<li><strong>pynvml (&gt;= 5.6.2)</strong> — Python bindings for the NVIDIA Management Library, used to collect GPU telemetry (power draw, utilization, etc.);</li>
<li><strong>psutil</strong> — cross-platform library used to retrieve CPU utilization and other system-level information;</li>
<li><strong>py-cpuinfo</strong> — used to obtain detailed CPU model information.</li>
</ul>

<p>An equivalent <code>requirements.txt</code>-style listing:</p>

<p><code>text
APScheduler
pynvml&gt;=5.6.2
psutil
py-cpuinfo
</code></p>

<h3>Hardware notes</h3>

<ul>
<li>GPU-level energy consumption tracking relies on <code>pynvml</code>, which requires an <strong>NVIDIA GPU with installed NVIDIA drivers</strong> (the <code>nvidia-smi</code> utility) to be available on the machine;</li>
<li>CPU-level tracking works through <code>psutil</code> / <code>py-cpuinfo</code> and does not require any additional hardware.</li>
</ul>

<p>The package also bundles the data files it needs at runtime (<code>data/cpu_names.csv</code>, <code>data/config.txt</code>, and <code>data/carbon_index.csv</code>), so no extra configuration is required after installation.</p>
<h2>Installation</h2>

<p>Eco2AI is distributed as a standard Python package built with <code>setuptools</code> (see the <code>setup.py</code> in the repository root). It can be installed either from the Python Package Index or directly from the source code of this repository.</p>

<h3>Install with pip</h3>

<p>The package can be installed directly using <code>pip</code>:</p>

<p><code>bash
pip install eco2ai
</code></p>

<h3>Install from source</h3>

<p>To install the latest version from the source code, clone this repository, change into the project directory, and run the provided setup script:</p>

<p><code>bash
git clone &lt;this-repository&gt;
cd eco2ai
python setup.py install
</code></p>

<h3>Dependencies</h3>

<p>The following dependencies are declared in <code>setup.py</code> and are installed automatically together with <code>eco2ai</code>:</p>

<ul>
<li><code>APScheduler</code></li>
<li><code>pynvml&gt;=5.6.2</code></li>
<li><code>psutil</code></li>
<li><code>py-cpuinfo</code></li>
</ul>

<p>Along with the Python code, the distribution also bundles the following data files (declared via <code>package_data</code> and <code>include_package_data</code> in <code>setup.py</code>), which are installed together with the package:</p>

<ul>
<li><code>eco2ai/data/cpu_names.csv</code></li>
<li><code>eco2ai/data/config.txt</code></li>
<li><code>eco2ai/data/carbon_index.csv</code></li>
</ul>
<h2>Usage</h2>

<p>Eco2AI lets you track the energy consumption and CO2 emissions of your ML training with just a few lines of code. The main entry point is the <code>Tracker</code> class: create a tracker instance, call <code>start()</code> right before your training process begins, and call <code>stop()</code> when the training is finished. The measured energy consumption and corresponding CO2 emissions are saved to a CSV file.</p>

<p>```python
from eco2ai import Tracker</p>

<p>tracker = Tracker(
    project<em>name="My</em>project",
    experiment<em>description="training the model",
    file</em>name="db_results.csv"
)</p>

<p>tracker.start()</p>

<h1>your training process</h1>

<p>tracker.stop()
```</p>

<p>The <code>Tracker</code> constructor accepts the following parameters:</p>

<p>| Parameter | Description |
|-----------|-------------|
| <code>project_name</code> | Specified by user project name. The default is <code>None</code>. |
| <code>experiment_description</code> | Specified by user experiment description. The default is <code>None</code>. |
| <code>file_name</code> | Name of file to save the results of calculations. The default is <code>None</code>. |
| <code>measure_period</code> | Period of power consumption measurements in seconds. The more period the more time between measurements. The default is <code>10</code>. |
| <code>emission_level</code> | The mass of CO2 in kilos, which is produced per every MWh of consumed energy. The default is <code>None</code>. |
| <code>alpha_2_code</code> | User specified country code. You can search for your country code <a href="https://www.iban.com/country-codes">here</a>. Default is <code>None</code>. |
| <code>region</code> | User specified country region/state/district. |</p>

<p>If <code>emission_level</code> is not set explicitly, it is calculated automatically based on the <code>alpha_2_code</code> and <code>region</code> parameters.</p>

<p>The tracker can also be applied as a decorator:</p>

<p>```python
import eco2ai</p>

<p>@eco2ai.track(
    project<em>name="My</em>project",
    experiment<em>description="training the model",
    file</em>name="db<em>results.csv"
)
def train</em>func():
    ...
```</p>
<h2>Contributing</h2>

<p>Thank you for considering contributing to <strong>Eco2AI</strong>!</p>

<p>Eco2AI is licensed under the <a href="http://www.apache.org/licenses/LICENSE-2.0">Apache License, Version 2.0</a>, with copyright held by Vladimir Lazarev, Nikita Zakharenko, Semyon Budyonny, and Leonid Zhukov.</p>

<h3>What counts as a Contribution</h3>

<p>Under the project's license, a "Contribution" is any work of authorship — including the original version of the Work and any modifications or additions to it, or Derivative Works thereof — that is intentionally submitted to the Licensor for inclusion in the Work by the copyright owner or by an individual or legal entity authorized to submit on their behalf.</p>

<p>"Submitted" means any form of electronic, verbal, or written communication sent to the Licensor or its representatives for the purpose of discussing and improving the Work, including communication via:</p>

<ul>
<li>source code control systems (e.g., pull requests),</li>
<li>issue tracking systems.</li>
</ul>

<p>If you do not want a particular communication to be treated as a Contribution, please conspicuously mark or otherwise designate it in writing as "Not a Contribution."</p>

<h3>Licensing of your contributions</h3>

<p>By submitting a Contribution, each Contributor grants users of the Work a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare Derivative Works of, publicly display, publicly perform, sublicense, and distribute the Work and such Derivative Works in Source or Object form.</p>

<h3>Adding the license notice to new files</h3>

<p>When adding new source files to the project, please include the standard Apache License header at the top of the file, in the appropriate comment syntax for the file format, along with a file/class name and a description of its purpose:</p>

<p>```
Copyright (с) Vladimir Lazarev, Nikita Zakharenko, Semyon Budyonny, leonid zhukov</p>

<p>Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at</p>

<pre><code>http://www.apache.org/licenses/LICENSE-2.0
</code></pre>

<p>Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```</p>
<h2>License</h2>

<p>Eco2AI is released under the <a href="http://www.apache.org/licenses/">Apache License 2.0</a>.</p>

<p>Under this license, you are free to use, reproduce, and distribute the Work or Derivative Works of this project in any medium, with or without modifications, and in Source or Object form, provided that you:</p>

<ul>
<li>Give any other recipients of the Work or Derivative Works a copy of the License;</li>
<li>Cause any modified files to carry prominent notices stating that you changed the files;</li>
<li>Retain, in the Source form of any Derivative Works that you distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work (excluding notices that do not pertain to any part of the Derivative Works).</li>
</ul>

<p>Note that the License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work.</p>

<p>The software is provided on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. The full text of the license can be found in the <code>LICENSE</code> file at the root of the repository.</p>

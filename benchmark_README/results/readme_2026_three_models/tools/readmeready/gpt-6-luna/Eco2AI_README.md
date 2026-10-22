# Eco2AI<h2>Description</h2>

<p>Eco2AI is a Python library for estimating the energy consumption and carbon emissions of computational workloads. It monitors a machine’s hardware while a workload runs and records the resulting measurements, helping developers assess the environmental impact of their computations.</p>
<h2>Requirements</h2>

<p>Eco2AI depends on the following Python packages:</p>

<ul>
<li><code>APScheduler</code></li>
<li><code>pynvml</code> (<code>&gt;=5.6.2</code>)</li>
<li><code>psutil</code></li>
<li><code>py-cpuinfo</code></li>
</ul>
<h2>Installation</h2>

<p>Install Eco2AI from PyPI:</p>

<p><code>bash
pip install eco2ai
</code></p>

<p>The package installation includes its Python dependencies: APScheduler, <code>pynvml</code>, <code>psutil</code>, and <code>py-cpuinfo</code>.</p>
<h2>Usage</h2>

<p>Create a <code>Tracker</code>, start it before the work you want to measure, and stop it when that work is complete. For example:</p>

<p>```python
import eco2ai</p>

<p>tracker = eco2ai.Tracker(
    project<em>name="example-project",
    experiment</em>description="Example run",
    file<em>name="emissions.csv",
    measure</em>period=10,
    alpha<em>2</em>code="US",
)</p>

<p>tracker.start()</p>

<h1>Run the code you want to measure.</h1>

<p>tracker.stop()
```</p>

<p><code>measure_period</code> sets the interval between power-consumption measurements, in seconds. You can also provide <code>region</code> to specify a country subdivision, or <code>emission_level</code> to supply the CO₂ emissions per MWh of consumed energy.</p>
<p>I’ll inspect the repository’s existing contribution guidance and project metadata, then draft only what the codebase supports.</p>

<h2>Contributing</h2>

<p>Contributions are works submitted to the project for inclusion, including modifications and additions. A submission may be made electronically, verbally, or in writing through channels used to discuss and improve the project; material designated <strong>“Not a Contribution”</strong> is excluded.</p>

<p>Contributions are subject to the project’s Apache License, Version 2.0. Under its terms, contributors grant a perpetual, worldwide, non-exclusive, royalty-free, irrevocable copyright license to reproduce, modify, display, perform, sublicense, and distribute their contributions.</p>
<h2>License</h2>

<p>Eco2AI is distributed under the Apache License, Version 2.0. See the <a href="http://www.apache.org/licenses/">license text</a> for its terms.</p>

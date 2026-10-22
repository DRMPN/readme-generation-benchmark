# eco4cast<h2>Description</h2>

<p>eco4cast is a project for ecological forecasting. The repository contains a Jupyter notebook that walks through the setup and execution of the forecasting workflow, including instructions for provisioning a cloud VM (Ubuntu Minimal with a 25 GB hard drive) and configuring API access using a primary API key.</p>
<h2>Requirements</h2>

<p><em>No information about the requirements of this project could be determined from the available source code. This section is intentionally left blank.</em></p>
<h2>Installation</h2>
<h2>Usage</h2>

<p>Unfortunately, based on the available context, there isn't enough detailed information to provide complete usage instructions. However, the general workflow implied by the project materials is as follows:</p>

<h3>Prerequisites</h3>

<ul>
<li><strong>ElectricityMaps Account</strong>: Sign up for an <a href="https://www.electricitymaps.com/">ElectricityMaps</a> account, as it will be used to monitor and manage the energy consumption and CO2 emissions of the VMs.</li>
<li><strong>Master Machine Setup</strong>: In this tutorial, Google Colab is used as the master machine to control the VMs.</li>
<li><strong>SSH and Terminal Access</strong>: Ensure that you have access to a terminal with SSH installed, as you will use this to interact with the VMs.</li>
<li>A machine located in one of the supported zones (see below).</li>
</ul>

<h3>Step 1. Setting up the master machine</h3>

<p>In the case of Colab, you don't need a virtual environment — just run the provided notebook code directly.</p>

<h3>Step 2. Setting up the worker machine</h3>

<p>Create a virtual environment (venv) on your machine and install the necessary dependencies.</p>

<h3>Currently supported zones</h3>

<ul>
<li><code>"BR-CS"</code> (Central Brazil)</li>
<li><code>"CA-ON"</code> (Canada Ontario)</li>
<li><code>"CH"</code> (Switzerland)</li>
<li><code>"DE"</code> (Germany)</li>
<li><code>"PL"</code> (Poland)</li>
<li><code>"BE"</code> (Belgium)</li>
<li><code>"IT-NO"</code> (North Italy)</li>
<li><code>"CA-QC"</code> (Canada Quebec)</li>
<li><code>"ES"</code> (Spain)</li>
<li><code>"GB"</code> (Great Britain)</li>
<li><code>"FI"</code> (Finland)</li>
<li><code>"FR"</code> (France)</li>
<li><code>"NL"</code> (Netherlands)</li>
</ul>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the <a href="http://www.apache.org/licenses/">Apache License 2.0</a>.</p>

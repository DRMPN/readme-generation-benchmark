# twint<h2>Description</h2>

<p>Twint is a Python package that provides a command-line tool, <code>twint</code>, and can also be imported as a library. It supports Python 3 (the project metadata lists Python 3.6, 3.7, and 3.8 on CPython) and is released under the MIT License.</p>

<p>The package includes the <code>twint</code> and <code>twint.storage</code> modules. Installing it registers the <code>twint</code> console command, which runs the <code>run_as_command</code> function in <code>twint.cli</code>.</p>
<h2>Requirements</h2>

<ul>
<li><strong>Python 3</strong> is required. The project is tested on Python 3.6, 3.7, and 3.8 (CPython).</li>
<li><strong>Dependencies</strong> are listed in <code>requirements.txt</code> and are installed with the package. The <code>setup.py</code> file also pulls in <code>googletrans</code> from a fork at <a href="https://github.com/x0rzkov/py-googletrans">x0rzkov/py-googletrans</a>.</li>
</ul>

<p>If you prefer not to set up your environment manually, the project provides a Docker image based on <code>python:3.6-buster</code>. It clones the <a href="https://github.com/twintproject/twint.git">twint repository</a> and installs it with <code>pip3</code>.</p>
<h2>Installation</h2>

<h3>From source</h3>

<p>Clone the repository and install it with <code>pip</code>:</p>

<p><code>bash
git clone --depth=1 https://github.com/twintproject/twint.git
cd twint
pip3 install . -r requirements.txt
</code></p>

<p>This installs the <code>twint</code> package along with its dependencies from <code>requirements.txt</code>. The package also registers a <code>twint</code> command-line entry point.</p>

<p>The project's <code>setup.py</code> lists Python 3.6, 3.7, and 3.8 as supported versions. The <code>googletrans</code> dependency is taken from a fork at <a href="https://github.com/x0rzkov/py-googletrans">x0rzkov/py-googletrans</a>.</p>

<h3>Using Docker</h3>

<p>The repository's Dockerfile uses <code>python:3.6-buster</code> as its base image, clones Twint, and installs it with the same <code>pip3 install . -r requirements.txt</code> command. To build and run the image:</p>

<p><code>bash
docker build -t twint .
docker run -it twint
</code></p>

<p>The container starts a bash shell with Twint installed.</p>
<h2>Usage</h2>

<p>Twint is configured through the following options, shown here with their default values:</p>

<p>| Option | Type | Default |
|---|---|---|
| <code>Retweets</code> | <code>bool</code> | <code>False</code> |
| <code>Query</code> | <code>str</code> | <code>None</code> |
| <code>Hide_output</code> | <code>bool</code> | <code>False</code> |
| <code>Custom_query</code> | <code>str</code> | <code>""</code> |
| <code>Popular_tweets</code> | <code>bool</code> | <code>False</code> |
| <code>Skip_certs</code> | <code>bool</code> | <code>False</code> |
| <code>Native_retweets</code> | <code>bool</code> | <code>False</code> |
| <code>Min_likes</code> | <code>int</code> | <code>0</code> |
| <code>Min_retweets</code> | <code>int</code> | <code>0</code> |
| <code>Min_replies</code> | <code>int</code> | <code>0</code> |
| <code>Links</code> | <code>Optional[str]</code> | <code>None</code> |
| <code>Source</code> | <code>Optional[str]</code> | <code>None</code> |
| <code>Members_list</code> | <code>Optional[str]</code> | <code>None</code> |
| <code>Filter_retweets</code> | <code>bool</code> | <code>False</code> |
| <code>Translate</code> | <code>bool</code> | <code>False</code> |
| <code>TranslateSrc</code> | <code>str</code> | <code>"en"</code> |
| <code>TranslateDest</code> | <code>str</code> | <code>"en"</code> |
| <code>Backoff_exponent</code> | <code>float</code> | <code>3.0</code> |
| <code>Min_wait_time</code> | <code>int</code> | <code>0</code> |
| <code>Bearer_token</code> | <code>str</code> | <code>None</code> |
| <code>Guest_token</code> | <code>str</code> | <code>None</code> |
| <code>deleted</code> | <code>list</code> | <code>None</code> |</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the MIT License. See the <code>LICENSE</code> file for the full text.</p>

<p>Copyright (c) 2018 Cody Zacharias</p>

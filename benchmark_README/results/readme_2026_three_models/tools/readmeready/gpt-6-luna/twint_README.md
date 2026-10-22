# twint<p>I’ll inspect the repository’s package metadata and core modules to summarize what Twint does.</p>

<h2>Description</h2>

<p>Twint is a Python tool for collecting tweets from Twitter without using the official Twitter API. It provides a command-line interface and supports searching for tweets with filters such as tweet count.</p>
<p>I’ll inspect the repository’s packaging metadata and dependency files to identify the requirements accurately.</p>

<h2>Requirements</h2>

<ul>
<li>Python 3.6 or later. The package classifiers list Python 3.6, 3.7, and 3.8.</li>
<li>Install the project dependencies from <code>requirements.txt</code> when installing Twint.</li>
</ul>
<h2>Installation</h2>

<p>Twint supports Python 3.6 and later. To install from the source repository:</p>

<p><code>bash
git clone --depth=1 https://github.com/twintproject/twint.git
cd twint
python3 -m pip install . -r requirements.txt
</code></p>
<h2>Usage</h2>

<p>Run Twint from the command line to collect tweets from a user or search for a term:</p>

<p><code>bash
twint -u username
twint -s "search terms"
</code></p>

<p>To write results to a CSV file:</p>

<p><code>bash
twint -u username -o tweets.csv --csv
</code></p>

<p>Twint can also be used from Python:</p>

<p>```python
import twint</p>

<p>config = twint.Config()
config.Username = "username"
config.Limit = 20</p>

<p>twint.run.Search(config)
```</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>twint is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for the full license text.</p>

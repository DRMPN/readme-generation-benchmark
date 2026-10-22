# public-apis<h2>Description</h2>

<p>This part of the project checks the formatting of entries in the API list. Each entry is a line in the README that names an API, links to it, and describes it. The checks help keep entries consistent.</p>

<p>The code includes three checks:</p>

<ul>
<li><strong>Title check:</strong> The title must use Markdown link syntax, <code>[TITLE](LINK)</code>. The title also must not end with "API", because every entry in the list is already an API.</li>
<li><strong>Description check:</strong> The first character must be capitalized. The description must not end with punctuation, and it must not exceed a maximum length.</li>
<li><strong>Auth check:</strong> The auth value must be <code>No</code> or enclosed in backticks, such as <code>`apiKey`</code>. The value must also be one of the recognized auth options.</li>
</ul>

<p>Each check returns a list of error messages tied to the line number where the problem occurred. An empty list means the entry passed that check.</p>
<h2>Requirements</h2>

<p>The project's Python dependencies are pinned to specific versions in <code>requirements.txt</code>:</p>

<p><code>
certifi==2021.10.8
charset-normalizer==2.0.10
idna==3.3
requests==2.27.1
urllib3==1.26.8
</code></p>

<p>To install them, run:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>
<h2>Installation</h2>

<p>The project's dependencies are pinned in <code>requirements.txt</code>:</p>

<p><code>
certifi==2021.10.8
charset-normalizer==2.0.10
idna==3.3
requests==2.27.1
urllib3==1.26.8
</code></p>

<p>To install them, run the following from the root of the repository:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>
<h2>Usage</h2>

<p>The context includes parts of a Python script that appears to check the project's API entries, along with a list of pinned dependencies. The snippets don't show how to run the script, so the steps below cover only what the code makes clear.</p>

<ul>
<li><strong>Dependencies:</strong> The script relies on <code>requests</code> (pinned to 2.27.1) and its supporting packages: <code>certifi</code>, <code>charset-normalizer</code>, <code>idna</code>, and <code>urllib3</code>.</li>
<li><strong>Formatting checks:</strong> The script parses the README by its <code>###</code> category headings and <code>* [Name](url)</code> entries. It enforces a minimum number of entries per category (<code>min_entries_per_category = 3</code>) and a maximum description length (<code>max_description_length = 100</code>). Errors are reported with line numbers, such as <code>(L012) message</code>.</li>
<li><strong>Accepted values:</strong> Each API entry is checked against allowed values for authentication (<code>apiKey</code>, <code>OAuth</code>, <code>X-Mashape-Key</code>, <code>User-Agent</code>, <code>No</code>), HTTPS support (<code>Yes</code>, <code>No</code>), and CORS support (<code>Yes</code>, <code>No</code>, <code>Unknown</code>).</li>
<li><strong>Link checking:</strong> The script includes a helper that inspects an HTTP response for Cloudflare protection markers, such as "Cloudflare", "Ray ID:", and "<em>cf</em>chl". This suggests it is used to detect when an API endpoint is blocked or gated by a browser check rather than returning real data.</li>
</ul>

<p>For background on the Cloudflare check, see the discussions in <a href="https://github.com/public-apis/public-apis/pull/2409">pull request #2409</a> and <a href="https://github.com/public-apis/public-apis/issues/2960">issue #2960</a>.</p>
<h2>Contributing</h2>

<p>I can't fill in this section. The provided context doesn't include any contribution guidelines, such as how to submit entries, PR requirements, or a code of conduct. It contains the MIT license, a list of Python requirements, and some links to discussions about Cloudflare detection, but none of these describe how to contribute.</p>
<h2>License</h2>

<p>This project is released under the MIT License. Copyright (c) 2022 public-apis.</p>

<p>The MIT License allows anyone to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided the copyright notice and permission notice are included in all copies or substantial portions of the software. The software is provided "as is," without warranty of any kind.</p>

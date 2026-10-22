# public-apis<h2>Description</h2>

<p>A collective list of free APIs for use in software and web development.</p>

<p>This repository serves as a community-maintained catalog of publicly available APIs. Each entry in the list contains the API's title (as a link to its site), a short description, and the authentication method it requires (for example, <code>apiKey</code> or <code>No</code> for APIs that need no authentication).</p>
<h2>Requirements</h2>

<p>Python, along with the dependencies listed in <code>requirements.txt</code>, is required to run the validation script locally:</p>

<ul>
<li>certifi==2021.10.8</li>
<li>charset-normalizer==2.0.10</li>
<li>idna==3.3</li>
<li>requests==2.27.1</li>
<li>urllib3==1.26.8</li>
</ul>
<h2>Installation</h2>

<p>If you only want to browse the list of APIs, there is nothing to install — the list is maintained directly in this repository.</p>

<p>If you want to work on the project locally (for example, to run the scripts that validate the entries in the list), follow the steps below.</p>

<h3>Prerequisites</h3>

<ul>
<li>Python 3 with <code>pip</code> installed</li>
</ul>

<h3>Steps</h3>

<ol>
<li><p>Clone this repository:</p>

<p><code>bash
git clone &lt;repository-url&gt;
cd public-apis
</code></p></li>
<li><p>Install the required dependencies from <code>requirements.txt</code>:</p>

<p><code>bash
pip install -r requirements.txt
</code></p></li>
</ol>

<p>This will install the following packages (as pinned in <code>requirements.txt</code>):</p>

<ul>
<li><code>certifi==2021.10.8</code></li>
<li><code>charset-normalizer==2.0.10</code></li>
<li><code>idna==3.3</code></li>
<li><code>requests==2.27.1</code></li>
<li><code>urllib3==1.26.8</code></li>
</ul>

<p>The primary dependency is <code>requests</code> (the remaining packages are its own dependencies). These are used by the project's validation scripts — such as the <code>validate</code> module, which provides the <code>format</code> and <code>links</code> utilities — to check the API entries in the list.</p>
<h2>Usage</h2>

<p>This repository is a collective list of free APIs for use in software and web development. The list is maintained as a single Markdown document, so there is nothing to install or run — you simply browse it and use the APIs that fit your needs.</p>

<h3>Navigating the list</h3>

<p>APIs are grouped into categories (for example, Animals, Business, Finance, etc.). The <strong>Index</strong> at the top of <code>README.md</code> links to every category, and each category contains a table of API entries with the following columns:</p>

<p>| Column   | Meaning                                                        |
| -------- | -------------------------------------------------------------- |
| API      | Name of the API, linked to its documentation                   |
| Description | Short description of what the API does (up to 100 characters) |
| Auth     | Whether authentication is required, and of which type          |
| HTTPS    | Whether the API supports HTTPS                                 |
| CORS     | Whether the API supports CORS                                  |</p>

<p>You can also use your browser's built-in search (Ctrl/Cmd + F) to look for a specific API or keyword.</p>

<h3>The <code>Auth</code> column</h3>

<p>| Value          | Meaning                                              |
| -------------- | ---------------------------------------------------- |
| <code>No</code>           | The API does not require authentication              |
| <code>apiKey</code>       | The API requires a static API key                    |
| <code>OAuth</code>        | The API requires OAuth-based authentication          |
| <code>X-Mashape-Key</code>| The API requires a Mashape key                       |
| <code>User-Agent</code>   | The API requires a <code>User-Agent</code> request header       |</p>

<h3>The <code>HTTPS</code> column</h3>

<ul>
<li><code>Yes</code> — the API supports HTTPS</li>
<li><code>No</code> — the API does not support HTTPS</li>
</ul>

<h3>The <code>CORS</code> column</h3>

<ul>
<li><code>Yes</code> — CORS is supported</li>
<li><code>No</code> — CORS is not supported</li>
<li><code>Unknown</code> — CORS support could not be determined</li>
</ul>

<h3>Maintenance scripts</h3>

<p>In addition to the list itself, the repository contains scripts used by the maintainers to keep it accurate and consistent:</p>

<ul>
<li>A <strong>validation script</strong> that enforces the structure and format of the list: the allowed <code>Auth</code> values (<code>apiKey</code>, <code>OAuth</code>, <code>X-Mashape-Key</code>, <code>User-Agent</code>, <code>No</code>), the allowed <code>HTTPS</code> values (<code>Yes</code>/<code>No</code>), the allowed <code>CORS</code> values (<code>Yes</code>/<code>No</code>/<code>Unknown</code>), the maximum description length, and a minimum number of entries per category.</li>
<li>A <strong>check script</strong> that uses the <code>requests</code> library to probe every listed API and detects endpoints that are unreachable or protected by Cloudflare.</li>
</ul>

<p>Discussions related to the maintenance and automated checking of the list can be found in <a href="https://github.com/public-apis/public-apis/pull/2409">pull request #2409</a> and <a href="https://github.com/public-apis/public-apis/issues/2960">issue #2960</a>.</p>
<h2>Contributing</h2>

<p>Thanks for your interest in contributing to the Public APIs project! Contributions are welcome!</p>

<p>Entries in the list are added, updated, or removed by opening a pull request. Pull requests are checked automatically: a validation script inspects the diff of each pull request and verifies the URLs of the entries that were added, so that pages which are unreachable — or protected by a Cloudflare security check — are detected.</p>

<p>Discussions in issues and pull requests:
- https://github.com/public-apis/public-apis/pull/2409
- https://github.com/public-apis/public-apis/issues/2960</p>
<h2>License</h2>

<p>This project is licensed under the MIT License.</p>

<p>Copyright (c) 2022 public-apis</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.</p>

# hackingtool<h2>Description</h2>

<p><strong>Hackingtool</strong> is an all-in-one toolkit that bundles a wide range of security and penetration testing tools into a single, easy-to-use framework. Instead of hunting for individual tools across the internet, Hackingtool organizes them into logical categories so you can launch them all from one place.</p>

<p>The toolkit is organized as a collection of tool categories, each grouping related tools together. The categories available include:</p>

<ul>
<li><strong>AnonSurf</strong> – Tools for staying anonymous while browsing</li>
<li><strong>Information Gathering</strong> – Tools for collecting information about targets</li>
<li><strong>DDOS Attack Tools</strong> – Denial-of-service tooling</li>
<li><strong>Payload Creator</strong> – Utilities for generating payloads</li>
<li><strong>Web Attack Tools</strong> – Tools aimed at attacking web applications</li>
<li><strong>Phishing Attack Tools</strong> – Phishing frameworks (including an advanced OTP phishing tool)</li>
<li><strong>XSS Attack Tools</strong> – Cross-site scripting attack tools</li>
<li><strong>SQL Injection Tools</strong> – SQLi-related tooling</li>
<li><strong>Wireless Attack Tools</strong> – Wi-Fi and wireless attack utilities</li>
<li><strong>Exploit Frameworks</strong> – Exploitation frameworks</li>
<li><strong>Post Exploitation</strong> – Tools for use after a system has been compromised</li>
<li><strong>Remote Administration</strong> – Remote access/administration tools</li>
<li><strong>Reverse Engineering</strong> – Reverse engineering utilities</li>
<li><strong>Steganography</strong> – Tools for hiding data within files</li>
<li><strong>Forensic Tools</strong> – Digital forensics utilities</li>
<li><strong>Wordlist Generator</strong> – Tools for generating password/word lists</li>
<li><strong>Other Tools</strong> – Miscellaneous utilities</li>
<li><strong>Tool Manager</strong> – Manage and update the installed tools</li>
</ul>

<p>Each tool in the collection can define its own installation commands, run commands, and an optional project URL pointing to the original tool's repository, making it simple to install and launch tools directly from Hackingtool.</p>

<blockquote>
  <p><strong>Note:</strong> The project's <code>README.md</code> is generated automatically from a <code>README_template.md</code> file using a script that builds the table of contents and tool descriptions from the tool definitions in the codebase. If you add a new tool or category, regenerate the README so it stays up to date.</p>
</blockquote>
<h2>Requirements</h2>

<p>Before installing and running <strong>hackingtool</strong>, make sure your system meets the following prerequisites:</p>

<ul>
<li><strong>Linux-based OS</strong> — the toolkit is designed for penetration testing distributions such as Kali Linux (Ubuntu and other Debian-based systems generally work as well).</li>
<li><strong>Python 3</strong> — the core framework and all tool collections are written in Python 3.</li>
<li><strong>pip (Python package manager)</strong> — used to install Python dependencies.</li>
<li><strong>Root / sudo privileges</strong> — many of the bundled tools (e.g. network and wireless attack tools) require elevated permissions to run, and several tool collections execute commands with <code>sudo</code>.</li>
<li><strong>git</strong> — required to clone the repository and for tools that pull their own source code from external repositories.</li>
</ul>

<h3>Additional system utilities</h3>

<p>Some tools bundled within the framework rely on command-line utilities that may not be installed by default:</p>

<ul>
<li><code>boxes</code> — used for formatting terminal output.</li>
<li><code>lolcat</code> — used to colorize terminal output.</li>
</ul>

<h3>Browser automation driver</h3>

<p>Certain web-related tools (such as those used for social media / web account automation) require Mozilla's <strong>geckodriver</strong>, which enables automation of the Firefox browser. You can download the appropriate release for your platform from the official geckodriver repository: https://github.com/mozilla/geckodriver/releases</p>

<blockquote>
  <p>[!!] On Linux, you can place the geckodriver binary in <code>/usr/bin</code> to make it available system-wide.</p>
</blockquote>
<h2>Installation</h2>

<h3>Prerequisites</h3>

<ul>
<li>Linux-based operating system (Kali Linux is recommended)</li>
<li>Python 3</li>
<li><code>sudo</code> privileges (many of the tools bundled with hackingtool require root access)</li>
</ul>

<h3>Steps</h3>

<ol>
<li><p><strong>Clone the repository</strong> from GitHub:</p>

<p><code>bash
git clone https://github.com/Z4nzu/hackingtool
cd hackingtool
</code></p></li>
<li><p><strong>Run the installation script</strong>:</p>

<p><code>bash
sudo bash install.sh
</code></p>

<p>The script will set up all required dependencies automatically. If the script fails, an error message will be displayed and the installation will stop.</p></li>
<li><p><strong>Launch hackingtool</strong>:</p>

<p><code>bash
sudo hackingtool
</code></p></li>
</ol>

<h3>Notes</h3>

<ul>
<li>Some of the individual tools included in the toolkit require external binaries to be installed manually. For example, tools that rely on browser automation need <strong>geckodriver</strong>, which can be downloaded from the <a href="https://github.com/mozilla/geckodriver/releases">geckodriver releases page</a>. On Linux, the geckodriver binary should be placed in <code>/usr/bin</code>.</li>
<li>Certain tools (such as those with their own install routines) may prompt you for confirmation before installing or uninstalling.</li>
</ul>

<h3>Updating</h3>

<p>To update an existing installation to the latest version, pull the latest changes and re-run the installation script:</p>

<p><code>bash
git pull
sudo bash install.sh
</code></p>

<p>If the script runs successfully, you will see a success message confirming that the tool has been updated.</p>

<h3>Uninstallation</h3>

<p>Each tool managed by hackingtool supports uninstallation. Before any uninstall commands are executed, you will be asked to confirm that you really want to remove the tool, giving you a chance to back out before anything is removed from your system.</p>
<h2>Usage</h2>

<h3>Requirements</h3>

<ul>
<li>Python 3</li>
<li>Linux-based operating system (Kali Linux is recommended, but most Debian/Ubuntu-based distributions will work)</li>
<li>Some tools require additional external programs (e.g., <code>geckodriver</code> for browser automation — you can download it from the <a href="https://github.com/mozilla/geckodriver/releases">GeckoDriver releases page</a> and place it in <code>/usr/bin</code> on Linux)</li>
</ul>

<h3>Installation</h3>

<p>Clone the repository and run the installer:</p>

<p><code>bash
git clone &lt;this-repository-url&gt;
cd hackingtool
pip3 install -r requirements.txt
sudo python3 install.py
</code></p>

<h3>Running the Toolkit</h3>

<p>After installation, launch the interactive menu:</p>

<p><code>bash
sudo hackingtool
</code></p>

<p>You will be presented with a menu of tool categories. Each category (collection) groups related individual tools, for example:</p>

<ul>
<li>Anonymity / Surfing tools</li>
<li>DDoS attack tools</li>
<li>Exploit frameworks</li>
<li>Forensic tools</li>
<li>Information gathering tools</li>
<li>Payload creators</li>
<li>Phishing attack tools</li>
<li>Post exploitation tools</li>
<li>Remote administration tools</li>
<li>Reverse engineering tools</li>
<li>SQL injection tools</li>
<li>Steganography tools</li>
<li>Tool manager (install/manage external tools)</li>
<li>Web attack tools</li>
<li>Wireless attack tools</li>
<li>Wordlist generators</li>
<li>XSS attack tools</li>
<li>And more (Android attacks, email verification, hash cracking, social media tools, Wi-Fi jamming, etc.)</li>
</ul>

<p>Simply enter the number of the category you want, then select the specific tool you wish to run and follow the on-screen prompts.</p>

<h3>Regenerating the README</h3>

<p>The project includes a script that automatically generates the table of contents and tool descriptions found in <code>README.md</code> from the tool definitions in the source code:</p>

<p><code>bash
python3 generate_readme.py
</code></p>

<p>This script reads the <code>README_template.md</code> file, injects a generated table of contents (<code>{{toc}}</code>) and a list of tool links/descriptions (<code>{{tools}}</code>), and writes the result to <code>README.md</code>. If you add a new tool or tool collection to the project, re-run this script to keep the README up to date.</p>
<h2>Contributing</h2>

<p>Contributions to <strong>hackingtool</strong> are welcome! If you'd like to add a new tool or improve an existing one, here's how the project is structured so you know where your changes belong:</p>

<h3>Adding a New Tool</h3>

<ol>
<li><p><strong>Create or edit a tool module</strong> — All tools live in the <code>tools/</code> directory, organized by category (e.g., <code>information_gathering_tools.py</code>, <code>wireless_attack_tools.py</code>, <code>xss_attack.py</code>, etc.).</p></li>
<li><p><strong>Use the provided base classes</strong> — The project uses two core classes from the <code>core</code> module:</p>

<ul>
<li><code>HackingTool</code> — the base class for a single tool. Define the tool's <code>TITLE</code>, <code>DESCRIPTION</code>, and optionally a <code>PROJECT_URL</code> pointing to the upstream project it wraps.</li>
<li><code>HackingToolsCollection</code> — used to group related tools into a category. Each collection exposes a <code>TITLE</code> and a <code>TOOLS</code> list.</li>
</ul></li>
<li><p><strong>Register your tool</strong> — Import your tool class in the main entry point and add it to the appropriate tools collection (or create a new collection) so it appears in the menu.</p></li>
</ol>

<h3>Regenerating the README</h3>

<p>The <code>README.md</code> file is <strong>auto-generated</strong>. After adding or changing tools, do <strong>not</strong> edit <code>README.md</code> directly. Instead:</p>

<ol>
<li>Update <code>README_template.md</code> if needed.</li>
<li>Run the generator script, which rebuilds the table of contents and tool descriptions from the registered tools and writes them into <code>README.md</code> using the <code>generate_readme()</code> function.</li>
</ol>

<p>The generator walks all registered <code>HackingToolsCollection</code> and <code>HackingTool</code> instances, builds a markdown table of contents, and links each tool entry to its <code>PROJECT_URL</code> if one is defined.</p>

<h3>Guidelines</h3>

<ul>
<li>Keep tool descriptions clear and concise.</li>
<li>If your tool wraps an external project, set <code>PROJECT_URL</code> so it gets linked in the README automatically.</li>
<li>Test that the tool menu renders correctly after regenerating the README.</li>
</ul>
<h2>License</h2>

<p>This project is licensed under the <strong>MIT License</strong>.</p>

<p>```
MIT License</p>

<p>Copyright (c) 2020 Mr.Z4nzu</p>

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
SOFTWARE.
```</p>

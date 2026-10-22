# hackingtool<h2>Description</h2>

<p>hackingtool is a Python project that collects security and penetration-testing tools in one place. Each tool is described in code, and the project's README is generated from those descriptions.</p>

<p>The tools are grouped into categories such as anonymity, DDoS, exploit frameworks, forensics, information gathering, payload creation, phishing, post-exploitation, remote administration, reverse engineering, SQL injection, steganography, web attacks, wireless attacks, wordlist generation, and XSS. Each category is a collection of tools, and collections can contain other collections.</p>

<p>Each tool is defined as a class with:</p>

<ul>
<li>A title and a short description.</li>
<li>Install commands, which are the shell commands used to set the tool up.</li>
<li>Run commands, which are the shell commands used to start it.</li>
<li>An optional project URL that points to the tool's upstream project.</li>
</ul>

<p>The project also includes a README generator. It walks through the list of tool collections and tools, builds a table of contents and a tool list in Markdown, and inserts them into a <code>README_template.md</code> file to produce <code>README.md</code>.</p>
<h2>Requirements</h2>
<h2>Installation</h2>

<p>Each tool in hackingtool has its own installation process. When you install a tool, the project runs the tool's <code>before_install</code> hook, then executes its install commands one by one in the shell. If any install commands were defined, the project then runs <code>after_install</code>, which prints "Successfully installed!".</p>

<p>Uninstalling works in a similar way. The project asks for confirmation through <code>before_uninstall</code>, runs the tool's uninstall commands if confirmed, and then runs <code>after_uninstall</code>.</p>

<p>Some tools require <code>sudo</code> for their install commands. For example, one tool's install commands include <code>sudo make install</code>, and the project's update flow re-runs the installation script with <code>sudo bash install.sh</code>.</p>
<h2>Usage</h2>

<p>The README's tool list and table of contents are generated automatically. Running the generator script from the repository root:</p>

<ol>
<li>Reads <code>README_template.md</code>.</li>
<li>Replaces the <code>{{toc}}</code> placeholder with a table of contents.</li>
<li>Replaces the <code>{{tools}}</code> placeholder with the list of tools.</li>
<li>Writes the result to <code>README.md</code>.</li>
</ol>

<p>Tool categories (collections) become nested Markdown headings, and each tool with a project URL is listed as a link to that project. Tools without a URL appear as plain text.</p>

<p>To update the README after changing the tool definitions, run the script directly with Python from the repository root.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the MIT License. Copyright (c) 2020 Mr.Z4nzu.</p>

<p>Permission is granted, free of charge, to any person obtaining a copy of this software and its associated documentation files to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, and to permit others to do the same, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice must be included in all copies or substantial portions of the software.</p>

<p>The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from, out of, or in connection with the software or its use.</p>

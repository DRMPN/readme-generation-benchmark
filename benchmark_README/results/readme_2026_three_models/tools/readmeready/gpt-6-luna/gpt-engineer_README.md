# gpt-engineer<h2>Description</h2>

<p>gpt-engineer uses an AI model to generate software from a prompt. It can also work with an existing project to improve it. You can configure the model and its response temperature, and choose whether to discuss the requirements before implementation, use lite mode, or enable self-healing.</p>
<h2>Requirements</h2>

<p>The package requires <a href="https://github.com/engineer-man/gpt-engineer"><code>parso</code></a> version <code>&gt;=0.8.3,&lt;0.9.0</code>.</p>
<h2>Installation</h2>

<p>From the repository root, install the project and its dependencies with Poetry:</p>

<p><code>bash
poetry install
</code></p>
<h2>Usage</h2>

<p>Create a project directory and add a <code>prompt</code> file describing what you want to build:</p>

<p><code>bash
mkdir my-project
cd my-project
echo "Build a simple task tracker" &gt; prompt
</code></p>

<p>Run GPT Engineer from the project directory:</p>

<p><code>bash
gpte
</code></p>
<h2>Contributing</h2>

<p>Contribution guidelines are in <code>.github/CONTRIBUTING.md</code>.</p>
<h2>License</h2>

<p>MIT License</p>

<p>Copyright (c) 2023 Anton Osika</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>

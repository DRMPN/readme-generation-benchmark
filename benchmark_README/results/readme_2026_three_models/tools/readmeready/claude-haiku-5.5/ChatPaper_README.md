# ChatPaper<h2>Description</h2>

<p>ChatPaper is a Python project that uses OpenAI language models to help readers work with academic papers. Based on the prompts in the code, it can:</p>

<ul>
<li><strong>Select key sections of a paper.</strong> Because of length limits, the project sends the paper's title, abstract, and section headings to <code>gpt-3.5-turbo</code>, which chooses at most two sections to analyze in detail.</li>
<li><strong>Propose preliminary concepts.</strong> The project asks the model for a ranked list of background concepts a reader should understand before the paper's main ideas. More fundamental concepts get lower numbers.</li>
<li><strong>Extract keywords.</strong> A separate system prompt handles keyword extraction.</li>
<li><strong>Write Chinese summaries.</strong> The output prompts ask for natural, fluent Chinese. Technical terms are kept in English in parentheses, and the output is organized as Markdown with numbered section headings.</li>
</ul>

<p>The repository's <code>setup.py</code> packages the project for installation and uses this <code>README.md</code> as the long description.</p>
<h2>Requirements</h2>

<p>ChatPaper is a Python project. The environment it was tested in used Python 3.9 with the following packages:</p>

<ul>
<li><code>gradio</code> (3.21.0)</li>
<li><code>openai</code> (0.27.2)</li>
<li><code>arxiv</code></li>
<li><code>feedparser</code> (6.0.10), used by <code>arxiv</code></li>
<li><code>markdown</code> (3.4.1)</li>
<li><code>Pillow</code> (8.4.0)</li>
<li><code>requests</code></li>
<li><code>tiktoken</code></li>
</ul>

<p>Install them with pip:</p>

<p><code>bash
pip install gradio==3.21.0 openai==0.27.2 arxiv markdown==3.4.1 Pillow==8.4.0 requests tiktoken
</code></p>
<h2>Installation</h2>

<p>The project uses a <code>setup.py</code> script at the repository root, so you can install it from a local clone with pip:</p>

<p><code>bash
pip install .
</code></p>

<p>The packages used by ChatPaper include <code>gradio</code>, <code>arxiv</code>, <code>feedparser</code>, <code>markdown</code>, <code>pandas</code>, <code>matplotlib</code>, <code>huggingface-hub</code>, <code>httpx</code>, <code>fastapi</code>, and <code>uvicorn</code>. The setup context I was given does not include the full dependency list, so it is not shown here.</p>
<h2>Usage</h2>

<p><em>(Left blank: the provided context does not include information about how to use ChatPaper.)</em></p>
<h2>Contributing</h2>

<p><em>(No contribution guidelines were found in the provided context, so this section is left blank.)</em></p>
<h2>License</h2>

<p>This project is released under the MIT License. Copyright (c) 2022 Titipat Achakulvisut and others.</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>

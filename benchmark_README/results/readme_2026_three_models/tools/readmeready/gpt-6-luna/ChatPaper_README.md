# ChatPaper<h2>Description</h2>

<p>ChatPaper uses ChatGPT to help developers and researchers read academic papers. It can generate structured, Chinese-language paper content and propose concepts to introduce in a paper’s preliminaries. To work within input-length limits, it can also select up to two sections for further processing based on a paper’s title, abstract, and section headings.</p>
<h2>Requirements</h2>

<p>ChatPaper depends on:</p>

<ul>
<li><code>arxiv</code></li>
<li><code>openai</code></li>
<li><code>tiktoken</code></li>
<li><code>gradio</code></li>
<li><code>markdown</code></li>
<li><code>Pillow</code></li>
</ul>
<h2>Installation</h2>

<p>From the repository root, install the package with pip:</p>

<p><code>bash
python -m pip install .
</code></p>
<h2>使用方法 (Usage)</h2>

<p>提交论文内容后，ChatPaper 会按以下格式生成论文信息和总结：</p>

<ol>
<li><strong>Title</strong>：论文标题</li>
<li><strong>Authors</strong>：作者</li>
<li><strong>Affiliation</strong>：作者单位</li>
<li><strong>Keywords</strong>：关键词</li>
<li><strong>Urls</strong>：相关链接</li>
<li><strong>Summary</strong>：概述论文的研究问题、主要贡献、研究方法，以及任务与性能表现。</li>
</ol>
<p>我先查看仓库里的贡献说明、项目文档和开发配置，再根据实际内容整理这一节。</p>

<h2>贡献 (Contributing)</h2>
<h2>License</h2>

<p>Copyright (c) 2022 Titipat Achakulvisut and others</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>

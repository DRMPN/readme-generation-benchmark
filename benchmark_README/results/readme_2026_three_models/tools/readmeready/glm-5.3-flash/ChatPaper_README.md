# ChatPaper<h2>Description</h2>

<p>ChatPaper is a tool that leverages large language models (via the OpenAI API) to automatically read, analyze, and summarize academic papers. Given a paper (e.g., fetched from arXiv), ChatPaper:</p>

<ul>
<li>Extracts key information such as the paper's title, abstract, and section contents.</li>
<li>Uses GPT models (e.g., <code>gpt-3.5-turbo</code>) through <code>openai.ChatCompletion</code> to intelligently select the most relevant sections of a paper when the full text is too long to process at once, asking the model to choose at most two sections based on the title, abstract, and available headings.</li>
<li>Generates structured auxiliary information for a paper, such as:
<ul>
<li><strong>Keywords</strong> relevant to the paper's domain.</li>
<li><strong>Preliminaries</strong> — a ranked list of fundamental concepts (ordered by how foundational they are) that a reader should know before reading the paper. This is produced via a dedicated system prompt that requests output in a JSON format.</li>
</ul></li>
<li>Supports Chinese translation/summarization of paper sections, with prompts that enforce rigorous terminology (annotated with English terms), natural and idiomatic Chinese phrasing, appropriate use of Markdown formatting (ordered lists, bold text, etc.), and a well-defined output format (<code>## Section name</code> followed by the translated content).</li>
</ul>

<p>The project is packaged with <code>setuptools</code> (see <code>setup.py</code>), uses <code>README.md</code> as its long description, and discovers packages automatically via <code>find_packages</code>.</p>
<h2>Requirements</h2>

<p>ChatPaper requires Python 3.9+ (tested with Python 3.9). The main dependencies include:</p>

<ul>
<li><code>openai</code> (0.27.2) — for interacting with the GPT model</li>
<li><code>arxiv</code> — for fetching papers from arXiv</li>
<li><code>gradio</code> (3.21.0) — for the web interface</li>
<li><code>tiktoken</code> — token counting</li>
<li><code>markdown</code> — markdown rendering</li>
<li><code>Pillow</code> — image handling</li>
<li><code>numpy</code>, <code>matplotlib</code> — data handling and plotting</li>
</ul>

<p>To install the requirements, run:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>

<p>You will also need an OpenAI API key to use ChatPaper.</p>
<h2>Installation</h2>

<p>To get started with ChatPaper, follow these steps:</p>

<h3>1. Clone the repository</h3>

<p><code>bash
git clone https://github.com/kaixindelele/ChatPaper.git
cd ChatPaper
</code></p>

<h3>2. Install the dependencies</h3>

<p>ChatPaper requires Python 3.x. Install the required Python packages using <code>pip</code>:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>

<p>This will install all necessary dependencies, including packages such as <code>gradio</code>, <code>arxiv</code>, and <code>fastapi</code> that are used by the project.</p>

<h3>3. Run ChatPaper</h3>

<p>Once the dependencies are installed, you can run ChatPaper with:</p>

<p><code>bash
python chat_paper.py
</code></p>

<blockquote>
  <p><strong>Note:</strong> Make sure you have configured your OpenAI API key (or other supported backend) before running, as ChatPaper needs access to a language model to summarize and review papers.</p>
</blockquote>
<h2>Usage</h2>

<p>ChatPaper 提供了命令行（Command Line）方式来抓取 arXiv 上的论文并调用 ChatGPT 进行总结。安装好依赖后，你可以在项目根目录下运行以下命令：</p>

<p><code>bash
python chat_paper.py --query "chatgpt" --limit 2
</code></p>

<p>常用参数说明：</p>

<ul>
<li><code>--query</code>：用于搜索 arXiv 论文的关键词，例如 <code>"chatgpt"</code>；</li>
<li><code>--limit</code>：每个搜索词抓取的论文数量上限；</li>
<li><code>--key</code>：你的 OpenAI API Key，也可以通过环境变量配置；</li>
<li><code>--file</code>：可以直接传入本地的论文 PDF 或 tex 文件进行总结。</li>
</ul>

<p>运行成功后，ChatPaper 会输出结构化的论文摘要，包括：</p>

<ol>
<li><strong>Title</strong>：论文标题；</li>
<li><strong>Authors</strong>：作者列表；</li>
<li><strong>Affiliation</strong>：作者机构；</li>
<li><strong>Keywords</strong>：关键词；</li>
<li><strong>Urls</strong>：论文链接；</li>
<li><strong>Summary</strong>：按研究背景、创新点、研究方法与实验结果四点组织的总结。</li>
</ol>

<blockquote>
  <p>注意：使用前需要配置可用的 OpenAI API Key，并且抓取 arXiv 时请遵守 arXiv 的访问频率限制。</p>
</blockquote>
<h2>Contributing</h2>
<h2>License</h2>

<p>Copyright (c) 2022 Titipat Achakulvisut and others</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>
<h2>Description</h2>

<p>ChatPaper is a Python tool that uses OpenAI's chat models (e.g., <code>gpt-3.5-turbo</code>, called through the OpenAI API) to automatically read, analyze, and summarize academic papers.</p>

<p>Given a paper, ChatPaper can:</p>

<ul>
<li><strong>Extract the paper's structure</strong> — the title, the abstract, the section names, and the text of each section — and feed this information to the language model.</li>
<li><strong>Generate keywords</strong> for the paper using a dedicated keyword-generation system prompt.</li>
<li><strong>Propose preliminary concepts</strong>: from the paper's title and contributions, it produces a ranked list of the foundational concepts a reader needs, ordered so that more fundamental concepts are introduced earlier.</li>
<li><strong>Work within the model's context-length limits</strong>: rather than sending the whole paper at once, ChatPaper first presents the model with the title, abstract, and the headings of the potential sections, and asks it to choose at most two sections. The full text of the abstract, introduction, conclusion, and the selected sections is then provided for deeper analysis.</li>
<li><strong>Translate paper content into Chinese</strong>: translations are idiomatic and logically coherent, technical terms are annotated with their English originals, the target research domain is taken into account, short inputs are not padded with unnecessary explanations, and Markdown formatting (ordered lists, bold text, etc.) is applied where appropriate.</li>
</ul>

<p>The system behavior for these tasks (keyword extraction, preliminaries proposal, section selection, and translation) is driven by configurable system prompts, and the project is packaged as a standard Python package built with <code>setuptools</code>.</p>
<h2>Requirements</h2>

<p>ChatPaper is a Python-based project. Before running it, make sure you have the following installed:</p>

<ul>
<li><strong>Python 3.9</strong> (or later)</li>
<li><strong>pip</strong> (for installing the dependencies listed below)</li>
</ul>

<h3>Core Dependencies</h3>

<p>The main Python packages required by ChatPaper are:</p>

<ul>
<li><code>gradio</code> (3.21.0) — web interface</li>
<li><code>openai</code> (0.27.2) — OpenAI API client</li>
<li><code>arxiv</code> — arXiv API client (uses <code>feedparser</code> under the hood)</li>
<li><code>markdown</code> (3.4.1)</li>
<li><code>Pillow</code> (8.4.0)</li>
</ul>

<p>Additional dependencies such as <code>feedparser</code>, <code>tiktoken</code>, <code>aiohttp</code>, <code>tqdm</code>, <code>requests</code>, <code>numpy</code>, <code>matplotlib</code>, <code>fastapi</code>, and <code>httpx</code> are installed automatically as transitive dependencies of the packages above.</p>

<h3>Installation</h3>

<p>You can install the dependencies directly with pip:</p>

<p><code>bash
pip install arxiv openai gradio markdown Pillow
</code></p>

<p>Alternatively, install ChatPaper from the repository root, which will pull in all required dependencies via its <code>setup.py</code>:</p>

<p><code>bash
pip install .
</code></p>
<h2>Installation</h2>

<p>ChatPaper is a Python project, so getting it running locally only requires cloning this repository and installing the package with <code>pip</code>.</p>

<h3>Prerequisites</h3>

<ul>
<li><strong>Python 3.9</strong> — the project's environment is based on Python 3.9 (installed packages live under <code>/usr/local/lib/python3.9/dist-packages</code>).</li>
<li><strong>pip</strong> — used to install the package and its dependencies.</li>
</ul>

<h3>Install from source</h3>

<ol>
<li><p>Clone or download this repository and change into the project root — the directory containing <code>setup.py</code> and <code>README.md</code>.</p></li>
<li><p>Install ChatPaper together with all of its dependencies:</p>

<p><code>bash
pip install .
</code></p>

<p>Packaging is defined in <code>setup.py</code>, which uses <code>setuptools</code> together with <code>find_packages</code> to automatically discover the project's modules, and reads <code>README.md</code> as the package's long description.</p></li>
</ol>

<h3>Key dependencies</h3>

<p>Installing ChatPaper will pull in the following main packages (plus their transitive dependencies):</p>

<ul>
<li><strong>gradio</strong> — provides the web interface. Its dependency chain includes <code>fastapi</code> (which requires <code>starlette</code>), <code>uvicorn</code>, <code>httpx</code> (with <code>httpcore</code>, <code>anyio</code>, <code>sniffio</code>, and <code>rfc3986[idna2008]</code>), <code>altair</code> (with <code>jsonschema</code>), <code>pandas</code>, <code>matplotlib</code> (with <code>cycler</code>, <code>fonttools</code>, <code>kiwisolver</code>, and <code>pyparsing</code>), <code>markdown</code> (with <code>markdown-it-py</code> and <code>linkify-it-py</code>), and <code>huggingface-hub</code> (with <code>filelock</code> and <code>packaging</code>).</li>
<li><strong>arxiv</strong> — used for interacting with arXiv. It depends on <code>feedparser</code>, which in turn requires <code>sgmllib3k</code>.</li>
</ul>
<h2>Usage</h2>

<h3>1. Install the dependencies</h3>

<p>Install the required Python packages (FastAPI/Gradio for the interfaces, <code>arxiv</code>/<code>feedparser</code> for fetching papers, etc.):</p>

<p><code>bash
pip install -r requirements.txt
</code></p>

<h3>2. Provide your OpenAI API key</h3>

<p>ChatPaper sends the parsed paper content to ChatGPT to generate its summaries, so you need a valid OpenAI API key. You can supply it either:</p>

<ul>
<li>via the <code>--key</code> command line argument, e.g. <code>--key "sk-..."</code>, or</li>
<li>by setting the <code>OPENAI_API_KEY</code> environment variable before running the script.</li>
</ul>

<h3>3. Run ChatPaper</h3>

<p><strong>A. Search arXiv and summarize the matching papers:</strong></p>

<p><code>bash
python chatpaper.py --query "GPT-4" --key "sk-..."
</code></p>

<p>This queries arXiv with your keywords, downloads the latest matching papers, parses their PDFs, and sends the content to ChatGPT. You can control how many papers are fetched with <code>--page_num</code>, and filter/extract the most relevant words with <code>--max_keywords</code> and <code>--filter_keys</code>.</p>

<p><strong>B. Summarize a single local PDF:</strong></p>

<p><code>bash
python chatpaper.py --pdf_path "path/to/your/paper.pdf" --key "sk-..."
</code></p>

<h3>4. Output</h3>

<p>For every paper, ChatPaper saves a summary file (controlled by <code>--file_format</code>, written to the directory given by <code>--save_path</code>) that follows this structure:</p>

<ol>
<li>Title</li>
<li>Authors</li>
<li>Affiliation</li>
<li>Keywords</li>
<li>Urls</li>
<li>Summary, structured around the following questions:
<ul>
<li>(1) What is the research background of the paper?</li>
<li>(2) What were the past methods and their remaining problems, and does the paper propose any new approaches or ideas?</li>
<li>(3) What is the research methodology proposed in the paper?</li>
<li>(4) On what task and what performance is achieved by the methods? Can the performance support the paper's goals?</li>
</ul></li>
</ol>

<p>The output language can be selected with <code>--language</code> (e.g. Chinese or English), and the ChatGPT model version with <code>--gpt_version</code>.</p>

<h3>5. Web interface</h3>

<p>A Gradio-based web demo is also included (<code>app.py</code>), so you can enter an arXiv query or a PDF and receive the same structured summaries in the browser instead of using the command line.</p>
<h2>Contributing</h2>

<p>Contributions to ChatPaper are welcome!</p>

<p>If you would like to help improve the project, you can:</p>

<ol>
<li><strong>Open an issue</strong> — If you find a bug in the paper-downloading, PDF parsing, or summarization workflow, or if you have a suggestion for a new feature (e.g., new prompt templates or output formats), please report it in the repository's issue tracker.</li>
<li><strong>Submit a pull request</strong> — Fork the repository, create a branch for your change, implement your fix or feature, and open a pull request describing what you changed and why.</li>
</ol>

<p>When contributing code, please keep in mind the core parts of the codebase you may touch:</p>

<ul>
<li>The OpenAI API interaction layer (e.g., chat completion calls used for paper summarization and section selection).</li>
<li>The arXiv search and PDF download/parsing logic.</li>
<li>The prompt templates used to extract structured summaries (title, authors, affiliation, keywords, URLs, and the multi-point summary).</li>
</ul>

<p>Since no detailed contributor guidelines or code-of-conduct documents were found in the repository, please follow standard open-source practice: keep changes focused, include a clear description of your modifications, and make sure existing functionality still works before submitting.</p>
<h2>License</h2>

<p>ChatPaper is released under the MIT License.</p>

<p>Copyright (c) 2022 Titipat Achakulvisut and others</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>

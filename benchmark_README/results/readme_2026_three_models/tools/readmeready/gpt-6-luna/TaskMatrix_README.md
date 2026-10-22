# TaskMatrix<p>I’ll inspect the repository’s README and core source files to identify what TaskMatrix does and summarize it accurately.</p>

<h2>Description</h2>

<p>TaskMatrix provides an LLM-based workflow for organizing tasks into a structured standard operating procedure (SOP). Each step has a name and description, and can include conditional jumps to other steps. When a step needs more detail, the Planning LLM can expand it into sub-steps that remain consistent with the overall SOP and avoid repeating its content.</p>

<p>The project also includes a Visual ChatGPT prompt for assisting with text- and visual-related tasks. It is designed to answer questions and provide explanations in Markdown.</p>
<h2>Requirements</h2>
<h2>Installation</h2>

<p>The repository includes a Dockerfile that installs Python 3.11 and the dependencies in <code>src/requirements.txt</code>. From the repository root, build and run the image:</p>

<p><code>bash
docker build -t taskmatrix .
docker run --rm taskmatrix
</code></p>

<p>The container starts the services through <code>supervisord.conf</code>. The <code>WORKERS</code> environment variable defaults to <code>2</code>; you can override it when running the container:</p>

<p><code>bash
docker run --rm -e WORKERS=4 taskmatrix
</code></p>

<p>To install the Python dependencies locally instead, use Python 3.11 and run:</p>

<p><code>bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
</code></p>
<h2>Usage</h2>

<p>Provide Planning LLM with a task to analyze. It returns a standard operating procedure (SOP) that breaks the task into steps; it is intended to guide the work, not complete the task itself.</p>

<p>The SOP should use this format, with optional conditional jumps when a condition determines which step to take next:</p>

<p><code>text
STEP 1: [step name][step description][[[if 'condition'][Jump to STEP N]]]
STEP 2: [step name][step description]
</code></p>

<p>If a step needs more detail, provide a sub-SOP for that step. The sub-SOP should fit the overall procedure and avoid repeating content already covered by the original steps.</p>
<p>I’ll inspect the repository for any contribution guidance, development setup, or workflow details before drafting this section.</p>

<h2>Contributing</h2>
<h2>License</h2>

<p>MIT License</p>

<p>Copyright (c) 2023 Microsoft</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>

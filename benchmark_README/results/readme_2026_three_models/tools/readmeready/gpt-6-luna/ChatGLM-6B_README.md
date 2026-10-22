# ChatGLM-6B<h2>Description</h2>

<p>ChatGLM-6B is a conversational language-model project. Its data configuration supports training with datasets from the <code>datasets</code> library or local JSONL and CSV files. Training examples can use prompt, response, and chat-history columns, with optional validation and test data. Sequence-length settings control tokenization and truncation for source and target text.</p>
<h2>Requirements</h2>

<ul>
<li>Python 3.8 or later</li>
<li>PyTorch 1.10 or later</li>
<li>Transformers 4.27.1</li>
</ul>

<p>Install the project dependencies with:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>
<h2>Installation</h2>

<p>Install the project dependencies from the repository root:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>
<h2>Usage</h2>

<p>Load the tokenizer and model, then use <code>chat</code> to generate a response. Pass the returned history into subsequent calls to continue the conversation.</p>

<p>```python
from transformers import AutoModel, AutoTokenizer</p>

<p>tokenizer = AutoTokenizer.from<em>pretrained(
    "THUDM/chatglm-6b",
    trust</em>remote<em>code=True,
)
model = AutoModel.from</em>pretrained(
    "THUDM/chatglm-6b",
    trust<em>remote</em>code=True,
).half().cuda()</p>

<p>response, history = model.chat(tokenizer, "你好", history=[])
print(response)</p>

<p>response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=history)
print(response)
```</p>

<p>For streaming output, use <code>stream_chat</code>:</p>

<p><code>python
for response, history in model.stream_chat(tokenizer, "你好", history=[]):
    print(response)
</code></p>

<p>The repository also provides command-line and web demos, which can be started with:</p>

<p><code>bash
python cli_demo.py
python web_demo.py
</code></p>
<p>I’ll check the repository’s README and contribution-related files for project-specific guidance.</p>

<h2>Contributing</h2>

<p>A contribution is work intentionally submitted for inclusion in the project, including modifications or additions. Submissions may be electronic, verbal, or written, including through source-control systems and issue trackers. Material explicitly designated as “Not a Contribution” is excluded.</p>

<p>Contributions are subject to the <a href="http://www.apache.org/licenses/LICENSE-2.0">Apache License, Version 2.0</a>, which grants a perpetual, worldwide, non-exclusive, royalty-free copyright license to reproduce, modify, display, perform, sublicense, and distribute the work and derivative works.</p>
<h2>License</h2>

<p>Copyright Zhengxiao Du. Licensed under the Apache License, Version 2.0. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.</p>

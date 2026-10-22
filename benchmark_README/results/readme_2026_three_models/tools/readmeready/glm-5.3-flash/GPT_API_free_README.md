# GPT_API_free<h2>Description</h2>

<p>GPT<em>API</em>free is a project that provides free access to GPT API services (such as GPT-3.5, GPT-4, etc.), allowing developers to use OpenAI-compatible API endpoints without needing to pay for OpenAI's official services.</p>

<p>The project offers a free API forwarding/proxy service that is compatible with the OpenAI API format. This means developers can use the standard <code>openai</code> Python library (or any OpenAI-compatible client) and simply change the <code>base_url</code> to point to the provided API endpoint.</p>

<p>Key features include:</p>

<ul>
<li><strong>Free GPT API access</strong>: Provides API keys for free usage of models like <code>gpt-3.5-turbo</code>.</li>
<li><strong>OpenAI API compatibility</strong>: Works with the official <code>openai</code> SDK — just set the <code>base_url</code> to the provided endpoint (e.g., <code>https://api.chatanywhere.tech/v1</code>).</li>
<li><strong>Supports both streaming and non-streaming responses</strong>: You can call the chat completions API in the usual way, with <code>stream=True</code> for streaming output.</li>
<li><strong>Simple integration</strong>: Minimal setup is required — configure your API key and base URL, then call <code>client.chat.completions.create</code> as you would with the official OpenAI API.</li>
</ul>

<p>Example usage:</p>

<p>```python
from openai import OpenAI</p>

<p>client = OpenAI(
    api<em>key="YOUR API KEY",
    base</em>url="https://api.chatanywhere.tech/v1"
)</p>

<h1>Non-streaming call</h1>

<p>completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)</p>

<h1>Streaming call</h1>

<p>stream = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=messages,
    stream=True,
)
```</p>

<p>The project is licensed under the MIT License (Copyright (c) 2023-2024 牛爷爷信息技术（南京）有限公司).</p>
<h2>Requirements</h2>

<p>Based on the example usage provided in this project, you will need the following to get started:</p>

<ul>
<li><strong>Python 3.6+</strong> — the sample code is written in Python.</li>
<li><p><strong>openai Python SDK</strong> — the example uses the official <code>OpenAI</code> client:</p>

<p><code>bash
pip install --upgrade openai
</code></p></li>
<li><p><strong>An API Key</strong> — you must supply your own key when constructing the client:</p>

<p>```python
from openai import OpenAI</p>

<p>client = OpenAI(
    api<em>key="YOUR API KEY",
    base</em>url="https://api.chatanywhere.tech/v1"
)
```</p></li>
</ul>

<p>With these in place, you can make both non-streaming and streaming calls to models such as <code>gpt-3.5-turbo</code>, as shown in the project's example code.</p>
<h2>Installation</h2>

<p>To use this project, you need to have Python installed along with the official OpenAI Python SDK.</p>

<p>Install the <code>openai</code> package using pip:</p>

<p><code>bash
pip install --upgrade openai
</code></p>

<p>Then configure the client to point to the API base URL and provide your API key:</p>

<p>```python
from openai import OpenAI</p>

<p>client = OpenAI(
    # defaults to os.environ.get("OPENAI<em>API</em>KEY")
    api<em>key="YOUR API KEY",
    base</em>url="https://api.chatanywhere.tech/v1"
)
```</p>

<p>Once configured, you can make calls to the API, for example using the <code>gpt-3.5-turbo</code> model with either non-streaming or streaming responses:</p>

<p>```python</p>

<h1>非流式响应 (Non-streaming response)</h1>

<p>def gpt<em>35</em>api(messages: list):
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print(completion.choices[0].message.content)</p>

<h1>流式响应 (Streaming response)</h1>

<p>def gpt<em>35</em>api_stream(messages: list):
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")</p>

<p>if <strong>name</strong> == '<strong>main</strong>':
    messages = [{'role': 'user', 'content': '鲁迅和周树人的关系'}]
    # 非流式调用
    # gpt<em>35</em>api(messages)
    # 流式调用
    gpt<em>35</em>api_stream(messages)
```</p>
<h2>Usage</h2>

<p>First, install the OpenAI Python SDK:</p>

<p><code>bash
pip install --upgrade openai
</code></p>

<p>Then configure the client to point to this free API service:</p>

<p>```python
from openai import OpenAI</p>

<p>client = OpenAI(
    # defaults to os.environ.get("OPENAI<em>API</em>KEY")
    api<em>key="YOUR API KEY",
    base</em>url="https://api.chatanywhere.tech/v1"
)
```</p>

<h3>Non-streaming call</h3>

<p>```python
def gpt<em>35</em>api(messages: list):
    """为提供的对话消息创建新的回答</p>

<pre><code>Args:
    messages (list): 完整的对话消息
"""
completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
print(completion.choices[0].message.content)
</code></pre>

<p>```</p>

<h3>Streaming call</h3>

<p>```python
def gpt<em>35</em>api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)</p>

<pre><code>Args:
    messages (list): 完整的对话消息
"""
stream = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=messages,
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
</code></pre>

<p>```</p>

<h3>Example</h3>

<p><code>python
if __name__ == '__main__':
    messages = [{'role': 'user', 'content': '鲁迅和周树人的关系'}]
    # 非流式调用 (Non-streaming call)
    # gpt_35_api(messages)
    # 流式调用 (Streaming call)
    gpt_35_api_stream(messages)
</code></p>
<h2>Contributing</h2>

<p>We welcome contributions to the GPT<em>API</em>free project! However, there is no detailed contribution guide (such as code style rules, branch conventions, or PR procedures) available in the repository at this time.</p>

<p>If you would like to contribute, you can:</p>

<ol>
<li>Fork the repository.</li>
<li>Create a new branch for your changes.</li>
<li>Make your modifications and submit a Pull Request describing the changes you have made.</li>
</ol>

<p>The project is licensed under the MIT License, so any contributions you submit will be subject to the same license terms.</p>
<h2>License</h2>

<p>This project is licensed under the MIT License.</p>

<p>```
MIT License</p>

<p>Copyright (c) 2023-2024 牛爷爷信息技术（南京）有限公司</p>

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

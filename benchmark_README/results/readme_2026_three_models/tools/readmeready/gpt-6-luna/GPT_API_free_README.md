# GPT_API_free<h2>Description</h2>

<p>GPT<em>API</em>free is a Python example of using the OpenAI client with the ChatAnywhere API endpoint. It sends a list of chat messages to <code>gpt-3.5-turbo</code> and prints the response, either all at once with <code>gpt_35_api</code> or incrementally with <code>gpt_35_api_stream</code>.</p>

<p>Set <code>api_key</code> to your API key before running the example.</p>
<h2>Requirements</h2>

<ul>
<li>Python with the <code>openai</code> package installed.</li>
<li>An API key for the configured ChatAnywhere endpoint (<code>https://api.chatanywhere.tech/v1</code>).</li>
</ul>
<h2>Installation</h2>

<p>Install the OpenAI Python package:</p>

<p><code>bash
pip install openai
</code></p>

<p>Set <code>api_key</code> in the client configuration to your API key before running the example. The client uses <code>https://api.chatanywhere.tech/v1</code> as its <code>base_url</code>.</p>
<h2>Usage</h2>

<p>Configure the OpenAI client with your API key and the ChatAnywhere API base URL. Pass conversation messages as a list of dictionaries with <code>role</code> and <code>content</code> fields.</p>

<p>```python
from openai import OpenAI</p>

<p>client = OpenAI(
    api<em>key="YOUR API KEY",
    base</em>url="https://api.chatanywhere.tech/v1",
)</p>

<p>messages = [{"role": "user", "content": "鲁迅和周树人的关系"}]
```</p>

<p>For a non-streaming response, call the chat completions API and print the returned message:</p>

<p><code>python
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
)
print(completion.choices[0].message.content)
</code></p>

<p>For a streaming response, set <code>stream=True</code> and print each content chunk as it arrives:</p>

<p>```python
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    stream=True,
)</p>

<p>for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```</p>
<p>I’ll check the repository for contribution guidance and project-specific development instructions.</p>

<h2>Contributing</h2>
<h2>License</h2>

<p>MIT License</p>

<p>Copyright (c) 2023-2024 牛爷爷信息技术（南京）有限公司</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.</p>

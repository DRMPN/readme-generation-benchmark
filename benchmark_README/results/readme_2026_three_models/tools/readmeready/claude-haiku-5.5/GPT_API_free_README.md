# GPT_API_free<h2>Description</h2>

<p>GPT<em>API</em>free is a small Python example project that shows how to call OpenAI's <code>gpt-3.5-turbo</code> chat model through the OpenAI Python SDK. Instead of calling the default OpenAI endpoint, the client is configured to send requests to <code>https://api.chatanywhere.tech/v1</code>.</p>

<p>The project is a single script that provides two helper functions:</p>

<ul>
<li><strong><code>gpt_35_api(messages)</code></strong> sends a list of chat messages and prints the full reply once it is ready (non-streaming).</li>
<li><strong><code>gpt_35_api_stream(messages)</code></strong> sends the same kind of message list and prints the reply as it is generated, chunk by chunk (streaming).</li>
</ul>

<p>Messages use the standard chat format, for example <code>[{'role': 'user', 'content': '...'}]</code>. When the script is run directly, it sends a sample question with the streaming function.</p>

<p>The script's <code>api_key</code> is set to the placeholder <code>"YOUR API KEY"</code>, so you need to replace it with your own key before running the code.</p>
<h2>Requirements</h2>

<ul>
<li>Python 3</li>
<li>The <code>openai</code> Python package, which the code imports as <code>from openai import OpenAI</code></li>
<li>A valid API key for the service at <code>https://api.chatanywhere.tech/v1</code>. The code currently has the placeholder <code>"YOUR API KEY"</code>, so replace it with your own key before running the script.</li>
</ul>
<h2>Installation</h2>

<p>This project is a single Python script that uses the <code>openai</code> Python package. Install it with pip:</p>

<p><code>bash
pip install openai
</code></p>

<p>Before running the script, replace the <code>api_key</code> placeholder (<code>"YOUR API KEY"</code>) in the source file with your own API key.</p>
<h2>Usage</h2>

<p>The project provides two helper functions that send a list of chat messages to the <code>gpt-3.5-turbo</code> model through an OpenAI-compatible endpoint (<code>https://api.chatanywhere.tech/v1</code>) and print the reply.</p>

<p>Before running the code, replace the <code>api_key="YOUR API KEY"</code> placeholder with your own API key.</p>

<h3>Non-streaming responses</h3>

<p><code>gpt_35_api(messages)</code> waits for the full answer and then prints it:</p>

<p><code>python
messages = [{'role': 'user', 'content': 'Hello'}]
gpt_35_api(messages)
</code></p>

<h3>Streaming responses</h3>

<p><code>gpt_35_api_stream(messages)</code> prints the answer as it arrives, chunk by chunk:</p>

<p><code>python
messages = [{'role': 'user', 'content': 'Hello'}]
gpt_35_api_stream(messages)
</code></p>

<h3>Message format</h3>

<p>Both functions take a <code>messages</code> list in the standard chat format, where each item has a <code>role</code> (such as <code>user</code>) and a <code>content</code> string.</p>

<h3>Running the example script</h3>

<p>When the file is run directly, it sends a sample question with the streaming function:</p>

<p><code>bash
python &lt;script_name&gt;.py
</code></p>

<p>The script calls <code>gpt_35_api_stream</code> by default. To use the non-streaming version instead, comment out the streaming call and uncomment <code>gpt_35_api(messages)</code>.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the MIT License. Copyright (c) 2023-2024 牛爷爷信息技术（南京）有限公司.</p>

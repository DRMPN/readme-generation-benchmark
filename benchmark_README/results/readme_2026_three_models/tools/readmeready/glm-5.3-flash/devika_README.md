# devika<p>~~~markdown</p>

<h2>Description</h2>

<p>Devika is an advanced AI software engineer that can understand high-level, human-provided objectives, break them down into concrete steps, research relevant information on the web, and write code to accomplish the given goal. It leverages large language models (LLMs), planning and reasoning algorithms, and web browsing capabilities to streamline the software development process.</p>

<p>Devika is designed as a competitive open-source alternative to proprietary AI software engineers such as Devin by Cognition AI.</p>

<p>Key capabilities include:</p>

<ul>
<li><strong>Objective decomposition</strong>: Takes a high-level task description and breaks it down into an actionable, step-by-step plan.</li>
<li><strong>Agentic planning and reasoning</strong>: Uses a multi-agent architecture with dedicated agents for planning, research, and coding to drive tasks to completion.</li>
<li><strong>Web research</strong>: Browses and gathers relevant information from the web to inform implementation decisions.</li>
<li><strong>Code generation</strong>: Writes code in the project workspace to fulfill the plan, tracking its own progress as it works through each subtask.</li>
<li><strong>Multiple LLM backends</strong>: Supports working with different large language model providers, including cloud-hosted models and locally hosted models.</li>
<li><strong>Web-based UI</strong>: Provides a browser-based interface to submit objectives, monitor the agent's planning and progress, and view generated output.</li>
</ul>

<p>In short, Devika aims to act as an autonomous AI pair-programmer: you describe <em>what</em> you want built, and it plans, researches, and implements it for you.
~~~</p>
<p>~~~
File: <code>README.md</code>
```md</p>

<h2>Requirements</h2>

<p>Before you start using Devika, make sure your machine has the following system dependencies, API keys, and services set up:</p>

<h3>System Dependencies</h3>

<ul>
<li><code>Python 3.10+</code> – the backend server and the AI agents are written in Python</li>
<li><code>uv</code> – the Python package manager used to install the backend dependencies</li>
<li><code>Bun</code> – used to install and run the frontend UI</li>
<li><code>Ollama</code> – required if you want to run open-source LLMs locally</li>
<li><code>Git</code> – Devika clones and works inside Git repositories while executing tasks</li>
</ul>

<h3>API Keys</h3>

<p>Devika integrates with multiple LLM providers and services. Add the keys for the providers you plan to use in <code>config.toml</code> or through the Settings screen in the UI (all keys are optional – only the providers you actually use are required):
- <code>CLAUDE_API_KEY</code> – Anthropic Claude models
- <code>OPENAI_API_KEY</code> – OpenAI GPT models
- <code>GEMINI_API_KEY</code> – Google Gemini models
- <code>MISTRAL_API_KEY</code> – Mistral models
- <code>GROQ_API_KEY</code> – Groq-hosted models
- <code>NETLIFY_API_KEY</code> – Netlify, used to deploy the web applications Devika generates</p>

<p>At least one LLM provider (one of the API keys above or a locally running Ollama model) is required for the agents to function.</p>

<h3>Database</h3>

<ul>
<li><code>SQLAlchemy</code> – Devika stores projects, agent states, and snapshots in a SQLite database through SQLAlchemy, which is installed automatically along with the backend dependencies.</li>
</ul>

<h3>Search</h3>

<ul>
<li>A Bing Search API key is required for the web search feature – set it in <code>config.toml</code> or via the Settings screen in the UI.
```
~~~</li>
</ul>
<p>~~~</p>

<h2>Installation</h2>

<ol>
<li><p><strong>Clone the Devika repository:</strong>
<code>bash
git clone https://github.com/stitionai/devika.git
</code></p></li>
<li><p><strong>Navigate to the project directory:</strong>
<code>bash
cd devika
</code></p></li>
<li><p><strong>Install the required Python dependencies:</strong>
<code>bash
pip install -r requirements.txt
</code>
Alternatively, if you use <code>uv</code> as your Python package manager:
<code>bash
uv pip install -r requirements.txt
</code></p></li>
<li><p><strong>Install the UI dependencies:</strong>
Devika's web interface is built with Svelte and uses Bun as its JavaScript runtime and package manager (make sure Bun is installed on your system):
<code>bash
cd ui &amp;&amp; bun install
</code></p></li>
<li><p><strong>Set up the configuration:</strong>
Update the <code>config.toml</code> file with your API keys and other settings.</p></li>
<li><p><strong>Run Devika:</strong>
<code>bash
python devika.py
</code></p></li>
<li><p><strong>Compile and run the UI server:</strong>
In a separate terminal, run:
<code>bash
cd ui &amp;&amp; bun run dev
</code></p></li>
</ol>

<p>Once both the backend server and the UI server are running, you can access the Devika web interface in your browser.
~~~</p>
<h2>Usage</h2>

<p>Once you have Devika installed and configured, follow these steps to start using it:</p>

<ol>
<li><p><strong>Start the backend server:</strong></p>

<p><code>bash
python devika.py
</code></p>

<p>This will launch the Devika backend, which serves the API on <code>http://localhost:1337</code> and spins up a SQLite interface to track agents, projects, and messages.</p></li>
<li><p><strong>Run the frontend UI:</strong></p>

<p>Navigate to the <code>ui</code> directory, install the dependencies, and start the development server:</p>

<p><code>bash
cd ui
bun install   # or: npm install
bun run dev   # or: npm run dev
</code></p>

<p>Open your browser and go to <code>http://localhost:3000</code> to access the Devika web interface.</p></li>
<li><p><strong>Configure settings:</strong></p>

<p>In the UI, click on <strong>Settings</strong> to configure:</p>

<ul>
<li><strong>API keys</strong> for the supported LLM providers (Claude, OpenAI, Gemini, etc.)</li>
<li><strong>Search engine keys</strong> (e.g., Bing) used by Devika's web browsing capability</li>
<li><strong>Model selection</strong>, search engine preference, and other options</li>
</ul>

<p>Your settings will be stored and used by the backend for subsequent runs.</p></li>
<li><p><strong>Create a project and interact with Devika:</strong></p>

<ul>
<li>Create a new project from the UI (or select an existing one).</li>
<li>Type your high-level objective in natural language in the chat interface and hit send.</li>
<li>Devika will break the objective down into an execution plan, research relevant information, and write code step by step.</li>
</ul></li>
<li><p><strong>Monitor progress in real time:</strong></p>

<p>While Devika is working, the interface provides live views of:</p>

<ul>
<li><strong>Agent state</strong> — the current execution step Devika is on</li>
<li><strong>Tracker &amp; snapshot list</strong> — the plan being generated and tracked</li>
<li><strong>Terminal</strong> — live output as commands run inside the project environment</li>
</ul></li>
<li><p><strong>Review the generated code:</strong></p>

<p>Once Devika completes its run, you can inspect the generated code in the editor pane and provide follow-up messages to refine the results through the chat interface.</p></li>
</ol>
<p>~~~
File: <code>README.md</code>
```md</p>

<h2>Contributing</h2>

<p>Contributions to Devika are always welcome! Whether you want to fix a bug, add a new feature, improve the documentation, or refactor existing code, your help is greatly appreciated.</p>

<h3>Getting Started</h3>

<ol>
<li><p><strong>Fork the repository</strong> on GitHub and clone your fork locally:
<code>git clone https://github.com/&lt;your-username&gt;/devika.git &amp;&amp; cd devika</code></p></li>
<li><p><strong>Set up the development environment</strong> by following the installation and configuration instructions in the <a href="https://github.com/stitionai/devika#readme">README</a>. This includes installing the required dependencies, configuring <code>config.toml</code> with your API keys, and setting up the frontend.</p></li>
<li><p><strong>Create a new branch</strong> for your work:
<code>git checkout -b feature/my-new-feature</code></p></li>
<li><p><strong>Make your changes</strong>, keeping the following guidelines in mind:</p>

<ul>
<li>Backend (Python) code lives under <code>src/</code>, with agents in <code>src/agents/</code>, LLM providers in <code>src/llm/</code>, and browser automation in <code>src/browser/</code>.</li>
<li>The frontend lives under <code>ui/</code>.</li>
<li>Follow the existing code style and keep your changes focused on a single feature or bug fix.</li>
<li>Update documentation if your changes affect setup, configuration, or user-facing behavior.</li>
</ul></li>
<li><p><strong>Test your changes</strong> locally to make sure everything works as expected before submitting.</p></li>
<li><p><strong>Commit and push</strong> your changes to your fork, then open a pull request against the main repository with a clear description of what you changed and why.</p></li>
</ol>

<h3>Reporting Issues</h3>

<p>If you find a bug or have an idea for a new feature, please open an issue on the <a href="https://github.com/stitionai/devika">GitHub repository</a>. Include as much detail as possible, such as steps to reproduce the problem, the expected behavior, and your environment setup.</p>

<p>Thank you for helping make Devika better!
```
~~~</p>
<p>~~~
File: <code>README.md</code>
```md</p>

<h2>License</h2>

<p>This project is licensed under the MIT License.</p>

<p>Copyright (c) 2024 stition</p>

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
```
~~~</p>

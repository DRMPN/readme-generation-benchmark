# gpt-engineer<h2>Description</h2>

<p><strong>gpt-engineer</strong> is a command-line tool that lets you build software by specifying it in natural language. Instead of writing the initial codebase yourself, you describe what you want, and gpt-engineer — powered by large language models — generates the code for you. It was created by Anton Osika and is maintained by Anton Osika &amp; Contributors.</p>

<p>gpt-engineer can be used in several ways:</p>

<ul>
<li><strong>Generate a new codebase</strong> — provide a prompt describing the project you want, and the AI writes the code.</li>
<li><strong>Improve an existing project</strong> — point gpt-engineer at an existing codebase and ask it to make changes or additions to it (improve mode).</li>
<li><strong>Clarify before implementing</strong> — before writing any code, the AI can discuss the specifications with you and ask clarifying questions (clarify mode).</li>
<li><strong>Self-healing</strong> — when the generated code is run, gpt-engineer can detect errors and automatically attempt to fix them (self-heal mode).</li>
<li><strong>Lite mode</strong> — run a lighter-weight flow for quicker, simpler outputs.</li>
</ul>

<p>Additional capabilities include:</p>

<ul>
<li>Prompts can be entered interactively or supplied via text files, including a separate file that specifies requirements for the entrypoint.</li>
<li>Custom "preprompts" can be used to adjust how the AI behaves.</li>
<li>Connection can go through Azure OpenAI services in addition to standard OpenAI access.</li>
<li>The tool stores its session data on disk and records human feedback on the AI's responses, which can be used in later runs.</li>
</ul>

<p>Documentation for the project is generated with Sphinx, and a separate README covering Windows usage is included in the docs.</p>
<h2>Requirements</h2>

<ul>
<li>Python 3.10 or later</li>
<li>pip</li>
<li>An OpenAI API key, if you plan to use OpenAI models</li>
</ul>

<p>If you prefer not to use OpenAI models, gpt-engineer can also be run with a locally hosted model via LangChain.</p>
<h2>Installation</h2>

<blockquote>
  <p><strong>Note</strong>
  gpt-engineer is meant to be used with Python 3.10 or 3.11 and Node.js.</p>
  
  <p>To install and use gpt-engineer, you need:
  - Python 3.10/3.11 (newer versions might work, but haven't been tested)
  - Node.js (version 18 or later)</p>
</blockquote>

<p><strong>Install gpt-engineer</strong>:</p>

<p>Open a terminal and run:</p>

<p><code>bash
python -m pip install gpt-engineer
</code></p>

<p><strong>PYTHON INSTALLATION</strong></p>

<p>If you have <code>python &lt; 3.10</code>:</p>

<p><code>bash
python3 -m pip install gpt-engineer
</code></p>

<p>For Python 3.10/3.11/3.12 you may have to build from source:</p>

<p><code>bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
python -m pip install -e .
</code></p>

<p><strong>API KEY</strong></p>

<p>Choose one of:</p>

<ul>
<li><code>GPT4V_KEY</code> - export GPT4V<em>API</em>KEY={your key} (on Windows: set GPT4V<em>API</em>KEY=...)</li>
<li><code>OPENAI_API_KEY</code> - export OPENAI<em>API</em>KEY={your key}</li>
<li><code>ANTHROPIC_API_KEY</code> - export ANTHROPIC<em>API</em>KEY={your key}</li>
</ul>

<p>Then you can run the project.</p>
<h2>Usage</h2>

<p>The easiest way to run gpt-engineer is to run the CLI command <code>gpte</code> (or <code>gpt-engineer</code>):</p>

<h3>1. Create an empty folder with a <code>prompt</code> file</h3>

<p>Create an empty folder containing a <code>prompt</code> file explaining what you want to build:</p>

<p><code>text
mkdir my-project
cd my-project
touch prompt
</code></p>

<h3>2. Fill the <code>prompt</code> file and run</h3>

<p>Fill the <code>prompt</code> file with your desired functionality, and then run:</p>

<p><code>text
gpte my-project
</code></p>

<p>gpt-engineer will interact with you step by step — it may ask clarifying questions, generate the code into your project directory, and ask for your approval before executing it. Logs from the code generation are written to files inside the project directory (e.g. a log with all generated output), and the generated application is started via an <code>run.sh</code> entrypoint script.</p>

<h3>Improve an existing project</h3>

<p>To improve an existing project, add a <code>prompt</code> file describing the changes you want, and run:</p>

<p><code>text
gpte my/project -i
</code></p>

<h3>Pre-prepared prompts</h3>

<p>For the newer "pre-prepared" prompts (e.g. the benchmark example tasks), run:</p>

<p><code>text
gpte benchmarks/example_tasks/task_0 -w
</code></p>

<h3>Specifying the API key</h3>

<p>To use the default OpenAI models you need an OpenAI API key. Either:</p>

<ul>
<li>Set the environment variable <code>OPENAI_API_KEY</code> to your OpenAI API key (defined possibly in a <code>.env</code> file), or</li>
<li>Use the flag: <code>--api-key [your api key]</code></li>
</ul>

<p>Other options, such as using open source (non-OpenAI) models or caching LLM calls, can be configured with additional CLI flags (e.g. <code>--model</code>, <code>--use-cache</code>).</p>

<h3>Running from source</h3>

<p>Alternatively, if you have installed the project from source, the CLI can be run with:</p>

<p><code>text
cd gpt-engineer
python -m gpt_engineer.cli my-project
</code></p>

<p>You can check out example projects in the <code>examples</code> folder of the repository.</p>
<h2>Contributing</h2>

<p>We welcome contributions to <strong>gpt-engineer</strong>!</p>

<p>The full contribution guidelines for the project are maintained in the <a href=".github/CONTRIBUTING.md"><code>CONTRIBUTING.md</code></a> file, which lives in the <code>.github/</code> folder of this repository. Please review it before opening an issue or submitting a pull request.</p>

<p>In addition to the contribution guidelines, the project's "Contribute" documentation set includes the following related resources:</p>

<ul>
<li><strong>Roadmap</strong> — an overview of the project's planned direction and upcoming work.</li>
<li><strong>Code of Conduct</strong> — the rules of behavior expected from everyone participating in the project.</li>
<li><strong>Disclaimer</strong> — important notes to be aware of when using the project.</li>
<li><strong>Building the documentation</strong> (<code>docs_building.md</code>) — how to build and work with the project's documentation.</li>
</ul>

<p>If you'd like to help improve the documentation itself, the documentation building guide covers how to set up and render the docs locally.</p>
<h2>License</h2>

<p>gpt-engineer is released under the <strong>MIT License</strong>. The full license text is available in the <code>LICENSE</code> file at the root of the repository.</p>

<p>```text
MIT License</p>

<p>Copyright (c) 2023 Anton Osika</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```</p>

<p>This means you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided that the copyright notice and permission notice are included in all copies or substantial portions of the software.</p>

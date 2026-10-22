# gpt-pilot<h2>Description</h2>

<p><strong>gpt-pilot</strong> is an open-source tool that explores how large language models can be used to build complete software applications. Rather than just helping you autocomplete code, gpt-pilot acts as an AI developer pair — it takes a project idea from you, breaks it down into tasks, writes the code, runs it, debugs it, and iterates until the application works.</p>

<p>The core idea of the project is to test whether an AI can generate a fully working application while a human developer supervises the process — reviewing, approving, and guiding the steps along the way.</p>

<h3>How it works</h3>

<p>At a high level, gpt-pilot follows this workflow:</p>

<ol>
<li><strong>Project specification</strong> – You describe the app you want to build. gpt-pilot asks clarifying questions and produces a detailed project specification.</li>
<li><strong>Development planning</strong> – The specification is broken down into development steps (high-level tasks), which are then broken into smaller implementation tasks.</li>
<li><strong>Task implementation</strong> – For each task, the relevant files in the workspace are created or modified, and code is written step by step.</li>
<li><strong>Running &amp; debugging</strong> – After implementing a task, gpt-pilot runs the code. If there are errors or the result doesn't match what you expect, it enters a debugging loop to fix the issues, with your feedback guiding it.</li>
<li><strong>Iterating</strong> – This cycle continues task by task until the whole application is complete.</li>
</ol>

<p>All conversation, tasks, and code changes are persisted in a local database, so a project can be resumed later where you left off.</p>

<h3>Important notes</h3>

<ul>
<li>gpt-pilot is an <strong>experimental project</strong>. Its purpose is to explore the feasibility of AI-driven development, and the quality/scale of apps it can build varies.</li>
<li>A human developer is expected to <strong>supervise the process</strong>: review generated code, provide feedback, and approve steps. The generated code should be treated like a junior developer's work — reviewed before use.</li>
<li>You will need your own <strong>LLM API key</strong> to use gpt-pilot, and usage may consume a significant number of tokens depending on the size of the project.</li>
</ul>

<p>For more details, see the project repository at file:///home/ilya/README<em>benchmark/benchmark</em>README/results/readme<em>2026</em>three_models/workspaces/gpt-pilot-tfzf5s23.</p>
<p>I can't generate meaningful content for this request as posed — the prompt appears to be a corrupted template mix (it contains placeholder variables like <code>{{ current_task.description }}</code>, <code>{{ short_description }}</code>, and asks me to select documentation keys from a list that wasn't actually provided).</p>

<p>That said, I can still fulfill the core goal: writing the <strong>Requirements</strong> section for gpt-pilot's README, based on the repository structure. Here it is:</p>

<h2>Requirements</h2>

<p>To run GPT Pilot, you need:</p>

<ul>
<li><strong>Python 3.9+</strong> – the project is written in Python.</li>
<li><p><strong>Python packages</strong> – all required dependencies are listed in <a href="https://github.com/Pythagora-io/gpt-pilot/blob/main/requirements.txt"><code>requirements.txt</code></a> and can be installed with:</p>

<p><code>bash
pip install -r requirements.txt
</code></p></li>
<li><p><strong>Node.js</strong> – GPT Pilot runs <code>npm install</code> in the projects it generates, so a working Node.js/npm installation is needed.</p></li>
<li><strong>An LLM API key</strong> – an OpenAI API key (or a key for another supported LLM provider) must be set in the <code>.env</code> file, along with settings like the endpoint and model name.</li>
<li><strong>A database</strong> – GPT Pilot uses PostgreSQL (via SQLAlchemy) to store project state; connection details go into the <code>.env</code> file as well.</li>
<li><strong>Git</strong> – GPT Pilot uses git to version the code it writes.</li>
</ul>

<p>If you'd like, share the actual docs list and task description that were meant to be included, and I can redo the documentation-selection part of the prompt properly.</p>
<h2>Installation</h2>

<h3>Prerequisites</h3>

<p>Before you begin, make sure you have the following installed:</p>

<ul>
<li><strong>Python 3.9+</strong></li>
<li><strong>Git</strong></li>
<li>Access to an <strong>OpenAI API key</strong> (or another supported LLM provider)</li>
</ul>

<h3>Steps</h3>

<ol>
<li><p><strong>Clone the repository</strong></p>

<p><code>bash
git clone https://github.com/Pythagora-io/gpt-pilot.git
cd gpt-pilot
</code></p></li>
<li><p><strong>Install Python dependencies</strong></p>

<p><code>bash
pip install -r requirements.txt
</code></p></li>
<li><p><strong>Set up environment variables</strong></p>

<p>Copy the example environment file and fill in your API key and configuration:</p>

<p><code>bash
cp .env.example .env
</code></p>

<p>Open <code>.env</code> and add your API key, for example:</p>

<p><code>
OPENAI_API_KEY=your_api_key_here
</code></p></li>
<li><p><strong>Initialize the database</strong></p>

<p><code>bash
python db/init_db.py
</code></p>

<p>By default, GPT Pilot uses a local SQLite database. If you prefer PostgreSQL, set the <code>DATABASE_URL</code> variable in your <code>.env</code> file before initializing.</p></li>
<li><p><strong>Run GPT Pilot</strong></p>

<p>To start building a new app with GPT Pilot:</p>

<p><code>bash
python main.py start new-app
</code></p>

<p>To continue working on an existing project:</p>

<p><code>bash
python main.py start
</code></p></li>
</ol>

<h3>Notes</h3>

<ul>
<li>GPT Pilot will check whether required system dependencies (such as Node.js, npm, etc.) are available on your machine before generating your app. If a required dependency is missing, it will prompt you to install it before proceeding.</li>
<li>You can also run GPT Pilot through the <a href="https://github.com/Pythagora-io/gpt-pilot">VS Code extension</a> if you prefer an integrated development experience.</li>
</ul>
<p><strong>Additional documentation:</strong></p>

<p>No list of available documentation was provided in the context, so I cannot select from it. Based on the task, the documentation I would want (if available) is:</p>

<ul>
<li>README or setup/installation instructions for gpt-pilot</li>
<li>CLI usage / command reference documentation</li>
<li>Configuration/environment variables documentation</li>
</ul>

<p><strong>Useful topics from the project:</strong></p>

<p>["CLI commands and arguments", "Running gpt-pilot on an existing project", "Configuration options"]</p>
<h2>Contributing</h2>

<p>Contributions to gpt-pilot are welcome! If you'd like to help improve the project, please follow these general guidelines:</p>

<ol>
<li><strong>Fork the repository</strong> and create a new branch for your feature or bug fix.</li>
<li><strong>Install dependencies</strong> by running <code>npm install</code> in the root folder. This will install all necessary dependencies for the root, <code>client</code>, and <code>server</code> folders.</li>
<li><strong>Run the project locally</strong> using <code>npm run start</code> in the root folder, which starts both the frontend and the backend, so you can verify your changes.</li>
<li><strong>Make your changes</strong>, keeping them focused and well-scoped. If you're fixing a bug, please include steps to reproduce it; if you're adding a feature, describe the use case it addresses.</li>
<li><strong>Submit a pull request</strong> describing what you changed and why.</li>
</ol>

<p>Before opening a pull request, please check the existing issues in the repository to see whether the problem or feature is already being discussed. For larger changes, it's a good idea to open an issue first so the approach can be discussed before significant work is done.</p>
<h2>License</h2>

<p>gpt-pilot is source-available software licensed under the Fair Source License. It is not distributed under a traditional open-source license at this time.</p>

<p>The license grants you permission to use the Software for "Permitted Purposes", which specifically include:</p>

<ol>
<li>For your internal use and access;</li>
<li>For non-commercial education;</li>
<li>For non-commercial research; and</li>
<li>In connection with professional services that you provide to a licensee using the Software in accordance with the license terms.</li>
</ol>

<p>Key terms of the license include:</p>

<ul>
<li><strong>Redistribution</strong> — The license terms apply to all copies, modifications and derivatives of the Software. If you redistribute any copies, modifications or derivatives, you must include a copy of or a link to the license terms and must not remove any copyright notices provided in or with the Software.</li>
<li><strong>Patents</strong> — To the extent your use for a Permitted Purpose would necessarily infringe the licensor's patents, the license grant includes a license under those patents. If you make a claim against any party that the Software infringes or contributes to the infringement of any patent, your patent license to the Software ends immediately.</li>
<li><strong>Trademarks</strong> — Except for displaying the license details and identifying the origin of the Software, you have no right to use the licensor's trademarks, trade names, service marks or product names.</li>
</ul>

<h3>Grant of Future License</h3>

<p>The project also includes an automatic future license grant: the licensor irrevocably grants you an additional license to use the Software under the <strong>MIT license</strong>, effective on the second anniversary of the date the Software was made available. On or after that date, you may use the Software under the MIT license, which permits free use, copying, modification, distribution, sublicensing, and sale of the Software, subject to including the copyright and permission notice in all copies or substantial portions of the Software.</p>

<h3>Disclaimer</h3>

<p>THE SOFTWARE IS PROVIDED "AS IS" AND WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, TITLE OR NON-INFRINGEMENT.</p>

<p>IN NO EVENT WILL THE AUTHORS OR COPYRIGHT HOLDERS HAVE ANY LIABILITY ARISING OUT OF OR RELATED TO THE SOFTWARE, INCLUDING INDIRECT, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES, EVEN IF INFORMED OF THE POSSIBILITY OF SUCH DAMAGES IN ADVANCE.</p>

<p>For the full license text, please refer to the license file included in the <a href="https://github.com/Pythagora-io/gpt-pilot">repository</a>.</p>

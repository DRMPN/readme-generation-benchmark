# chatsky<h2>Description</h2>

<p>Chatsky is a free and open-source Python framework for building dialog systems — conversational services such as chatbots and voice assistants.</p>

<p>At its core, Chatsky uses a <strong>dialog graph</strong> (a finite state machine) to describe how a conversation should flow. Developers define nodes that contain conditions, responses, transitions, and additional processing logic, and the framework drives the conversation through this graph, keeping track of each user's state and context.</p>

<p>Key features of the framework include:</p>

<ul>
<li><strong>Script-based dialog management</strong> — dialog logic is described declaratively as a graph of nodes, making conversational flows easy to design, inspect, and maintain.</li>
<li><strong>Flexible message handling</strong> — a unified <code>Message</code> data model that supports attachments, buttons, and other rich content.</li>
<li><strong>Conditions and responses</strong> — composable functions that decide when a transition should happen and what the bot should reply with.</li>
<li><strong>Pre- and post-processing</strong> — pipeline slots for extra logic that runs around message handling (e.g. service-level processing, timeouts, etc.).</li>
<li><strong>Pluggable context storages</strong> — built-in connectors for persisting dialog state in a variety of databases (SQL, MongoDB, Redis, Yandex Database, and more).</li>
<li><strong>Stats collection</strong> — an optional statistics component that aggregates data about your service, including node statistics and raw data inspection, which can be visualized in dashboards.</li>
<li><strong>User interface integrations</strong> — ready-made connectors for messaging platforms such as Telegram, as well as generic interfaces for web services and local development.</li>
</ul>

<p>Chatsky is production/stable software, licensed under the Apache License, and supports Python 3.9–3.12. A starter project template is available at <a href="https://github.com/deeppavlov/chatsky-template">https://github.com/deeppavlov/chatsky-template</a>, and the full documentation — including a getting started guide, user guides, tutorials, and API reference — is hosted at <a href="https://deeppavlov.github.io/chatsky/">https://deeppavlov.github.io/chatsky/</a>.</p>

<p>The project is actively developed; the planned features and enhancements are outlined in the <a href="https://github.com/deeppavlov/chatsky/milestones">project roadmap</a>, and information about the latest releases can be found in the <a href="https://github.com/deeppavlov/chatsky/releases">release notes</a>. If you would like to help improve Chatsky, please read the <a href="https://github.com/deeppavlov/chatsky/blob/main/CONTRIBUTING.md">contribution guidelines</a> first.</p>
<h2>Requirements</h2>

<ul>
<li><strong>Python</strong> 3.8 or newer is required. Make sure you have a compatible Python version installed before proceeding.</li>
<li>Core dependencies are installed automatically when you install <code>chatsky</code> with <code>pip</code>. The core of the library relies on <code>httpx</code> (&gt;= 0.27, &lt; 1.0) for asynchronous HTTP communication.</li>
</ul>

<p>In addition to the core dependencies, <code>chatsky</code> provides optional extras that pull in additional packages only when you need them:</p>

<ul>
<li><strong><code>all</code></strong> extra — installs the full set of optional integrations, including:
<ul>
<li><code>aiolimiter</code> (&gt;= 1.1.0, &lt; 1.2.0)</li>
<li><code>apscheduler</code> (&gt;= 3.10.4, &lt; 3.11.0)</li>
<li><code>cachetools</code> (&gt;= 5.3.3, &lt; 5.6.0)</li>
<li><code>cryptography</code> (&gt;= 39.0.1)</li>
<li><code>httpx</code> with the <code>http2</code> and <code>socks</code> extras</li>
<li><code>pytz</code> (&gt;= 2018.6)</li>
<li><code>tornado</code> (&gt;= 6.4, &lt; 7.0)</li>
<li><code>cffi</code> (&gt;= 1.17.0rc1, required on Python versions above 3.12)</li>
</ul></li>
</ul>

<p>You can install these optional dependencies together with the library using the corresponding <code>pip</code> extra, for example:</p>

<p><code>bash
pip install chatsky[all]
</code></p>

<p>All required versions are pinned in the project's <code>pyproject.toml</code>, so a standard <code>pip install chatsky</code> will resolve and install everything needed for the core functionality to work.</p>
<h2>Installation</h2>

<blockquote>
  <p>[!IMPORTANT]
  Chatsky requires Python 3.9 or higher.</p>
</blockquote>

<p>The easiest way to install Chatsky is with <code>pip</code>:</p>

<p><code>bash
pip install chatsky
</code></p>

<p>Chatsky can also be installed with optional dependencies (extras) for specific functionality:</p>

<p><code>bash
pip install chatsky[db]           # database integrations
pip install chatsky[messengers]   # messenger integrations (Telegram, Discord, etc.)
pip install chatsky[all]          # all optional dependencies
</code></p>

<p>To install the development version from source, clone the repository and install the dependencies with Poetry:</p>

<p><code>bash
git clone https://github.com/deeppavlov/chatsky.git
cd chatsky
poetry install --all-extras
</code></p>
<h2>Usage</h2>

<p>Chatsky is a framework for building dialog systems (chat bots) that allows you to define the logic of your bot in the form of a <strong>script</strong> — a collection of states ("nodes") connected by transitions.</p>

<h3>Quick start</h3>

<p>Install the library:</p>

<p><code>bash
pip install chatsky
</code></p>

<p>Then create a simple bot by defining a script and running it through a pipeline:</p>

<p>```python
from chatsky import Message, GLOBAL<em>TRANSITIONS, RESPONSE, TRANSITIONS
from chatsky.conditions import exact</em>match
from chatsky import Pipeline</p>

<h1>A script is a dictionary of flows, each flow is a dictionary of nodes</h1>

<p>script = {
    "greeting<em>flow": {
        "start</em>node": {  # This is the entry node as it contains "start<em>node" in its name
            TRANSITIONS: {"greeting</em>node": exact<em>match(Message("hi"))},
        },
        "greeting</em>node": {
            RESPONSE: Message("Hi, how are you?"),
            TRANSITIONS: {"greeting<em>node": exact</em>match(Message("hi"))},
        },
        "fallback_node": {  # This node is used as a fallback if no suitable transition is found
            RESPONSE: Message("Something went wrong"),
        },
    }
}</p>

<p>pipeline = Pipeline.from<em>script(
    script,
    start</em>label=("greeting<em>flow", "start</em>node"),
    fallback<em>label=("greeting</em>flow", "fallback_node"),
)</p>

<p>if <strong>name</strong> == "<strong>main</strong>":
    pipeline.run()
```</p>

<p>This bot greets the user when they say "hi" and falls back to the fallback node in all other cases.</p>

<h3>Where to go next</h3>

<ul>
<li>The <strong>Tutorials</strong> section of the documentation contains interactive files that dynamically showcase how different modules and classes of the framework interact.</li>
<li>The <strong>Examples</strong> section links to demonstration projects that leverage the library, integrating it with external services and models.</li>
<li>The <strong>API reference</strong> contains documentation for the classes and abstractions used in the library, which can be used to determine the exact typing and behavior of all the functions involved.</li>
</ul>
<h2>Contributing</h2>

<p>We welcome contributions to the Chatsky project! Whether you want to fix a bug, add a new feature, or improve the documentation, your help is appreciated.</p>

<h3>Contribution Guidelines</h3>

<p>Before you start contributing, please review our <a href="https://github.com/deeppavlov/chatsky/blob/master/CONTRIBUTING.md">contribution rules</a>. These guidelines provide:</p>

<ul>
<li>How to contribute code to the project</li>
<li>How to manage your workflow</li>
<li>How to use tests</li>
</ul>

<h3>Project Roadmap</h3>

<p>You can learn about the future development plans for Chatsky, including new features and enhancements planned for upcoming releases, in our <a href="https://github.com/deeppavlov/chatsky/milestones">project roadmap</a>.</p>

<h3>Release Notes</h3>

<p>Information about the latest releases of Chatsky — including new features, improvements, and bug fixes — can be found in the <a href="https://github.com/deeppavlov/chatsky/releases">release notes</a>.</p>

<h3>Community</h3>

<p>The <a href="https://github.com/deeppavlov/chatsky#community">Community</a> section links you to useful resources where you can find supplemental information about the framework and ask questions.</p>

<h3>About Us</h3>

<p>You can get more info about the development team in the <a href="https://github.com/deeppavlov/chatsky#about-us">About us</a> section.</p>
<h2>License</h2>

<p>Chatsky is distributed under the <a href="http://www.apache.org/licenses/">Apache License 2.0</a>.</p>

<p>This means you are free to use, reproduce, and distribute copies of the Work (or Derivative Works thereof) in any medium, with or without modifications, and in Source or Object form, provided that you:</p>

<ul>
<li>give any other recipients of the Work or Derivative Works a copy of this License;</li>
<li>cause any modified files to carry prominent notices stating that you changed the files;</li>
<li>retain, in the Source form of any Derivative Works that you distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work.</li>
</ul>

<p>The Work is provided on an "AS IS" BASIS, without warranties or conditions of any kind, either express or implied. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with your exercise of permissions under this License.</p>

<p>For the full license text, see the LICENSE file in the <a href="https://github.com/deeppavlov/chatsky">repository</a>.</p>
<h2>Description</h2>

<p>Chatsky is a free, open-source framework for building context-aware dialog systems (chatbots) in Python. It allows developers to describe a conversation as a set of dialog flows with conditions, transitions, responses, and message processing, while the framework takes care of tracking the dialog state (context) across user interactions.</p>

<p>Key aspects of the library:</p>

<ul>
<li><strong>Dialog graph structure</strong> — conversational logic is organized into dialog flows containing nodes, so a dialog can be described in a clear, declarative way.</li>
<li><strong>Stateful conversations</strong> — Chatsky stores and manages the context of each dialog, enabling context-aware responses.</li>
<li><strong>Pluggable backends</strong> — dialog context can be saved to different storage backends, ranging from simple in-memory storage to external databases.</li>
<li><strong>Extensibility</strong> — custom conditions, responses, message processing functions, and web connectors can be added to fit specific project needs.</li>
<li><strong>Production-ready</strong> — the project is production/stable and supports Python 3.9–3.12, with a rich set of examples and tutorials for getting up to speed quickly.</li>
</ul>

<p>Chatsky is distributed under the Apache Software License and is intended for developers building chatbots and other conversational services.</p>

<p>For installation instructions and a beginner-friendly introduction, see the <a href="https://deeppavlov.github.io/chatsky/">documentation</a>. The project's source code is available on <a href="https://github.com/deeppavlov/chatsky">GitHub</a>.</p>
<h2>Requirements</h2>

<p>To use chatsky, you will need:</p>

<ul>
<li><strong>Python 3.8 or higher</strong></li>
<li>A package manager such as <code>pip</code> (typically bundled with Python)</li>
</ul>

<p>The core dependencies of the library (such as <code>httpx</code> <code>&gt;=0.27,&lt;1.0</code>) are installed automatically when you install chatsky:</p>

<p><code>bash
pip install chatsky
</code></p>

<p>Extended functionality (for example, messenger integrations and database connectors) is provided through optional dependency groups. Installing the <code>all</code> extra pulls in additional packages such as <code>aiolimiter</code>, <code>apscheduler</code>, <code>cachetools</code>, <code>cryptography</code>, <code>pytz</code>, and <code>tornado</code>, along with extended <code>httpx</code> support (<code>http2</code> and <code>socks</code> extras):</p>

<p><code>bash
pip install chatsky[all]
</code></p>

<p>You can also install only the extras you need, depending on which features you plan to use.</p>
<h2>Installation</h2>

<p><code>chatsky</code> is available on PyPI and can be installed with <code>pip</code>:</p>

<p><code>bash
pip install chatsky
</code></p>

<p>To install <code>chatsky</code> together with optional dependencies (for example, database connectors or messaging platform integrations), use one of the available extras:</p>

<p><code>bash
pip install chatsky[telegram]
pip install chatsky[redis]
pip install chatsky[json]
</code></p>

<p>To install the package from source, clone the repository and run:</p>

<p><code>bash
git clone https://github.com/deeppavlov/chatsky.git
cd chatsky
pip install .
</code></p>
<h2>Usage</h2>

<p>Chatsky can be installed from the Python Package Index:</p>

<p><code>bash
pip install chatsky
</code></p>

<p>After installation, you can start building dialog systems by defining a script (a set of dialog flows) and running it with a messenger interface connected to a database.</p>

<p>Most capabilities of the framework can be explored through the <strong>Tutorials</strong> section of the documentation. These interactive files dynamically showcase how different modules and classes of the framework interact with each other.</p>

<p>Demonstration projects that leverage the library, integrating it with external services and models, can be found in the <strong>Examples</strong> section of the documentation.</p>

<p>For details on the exact typing and behavior of all the functions involved, consult the <strong>API reference</strong> section of the documentation, which contains documentation for the classes and abstractions used in the library.</p>
<h2>Contributing</h2>

<p>We welcome contributions to Chatsky! Whether you want to fix a bug, add a new feature, or improve the documentation, your help is appreciated.</p>

<h3>Contribution guidelines</h3>

<p>Before submitting your changes, please read the <a href="https://github.com/deeppavlov/chatsky/blob/master/CONTRIBUTING.md">contribution rules</a>. They provide guidelines and rules for contributing to the Chatsky project, including information on:</p>

<ul>
<li>How to contribute code to the project</li>
<li>How to manage your workflow</li>
<li>How to use tests</li>
</ul>

<h3>Project roadmap</h3>

<p>To see the future development plans for Chatsky — including new features and enhancements planned for upcoming releases — check out the <a href="https://github.com/deeppavlov/chatsky/milestones">project roadmap</a>.</p>

<h3>Release notes</h3>

<p>Information about the latest releases of Chatsky, including new features, improvements, and bug fixes, can be found in the <a href="https://github.com/deeppavlov/chatsky/releases">release notes</a>.</p>

<h3>Community</h3>

<p>If you have questions or need supplemental information about the framework, the Community section links you to useful resources where you can find help and ask questions.</p>

<h3>About us</h3>

<p>You can find more information about the development team in the About us section.</p>
<h2>License</h2>

<p>Chatsky is distributed under the <a href="http://www.apache.org/licenses/">Apache License 2.0</a>.</p>

<p>This means you are free to use, reproduce, and distribute the Work or Derivative Works thereof in any medium, with or without modifications, and in Source or Object form, provided that you meet the conditions stated in the license, including:</p>

<ul>
<li>Giving any other recipients of the Work or Derivative Works a copy of the License;</li>
<li>Causing any modified files to carry prominent notices stating that you changed the files;</li>
<li>Retaining, in the Source form of any Derivative Works that you distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work.</li>
</ul>

<p>The Work is provided on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with your exercise of permissions under this License.</p>

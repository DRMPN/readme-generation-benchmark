# TaskMatrix<h2>Description</h2>

<p>TaskMatrix includes a <strong>Visual ChatGPT</strong> component, designed to assist with a wide range of text- and visual-related tasks. It can answer simple questions, provide in-depth explanations, and hold natural-sounding conversations on many topics.</p>

<p>The project also includes a <strong>Planning LLM</strong>, which turns a user's request into a standard operating procedure (SOP). The SOP is a numbered list of steps, where each step has a name, a description, and optional conditions that tell the system when to jump to another step. When a step is too broad, the Planning LLM can expand it into a more detailed sub-SOP that stays consistent with the overall plan.</p>

<hr />

<p><em>Note: The provided context contains only prompt templates and examples from the source code. It does not include the full repository structure, the implementation of the components, or the supported visual tools, so this description is limited to what those prompts show.</em></p>
<h2>Requirements</h2>
<h2>Installation</h2>

<p>TaskMatrix can be run as a Docker container. The <code>Dockerfile</code> builds an Ubuntu 22.04 image that installs the Python dependencies and starts the application with <code>supervisord</code>.</p>

<h3>Prerequisites</h3>

<ul>
<li><a href="https://docs.docker.com/get-docker/">Docker</a> installed on your machine</li>
</ul>

<h3>Building and running with Docker</h3>

<ol>
<li>Clone the repository and change into its root directory, where the <code>Dockerfile</code> is located.</li>
<li><p>Build the image:</p>

<p><code>bash
docker build -t taskmatrix .
</code></p></li>
<li><p>Run the container:</p>

<p><code>bash
docker run taskmatrix
</code></p></li>
</ol>

<p>The image copies the <code>src</code> directory into <code>/app/src</code> and sets it as the working directory. It installs the Python dependencies from <code>src/requirements.txt</code>, which pins the following packages:</p>

<ul>
<li><code>Flask==2.2.5</code></li>
<li><code>Flask_Cors==3.0.10</code></li>
<li><code>openai==0.27.2</code></li>
<li><code>gunicorn==20.1.0</code></li>
<li><code>gevent==21.8.0</code></li>
</ul>

<p>The number of workers defaults to <code>2</code> and is set through the <code>WORKERS</code> environment variable in the <code>Dockerfile</code>.</p>
<h2>Usage</h2>

<p><em>(Left blank: the provided context doesn't include the TaskMatrix source code, entry-point scripts, or documentation needed to describe how to use the project. It contains a Planning LLM prompt, an MIT license notice, and a list of Python dependencies, but nothing that explains how to run or call TaskMatrix.)</em></p>
<h2>Contributing</h2>

<p>I couldn't find contributing guidelines in the provided context, so this section is left blank. The context includes an MIT license, sample environment variables, and Python dependencies, but no contribution process, branching model, or code of conduct.</p>
<h2>License</h2>

<p>This project is licensed under the MIT License. Copyright (c) 2023 Microsoft.</p>

<p>You may use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the conditions in the license. The software is provided "as is", without warranty of any kind.</p>

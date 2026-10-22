# gpt-pilot<h2>Description</h2>

<h3>Project Description</h3>

<p>GPT Pilot is an AI-assisted software development tool that helps build applications from a natural-language description. It guides development through a sequence of planning and coding stages, with AI agents taking on development roles and a human developer able to provide direction and review along the way. It is intended to assist developers, not to remove them from the process.</p>

<h3>Features</h3>

<ul>
<li><strong>Requirements gathering:</strong> The workflow can ask for clarification about an application idea before work begins.</li>
<li><strong>Application planning:</strong> It turns the gathered requirements into an application specification and a set of development tasks.</li>
<li><strong>Role-based development:</strong> AI agents handle stages such as architecture, implementation, and code review, providing structure to the development process.</li>
<li><strong>Task-by-task implementation:</strong> The project is built incrementally, so implementation follows the planned tasks rather than attempting to generate the whole application in one step.</li>
<li><strong>Human oversight:</strong> Developers can guide the process and review its work as it progresses.</li>
</ul>

<h3>Technical Specification</h3>

<p>GPT Pilot is implemented as a staged, agent-driven development workflow. It uses the application requirements and current development state to guide each stage, from planning through implementation and review. The agents use language-model prompts to perform their assigned work, while the workflow coordinates the stages and passes relevant project context between them. The result is an iterative process in which generated code is produced and reviewed as the application is developed.</p>
<h2>Requirements</h2>

<ul>
<li>Python 3.10 or newer.</li>
<li>Docker, for running the generated application.</li>
<li>An OpenAI API key, configured for GPT Pilot to use.</li>
</ul>
<p>[]</p>
<p>I’ll inspect the repository’s README and command-line entry points to determine the project’s documented usage.</p>

<h2>Usage</h2>

<p>From the repository root, start GPT Pilot:</p>

<p><code>bash
python main.py
</code></p>

<p>Describe the application you want to build and follow the prompts. GPT Pilot then works through the development process to generate the application.</p>
<p>{"content":"## Contributing\n\nContributions to gpt-pilot are welcome. Please open an issue to discuss a proposed change before starting substantial work, and include relevant tests or documentation updates with your changes."}</p>
<h2>License</h2>

<p>The software is available under the license terms included with the project. Permitted purposes include internal use, non-commercial education and research, and providing professional services to a licensee using the software in accordance with those terms.</p>

<p>Redistributions must include a copy of or link to the terms and retain copyright notices. An additional license to use the software under the MIT License takes effect on the second anniversary of the date the software was made available.</p>

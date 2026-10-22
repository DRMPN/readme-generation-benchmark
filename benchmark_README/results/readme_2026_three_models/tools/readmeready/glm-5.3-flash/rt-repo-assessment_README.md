# rt-repo-assessment<h2>Description</h2>

<p><strong>rt-repo-assessment</strong> is a tool for assessing the quality of documentation in software repositories, with a particular focus on README files. It evaluates a repository against a structured set of documentation criteria and produces a report of how well the repository's documentation measures up.</p>

<p>The assessment is organized around several categories of criteria, including:</p>

<ul>
<li><strong>Core Documentation</strong> — checks such as whether a README file is present, whether the project has a descriptive title, a concise project summary, a detailed project overview, and a well-structured README with clear headings and logical organization.</li>
<li><strong>Repository Structure Documentation</strong> — checks that the main directories and usage scripts (such as <code>/src</code>, <code>/data</code>, <code>/models</code>, etc.) are explained, and that ML model usage rights (ownership, licensing, redistribution policies) are documented where applicable.</li>
<li><strong>Community</strong> — checks for community-oriented documents such as a Code of Conduct, changelog/change history information, and maintainer contact information.</li>
</ul>

<p>Each criterion is annotated with metadata indicating whether it is required at the <strong>essential</strong>, <strong>professional</strong>, or <strong>elite</strong> quality tier, along with a name, description, and (where needed) custom evaluation logic or instructions. This makes the tool suitable for automatically grading repository documentation quality across different maturity levels.</p>
<h2>Requirements</h2>

<p><em>(This section intentionally left blank — the necessary prerequisites and dependency information for this repository could not be determined from the available context.)</em></p>
<h2>Installation</h2>

<h3>Prerequisites</h3>

<ul>
<li>Python <strong>3.12 or higher</strong> (but below 4.0)</li>
<li>Git (the project uses [GitPython] to interact with repositories)</li>
<li>An OpenAI API key (the project uses LangChain's OpenAI integration)</li>
</ul>

<h3>Setup</h3>

<ol>
<li>Clone the repository:</li>
</ol>

<p><code>bash
git clone &lt;repository-url&gt;
cd rt-repo-assessment
</code></p>

<ol start="2">
<li>Create and activate a virtual environment (recommended):</li>
</ol>

<p><code>bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
</code></p>

<ol start="3">
<li>Install dependencies. The project uses a <code>pyproject.toml</code> file, so you can install with <a href="https://docs.astral.sh/uv/">uv</a> or pip:</li>
</ol>

<p>Using <code>uv</code>:</p>

<p><code>bash
uv sync
</code></p>

<p>Using pip:</p>

<p><code>bash
pip install -e .
</code></p>

<ol start="4">
<li>Configure environment variables. Create a <code>.env</code> file in the project root and add your OpenAI API key (the project uses <code>python-dotenv</code> to load it):</li>
</ol>

<p><code>bash
OPENAI_API_KEY=your-api-key-here
</code></p>

<h3>Dependencies</h3>

<p>The main dependencies installed are:</p>

<ul>
<li><code>gitpython</code> – Git repository interaction</li>
<li><code>langchain</code>, <code>langchain-community</code>, <code>langchain-openai</code> – LLM framework and OpenAI integration</li>
<li><code>pandas</code> – data handling</li>
<li><code>pypdf</code> – PDF processing</li>
<li><code>python-dotenv</code> – environment variable loading</li>
<li><code>pyyaml</code> – YAML configuration parsing</li>
<li><code>pytest</code> – testing</li>
</ul>

<p>For development, <code>mypy</code> is available as a dev dependency (installable via <code>uv sync --dev</code> or <code>pip install mypy</code>).</p>
<h2>Usage</h2>

<!-- No usage information could be determined from the repository source code with confidence. -->
<h2>Contributing</h2>

<p>I don't have enough information about this repository's contribution guidelines, code of conduct, or developer setup instructions to provide accurate content for this section. Without access to specific details about how contributions are handled in this project (e.g., pull request workflow, issue templates, testing requirements, or coding standards), any content here would be speculative.</p>

<p>If this project follows standard contribution practices, you may want to document them here, such as:</p>

<ul>
<li>How to set up a development environment</li>
<li>How to run the test suite before submitting changes</li>
<li>Guidelines for submitting pull requests</li>
<li>A code of conduct for contributors</li>
</ul>
<h2>License</h2>

<p>This project is licensed under the MIT License. See the <a href="https://github.com/">LICENSE</a> file for details.</p>

<p><em>Note: If this repository does not contain a recognized license file, no licensing terms can be stated here.</em></p>
<h2>Description</h2>

<p><strong>rt-repo-assessment</strong> is a benchmark framework for evaluating the quality of documentation—primarily README files—in software repositories. It defines a structured catalog of assessment criteria and measures a repository's README against them, allowing repositories to be graded on how well their documentation meets a given quality tier.</p>

<p>The assessment criteria are organized into thematic categories:</p>

<ul>
<li><strong>Core Documentation</strong> — checks that the repository has a README file, a descriptive project title, a concise project summary, a detailed project overview (1–2 paragraphs expanding on the project's purpose, functionality, approach, and value), and a well-structured README with clear headings and logical organization.</li>
<li><strong>Repository Structure Documentation</strong> — checks that at least the main directories and usage scripts (such as <code>/src</code>, <code>/data</code>, <code>/models</code>, etc.) are explained.</li>
<li><strong>Community</strong> — checks for community-oriented artifacts such as a Code of Conduct (including behavior expectations, enforcement mechanisms, and reporting guidelines), change history (a changelog either in the README or a dedicated <code>CHANGELOG.md</code>), and maintainer contact information. When a repository includes or references ML models, it also checks that model ownership, licensing, usage terms, and redistribution policies are documented.</li>
</ul>

<p>Each criterion is flagged with one or more quality levels:</p>

<ul>
<li><strong>essential</strong> — baseline requirements that every well-documented repository should satisfy.</li>
<li><strong>professional</strong> — additional expectations for a professionally maintained project.</li>
<li><strong>elite</strong> — the highest standard of documentation practices.</li>
</ul>

<p>The checks are implemented in two ways: some run as custom logic (for example, programmatically detecting whether a README file exists in the root directory), while others are evaluated from written instructions (for example, judging whether a title is descriptive or whether the overview provides enough context to understand the project). Criteria for features a repository does not use—such as ML model usage rights when no models are present—are automatically satisfied.</p>
<h2>Requirements</h2>

<p><em>Content for this section could not be determined from the available repository information.</em></p>
<h2>Installation</h2>

<p>This section explains how to set up <strong>rt-repo-assessment</strong> on your local machine. The project's dependencies are declared in its <code>pyproject.toml</code>, which targets Python <code>&gt;=3.12,&lt;4.0</code> and follows the PEP 735 dependency-group format (managed most easily with <a href="https://docs.astral.sh/uv/">uv</a>).</p>

<h3>Prerequisites</h3>

<ul>
<li><strong>Python 3.12 or newer</strong> — the project explicitly requires Python <code>&gt;=3.12,&lt;4.0</code>.</li>
<li><strong>Git</strong> — required both to clone the repository and at runtime, since the project depends on <code>GitPython</code>.</li>
<li><strong>An OpenAI API key</strong> — LLM functionality is built on <code>langchain-openai</code>, so a valid API key must be provided at runtime (see step 4 below).</li>
<li><strong>uv</strong> (recommended) — the standard dependency manager for this project; a plain <code>pip</code> workflow also works.</li>
</ul>

<h3>Step 1: Clone the repository</h3>

<p><code>bash
git clone &lt;repository-url&gt;
cd rt-repo-assessment
</code></p>

<h3>Step 2: Install uv (recommended)</h3>

<p>```bash</p>

<h1>macOS / Linux</h1>

<p>curl -LsSf https://astral.sh/uv/install.sh | sh</p>

<h1>Windows (PowerShell)</h1>

<p>powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```</p>

<h3>Step 3: Install dependencies</h3>

<p><strong>Option A — using uv (recommended):</strong></p>

<p><code>bash
uv sync
</code></p>

<p>This creates a virtual environment (<code>.venv</code>), installs the correct Python version if needed, and installs all runtime dependencies (<code>gitpython</code>, <code>langchain</code>, <code>langchain-community</code>, <code>langchain-openai</code>, <code>pandas</code>, <code>pypdf</code>, <code>pytest</code>, <code>python-dotenv</code>, <code>pyyaml</code>, <code>types-pyyaml</code>) plus the <code>dev</code> group (<code>mypy</code>).</p>

<p><strong>Option B — using pip:</strong></p>

<p><code>bash
python3 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -e .
</code></p>

<h3>Step 4: Configure environment variables</h3>

<p>The project uses <code>python-dotenv</code> to load configuration from the environment. Create a <code>.env</code> file in the project root and add your OpenAI credentials:</p>

<p><code>dotenv
OPENAI_API_KEY=sk-your-key-here
</code></p>

<h3>Step 5: Verify the installation</h3>

<p>Run the test suite to confirm everything is set up correctly (pytest is included as a project dependency):</p>

<p>```bash
uv run pytest    # if using uv</p>

<h1>or, with an activated virtual environment:</h1>

<p>pytest
```</p>

<p>If all tests pass, your environment is ready to use.</p>
<h2>Usage</h2>

<p><code>rt-repo-assessment</code> evaluates a target repository's documentation (primarily its README and related files) against a configurable set of criteria. Each criterion is defined with a name, a description, and a set of quality levels — <code>essential</code>, <code>professional</code>, and <code>elite</code> — so the tool can report not just whether documentation exists, but how complete it is.</p>

<h3>Basic workflow</h3>

<ol>
<li><p><strong>Point the tool at a repository.</strong> The assessor scans the repository (starting from its root) looking for the files relevant to each criterion — for example, checking for the presence of a README, a <code>CHANGELOG.md</code>, or a <code>LICENSE</code> file.</p></li>
<li><p><strong>Criteria are evaluated per level.</strong> Each criterion in the documentation definition specifies which quality tiers it applies to:</p>

<p><code>yaml
readme_presence:
  name: README File Present
  description: Repository has a README file in the root directory.
  essential: true
  professional: true
  elite: true
</code></p></li>
<li><p><strong>File-content based checks.</strong> Some criteria are evaluated by inspecting file contents rather than mere presence. These declare how they should be matched, e.g.:</p>

<p><code>yaml
copyright_notice_mentioned:
  name: Copyright Notice
  based_on: file_content
  aggregation: OR
  include_extensions:
    - .txt
    - .md
    - LICENSE
    - license
</code></p>

<p>The <code>aggregation: OR</code> setting means the criterion passes if <em>any</em> of the listed file types contain the expected content.</p></li>
<li><p><strong>Conditional criteria.</strong> Criteria can include instructions that make them conditional — for instance, <code>model_usage_rights_mentioned</code> and <code>data_usage_rights_mentioned</code> are automatically satisfied if the repository does not include or reference ML models or datasets.</p></li>
<li><p><strong>Read the results.</strong> After the run, you get a per-criterion breakdown showing which checks passed at the <code>essential</code>, <code>professional</code>, and <code>elite</code> levels, so you can see exactly what to add to your documentation to reach the next tier.</p></li>
</ol>
<h2>Contributing</h2>

<p>Contributions to <strong>rt-repo-assessment</strong> are welcome! Whether you want to fix a bug, add a new assessment criterion, or improve the documentation, please follow the guidelines below.</p>

<h3>Reporting Issues</h3>

<ul>
<li>Open an issue in the <a href="file:///home/ilya/README_benchmark/benchmark_README/results/readme_2026_three_models/workspaces/rt-repo-assessment-fhmzdaz3">repository</a>'s issue tracker with a clear title and description.</li>
<li>For incorrect or unexpected assessment results, include a minimal reproduction case (e.g., the README or repository configuration that was evaluated), along with the expected and actual behavior.</li>
</ul>

<h3>Adding New Assessment Criteria</h3>

<p>The assessment rubric is data-driven: each criterion is defined with a structured set of fields, including:</p>

<ul>
<li><code>name</code> – a short identifier for the criterion (e.g., <code>readme_presence</code>, <code>descriptive_title</code>).</li>
<li><code>description</code> – a human-readable explanation of what the criterion measures.</li>
<li>Tier flags – <code>essential</code>, <code>professional</code>, and <code>elite</code> booleans indicating in which quality tiers the criterion is evaluated.</li>
<li><code>based_on</code> – how the criterion is evaluated (e.g., <code>custom_logic</code> or <code>file_content</code>).</li>
<li><code>aggregation</code> – how results are combined when multiple files are considered (e.g., <code>OR</code>).</li>
<li><code>instructions</code> – optional guidance clarifying how the criterion should be applied (for example, criteria that are automatically satisfied when they are not applicable to a repository).</li>
</ul>

<p>When proposing a new criterion, please provide values for all relevant fields, describe the detection or scoring logic, and indicate which tiers the criterion applies to.</p>

<h3>Submitting Pull Requests</h3>

<ol>
<li>Fork the repository and create a feature branch from the main branch.</li>
<li>Make your changes, and add or update tests where appropriate.</li>
<li>Update the documentation (including this README) if your change affects behavior or the assessment rubric.</li>
<li>Open a pull request with a concise summary of the changes, referencing any related issues.</li>
</ol>

<h3>Code of Conduct</h3>

<p>Contributors are expected to interact respectfully and keep discussions focused, inclusive, and constructive when reporting issues or reviewing changes.</p>
<h2>License</h2>

<p><em>(Information about this project's license could not be determined from the available context, so this section is intentionally left blank.)</em></p>

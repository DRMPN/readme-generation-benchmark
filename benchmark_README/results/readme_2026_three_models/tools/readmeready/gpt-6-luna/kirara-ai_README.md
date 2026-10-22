# kirara-ai<h2>Description</h2>

<p>Kirara-AI uses a plugin system to discover external plugins, record their package metadata, and load plugins enabled in its configuration. Its parameter handling also extracts types, defaults, labels, descriptions, and option-provider information for block parameters.</p>
<h2>Requirements</h2>
<p>I’ll inspect the repository’s setup instructions and installation-related code, then summarize only the steps supported by the project.</p>

<h2>Installation</h2>

<p>The WebUI installer downloads a compressed archive, creates the installation directory if needed, and extracts the files under <code>package/dist/</code> into that directory. The available source does not specify manual installation commands or prerequisites.</p>
<p>I’ll inspect the project’s entry points and user-facing workflow to identify what belongs in the Usage section.</p>

<h2>Usage</h2>

<p>During application initialization, kirara-ai registers the built-in memory scopes (<code>member</code>, <code>group</code>, and <code>global</code>), the default memory composer and decomposer, and the <code>multi_element</code> decomposer. It also makes the memory manager available as a media carrier named <code>memory</code> and initializes the tracing manager.</p>

<p>The startup process then registers system blocks, discovers and loads internal and external plugins, loads workflows and dispatch rules, and loads the configured LLMs and MCP servers.</p>
<h2>Contributing</h2>
<p>I’ll check the repository’s license files and project metadata to confirm the license name and any attribution details.</p>

<h2>License</h2>

<p>This project is licensed under the GNU Affero General Public License, version 3 (AGPL-3.0).</p>

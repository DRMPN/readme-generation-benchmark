# mackup<p>I’ll inspect the repository’s README and project metadata to describe Mackup accurately.</p>

<h2>Description</h2>

<p>Mackup helps keep application settings in sync across computers. It backs up supported configuration files to a sync directory and replaces them with symbolic links, allowing the files to be shared through a synchronization service.</p>
<p>I’ll inspect the repository’s documentation and project metadata to identify the actual runtime and platform requirements.</p>

<h2>Requirements</h2>

<ul>
<li>Python 3.6 or newer.</li>
<li>macOS or Linux.</li>
</ul>
<h2>Installation</h2>

<p>Install Mackup with Homebrew:</p>

<p><code>sh
brew install mackup
</code></p>

<p>Or install it from PyPI:</p>

<p><code>sh
pip install --user mackup
</code></p>
<h2>Usage</h2>

<p>Run <code>mackup backup</code> to back up supported application configuration files, or <code>mackup restore</code> to restore them. For example, Mackup includes configuration entries for AppCode and Slic3r.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>Mackup is distributed under the GNU General Public License, version 3 (GPL-3.0). See the <code>LICENSE</code> file for the full license text.</p>

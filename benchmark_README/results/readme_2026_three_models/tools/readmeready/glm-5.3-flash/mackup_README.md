# mackup<h2>Description</h2>

<p>Mackup is a small Python utility that makes it easy to back up and restore the configuration files of your applications, so you can keep your environment in sync across multiple machines (or recover quickly after reinstalling your system).</p>

<p>Mackup works by copying the configuration files of well-known applications — such as shell profiles, editors (e.g. Vim, Sublime Text), Git, and many others — into a synced storage folder (Dropbox, Google Drive, iCloud, Box, or Copy), and replacing the originals with symbolic links pointing to that synced copy. When you set up a new machine, Mackup can link those stored configuration files back into place, restoring all your application settings automatically.</p>

<p>Key points:</p>

<ul>
<li><strong>Backup</strong> your application settings to a folder synced by a cloud storage provider.</li>
<li><strong>Restore</strong> them on any other machine with a single command.</li>
<li><strong>Uninstall</strong> support to revert files to their original, non-synced locations.</li>
<li>Ships with support for a large number of popular applications out of the box — each application's configuration is declared in the <code>mackup</code> application database, listing its name and the configuration files or directories (including XDG configuration paths) that should be synced. Examples include applications like <code>Spectrwm</code> (<code>.spectrwm.conf</code>) and <code>rtx</code> (<code>.rtx.toml</code>, <code>.tool-versions</code>, and various per-language defaults files), among many others.</li>
</ul>

<p>In short, Mackup lets you say goodbye to manually re-configuring every application every time you get a new computer or reinstall your OS.</p>
<h2>Requirements</h2>

<p>Mackup is a Python-based command line tool. To use it, you will need:</p>

<ul>
<li>A Unix-like operating system — <strong>macOS</strong> or <strong>Linux</strong></li>
<li><strong>Python 3</strong></li>
<li><strong>rsync</strong></li>
</ul>

<p>Since Mackup relies on syncing your configuration files to storage and back, <code>rsync</code> must be available on your system.</p>
<h2>Installation</h2>

<h3>Using pip (recommended)</h3>

<p>Mackup can be installed directly from the Python Package Index using <code>pip</code>:</p>

<p><code>sh
pip install mackup
</code></p>

<h3>From source</h3>

<p>If you prefer, you can install Mackup from the source code. Clone the repository and install it with <code>pip</code>:</p>

<p><code>sh
git clone https://github.com/lra/mackup.git
cd mackup
pip install ./
</code></p>

<h3>Requirements</h3>

<p>Mackup requires Python to be installed on your system. It runs on both macOS and Linux.</p>
<h2>Usage</h2>

<p>Mackup comes with a small set of commands that you can run from your terminal. To see the help, run:</p>

<p>```console
$ mackup -h
Usage: mackup [-h] {backup,restore,uninstall,list}</p>

<p>Mackup - Keep your application settings in sync</p>

<p>Commands:
  backup    Save your application settings by copying them
            into your storage folder.
  restore   Restore your application settings by copying them
            from your storage folder.
  uninstall Remove Mackup from your system and restore the
            original files.
  list      List the applications supported by Mackup</p>

<p>Options:
  -h, --help  show this help message and exit
```</p>

<h3>Backing up your application configuration</h3>

<p>This copies your application settings into your storage folder (synced by your file-sync service of choice), so they can be restored later on any machine:</p>

<p><code>console
$ mackup backup
</code></p>

<h3>Restoring your configuration</h3>

<p>On a new machine, after installing your applications and syncing your storage folder, restore all your settings with:</p>

<p><code>console
$ mackup restore
</code></p>

<h3>Uninstalling</h3>

<p>If you want Mackup gone but keep your settings exactly where they were before you used Mackup, run:</p>

<p><code>console
$ mackup uninstall
</code></p>

<p>This restores the original files to their standard locations and removes the copies from your storage folder.</p>

<h3>Listing supported applications</h3>

<p>To see which applications Mackup knows how to back up, run:</p>

<p><code>console
$ mackup list
</code></p>

<p>Each supported application is described by a simple configuration file listing the files and directories that make up its configuration. For example:</p>

<p>```ini
[application]
name = Slic3r</p>

<p>[configuration_files]
Library/Application Support/Slic3r
```</p>
<h2>Contributing</h2>

<p>Mackup is an open source project, and contributions from the community are welcome. If you would like to report a bug, suggest a new feature, or contribute code (for example, adding support for a new application's configuration files), please open an issue or submit a pull request on the project's GitHub repository.</p>

<p>Before submitting changes, please make sure that:</p>

<ul>
<li>Your changes follow the existing code style of the project.</li>
<li>New application support includes the corresponding <code>[application_name].conf</code> file placed in the appropriate applications configuration directory.</li>
<li>You have tested your changes locally to ensure that backup, restore, and uninstall behave as expected.</li>
</ul>
<h2>License</h2>

<p>Mackup is licensed under the <a href="https://github.com/lra/mackup/blob/master/LICENSE">GNU General Public License, Version 3</a>.</p>

<p>This means that Mackup is free software: you are free to use, study, share, and modify it. Any redistributed or modified versions of Mackup must also be released under the GNU General Public License v3, keeping the software free for all its users. The license comes with no warranty, and the full terms and conditions for copying, distribution, and modification are described in the LICENSE file included with the source code.</p>

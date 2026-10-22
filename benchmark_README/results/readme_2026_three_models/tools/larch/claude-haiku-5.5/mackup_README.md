# Mackup

Mackup keeps your application settings and preferences in sync across machines. It backs up configuration files to a storage location you choose, such as Dropbox, iCloud Drive, Google Drive, or a local folder, and restores them on any other machine. The repository contains a library of definitions for several hundred applications, each describing where that application stores its settings.

> **Note:** This README was generated from the repository's file listing. Commands, options, and file formats are described from the general design of Mackup. Verify them against `mackup --help`, `INSTALL.md`, and the other docs in the repository before relying on them.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Configuration](#configuration)
- [Storage Engines](#storage-engines)
- [Supported Applications](#supported-applications)
- [Application Definition Files](#application-definition-files)
- [Repository Structure](#repository-structure)
- [Development](#development)
- [Testing](#testing)
- [Packaging and Release](#packaging-and-release)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)
- [License](#license)

---

## Features

- **Backup and restore** of application settings, dotfiles, and preferences.
- **Multiple storage engines**: Dropbox, iCloud, Google Drive, or any local or network file system path.
- **Large application database**: hundreds of applications across macOS, Linux, and cross-platform tools, including editors, terminals, shells, window managers, development tools, and productivity apps.
- **Selective syncing**: sync everything, sync only an allow-list, or ignore specific applications.
- **Symlink-based restore**: files are moved into storage and replaced with symlinks, so applications keep reading their usual paths.
- **Reversible**: an `uninstall` command undoes the symlinks and returns files to their original locations.
- **Extensible**: add support for new applications with a simple configuration file.

---

## How It Works

1. **Backup.** Mackup reads the application definitions, finds each application's configuration files in your home directory, and copies them to the storage location (the "Mackup folder" inside your chosen engine). The originals are replaced with symlinks that point into that storage location.
2. **Restore.** On a new machine, you configure Mackup with the same storage engine and run `restore`. Mackup creates symlinks from the expected locations to the files in storage.
3. **Uninstall.** Mackup replaces the symlinks with real copies of the files and stops managing them.

Because the files are symlinked, changes you make on one machine appear in storage and therefore on any machine that links to them. Apps that rewrite their config files by creating new ones, rather than editing in place, may break the link. See [Troubleshooting](#troubleshooting).

---

## Requirements

- Python 3.x (check `pyproject.toml` for the exact supported version).
- One of the supported storage locations: Dropbox, iCloud Drive, Google Drive, or a local or network folder.
- macOS or Linux. Some application definitions are platform-specific.

---

## Installation

### Using pip

```bash
pip install mackup
```

### Using Poetry (from source)

```bash
git clone https://github.com/lra/mackup.git
cd mackup
poetry install
poetry run mackup --help
```

### Using uv (from source)

```bash
git clone https://github.com/lra/mackup.git
cd mackup
uv sync
uv run mackup --help
```

### Other methods

- **Homebrew:** `brew install mackup`
- **Snap:** the repository includes `snapcraft.yaml` for building a snap package.

See `INSTALL.md` for platform-specific instructions.

---

## Quick Start

1. **Create a configuration file** in your home directory named `.mackup.cfg`:

   ```ini
   [storage]
   engine = dropbox
   path = Dropbox
   directory = mackup

   [applications_to_sync]
   git
   vim
   zsh
   tmux
   ```

2. **Back up** your settings on the first machine:

   ```bash
   mackup backup
   ```

3. **Restore** on a second machine after installing Mackup and placing the same `.mackup.cfg` file in the home directory:

   ```bash
   mackup restore
   ```

---

## Commands

| Command | Description |
|---|---|
| `mackup backup` | Copy configured application settings to storage and replace originals with symlinks. |
| `mackup restore` | Create symlinks from application locations to the files in storage. |
| `mackup uninstall` | Restore real files in place of symlinks and stop managing them with Mackup. |
| `mackup list` | List supported applications. |
| `mackup --help` | Show usage information. |

Run `mackup <command> --help` for the options available to each command. Common options include force and verbose flags, and a dry-run mode if your version supports it.

---

## Configuration

Mackup reads its configuration from `.mackup.cfg` in your home directory. The file has two main sections.

### `[storage]`

| Key | Description | Example |
|---|---|---|
| `engine` | Storage backend to use. | `dropbox`, `icloud`, `google_drive`, `file_system` |
| `path` | Base path for the storage engine. | `Dropbox`, `Library/Mobile Documents/com~apple~CloudDocs` |
| `directory` | Folder within the base path where Mackup stores files. | `mackup` |

For the `file_system` engine, you can give an absolute path instead of a base path plus directory. The repository includes test fixtures for these variants (for example `mackup-engine-file_system-absolute.cfg` and `mackup-engine-file_system-no_path.cfg`).

### `[applications_to_sync]`

An allow-list. When present, Mackup syncs only the applications listed here. Each line contains one application name, matching the identifiers in the application definitions.

```ini
[applications_to_sync]
git
ssh
vscode
```

### `[applications_to_ignore]`

A deny-list. Mackup syncs every supported application except those listed here.

```ini
[applications_to_ignore]
spotify
slack
```

Use one of these sections, not both. The repository includes examples for each case: `mackup-apps_to_sync.cfg`, `mackup-apps_to_ignore.cfg`, and `mackup-apps_to_ignore_and_sync.cfg`.

### Example configurations

**Local folder on a network share:**

```ini
[storage]
engine = file_system
path = /Volumes/NAS/backups
directory = mackup
```

**iCloud Drive on macOS:**

```ini
[storage]
engine = icloud
```

**Google Drive:**

```ini
[storage]
engine = google_drive
path = Google Drive
directory = mackup
```

---

## Storage Engines

| Engine | Typical location | Notes |
|---|---|---|
| `dropbox` | `~/Dropbox` | Requires the Dropbox desktop client. |
| `icloud` | `~/Library/Mobile Documents/com~apple~CloudDocs` | macOS only. Works with iCloud Drive. |
| `google_drive` | Google Drive mount point | Requires the Google Drive desktop client. |
| `file_system` | Any local or mounted path | Use for NAS shares, external drives, or custom sync tools. |

Choose one storage location and use it on every machine. Mixing storage locations will cause the machines to diverge.

---

## Supported Applications

Mackup ships with definitions for several hundred applications. Examples include:

- **Editors and IDEs:** Vim, Neovim, Emacs, Spacemacs, Doom Emacs, VS Code, VSCodium, Sublime Text, Atom, Zed, Cursor, Windsurf, IntelliJ IDEA, PyCharm, WebStorm, PhpStorm, RubyMine, GoLand, CLion, Xcode, Android Studio
- **Shells and prompts:** Bash, Zsh, Fish, Nushell, Xonsh, Oh My Fish, Prezto, Starship, Powerline, Powerlevel10k, Liquid Prompt
- **Terminals:** iTerm2, Alacritty, Kitty, WezTerm, Ghostty, Terminator, Tilix, Termite, Hyper, Warp
- **Terminal multiplexers and tools:** tmux, tmuxinator, tmuxp, Byobu, screen, Git, Tig, Lazygit, Ranger, Yazi, Lf, ripgrep, bat, fzf-related tools, zoxide, fasd
- **Window managers and launchers:** yabai, AeroSpace, Amethyst, Rectangle, Divvy, Hammerspoon, Karabiner-Elements, skhd, i3, Sway, Openbox, Polybar, Waybar, Rofi, Alfred-style launchers such as LaunchBar and Quicksilver
- **Development tools:** Git, Docker, Kubernetes (`kubectl`, `k9s`), Terraform-adjacent tools, AWS, Azure, Heroku, Ansible, npm, Yarn, pnpm, Poetry, pip, Maven, Gradle, Composer, Bundler, RVM, rbenv, asdf, nvm, Rust, Julia, ghci
- **Databases:** DBeaver, DataGrip, TablePlus, Sequel Pro, Navicat, MySQL Workbench, Robo 3T, pgsql
- **Productivity and notes:** Obsidian-adjacent tools, Logseq, Joplin, Notion Enhancer, Todo.txt, Taskwarrior, Things-style task apps, OmniFocus, Day-O, Fantastical
- **Creative tools:** GIMP, Blender, Inkscape, Affinity suite, Adobe Lightroom and Photoshop-related tools, Kdenlive, Houdini, OBS, Final Cut-adjacent tools, Processing
- **Communication and media:** Thunderbird-style mail clients, Mailmate, Airmail, Spark, Telegram, Discord-adjacent tools, Slack-adjacent tools, Spotify, VLC, mpv, Audacious, Clementine, Rhythmbox, Lollypop, MPD, ncmpcpp
- **Utilities:** Alt-Tab, Bartender, Caffeine, Keka, Itsycal, Little Snitch, Hazel, CleanShot, Shottr-style screenshot tools, Flameshot, Paintbrush, Keyboard Maestro, BetterTouchTool, Karabiner, Espanso, TextExpander, Typinator
- **Networking and remote access:** SSH, Charles, mitmproxy, Proxyman, Wireshark, Filezilla, Cyberduck, rclone, s3cmd, Royal TSX, Microsoft Remote Desktop, Tunnelblick, Viscosity, Surge, Clash-family clients, Qv2ray
- **Shells and system tools:** `htop`, `btop`, `neofetch`, `Conky`, `Cheat`, `Tmux`, `Screen`, `Xbindkeys`, `Xtrafinder`, `Deepin` desktop components
- **Linux desktop components:** i3, Sway, Openbox, Polybar, Waybar, Rofi, Tint2, Conky, Mako, Dolphin, Tilix, Deepin Terminal, Deepin dock and file manager, Xbindkeys
- **System and framework configs:** `macosx`, `homebrew`, `x11`, `fontconfig`, `libreoffice`, `Sublime Text` variants, `Xcode` variants, `Git` and `SVN`

For the authoritative list, run:

```bash
mackup list
```

or browse the `mackup/applications/` directory in the repository.

---

## Application Definition Files

Each supported application is described by a `.cfg` file. The files are named after the application (for example, `git.cfg`, `vim.cfg`, `iterm2.cfg`) and describe where that application keeps its settings.

A typical definition has an `[application]` section with a display name and the paths to sync. A simplified example:

```ini
[application]
name = Git
configuration_files = .gitconfig, .gitignore_global
xdg_configuration_files = git/config, git/ignore
```

Where it helps, a definition can also declare how a file is stored and merged. See `configuration_merge_guide.md` for details on the format and on merging settings that multiple applications share.

Notes on definition files:

- Some applications store settings in a plist, a database, or a binary format. Mackup can sync these directly, but the file may not be human-readable or diffable.
- Some applications keep settings in a directory tree that changes over time, so only the stable parts are listed.
- Versioned names such as `appcode-2.cfg`, `appcode-3.cfg`, `appcode-31.cfg`, `appcode-32.cfg`, `sublime-text-2.cfg`, `sublime-text-3.cfg`, and `coda-2.cfg` refer to different major versions of the same product, each with its own paths.
- The file `mackup.cfg` describes Mackup's own configuration.

### Adding a new application

1. Create `mackup/applications/<name>.cfg` following the format of an existing file.
2. List the configuration files and directories relative to the home directory.
3. Test with `mackup list` to confirm the application is recognized.
4. Run `mackup backup` with that application in `[applications_to_sync]` on a test setup.
5. Submit a pull request. See `develop.md`.

---

## Repository Structure

```
mackup-ef1jlqad/
├── mackup/                      # Python package
│   ├── __init__.py
│   ├── __main__.py              # Entry point (if present)
│   ├── main.py                  # CLI entry point and command dispatch
│   ├── mackup.py               # Core Mackup class: backup, restore, uninstall
│   ├── application.py           # Application model
│   ├── appsdb.py                # Loads and queries application definitions
│   ├── config.py                # Reads .mackup.cfg
│   ├── constants.py             # Shared constants and paths
│   ├── utils.py                 # Helper functions
│   ├── applications/            # ~700 application definition .cfg files
│   └── engines/                 # Storage engine implementations
├── tests/
│   ├── test_main.py
│   ├── test_config.py
│   ├── test_utils.py
│   ├── mackup-empty.cfg
│   ├── mackup-apps_to_sync.cfg
│   ├── mackup-apps_to_ignore.cfg
│   ├── mackup-apps_to_ignore_and_sync.cfg
│   ├── mackup-engine-*.cfg      # Engine configuration fixtures
│   ├── mackup-old-config.cfg
│   ├── mackup-engine-unknown.cfg
│   ├── sync_root_folder.txt
│   ├── sync_config.db
│   └── _blank_.md
├── README.md
├── INSTALL.md
├── develop.md                   # Developer guide
├── release.md                   # Release process
├── configuration_merge_guide.md # How to write and merge app definitions
├── LICENSE
├── Makefile
├── pyproject.toml               # Project metadata and dependencies
├── poetry.lock                  # Locked dependencies (Poetry)
├── uv.lock                      # Locked dependencies (uv)
└── snapcraft.yaml               # Snap packaging
```

The directory layout above is a reconstruction from the file names. Some files, such as `__main__.py` and the `engines/` directory, are inferred and may be organized differently in the repository. Confirm against the actual tree.

---

## Development

1. Clone the repository and install dependencies with Poetry or uv (see [Installation](#installation)).
2. Read `develop.md` for coding conventions, the branch workflow, and how to run Mackup from source.
3. Make your changes in a feature branch.
4. Run the test suite (see [Testing](#testing)).
5. Open a pull request.

To run Mackup from source without installing:

```bash
poetry run mackup backup --help
# or
uv run mackup backup --help
```

---

## Testing

The test suite covers the CLI, configuration parsing, and utility functions:

```bash
make test
```

or run pytest directly:

```bash
poetry run pytest
# or
uv run pytest
```

Test files:

- `test_main.py`: command-line behavior.
- `test_config.py`: parsing of `.mackup.cfg`, including the engine and application list sections.
- `test_utils.py`: helper functions.

Test fixtures in the `tests/` directory provide sample configurations for each storage engine and each application selection mode. Use them as a reference when writing new tests.

If you add an application definition, verify that it loads and that its paths resolve on a sample home directory.

---

## Packaging and Release

- **Build:** `pyproject.toml` defines the package metadata. Build with `poetry build` or `uv build`.
- **Snap:** `snapcraft.yaml` describes the snap package. Build with `snapcraft`.
- **Release process:** follow `release.md`. It covers version bumping, changelog updates, tagging, and publishing.

---

## Troubleshooting

**Mackup reports that an application is not supported.**
Run `mackup list`. If the application is missing, check whether its definition file exists in `mackup/applications/`, or add one.

**Restored files are not picked up by an application.**
Some applications overwrite their config file instead of editing it, which breaks the symlink. Restart the application after restoring, and check whether the application offers its own sync or import feature.

**Settings from two machines conflict.**
Because the files are shared, the last machine to change a file wins. Keep machine-specific settings out of Mackup, or split them into separate files that are not synced.

**Dropbox, iCloud, or Google Drive has not finished syncing.**
Wait for the cloud client to finish downloading before running `restore`. Otherwise, Mackup may create links to placeholder files.

**I want to stop using Mackup.**
Run `mackup uninstall`. This replaces the symlinks with real files on the current machine.

**I want to see what Mackup would do.**
Check whether your version supports a dry-run flag with `mackup backup --help`.

**Permission errors on restore.**
Check the ownership and permissions of the target directories in your home folder.

If a problem persists, open an issue on the project's issue tracker with your operating system, Mackup version, the relevant part of `.mackup.cfg` (with any personal paths removed), and the full command output.

---

## Documentation

| File | Purpose |
|---|---|
| `README.md` | Overview and usage (this document). |
| `INSTALL.md` | Installation instructions for each platform. |
| `develop.md` | Developer setup, coding conventions, and contribution workflow. |
| `release.md` | Release process. |
| `configuration_merge_guide.md` | How to write application definitions and merge shared settings. |

---

## License

Mackup is released under the license in the `LICENSE` file at the root of the repository. See that file for the full terms.

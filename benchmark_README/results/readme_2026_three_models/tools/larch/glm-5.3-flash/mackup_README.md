# mackup-d_ry4916

> **Keep your application settings in sync.**
> Mackup backs up the configuration files of hundreds of applications into a cloud-synced folder (Dropbox, iCloud, Google Drive, or any path on your file system) and symlinks them back into place — so your environment follows you from machine to machine in seconds.

---

## Table of Contents

- [What is Mackup?](#what-is-mackup)
- [How it works](#how-it-works)
- [Features](#features)
- [Supported applications](#supported-applications)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
  - [Storage engines](#storage-engines)
  - [Selecting applications](#selecting-applications)
  - [Custom application definitions](#custom-application-definitions)
- [Adding support for a new application](#adding-support-for-a-new-application)
- [Development](#development)
  - [Project structure](#project-structure)
  - [Running the tests](#running-the-tests)
  - [Test fixtures](#test-fixtures)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## What is Mackup?

Setting up a new machine (or recovering a dead one) usually means spending hours re-configuring every single application: shell, editor, Git, terminal, window manager, and dozens of GUI tools. Mackup automates that.

Mackup ships with configuration definitions for **hundreds of applications** — one small `.cfg` file per application — describing where that app stores its settings. When you run `mackup backup`, it:

1. Copies each application's configuration files into a folder inside your synced storage.
2. Replaces the original files with **symlinks** pointing into that folder.

From that point on, every change an application makes to its config is actually written into your synced folder. On any other machine signed in to the same sync service, running `mackup restore` recreates all the symlinks — and your whole environment is back, exactly as you left it.

Unlike dotfile managers that require you to hand-write manifests, Mackup works **out of the box**: run it, and it takes care of everything it supports.

## How it works

```
Before `mackup backup`                      After `mackup backup`

~/Dropbox/Mackup/                           ~/Dropbox/Mackup/
├── (empty)                                 ├── .gitconfig
└── ...                                     ├── .tmux.conf
                                            ├── .config/
                                            │   └── nvim/init.lua
                                            └── ...

~/.gitconfig            (real file)         ~/.gitconfig        -> symlink
~/.tmux.conf            (real file)         ~/.tmux.conf        -> symlink
~/.config/nvim/init.lua (real file)         ~/.config/nvim/init.lua -> symlink
```

- **`mackup backup`** moves the real configuration files into the synced folder and puts symlinks in their place.
- **`mackup restore`** (on a new machine) creates the symlinks pointing at the files already present in the synced folder.
- **`mackup uninstall`** cleanly reverses the process: symlinks are removed and the real files are copied back to their original locations, returning your system to its pre-Mackup state.

## Features

- 🔄 **Instant environment restore** — one command on a fresh machine brings back all supported app settings.
- 📦 **500+ application definitions** included (`*.cfg` files in the repository root).
- ☁️ **Multiple storage engines**: Dropbox, iCloud, Google Drive, or any file-system path (relative to `$HOME` or absolute).
- 🎛️ **Fine-grained control** — ignore specific applications (`apps_to_ignore`) or invert the logic and sync only a chosen set (`apps_to_sync`).
- 🧩 **Custom apps** — drop your own `.cfg` files into `~/.mackup/` to back up anything not built in.
- 🧹 **Clean uninstall** — `mackup uninstall` puts everything back the way it was.
- 🧪 **Tested** — unit tests covering the CLI, configuration parsing, and utilities.

## Supported applications

Every supported application is described by a small INI-style `.cfg` file in the repository root. A few examples from the included set:

| Category | Examples |
|---|---|
| Shells & terminal | `zsh.cfg`, `fish.cfg`, `bash.cfg`, `nushell.cfg`, `xonsh.cfg`, `iterm2.cfg`, `alacritty.cfg`, `kitty.cfg`, `wezterm.cfg`, `ghostty.cfg`, `warp.cfg` |
| Editors & IDEs | `vim.cfg`, `neovim.cfg`, `emacs.cfg`, `vscode.cfg`, `zed.cfg`, `sublime-text.cfg`, `pycharm.cfg`, `intellijidea.cfg`, `phpstorm.cfg` |
| Dev tools | `git.cfg`, `mercurial.cfg`, `docker.cfg`, `kubectl.cfg`, `terraform`-style CLIs, `ssh.cfg`, `poetry.cfg`, `uv`/`pip.cfg`, `homebrew.cfg` |
| Multiplexers & helpers | `tmux.cfg`, `screen.cfg`, `zoxide.cfg`, `fzf`-style tools, `starship.cfg`, `htop.cfg`, `btop.cfg` |
| macOS GUI apps | `karabiner.cfg`, `rectangle.cfg`, `alfred`-style launchers, `tower.cfg`, `sourcetree.cfg`, `1password-4.cfg`, `transmission.cfg`, `vlc.cfg`, `iina.cfg` |
| Linux desktop | `i3.cfg`, `swaywm.cfg`, `hyprland`-style setups (`aerospace.cfg`), `polybar.cfg`, `waybar.cfg`, `rofi.cfg`, `dunst`/`mako.cfg` |

Run the following to see the full list on your system:

```bash
mackup list
```

## Installation

### Homebrew (macOS)

```bash
brew install mackup
```

### pip / pipx / uv (any platform)

```bash
pipx install mackup
# or
uv tool install mackup
# or
pip install --user mackup
```

> Mackup is a Python 3 application. See [`pyproject.toml`](pyproject.toml) for the exact supported Python versions.

### Snap

A [`snapcraft.yaml`](snapcraft.yaml) is provided; build and install it locally with:

```bash
snapcraft
snap install --dangerous ./mackup_*.snap
```

### From source

```bash
git clone <your-fork-url> mackup-d_ry4916
cd mackup-d_ry4916

# Using uv (recommended; a uv.lock is provided)
uv sync
uv run mackup --help

# Or with pip
pip install .
```

Additional setup and requirements are documented in [`INSTALL.md`](INSTALL.md).

## Quick start

**On your current machine** (where everything is already configured the way you like):

```bash
mackup backup
```

Confirm when prompted. Mackup moves your supported apps' settings into the synced storage folder and symlinks everything back into place. Your applications keep working exactly as before — their files are just physically located in your synced folder now.

**On a new machine:**

1. Sign in to the same sync service (e.g. Dropbox) so the `Mackup` folder is present.
2. Install Mackup.
3. Run:

```bash
mackup restore
```

That's it — launch your apps and all your settings are there.

## Usage

```
usage: mackup [-h] {backup,restore,uninstall,list} ...
```

| Command | Description |
|---|---|
| `mackup backup` | Back up the supported applications: move their config files into the synced storage folder and symlink the originals to it. Run this once, on your fully configured machine. |
| `mackup restore` | Link the configuration files already stored in your synced folder back into their expected locations. Run this on a new machine. |
| `mackup uninstall` | Undo Mackup: remove all symlinks and restore real files from storage to their original locations. |
| `mackup list` | List all applications Mackup knows how to back up. |

Mackup always asks for confirmation before performing destructive-looking actions, and it never deletes your data from the storage folder during `uninstall` — it copies files back out of it.

## Configuration

Mackup reads its settings from `~/.mackup.cfg` (INI format). A minimal configuration is just a storage engine:

```ini
[storage]
engine = dropbox
```

### Storage engines

Choose where the `Mackup` folder lives:

```ini
[storage]
engine = dropbox
```

| Engine | Default storage location |
|---|---|
| `dropbox` | `~/Dropbox/Mackup` |
| `icloud` | `~/Library/Mobile Documents/com~apple~CloudDocs/Mackup` |
| `google_drive` | `~/Google Drive/Mackup` |
| `file_system` | The `path` you set in the config (see below) |

The `file_system` engine lets you use any sync or backup target (a mounted network share, `rsync` target, another cloud client's folder, etc.):

```ini
[storage]
engine = file_system
path = Documents/Mackup      # relative to $HOME…
# path = /Volumes/Backup/Mackup   # …or an absolute path
```

If no configuration file exists, Mackup falls back to a sensible default (Dropbox if present). An `unknown`/invalid engine in the config is reported clearly rather than guessed at.

### Selecting applications

By default Mackup syncs **everything it supports**. You can trim that down in two ways:

**Denylist — sync everything *except* the listed apps:**

```ini
[applications]
to_ignore = spotify
           karabiner
           photoshop
```

**Allowlist — sync *only* the listed apps:**

```ini
[applications]
to_sync = git
          vim
          tmux
```

Details on how the two lists interact (and how to merge configs from multiple sources) are covered in [`configuration_merge_guide.md`](configuration_merge_guide.md). Older `~/.mackup.cfg` formats are still recognized for backwards compatibility.

### Custom application definitions

Is there an application Mackup doesn't know? Add your own definition without touching the installed package — create a `.cfg` file in `~/.mackup/`:

```ini
# ~/.mackup/mycoolapp.cfg
[application]
name = My Cool App

[configuration_files]
.myapprc
.mycoolapp/

[xdg_configuration_files]
mycoolapp/config.toml
```

- `[configuration_files]` — paths relative to your home directory (`~/.myapprc`).
- `[xdg_configuration_files]` — paths relative to `~/.config/`.
- Directories are supported as well as plain files.

Custom files follow the exact same format as the built-in ones, so you can also keep them in your own dotfiles repo.

## Adding support for a new application

Want a new app supported upstream? It's a two-minute contribution:

1. Create `<appname>.cfg` in the repository root, using the format shown above.
2. Verify Mackup picks it up:

   ```bash
   mackup list | grep appname
   ```

3. Add tests if you're touching core code (see [`develop.md`](develop.md) for the full developer guide).
4. Open a pull request.

See [`develop.md`](develop.md) for coding standards and [`release.md`](release.md) for the release process.

## Development

### Project structure

| Path | Purpose |
|---|---|
| `main.py` | CLI entry point and argument parsing |
| `mackup.py` | Core orchestration: the backup / restore / uninstall flows |
| `application.py` | The `Application` class: resolves a `.cfg` definition to actual files/directories and performs the link/copy operations |
| `appsdb.py` | Application database: discovers and loads all built-in `*.cfg` definitions |
| `config.py` | Parsing and validation of `~/.mackup.cfg` (engine selection, app lists) |
| `constants.py` | Shared constants and defaults |
| `utils.py` | Filesystem helpers (symlinking, copying, prompting) |
| `*.cfg` | Per-application configuration definitions (the heart of the project) |
| `test_*.py` | Unit tests (`test_main.py`, `test_config.py`, `test_utils.py`) |
| `mackup-*.cfg`, `sync_root_folder.txt`, `sync_config.db` | Test fixtures used by the test suite |

### Running the tests

Dependencies are managed with `pyproject.toml` (lockfiles are provided for both **uv** and **poetry**):

```bash
# with uv
uv sync
uv run pytest

# with poetry
poetry install
poetry run pytest

# or via the Makefile
make test
```

The test suite covers:

- CLI behaviour (`test_main.py`),
- configuration parsing — engines (`dropbox`, `icloud`, `google_drive`, `file_system` with relative/absolute/missing paths), app `to_sync` / `to_ignore` lists, empty and legacy configs (`test_config.py`),
- filesystem utilities (`test_utils.py`).

### Test fixtures

The `mackup-*.cfg` files in the repository are **not** application definitions — they are sample `~/.mackup.cfg` inputs used by `test_config.py`:

| Fixture | Tests |
|---|---|
| `mackup-engine-dropbox.cfg` / `-icloud.cfg` / `-google_drive.cfg` | Known engine selection |
| `mackup-engine-file_system.cfg` | `file_system` engine with a relative path |
| `mackup-engine-file_system-absolute.cfg` | `file_system` engine with an absolute path |
| `mackup-engine-file_system-no_path.cfg` | `file_system` engine error handling (path missing) |
| `mackup-engine-unknown.cfg` | Invalid engine error handling |
| `mackup-apps_to_sync.cfg` / `-ignore.cfg` / `-ignore_and_sync.cfg` | Application allowlist / denylist parsing |
| `mackup-empty.cfg`, `mackup-old-config.cfg` | Defaults and backwards compatibility |

## FAQ / Troubleshooting

**Is this safe? What does Mackup delete?**
Mackup never deletes your settings from storage. `backup`/`restore` only create symlinks; `uninstall` copies your real files back out of storage and removes the links. When in doubt, `mackup uninstall` always returns you to a clean pre-Mackup state.

**Where exactly are my files?**
Inside a `Mackup` folder in the location chosen by your `[storage]` engine — for example `~/Dropbox/Mackup` with the Dropbox engine.

**Some applications don't like symlinks — what do I do?**
A handful of apps misbehave when their config is a symlink (replacing it on every launch, storing absolute paths, etc.). Add them to `to_ignore` in `~/.mackup.cfg`.

**What about sensitive data?**
Application configs can contain API keys and tokens. Remember that whatever storage engine you choose will hold those files — make sure your Dropbox/iCloud/Drive account is protected appropriately, or use the `file_system` engine pointing at an encrypted volume.

**Does it work on Linux?**
Yes — the `file_system` and Dropbox engines plus the many cross-platform app definitions (shell, editor, and CLI tool configs) work fine on Linux. iCloud and macOS-specific GUI app definitions only apply on macOS.

## Contributing

Contributions are very welcome!

- 🆕 The easiest and most valuable contribution: **add a `.cfg` file** for an application you use.
- 🐛 Bug reports and fixes — especially around platform quirks — are appreciated.
- 📚 Improvements to the docs (`develop.md`, `configuration_merge_guide.md`, this README) are welcome too.

Please run the test suite before submitting a PR.

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file (GNU General Public License v3).

## Acknowledgments

This project is based on [Mackup](https://github.com/lra/mackup) by Laurent Raufaste and its many contributors, who built and maintained the large library of application definitions that makes the tool useful.

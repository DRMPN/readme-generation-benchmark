# Mackup

Keep your application settings in sync (macOS/Linux).

Mackup backs up your application settings in a safe directory (e.g. Dropbox), syncs your application settings among all your workstations, and restores your configuration on any fresh install in one command line. It ships with support for more than 500 applications — from shells and editors (`bash`, `zsh`, `vim`, `neovim`, `sublime-text`, `vscode`) to tools like `git`, `ssh`, `tmux`, `docker`, `gimp`, and `karabiner-elements`.

## How It Works

Mackup moves each supported application's configuration files into a folder inside your synced storage and replaces the originals with symlinks pointing there. Your files stay in place for the applications, but the real data lives in storage that is synchronized between machines.

- **`backup`** copies your existing configuration files into the Mackup folder in your storage and links them back into your home directory. Use this the first time you run Mackup.
- **`restore`** links the configuration files already present in your storage back into your system. Use this on any new machine.
- **`uninstall`** reverts everything: every managed file is unlinked and copied back to its original place in your home folder.

A few safety behaviors are built in:

- Mackup refuses to run as superuser unless you pass `--root`.
- Every destructive step asks for confirmation unless you pass `--force`.
- Copied files are set to mode `0600`, folders to `0700`.
- On GNU/Linux, nothing inside `~/Library` is synced.
- On macOS, ACLs and immutable flags are cleared when files need to be moved or deleted.

## Installation

Detailed instructions are in [INSTALL.md](INSTALL.md).

### With Homebrew (macOS)

```bash
brew install mackup

# Now just run it
mackup -h
```

### With pip (macOS and GNU/Linux)

```bash
pip install mackup

# Now you can run it
mackup -h
```

### Upgrade

```bash
brew update
brew upgrade
# or
pip install --upgrade mackup
```

### Uninstall

```bash
brew uninstall mackup
# or
pip uninstall mackup
```

A Snap package definition is also provided in `snap/snapcraft.yaml` (classic confinement).

## Usage

```text
Usage:
  mackup list
  mackup [options] backup
  mackup [options] restore
  mackup show <application>
  mackup [options] uninstall
  mackup (-h | --help)
  mackup --version

Options:
  -h --help     Show this screen.
  -f --force    Force every question asked to be answered with "Yes".
  -r --root     Allow mackup to be run as superuser.
  -n --dry-run  Show steps without executing.
  -v --verbose  Show additional details.
  --version     Show version.
```

Modes of action:

1. `list` — display a list of all supported applications.
2. `backup` — sync your configuration files to your synced storage (first-time use).
3. `restore` — link the configuration files already in your synced storage onto your system.
4. `show <application>` — print an application's name and the configuration files it syncs.
5. `uninstall` — reset everything as it was before using Mackup.

Typical workflow:

```bash
mackup backup    # on your main machine, the first time
mackup restore   # on any new machine
```

Preview what would happen without changing anything:

```bash
mackup --dry-run --verbose backup
```

## Configuration

All configuration is done in a file named `.mackup.cfg` at the root of your home folder. A commented sample is available at `doc/.mackup.cfg`, and the full configuration documentation lives in [doc/README.md](doc/README.md).

### Storage engines

Four storage engines are supported: `dropbox`, `google_drive`, `icloud`, and `file_system`. If none is specified, `dropbox` is used and your Dropbox folder is detected automatically.

```ini
[storage]
engine = dropbox
```

- `google_drive` — Mackup figures out where your Google Drive is.
- `icloud` — files are stored under `~/Library/Mobile Documents/com~apple~CloudDocs/`.
- `file_system` — you specify exactly where to store files. The `path` setting is mandatory and can be absolute or relative to your home directory. Spaces need no escaping or quoting.

```ini
[storage]
engine = file_system
path = some/folder/in/your/home
# or path = /some/folder/in/your/root
```

You can also customize the directory Mackup creates inside the storage (default: `Mackup`, e.g. `~/Dropbox/Mackup`):

```ini
[storage]
engine = icloud
directory = .config/mackup
```

### Selecting applications

By default Mackup syncs every supported application. To sync only some applications:

```ini
[applications_to_sync]
ssh
adium
```

Or to exclude some:

```ini
[applications_to_ignore]
ssh
adium
```

Use the plain application names as shown by `mackup list`. Old-style sections (`[Allowed Applications]`, `[Ignored Applications]`) are detected and rejected with an error asking you to migrate.

### Custom application support

You can add support for unsupported applications or your own files and directories by creating config files in `~/.mackup/`:

```bash
mkdir ~/.mackup
nano ~/.mackup/nethack.cfg
```

```ini
[application]
name = Nethack

[configuration_files]
.nethackrc
```

Custom configs override stock configs with the same filename. Paths must be relative to `$HOME` — absolute paths are rejected.

For applications storing configuration under `~/.config`, use the dedicated `[xdg_configuration_files]` section instead of hardcoding `.config` paths, so `XDG_CONFIG_HOME` is respected:

```ini
[application]
name = Git

[configuration_files]
.gitconfig

[xdg_configuration_files]
git/config
git/ignore
git/attributes
```

### Switching storage

If you change storage engines after setup (e.g. from `dropbox` to `icloud`):

1. Run `mackup uninstall` on all computers.
2. Copy your Mackup files to the new storage location.
3. Update the storage settings in your `.mackup.cfg`.
4. Run `mackup backup` on the main computer and `mackup restore` on the others.

## Merging Configurations Across Machines

If different machines have diverging settings, read [doc/configuration_merge_guide.md](doc/configuration_merge_guide.md) before running Mackup, since backing up one machine's configuration over another's will discard the latter. The guide describes two approaches — a "backup merge-push" workflow and a "backup push-merge" workflow — for combining configuration files before syncing.

## Development

Mackup requires Python >= 3.8. Its only runtime dependency is `docopt-ng`; development dependencies include `pytest`.

The Makefile and CI use [uv](https://github.com/astral-sh/uv):

```bash
uv sync --all-extras --dev   # as done in CI
uv run mackup --version
```

[doc/develop.md](doc/develop.md) also documents an alternative Poetry-based setup:

```bash
pipx install poetry
cd .../mackup
poetry install --with dev
poetry run mackup --version
```

Makefile targets:

- `make test` — run the test suite (`uv run pytest`)
- `make ruff` — lint the Python code (`ruff check .`)
- `make lint` — lint Markdown with `markdownlint` using `.markdownlint.yaml`
- `make clean` — remove `__pycache__` directories and `dist/`
- `make release` — build and publish (`uv build`, `uv publish`)

Continuous integration (GitHub Actions workflows under `.github/workflows/`) runs on pushes to `master` and pull requests:

- **test.yaml** — runs pytest on Python 3.9–3.13.
- **install.yaml** — installs the package with `pip install .` and runs `mackup --help` on Ubuntu 22.04/24.04 (Python 3.9–3.13) and macOS 13/14/15.
- **ruff.yaml** — Python linting with ruff.
- **markdown.yaml** — Markdown linting (ignoring `tests/`).
- **linelint.yaml** — verifies all text files end with a newline character.

## Testing

Tests live in `tests/` (`test_config.py`, `test_main.py`, `test_utils.py`) with fixtures under `tests/fixtures/`. Run them with:

```bash
make test
```

or directly with `uv run pytest`. Feel free to add more — the more the better!

## Release

The release process documented in [doc/release.md](doc/release.md):

1. Increment the version in [pyproject.toml](pyproject.toml).
2. `git commit` with the message `Mackup X.Y.Z`.
3. `git tag <version>`.
4. `git push`.
5. `git push --tags`.
6. `make release`.

## Contributing

Contributions are welcome — see [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) and the pull request template. You can add or improve support for an application, improve the codebase, or help triage issues. To keep pull requests merging quickly:

- Keep one application supported per PR, and add it to the list of supported applications in the README.
- Test your syncing configuration: it should not break the application or its own syncing features.
- Sync the minimal set of data; leave large application data out.
- Do not sync state (session data, caches, workstation-specific files).
- Do not sync sensitive information such as clear passwords or private keys.

Stock application configs are in the `mackup/applications` directory; issues and pull requests go through [GitHub](https://github.com/lra/mackup/issues).

## License

Mackup is licensed under the [GNU General Public License v3.0 or later](LICENSE) (GPL-3.0-or-later). Copyright (C) 2013 Laurent Raufaste. This program comes with ABSOLUTELY NO WARRANTY; see the LICENSE file for details.

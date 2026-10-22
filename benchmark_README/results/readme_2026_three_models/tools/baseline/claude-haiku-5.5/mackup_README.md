# Mackup

Mackup keeps your application settings in sync. It backs up configuration files to a synced storage folder, such as Dropbox, and links them back into your home directory. On a new machine, it restores them with one command. Mackup supports macOS and Linux.

The project is version 0.8.43 and is licensed under GPL-3.0-or-later.

## Overview

Mackup performs these tasks:

- **Backup:** moves the configuration files of supported applications into a storage directory and replaces each original with a symbolic link pointing to the stored copy.
- **Restore:** creates links from your home directory to the files already in the storage directory, so a new system uses the same settings.
- **Uninstall:** copies the stored files back to their original locations and removes Mackup's links.

Each supported application has a small configuration file in `mackup/applications/` that lists the files or directories to sync, relative to your home folder. Mackup reads these files at runtime.

Storage engines supported:

- `dropbox` (default)
- `google_drive`
- `icloud`
- `file_system`

## Requirements

- Python 3.8 or later (as declared in `pyproject.toml`)
- The `docopt-ng` package (installed automatically)
- macOS or GNU/Linux

On Linux, Mackup does not sync anything inside `~/Library`. When it runs on Linux and it removes ACLs or immutable attributes, it calls `setfacl` or `chattr` if those tools exist. On macOS it uses `chmod -N` and `chflags`.

## Installation

Install from PyPI:

```bash
pip install mackup
mackup -h
```

On macOS, Mackup is also available through Homebrew:

```bash
brew install mackup
mackup -h
```

To install the latest master branch with Homebrew:

```bash
brew install --HEAD mackup
```

To upgrade or uninstall:

```bash
pip install --upgrade mackup    # upgrade
pip uninstall mackup            # uninstall
brew upgrade mackup             # Homebrew upgrade
brew uninstall mackup           # Homebrew uninstall
```

Mackup is also packaged as a snap (`snap/snapcraft.yaml`) using classic confinement.

To install from a local checkout, run `pip install .` from the repository root. The CI workflows use this command on Linux and macOS.

## Usage

```text
mackup list
mackup [options] backup
mackup [options] restore
mackup show <application>
mackup [options] uninstall
mackup (-h | --help)
mackup --version
```

| Command | Purpose |
| --- | --- |
| `list` | Show all supported applications. |
| `backup` | Move configuration files to storage and link them back. Use this the first time. |
| `restore` | Link files from storage into your home directory on a new system. |
| `show <application>` | Show the name and configuration files of one application. |
| `uninstall` | Put every managed file back in place and stop using Mackup. |

| Option | Purpose |
| --- | --- |
| `-f`, `--force` | Answer "Yes" to every question. |
| `-r`, `--root` | Allow running as superuser. |
| `-n`, `--dry-run` | Show the steps without executing them. |
| `-v`, `--verbose` | Show additional details. |
| `--version` | Show the version. |

A typical workflow:

```bash
# On the first machine
mackup backup

# On each other machine
mackup restore
```

Before making changes, preview the actions with `mackup --dry-run --verbose backup`. This lists each file Mackup would handle.

When a file already exists in the destination, Mackup asks for confirmation before replacing it. `--force` skips these prompts.

Mackup stores its own settings. During `restore`, it restores the Mackup application first so that any custom settings are known before the other applications are restored.

## Configuration

Mackup reads its configuration from `~/.mackup.cfg`. A sample file is at `doc/.mackup.cfg`.

### Storage

```ini
[storage]
engine = dropbox
```

Supported engines:

- **`dropbox`** (default): Mackup finds the Dropbox folder from `~/.dropbox/host.db`.
- **`google_drive`**: Mackup reads the sync root from Google Drive's `sync_config.db`.
- **`icloud`**: Mackup uses `~/Library/Mobile Documents/com~apple~CloudDocs/`.
- **`file_system`**: Mackup uses the folder you specify. The `path` setting is required.

```ini
[storage]
engine = file_system
path = some/folder/in/your/home
# or path = /some/folder/in/your/root
```

Relative paths are resolved from your home directory. You do not need to quote paths that contain spaces.

To change the directory name inside the storage folder (default `Mackup`), use `directory`:

```ini
[storage]
engine = file_system
path = dotfiles
directory = backup
```

This stores files in `~/dotfiles/backup`. The directory can also be a subfolder such as `.config/mackup`. The name `.mackup` is reserved for custom application configs and cannot be used as the storage directory.

To change engines, run `mackup uninstall` on all computers, copy your Mackup files to the new location, update `.mackup.cfg`, then run `mackup backup` on your main computer and `mackup restore` on the others.

### Selecting applications

Use `[applications_to_sync]` to sync only the listed applications:

```ini
[applications_to_sync]
ssh
adium
```

Use `[applications_to_ignore]` to skip applications:

```ini
[applications_to_ignore]
ssh
adium
```

Names come from `mackup list` and must not contain spaces. If `[applications_to_sync]` is empty, Mackup syncs every supported application. Ignored applications are excluded even if they are also listed in `[applications_to_sync]`.

Mackup stops with an error if the file contains the obsolete `[Allowed Applications]` or `[Ignored Applications]` sections. Migrate them to the sections above.

### Custom application configurations

To sync files that are not in the built-in list, create `~/.mackup/` and add `.cfg` files there. Each file needs an `[application]` section with a `name` and a `[configuration_files]` section listing paths relative to `$HOME`:

```ini
[application]
name = Nethack

[configuration_files]
.nethackrc
```

A custom file named after an existing application replaces the built-in configuration for that application. Custom applications appear in `mackup list`.

### XDG configuration directories

Applications that store settings under `~/.config` should use the `[xdg_configuration_files]` section. Paths in this section are relative to `$XDG_CONFIG_HOME`, so omit the `.config` prefix:

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

If `XDG_CONFIG_HOME` is set, it must be inside your home directory.

## Development

The project is a Python package with its source in `mackup/`. The entry point is `mackup.main:main`.

Set up a development environment with uv, as the CI and Makefile do:

```bash
uv sync --all-extras --dev
uv run mackup --version
```

`doc/develop.md` describes a Poetry-based setup (`poetry install --with dev`). The repository contains both `poetry.lock` and `uv.lock`.

To add or test an application configuration:

1. Fork the repository and create a branch.
2. Add the configuration file to `mackup/applications/`.
3. Run `mackup backup` from a checkout to test it.

The guide in `doc/README.md` also mentions `make develop` and `make undevelop`, but the Makefile does not define these targets.

Other project files:

- `mackup/main.py`: command-line interface and command dispatch.
- `mackup/mackup.py`: runtime state, storage checks, and application selection.
- `mackup/application.py`: backup, restore, and uninstall logic for each application.
- `mackup/appsdb.py`: loads application configurations.
- `mackup/config.py`: parses `.mackup.cfg`.
- `mackup/utils.py`: file operations, storage discovery, and confirmation prompts.

### Makefile targets

| Target | Command |
| --- | --- |
| `make test` | `uv run pytest` |
| `make lint` | `markdownlint -c .markdownlint.yaml '**/*.md'` |
| `make ruff` | `ruff check .` |
| `make clean` | Removes `__pycache__` directories and `dist/`. |
| `make release` | Cleans, runs `uv build`, then `uv publish`. |

## Testing

Tests are in `tests/` and use `unittest`-style classes run by pytest:

- `tests/test_config.py` checks configuration parsing for each storage engine, application selection, and error cases.
- `tests/test_main.py` checks the color helper functions.
- `tests/test_utils.py` checks confirmation prompts, deletion, copying, linking, permissions, error handling, and platform checks.

Fixtures in `tests/fixtures/` include sample `.mackup.cfg` files and simulated storage folders. Run the suite with:

```bash
make test
```

Some tests modify `HOME` to point at the fixtures directory, and the storage path tests expect fixture-specific values.

## Continuous integration

GitHub Actions workflows in `.github/workflows/` run on pushes to `master` and on pull requests:

- **Run tests** (`test.yaml`): pytest on Ubuntu with Python 3.9 through 3.13.
- **Test installs** (`install.yaml`): `pip install .` and `mackup --help` on Ubuntu 22.04 and 24.04 in Python containers, and on macOS 13, 14, and 15.
- **Lint Python** (`ruff.yaml`): ruff.
- **Lint Markdown** (`markdown.yaml`): markdownlint using `.markdownlint.yaml`, ignoring `tests/`.
- **linelint** (`linelint.yaml`): checks that text files end with a newline.

## Contributing

See `.github/CONTRIBUTING.md` and `.github/PULL_REQUEST_TEMPLATE.md`. The main guidelines are:

- Keep one application per pull request.
- Add the application to the supported list in this README.
- Sync only the minimal set of data.
- Do not sync state files, caches, workstation-specific files, or sensitive information such as passwords or private keys.
- Test changes and lint them locally.

Issues are tracked on GitHub at https://github.com/lra/mackup/issues.

For the merge workflow across machines, see `doc/configuration_merge_guide.md`.

## Releasing

From `doc/release.md`:

1. Increment `version` in `pyproject.toml`.
2. Commit with the message `Mackup X.Y.Z`.
3. Tag the commit with `<version>`.
4. Run `git push` and `git push --tags`.
5. Run `make release`.

## License

Mackup is free software licensed under the GNU General Public License, version 3 or (at your option) any later version (GPL-3.0-or-later). The full text is in `LICENSE`. The license states that the program comes with no warranty.

## Author and contact

Mackup was written by Laurent Raufaste. The package metadata gives the contact address `analogue@glop.org`. The copyright notice refers to <http://glop.org/>. The repository does not include a postal address.

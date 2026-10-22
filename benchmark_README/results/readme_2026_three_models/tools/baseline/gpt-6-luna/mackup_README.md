# Mackup

Mackup keeps application settings and dotfiles in a shared storage directory and links them back into their expected locations in your home directory. Back up configurations on one computer, then restore them on another. The project supports macOS and Linux and includes application profiles for a broad range of command-line tools, editors, and desktop applications.

Mackup uses a storage directory such as Dropbox, Google Drive, iCloud Drive, or a directory you choose. During backup, it copies configured files into that directory and replaces the originals with symbolic links to the stored copies. Restoring creates links from the stored files on the current computer.

> **Take care when syncing existing settings.** Restoring can replace files already in your home directory after confirmation. If you need to combine settings from multiple computers, merge the files yourself before backing them up. See [`doc/configuration_merge_guide.md`](doc/configuration_merge_guide.md).

## Install

Mackup requires Python 3.8 or later. The package depends on `docopt-ng`.

### Install with pip

```bash
pip install mackup
mackup --help
```

To upgrade:

```bash
pip install --upgrade mackup
```

To uninstall the package:

```bash
pip uninstall mackup
```

### Install with Homebrew

The installation guide also documents Homebrew for macOS:

```bash
brew install mackup
mackup --help
```

To upgrade, run `brew update` and `brew upgrade`. To uninstall, run `brew uninstall mackup`. The guide includes additional instructions for installing the Homebrew master-branch build.

For more installation detail, see [`INSTALL.md`](INSTALL.md).

## Usage

The command-line interface provides these main commands:

```text
mackup list
mackup backup
mackup restore
mackup show <application>
mackup uninstall
```

- **`mackup list`** displays the supported application names. Use these names in configuration sections; they are identifiers such as `ssh`, not display names such as “SSH.”
- **`mackup backup`** stores the selected configuration files in your configured storage and links them from their original locations. Use this on the computer whose settings you want to share first.
- **`mackup restore`** links stored configuration files into their expected locations. Use it on another computer that can access the same storage.
- **`mackup show <application>`** displays an application’s display name and the paths Mackup manages for it.
- **`mackup uninstall`** copies managed files back to their original locations and removes the links. It asks for confirmation before proceeding.

Useful options can be added to commands:

```bash
mackup --dry-run --verbose backup
mackup --dry-run restore
mackup --force backup
```

`--dry-run` shows the steps without executing them. `--verbose` prints additional details, including paths. `--force` answers confirmation prompts “Yes”; use it only when you are confident about the changes. Running as root is blocked by default. `--root` explicitly allows it, but the program warns that doing so can be dangerous. Use `mackup --help` for the complete command synopsis and `mackup --version` to print the installed version.

## Configuration

Mackup reads `~/.mackup.cfg`. If you do not create this file, the default storage engine is Dropbox, and Mackup uses a directory named `Mackup` inside the detected storage location.

### Choose a storage location

Set the engine in a `[storage]` section:

```ini
[storage]
engine = dropbox
```

The supported engines are `dropbox`, `google_drive`, `icloud`, and `file_system`. Mackup attempts to detect the folder for Dropbox, Google Drive, and iCloud Drive. If you choose `file_system`, provide a path relative to your home directory or an absolute path:

```ini
[storage]
engine = file_system
path = dotfiles
directory = backup
```

This example stores Mackup’s files in `~/dotfiles/backup`. The `directory` setting changes the final directory name; the default is `Mackup`. Paths may contain spaces and do not need quotes or escaping.

### Select applications

By default, Mackup selects all supported applications. To sync only selected applications, list their identifiers under `[applications_to_sync]`:

```ini
[applications_to_sync]
ssh
git
```

To exclude applications, list them under `[applications_to_ignore]`:

```ini
[applications_to_ignore]
adium
```

Ignored applications are excluded even if they are also listed for syncing. The application identifiers are filenames in `mackup/applications` without the `.cfg` extension. Run `mackup list` to see the identifiers available in your installed version.

### Add a custom application or paths

You can define profiles locally in `~/.mackup/`. Each `.cfg` file has an `[application]` section with a display name and a `[configuration_files]` section containing paths rooted at your home directory:

```ini
[application]
name = My files

[configuration_files]
bin
.hidden
```

For configuration under the XDG configuration directory, use `[xdg_configuration_files]` and list paths relative to that directory:

```ini
[application]
name = Example app

[xdg_configuration_files]
example/config
```

Mackup uses `XDG_CONFIG_HOME` when set, and requires it to be inside your home directory. A custom profile with the same filename as a built-in profile takes precedence over the built-in one. The `doc/` directory contains sample profiles and a sample `.mackup.cfg`; the full configuration guide is [`doc/README.md`](doc/README.md).

## Development

Clone the repository and install its development dependencies with [uv](https://docs.astral.sh/uv/):

```bash
uv sync --all-extras --dev
```

The project metadata declares Python 3.8 or later as its minimum. The CI test workflow runs the test suite with Python 3.9 through 3.13; the install workflow also checks installation on macOS and Linux.

To run Mackup from the local environment:

```bash
uv run mackup --version
```

Application profiles are stored in `mackup/applications/`. When adding or updating support, keep each pull request focused on one application. Profiles should sync only the configuration needed, avoid workstation-specific state and sensitive information, and be tested to ensure they do not disrupt the application or its own sync features. See [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) for contribution guidance.

## Testing and linting

Run the test suite with:

```bash
make test
```

This invokes `uv run pytest`. You can also run it directly:

```bash
uv run pytest
```

Python linting uses Ruff:

```bash
make ruff
```

Markdown linting is available through:

```bash
make lint
```

The repository’s CI workflows run tests, Ruff, Markdown linting, and checks for trailing newlines on pushes and pull requests. Tests and fixtures are in `tests/`.

## License

Mackup is licensed under the **GNU General Public License, version 3 or (at your option) any later version (GPL-3.0-or-later)**. See [`LICENSE`](LICENSE) for the full license text.

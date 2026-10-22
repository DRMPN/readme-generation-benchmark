# Mackup

Mackup keeps your application settings and dotfiles in sync across computers.
It backs up the configuration files of supported applications to a folder in a
cloud storage service (or any folder you choose), replaces the originals with
links to the backup, and can restore those settings on a new machine with one
command.

Mackup is licensed under the GPL-3.0-or-later. It supports macOS and Linux.

## How it works

- `mackup backup` moves each configuration file from your home folder into the
  Mackup storage folder and creates a symbolic link at the original location.
- `mackup restore` creates those links on another machine, pointing at the
  files already in the storage folder.
- `mackup uninstall` replaces each link with a real copy of the file and undoes
  Mackup's changes to your home folder.

If a file already exists at the destination, Mackup asks before replacing it
unless you pass `--force`.

## Requirements

- Python 3.8 or newer (`requires-python` in `pyproject.toml`). The test workflow
  runs on Python 3.9 through 3.13.
- A storage location: Dropbox, Google Drive, iCloud Drive, or any local folder
  you choose with the `file_system` engine.
- Mackup depends on `docopt-ng`.

## Installation

### With pip

```bash
pip install mackup
mackup --help
```

### With Homebrew (macOS)

```bash
brew install mackup
mackup --help
```

See [INSTALL.md](INSTALL.md) for upgrade and uninstall instructions, and for
installing from the Homebrew `HEAD` version.

## Quick start

1. On your first computer, back up the settings of the applications you want
   to sync:

   ```bash
   mackup backup
   ```

2. On each other computer, restore them:

   ```bash
   mackup restore
   ```

Run `mackup --dry-run --verbose backup` first to see what Mackup would do
without changing any files.

## Commands

```text
mackup list
mackup [options] backup
mackup [options] restore
mackup show <application>
mackup [options] uninstall
mackup (-h | --help)
mackup --version
```

| Command | Description |
| --- | --- |
| `list` | List the supported applications. |
| `backup` | Copy configuration files to the storage folder and link them back. Use this the first time you run Mackup on a computer. |
| `restore` | Link the configuration files in the storage folder into your home folder. Use this on any other computer. |
| `show <application>` | Show the display name and configuration files Mackup manages for one application. |
| `uninstall` | Replace every managed link with a real copy of the file, returning your home folder to its pre-Mackup state. Asks for confirmation unless `--force` or `--dry-run` is used. |

`restore` restores the Mackup configuration first, so that any custom settings
are applied before the other applications are restored.

### Options

| Option | Description |
| --- | --- |
| `-h`, `--help` | Show help. |
| `-f`, `--force` | Answer "Yes" to every confirmation prompt. |
| `-r`, `--root` | Allow Mackup to run as the superuser. Without this option, Mackup refuses to run as root. |
| `-n`, `--dry-run` | Show the steps without executing them. |
| `-v`, `--verbose` | Show additional details. |
| `--version` | Show the version. |

## Configuration

Mackup reads its configuration from `~/.mackup.cfg`. Every setting is optional.
A complete sample is in [doc/.mackup.cfg](doc/.mackup.cfg).

### Storage

Set the storage engine in the `[storage]` section. If no engine is set, Mackup
uses `dropbox`.

| Engine | Setting | Where files are stored |
| --- | --- | --- |
| `dropbox` | `engine = dropbox` (default) | The Dropbox folder, found from `~/.dropbox/host.db`. |
| `google_drive` | `engine = google_drive` | The Google Drive sync folder, found from Google Drive's local `sync_config.db`. |
| `icloud` | `engine = icloud` | `~/Library/Mobile Documents/com~apple~CloudDocs/` |
| `file_system` | `engine = file_system` and `path = ...` | The folder given in `path`. An absolute path starts at `/`; a relative path is relative to your home folder. `path` is required for this engine. |

Example for a custom folder:

```ini
[storage]
engine = file_system
path = dotfiles
```

Spaces in paths do not need escaping or quotes.

Files are placed in a subdirectory named `Mackup` by default. Change it with
`directory`:

```ini
[storage]
engine = file_system
path = dotfiles
directory = backup
```

This stores files in `~/dotfiles/backup`. `directory` may be a nested path, such
as `.config/mackup`, but it cannot be `.mackup`.

#### Switching storage

To change storage after Mackup is set up:

1. Run `mackup uninstall` on every computer.
2. Copy your Mackup files to the new storage location.
3. Update `[storage]` in `~/.mackup.cfg`.
4. Run `mackup backup` on your main computer and `mackup restore` on the others.

### Choosing applications

By default, Mackup manages every supported application. Narrow or change the
list with two optional sections, one application name per line. Run
`mackup list` to see valid names.

Sync only the applications you list:

```ini
[applications_to_sync]
ssh
adium
```

Never sync the applications you list:

```ini
[applications_to_ignore]
ssh
adium
```

If an application appears in both sections, it is ignored.

The `[Allowed Applications]` and `[Ignored Applications]` sections from old
versions of Mackup are no longer supported. Mackup stops with an error if it
finds them.

### Custom applications and files

To add support for an application that Mackup does not include, or to sync
your own files, create a `.cfg` file in `~/.mackup/`. Paths are relative to
your home folder.

```bash
mkdir ~/.mackup
```

`~/.mackup/nethack.cfg`:

```ini
[application]
name = Nethack

[configuration_files]
.nethackrc
```

`~/.mackup/my-files.cfg`:

```ini
[application]
name = My personal synced files and dirs

[configuration_files]
bin
.hidden
```

Then run `mackup list` to confirm the new names (`nethack`, `my-files`) appear.

A custom file named the same as a built-in one (for example
`~/.mackup/git.cfg`) replaces the built-in definition for that application.

Absolute paths are not allowed in `[configuration_files]`.

### XDG configuration directories

Applications that store settings in `~/.config` should use the
`[xdg_configuration_files]` section. Mackup then respects `XDG_CONFIG_HOME`,
which must be inside your home folder. Omit the `.config/` prefix:

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

## Supported applications

The repository includes 579 application definitions in
[mackup/applications](mackup/applications). Run `mackup list` to see the names
for your installed version, and `mackup show <application>` to see which files
an application includes.

On Linux, `mackup restore` skips files under `~/Library`.

## Development

Set up a development environment with Poetry, as described in
[doc/develop.md](doc/develop.md):

```bash
poetry install --with dev
poetry run mackup --version
```

Common tasks, from the [Makefile](Makefile):

| Command | Description |
| --- | --- |
| `make test` | Run the test suite with `uv run pytest`. |
| `make ruff` | Run `ruff check .`. |
| `make lint` | Run `markdownlint` on all Markdown files. |
| `make clean` | Remove build and cache output. |

The tests are in [tests](tests). Continuous integration runs the tests on
Python 3.9 through 3.13 and installs Mackup on Ubuntu and macOS. See
[.github/workflows](.github/workflows).

## Contributing

Contributions are welcome, including new or improved application definitions,
code changes, and issue triage. Please read
[.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) before opening a pull
request. Its main points:

- One application per pull request.
- Add the application to the list in this README.
- Sync only the files needed to restore the application's settings. Do not
  sync caches, session data, or files specific to one computer.
- Do not sync secrets such as passwords or private keys.

To test a new application definition locally, see
[Locally test an application](doc/README.md#locally-test-an-application-before-submitting-a-pull-request)
in the configuration guide.

For more detail, see:

- [doc/README.md](doc/README.md): full configuration guide.
- [INSTALL.md](INSTALL.md): installation, upgrade, and removal.
- [doc/configuration_merge_guide.md](doc/configuration_merge_guide.md): how to
  merge settings from several computers before syncing.
- [doc/release.md](doc/release.md): release steps.

## License

Mackup is free software, licensed under the GNU General Public License v3.0 or
later. See [LICENSE](LICENSE).

## Links

- Source: <https://github.com/lra/mackup>
- Issues: <https://github.com/lra/mackup/issues>
- Releases: <https://github.com/lra/mackup/releases>

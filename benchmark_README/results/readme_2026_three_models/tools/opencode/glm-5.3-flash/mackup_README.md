# Mackup

Keep your application settings in sync (macOS/Linux).

Mackup is a Python command-line tool that syncs your application configuration files across computers. It copies your configuration files to a synced storage folder and creates links in their original locations, allowing you to seamlessly restore them on another system.

## Features

- Synchronize application settings across multiple systems.
- Supports hundreds of popular applications out of the box.
- Multiple storage engine integrations: Dropbox, Google Drive, iCloud, and custom file system paths.
- Dry-run mode to preview actions without making changes.
- Easily extensible with custom application configuration files.

## Supported Applications

Mackup supports a large collection of applications out of the box, including Git, SSH, Vim, Neovim, iTerm2, Karabiner, Homebrew, VS Code, Sublime Text, tmux, Zsh, Fish, Bash, and many more.

To list all supported applications, run:

```bash
mackup list
```

To inspect the files tracked for a specific application, run:

```bash
mackup show <application>
```

## Installation

Mackup can be installed with Homebrew (macOS) or pip (macOS/Linux).

### Homebrew (macOS)

```bash
brew install mackup
```

### pip (macOS/Linux)

```bash
pip install mackup
```

Mackup requires Python 3.8 or newer.

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

### Modes of Action

1. **`backup`** — Sync your configuration files to your synced storage. Use this the first time you use Mackup.
2. **`restore`** — Link the configuration files already in your synced storage on your system. Use it on any new system you set up.
3. **`uninstall`** — Reset everything as it was before using Mackup. Every file managed by Mackup is unlinked and copied back to its original place in your home folder.
4. **`list`** — Display a list of all supported applications.
5. **`show`** — Display the configuration files tracked for a specific application.

## Configuration

All configuration is done in a file named `.mackup.cfg` stored at the root of your home folder. A sample configuration file is available in [doc/.mackup.cfg](doc/.mackup.cfg).

```bash
cp doc/.mackup.cfg ~/.mackup.cfg
```

### Storage Engines

Mackup stores your configuration files in one of four storage engines. If none is specified, it defaults to `dropbox`.

#### Dropbox (default)

```ini
[storage]
engine = dropbox
```

#### Google Drive

```ini
[storage]
engine = google_drive
```

#### iCloud

```ini
[storage]
engine = icloud
```

#### File System

Store files in a directory of your choosing. The `path` setting is mandatory and can be absolute (from the `/` of your drive) or relative to your home directory. Spaces in paths do not need escaping or quoting.

```ini
[storage]
engine = file_system
path = some/folder/in/your/home
# or path = /some/folder/in/your/root
```

#### Custom Directory Name

By default, Mackup creates a `Mackup` directory in the storage engine you chose (e.g., `~/Dropbox/Mackup`). You can customize this:

```ini
[storage]
engine = file_system
path = dotfiles
directory = backup
```

The above stores your files in `~/dotfiles/backup`.

### Selecting Applications

To only sync specific applications, add their names to the `[applications_to_sync]` section in `~/.mackup.cfg`, one per line:

```ini
[applications_to_sync]
ssh
adium
```

To ignore specific applications, use the `[applications_to_ignore]` section instead:

```ini
[applications_to_ignore]
ssh
adium
```

Use `mackup list` to get a list of valid application names.

### Adding Custom Applications

You can add support for applications or custom files and directories not yet supported by Mackup. Create a `.mackup` directory in your home and add a `.cfg` file for the application:

```bash
mkdir ~/.mackup
nano ~/.mackup/nethack.cfg
```

Example content:

```ini
[application]
name = Nethack

[configuration_files]
.nethackrc
```

Files and directories to be synced should be rooted at `$HOME`. If you override an application config that Mackup already supports, your custom config replaces the stock one.

### XDG Configuration Files

For applications storing their configuration under the `~/.config` folder, use the dedicated `xdg_configuration_files` section instead of hardcoding `.config`, since the location can be overridden by the `XDG_CONFIG_HOME` environment variable:

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

### Switching Storage

If you change your mind and switch storage solutions after Mackup is already set up (e.g., from `dropbox` to `icloud`), complete the following steps:

1. Run `mackup uninstall` on all computers.
2. Copy your Mackup files to the new storage location.
3. Change the storage provider details in your `.mackup.cfg` file.
4. Run `mackup backup` on the main computer and `mackup restore` on all others.

For more details on configuration, see the [configuration documentation](doc/README.md).

## Development

### Setting Up the Environment

Install a recent Python and the dependency management tooling, then install dependencies:

```bash
pipx install poetry
cd .../mackup
poetry install --with dev
```

You can now edit files and see the impact of your changes:

```bash
poetry run mackup --version
```

### Testing

To run the test suite:

```bash
make test
```

### Linting

```bash
make lint
make ruff
```

### Releasing

1. Increment the version in `pyproject.toml`.
2. `git commit` with the message `Mackup X.Y.Z`.
3. `git tag <version>`.
4. `git push`.
5. `git push --tags`.
6. `make release`.

## Contributing

Contributions are welcome! To add support for a new application:

1. Fork this project and create a branch.
2. Add the appropriate application config file in the `mackup/applications` folder.
3. Run `make develop` to replace the currently installed Mackup with your local modified version.
4. Run `mackup backup` to test that everything works as expected.
5. Run `make undevelop` to revert to the official version.
6. Commit, push, and open a pull request.

If you would like official support for an application, you can also open a [new issue](https://github.com/lra/mackup/issues) to request it.

## License

This project is licensed under the [GPL-3.0-or-later](LICENSE).

Copyright (C) 2013-2021 Laurent Raufaste.

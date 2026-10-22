# Mackup

Mackup keeps supported application settings in sync across macOS and Linux
machines by placing configuration files in a directory that is synchronized by
another service (for example, Dropbox), then linking those files back into your
home directory. The synchronization itself is performed by that storage
service; Mackup manages the files and links.

Mackup includes application profiles describing which files belong to each
supported application. Run `mackup list` to see the profiles available in your
installation. You can also define your own profiles.

## Install

Mackup requires Python 3.8 or newer. Install it from PyPI with:

```sh
python -m pip install mackup
```

The project also documents installation with Homebrew on macOS. See
[`INSTALL.md`](INSTALL.md) for installation, upgrade, and uninstall
instructions.

## Quick start

1. Make sure your chosen storage service is installed, configured, and
   synchronizing on the machine. By default Mackup uses Dropbox and attempts to
   locate its folder.
2. Optionally configure Mackup in `~/.mackup.cfg` (see
   [Configuration](#configuration)).
3. On the machine whose settings you want to share, run:

   ```sh
   mackup backup
   ```

   Mackup copies selected files into the Mackup directory in your storage and
   replaces their original home-directory paths with symbolic links to those
   stored files. It asks before replacing an existing backup.
4. On another machine, wait for the storage service to synchronize the Mackup
   directory, then run:

   ```sh
   mackup restore
   ```

   Mackup links the stored files into the home directory. If a destination
   already exists, Mackup asks whether to replace it.

Review the files to be managed before making changes, particularly when
combining configurations from multiple machines. Mackup does not merge
application settings; see the
[configuration merge guide](doc/configuration_merge_guide.md).

## Commands

```text
mackup list
mackup show <application>
mackup [options] backup
mackup [options] restore
mackup [options] uninstall
```

- `list` displays available application names. Use these names in configuration.
- `show <application>` displays an application's profile and the paths it
  manages.
- `backup` stores selected configuration files and links the home-directory
  paths to the stored copies.
- `restore` links stored copies into the home directory.
- `uninstall` copies managed files back into their original home-directory
  paths. It does not remove the Mackup directory from synchronized storage.

Options:

- `-n`, `--dry-run`: show planned steps without executing them.
- `-v`, `--verbose`: show additional details.
- `-f`, `--force`: answer yes to every confirmation prompt. Use with care;
  this can approve replacing existing files.
- `-r`, `--root`: allow running as superuser. Running as root can be dangerous;
  use this only when you understand the consequences.
- `-h`, `--help`: show command help.
- `--version`: show the installed version.

For example, preview a backup with more detail:

```sh
mackup --dry-run --verbose backup
```

## Configuration

Create `~/.mackup.cfg` to choose a storage engine or control which applications
are backed up. Without an application allow-list, Mackup selects all available
profiles and then excludes any listed under `applications_to_ignore`.

### Storage

The default storage engine is `dropbox`. Mackup also supports `google_drive`,
`icloud`, and `file_system`:

```ini
[storage]
engine = file_system
path = dotfiles
directory = Mackup
```

For `file_system`, `path` is required and may be absolute or relative to your
home directory. `directory` is optional; it names the folder Mackup uses within
the storage path and defaults to `Mackup`. The Dropbox, Google Drive, and iCloud
engines attempt to detect their respective storage locations.

### Selecting applications

To back up only a chosen set of applications, add their names under
`applications_to_sync`:

```ini
[applications_to_sync]
ssh
zsh
```

To exclude applications, use `applications_to_ignore`:

```ini
[applications_to_ignore]
ssh
```

If an application appears in both sections, the ignore list takes precedence.
Use `mackup list` for the valid names.

More configuration examples and storage details are in the
[configuration guide](doc/README.md).

## Custom application profiles

User profiles live in `~/.mackup/` and use the application name as the `.cfg`
filename. A user profile overrides the bundled profile with the same name. For
example, `~/.mackup/nethack.cfg` can contain:

```ini
[application]
name = Nethack

[configuration_files]
.nethackrc
```

Paths in `configuration_files` are relative to the home directory. For
configuration under the XDG config directory, use
`xdg_configuration_files`; these paths are resolved against
`$XDG_CONFIG_HOME` (or `~/.config` when it is unset). For example:

```ini
[application]
name = Example application

[xdg_configuration_files]
example/config
```

The full guide to storage settings, application selection, and profile files is
in [`doc/README.md`](doc/README.md).

## Development and tests

The repository uses `uv` for its test command. With development dependencies
available, run:

```sh
make test
```

This runs `uv run pytest`. The `make lint` target runs Markdown linting, and
`make ruff` runs Ruff.

## License

Mackup is distributed under the GNU General Public License, version 3 or later.
See [`LICENSE`](LICENSE).

## Links

- [Configuration guide](doc/README.md)
- [Installation instructions](INSTALL.md)
- [Configuration merge guide](doc/configuration_merge_guide.md)
- [Development notes](doc/develop.md)
- [Issue tracker](https://github.com/lra/mackup/issues)

# Mackup

Mackup keeps application settings in one place so you can back them up and use them on multiple computers. It stores supported configuration files in a sync folder—such as a folder managed by Dropbox, Google Drive, or iCloud—and links the original locations to those stored files.

Mackup supports macOS and Linux. Its repository includes configuration definitions for many applications, including Git, Bash, Zsh, Vim, Neovim, Visual Studio Code, and numerous others.

## How it works

For each supported application, Mackup knows which settings files or directories to manage. When you back up an application, Mackup places those settings in the configured storage location and links the application’s usual configuration location to the stored copy.

This lets the application continue using its settings normally while your sync service keeps the stored copy up to date. On another computer, restoring the settings connects that computer’s application configuration to the same stored files.

Mackup backs up settings; it does **not** install applications or sync application data that is not included in an application’s Mackup definition.

## Installation

Install Mackup with `pipx`:

```bash
pipx install mackup
```

Or install it with `pip`:

```bash
python -m pip install --user mackup
```

Make sure the directory containing user-installed Python commands is on your `PATH`. Your chosen storage provider may also require its desktop client to be installed and signed in.

## Quick start

1. Choose a storage location that is available on every computer where you want to use Mackup.
2. Configure Mackup to use that location.
3. Back up settings on your first computer.
4. Install Mackup and the relevant applications on another computer.
5. Restore the settings there.

For example, to use a folder managed by a sync service, create `~/.mackup.cfg`:

```ini
[storage]
engine = file_system
path = ~/Dropbox/Mackup
```

Replace the example path with the directory you want to use. The directory should be inside a location that your sync service actually synchronizes.

Then run:

```bash
mackup backup
```

On another computer, configure Mackup to use the same synchronized directory and run:

```bash
mackup restore
```

The first backup or restore can affect existing configuration files. Review Mackup’s prompts and make a separate backup of important files before proceeding.

## Commands

Run `mackup --help` for the commands and options available in your installed version.

Common commands include:

```bash
mackup backup    # Back up supported application settings
mackup restore   # Restore settings from the configured storage
mackup list      # List applications Mackup knows about
mackup uninstall # Undo Mackup's local links
```

`mackup uninstall` is for removing Mackup’s links from the local machine; it is not a substitute for managing or deleting your synchronized backup. Review the command’s prompts before confirming changes.

## Configuration

Mackup’s user configuration file is `~/.mackup.cfg`. It specifies the storage engine and, where applicable, the storage path. For example:

```ini
[storage]
engine = file_system
path = ~/Sync/Mackup
```

The repository includes definitions for several storage engines, including file-system storage, Dropbox, Google Drive, and iCloud. Availability and setup details can depend on your operating system and the sync client you use. Check `mackup --help` and the configuration examples in the repository for the options supported by your version.

You can also control which applications Mackup handles. For example, to limit syncing to selected applications:

```ini
[applications_to_sync]
git
vim
zsh
```

To omit applications:

```ini
[applications_to_ignore]
```

Application names must match Mackup’s definitions. Use `mackup list` to see the names recognized by your installation. If you use an application-specific selection, review it when you add new applications: newly supported apps may not be included automatically.

## Supported applications

Mackup’s application definitions describe the settings files and directories it can manage. The repository contains definitions for a large selection of applications and tools, including:

- Shells and terminal tools, such as Bash, Zsh, Fish, tmux, and Alacritty
- Editors and IDEs, such as Vim, Neovim, Emacs, Visual Studio Code, and IntelliJ IDEA
- Developer tools, such as Git, npm, Poetry, Docker, and Kubernetes tools
- Desktop and productivity applications, such as Alfred, Rectangle, and Obsidian

The available list changes over time and may vary by platform. Run:

```bash
mackup list
```

An application being listed does not guarantee that every version or every setting it uses is supported. Mackup manages only the files described in that application’s definition.

## Important considerations

- **Keep your storage private.** Application settings can contain credentials, tokens, server details, or other sensitive information. Mackup is not a secret-management tool; review what you sync and protect your storage appropriately.
- **Back up important files first.** Mackup may move or link files in an application’s configuration directory. Keep a separate backup before your first run.
- **Use one storage location consistently.** Computers restoring settings should point to the same synchronized Mackup directory.
- **Expect platform differences.** Some applications and settings are specific to macOS or Linux, and a setting that works on one system may not work on another.
- **Allow sync to finish.** Before restoring on another computer, make sure the storage provider has finished downloading the Mackup directory.

## Development

The repository contains the Mackup implementation, application definitions, and tests. To run the test suite from a development checkout:

```bash
python -m pytest
```

The project also includes packaging and lock files for its Python environment. See `pyproject.toml` and the project’s development documentation for additional setup details.

## License

See the [`LICENSE`](LICENSE) file for license terms.

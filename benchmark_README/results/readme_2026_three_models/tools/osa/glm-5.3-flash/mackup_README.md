# mackup-qg24al6x

---

[![PyPi](https://badge.fury.io/py/mackup.svg)](https://badge.fury.io/py/mackup)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Mackup is a Python command-line utility that keeps application settings in sync across machines by moving configuration files into a synced storage folder (Dropbox, Google Drive, iCloud, or a filesystem path) and symlinking them back into place. It is aimed at macOS and Linux users who want their dotfiles and application settings to follow them between systems, as well as developers contributing new application profiles. The tool offers a CLI with commands for listing supported applications, backing up, restoring, and uninstalling, with application support driven by data files. See Getting Started for runnable steps.

> **Naming note:** this repository (`mackup-qg24al6x`) is a local copy of the upstream Mackup project. The package published on PyPI is `mackup`, which is what `pip install mackup` installs.

---

## Core Features

- Keeps application settings in sync across machines by storing config files in a synced storage folder (Dropbox, Google Drive, iCloud, or the filesystem) and symlinking them back into place.
- Provides simple commands to back up settings on an existing machine and restore them on any new system, plus an uninstall command that safely reverts everything to its original state.
- Supports a large set of applications out of the box through a built-in, data-driven database of application profiles, which developers can extend with custom profiles.
- Lets users tailor behavior with a configuration file to choose the storage backend, a custom storage directory, and specific applications to sync or ignore.
- Includes a dry-run mode that shows the steps Mackup would take without executing anything, making it safe to preview changes.

---

## Installation

**Prerequisites:** Python is required; see `pyproject.toml` for the exact supported version range.

Install Mackup from PyPI:

```sh
pip install mackup
```

---

## Getting Started

**Prerequisites:**

- A macOS or Linux system with Python available.
- A synced storage folder supported by Mackup (Dropbox, Google Drive, iCloud, or any filesystem path).
- Mackup installed. See [INSTALL.md](./INSTALL.md) for installation instructions.

**Quickstart:**

1. Configure Mackup by creating a `.mackup.cfg` file in your home directory:

```bash
    vi ~/.mackup.cfg
```

    By default, Mackup uses Dropbox as its storage engine. To use a different engine, specify it in the config file, for example:

```ini
    [storage]
    engine = google_drive
```

    See the [documentation in `doc/`](./doc) for storage engine options (including `file_system`, which requires a `path` setting).

2. List the supported applications to see what Mackup can sync:

```bash
    mackup list
```

3. Inspect which configuration files a given application uses (optional):

```bash
    mackup show <application>
```

4. On your first machine, back up your configuration files to your synced storage:

```bash
    mackup backup
```

5. On any new machine (with the same storage synced), link your existing configuration files back into place:

```bash
    mackup restore
```

Useful options: `--dry-run` to show steps without executing, `--verbose` for details, and `--force` to answer "Yes" to every question.

To undo everything, run `mackup uninstall`, which copies the managed files back to their original place in your home folder.

---

## Testing

Contributors can verify changes against the test suite in the `tests/` directory, which includes unit tests for core functionality in modules such as `tests/test_config.py`, `tests/test_main.py`, and `tests/test_utils.py`. A canonical test command is not documented in this copy of the repository, so refer to the test modules and project configuration for how to run them.

---

## Documentation

A detailed Mackup description is available [here](./doc).

---

## Contributing

- **[Submit Pull Requests](./.github/CONTRIBUTING.md)**: To learn more about making a contribution to Mackup.

---

## License

This repository is a local copy of the Mackup project. Upstream Mackup is licensed under GPL-3.0; see the [LICENSE](./LICENSE) file for the exact terms that apply to this copy.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). mackup-qg24al6x repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{mackup-qg24al6x,

        author = {README Benchmark},

        title = {mackup-qg24al6x repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---

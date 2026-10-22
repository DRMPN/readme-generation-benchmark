# mackup-xoxqy093

---

[![PyPi](https://badge.fury.io/py/mackup.svg)](https://badge.fury.io/py/mackup)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Mackup keeps application settings and configuration files in sync across machines by storing them in a synced storage location and linking them back into place on other systems. It is a command-line tool written in Python, and it supports backing up, restoring, listing supported applications, showing the files managed for a given application, and reversing its changes. The primary audience is end users and developers who manage personal dotfiles and application settings, with contributor documentation available for open-source development. For runnable steps, see the Getting Started section.

---

## Core Features

- **Back up and restore application settings:** `mackup backup` copies supported applications' configuration files to synced storage, and `mackup restore` links those files on a new system, so settings stay consistent across machines.
- **Selective sync:** Choose which applications to include or exclude in the `.mackup.cfg` file, so only the apps you need are backed up or restored.
- **Multiple storage backends:** Select Dropbox, Google Drive, iCloud, or a local file system path through the storage engine setting, so you can use the storage service you already rely on.
- **Custom application definitions:** Add your own `.cfg` definitions in the custom apps directory in your home folder, so you can manage applications that are not bundled, and custom definitions take precedence over bundled ones.
- **Inspect and remove managed settings:** `mackup list` shows all supported applications, `mackup show <application>` displays an application's configuration files, and `mackup uninstall` asks for confirmation before processing managed files. Use `--dry-run` to preview steps without executing them.

---

## Installation

**Prerequisites:** requires Python >= 3.8

Install mackup-xoxqy093 using one of the following methods:

**Using PyPi:**

```sh
pip install mackup
```

---

## Getting Started

### Prerequisites

- Python with Mackup installed. See [INSTALL.md](../INSTALL.md) for installation steps.
- A supported storage location. The default engine is `dropbox`. Other options are `google_drive`, `icloud`, and `file_system`. See [doc/README.md](doc/README.md) for storage configuration.

### Steps

1. Install Mackup by following [INSTALL.md](INSTALL.md).

2. Optionally, create `~/.mackup.cfg` to choose a storage engine. If you skip this step, Mackup uses the default `dropbox` engine. A sample file is available at `doc/.mackup.cfg`.

3. List the supported applications:

```bash
   mackup list
```

4. Back up your configuration files to the storage location:

```bash
   mackup backup
```

   To preview the steps without making changes, add the dry-run flag:

```bash
   mackup --dry-run backup
```

5. On another machine, restore your configuration files from the storage location:

```bash
   mackup restore
```

For all commands and options, run `mackup --help`.

---

## Architecture

Mackup is a Python command-line tool. The architecture below covers three areas: the command entry point, storage engine selection, and the application registry.

- **Command entry point (`mackup/main.py`):** Uses docopt to parse the `list`, `backup`, `restore`, `show <application>`, and `uninstall` commands. Each command loads the application registry, runs environment checks, and then processes each selected application.
- **Storage engine selection (`mackup/config.py`):** The `engine` setting selects the storage backend: Dropbox, Google Drive, iCloud, or a local file system path. If no engine is set, Dropbox is used. An unknown engine value raises a configuration error.
- **Application registry (`mackup/appsdb.py`):** Loads application definitions from `.cfg` files in the bundled applications directory and in a custom applications directory under the home folder. When both locations define the same file name, the custom definition takes precedence over the stock one.
- **Control flow:** `main.py` builds the registry, selects the applications to process, and runs the requested operation for each one. Application files are backed up to, or restored from, the configured storage location.

The contents of `mackup/applications/` and the internals of `application.py` were not reviewed, so the set of supported applications and the per-application logic are not described here.

---

## Documentation

A detailed mackup-xoxqy093 description is available [here](./doc).

---

## Contributing

- **[Submit Pull Requests](./.github/CONTRIBUTING.md)**: To learn more about making a contribution to mackup-xoxqy093.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). mackup-xoxqy093 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{mackup-xoxqy093,

        author = {README Benchmark},

        title = {mackup-xoxqy093 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---
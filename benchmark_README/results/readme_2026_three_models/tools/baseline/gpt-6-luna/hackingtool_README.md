# HackingTool

HackingTool is a Python-based, interactive terminal menu for organizing and launching security, networking, forensics, and related utilities. It groups tools into collections and provides options such as install, run, and, for some entries, additional actions. Many entries wrap third-party projects; their installation commands and requirements vary, and some tools require manual setup or system packages.

The main program is `hackingtool.py`. Its menu includes collections for information gathering, wordlist generation, wireless testing, SQL injection, web and XSS testing, forensics, reverse engineering, payload creation, and other areas. The available entries are defined in the Python modules under `tools/`.

> **Use responsibly.** This project includes tools capable of intrusive actions, including scanning, credential attacks, phishing, and denial-of-service activity. Run tools only on systems and networks you own or have explicit permission to assess, and follow applicable laws and policies. The application itself warns against illegal use. Third-party tools may have separate terms and risks.

## Requirements

The project is designed primarily for Linux. The main program checks the operating system: on Linux it opens the interactive menu; on Windows it displays a Debian recommendation, and other systems receive a system-check message.

The setup scripts target Kali Linux/Parrot OS using `apt` or Arch Linux using `pacman`. The Docker image uses Kali Linux. The top-level Python dependencies in `requirements.txt` are:

- `boxes`
- `flask`
- `lolcat`
- `requests`

The menu and installer also call external programs such as Git, Python and pip, `figlet`, and system package managers. Individual tools may need many additional dependencies, including language runtimes, compilers, system libraries, or hardware such as a wireless adapter. Check an entry’s description and linked project before installing it.

## Installation

### Install using the provided script

`install.sh` requires root privileges and an internet connection. From a checkout of the repository, run:

```bash
sudo ./install.sh
```

The script prompts for a platform choice, or accepts the choice as an argument:

```bash
sudo ./install.sh 1   # Kali Linux / Parrot OS (apt)
sudo ./install.sh 2   # Arch Linux (pacman)
```

The installer installs system packages, clones the repository to `/usr/share/hackingtool`, creates a Python virtual environment there, installs `requirements.txt`, and creates a `hackingtool` launcher in `/usr/bin`. If the installation directory already exists, the script asks whether to replace it. Once installation completes, the script reports that the command `hackingtool` can be used to start the program.

The installer performs system package updates and requires network access to download the repository and dependencies. Review the script before running it, especially on a system where you do not want it to modify packages or files.

### Run from a checkout

To launch directly from a repository checkout:

```bash
python3 hackingtool.py
```

On Linux, the first launch checks for `~/hackingtoolpath.txt`. If it is absent, the program prompts you to enter a tool-installation directory manually or select the default `/home/hackingtool/`. It creates the selected directory and changes into it before showing the menu. The file stores this path for subsequent launches. The default path is distinct from the installer’s repository location, `/usr/share/hackingtool`.

### Docker

The `Dockerfile` builds on `kalilinux/kali-rolling:latest`, installs system utilities and Python dependencies, and starts `hackingtool.py` as the container entry point. Build and run it with an interactive terminal:

```bash
docker build -t hackingtool .
docker run --rm -it hackingtool
```

The image declares ports `1-65535` as exposed. The supplied `docker-compose.yml` instead uses the image `vgpastor/hackingtool`, mounts the current directory at `/root/hackingtool`, allocates a terminal, and maps host port 22 to container port 22. Start that configuration with:

```bash
docker compose up
```

The Compose service uses an image rather than a `build` directive, so it does not build the local Dockerfile by itself.

## Usage

Start the program with `hackingtool` after using the installer, or run `python3 hackingtool.py` from the project directory. Use the terminal prompts to select a collection, then a tool and one of its available actions. Tool entries may offer installation and running, while others provide only one of those actions or custom options. Some actions ask for values such as a hostname, URL, file path, or other input. Use `99` to go back or exit from a menu.

Tool installation and execution are delegated to shell commands in the individual tool definitions. They may invoke `sudo`, clone external repositories, install packages, or modify files. Read the commands and linked project information before choosing an action. The menu is a launcher and collection manager; it does not guarantee that every third-party tool is available, current, or compatible with your system.

The **Update or Uninstall | Hackingtool** collection provides actions to update the system, update HackingTool, or uninstall it. The repository also includes `update.sh`, which is intended for the `/usr/share/hackingtool` installation, requires root privileges and internet access, pulls repository changes, and reruns the installer.

## Configuration

The main configuration established at first launch is the tool installation directory, stored in `~/hackingtoolpath.txt`. Choose a directory where the account running HackingTool can create files; individual wrapped commands may still require elevated privileges.

There is no central configuration file for third-party tools in the supplied project files. Their options, dependencies, and any required API keys or manual configuration are specific to each tool. Consult the tool’s displayed information and its project URL before use.

## Development

The menu framework is in `core.py`. Tool and collection classes are defined in `tools/`, with `hackingtool.py` assembling the top-level collections. To add or change an entry, follow the existing `HackingTool` or `HackingToolsCollection` patterns and ensure it is included in the appropriate collection.

For a local development environment, install the listed Python dependencies and start the program from the checkout:

```bash
python3 -m pip install -r requirements.txt
python3 hackingtool.py
```

The GitHub issue templates provide forms for bug reports and feature requests. When reporting a problem, include reproduction steps, expected behavior, operating-system details, and relevant context. For a feature request, describe the problem, desired change, and alternatives considered.

## Testing and code checks

The GitHub Actions workflows run on pushes and pull requests targeting `master`. `lint_python.yml` runs Ruff checks, codespell, Black in check mode, mypy, pytest, doctest, and a dependency safety check. Several checks are explicitly allowed to continue on failure, including Black, mypy, pytest, and doctest; Ruff’s must-fix check, codespell, and `safety check` are not marked that way.

The repository includes no test files in the supplied file tree. To run the test commands used by CI locally, install the relevant development tools and run:

```bash
pytest .
pytest --doctest-modules .
```

The `test_install.yml` workflow exercises the installer and interactive menu on Ubuntu using scripted input. These checks do not establish that every external tool can be installed or run successfully on every supported system.

## License

This project is provided under the MIT License. Copyright © 2020 Mr.Z4nzu. The license permits use, modification, distribution, and sublicensing, subject to including the copyright and permission notice in copies or substantial portions. The software is provided “as is,” without warranty or liability; see [`LICENSE`](LICENSE) for the full terms.

# hackingtool

hackingtool is a menu-driven Python launcher that organizes a collection of security and penetration-testing tools into categories. From one interactive menu, you can install, run, open the project page for, or uninstall each tool. The project's banner identifies it as Version 1.1.0 and links to `https://github.com/Z4nzu/hackingtool`.

> **Disclaimer:** The program banner states "Please Don't Use For illegal Activity." Many of the listed tools are offensive security tools. Use them only on systems you own or have explicit permission to test.

## Overview

The application is built around a small object model in `core.py`:

- `HackingTool` represents a single tool. It defines a title, description, install and uninstall commands, run commands, and a project URL. Each tool shows a menu of options, which by default include **Install** and **Run**.
- `HackingToolsCollection` groups tools into a named category, such as "Wireless attack tools," and displays them as a submenu.

`hackingtool.py` builds the top-level `all_tools` list, which contains 18 categories:

- Anonymously Hiding Tools
- Information gathering tools
- Wordlist Generator
- Wireless attack tools
- SQL Injection Tools
- Phishing attack tools
- Web Attack tools
- Post exploitation tools
- Forensic tools
- Payload creation tools
- Exploit framework
- Reverse engineering tools
- DDOS Attack Tools
- Remote Administrator Tools (RAT)
- XSS Attack Tools
- Steganography tools
- Other tools
- Update or Uninstall | Hackingtool

Most tools are installed by cloning their upstream Git repositories or by running package-manager commands, then executed through shell commands. Some tools have custom prompts that collect input (for example, a target IP or URL) before running.

## Repository Layout

| Path | Purpose |
|---|---|
| `hackingtool.py` | Entry point; defines the tool catalog and the Linux startup logic |
| `core.py` | Base classes `HackingTool` and `HackingToolsCollection`, and menu handling |
| `tools/` | Category modules (for example, `tools/wireless_attack_tools.py`) |
| `tools/others/` | Sub-category modules used by `tools/other_tools.py` |
| `install.sh` | Root-only installer for Kali/Parrot (apt) and Arch Linux (pacman) |
| `update.sh` | Root-only updater that pulls the repository and re-runs `install.sh` |
| `Dockerfile` | Container image based on `kalilinux/kali-rolling` |
| `docker-compose.yml` | Compose service definition for the container |
| `generate_readme.py` | Builds this README's tool list from `all_tools` |
| `requirements.txt` | Python dependencies |
| `.github/` | Issue templates and GitHub Actions workflows |

## Requirements

**Python dependencies** (`requirements.txt`):

- `boxes`
- `flask`
- `lolcat`
- `requests`

**System packages.** `install.sh` installs these for the apt option:

- `git`, `python3-pip`, `figlet`, `boxes`, `php`, `curl`, `xdotool`, `wget`
- `python3-venv` (installed separately)

The Dockerfile installs `git`, `python3-pip`, `figlet`, `sudo`, `boxes`, `php`, `curl`, `xdotool`, and `wget`. The menu uses `figlet` and `boxes` for headers and `lolcat` for colored output.

**Platform:** The application's startup logic is written for Linux. On Windows, it prints a message recommending a Debian system and opens a web page. On other systems, it prints "Please Check Your System or Open New Issue."

## Installation

### Option 1: Installer script (Linux)

The installer must be run as root.

```bash
sudo ./install.sh
```

You can also pass the menu choice as an argument to skip the prompt:

```bash
sudo ./install.sh 1   # Kali Linux / Parrot OS (apt)
sudo ./install.sh 2   # Arch Linux (pacman)
```

The script:

1. Checks for an internet connection by contacting google.com or github.com.
2. Installs the required system packages for the selected platform.
3. Removes any existing `/usr/share/hackingtool` after confirmation.
4. Clones the repository into `/usr/share/hackingtool`.
5. Creates a virtual environment at `/usr/share/hackingtool/venv` and installs `requirements.txt`.
6. Creates a launcher script and moves it to `/usr/bin/hackingtool`.

After installation, start the tool by typing:

```bash
hackingtool
```

### Option 2: Docker

The Dockerfile builds an image from `kalilinux/kali-rolling`, copies the project into `/root/hackingtool`, and sets the entry point to run `hackingtool.py`:

```bash
docker build -t hackingtool .
```

`docker-compose.yml` defines a service named `hackingtool` that uses the image `vgpastor/hackingtool`, enables `stdin_open` and `tty`, mounts the current directory at `/root/hackingtool`, and maps host port 22 to container port 22.

## Usage

### Main menu

On startup, the tool clears the screen, displays the banner, and lists the categories with numbers starting at 0. Enter a category number to open it. Enter `99` to exit.

### Tool menus

Selecting a tool displays its description and project URL, followed by a menu like this:

- `[1] Install` (when the tool is installable)
- `[2] Run` (when the tool is runnable)
- Additional tool-specific options, such as `Stop` for AnonSurf or `Update` for BlackPhish
- `[98] Open project page` (when a project URL is defined)
- `[99] Back to ...`

Press Enter after an action to return to the menu. Options that have no defined commands for the selected action have no effect.

### Update and uninstall

The **Update or Uninstall | Hackingtool** category provides:

- **Update Tool or System:** Runs `sudo apt update && sudo apt full-upgrade -y` and installs several packages, including `tor`, `openssl`, `curl`, and `python3-pip`. The **Update Hackingtool** option removes the old copy under `/etc/hackingtool`, clones the repository again, and runs `install.sh`.
- **Uninstall HackingTool:** Removes `/usr/share/doc/hackingtool/` and `/etc/hackingtool/`, then exits.

To update from the command line, run:

```bash
sudo ./update.sh
```

`update.sh` changes to `/usr/share/hackingtool`, checks the internet connection, runs `git pull`, and then runs `sudo bash install.sh`.

## Configuration

### Tool install location (Linux)

On Linux, `hackingtool.py` reads `~/hackingtoolpath.txt` to find the directory where tools are installed. If the file does not exist, the program shows a prompt:

- **1 (Manual):** Enter a directory path. The path is saved to the file.
- **2 (Default):** Saves `/home/hackingtool/` and continues after a short pause.
- Any other choice prints "Try Again..!!" and exits.

The program then creates the directory if needed, changes into it, and opens the menu. The Dockerfile writes `/root/hackingtool/` to `/home/hackingtoolpath.txt` during the image build.

### Installer paths

`install.sh` uses these fixed paths:

- Install directory: `/usr/share/hackingtool`
- Launcher: `/usr/bin/hackingtool`
- Virtual environment: `/usr/share/hackingtool/venv`

### Docker configuration

- The compose file bind-mounts the current project directory into the container at `/root/hackingtool`.
- The Dockerfile sets `EXPOSE 1-65535` and the entry point `python3 /root/hackingtool/hackingtool.py`.

## Development

### Project structure

The project uses two base classes from `core.py`:

- `HackingTool` supports the attributes `TITLE`, `DESCRIPTION`, `INSTALL_COMMANDS`, `INSTALLATION_DIR`, `UNINSTALL_COMMANDS`, `RUN_COMMANDS`, `OPTIONS`, and `PROJECT_URL`. Override the hook methods `before_install`, `after_install`, `before_uninstall`, `after_uninstall`, `before_run`, and `after_run` as needed. Override `run` for custom interactive behavior.
- `HackingToolsCollection` requires a `TITLE` and a `TOOLS` list.

Constructor arguments control which default options appear. For example, `installable=False` removes **Install**, and `runnable=False` removes **Run**.

### Adding a tool

1. Create a subclass of `HackingTool` in the appropriate module under `tools/`.
2. Add the instance to that module's `HackingToolsCollection.TOOLS` list.
3. If you create a new category, import it in `hackingtool.py` and add it to `all_tools`.

### README generation

`generate_readme.py` imports `all_tools` from `hackingtool.py`, creates a table of contents and a tool list, and fills the placeholders `{{toc}}` and `{{tools}}` in a file named `README_template.md`. The script writes the result to `README.md`. The template file is not included in the supplied repository files.

### Code style

Development tooling in the repository includes:

- `ruff` (in the lint workflow)
- `black`
- `codespell`
- `mypy`
- `safety`

The lint workflow runs these tools on pushes and pull requests to `master`.

## Testing

No dedicated unit test files are present in the repository tree. The available automated checks are:

- **`lint_python.yml`** runs on pushes and pull requests to `master`. It runs ruff checks, `black --check`, `codespell`, `mypy`, `pytest`, `pytest --doctest-modules`, and `safety check`. Several steps use `|| true`, so they do not fail the workflow.
- **`test_install.yml`** runs on the same events on `ubuntu-latest`. It runs `sudo ./install.sh 1`, then pipes a sequence of menu inputs into `hackingtool`. The matrix includes sequences that install and run a tool, update the system or the tool, uninstall, and quit.

To run the install test sequence yourself, provide the menu inputs in order, separated by newlines.

## Contributing

The `.github/ISSUE_TEMPLATE/` directory contains templates for:

- **Bug reports:** describe the bug, steps to reproduce, expected behavior, and environment details (desktop and smartphone sections).
- **Feature requests:** describe the problem, the proposed solution, alternatives considered, and additional context.

## License

This project is licensed under the MIT License. The license text is in `LICENSE`, and the copyright line reads: "Copyright (c) 2020 Mr.Z4nzu."

# Hackingtool – All-In-One Hacking Toolkit

**Version 1.1.0** — [https://github.com/Z4nzu/hackingtool](https://github.com/Z4nzu/hackingtool)

> ⚠️ **Disclaimer:** Hackingtool is intended **for educational and authorized security testing purposes only**. Please do not use this tool for any illegal activity. The authors and contributors are not responsible for any misuse of this software.

Hackingtool is a menu-driven, all-in-one toolkit for Linux (best run on Kali Linux, Parrot OS, or Arch Linux) that wraps a large collection of well-known open-source security and penetration-testing tools behind a single, unified terminal interface. Instead of cloning, installing, and remembering the syntax of dozens of separate projects, you can browse them by category, install them with one keystroke, and launch them directly from the tool's text menus.

The framework is written in Python and requires no complex configuration: every tool is described declaratively (install commands, run commands, project URL) so the main menu can install, run, uninstall, and link to each tool's upstream project automatically.

## Features

- **Single unified menu** for a large set of security tools, organized into categories.
- **Automatic installation** of bundled tools via `git clone` / package-manager commands, tracked per tool.
- **Run, install, and uninstall** actions for each tool, plus links to each tool's project page (opened in your browser).
- **Tool manager** built into the app for updating the system/tool or uninstalling hackingtool entirely.
- **Cross-distribution installer** supporting apt-based distros (Kali/Parrot) and pacman-based distros (Arch Linux).
- **Docker support** via a `Dockerfile` and `docker-compose.yml`.
- **Pretty terminal output** using `figlet`, `boxes`, and `lolcat`.

## Requirements

- A **Linux** system (a Debian-based system such as Kali Linux or Parrot OS is recommended for best results; Arch Linux is supported by the installer). The program explicitly warns when run on Windows and suggests a Debian system instead.
- **Root privileges** — the installer and most bundled tools must run as root.
- Internet connectivity (checked by the install/update scripts).
- Python 3 and `pip3`.
- The following packages are installed by the installer: `git`, `python3-pip`, `figlet`, `boxes`, `php`, `curl`, `xdotool`, `wget` (and `python3-venv` for the virtual environment).
- Python dependencies listed in `requirements.txt`: `boxes`, `flask`, `lolcat`, `requests`.

## Installation

### Automated installation (Linux)

Run the installer as root and choose your package manager:

```bash
sudo bash install.sh 1   # Kali Linux / Parrot OS (apt)
sudo bash install.sh 2   # Arch Linux (pacman)
```

Or run it without arguments and pick the option interactively.

The installer will:

1. Check your internet connection.
2. Update packages and install required system dependencies.
3. Clone the repository to `/usr/share/hackingtool` (asking to replace an existing installation if present).
4. Create a Python virtual environment at `/usr/share/hackingtool/venv`.
5. Install the Python requirements into the virtual environment.
6. Create a launcher script at `/usr/bin/hackingtool` so you can start the tool from anywhere.

After installation, simply type:

```bash
hackingtool
```

### Docker installation

A `Dockerfile` is provided based on `kalilinux/kali-rolling:latest`. It installs the system dependencies and Python requirements, copies the project into `/root/hackingtool`, and sets `hackingtool.py` as the entrypoint:

```bash
docker build -t hackingtool .
docker run -it hackingtool
```

Alternatively, use the provided `docker-compose.yml`, which mounts the repository into the container at `/root/hackingtool` and keeps an interactive TTY session:

```bash
docker-compose up
```

The compose file also publishes port `22` and exposes the full port range (the container is based on Kali Linux, and many bundled tools require network access).

## Usage

When you start `hackingtool` for the first time on Linux, you are asked where all your tools should be installed:

- **Option 1 (Manual):** enter a custom path (including the directory name).
- **Option 2 (Default):** use `/home/hackingtool/`.

Your choice is stored in `~/hackingtoolpath.txt` and re-used on subsequent launches. The directory is created if it does not exist, and the program changes into it before launching the main menu.

The main menu lists all tool categories. Select a category by number, then select a tool inside it. Each tool offers options such as **Install**, **Run**, and additional tool-specific actions (for example, *Update*/*Troubleshoot* for TheFatRat, *Stop* for Anonsurf, or GUI/CLI modes for Bulk extractor). Use option `98` on a tool to open its upstream project page in your browser, and `99` to go back (or exit from the main menu). Some tools prompt for input (targets, URLs, wordlists, ports, etc.) before running.

### Available tool categories

The main menu (`All tools`) includes the following collections:

- **Anonymously Hiding Tools** — Anonymously Surf (kali-anonsurf), Multitor.
- **Information Gathering** — nmap, Dracnmap, Port Scanning, Host to IP, Xerosploit, RED HAWK, ReconSpider, IsItDown, Infoga (email OSINT), ReconDog, Striker, SecretFinder, Shodan (Shodanfy.py), rang3r, Breacher.
- **Wordlist Generator** — Cupp, WordlistCreator, Goblin WordGenerator, SMWYG (password list search over 1.4 billion leaked credentials).
- **Wireless Attack Tools** — WiFi-Pumpkin, pixiewps, BluePot (Bluetooth honeypot), Fluxion, Wifiphisher, Wifite, EvilTwin, Fastssh, Howmanypeoplearearound.
- **SQL Injection Tools** — Sqlmap, NoSQLMap, Damn Small SQLi Scanner, Explo, Blisqy, Leviathan, SQLScan.
- **Phishing Attack Tools** — Autophisher RK, Pyphisher, AdvPhishing, Setoolkit, SocialFish, HiddenEye, Evilginx2, I-See_You, SayCheese, QR Code Jacking, BlackEye, ShellPhish, Thanos, QRLJacking, BlackPhish, MaskPhish, dnstwist.
- **Web Attack Tools** — Web2Attack, Skipfish, SubDomain Finder (Sublist3r), CheckURL, Blazy, Sub-Domain TakeOver, Dirb.
- **Post Exploitation Tools** — Vegile (Ghost In The Shell), Chrome Keylogger (HeraKeylogger).
- **Forensic Tools** — Autopsy, Wireshark, Bulk extractor, Guymager, Toolsley.
- **Payload Creation Tools** — TheFatRat, Brutal, Stitch, MSFvenom Payload Creator, Venom, Spycam, Mob-Droid, Enigma.
- **Exploit Frameworks** — RouterSploit, WebSploit, Commix, Web2Attack.
- **Reverse Engineering Tools** — Androguard, Apk2Gold, Jadx.
- **DDoS Attack Tools** — SlowLoris, aSYNcrone, UFONet, GoldenEye, SaphyraDDoS.
- **Remote Administrator Tools (RAT)** — Stitch, Pyshell.
- **XSS Attack Tools** — DalFox, XSS Payload Generator, extended-xss-search, XSS-Freak, XSpear, XSSCon, XanXSS, XSStrike, RVuln.
- **Steganography Tools** — SteganoHide, StegnoCracker, StegoCracker, Whitespace (snow10).
- **Other Tools** — sub-collections for SocialMedia Bruteforce (Instagram/Facebook/Gmail all-in-one, Application Checker), Android Hacking (Keydroid, MySMS, Lockphish, DroidCam, EvilApp), HatCloud, IDN Homograph Attack (EvilURL), Email Verify (KnockMail), Hash Cracking (Hash Buster), WiFi Deauthenticate (WifiJammer-NG, KawaiiDeauther), SocialMedia Finder (social_mapper, finduser, Sherlock, SocialScan), Payload Injector (Debinject, Pixload), Web Crawling (GoSpider), and Mix Tools (Tilix terminal multiplexer, Crivo).
- **Update or Uninstall** — update the system or hackingtool itself, or uninstall hackingtool.

> Note: DDoS tooling is included explicitly **for security testing purposes only**. Several bundled tools (e.g., WiFi monitoring, social-media brute forcing) may be illegal to use against networks or accounts you do not own — check your local laws.

## Configuration

- **Install path:** stored in `~/hackingtoolpath.txt` (set on first run). Bundled tools are cloned and installed inside this directory. The Docker image writes `/root/hackingtool/` to `/home/hackingtoolpath.txt`.
- **Application install location:** the installer places the app in `/usr/share/hackingtool` and a launcher in `/usr/bin/hackingtool`.
- **Docker:** edit `docker-compose.yml` to change the mounted volume, container name, or published ports.

## Updating and Uninstalling

- From the shell: run `sudo bash update.sh` as root. It verifies internet connectivity, marks the install directory as a git safe-directory, pulls the latest repository changes, and re-runs `install.sh`.
- From within the app: choose **Update or Uninstall | Hackingtool**, then either *Update System* (apt update/full-upgrade plus tor, openssl, curl, python3-pip) or *Update Hackingtool* (re-clones the repository and re-runs the installer).
- To uninstall, choose **Uninstall HackingTool** in the same menu; it removes the hackingtool directories from `/etc` and `/usr/share/doc` and exits.

## Development

The project is built around two small framework classes in `core.py`:

- **`HackingTool`** — a single tool. You declare its `TITLE`, `DESCRIPTION`, `INSTALL_COMMANDS`, `UNINSTALL_COMMANDS`, `RUN_COMMANDS`, `PROJECT_URL`, and extra `OPTIONS` (tuples of an option name and a callable). The base class handles rendering the info box, prompting for menu selections, and executing install/run/uninstall command sequences via the shell. Lifecycle hooks (`before_install`, `after_install`, `before_run`, `after_run`, `before_uninstall`, etc.) allow customization.
- **`HackingToolsCollection`** — a category that groups multiple `HackingTool` (or nested collection) instances under one menu, rendered with `figlet`.

To add a new tool, create a class inheriting from `HackingTool` with the appropriate commands, add it to the relevant collection's `TOOLS` list (creating a new `HackingToolsCollection` if needed), and register the collection in `all_tools` in `hackingtool.py`.

`generate_readme.py` regenerates this README from `README_template.md` by walking `all_tools` and substituting a table of contents (`{{toc}}`) and tool listings (`{{tools}}`).

## Testing and CI

Two GitHub Actions workflows run on pushes and pull requests to `master`:

- **`lint_python`** — installs `ruff`, `black`, `codespell`, `mypy`, `pytest`, and `safety`; runs ruff checks (with a "must-fix" pass on stopper-level issues), black format check, codespell, mypy type checking, pytest (including doctests), and a `safety` dependency check.
- **`test_install`** — runs `install.sh` on an Ubuntu runner and drives the interactive `hackingtool` menu through scripted key sequences (install/run/update/uninstall paths) to verify the installation works end-to-end.

## License

This project is licensed under the **MIT License** — Copyright (c) 2020 Mr.Z4nzu. See the `LICENSE` file for the full text.

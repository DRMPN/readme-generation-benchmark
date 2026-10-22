# HackingTool

HackingTool is a Python 3 terminal menu that collects, installs, and launches a large set of open-source security and penetration-testing tools from one interface. It is version 1.1.0 (from the header of `hackingtool.py`) and is released under the MIT License.

> **Use responsibly.** The tool's own startup banner reads "Please Don't Use For illegal Activity." Many of the tools it manages (phishing kits, DDoS utilities, credential brute-forcers, RATs, and Wi-Fi deauthentication tools) can cause real harm when pointed at systems you do not own or have no written permission to test. You are responsible for how you use them and for complying with applicable laws.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running with Docker](#running-with-docker)
- [Updating and Uninstalling](#updating-and-uninstalling)
- [Tool Categories](#tool-categories)
- [Repository Layout](#repository-layout)
- [Known Limitations](#known-limitations)
- [Contributing](#contributing)
- [License](#license)

## Features

- A numbered, interactive menu organized into 17 tool categories plus an update/uninstall section.
- Per-tool options that typically include **Install**, **Run**, and any tool-specific actions defined in the code.
- Install commands for each tool that are executed from the menu (most are `git clone` commands or package-manager calls).
- Shortcut `98` opens a tool's project page in your web browser, when the tool defines one.
- Navigation: `99` goes back to the parent menu, or exits from the top-level menu.
- Built-in self-update and uninstall actions (see [Updating and Uninstalling](#updating-and-uninstalling)).

## Requirements

**Operating system:** The code is designed for Linux. The installer script targets Debian-based systems (Kali Linux, Parrot OS) using `apt`, and Arch Linux using `pacman`. On Windows, `hackingtool.py` does not run the menu; it prints a recommendation to use a Debian system and opens a web page. Other systems print a message asking the user to open an issue.

**Privileges:** `install.sh` and `update.sh` must be run as root. Some individual tools call `sudo` internally.

**Runtime dependencies** (from `requirements.txt`, installed with pip):

- `boxes`
- `flask`
- `lolcat`
- `requests`

**System packages** installed by `install.sh` for the apt path: `git`, `python3-pip`, `figlet`, `boxes`, `php`, `curl`, `xdotool`, `wget`, and `python3-venv`. The Arch path installs `python-pip` and `figlet`, and builds `boxes` from the AUR.

**Network:** An internet connection is required for installation, which checks connectivity to google.com and github.com.

## Installation

Installation is done with `install.sh`, which must run as root. It downloads the repository to `/usr/share/hackingtool`, creates a Python virtual environment at `/usr/share/hackingtool/venv`, installs the requirements, and creates a launcher at `/usr/bin/hackingtool`.

```bash
git clone https://github.com/Z4nzu/hackingtool.git
cd hackingtool
sudo bash install.sh
```

When the script starts, it asks you to choose your distribution:

- `1` – Kali Linux / Parrot OS (apt)
- `2` – Arch Linux (pacman)
- `0` – Exit

You can also pass the choice as an argument (`1` or `2`) to skip the prompt.

If `/usr/share/hackingtool` already exists, the script asks whether to replace it. Answering anything other than `y` or `Y` stops the installation.

After a successful install, start the tool with:

```bash
hackingtool
```

### First run: setting the tools directory

On Linux, the first time `hackingtool` runs it asks where tools should be installed and saves the answer to `~/hackingtoolpath.txt`:

- `1` – Manual: enter a directory path.
- `2` – Default: uses `/home/hackingtool/`.

The program creates that directory if needed, changes into it, and then shows the menu. Tools that clone repositories will place them there.

## Usage

Run the menu:

```bash
hackingtool
```

The top-level menu lists every category. Enter a number to open a category, then a number to open a tool. Each tool screen shows its options numbered from `1`:

| Input | Action |
|-------|--------|
| A number from the list | Run that option (e.g., `Install`, `Run`, or a tool-specific action) |
| `98` | Open the tool's project page in a web browser (only shown if the tool has a project URL) |
| `99` | Go back to the previous menu, or exit at the top level |

After an action finishes, the menu waits for you to press Enter before redrawing.

You can also run the Python entry point directly from the repository directory:

```bash
python3 hackingtool.py
```

Tools are typically installed into the tools directory you chose on first run, and each tool's **Run** option executes its own commands. Individual tools have their own dependencies, prerequisites, and usage requirements that are not covered here; consult each tool's project page (opened with `98`) for details.

## Running with Docker

The repository includes a `Dockerfile` and a `docker-compose.yml`.

**`Dockerfile`** builds on `kalilinux/kali-rolling:latest`, installs the system packages and Python requirements, copies the repository to `/root/hackingtool`, writes `/root/hackingtool/` to `/home/hackingtoolpath.txt`, and runs `hackingtool.py` as the entrypoint. The menu reads `~/hackingtoolpath.txt`, which for root is `/root/hackingtoolpath.txt`, so the first-run path prompt may still appear inside the container.

```bash
docker build -t hackingtool .
docker run -it hackingtool
```

**`docker-compose.yml`** runs the image `vgpastor/hackingtool`, mounts the current directory into `/root/hackingtool`, enables stdin and a TTY, and publishes host port 22 to container port 22.

```bash
docker compose up
```

Note that the compose file references a prebuilt image (`vgpastor/hackingtool`) rather than building from the local `Dockerfile`. The compose file does not contain a `build:` section. This project does not verify the contents of that third-party image.

## Updating and Uninstalling

The **Update or Uninstall | Hackingtool** category contains two sections:

- **Update Tool or System**
  - *Update System* runs `apt update`/`full-upgrade` and installs `tor`, `openssl`, `curl`, and `python3-pip`.
  - *Update Hackingtool* removes the existing installation directories, clones the repository into `/etc/hackingtool`, and runs its `install.sh`.
- **Uninstall HackingTool**
  - *Uninstall* removes `/etc/hackingtool/` and `/usr/share/doc/hackingtool/`, then exits.

You can also update the installed copy from the command line with `update.sh`, which must run as root. It requires an internet connection, runs `git pull` inside `/usr/share/hackingtool`, and then re-runs `install.sh`:

```bash
sudo bash update.sh
```

See [Known Limitations](#known-limitations) regarding the paths these actions use.

## Tool Categories

The main menu contains the following categories. Each entry lists the module that defines it and examples of the tools it includes, taken from the code. The menu itself is the authoritative list; some categories contain subcategories.

| Category | Module | Examples |
|----------|--------|----------|
| Anonymously Surf (AnonSurf) | `tools/anonsurf.py` | Anonymously Surf (kali-anonsurf), Multitor |
| Information Gathering | `tools/information_gathering_tools.py` | Nmap, Dracnmap, Xerosploit, RED HAWK, ReconSpider, Infoga, ReconDog, Striker, SecretFinder, Shodan lookup, rang3r, Breacher |
| Wordlist Generator | `tools/wordlist_generator.py` | CUPP, WordlistCreator (wlcreator), Goblin WordGenerator |
| Wireless Attack Tools | `tools/wireless_attack_tools.py` | WiFi-Pumpkin, pixiewps, Bluetooth honeypot (bluepot), Fluxion, Wifiphisher, Wifite, fakeap (EvilTwin), fastssh |
| SQL Injection Tools | `tools/sql_tools.py` | sqlmap, NoSQLMap, DSSS, Explo, Blisqy, Leviathan, SQLScan |
| Phishing Attack Tools | `tools/phising_attack.py` | Autophisher RK, PyPhisher, AdvPhishing, Setoolkit, SocialFish, HiddenEye, Evilginx2, I-See-You, SayCheese, QRLJacking, BlackEye, ShellPhish, BlackPhish |
| Web Attack Tools | `tools/webattack.py` | Web2Attack, Skipfish, Sublist3r, checkURL, Blazy, subdomain takeover checker, Dirb |
| Post Exploitation Tools | `tools/post_exploitation.py` | Vegile, Hera Chrome Keylogger |
| Forensic Tools | `tools/forensic_tools.py` | Autopsy, Wireshark, Bulk extractor, Guymager, Toolsley |
| Payload Creator | `tools/payload_creator.py` | TheFatRat, Brutal, Stitch, MSFPC, Venom, Spycam, Mob-Droid, Enigma |
| Exploit Frameworks | `tools/exploit_frameworks.py` | RouterSploit, WebSploit, Commix |
| Reverse Engineering | `tools/reverse_engineering.py` | Androguard, Apk2Gold, JADX |
| DDoS Attack Tools | `tools/ddos.py` | ddos, SlowLoris, aSYNcrone, UFOnet, GoldenEye, SaphyraDDoS |
| Remote Administration Tools (RAT) | `tools/remote_administration.py` | Stitch, Pyshell |
| XSS Attack Tools | `tools/xss_attack.py` | DalFox, XSS-LOADER, Extended XSS Searcher, XSS-Freak, XSpear, XSSCon, XanXSS, XSStrike, RVuln |
| Steganography Tools | `tools/steganography.py` | SteganoHide, SteganoCracker, StegoCracker, Whitespace (snow) |
| Other Tools | `tools/other_tools.py` | Subcategories below, plus HatCloud |
| Update or Uninstall \| Hackingtool | `tools/tool_manager.py` | See [Updating and Uninstalling](#updating-and-uninstalling) |

### Other Tools subcategories

The **Other Tools** category (`tools/other_tools.py`) contains these subcategories, defined in `tools/others/`:

- **Social media brute-forcing** (`socialmedia.py`): Instagram Attack, AllinOne SocialMedia Attack, Facebook Attack, Application Checker
- **Android attacks** (`android_attack.py`): Keydroid, MySMS, Lockphish, DroidCam, EvilApp
- **IDN homograph attacks** (`homograph_attacks.py`): EvilURL
- **Email verification** (`email_verifier.py`): KnockMail
- **Hash cracking** (`hash_crack.py`): Hash Buster
- **Wi-Fi jamming / deauthentication** (`wifi_jamming.py`): WifiJammer-NG, KawaiiDeauther
- **Social media discovery** (`socialmedia_finder.py`): social_mapper, finduser, Sherlock, socialscan
- **Payload injection** (`payload_injection.py`): Debinject, Pixload
- **Web crawling** (`web_crawling.py`): Gospider
- **Mixed tools** (`mix_tools.py`): Terminal Multiplexer, Crivo

Tool names above are as they appear in the menu; several are offered as separate entries that point to the same project (for example, WifiPhisher appears under both Wireless Attack Tools and Phishing Attack Tools).

## Repository Layout

```
hackingtool.py          Entry point: builds the menu and handles first-run setup
core.py                 Base classes: HackingTool and HackingToolsCollection (menu logic)
install.sh              Root installer (apt or pacman), creates /usr/bin/hackingtool
update.sh               Pulls the latest code and re-runs install.sh
requirements.txt        Python dependencies
Dockerfile              Kali-based image for running the tool
docker-compose.yml      Compose service using the vgpastor/hackingtool image
generate_readme.py      Script that fills README_template.md with the tool list
tools/                  One module per menu category
tools/others/           Subcategory modules used by "Other Tools"
images/                 Screenshots
LICENSE                 MIT License
```

Each tool is a subclass of `HackingTool` with a `TITLE`, `DESCRIPTION`, optional `PROJECT_URL`, and lists of `INSTALL_COMMANDS`, `RUN_COMMANDS`, `UNINSTALL_COMMANDS`, and `OPTIONS`. Categories are subclasses of `HackingToolsCollection` with a `TOOLS` list.

## Known Limitations

- **Linux-focused.** Installation and the menu target Linux. Windows and other platforms are not supported by the menu.
- **Install and uninstall paths differ.** `install.sh` and `update.sh` use `/usr/share/hackingtool` and `/usr/bin/hackingtool`. The in-app *Update Hackingtool* and *Uninstall* actions operate on `/etc/hackingtool` and `/usr/share/doc/hackingtool`, so they do not remove the installation directory or the `/usr/bin/hackingtool` launcher created by `install.sh`.
- **Some installs are fragile.** The menu runs shell commands with `os.system`, and failures are not always reported back to the user. Tool-specific install and run steps depend on the upstream projects, which may change or disappear.
- **Dependency on upstream tools.** Each tool is fetched from its upstream project. This repository does not audit or vouch for their contents.
- **Contributor tooling.** `generate_readme.py` reads `README_template.md`, which is not included in this repository, so it cannot currently generate the README.
- **Tool status unknown.** Several tools are old, and the code does not record whether each one still works with current systems.

## Contributing

The upstream project is hosted at [https://github.com/Z4nzu/hackingtool](https://github.com/Z4nzu/hackingtool). To add a tool, create a `HackingTool` subclass in the appropriate `tools/` module, define its `TITLE`, `DESCRIPTION`, and `PROJECT_URL`, add its install and run commands, and register it in that category's `TOOLS` list, following the patterns in `core.py` and `tools/`.

## License

This project is licensed under the MIT License. Copyright (c) 2020 Mr.Z4nzu. See [LICENSE](LICENSE) for the full text.

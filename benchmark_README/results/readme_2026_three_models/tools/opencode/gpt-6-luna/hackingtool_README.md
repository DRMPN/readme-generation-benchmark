# Hackingtool

Hackingtool is a Python command-line menu for installing and launching a collection of security, reconnaissance, forensics, and related utilities. The menu groups tools by purpose; individual entries may install a separate third-party project or run a command already available on the system.

The launcher identifies itself as version **1.1.0**. This repository is Linux-oriented: the main program configures a working directory and opens its menu on Linux. It does not offer the same workflow on Windows or other operating systems.

> **Use responsibly:** Only use these tools on systems, accounts, and networks you own or are explicitly authorized to assess. Some entries perform intrusive actions, and many invoke shell commands with elevated privileges. Review commands and third-party projects before installing or running them. You are responsible for complying with applicable laws and rules of engagement.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Run from a checkout](#run-from-a-checkout)
- [Using the menu](#using-the-menu)
- [Tool categories](#tool-categories)
- [Docker files](#docker-files)
- [License](#license)

## Features

- Interactive terminal menus with tools grouped into collections.
- Per-tool menu actions, which may include installation, running, opening a project page, or a tool-specific action.
- A configurable directory for the tool folders installed by menu entries.
- An installer script for Kali/Parrot-style `apt` systems and Arch Linux `pacman` systems.

This is a launcher and collection, not a guarantee that every third-party tool is maintained, compatible with current systems, or installed by the main installer. Many entries have their own prerequisites; some entries provide only partial menu actions or expect a program to be installed separately.

## Requirements

- Linux for the normal launcher workflow.
- Python 3 and the Python packages listed in [`requirements.txt`](requirements.txt): `boxes`, `flask`, `lolcat`, and `requests`.
- The relevant system commands and dependencies for the selected tools. The menu and installer use utilities such as Git, `sudo`, `figlet`, `boxes`, and `lolcat`; individual tools may additionally require language runtimes, hardware, or other packages.
- Internet access for the installer and for menu actions that clone or download third-party projects.

The included `install.sh` requires root privileges and offers `apt` (Kali Linux/Parrot OS) and `pacman` (Arch Linux) paths. It updates/upgrades system packages, installs prerequisites, clones this repository into `/usr/share/hackingtool`, creates a virtual environment, and installs a `hackingtool` launcher in `/usr/bin`. Read the script before running it; it makes system-level changes.

## Installation

To use the repository installer on a supported distribution:

```bash
git clone https://github.com/Z4nzu/hackingtool.git
cd hackingtool
sudo bash install.sh
```

Choose the matching distribution option when prompted. After a successful install, the script instructs you to start the program with:

```bash
hackingtool
```

The installer checks for an existing `/usr/share/hackingtool` directory and asks whether to replace it. It also needs network access to fetch the repository and packages.

## Run from a checkout

For a manual launch, install the listed Python requirements and start the main program:

```bash
python3 -m pip install -r requirements.txt
python3 hackingtool.py
```

On its first Linux launch, the program asks where tool projects should be installed and saves that choice in `~/hackingtoolpath.txt`. You can choose a path manually or select the built-in default, `/home/hackingtool/`. The program creates the selected directory and changes into it before showing the menu. Menu actions may require additional system packages or elevated privileges.

## Using the menu

Choose a collection in the main menu, then choose a tool. Tool menus typically offer **Install** and **Run**, plus any actions defined by that entry. Some tools omit one or both of those actions or require manual setup. Use `99` to go back from a nested menu (or exit at the main menu); where a project URL is available, `98` opens its project page.

Install and run actions execute commands defined in the repository, often by passing them to the system shell. Review those commands and the linked upstream project before proceeding, especially when running as root. Tool availability and behavior depend on the external project, your operating system, and its dependencies.

## Tool categories

The main menu currently includes these collections:

| Collection | Examples of included entries |
| --- | --- |
| Anonymously Hiding Tools | Anonymously Surf, Multitor |
| Information gathering tools | Nmap, Dracnmap, port scanning, host-to-IP lookup, Xerosploit, RED HAWK, ReconSpider, Infoga, ReconDog, Striker, SecretFinder, Shodan, rang3r, Breacher, and an IsItDown web shortcut |
| Wordlist Generator | Cupp, WordlistCreator, Goblin WordGenerator, password-list entry |
| Wireless attack tools | WiFi-Pumpkin, pixiewps, BluePot, Fluxion, Wifiphisher, Wifite, EvilTwin, Fastssh, Howmanypeople |
| SQL Injection Tools | sqlmap, NoSqlMap, DSSS, Explo, Blisqy, Leviathan, SQLScan |
| Phishing attack tools | Autophisher RK, Pyphisher, AdvPhishing, Setoolkit, SocialFish, HiddenEye, Evilginx2, I-See_You, SayCheese, QR Code Jacking, BlackEye, ShellPhish, Thanos, QRLJacking, Miskphish, BlackPhish, and dnstwist (its menu entry does not define the title field used by the menu) |
| Web Attack tools | Web2Attack, Skipfish, SubDomain Finder, CheckURL, Blazy, Sub-Domain TakeOver, Dirb |
| Post exploitation tools | Vegile, Chrome Keylogger |
| Forensic tools | Autopsy, Wireshark, Bulk extractor, Guymager, Toolsley |
| Payload creation tools | The FatRat, Brutal, Stitch, MSFvenom Payload Creator, Venom Shellcode Generator, Spycam, Mob-Droid, Enigma |
| Exploit framework | RouterSploit, WebSploit, Commix, Web2Attack |
| Reverse engineering tools | Androguard, Apk2Gold, JadX |
| DDOS Attack Tools | SlowLoris, Asyncrone, UFOnet, GoldenEye, SaphyraDDoS |
| Remote Administrator Tools (RAT) | Stitch, Pyshell |
| XSS Attack Tools | DalFox, XSS Payload Generator, Extended XSS Searcher and Finder, XSS-Freak, XSpear, XSSCon, XanXSS, XSStrike, RVuln |
| Steganograhy tools | SteganoHide, StegnoCracker, StegoCracker, Whitespace |
| Other tools | SocialMedia Bruteforce (Instagram Attack, AllinOne SocialMedia Attack, Facebook Attack, Application Checker); Android Hacking tools (Keydroid, MySMS, Lockphish, DroidCam, EvilApp); HatCloud; IDN Homograph Attack (EvilURL); Knockmail; Hash Buster; Wifi Deauthenticate (WifiJammer-NG, KawaiiDeauther); SocialMedia Finder (facial and username search, Sherlock, SocialScan); Payload Injector (Debinject, Pixload); Web crawling (Gospider); Mix tools (Terminal Multiplexer, Crivo) |
| Update or Uninstall \| Hackingtool | Update System, Update Hackingtool, Uninstall HackingTool |

The list reflects entries wired into the current menu. It does not mean that each tool is bundled with this repository or that every entry has both an install and run action. Several entries link to independent upstream projects, and their requirements and behavior are maintained separately.

## Docker files

The repository includes a [`Dockerfile`](Dockerfile) based on Kali Linux and a [`docker-compose.yml`](docker-compose.yml). The Compose service references the `vgpastor/hackingtool` image, mounts the current directory at `/root/hackingtool`, opens an interactive terminal, and maps host port `22` to container port `22`. Review these settings and the image source before using them; the Compose port mapping is part of the supplied configuration, not a requirement of the Python menu.

## License

The repository's [`LICENSE`](LICENSE) is the MIT License. Third-party tools linked or installed by the menu may have separate licenses and terms.

# Hackingtool — All in One Hacking Tool for Linux

**Version 1.1.0** · **License: MIT** · **Platform: Linux** · **Python 3**

Hackingtool is a menu-driven command-line framework that bundles **more than 125 open-source security and penetration-testing tools** for Linux behind a single interface. It does not reimplement the attacks itself; each menu entry downloads the upstream project, runs its installer, and launches it from the framework's menu.

- Project page: <https://github.com/Z4nzu/hackingtool>
- Created by [Z4nzu](https://github.com/Z4nzu)

## ⚠️ Disclaimer

> **This tool is for educational and legal security-testing purposes only. Please don't use it for illegal activity.**
>
> Hackingtool must be run as **root** and installs third-party software from external repositories. Several bundled tools explicitly warn that monitoring or attacking systems and networks you do not own may be illegal in your country. You are solely responsible for how you use this software; it is provided "AS IS", without warranty of any kind (see the [MIT license](LICENSE)).

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Demo](#-demo)
- [Tool Index](#-tool-index)
- [Repository Layout](#-repository-layout)
- [Adding a New Tool](#-adding-a-new-tool)
- [License](#-license)

## ✨ Features

- **Single menu interface** for a large collection of security tools, grouped into 18 categories.
- **Install / Run / Update** individual tools from the menu; each tool shows its description and upstream project URL (`[98]` opens the project page, `[99]` goes back).
- **First-run setup** asks where downloaded tools should be installed (manual path or default `/home/hackingtool/`) and stores the choice in `~/hackingtoolpath.txt`.
- **Tool manager** built in: update the system or hackingtool itself, and uninstall the framework from the menu.
- Terminal UI rendered with `figlet`, `boxes` and `lolcat`.
- **Docker support** via `Dockerfile` and `docker-compose.yml`.

## 🔧 Requirements

- A Linux system — a Debian-based distribution (Kali Linux / Parrot OS) is recommended by the program itself; the installer also supports Arch Linux (pacman). On Windows the program only prints a warning and recommends running it on a Debian system.
- Root privileges (the installer refuses to run without them and most operations use `sudo`).
- Internet connection (checked by the installer).
- Python 3 with `pip` and `venv`.
- System packages: `git`, `python3-pip`, `figlet`, `boxes`, `php`, `curl`, `xdotool`, `wget` (installed automatically by `install.sh`).
- Python packages (`requirements.txt`): `boxes`, `flask`, `lolcat`, `requests`.

## 📥 Installation

### Option 1 — Install script (Kali/Parrot or Arch)

```bash
git clone https://github.com/Z4nzu/hackingtool.git
cd hackingtool
chmod +x install.sh
sudo bash install.sh
```

The script must be run **as root**. It asks whether to install via `apt` (option 1, Kali Linux / Parrot OS) or `pacman` (option 2, Arch Linux), then:

1. Updates package lists and installs the system dependencies listed above.
2. Clones the repository to `/usr/share/hackingtool`.
3. Creates a Python virtual environment there and installs `requirements.txt`.
4. Creates a launcher script at `/usr/bin/hackingtool` that activates the venv and runs `hackingtool.py`.

Afterwards, just type `hackingtool` in a terminal.

### Option 2 — Docker

Build and run locally (based on `kalilinux/kali-rolling`):

```bash
docker build -t hackingtool .
docker run -it hackingtool
```

Or use `docker-compose.yml`, which runs the published image `vgpastor/hackingtool` with a TTY attached and mounts the repository at `/root/hackingtool`:

```bash
docker compose up
```

Inside the container the default tool-install path is `/root/hackingtool/`.

## 🚀 Usage

```bash
sudo hackingtool        # after running install.sh
# or, from a checkout:
sudo python3 hackingtool.py
```

**First run:** you are asked where all downloaded tools should be installed:

- `[1]` Manual — enter a custom directory
- `[2]` Default — `/home/hackingtool/`

The choice is saved to `~/hackingtoolpath.txt` and reused on later runs; the program then changes into that directory and shows the main menu.

**Menus:** the main menu lists the tool categories (see the [Tool Index](#-tool-index)). Selecting a category shows its tools; selecting a tool shows its description and options — typically **Install**, **Run**, and any tool-specific extras. `[98]` opens the tool's upstream project page in a browser, `[99]` returns to the previous menu (or exits).

**Update / Uninstall:** choose **Update or Uninstall | Hackingtool** in the main menu to

- update the system via `apt`,
- update hackingtool itself (re-clones the repository and re-runs `install.sh`),
- uninstall hackingtool (removes `/etc/hackingtool/` and `/usr/share/doc/hackingtool/`).

Alternatively, update the installed copy with:

```bash
sudo bash update.sh
```

## 🖼 Demo

Screenshots (taken from an earlier version of the menu) are in the [`images/`](images/) directory:

![Main menu](images/A00.png)

![Tool submenu](images/A0.png)

## 🧰 Tool Index

All tools registered in the menu, exactly as shipped in this version.

### Anonymously Hiding Tools

- [Anonymously Surf](https://github.com/Und3rf10w/kali-anonsurf) — overwrites RAM on shutdown and changes IP (`anonsurf start/stop`)
- [Multitor](https://github.com/trimstray/multitor) — multiple Tor instances with different exit IPs

### Information Gathering Tools

- [Network Map (nmap)](https://github.com/nmap/nmap) — network discovery and security auditing
- [Dracnmap](https://github.com/Screetsec/Dracnmap) — scripted nmap exploitation/information gathering
- Port scanning — built-in wrapper around `nmap -O -Pn`
- Host to IP — built-in hostname resolution
- [Xerosploit](https://github.com/LionSec/xerosploit) — man-in-the-middle testing toolkit
- [RED HAWK (All In One Scanning)](https://github.com/Tuhinshubhra/RED_HAWK) — information gathering and vulnerability scanning
- [ReconSpider (For All Scanning)](https://github.com/bhavsec/reconspider) — OSINT framework for IPs, emails, websites, organizations
- IsItDown (Check Website Down/Up) — opens <https://www.isitdownrightnow.com/>
- [Infoga - Email OSINT](https://github.com/m4ll0k/Infoga) — email account information from public sources
- [ReconDog](https://github.com/s0md3v/ReconDog) — information gathering suite
- [Striker](https://github.com/s0md3v/Striker) — recon and vulnerability scanning suite
- [SecretFinder (like API & etc)](https://github.com/m4ll0k/SecretFinder) — finds API keys, tokens, JWTs in JavaScript files
- [Find Info Using Shodan](https://github.com/m4ll0k/Shodanfy.py) — Shodan lookups without an API key
- [Port Scanner - rang3r](https://github.com/floriankunushevci/rang3r) — multithreaded alive-host scanner
- [Breacher](https://github.com/s0md3v/Breacher) — multithreaded admin-panel finder

### Wordlist Generator

- [Cupp](https://github.com/Mebus/cupp) — interactive wordlist generator
- [WordlistCreator](https://github.com/Z4nzu/wlcreator) — generates password combinations by length/charset
- [Goblin WordGenerator](https://github.com/UndeadSec/GoblinWordGenerator)
- [Password list (1.4 Billion Clear Text Password)](https://github.com/Viralmaniar/SMWYG-Show-Me-What-You-Got) — searches the BreachCompilation leak

### Wireless Attack Tools

- [WiFi-Pumpkin](https://github.com/P0cL4bs/wifipumpkin3) — rogue access-point framework
- [pixiewps](https://github.com/wiire/pixiewps) — offline WPS Pixie Dust attack
- [Bluetooth Honeypot GUI Framework](https://github.com/andrewmichaelsmith/bluepot)
- [Fluxion](https://github.com/FluxionNetwork/fluxion)
- [Wifiphisher](https://github.com/wifiphisher/wifiphisher) — rogue AP framework for red-team Wi-Fi engagements
- [Wifite](https://github.com/derv82/wifite2) — automated wireless attack tool
- [EvilTwin](https://github.com/Z4nzu/fakeap) — Evil Twin attack with fake AP and fake page
- [Fastssh](https://github.com/Z4nzu/fastssh) — multithreaded SSH scan and brute force
- Howmanypeople — counts nearby people by Wi-Fi signals (wireless adapter required; warns it may be illegal to monitor networks you don't own)

### SQL Injection Tools

- [Sqlmap tool](https://github.com/sqlmapproject/sqlmap) — automated SQL injection detection/exploitation
- [NoSqlMap](https://github.com/codingo/NoSQLMap) — NoSQL injection auditing (requires MongoDB)
- [Damn Small SQLi Scanner](https://github.com/stamparm/DSSS) — GET/POST SQLi vulnerability scanner
- [Explo](https://github.com/dtag-dev-sec/explo) — describes web security issues in human/machine-readable format
- [Blisqy - Exploit Time-based blind-SQL injection](https://github.com/JohnTroony/Blisqy) — time-based blind SQLi in HTTP headers
- [Leviathan - Wide Range Mass Audit Toolkit](https://github.com/leviathan-framework/leviathan) — service discovery, brute force, SQLi detection (requires API keys)
- [SQLScan](https://github.com/Cvar1984/sqlscan) — quick scanner for SQL injection points

### Phishing Attack Tools

- [Autophisher RK](https://github.com/CodingRanjith/autophisher) — automated phishing toolkit
- [Pyphisher](https://github.com/KasRoudra/PyPhisher) — phishing tool with 77 website templates
- [AdvPhishing](https://github.com/Ignitetch/AdvPhishing) — advanced/OTP phishing
- [Setoolkit](https://github.com/trustedsec/social-engineer-toolkit) — Social-Engineer Toolkit
- [SocialFish](https://github.com/UndeadSec/SocialFish) — automated phishing tool and information collector
- [HiddenEye](https://github.com/Morsmalleo/HiddenEye) — modern phishing tool with tunneling services
- [Evilginx2](https://github.com/kgretzky/evilginx2) — man-in-the-middle phishing framework that bypasses 2FA (requires Go ≥ 1.14)
- [I-See_You](https://github.com/Viralmaniar/I-See-You) — locates a target via a phishing link
- [SayCheese](https://github.com/hangetzzu/saycheese) — takes webcam shots via a malicious link
- [QR Code Jacking](https://github.com/cryptedwolf/ohmyqr)
- [BlackEye](https://github.com/An0nUD4Y/blackeye) — phishing tool with 38 website templates
- [ShellPhish](https://github.com/An0nUD4Y/shellphish) — phishing tool for 18 social networks
- [Thanos](https://github.com/TridevReddy/Thanos) — browser-to-browser phishing toolkit
- [QRLJacking](https://github.com/OWASP/QRLJacking) — QR login hijacking (requires geckodriver)
- [BlackPhish](https://github.com/iinc0gnit0/BlackPhish)
- [Miskphish](https://github.com/jaykali/maskphish) — hides a phishing URL behind a normal-looking URL
- [dnstwist](https://github.com/elceef/dnstwist)

### Web Attack Tools

- [Web2Attack](https://github.com/santatic/web2attack) — web hacking framework
- Skipfish — active web application security reconnaissance (uses an existing `skipfish` install)
- [SubDomain Finder (Sublist3r)](https://github.com/aboul3la/Sublist3r) — enumerates subdomains via OSINT
- [CheckURL](https://github.com/UndeadSec/checkURL) — detects evil URLs using IDN homograph attacks
- [Blazy](https://github.com/UltimateHackers/Blazy) — login-page brute forcer (also finds clickjacking)
- [Sub-Domain TakeOver](https://github.com/edoardottt/takeover)
- [Dirb](https://gitlab.com/kalilinux/packages/dirb) — web content scanner with dictionary-based attacks

### Post Exploitation Tools

- [Vegile - Ghost In The Shell](https://github.com/Screetsec/Vegile) — sets up backdoors/rootkits and hides processes in Metasploit sessions
- [Chrome Keylogger](https://github.com/UndeadSec/HeraKeylogger)

### Forensic Tools

- Autopsy — cyber-investigation platform; runs the system-installed `autopsy`
- Wireshark — network capture and analysis; runs the system-installed `wireshark`
- [Bulk extractor](https://github.com/simsong/bulk_extractor) — extracts information without parsing the file system (GUI or CLI mode)
- [Disk Clone and ISO Image Acquire (Guymager)](https://guymager.sourceforge.io/) — forensic imager for media acquisition
- [Toolsley](https://www.toolsley.com/) — file signature verifier, file identifier, hash & validate, binary inspector, and more

### Payload Creation Tools

- [The FatRat](https://github.com/Screetsec/TheFatRat) — creates backdoors/payloads that bypass most antivirus
- [Brutal](https://github.com/Screetsec/Brutal) — payloads for HID devices (requires Arduino/TeensyDuino setup)
- [Stitch](https://nathanlopez.github.io/Stitch) — cross-platform Python RAT/payload builder
- [MSFvenom Payload Creator (MSFPC)](https://github.com/g0tmi1k/msfpc) — wrapper to generate many payload types
- [Venom Shellcode Generator](https://github.com/r00t-3xp10it/venom) — delivers payloads via a fake web page (LAN)
- [Spycam](https://github.com/indexnotfound404/spycam) — Win32 payload that exfiltrates webcam images
- [Mob-Droid](https://github.com/kinghacker0/Mob-Droid) — easy Metasploit payload generation for Android
- [Enigma](https://github.com/UndeadSec/Enigma) — multi-platform payload dropper

### Exploit Framework

- [RouterSploit](https://github.com/threat9/routersploit) — exploitation framework for embedded devices
- [WebSploit](https://github.com/The404Hacking/websploit) — advanced MITM framework
- [Commix](https://github.com/commixproject/commix) — automated OS command injection and exploitation
- [Web2Attack](https://github.com/santatic/web2attack)

### Reverse Engineering Tools

- [Androguard](https://github.com/androguard/androguard) — reverse engineering and malware analysis of Android apps
- [Apk2Gold](https://github.com/lxdvs/apk2gold) — decompiles Android apps to Java
- [JadX](https://github.com/skylot/jadx) — Dex-to-Java decompiler (APK, dex, aar, zip)

### DDoS Attack Tools

*Listed in the menu for security testing purposes only.*

- SlowLoris — HTTP denial-of-service (installed via `pip3 install slowloris`)
- [Asyncrone | Multifunction SYN Flood DDoS Weapon](https://github.com/fatihsnsy/aSYNcrone)
- [UFOnet](https://github.com/epsylon/ufonet) — P2P DoS/DDoS toolkit with a GUI
- [GoldenEye](https://github.com/jseidl/GoldenEye) — HTTP DoS test tool
- [SaphyraDDoS](https://github.com/anonymous24x7/Saphyra-DDoS)

### Remote Administration Tools (RAT)

- [Stitch](https://github.com/nathanlopez/Stitch) — cross-platform Python framework for building custom payloads (Windows/Mac/Linux)
- [Pyshell](https://github.com/knassar702/pyshell) — RAT that can upload/download files and execute OS commands

### XSS Attack Tools

- [DalFox (Finder of XSS)](https://github.com/hahwul/dalfox) — XSS scanning and parameter analysis (requires Go)
- [XSS Payload Generator](https://github.com/capture0x/XSS-LOADER) — payload generator, scanner and dork finder
- [Extended XSS Searcher and Finder](https://github.com/Damian89/extended-xss-search)
- [XSS-Freak](https://github.com/PR0PH3CY33/XSS-Freak) — XSS scanner written in Python 3
- [XSpear](https://github.com/hahwul/XSpear) — XSS scanner distributed as a Ruby gem
- [XSSCon](https://github.com/menkrep1337/XSSCon)
- [XanXSS](https://github.com/Ekultek/XanXSS) — reflected XSS search with template-based payloads
- [Advanced XSS Detection Suite (XSStrike)](https://github.com/UltimateHackers/XSStrike)
- [RVuln](https://github.com/iinc0gnit0/RVuln) — multithreaded web vulnerability scanner written in Rust

### Steganography Tools

- SteganoHide — hide/extract data with `steghide`
- StegnoCracker — uncovers hidden data with a brute-force utility (`stegcracker`)
- [StegoCracker](https://github.com/W1LDN16H7/StegoCracker) — hide data in image/audio files and retrieve it
- [Whitespace](https://github.com/beardog108/snow10) — steganography using whitespace and Unicode characters

### Other Tools

- **SocialMedia Bruteforce**
  - [Instagram Attack](https://github.com/chinoogawa/instaBrute) — brute force against Instagram
  - [AllinOne SocialMedia Attack](https://github.com/Matrix07ksa/Brute_Force) — brute force for Gmail, Hotmail, Twitter, Facebook, Netflix
  - [Facebook Attack](https://github.com/Matrix07ksa/Brute_Force) — Facebook brute forcer
  - [Application Checker](https://github.com/jakuta-tech/underhanded) — checks if an app is installed on the target device through a link
- **Android Hacking Tools**
  - [Keydroid](https://github.com/F4dl0/keydroid) — Android keylogger + reverse shell
  - [MySMS](https://github.com/papusingh2sms/mysms) — generates an Android app to read SMS over WAN
  - [Lockphish](https://github.com/JasonJerry/lockphish) — grabs Windows credentials / Android PIN / iPhone passcode via a phishing lock screen
  - [DroidCam (Capture Image)](https://github.com/kinghacker0/WishFish) — grabs a front-camera snap using a link
  - [EvilApp (Hijack Session)](https://github.com/crypticterminal/EvilApp) — generates an Android app that hijacks authenticated cookie sessions
- **HatCloud (Bypass CloudFlare for IP)** — [HatCloud](https://github.com/HatBashBR/HatCloud) discovers the real IP behind CloudFlare
- **IDN Homograph Attack** — [EvilURL](https://github.com/UndeadSec/EvilURL) generates and detects unicode evil domains
- **Email Verify Tools** — [Knockmail](https://github.com/heywoodlh/KnockMail) verifies if an email address exists
- **Hash Cracking Tools** — [Hash Buster](https://github.com/s0md3v/Hash-Buster) automatic hash-type identification (MD5, SHA1, SHA256, SHA384, SHA512)
- **Wifi Deauthenticate**
  - [WifiJammer-NG](https://github.com/MisterBianco/wifijammer-ng) — continuously jams Wi-Fi clients and access points in range
  - [KawaiiDeauther](https://github.com/aryanrtm/KawaiiDeauther) — deauth jamming and fake AP spam
- **SocialMedia Finder**
  - [Find SocialMedia By Facial Recognation System](https://github.com/Greenwolf/social_mapper) — correlates profiles via facial recognition
  - [Find SocialMedia By UserName](https://github.com/xHak9x/finduser) — finds usernames across 75+ social networks
  - [Sherlock](https://github.com/sherlock-project/sherlock) — hunts down social media accounts by username
  - [SocialScan | Username or Email](https://github.com/iojw/socialscan) — checks username/email availability on online platforms
- **Payload Injector**
  - [Debinject](https://github.com/UndeadSec/Debinject) — injects malicious code into `*.deb` packages
  - [Pixload](https://github.com/chinarulezzz/pixload) — creates/injects payloads into images
- **Web Crawling** — [Gospider](https://github.com/jaeles-project/gospider) — fast web spider written in Go
- **Mix Tools**
  - Terminal Multiplexer — installs `tilix`, a tiling terminal emulator
  - [Crivo](https://github.com/GMDSantana/crivo) — extracts and filters URLs, IPs, domains and subdomains from pages or text

### Update or Uninstall | Hackingtool

- **Update Tool or System** — update the system (`apt update && apt full-upgrade`) or update hackingtool itself
- **Uninstall HackingTool** — remove the framework

## 📁 Repository Layout

```
.
├── hackingtool.py        # Entry point: registers all tool collections, first-run path setup
├── core.py               # Framework: HackingTool / HackingToolsCollection base classes and menu engine
├── tools/                # One module per tool category
│   └── others/           # Sub-categories of "Other tools"
├── install.sh            # Root installer (apt or pacman), creates the `hackingtool` launcher
├── update.sh             # Updates the installed copy and re-runs install.sh
├── Dockerfile            # Kali-based container image
├── docker-compose.yml    # Runs the vgpastor/hackingtool image with the repo mounted
├── requirements.txt      # Python dependencies (boxes, flask, lolcat, requests)
├── generate_readme.py    # Regenerates the tool index in README.md from the registered tools
├── images/               # Demo screenshots
└── LICENSE               # MIT
```

## ➕ Adding a New Tool

Tools are simple Python classes registered in the framework:

1. Create a module under `tools/` (or `tools/others/`) and subclass `HackingTool` with the attributes `TITLE`, `DESCRIPTION`, `INSTALL_COMMANDS`, `UNINSTALL_COMMANDS`, `RUN_COMMANDS`, `OPTIONS` and `PROJECT_URL` — see `core.py` for the base class and any existing file in `tools/` for examples.
2. Group related tools with a `HackingToolsCollection` subclass.
3. Register the collection in the `all_tools` list in `hackingtool.py`.

`generate_readme.py` can regenerate the tool index in this README from the registered tools (it reads a `README_template.md` template and replaces `{{toc}}` and `{{tools}}` placeholders).

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file. Copyright (c) 2020 Mr.Z4nzu.
# python-spider-66zrgj89

A collection of Python web-scraping and automation scripts covering video platforms, novel and document sites, music, images, e-commerce, login and captcha handling, QR code generation, and a Scrapy project.

> **Note:** This README was written from the file listing alone, not from the source code. Descriptions of individual scripts are inferred from their names and should be checked against the code. Dependencies, usage commands, and configuration details need to be confirmed before publishing.

---

## Table of Contents

- [Overview](#overview)
- [Disclaimer](#disclaimer)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Module Reference](#module-reference)
- [Scrapy Project](#scrapy-project)
- [QR Code Generator (MyQR)](#qr-code-generator-myqr)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This repository is a set of standalone scripts for learning and experimenting with web scraping and automation. Most scripts are independent, so you can run any one without the others. The main topics are:

| Category | Target | Purpose (inferred) |
|---|---|---|
| Video | Bilibili | Download videos, handle "lucky man" feature, convert danmaku XML to ASS subtitles |
| Video | Douyin (TikTok China) | Fetch videos and signatures, with an improved "pro" version |
| Novels | Biquge, Biquku, Xbqg, Baiwan | Crawl and save novel text by chapter |
| Documents | Baidu Wenku | Extract document content, with a "pro" version |
| Music | NetEase Cloud Music | Fetch song lists and audio (`music_list.txt`) |
| Images | Unsplash | Download wallpapers and photos |
| Comics / Cartoons | Various | Download comics and cartoon episodes |
| E-commerce / Finance | JD.com, financial data | Price and product data, financial data collection |
| Login / Captcha | Taobao, 12306, Geetest, a university academic system (zhengfang) | Simulated login and captcha recognition |
| Utilities | QR codes, proxies, downloaders | Generate QR codes, manage proxy IPs, download files |
| Framework | Scrapy | A full crawler project with pipelines, middlewares, and items |

---

## Disclaimer

**Use these scripts responsibly and only in accordance with the law.**

- Respect each website's `robots.txt`, Terms of Service, and copyright.
- Do not use the scripts to bypass authentication, overload servers, or redistribute copyrighted content.
- Login, captcha, and signature-related scripts (Taobao, 12306, Geetest, Douyin signatures, zhengfang) are for education and research. Do not use them to access accounts you do not own or to violate platform rules.
- Add delays between requests and avoid high-concurrency crawling.
- The authors are not responsible for misuse.

---

## Project Structure

```
python-spider-66zrgj89/
├── Bilibili & video
│   ├── bilibili.py
│   ├── bilibili_luckyman.py
│   ├── video_downloader.py
│   ├── video_download.py
│   ├── vidoe_downloader.py          # filename typo in original repo
│   ├── xml2ass.py                   # danmaku XML → ASS subtitles
│   └── cartoon.py
├── Douyin
│   ├── douyin.py
│   ├── douyin_pro.py
│   ├── fuck-byted-acrawler.js       # JS for ByteDance request signatures
│   ├── app.js
│   └── index.html
├── Novels
│   ├── biqukan.py
│   ├── biquge20180731.py
│   ├── baiwan.py
│   └── xbqg_spider.py
├── Documents
│   ├── baiduwenku.py
│   └── baiduwenku_pro_1.py
├── Music
│   ├── Netease.py
│   └── music_list.txt
├── Images
│   ├── unsplash.py
│   ├── unsplash20180731.py
│   └── api.py
├── E-commerce & finance
│   ├── jd.py
│   └── financical.py
├── Login & captcha
│   ├── taobao_login.py
│   ├── 12306.py
│   ├── geetest.py
│   ├── shuaia.py
│   ├── zhengfang.txt
│   └── code.jpg
├── Utilities
│   ├── daili.py                     # proxy handling
│   ├── downloader.py
│   ├── download.py
│   ├── hero.py
│   ├── file.txt
│   └── question.txt
├── Scrapy project
│   ├── scrapy.cfg
│   ├── spider.py
│   ├── comic_spider.py
│   ├── items.py
│   ├── pipelines.py
│   ├── middlewares.py
│   └── settings.py
├── MyQR (QR code library)
│   ├── myqr.py
│   ├── matrix.py  structure.py  theqrmodule.py
│   ├── constant.py  data.py  draw.py  ECC.py  terminal.py
│   ├── qrcode.png  bg.png
│   └── requirements.txt
├── Assets
│   ├── 1.png  test_1.png  gzh-1.jpg  spider.png  zf.png
└── requirements.txt (and README.md files in subfolders)
```

Some subfolders contain their own `README.md` and `requirements.txt`. Check those first when working in a specific category.

---

## Installation

### Requirements

- Python 3.7 or later (3.8+ recommended)
- pip
- Node.js (only if you run the Douyin signature script, which uses `fuck-byted-acrawler.js`)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/python-spider-66zrgj89.git
   cd python-spider-66zrgj89
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. Install dependencies. The repository has several `requirements.txt` files, so install the root one first, then any in the subfolder you plan to use:

   ```bash
   pip install -r requirements.txt
   pip install -r MyQR/requirements.txt    # only if you use the QR code tool
   ```

   Typical libraries for this kind of project include `requests`, `beautifulsoup4`, `lxml`, `scrapy`, `pillow`, `pycryptodome`, `selenium`, and `qrcode`. Confirm the exact list in the requirements files.

4. For the Douyin signature script, install Node.js and any npm packages the JS file needs.

---

## Usage

Each script is run directly. Run it from the directory that contains it so relative paths (such as `music_list.txt` or `code.jpg`) resolve correctly.

```bash
python biqukan.py                # crawl a novel
python unsplash.py               # download images
python myqr.py "https://example.com" -v 5 -l H -p bg.png   # generate a QR code
scrapy crawl <spider_name>       # run the Scrapy project (from the directory with scrapy.cfg)
```

Most scripts prompt for input or have configuration variables near the top. Check each file for:

- Target URLs or IDs
- Output directory
- Request headers (User-Agent, Cookie)
- Proxy settings (see `daili.py`)

### Typical Workflow

1. Pick the category you need.
2. Read its `README.md` if it exists.
3. Install the requirements.
4. Adjust the configuration (URLs, headers, output path).
5. Run the script and check the output folder.

---

## Module Reference

### Bilibili and Video

| File | Description |
|---|---|
| `bilibili.py` | Bilibili video info and download. |
| `bilibili_luckyman.py` | Variant script for a specific Bilibili feature. |
| `video_downloader.py` / `video_download.py` / `vidoe_downloader.py` | General video downloaders. Multiple versions exist, so compare them before choosing one. |
| `xml2ass.py` | Converts Bilibili danmaku (bullet-comment) XML into ASS subtitle files for players such as mpv or PotPlayer. Two copies exist in the repository. |
| `cartoon.py` | Cartoon/animation episode downloader. |

### Douyin

| File | Description |
|---|---|
| `douyin.py` | Basic Douyin scraper. |
| `douyin_pro.py` | Extended version. |
| `fuck-byted-acrawler.js` | JavaScript that generates the `_signature` or `a_bogus` parameter. Called from Python. |
| `app.js`, `index.html` | Small web front end, possibly for testing signatures or viewing results. |

### Novels

| File | Description |
|---|---|
| `biqukan.py` | Scrapes novels from Biquku (two copies). |
| `biquge20180731.py` | Biquge novel crawler, dated 2018-07-31. |
| `baiwan.py` | Novel site crawler. |
| `xbqg_spider.py` | Xbqg (新笔趣阁) novel crawler. |

### Documents

| File | Description |
|---|---|
| `baiduwenku.py` | Extracts text from Baidu Wenku documents. |
| `baiduwenku_pro_1.py` | Improved version. |

### Music

| File | Description |
|---|---|
| `Netease.py` | NetEase Cloud Music song list and audio fetcher. |
| `music_list.txt` | Input list of songs or playlist IDs. |

### Images and Wallpapers

| File | Description |
|---|---|
| `unsplash.py` | Downloads images from Unsplash through its API. |
| `unsplash20180731.py` | Earlier version. |
| `api.py` | API helper, possibly for Unsplash or another image service. |

### E-commerce and Finance

| File | Description |
|---|---|
| `jd.py` | JD.com product or price scraper. |
| `financical.py` | Financial data collection. |

### Login and Captcha

| File | Description |
|---|---|
| `taobao_login.py` | Simulated Taobao login. |
| `12306.py` | Railway ticket site automation. |
| `geetest.py` | Geetest slider captcha handling. |
| `shuaia.py` | Captcha or login helper. |
| `zhengfang.txt`, `code.jpg` | Sample for a university academic system (zhengfang) login with captcha. |

### Utilities

| File | Description |
|---|---|
| `daili.py` | Proxy IP fetching and rotation. |
| `downloader.py` / `download.py` | Generic file downloaders. |
| `hero.py` | Game hero data scraper (inferred). |
| `file.txt`, `question.txt` | Input or data files used by scripts. |

---

## Scrapy Project

The Scrapy files form a standard project layout:

```
scrapy.cfg          # project configuration
spider.py           # spider definition
comic_spider.py     # comic spider
items.py            # data item definitions
pipelines.py        # item processing and saving
middlewares.py      # request/response middleware (headers, proxies)
settings.py         # crawler settings
```

Run it from the folder containing `scrapy.cfg`:

```bash
scrapy list                       # show available spiders
scrapy crawl comic                # run a spider (name set in comic_spider.py)
scrapy crawl comic -o output.json # export to JSON
```

Recommended settings to review in `settings.py`:

- `ROBOTSTXT_OBEY = True`
- `DOWNLOAD_DELAY`
- `USER_AGENT`
- `ITEM_PIPELINES` and `DOWNLOADER_MIDDLEWARES`

---

## QR Code Generator (MyQR)

The `myqr.py` module and its supporting files (`matrix.py`, `structure.py`, `theqrmodule.py`, `constant.py`, `data.py`, `draw.py`, `ECC.py`, `terminal.py`) form a QR code library. It can produce plain or artistic QR codes, optionally blended into a background image such as `bg.png`.

Example:

```bash
python myqr.py "https://github.com" -v 5 -l H -p bg.png -c
```

| Option | Meaning |
|---|---|
| `words` | Text or URL to encode |
| `-v` | Version (1–40), controls size |
| `-l` | Error correction level: L, M, Q, or H |
| `-p` | Picture to blend in |
| `-c` | Colorize output |
| `-n` | Output file name |

Sample output images in the repository: `qrcode.png`, `bg.png`, `zf.png`.

---

## Troubleshooting

| Problem | Suggested fix |
|---|---|
| `ModuleNotFoundError` | Install the requirements for that folder. |
| HTTP 403 or 429 | Add a realistic `User-Agent`, slow down requests, or use a proxy. |
| Empty results | The site's HTML or API may have changed. Update the selectors or endpoints. |
| Douyin signature fails | Check that Node.js is installed and the JS file runs. |
| Garbled Chinese text | Save output with `encoding='utf-8'`. |
| Captcha failures | Captcha logic is fragile. Expect to maintain it. |
| File not found | Run the script from its own directory, or use absolute paths. |

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-change`.
3. Commit your changes with clear messages.
4. Open a pull request describing what changed and how you tested it.

When adding a new spider, include a short description, the required dependencies, and a usage example. Please respect the disclaimer above.

---

## License

No license file was included in the listing. Add a `LICENSE` file (for example MIT or Apache-2.0) and update this section. Until then, all rights are reserved by the author.

---

## Acknowledgements

- The MyQR module is based on the open-source `MyQR` project by the original author.
- Thanks to the authors of Scrapy, Requests, BeautifulSoup, and the other libraries this project uses.

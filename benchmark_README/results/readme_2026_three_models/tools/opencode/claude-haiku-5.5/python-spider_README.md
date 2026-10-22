# Python Spider

A collection of standalone Python web-scraping and downloading scripts. Each subfolder or top-level file is an independent example, not a single installable package. Most were written for learning, and many target websites or APIs that have since changed.

Some of the source files contain Chinese comments and the original documentation is in Chinese. The project's own docs reference the author's Python 3 web-scraping tutorial series, and the 2020 tutorial index is in [`2020/README.md`](2020/README.md).

## Status

Read this before running anything:

- **Many examples are likely outdated.** The 2020 tutorial README itself says that many practical examples "have already become invalid." Site layouts, APIs, and anti-bot measures change, so a script may fail without any code change.
- **Several scripts need configuration before they run.** Examples include placeholder values such as `xxx`, `username`/`password`, and empty API keys (`AK`/`SK` in `2020/api/api.py`). Some also use hard-coded Windows paths such as `D:/chromedriver` or `J:\迅雷下载\chromedriver.exe`.
- **Some scripts rely on third-party services** that may be unavailable. For example, `douyin/douyin.py` posts to a signature service at a hard-coded address, and `douyin/README.md` notes that the service may stop working.
- **Some scripts are Windows-only.** `2020/bilibili/download.py` imports `win32com`, and `2020/taobao/taobao_login.py` depends on a local Chrome driver and screen-image matching through `pyautogui`.
- **Some scripts are for code reading only.** `2020/api/api.py` uses the Jupyter magic `%matplotlib inline`, so it is not a standalone Python script.
- **No tests** are included.
- **No license file** is included, so the reuse terms are not stated in this repository.

## Contents

| Path | Description | Entry point |
| --- | --- | --- |
| `bilibili/` | Downloads Bilibili videos and danmaku (comments). Converts the XML danmaku to ASS subtitle format (`xml2ass.py`). | `bilibili.py` |
| `bilibili_luckyman/` | Collects user names, IDs, and comments from the forwards of a Bilibili dynamic post. | `bilibili_luckyman.py` |
| `douyin/` | Downloads videos from a Douyin user account. | `douyin.py` |
| `dingdong/` | Downloads product review images from JD.com search results. | `jd.py` |
| `video_downloader/` | Tkinter GUI for the "VIP video" helper. Includes a bundled QR-code generator package, `MyQR/`. | `video_downloader.py` |
| `zhengfang_system_spider/` | Retrieves a student's timetable, grades, and grade points from a school academic system that uses the ZhengFang platform. | `spider.py` |
| `cartoon/` | Scrapy project that crawls comic chapter pages and saves images. | `scrapy crawl comic` |
| `baiwan/` | Quiz-answer helper for a live trivia show. It fetches question data, searches for answers, and writes them to `question.txt`. The API URL is a placeholder, so it does not run as shipped. | `baiwan.py` |
| `Netease/` | Netease Cloud Music request helper implementing the site's AES/RSA request encryption. Includes a `music_list.txt` file. | `Netease.py` |
| `one_hour_spider/` | Several small examples from the author's one-hour series, including novel downloaders for `biqukan` and `biquge`, an Unsplash photo downloader, and a video downloader. | Each `.py` file |
| `2020/` | Code for the 2020 tutorial series. Subfolders include `xbqg/` (novel), `dmzj/` (comics), `zycjw/` (video, uses FFmpeg), `api/` (image beautification API), `taobao/` (login automation), and `bilibili/` (danmaku). | Each subfolder's `.py` file |
| `geetest.py` | Selenium example for handling a slider CAPTCHA by reading the canvas image. | `geetest.py` |
| `12306.py` | Selenium-style train-ticket query and booking automation using `splinter`. Uses placeholder credentials and a Windows chromedriver path. | `12306.py` |
| `daili.py` | Scrapes proxy addresses from a public proxy-listing site (xicidaili). | `daili.py` |
| `downloader.py` | Generic file downloader with a terminal progress bar. Prompts for a URL. | `downloader.py` |
| `hero.py` | Downloads League of Legends hero images from a Fiddler-captured API. | `hero.py` |
| `biqukan.py` | Downloads a novel from a web novel site into a text file. | `biqukan.py` |
| `baiduwenku.py`, `baiduwenku_pro_1.py` | Extract text from Baidu Wenku documents. `baiduwenku.py` uses Selenium and a hard-coded Windows chromedriver path. | Each file |
| `douyin_pro.py` | Alternative Douyin video downloader using `splinter`. Hard-codes a Windows chromedriver path. | `douyin_pro.py` |
| `financical.py` | Retrieves financial indicators for Hong Kong stocks from `quotes.money.163.com`. Imports `pymysql`, so it appears to store results in MySQL. | `financical.py` |
| `shuaia.py` | Downloads images from a picture site, saving them as `.jpg` files. | `shuaia.py` |

Some subfolders and files are not described in detail here. Check the source file's header comments for the latest details.

## Requirements

Python 3 is required. The `zhengfang_system_spider/README.md` specifies Python 3.6.

There is no top-level requirements file. Install dependencies per project as needed.

Only two projects include a requirements file:

- `video_downloader/requirements.txt`: `imageio`, `numpy`, `Pillow`, `beautifulsoup4`
- `zhengfang_system_spider/requirements.txt`: `lxml==4.6.3`, `requests==2.20.0`, `Pillow>=6.2.2`, `beautifulsoup4==4.6.0`

Other third-party packages are imported by the scripts but are not listed in any requirements file. These include:

- `requests`, `beautifulsoup4`, `lxml`: used by most scripts
- `selenium`: `geetest.py`, `baiduwenku.py`, `daili.py`, `taobao`
- `splinter`: `12306.py`, `douyin_pro.py`
- `Crypto` (PyCryptodome): `Netease/Netease.py`
- `click`: `Netease/Netease.py`
- `pymysql`: `financical.py`
- `scrapy`: `cartoon/`
- `tqdm`: `2020/xbqg/`, `2020/dmzj/`
- `ffmpy3`: `2020/zycjw/` (also needs FFmpeg installed)
- `pyautogui`, `retrying`: `2020/taobao/`
- `opencv-python` (`cv2`), `numpy`, `matplotlib`: `2020/api/`
- `pywin32` (`win32com`): `2020/bilibili/download.py`
- `Pillow`: several scripts

Some projects also need external tools:

- **FFmpeg**: the Bilibili downloader (`bilibili/README.md`) and `2020/zycjw/`
- **Chrome or Chromium and a matching ChromeDriver**: Selenium and splinter scripts

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd python-spider
```

Install the requirements for a specific project. For example, for the ZhengFang spider:

```bash
cd zhengfang_system_spider
pip install -r requirements.txt
```

For the others, install the packages listed above as needed.

## Usage

Run each script from its own folder, since most of them use relative paths for output.

### Bilibili (`bilibili/`)

```bash
cd bilibili
python bilibili.py -d 猫 -k 猫 -p 10
```

- `-d`: output folder name
- `-k`: Bilibili search keyword
- `-p`: number of search-result pages to download

Requires FFmpeg for merging segmented videos, according to `bilibili/README.md`.

To convert a danmaku XML file to ASS format:

```bash
python xml2ass.py -s 1920x1080 input.xml
```

`-s` (stage size, `WIDTHxHEIGHT`) is required. Other options include `-o` (output file), `-fn` (font), `-fs` (font size), `-a` (alpha), `-l` (lifetime in seconds), `-p` (bottom protected height), and `-r` (reduce comments when the screen is full).

### Douyin (`douyin/`)

```bash
cd douyin
python douyin.py
```

The script uses a hard-coded external signature service (see "Status" above).

### JD.com review images (`dingdong/`)

```bash
cd dingdong
python jd.py -k 芒果
```

- `-k`: search keyword (required)
- `-d`: output folder (defaults to the script's folder)
- `-n`: number of products whose review images are downloaded

### ZhengFang academic system (`zhengfang_system_spider/`)

```bash
cd zhengfang_system_spider
python spider.py
```

Follow the prompts for the school's academic system URL, student ID, password, and CAPTCHA. Results are saved to `zhengfang.txt` in the same folder. This script is intended for your own account data; see "Responsible use" below.

### Video downloader GUI (`video_downloader/`)

```bash
cd video_downloader
pip install -r requirements.txt
python video_downloader.py
```

Opens a Tkinter window. The `MyQR/` package is a local module for generating QR codes.

### Scrapy comic crawler (`cartoon/`)

```bash
cd cartoon
scrapy crawl comic
```

The spider is named `comic` in `cartoon/cartoon/spiders/comic_spider.py`. The spider crawls chapter links and saves images through the item pipeline in `cartoon/cartoon/pipelines.py`. Scrapy must be installed.

### Other scripts

Run each script with `python <filename>.py`. Check its `__main__` block or header comments for required arguments and configuration. Several scripts need placeholder values replaced before use, and some have hard-coded file paths that need changing.

## Responsible use

These scripts access third-party websites and services. Before running any of them:

- Check the site's terms of service and `robots.txt`.
- Keep request rates reasonable. Several scripts include `time.sleep` calls, but many do not.
- Do not use credentials that you do not own. Several scripts, including `12306.py` and `2020/taobao/taobao_login.py`, log in to user accounts.
- Respect copyright. Some scripts download novels, comics, videos, or images. Use them only for content you have the right to access.

## Attribution

Most scripts in this repository are attributed to Jack Cui (Jack-Cherish). The source code headers and project READMEs refer to a Python web-scraping tutorial series by that author. Some subfolders also credit other contributors, such as `steven7851` in `douyin/README.md`.

## License

No license file is included in this repository. Check with the repository owner before reusing or redistributing the code.

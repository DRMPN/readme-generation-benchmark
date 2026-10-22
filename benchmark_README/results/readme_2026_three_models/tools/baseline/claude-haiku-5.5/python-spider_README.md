# Python Spider

A collection of standalone Python web-crawler and scraping scripts. The repository contains many small examples covering different sites and techniques, from novel and comic downloaders to video, danmaku (bullet-comment), and music downloaders, plus a university-system grade scraper and a 2020 tutorial series. Each script is largely independent, so there is no single entry point or shared package.

> **Note:** The scripts target websites and APIs that change over time. The 2020 tutorial notes that many of its earlier examples are no longer working, and several scripts depend on external services that may be unavailable.

## Repository Overview

| Path | Description (from the supplied files) |
| --- | --- |
| `2020/` | Python 3 crawler tutorial series (2020). Subfolders: `xbqg` (novel download), `dmzj` (comic download), `zycjw` (video download), `api` (image beautify API call), `bilibili` (video and danmaku), `taobao` (login script). |
| `bilibili/` | Searches Bilibili, downloads videos and danmaku, and converts XML danmaku to ASS subtitles. |
| `bilibili_luckyman/` | Random prize-draw helper that reads repost data from a Bilibili dynamic. |
| `baiwan/` | Baiwan quiz helper that searches Baidu Zhidao for answers. Includes a Node.js `app.js` that serves `index.html` and pushes messages over Socket.IO. |
| `baiduwenku.py`, `baiduwenku_pro_1.py` | Baidu Wenku document text extraction. |
| `biqukan.py`, `one_hour_spider/biqukan.py`, `one_hour_spider/biquge20180731.py` | Novel downloaders for biqukan and biqubao sites. |
| `cartoon/` | Scrapy project with a comic spider (`cartoon/spiders/comic_spider.py`). |
| `daili.py` | Fetches proxy IPs from xicidaili and tests them with `ping`. |
| `dingdong/` | Downloads JD product review photos by keyword. |
| `douyin/`, `douyin.py`, `douyin_pro.py` | Downloads Douyin (TikTok China) videos for a user. |
| `downloader.py` | Generic file downloader with a progress bar. |
| `financical.py` | Downloads financial statement data for a Hong Kong stock and stores it in MySQL. |
| `geetest.py` | Experimental slider-captcha (Geetest) recognition using Selenium and Pillow. |
| `hero.py` | Downloads hero images and equipment data for a mobile game's helper API. |
| `one_hour_spider/` | Assorted short scripts: novel, Unsplash wallpaper, and video downloaders. |
| `Netease/` | Downloads songs from NetEase Cloud Music listed in `music_list.txt`. |
| `shuaia.py` | Downloads images from shuaia.net. |
| `video_downloader/` | Tkinter GUI for playing or downloading videos via third-party parsing pages, with QR-code generation via a bundled `MyQR` package. |
| `zhengfang_system_spider/` | Scrapes a university Zhengfang academic system for timetable, grades, and grade-exam results. |
| `12306.py` | Selenium-based ticket-booking automation script for 12306.cn. |

## Setup

Clone the repository:

```bash
git clone git@github.com:Jack-Cherish/python-spider.git
cd python-spider
```

Python is not versioned for the whole repository. The `zhengfang_system_spider/README.md` lists **Python 3.6** as its environment. The `.pyc` cache files in the tree are for CPython 3.4 and 3.5, so older interpreters were used at some point.

There is no top-level requirements file. Only two folders include one:

**`video_downloader/requirements.txt`**
```text
imageio
numpy
Pillow
beautifulsoup4
```

**`zhengfang_system_spider/requirements.txt`**
```text
lxml==4.6.3
requests==2.20.0
Pillow>=6.2.2
beautifulsoup4==4.6.0
```

Install dependencies for a specific project:

```bash
cd zhengfang_system_spider
pip install -r requirements.txt
```

For other scripts, install the packages their `import` statements require. Examples include `requests`, `beautifulsoup4`, `lxml`, `selenium`, `splinter`, `Pillow`, `pymysql`, `pycryptodome` (for `Crypto`), `click`, `scrapy`, and `pywin32` (for `win32com`, used by `2020/bilibili/download.py`). The repository does not list these in a single file.

Some tools need external software:

- **FFmpeg** must be installed and on your `PATH` for the Bilibili downloader to merge multi-part videos. The Bilibili README links to http://ffmpeg.org/.
- **ChromeDriver** is required by the Selenium and Splinter scripts, such as `12306.py`, `geetest.py`, and `douyin_pro.py`.
- **MySQL** is required by `financical.py`.
- **Node.js** with the `node-schedule`, `socket.io`, and `line-reader` packages is required by `baiwan/app.js`. The supplied files do not include a `package.json`, so these packages must be installed manually.

## Usage

Each script is run directly from its folder. Examples follow the usage documented in the supplied files.

### Bilibili video and danmaku downloader (`bilibili/`)

Downloads videos and danmaku for search results. Requires FFmpeg.

```bash
cd bilibili
python bilibili.py -d 猫 -k 猫 -p 10
```

| Argument | Meaning |
| --- | --- |
| `-d` | Folder to save videos into |
| `-k` | Bilibili search keyword |
| `-p` | Number of search result pages to download |

Danmaku XML is converted to ASS with `xml2ass.py`, which the README says supports players such as PotPlayer.

### JD review photo downloader (`dingdong/`)

```bash
cd dingdong
python jd.py -k 芒果
```

| Argument | Meaning |
| --- | --- |
| `-d` | Save path (default: the script's folder) |
| `-k` | Search keyword |
| `-n` | Number of stores whose review photos are downloaded |

### Douyin video downloader (`douyin/`)

```bash
cd douyin
python douyin.py
```

The script prints a welcome banner and prompts for the user ID. It calls a third-party signature service (`http://49.233.200.77:5001` in `douyin/douyin.py`). The README notes that the service may be shut down and that `pyppeteer` could be used instead.

The root-level `douyin_pro.py` and `douyin.py` are older versions. `douyin_pro.py` uses Splinter with `D:/chromedriver` and a headless Chrome browser.

### NetEase Cloud Music downloader (`Netease/`)

Reads song names from `music_list.txt`, one per line, and searches for each one:

```bash
cd Netease
python Netease.py
```

Downloaded files go to a `Musics` folder. Cookies are stored in a file named `Cookie`. Each file is saved as `<number>_<song name>.mp3`.

### Zhengfang academic system scraper (`zhengfang_system_spider/`)

```bash
cd zhengfang_system_spider
pip install -r requirements.txt
python spider.py
```

The script asks for the school's academic-system URL (for example, `http://115.236.84.162`), student ID, and password. It downloads the CAPTCHA to `code.jpg`, opens it, and asks you to type the code. After login, it writes the timetable, grades, GPA, and English-exam results to `zhengfang.txt` in the same folder.

### Other scripts

- `12306.py`: Opens a Chrome browser with Splinter and automates a ticket search and booking flow. Run with `python 12306.py`.
- `baiduwenku_pro_1.py`: Prompts for a Baidu Wenku URL, then saves text output as a `.txt` file. For image-based documents, it saves page images into a folder named after the document ID.
- `biqukan.py`: Prompts for a novel's catalog URL and writes the chapters into a single text file.
- `hero.py`: Prints the hero list, asks for a hero ID, and displays equipment information. Images are saved to `hero_images/`.
- `financical.py`: Prompts for a stock code and stores the financial statements in MySQL.
- `video_downloader/video_downloader.py`: Launches a Tkinter GUI. Enter a video URL and choose a playback channel, or generate a QR code for mobile viewing. The QR code step expects the `Images/` folder to be present.
- `2020/api/api.py`: Sends an image to the Face++ beautify API. It uses `%matplotlib inline`, so it is intended for Jupyter.
- `bilibili_luckyman/bilibili_luckyman.py`: Fetches repost data from a hard-coded Bilibili dynamic URL and selects 30 random winners. A fixed random seed is used.

## Configuration

Many scripts are configured by editing constants in the source file. The repository has no configuration files except the `requirements.txt` files and `cartoon/scrapy.cfg`, which defines the Scrapy settings module and project name. Before running a script, check it for the following settings.

| Script | Settings to edit |
| --- | --- |
| `12306.py` | `username`, `passwd`, `starts`, `ends`, `dtime`, `order`, `users`, `xb`, `pz`, and `executable_path` (`D:/chromedriver`). Values are placeholders such as `xxx`. |
| `douyin_pro.py` | ChromeDriver path `D:/chromedriver`. |
| `geetest.py` | Target URL `self.url = '*'` and ChromeDriver path `D:\\chromedriver.exe`. |
| `baiduwenku.py` | ChromeDriver path (`J:\迅雷下载\chromedriver.exe`) and target document URL. |
| `financical.py` | MySQL connection: host `127.0.0.1`, port `3306`, user `root`, password `yourpasswd`, database `financialdata`. |
| `baiwan/baiwan.py` | The question API URL contains a placeholder (`xxxxxxx`). The code notes that the API is specific to each user and is not published. |
| `2020/bilibili/download.py` | Placeholder URL `jiexi_url = 'xxx'` and a space URL. It also depends on Windows-only `win32com` and Thunder (Xunlei) software. |
| `biqukan.py`, `one_hour_spider/biquge20180731.py` | Output paths. The second uses a hard-coded `G:/pythonlearn` path. |
| `Netease/Netease.py` | Timeout (60), output folder (`Musics`), cookie file (`Cookie`), and the list file `music_list.txt`. |
| `bilibili/bilibili.py` | Search keyword, output folder, and number of pages, via command-line arguments. |

Some scripts also contain hard-coded values such as request headers, API tokens, device parameters, and specific user or item IDs (for example, `user_id = 'sm666888'` in the root `douyin.py`). Replace these with your own values before use.

## Development

The repository is a collection of examples rather than an installable package. Most files are self-contained, have no shared module, and have no packaging metadata such as `setup.py` or `pyproject.toml`.

Suggested workflow:

1. Pick the folder for the site or technique you are working on. The `2020/` tutorial folders are the most structured examples.
2. Check the folder's `README.md`, if there is one, for usage and parameters.
3. Replace placeholder values and local paths in the script (see [Configuration](#configuration)).
4. Keep generated output (such as downloaded media, `zhengfang.txt`, and `__pycache__`) out of version control.

The `cartoon/` folder is a Scrapy project. The spider code is in `cartoon/spiders/comic_spider.py`, and the project settings are in `cartoon/settings.py`.

The `video_downloader/MyQR/` folder contains a vendored QR-code library. The `bilibili/xml2ass.py` file is a copy of the Danmaku2ASS tool, which the file header says is released under GPL version 3.

## Testing

The supplied file tree contains **no test files** and no test configuration, such as `pytest.ini`, `tox.ini`, or a `tests/` folder. There is no documented testing procedure. To check a script, run it manually with the arguments described in its README or source code.

## Contributing

The supplied files do not include a contributing guide, code of conduct, or issue template. The 2020 README invites readers to star the project and contact the author for feedback. Contact details are provided as links to a WeChat group, a WeChat official account, Bilibili, and other channels.

## Disclaimer

The `baiwan/baiwan.py` header states that the software is for learning and exchange only and must not be used for any commercial purpose. The `video_downloader` GUI displays the same message. Scripts that automate logins, bypass CAPTCHAs, or use third-party APIs may conflict with the terms of service of the sites they target. Review those terms before running any script.

## License

No license file appears in the supplied repository contents, and no license is stated in the supplied files. Check the repository for a `LICENSE` file before reusing or redistributing this code. The bundled `bilibili/xml2ass.py` file carries its own GPL version 3 notice in its header.

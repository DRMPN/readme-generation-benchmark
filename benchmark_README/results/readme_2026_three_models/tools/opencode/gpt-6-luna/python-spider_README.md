# Python Spider

A collection of Python web-scraping and automation examples. The repository contains standalone scripts and small, separate projects for retrieving and processing data from particular websites; it is not a single application or installable Python package.

## Contents

### Standalone scripts

| Path | What the code does |
| --- | --- |
| `downloader.py` | Downloads a URL entered at the prompt and displays a console progress bar. |
| `12306.py` | Browser automation example for searching and booking China Railway tickets. Account, route, date, passenger, and ChromeDriver settings are hard-coded placeholders or values in the script. |
| `baiduwenku.py`, `baiduwenku_pro_1.py` | Examples for extracting text or page images from Baidu Wenku documents. |
| `biqukan.py` | Retrieves novel chapters and writes them to a text file. |
| `daili.py` | Scrapes a proxy list and pings candidate proxy IP addresses. |
| `douyin.py`, `douyin_pro.py` | Examples for retrieving and downloading videos associated with a Douyin user. The latter uses Chrome through Splinter. |
| `financical.py` | Attempts to retrieve financial statements from NetEase Quotes and write them to MySQL. Database settings are embedded in the code. |
| `geetest.py` | Slider-captcha image-analysis example with browser interaction code. The slider-drag step is commented out; the script also contains a placeholder URL and a hard-coded ChromeDriver path. |
| `hero.py` | Queries 王者荣耀 (Honor of Kings) hero and equipment information and can download hero images. |
| `shuaia.py` | Scrapes image links from shuaia.net and saves images in an `images` directory. |

### Directories

| Path | Contents |
| --- | --- |
| [`2020/`](2020/README.md) | Code accompanying a 2020 Python 3 web-scraping tutorial series: novel and comic downloads, video downloading, a face-beautification API example, Taobao browser automation, and Bilibili video/danmaku code. The folder README links to the tutorial articles. |
| `baiwan/` | A “百万英雄” quiz-answering example, with related HTML, JavaScript, and text files. |
| [`bilibili/`](bilibili/README.md) | Bilibili video search/download and XML danmaku-to-ASS conversion. Its README describes the command-line options and notes the FFmpeg requirement for merging segmented video. |
| [`bilibili_luckyman/`](bilibili_luckyman/README.md) | A Bilibili dynamic-forwarding giveaway picker. |
| `cartoon/` | A Scrapy project whose `comic` spider collects comic chapter image URLs and whose pipeline downloads them. The image destination is configured in `cartoon/cartoon/settings.py`. |
| [`dingdong/`](dingdong/README.md) | A JD.com product-review image downloader. The README documents its command-line options. |
| [`douyin/`](douyin/README.md) | Another Douyin user-video downloader example, separate from the root-level scripts. |
| `Netease/` | A NetEase Cloud Music script using request encryption and AES. |
| `one_hour_spider/` | Older examples for Unsplash photos, novels, and video downloading. |
| `video_downloader/` | A Tkinter video-link utility, bundled MyQR QR-code code, and image assets. Its dependencies are listed in `video_downloader/requirements.txt`. |
| [`zhengfang_system_spider/`](zhengfang_system_spider/README.md) | A script for retrieving a personal timetable and grades from a ZhengFang academic-management system. Its README gives setup and run instructions. |

## Running examples

There is no repository-wide entry point or root dependency file. Choose a script or subproject, read its comments and any directory-level README, then run it from the directory expected by that code. For example, the ZhengFang README instructs:

```bash
cd zhengfang_system_spider
pip install -r requirements.txt
python spider.py
```

The Bilibili project documents this invocation (run from `bilibili/`):

```bash
python bilibili.py -d <download-directory> -k <search-keyword> -p <number-of-pages>
```

Dependencies are specific to each example. The repository includes requirements files for `video_downloader/` and `zhengfang_system_spider/`; they do not cover every script. Some examples also expect external programs, browser drivers, API credentials, database configuration, or paths to be edited in the source before use.

## Maintenance and compatibility

These are historical, website-specific examples, not a maintained crawler framework. Many scripts rely on particular page layouts, endpoints, or browser behavior, which may have changed since the examples were written. Check and adapt a script before running it. Follow the relevant websites’ terms, applicable laws, and privacy requirements, and use the examples only for content you are authorized to access.

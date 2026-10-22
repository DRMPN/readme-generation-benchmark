# Python Spider

A collection of Python web crawler and scraper examples, originally created by **Jack Cui** as learning material for his Python web crawling tutorial series. Each directory or script targets a specific website, platform, or task, and most of them are accompanied by a corresponding tutorial article.

> **Note:** These projects are intended for **learning and educational purposes only**. Many of the examples were written years ago, and the target sites, APIs, and anti-crawler mechanisms have changed over time — a large portion of the examples are likely no longer functional without modification.

## Project Structure

The repository is organized as a set of independent mini-projects:

| Path | Description |
| :--- | :--- |
| `2020/` | The 2020 rewritten tutorial series (novel downloader, comic downloader, video downloader, API, Taobao, Bilibili danmaku). |
| `baiwan/` | Question-answer assistant for the "百万英雄" (Million Heroes) live quiz app; fetches questions from the app API and searches Baidu Zhidao for answers. |
| `baiduwenku.py` | Baidu Wenku document downloader using Selenium. |
| `baiduwenku_pro_1.py` | An improved version of the Baidu Wenku downloader. |
| `bilibili/` | Bilibili video and danmaku (bullet comment) downloader; converts XML danmaku to ASS subtitle files. Requires FFmpeg for merging segmented videos. |
| `bilibili_luckyman/` | Helper script for Bilibili forwarding/lottery events. |
| `biqukan.py` | Novel downloader for `biqukan.com`. |
| `cartoon/` | A Scrapy-based comic spider project. |
| `daili.py` | Proxy IP collector (scrapes high-anonymity proxies from `xicidaili.com`). |
| `dingdong/` | JD.com (京东) product review image downloader. Usage: `python jd.py -k 芒果`. |
| `douyin.py` / `douyin_pro.py` | Douyin (抖音) video downloader. |
| `douyin/` | Douyin-related auxiliary assets (e.g., `fuck-byted-acrawler.js`). |
| `downloader.py` | Generic file downloader with a progress bar class. |
| `financical.py` | Financial data scraper for `quotes.money.163.com` (HK stock data); stores results in a MySQL database via `pymysql`. |
| `geetest.py` | Geetest sliding captcha cracker. |
| `hero.py` | Downloads League of Legends hero images from the "英雄联盟盒子" (LoL Box) API. |
| `Netease/` | NetEase Cloud Music downloader, including AES/RSA request encryption logic. |
| `one_hour_spider/` | Quick standalone examples: Biquge/Unsplash/Biqukan scrapers and a simple video downloader. |
| `shuaia.py` | Image downloader for `shuaia.net`. |
| `video_downloader/` | A Tkinter GUI application for downloading videos from sites like iQiyi and Youku, with built-in QR code generation (via the bundled `MyQR` module). |
| `zhengfang_system_spider/` | Crawler for the Zhengfang (正方) academic management system — fetches personal class schedule, grades, and GPA. Usage: `python spider.py`. |
| `12306.py` | 12306 train ticket purchase script using Splinter (browser automation). |

## Requirements

- **Python 3** is required across the board.
- Commonly used libraries include: `requests`, `beautifulsoup4`, `lxml`, `Pillow`, `numpy`, `imageio`, `selenium`, `scrapy`, `pymysql`, `Crypto` (pycryptodome / pycryptodome equivalents), `click`, `splinter`, and `tkinter` (usually bundled with Python).
- Individual sub-projects have their own `requirements.txt` where applicable. For example:

```bash
# For the zhengfang_system_spider sub-project
pip install -r zhengfang_system_spider/requirements.txt

# For the video_downloader sub-project
pip install -r video_downloader/requirements.txt
```

Since each mini-project is independent, you should check for a `requirements.txt` or inspect the imports at the top of a specific script to determine its dependencies.

## Usage

Each project is designed to be run independently from within its own directory. For example:

```bash
# Download Bilibili videos with danmaku
cd bilibili
python bilibili.py -d 猫 -k 猫 -p 10

# Download JD.com review images
cd dingdong
python jd.py -k 芒果

# Scrape the Zhengfang academic system
cd zhengfang_system_spider
python spider.py
```

Note that many scripts rely on hardcoded URLs, API endpoints, or Selenium WebDriver paths (e.g., `chromedriver.exe` paths in `baiduwenku.py` and `12306.py`), which may need to be updated to run correctly today.

## Disclaimer

This repository is shared for educational purposes related to learning web crawling technology. Please respect the target websites' `robots.txt`, terms of service, and applicable laws. Do not use these scripts for any commercial or malicious purposes.

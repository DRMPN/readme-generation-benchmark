# README

## Introduction

**python-spider-wx1ybi1y** is a collection of Python-based web scraping, automation, and download tools. This repository gathers a variety of independent scripts and mini-projects — from video downloaders and login automations to spider frameworks, captcha handling, and utility scripts. Each script is self-contained and solves a specific task.

## Repository Structure

### 🕷️ Spiders & Scrapers

| File | Description |
|------|-------------|
| `biqukan.py` | Spider for scraping novel content from biqukan.com |
| `biquge20180731.py` | Novel scraper for biquge book sites |
| `xbqg_spider.py` | Novel site spider (笔趣阁 variant) |
| `comic_spider.py` | Comic/image scraping tool (with `items.py` for Scrapy item definitions) |
| `spider.py` | General-purpose spider for educational system (正方教务系统), paired with `zhengfang.txt` |
| `12306.py` | 12306 train ticket query/spider script |
| `financical.py` | Financial data scraper |
| `Netease.py` | NetEase music spider (with `music_list.txt` playlist input) |
| `jd.py` | JD.com (京东) related spider/automation |
| `baiwan.py` | "百万英雄" quiz answer assistant (with `question.txt` for OCR'd questions) |
| `api.py` | Helper API utilities for the quiz assistant |
| `app.js` | Companion Node.js script for the quiz tool |
| `index.html` | Front-end page used by the quiz assistant |

### 🎬 Video & Media Downloaders

| File | Description |
|------|-------------|
| `douyin.py` | Douyin (抖音) video downloader |
| `douyin_pro.py` | Enhanced Douyin downloader (paired with `fuck-byted-acrawler.js` for signature cracking) |
| `bilibili_luckyman.py` | Bilibili lottery/lucky-user picker |
| `bilibili.py` | Bilibili video downloader |
| `video_download.py` | Generic video download tool |
| `video_downloader.py` | Alternative video downloader |
| `vidoe_downloader.py` | Another video download variant |
| `xml2ass.py` | Converts Bilibili danmaku XML files to ASS subtitle format |
| `downloader.py` | Simple file download utility |

### 📷 QRCodes & Utilities

| File | Description |
|------|-------------|
| `myqr.py` | MyQR — generate artistic/animated QR codes |
| `theqrmodule/` | Supporting module for MyQR (`__init__.py`, `data.py`, `matrix.py`, `structure.py`, `constant.py`, `draw.py`, `ECC.py`, `terminal.py`) |
| `unsplash.py` | Unsplash image downloader |
| `unsplash20180731.py` | Updated Unsplash crawler |
| `baiduwenku.py` | Baidu Wenku document downloader |
| `baiduwenku_pro_1.py` | Improved Baidu Wenku downloader |
| `geetest.py` | Geetest (极验) sliding captcha analysis/bypass helper |
| `daili.py` | Proxy (代理) pool/IP checking utility |
| `shuaia.py` | 刷票 / voting automation script |
| `zf.py`-related assets | `code.jpg`, `zf.png` — captcha samples used by the educational-system spider |

### 📦 Scrapy Project

- `scrapy.cfg` — Scrapy configuration
- `__init__.py`, `pipelines.py`, `middlewares.py`, `settings.py` — Scrapy project scaffolding for the comic spider

### 🖼️ Assets

- `1.png`, `test_1.png`, `spider.png`, `qrcode.png`, `bg.png`, `gzh-1.jpg` — images/docs
- `README.md` files — per-subproject documentation
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.x
- Install dependencies:

```bash
pip install -r requirements.txt
```

Commonly used libraries include: `requests`, `scrapy`, `selenium`, `Pillow`, `qrcode`, `imageio`, `moviepy`, `BeautifulSoup4`.

Some scripts (e.g., Douyin Pro) additionally require **Node.js** to run the bundled JavaScript (`app.js`, `fuck-byted-acrawler.js`) for signature generation.

## Usage

Each script is standalone. Run it directly, e.g.:

```bash
python biqukan.py          # scrape a novel
python douyin_pro.py       # download Douyin videos
python myqr.py             # generate QR codes
python xml2ass.py          # convert danmaku XML to ASS
```

Refer to the per-folder `README.md` files for detailed usage of individual sub-projects.

## Disclaimer

⚠️ **This project is for educational purposes only.** All scripts are provided for learning web-scraping techniques. Please respect the target websites' terms of service, robots.txt, and applicable laws. The author is not responsible for any misuse.

## License

For personal learning and research use.

# Python Spider — A Collection of Python Web Crawler Examples

A curated collection of practical Python 3 web spider (crawler) examples and tutorials, covering everything from simple static-page scraping to browser automation, app API reverse engineering, and multimedia downloading. The repository accompanies a series of published crawler tutorial articles (the `2020/` directory contains the 2020 rewrite of the tutorial series, with each example linked to its corresponding article).

> **Note from the author (2020/README.md):** Many of the older examples have become ineffective over time as target websites changed. The 2020 series was rewritten with updated examples, and new articles are published regularly on the author's public channels (WeChat public account, Bilibili, Zhihu, CSDN, etc.).

---

## Project Structure

### Top-level standalone scripts

| File | Description |
|---|---|
| `biqukan.py` | Novel downloader for the 笔趣看 (biqukan.com) site. Parses the table of contents, downloads every chapter, and writes the result to a single `.txt` file with a live progress percentage. |
| `baiduwenku.py` | Selenium-based scraper for Baidu Wenku documents. Uses a mobile user agent with headless Chrome, extracts the title, page count, and text content of a document. |
| `baiduwenku_pro_1.py` | A `requests`-based version that detects the document type (`doc`, `txt`, or other formats such as `ppt`) via the Wenku API, downloads text (or page images for non-text types), and saves the output as a `.txt` file or a folder of `.jpg` images. |
| `daili.py` | High-anonymity proxy IP harvester. Scrapes proxies from 西祠代理 (xicidaili.com), then verifies each candidate by pinging it and selecting a proxy with an average response time under 200 ms. |
| `douyin.py` | Douyin (TikTok China) app video downloader. Searches a user by ID via the Douyin API, lists all of their videos, and downloads each one with a progress display. |
| `douyin_pro.py` | A headless-Chrome (splinter-based) variant of the Douyin downloader. |
| `12306.py` | 12306 train-ticket booking assistant built on splinter + ChromeDriver. Fills in the username/password, waits for the user to enter the captcha manually, then repeatedly clicks "查询" until tickets can be ordered, selects the passenger, seat class, and seat, and submits the order. Station codes, date, train index, passengers, seat class, and ticket type are configured at the top of the file. |
| `financical.py`, `hero.py`, `shuaia.py`, `downloader.py` | Additional example crawlers included in the repository. |

### Directory-based projects

| Directory | Description |
|---|---|
| `2020/` | The 2020 tutorial series code: `xbqg/` (novel download), `dmzj/` (comic download with dynamic loading / anti-crawler handling), `zycjw/` (video download), `api/` (Face++ beautify API demo — whitening, smoothing, thin-face parameters, base64 image in/out), `taobao/` (Taobao automated login), `bilibili/` (B站 video + danmaku download, XML→ASS conversion, automatic Thunder download tasks and video renaming). |
| `bilibili/` | Downloads B站 videos and danmaku (bullet comments) and converts native XML danmaku to `.ass` subtitle files playable in PotPlayer and similar players. Supports FFmpeg-based merging of segmented videos. |
| `bilibili_luckyman/` | A B站 repost/forward lottery assistant, written for the author's 300,000-follower giveaway. |
| `dingdong/` | Downloads user review ("晒单") images for JD.com products. |
| `zhengfang_system_spider/` | Scrapes the 正方 (ZhengFang) educational administration system: personal class timetable, full academic history with credits/GPA computation, and standardized-test (e.g., CET-4/6) scores. Results are written to `zhengfang.txt`. Login handles the `__VIEWSTATE` token and displays the CAPTCHA (`code.jpg`) for manual entry. |
| `video_downloader/` | GUI video downloader with QR-code generation (bundled `MyQR` library). Dependencies: `imageio`, `numpy`, `Pillow`, `beautifulsoup4` (see `video_downloader/requirements.txt`). |
| `one_hour_spider/` | "One-hour spider" tutorial examples: biquge/biqukan novel crawlers, Unsplash image crawler, and a video downloader. |
| `cartoon/` | A Scrapy project (`scrapy.cfg`, items/middlewares/pipelines/spiders) for downloading comics. |
| `Netease/` | NetEase Cloud Music related script with `music_list.txt`. |
| `baiwan/` | 百万英雄 (live quiz) assistant: `baiwan.py`, `app.js`, question history (`question.txt`). |

---

## Environment & Setup

### Requirements

- **Python 3** (the `zhengfang_system_spider` README explicitly targets Python 3.6)
- Common libraries used across the project: `requests`, `beautifulsoup4` (bs4), `lxml`, `Pillow`, `selenium`, `splinter` + ChromeDriver, `scrapy`, `numpy`, `imageio`, `pypinyin`-style utility modules where noted, and Windows-only extras such as `pywin32` (used by the Thunder COM automation in `2020/bilibili/download.py`).

### Installation

1. Clone the repository:

```bash
git clone git@github.com:Jack-Cherish/python-spider.git
```

2. Some sub-projects ship their own `requirements.txt`. Install per project, for example:

```bash
cd zhengfang_system_spider
pip install -r requirements.txt        # lxml, requests, Pillow, beautifulsoup4
```

```bash
cd video_downloader
pip install -r requirements.txt        # imageio, numpy, Pillow, beautifulsoup4
```

3. For browser-automation scripts (`12306.py`, `baiduwenku.py`, `douyin_pro.py`), install **FFmpeg** where required (see `bilibili/README.md`) and configure its path in the environment variables. Also download **ChromeDriver** and set the `executable_path` inside the script (e.g., `D:/chromedriver`).

---

## Usage

Each script is run independently. Representative examples drawn from the code and sub-READMEs:

**B站 video + danmaku downloader** (`bilibili/`):

```bash
python bilibili.py -d 猫 -k 猫 -p 10
```

- `-d` — folder name to save videos
- `-k` — keyword to search on B站
- `-p` — how many pages of search results to download

**JD review-image downloader** (`dingdong/`):

```bash
python jd.py -k 芒果
```

- `-d` — save path (defaults to the script's folder)
- `-k` — search keyword
- `-n` — number of shops' review images to download

**ZhengFang academic system spider** (`zhengfang_system_spider/`):

```bash
cd zhengfang_system_spider
python spider.py
```

Follow the interactive prompts to enter your school's educational-administration URL, student ID, password, and CAPTCHA. The timetable, historical grades, computed average GPA / total credit GPA / total credits, and standardized-test results are saved to `zhengfang.txt`.

**笔趣看 novel downloader** (`biqukan.py`):

```bash
python biqukan.py
```

Paste the novel's table-of-contents URL when prompted. The downloader removes any existing output file, then writes chapters one by one while printing download progress.

**Baidu Wenku downloader** (`baiduwenku_pro_1.py`):

```bash
python baiduwenku_pro_1.py
```

Enter the Wenku document URL. Text documents (`doc`/`txt`) are parsed and saved as `<title>.txt`; other types (e.g., PPT) are downloaded as numbered `.jpg` page images in a folder named after the document ID.

**Douyin video downloader** (`douyin.py`):

```bash
python douyin.py
```

Set the target `user_id` in the script's `run()` method; videos are saved into a folder named after the user's nickname. The `douyin/` variant relies on an external signature service (see `douyin/README.md`); alternatively `pyppeteer` can be used to obtain signatures via browser emulation.

**12306 ticket assistant** (`12306.py`):

Edit the class attributes at the top of `12306.py` (username, password, from/to station codes, departure date, train order, passenger names, seat class `xb`, ticket type `pz`), then:

```bash
python 12306.py
```

The script opens Chrome via splinter, fills in credentials, waits for you to solve the CAPTCHA, and then loops the ticket query until booking becomes possible.

**Face++ beautify demo** (`2020/api/api.py`): fill in your Face++ `AK`/`SK`, adjust the whitening/smoothing/thin-face parameters, and run it to compare the original and processed images side by side with matplotlib.

**B站 2020 downloader** (`2020/bilibili/download.py`): fetches a UP主's full video list via the B站 space API, sends download tasks to Thunder (Xunlei) via COM automation, downloads each video's danmaku XML, converts it to `.ass` with `xml2ass`, and renames downloaded files to their video titles.

---

## Configuration

- **Hard-coded parameters:** Several legacy scripts keep their settings as module-level constants or class attributes (e.g., `12306.py` station/date/passenger config, `douyin.py` user ID, ChromeDriver paths such as `D:/chromedriver`). Edit these values in the source before running.
- **API keys:** `2020/api/api.py` requires your own Face++ API Key and API Secret.
- **External services:** The `douyin/` project depends on a third-party signature service; the `2020/bilibili/` video-resolution URL is obtained via the author's channel (see the comment in `download.py`).
- **Proxy behavior:** `daili.py` filters harvested proxies by ping latency (threshold 200 ms) automatically — no manual configuration needed.

---

## Development

- Each example is a self-contained script or project; add new crawlers by following the existing structure (a `requests`/`BeautifulSoup` core, or `selenium`/`splinter` for JS-heavy sites, or a Scrapy project as in `cartoon/`).
- The bundled `MyQR` library inside `video_downloader/` implements QR-code generation from scratch (`myqr.py`, `terminal.py`, and supporting `mylibs/` modules).
- `xml2ass.py` (in both `bilibili/` and `2020/bilibili/`) is derived from **Danmaku2ASS** by StarBrilliant and auto-detects comment formats from Niconico, Acfun, Bilibili, Tudou, MioMio, and sH5V before converting them to ASS subtitle dialogues.
- Note that many examples were written years ago against specific site layouts and APIs; expect to update selectors, endpoints, and headers when adapting them.

---

## Testing

The repository does not include an automated test suite. Verification is done by running each script against its target site and inspecting the output artifacts (e.g., `zhengfang.txt` for the academic spider, downloaded `.mp4`/`.ass` files for the B站 downloader, generated novel `.txt` files, and the screenshots in `zhengfang_system_spider/screenshot/`).

---

## License

No repository-wide `LICENSE` file is present in this snapshot. The bundled `xml2ass.py` (Danmaku2ASS) is explicitly released under the **GNU General Public License version 3** (see its header). All other example code is provided for educational purposes as part of the author's crawler tutorial series — please respect the target websites' terms of service and use the code responsibly.

# Python Spider

A collection of standalone Python web-scraping and automation examples, organized around practical projects and tutorials. The repository includes scripts for downloading videos, danmaku, novels, images, music, and product photos, as well as examples that query APIs or extract information from websites.

This is a collection, not a single installable application: projects have separate dependencies, entry points, and configuration, and there is no shared command-line interface. Many examples depend on remote websites and services that may have changed since the code was written. The 2020 tutorial README explicitly notes that some older examples no longer work and describes plans to refresh them. Treat each script as a historical learning example and check its source and any project-specific README before running it.

## Projects at a glance

| Path | What the supplied files describe |
| --- | --- |
| `bilibili/` | Search Bilibili videos, download video segments and XML danmaku, and convert danmaku to ASS subtitles. |
| `2020/` | Newer tutorial examples, including novel, manga, video, API, Taobao, and Bilibili-related code. See [`2020/README.md`](2020/README.md) for the article and code index. |
| `douyin/` | Download videos associated with a Douyin user, including uploaded or favorited videos in the interactive version. |
| `dingdong/` | Search JD products and download customer review images. |
| `zhengfang_system_spider/` | Retrieve a personal timetable, grades, and grade-test results from a ZhengFang academic system. |
| `Netease/` | Search for songs listed in `music_list.txt` and download available results. |
| `cartoon/` | Scrapy project structure with a comic spider, settings, items, middleware, and pipeline files. |
| `video_downloader/` | Tkinter interface for opening video links through configured third-party playback services, with QR-code generation. |
| Root-level scripts and `one_hour_spider/` | Additional independent experiments, including document, novel, image, proxy, finance, and video examples. |

The folders `bilibili_luckyman/` and `baiwan/` contain separate examples for a Bilibili repost giveaway helper and a question-answering display workflow, respectively. Their own READMEs or source files provide the available context.

## Setup

Use a separate environment for each example where practical. The repository does not provide a root-level `requirements.txt`, package metadata, or a unified installation command. Dependencies therefore vary by script.

For the video downloader and ZhengFang spider, install the dependencies listed in their respective directories:

```bash
python -m venv .venv
# Activate the environment using the command for your shell.
python -m pip install -r video_downloader/requirements.txt
```

```bash
python -m pip install -r zhengfang_system_spider/requirements.txt
```

The `video_downloader/requirements.txt` file lists `imageio`, `numpy`, `Pillow`, and `beautifulsoup4`. The ZhengFang requirements pin `lxml`, `requests`, and `beautifulsoup4`, and specify a minimum Pillow version. Its README names Python 3.6 as the dependency environment.

Other scripts import libraries such as `requests`, `beautifulsoup4`, `lxml`, `selenium`, `splinter`, `pymysql`, `Crypto`, `click`, `Scrapy`, OpenCV, and Matplotlib. These are not covered by a single project-wide dependency file. Install only the dependencies required by the example you intend to use, and consult its imports and any local requirements file.

Some programs also need software or services beyond Python packages. The Bilibili README requires FFmpeg on the system path to merge segmented downloads. The 12306 example expects ChromeDriver at a Windows-specific path. Browser-driven scripts require a compatible browser and driver. `2020/bilibili/download.py` imports Windows’ `win32com` integration and calls the Thunder client. The Face++ example requires API credentials. These requirements are specific to those scripts, not to the repository as a whole.

## Usage

Run an example from its own directory when it reads or writes files using relative paths. For instance, the ZhengFang spider’s documented workflow is:

```bash
cd zhengfang_system_spider
python spider.py
```

It prompts for the school’s academic-system URL, student number, password, and verification code. The source saves a captcha image as `code.jpg`; after a successful login, timetable and result data are written to `zhengfang.txt`.

The Bilibili downloader accepts a destination directory, search keyword, and number of search pages:

```bash
cd bilibili
python bilibili.py -d downloads -k 猫 -p 10
```

This usage is also shown in `bilibili/README.md`. The script downloads matching videos and danmaku and invokes `xml2ass.py` to create ASS subtitles. FFmpeg is needed for merging segmented video files.

The JD晒单-image example takes a keyword and optional output directory and product count:

```bash
cd dingdong
python jd.py -k 芒果 -n 1
```

Its CLI also accepts `-d` for the output path. See `dingdong/README.md` for the documented options.

The Douyin project’s interactive script can be started with:

```bash
cd douyin
python douyin.py
```

It prompts for a user ID, whether to download watermarked video, whether to fetch favorites or uploads, and a save path. The separate root-level `douyin.py` has different behavior and uses a fixed user ID in its `run()` method; do not assume it has the same prompts or options.

The Netease example is run from its directory:

```bash
cd Netease
python Netease.py
```

It reads song names from `music_list.txt` and saves downloaded files under `Musics`, as configured in the script. Not every script has a documented command-line interface; inspect its `if __name__ == "__main__":` block before running it.

## Configuration

Most examples are configured directly in Python source rather than through a shared settings file. Review and change values such as URLs, user IDs, search terms, output directories, page counts, and browser-driver paths before execution.

Several scripts contain placeholders or environment-specific values. For example, `12306.py` includes placeholder account and passenger values and a Windows ChromeDriver path. `2020/api/api.py` leaves the Face++ API key and secret empty. `2020/bilibili/download.py` contains a placeholder parsing-service URL. The root `financical.py` includes a local MySQL connection configuration and references a `code` variable in its database method. Do not expect these examples to run unchanged.

The ZhengFang spider prompts for account information at runtime. Its output includes personal academic data, so handle generated files such as `zhengfang.txt` and captcha images accordingly. For any example that accesses a third-party service, check its current availability and the site’s requirements before use.

## Development and testing

There is no repository-wide test suite or common development workflow shown in the supplied files. No root-level test configuration is present in the listed tree. The examples are independent, so changes should be tested within the relevant project rather than by assuming that the whole repository has one build or test command.

A useful first check for a Python file is to compile it without running network or browser actions:

```bash
python -m py_compile path/to/script.py
```

This checks syntax only; it does not verify compatibility with current websites, API responses, credentials, browser drivers, or installed dependencies. For behavior changes, test with a small, permitted request and a temporary output directory where possible. Check generated files and logs, and avoid running scripts that submit orders or perform other consequential actions unless you have reviewed their behavior.

For the 2020 tutorial series, [`2020/README.md`](2020/README.md) links several articles to their corresponding code folders. The local READMEs in `bilibili/`, `douyin/`, `dingdong/`, and `zhengfang_system_spider/` provide additional project-specific notes.

## License

No repository-wide license is identified in the supplied files. Do not assume that every project in this collection has the same license. The `xml2ass.py` files state that the Danmaku2ASS program is released under the GNU General Public License version 3 and include a no-warranty notice. Check individual source files and third-party components for their terms before reuse or redistribution.

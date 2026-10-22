# SMSBoom - 短信测压工具

> ⚠️ **重要声明**：本项目原设计用途为对**自己的手机号**进行短信接口压力测试。使用本工具对他人手机号进行轰炸属于违法行为，请务必遵守当地法律法规，仅用于合法的安全测试和学习研究。

## 项目简介

SMSBoom 是一个基于 Python 的短信测压/短信轰炸工具。它通过加载大量第三方网站的短信验证码发送接口（`api.json` 和 `GETAPI.json`），向指定手机号并发发送大量验证码请求。

主要特性：

- **多线程请求**：基于 `ThreadPoolExecutor` 的线程池并发请求，默认 64 线程
- **异步并发**：基于 `asyncio` + `httpx.AsyncClient` 的真异步请求模式，支持高并发极限测压
- **单线程模式**：用于测试接口可用性
- **代理支持**：可加载 HTTP / SOCKS4 / SOCKS5 代理列表，避免本机 IP 被封
- **多手机号支持**：可通过 `-p` 参数多次传入多个手机号
- **接口自动更新**：可从 GitHub 拉取最新的接口配置文件
- **GUI 界面**：提供一个基于 Tkinter 的简单图形界面（`smsboom_GUI.py`）
- **接口爬取工具**：`debug/` 目录下提供爬虫脚本，可从在线轰炸平台爬取并校验接口

## 项目结构

```
├── smsboom.py            # 主程序（命令行入口）
├── smsboom_GUI.py        # Tkinter 图形界面（简化版）
├── api.json              # POST 接口列表
├── GETAPI.json           # GET 接口列表
├── Dockerfile            # Docker 构建文件
├── requirements.txt      # Python 依赖
├── utils/
│   ├── __init__.py       # 随机 User-Agent 列表
│   ├── log.py            # loguru 日志配置
│   ├── models.py         # API Pydantic 模型
│   ├── req.py            # 请求逻辑（同步/异步/代理）
│   └── sql.py            # SQLite 数据库读写（爬虫用）
├── debug/
│   ├── api.js            # 第三方网站短信接口（JS 版）
│   ├── api_tou.json      # 转换后的接口数据
│   ├── hz-web.json       # 在线轰炸平台网址列表
│   ├── spider-api.py     # 接口爬虫脚本
│   ├── tou_api.py        # touapi.json 转换脚本
│   └── touapi.json       # 原始接口数据
└── .github/workflows/run.yaml  # GitHub Actions 工作流
```

## 环境要求

- Python 3.x（GitHub Actions 工作流中使用 Python 3.8）
- 依赖：`httpx`、`click`、`loguru`、`pydantic`、`requests`、`prettytable`、`tqdm` 等（见 `requirements.txt`）

## 安装

### 方式一：源码运行

```bash
git clone <仓库地址>
cd SMSBoom
pip3 install -r requirements.txt
```

### 方式二：Docker

项目附带 `Dockerfile`，使用 Pipenv 管理依赖：

```bash
docker build -t smsboom .
docker run --rm smsboom run -p 13800138000 -t 64
```

Docker 镜像的默认入口命令为 `pipenv run python smsboom.py`，可以在 `docker run` 时追加子命令和参数。

## 使用方法

主程序 `smsboom.py` 基于 Click 实现命令行组，包含以下子命令：

### run - 多线程轰炸

```bash
python3 smsboom.py run -p 13800138000 -t 64 -f 1 -i 60
```

参数说明：

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `--thread` | `-t` | 线程数 | 64 |
| `--phone` | `-p` | 手机号，可多次 `-p` 传入多个 | 无（不传则交互输入） |
| `--frequency` | `-f` | 执行次数（波数） | 1 |
| `--interval` | `-i` | 每波之间的间隔秒数 | 60 |
| `--enable_proxy` | `-e` | 开启代理（需先准备代理文件） | 关闭 |

示例 - 多手机号、多波次：

```bash
python3 smsboom.py run -p 13800138000 -p 13900139000 -t 32 -f 3 -i 30
```

若不通过 `-p` 传入手机号，程序会交互式提示输入。手机号必须为纯数字，否则程序退出。

### asyncRun - 异步极速模式

以真异步方式请求全部接口（理论上可达成百万级并发）：

```bash
python3 smsboom.py asyncRun -p 13800138000
```

### oneRun - 单线程测试

单线程逐个请求所有接口，适合测试接口可用性：

```bash
python3 smsboom.py oneRun -p 13800138000
```

### update - 更新接口

从 GitHub（`OpenEthan/SMSBoom` 仓库的镜像地址）拉取最新的 `api.json` 和 `GETAPI.json`：

```bash
python3 smsboom.py update
```

## 配置

### 接口文件

- **`api.json`**：POST/GET 结构化接口列表，每个条目包含 `desc`（描述）、`url`、`method`、`header`、`data` 字段。`data` 中使用 `[phone]` 占位符，部分接口还支持 `[timestamp]` 占位符（自动替换为当前时间戳）。
- **`GETAPI.json`**：纯 GET URL 接口列表，URL 中使用 `[phone]` 占位符。

程序启动时若接口文件缺失或 JSON 语法错误，会记录错误日志并提示使用 `update` 命令重新下载。

### 代理配置

开启 `-e` 前需在脚本同目录准备以下任一文件（不存在时程序会自动创建空文件）：

- `http_proxy.txt` — 每行一个 HTTP 代理
- `socks5_proxy.txt` — 每行一个 SOCKS5 代理
- `socks4_proxy.txt` — 每行一个 SOCKS4 代理

开启代理后，每一波轰炸会对每个代理执行一轮全接口请求。若代理列表为空却开启了 `-e`，程序会报错退出。

### 日志

日志基于 `loguru`，输出格式包含时间、级别、线程名、模块与行号。程序运行时会自动在工作目录下创建 `logs/` 目录（文件日志输出默认处于注释状态）。

## 图形界面

`smsboom_GUI.py` 提供一个极简的 Tkinter 窗口，包含手机号输入框和"启动轰炸"按钮：

```bash
python3 smsboom_GUI.py
```

## 开发（debug 目录）

`debug/` 目录包含接口维护相关的开发工具：

- **`spider-api.py`**：接口爬虫。基于 `hz-web.json` 中的在线测压平台网址，抓取页面上的接口图片链接，经过三重校验（包含默认手机号、去除空白字符、URL 格式合法）后放入队列，再由 254 个线程逐一验证接口可用性（返回 200 视为有效），结果存入 SQLite 数据库（`debug/api.db`，表 `API200`）。包含三个子命令：
  - `spider_all` — 根据 `hz-web.json` 爬取全部网站（会先校验网站有效性并支持写回文件）
  - `spider_one` — 爬取单个指定网址（`--url`、`--key` 参数）
  - `save_api` — 将数据库中的接口保存到 `GETAPI.json`
- **`tou_api.py`**：读取 `touapi.json`（数组格式的原始接口数据），转换为标准 API JSON 并写入 `api_tou.json`。
- **`api.js`**：以 JavaScript/jQuery 形式记录的第三方网站短信接口合集，可用于浏览器环境调试。

## 测试

项目没有独立的自动化测试套件。可以借助以下方式验证功能：

- 使用 `oneRun` 子命令单线程遍历接口，观察日志中每个接口的响应：
  ```bash
  python3 smsboom.py oneRun -p <你的手机号>
  ```
- 单独运行日志模块验证输出格式：
  ```bash
  python3 -m utils.log
  ```

## CI/CD

`.github/workflows/run.yaml` 定义了一个 GitHub Actions 工作流（`workflow_dispatch` 手动触发）：

1. 签出代码
2. 配置 Python 3.8 环境
3. 安装 `requirements.txt` 并执行：
   ```bash
   python3 smsboom.py run -p ${{ secrets.NUMBER }} -t 32
   ```

手机号通过仓库 Secret `NUMBER` 配置。文件中的定时触发（`schedule`）配置目前处于注释状态，如需定时运行可自行启用并修改 cron 表达式。

## 免责声明

- 本工具仅供学习交流与安全研究，请勿用于任何违法用途。
- 对他人手机号进行短信轰炸可能违反《中华人民共和国刑法》《治安管理处罚法》等相关法律。
- 使用本项目产生的一切后果由使用者自行承担。

## 许可证

本项目基于 **Apache License 2.0** 许可证开源，版权所有 © 2022 WhaleFall。详情请参阅项目根目录下的 `LICENSE` 文件。

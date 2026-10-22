# Kirara AI

一个用于构建 AI Agent 的框架。Kirara AI 提供了即时通讯（IM）接入、大语言模型（LLM）后端管理、工作流引擎、消息分发规则、记忆系统、MCP 集成、媒体管理以及带 Web 管理界面的完整运行时，可通过插件灵活扩展。

- 版本：`3.3.0a2`
- 作者：Lss233
- 许可证：AGPL-3.0-only
- 文档：https://kirara-docs.app.lss233.com
- 项目主页：https://github.com/lss233/chatgpt-mirai-qq-bot

## 功能特性

- **多平台 IM 接入**：内置 Telegram、QQ Bot（QQ 官方机器人）、微信企业号（WeCom）以及 HTTP Legacy 适配器插件，适配器通过注册表机制统一管理。
- **多 LLM 后端支持**：内置预设适配器插件，覆盖 OpenAI、Claude、Gemini、DeepSeek、Ollama、Moonshot（Kimi）、MiniMax、Mistral、SiliconFlow、腾讯云、火山引擎、OpenRouter、阿里云、Voyage 等主流服务；支持文本对话、图像生成、Embedding、Rerank 等模型类型与能力。
- **工作流引擎**：以「块（Block）」为基本单元构建工作流，包含 IM、LLM、记忆、游戏（骰子/抽卡）、MCP 工具、变量、系统等内置块；支持消息分发规则（按前缀、关键词、正则、@提及、聊天类型等条件路由到工作流）。
- **记忆系统**：支持作用域（scopes）、组合/分解策略（composer/decomposer），持久化支持本地文件与 Redis。
- **MCP 集成**：内置 MCP 模块，支持 stdio/SSE 连接方式连接外部 MCP 服务器，并可将 MCP 工具作为工作流块使用。
- **Web 管理界面**：基于 Quart/FastAPI + Hypercorn 的 Web 服务，提供认证（JWT + 密码哈希）、IM、LLM、分发规则、块、工作流、插件、系统、媒体、MCP、Tracing 等管理 API。
- **数据库与迁移**：使用 SQLAlchemy（默认 SQLite，位于 `data/db/kirara.db`），通过 Alembic 自动执行数据库迁移。
- **媒体管理**：统一管理消息中的媒体对象，支持 MIME 类型识别、未引用文件自动清理。
- **可观测性**：内置 Tracing 模块，可记录 LLM 请求链路。
- **内网穿透**：内置 frpc 插件，可按需将本机 Web 服务暴露到公网。

## 环境要求

- Python >= 3.10（MCP 组件仅支持 Python 3.10 及以上版本；Docker 镜像基于 Python 3.11）
- 可选系统依赖（Docker 镜像中已包含）：`wkhtmltopdf`、`ffmpeg`、`libmagic1`

## 安装

### 从 PyPI 安装

```bash
pip install kirara-ai
```

### 从源码安装

```bash
git clone https://github.com/lss233/chatgpt-mirai-qq-bot.git
cd chatgpt-mirai-qq-bot
pip install -e .
```

### 使用 Docker

仓库提供了多阶段构建的 `Dockerfile`：第一阶段构建 wheel 包，第二阶段安装系统依赖、下载 Web UI（npm 包 `kirara-ai-webui`）并安装应用。镜像默认暴露 `8080` 端口：

```bash
docker build -t kirara-ai .
docker run -d -p 8080:8080 -v $(pwd)/data:/app/data kirara-ai
```

Web UI 由 Dockerfile 自动下载并安装到 `/app/web`。如果手动部署时 Web UI 缺失，可从 https://github.com/DarkSkyTeam/chatgpt-for-bot-webui/releases 下载并解压到运行目录下的 `web/` 文件夹（确保存在 `web/index.html`）。

Windows 用户也可以使用 CI 产出的快速启动包（Windows Quickstart，内含 WinPython 运行时、FFmpeg 与 VC++ 运行库）。

## 快速开始

1. 首次运行前，可将仓库根目录的 `config.yaml.example` 复制为数据目录下的 `config.yaml`。
2. 启动服务：

```bash
# 以模块方式启动
python -m kirara_ai

# 或使用安装后的命令行入口
kirara_ai

# 可选参数
python -m kirara_ai -H 0.0.0.0 -p 8080
```

命令行参数：

| 参数 | 说明 |
| --- | --- |
| `-H` / `--host` | 覆盖 Web 服务监听地址 |
| `-p` / `--port` | 覆盖 Web 服务监听端口 |

3. 启动后访问 `http://127.0.0.1:8080` 打开 Web 管理界面，在界面中配置 IM 适配器、LLM 后端、分发规则与工作流。

## 配置

### 数据目录

所有运行时数据默认存储在当前工作目录的 `data/` 下，可通过环境变量 `DATA_PATH` 覆盖：

```bash
export DATA_PATH=/path/to/data
```

主要数据目录结构：

```
data/
├── config.yaml          # 全局配置（ConfigLoader 支持 YAML 读写并保留注释）
├── plugins/             # 外部插件目录
├── db/                  # SQLite 数据库
├── dispatch_rules/      # 消息分发规则（rules.yaml）
├── fonts/               # 内置字体（sarasa-mono-sc-regular.ttf）
├── media/               # 媒体文件存储
├── memory/              # 记忆持久化数据（file 模式）
├── web/                 # Web UI 静态文件与密码哈希（password.hash）
└── workflows/           # 工作流定义（YAML）
```

### 主要配置项（`config.yaml`）

全局配置由 Pydantic 模型定义，核心字段包括：

- `ims`：IM 适配器列表（名称、是否启用、适配器类型、适配器配置）。
- `llms`：LLM API 后端列表（名称、适配器类型、配置、启用的模型列表及模型类型/能力）。
- `mcp`：MCP 服务器列表（支持 `stdio` / `sse` 连接，可配置命令、参数、环境变量、请求 Headers）。
- `defaults.llm_model`：默认 LLM 模型（如 `gemini-1.5-flash`）。
- `memory`：记忆持久化（`file` / `redis`）、每个作用域最大记忆条目数、默认作用域类型。
- `web`：监听地址（默认 `127.0.0.1`）、端口（默认 `8080`）、JWT 密钥、密码哈希文件路径。
- `plugins`：启用的外部插件列表、插件市场 URL。
- `update`：PyPI / npm 镜像源地址。
- `frpc`：内网穿透配置（服务器地址、端口、令牌、远程端口）。
- `system.timezone`：时区（默认 `Asia/Shanghai`）。
- `tracing.llm_tracing_content`：是否记录 LLM 请求内容。
- `media`：媒体清理间隔天数、是否自动删除未引用媒体。

配置保存时会自动创建 `.bak` 备份。

## 使用

### 默认分发规则

安装后自带一组默认分发规则（见 `data/dispatch_rules/rules.yaml`）：

| 命令/触发条件 | 说明 |
| --- | --- |
| `/chat <内容>` 或在群聊中 @机器人 | 群聊 AI 对话 |
| 私聊直接发送内容 | 私聊 AI 对话 |
| `.roll XdY` | 骰子游戏 |
| 「抽卡」「十连」「单抽」 | 抽卡模拟器 |
| `/help` | 显示帮助信息 |
| `/清空记忆` | 清空当前对话记忆 |
| 其他消息（fallback） | 默认记忆存储工作流 |

分发规则支持按前缀、关键词、正则、@提及、聊天类型（群聊/私聊）等条件组合，并带有优先级与启用开关，可在 Web 界面中编辑。

### 插件

框架采用插件化架构，插件通过 `chatgpt_mirai.plugins` entry point 注册。内置插件包括：

- **IM 适配器**：`telegram`、`qqbot`、`wecom`、`http_legacy`
- **LLM 预设适配器**：`llm_presets`（OpenAI、Claude、Gemini、DeepSeek、Ollama 等）
- **bundled_frpc**：内网穿透

外部插件放入 `data/plugins/` 目录并在配置中启用；插件市场默认地址为 `https://kirara-plugin.app.lss233.com/api/v1`，可在 Web 界面中浏览安装。

## 开发

### 项目结构

```
kirara_ai/
├── config/          # 配置加载与全局配置模型
├── database/        # SQLAlchemy 数据库管理与 Alembic 迁移
├── events/          # 事件总线与各类应用事件
├── im/              # IM 适配器抽象、注册表与消息模型
├── ioc/             # 依赖注入容器
├── llm/             # LLM 适配器抽象、注册表与请求/响应格式
├── mcp_module/      # MCP 客户端集成
├── media/           # 媒体对象、载体与类型管理
├── memory/          # 记忆系统（作用域、组合/分解、持久化）
├── plugin_manager/  # 插件加载与生命周期管理
├── plugins/         # 内置插件
├── system/          # 系统更新
├── tracing/         # 链路追踪
├── web/             # Web 服务、认证与 REST API
└── workflow/        # 工作流核心（块、分发、执行）与内置实现
```

### 开发环境

推荐使用 pre-commit 钩子（仓库含 `.pre-commit-config.yaml`、`.pylintrc`）：

```bash
pip install pre-commit
pre-commit install
```

类型检查使用 mypy（配置见 `pyproject.toml` 与 `alembic.ini` 同级的项目配置）：

```bash
mypy --python-version 3.10 --ignore-missing-imports kirara_ai
```

CI（GitHub Actions）包含以下工作流：

- **run-tests.yml**：在 Ubuntu（Docker 容器内，带 pytest-cov 覆盖率并上传 Codecov）与 Windows（Python 3.13）上运行测试。
- **project_check.yml**：运行 mypy 类型检查，并将结果以 Issue 形式报告。
- **docker-latest.yml / docker-tag.yml**：构建并发布 Docker 镜像。
- **quickstart-windows.yml**：构建 Windows 快速启动包。
- **stale.yml**：自动处理不活跃的 Issue / PR。
- **pr_review.yml**：PR 类型检查评论。
- **dependabot.yml**：依赖自动更新。

## 测试

测试基于 `pytest`（配置见 `pytest.ini`），覆盖 LLM 适配器、记忆系统、系统块、工作流执行器、Web API、认证、Tracing、MCP 服务器等模块，并包含模拟 OpenAI/Gemini/Ollama/Voyage 接口的 mock 应用。

```bash
# 安装依赖
pip install -e .
pip install pytest pytest-asyncio

# 运行全部测试
python -m pytest ./tests -vs

# 运行覆盖率（与 CI 一致）
python -m pytest ./tests -v --cov=kirara_ai --cov-report=term-missing
```

## 许可证

本项目基于 **GNU Affero General Public License v3.0（AGPL-3.0-only）** 发布，完整条款见 [LICENSE](LICENSE) 文件。

简而言之：

- 你可以自由地使用、修改和分发本项目。
- 分发修改版本时，必须以相同的许可证开放源代码。
- 通过网络服务器向用户提供修改版本时，必须向这些用户提供对应的源代码（AGPL 第 13 条）。
- 本项目不提供任何形式的担保；作者不对使用造成的任何损失承担责任。

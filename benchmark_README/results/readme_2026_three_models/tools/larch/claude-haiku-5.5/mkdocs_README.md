# mkdocs-rpsphcuf

A Python static site generator for project documentation, built on [MkDocs](https://www.mkdocs.org/). It turns Markdown source files into a navigable HTML site, with live reloading during development, a client-side search index, built-in themes, a plugin and hook system, and support for translated theme strings.

> **Note:** This README was written from the repository's file listing, not from the source code itself. The feature descriptions and commands follow the standard MkDocs layout that these files match. Check the command names and paths against the code before publishing.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command-Line Interface](#command-line-interface)
- [Configuration](#configuration)
- [Writing Documentation](#writing-documentation)
- [Themes](#themes)
- [Search](#search)
- [Plugins and Hooks](#plugins-and-hooks)
- [Localization and Translations](#localization-and-translations)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Code Style](#code-style)
- [Building the Documentation](#building-the-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Project documentation is usually written as plain text files that are versioned alongside the code. This project takes those Markdown files, plus a single YAML configuration file, and produces a static HTML site that can be hosted anywhere, such as GitHub Pages, Read the Docs, Netlify, or a plain web server.

The core workflow is:

1. Write Markdown files in a `docs/` directory.
2. Describe the site (name, navigation, theme, extensions) in `mkdocs.yml`.
3. Preview the site locally with a live-reloading development server.
4. Build the static site into a `site/` directory and deploy it.

## Features

- **Markdown rendering** with Python-Markdown and its extensions, including tables, admonitions, table of contents generation, and code highlighting.
- **Live preview server** that rebuilds and reloads the browser when source files change.
- **Two bundled themes**: `mkdocs` (the default) and `readthedocs`. Both support light and dark color modes and responsive layouts.
- **Client-side search** using a prebuilt Lunr.js index, with stemming and stop-word support for many languages.
- **Explicit or automatic navigation** defined in `mkdocs.yml` or inferred from the file tree.
- **Plugin architecture** with lifecycle events, so you can extend or modify the build.
- **Hooks** for running custom Python code at specific build points without packaging a plugin.
- **Theme localization** through gettext `.po`/`.pot` catalogs, with translations for many languages.
- **Custom themes and template overrides** using Jinja2.
- **Built-in GitHub Pages deployment** via a `gh-deploy` command.
- **Project scaffolding** with a `new` command that creates a starter project.

## Installation

### Requirements

- Python 3.8 or newer (check `pyproject.toml` for the exact minimum)
- `pip`

### From PyPI

```bash
pip install mkdocs
```

### From this repository

```bash
git clone https://github.com/<your-account>/mkdocs-rpsphcuf.git
cd mkdocs-rpsphcuf
pip install -e .
```

The editable install (`-e`) lets you test changes to the source without reinstalling.

To verify the installation:

```bash
mkdocs --version
```

## Quick Start

Create a new project:

```bash
mkdocs new my-project
cd my-project
```

This creates:

```text
my-project/
├── mkdocs.yml
└── docs/
    └── index.md
```

Start the development server:

```bash
mkdocs serve
```

Open http://127.0.0.1:8000/ in a browser. Edits to files in `docs/` or to `mkdocs.yml` will trigger an automatic rebuild and reload.

Build the static site:

```bash
mkdocs build
```

The output goes to `site/`.

## Command-Line Interface

| Command | Description |
|---|---|
| `mkdocs new <dir>` | Create a new project with a starter `mkdocs.yml` and `docs/index.md`. |
| `mkdocs serve` | Start a live-reloading development server (default `127.0.0.1:8000`). |
| `mkdocs build` | Build the site into `site/`. |
| `mkdocs gh-deploy` | Build the site and push it to the `gh-pages` branch on GitHub. |

### Useful options

```bash
mkdocs serve --dev-addr 0.0.0.0:8080   # Bind to a different address and port
mkdocs serve --no-livereload           # Disable automatic reloading
mkdocs build --clean                   # Remove the site directory before building
mkdocs build --strict                  # Treat warnings as errors
mkdocs build --site-dir dist           # Write output to a different directory
mkdocs build -v                        # Verbose output
mkdocs gh-deploy --force               # Force-push to gh-pages
```

Run `mkdocs --help` or `mkdocs <command> --help` for the full list.

## Configuration

All site settings live in `mkdocs.yml` at the project root. A complete example:

```yaml
site_name: My Project
site_url: https://example.com/docs/
site_description: Documentation for My Project
site_author: Jane Developer
repo_url: https://github.com/example/my-project
repo_name: example/my-project
edit_uri: edit/main/docs/

docs_dir: docs
site_dir: site
use_directory_urls: true
strict: false

theme:
  name: mkdocs          # or "readthedocs"
  locale: en
  language: en
  features:
    - navigation.sections
    - navigation.top
    - search.highlight
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - User Guide:
      - Installation: user-guide/installation.md
      - Configuration: user-guide/configuration.md
  - API Reference: api.md

markdown_extensions:
  - toc:
      permalink: true
  - admonition
  - tables
  - codehilite

plugins:
  - search

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/example/my-project
```

### Key options

| Option | Purpose |
|---|---|
| `site_name` | **Required.** Name shown in the header and page titles. |
| `site_url` | Base URL of the published site. Needed for correct canonical links and sitemaps. |
| `docs_dir` | Source directory for Markdown files. Default: `docs`. |
| `site_dir` | Output directory for the built site. Default: `site`. |
| `use_directory_urls` | When true, `page.md` becomes `page/index.html` for cleaner URLs. |
| `nav` | Explicit site navigation. If omitted, navigation is generated from the file tree. |
| `theme` | Theme name, custom directory, features, palette, and locale. |
| `markdown_extensions` | Python-Markdown extensions to enable, with optional settings. |
| `plugins` | Plugins to run during the build. |
| `hooks` | Python files containing hook functions. |
| `extra` | Arbitrary data made available to templates. |
| `extra_css` / `extra_javascript` | Additional stylesheets and scripts to include. |
| `strict` | Fail the build on warnings. |

## Writing Documentation

Pages are standard Markdown files in `docs/`.

```markdown
# Page Title

Regular paragraph text with **bold**, *italic*, and `inline code`.

## Section

- Bullet item
- Another item

| Column A | Column B |
|----------|----------|
| 1        | 2        |

!!! note
    Admonitions work when the `admonition` extension is enabled.

```python
def hello():
    print("Hello, world")
```
```

### Navigation

- If `nav` is set in `mkdocs.yml`, only listed pages appear in the navigation, in the order given.
- If `nav` is omitted, pages are sorted alphabetically, and `index.md` is placed first.
- Pages not listed in `nav` still build, but they will not appear in the navigation menu.

### Assets

Images, stylesheets, and scripts placed in `docs/` are copied to the site unchanged. Reference them with relative paths:

```markdown
![Screenshot](images/screenshot.png)
```

## Themes

### Bundled themes

- **mkdocs**: The default theme. Clean, with a responsive sidebar, search, and light and dark modes.
- **readthedocs**: Styled to resemble the Read the Docs default, with a left-hand navigation panel and a top bar.

Select a theme in `mkdocs.yml`:

```yaml
theme:
  name: readthedocs
```

### Customizing a theme

Override individual templates or add assets without forking the theme. Create a `custom_dir` and point the theme at it:

```yaml
theme:
  name: mkdocs
  custom_dir: overrides/
```

Any file in `overrides/` with the same name as a theme template (for example, `main.html`) replaces the bundled version. Extra CSS and JavaScript can be added through `extra_css` and `extra_javascript`.

### Creating a theme

A theme is a directory containing:

- `mkdocs_theme.yml`: metadata and default options
- Jinja2 templates such as `base.html`, `main.html`, `404.html`, and `search.html`
- Static assets such as CSS, JavaScript, fonts, and images
- Optional `messages.pot` and `.po` files for localization

Packaged themes are discovered through the `mkdocs.themes` entry point, so a third-party theme can be installed with `pip` and selected by name.

## Search

Search is provided by the `search` plugin, which is enabled by default. During the build it generates a JSON search index that the browser loads and queries using Lunr.js. There is no server-side component, so search works on any static host.

Relevant files:

- `search/search_index.py`: builds the index
- `search/prebuild-index.js`: optional prebuilt index support
- `search/lunr.js`, `search/main.js`, `search/worker.js`: client-side search
- `search/lunr.*.js`: language-specific stemmers and stop-word lists

Configure the plugin:

```yaml
plugins:
  - search:
      lang:
        - en
        - de
      separator: '[\s\-\.]+'
```

Languages with stemmers include Arabic, Chinese, Danish, Dutch, Finnish, French, German, Hindi, Hungarian, Italian, Japanese, Korean, Norwegian, Portuguese, Romanian, Russian, Spanish, Swedish, Tamil, Telugu, Thai, Turkish, Vietnamese, and others.

## Plugins and Hooks

### Plugins

Plugins are Python classes that subscribe to build events. Enable them in `mkdocs.yml`:

```yaml
plugins:
  - search
  - some-third-party-plugin:
      option: value
```

Plugins can respond to events at various stages of the build, including:

- `on_config`: after configuration is loaded
- `on_files`: after source files are discovered
- `on_nav`: after navigation is built
- `on_page_markdown`: after a page is read and before it is converted
- `on_page_content`: after Markdown is rendered to HTML
- `on_post_page`: after each page is written
- `on_post_build`: after the full build is complete

The `docs/plugin-events.md` file in this repository documents the event sequence.

### Hooks

Hooks are simpler: they are plain functions in a Python file referenced from `mkdocs.yml`. They are useful for small project-specific customizations that do not need to be packaged.

```yaml
hooks:
  - hooks.py
```

## Localization and Translations

Theme strings such as "Next", "Previous", and "Search" are translated through gettext catalogs:

- `messages.pot`: the template catalog, with all translatable strings
- `*/LC_MESSAGES/messages.po`: per-language translations

Set the language in `mkdocs.yml`:

```yaml
theme:
  name: mkdocs
  locale: fr
```

The repository includes translation catalogs for many languages across both bundled themes. To add a translation:

1. Extract strings from the theme.
2. Initialize or update the `.po` file for your language.
3. Translate the entries and compile the catalog.

The `babel.cfg` file in the theme directory configures string extraction. Babel is optional and only needed to maintain translations.

## Deployment

### GitHub Pages

```bash
mkdocs gh-deploy
```

This builds the site and pushes the output to the `gh-pages` branch. Enable GitHub Pages in the repository settings to serve it. Use `CNAME` to set a custom domain.

### Read the Docs

Add a `.readthedocs.yaml` file to the repository that installs MkDocs and runs `mkdocs build`. Read the Docs will build and host the site.

### Other static hosts

Run `mkdocs build` and upload the contents of `site/` to any static file host, such as Netlify, S3, Cloudflare Pages, or nginx.

## Project Structure

The repository follows the layout of a standard MkDocs project. Based on the file listing, the main parts are:

```text
mkdocs-rpsphcuf/
├── mkdocs/                      # Main Python package
│   ├── __init__.py
│   ├── __main__.py              # Entry point for `python -m mkdocs`
│   ├── exceptions.py            # Custom exception types
│   ├── commands/                # CLI commands
│   │   ├── build.py
│   │   ├── serve.py
│   │   ├── new.py
│   │   └── gh_deploy.py
│   ├── config/                  # Configuration loading and validation
│   │   ├── base.py
│   │   ├── config_options.py
│   │   └── defaults.py
│   ├── structure/               # Site model
│   │   ├── files.py
│   │   ├── pages.py
│   │   ├── nav.py
│   │   └── toc.py
│   ├── theme.py                 # Theme loading
│   ├── utils/                   # Shared helpers (meta, yaml, templates, cache, filters)
│   ├── localization.py          # Translation support
│   ├── livereload/              # Development server with live reload
│   ├── search/                  # Search index and client-side assets
│   ├── contrib/                 # Optional integrations
│   ├── themes/
│   │   ├── mkdocs/              # Default theme
│   │   └── readthedocs/         # Read the Docs-style theme
│   └── tests/                   # Test suite
├── docs/                        # Project documentation (built with MkDocs itself)
├── mkdocs.yml                   # Configuration for the project's own docs
├── pyproject.toml               # Package metadata and build configuration
├── setup.py                     # Legacy packaging entry point
├── hatch_build.py               # Hatch build hook
├── requirements-docs.txt        # Dependencies for building the docs
├── requirements-style.txt       # Dependencies for linting and formatting
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-account>/mkdocs-rpsphcuf.git
   cd mkdocs-rpsphcuf
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

3. Install the package in editable mode with development dependencies:

   ```bash
   pip install -e .
   pip install -r requirements-docs.txt
   pip install -r requirements-style.txt
   ```

4. Confirm the setup:

   ```bash
   mkdocs --version
   ```

## Running Tests

The test suite lives in `mkdocs/tests/` and covers the CLI, configuration, build pipeline, navigation, page rendering, the table of contents, search, themes, localization, plugins, and live reload.

Run the full suite:

```bash
python -m unittest discover -s mkdocs/tests -t .
```

Run a single module:

```bash
python -m unittest mkdocs.tests.build_tests
```

Or, if `pytest` is installed:

```bash
pytest mkdocs/tests
```

## Code Style

Style checks and formatting are listed in `requirements-style.txt`. Run them before submitting changes. Typical tools for this kind of project include:

- **ruff** or **flake8** for linting
- **black** or **ruff format** for formatting
- **mypy** for type checking, if configured

Check `pyproject.toml` and `CONTRIBUTING.md` for the exact configuration and commands.

## Building the Documentation

The project documentation is written in Markdown in `docs/` and built with MkDocs itself.

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

Then open http://127.0.0.1:8000/.

## Contributing

Contributions are welcome. Before opening a pull request:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Open an issue to discuss significant changes.
3. Fork the repository and create a topic branch.
4. Add or update tests for your change.
5. Run the test suite and style checks.
6. Update the documentation in `docs/` if user-facing behavior changes.
7. Submit a pull request with a clear description.

Bug reports should include the MkDocs version, Python version, operating system, a minimal `mkdocs.yml`, and the steps to reproduce.

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.

---

## Acknowledgements

This project builds on the work of the MkDocs community and on several open-source libraries, including Python-Markdown, Jinja2, Click, PyYAML, Lunr.js, Bootstrap, Font Awesome, and jQuery. Font and library files bundled in the themes are distributed under their respective licenses.

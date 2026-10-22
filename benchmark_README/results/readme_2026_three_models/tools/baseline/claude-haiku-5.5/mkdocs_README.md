# MkDocs

MkDocs is a fast, simple static site generator for building project documentation. You write source files in Markdown, configure the site with a single YAML file (`mkdocs.yml`), and MkDocs builds a static HTML site that you can host almost anywhere. The project is distributed on PyPI as `mkdocs`, and its documentation is published at <https://www.mkdocs.org/>.

## Overview

MkDocs provides the following capabilities, as described in the project documentation and source:

- **Markdown-based sources.** Pages are written in Markdown and rendered with the Python-Markdown library. Extensions can be enabled through the `markdown_extensions` setting.
- **YAML configuration.** The site is configured through `mkdocs.yml`. The `site_name` setting is the only required option.
- **Built-in themes.** Two themes ship with MkDocs: `mkdocs` (the default, based on Bootstrap) and `readthedocs`. Both support translations, and the `mkdocs` theme also supports light and dark color modes.
- **Built-in search.** The `search` plugin is enabled by default and uses lunr.js to provide client-side search. Multiple languages are supported through lunr-languages.
- **Live-reloading development server.** `mkdocs serve` rebuilds the site when the configuration file, documentation directory, or theme changes.
- **Plugins and hooks.** Plugins are Python packages that hook into build events. Hooks allow the same kind of event handlers to be defined in local Python files without installing a package.
- **Static output.** `mkdocs build` writes a `site/` directory of static files. The `gh-deploy` command publishes the site to GitHub Pages.

## Installation

MkDocs requires Python 3.8 or later. The project classifiers list support for Python 3.8 through 3.12 on CPython and PyPy.

Install MkDocs from PyPI with pip:

```bash
pip install mkdocs
```

To enable theme localization, install the optional `i18n` extra, which adds the `babel` dependency:

```bash
pip install 'mkdocs[i18n]'
```

Run `mkdocs --version` to confirm the installation. The output reports the installed version, its location, and the Python version in use.

The core dependencies declared in `pyproject.toml` include `click`, `Jinja2`, `Markdown`, `PyYAML`, `watchdog`, `ghp-import`, `pyyaml_env_tag`, `packaging`, `mergedeep`, `pathspec`, `mkdocs-get-deps`, and `colorama` on Windows.

To install a development version directly from the repository, the contributing guide suggests:

```bash
pip install git+https://github.com/mkdocs/mkdocs.git
```

## Quick Start

Create a new project, then start the development server:

```bash
mkdocs new my-project
cd my-project
mkdocs serve
```

`mkdocs new` creates a `mkdocs.yml` file and a `docs/` directory containing `index.md`. `mkdocs serve` builds the site and serves it at <http://127.0.0.1:8000/> by default.

To produce the static site, run:

```bash
mkdocs build
```

The output is written to the `site/` directory.

## Usage

MkDocs provides a command-line interface through the `mkdocs` command. The commands defined in `mkdocs/__main__.py` are:

| Command | Purpose |
| --- | --- |
| `mkdocs new <project_directory>` | Create a new MkDocs project. |
| `mkdocs serve` | Run the built-in development server with live reloading. |
| `mkdocs build` | Build the documentation site into `site_dir`. |
| `mkdocs gh-deploy` | Build the site and deploy it to GitHub Pages. |
| `mkdocs get-deps` | Print the PyPI packages inferred from the plugins, themes, and extensions in `mkdocs.yml`. |

Some useful options:

- `mkdocs serve -a <IP:PORT>` sets the address of the development server. `-o` opens the site in a browser.
- `mkdocs serve --dirty` rebuilds only changed files. `--clean` performs a normal build.
- `mkdocs build --strict` aborts the build on any warning.
- `mkdocs build -f <file>` uses a specific configuration file, and `-f -` reads it from standard input.
- `-v`/`--verbose` enables debug output, and `-q`/`--quiet` silences warnings.
- `--color/--no-color` controls colored output. The `NO_COLOR` environment variable is also respected.

Run `mkdocs --help` or `mkdocs <command> --help` for the full option list.

To install the packages needed by a site's plugins and extensions, the `get-deps` command can be combined with pip:

```bash
pip install $(mkdocs get-deps)
```

## Configuration

Project settings live in `mkdocs.yml`, which MkDocs looks for in the current directory by default. A minimal configuration is:

```yaml
site_name: My Documentation
nav:
  - Home: index.md
  - About: about.md
theme:
  name: readthedocs
```

Commonly used settings documented in the user guide include:

- **`site_name`** (required): The main title of the project documentation.
- **`site_url`**: The canonical URL of the site. It also determines the path used by `mkdocs serve`.
- **`repo_url`**, **`repo_name`**, **`edit_uri`**, and **`edit_uri_template`**: Links to the source repository and to the editable source of each page.
- **`nav`**: The navigation structure. If omitted, navigation is generated automatically from the Markdown files in `docs_dir`, sorted alphabetically with index files first.
- **`theme`**: A theme name, or a mapping with `name`, `locale`, `custom_dir`, and theme-specific options.
- **`docs_dir`** (default `docs`) and **`site_dir`** (default `site`).
- **`use_directory_urls`** (default `true`): Controls whether pages are written as `index.html` inside directories.
- **`strict`** (default `false`): Treats warnings as errors.
- **`dev_addr`** (default `127.0.0.1:8000`): The address for `mkdocs serve`.
- **`extra_css`**, **`extra_javascript`**, **`extra_templates`**, and **`extra`**: Additional assets, templates, and template variables.
- **`markdown_extensions`**: Python-Markdown extensions. The defaults are `meta`, `toc`, `tables`, and `fenced_code`.
- **`plugins`** (default `['search']`): Plugins to run. Specifying this setting replaces the defaults, so `search` must be listed again to keep it.
- **`hooks`**: Local Python files that provide plugin-style event handlers.
- **`exclude_docs`**, **`draft_docs`**, and **`not_in_nav`**: Gitignore-style patterns that control which files are excluded, treated as drafts, or left out of the navigation.
- **`validation`**: Strictness levels (`warn`, `info`, or `ignore`) for link and anchor checks.

Configuration files can inherit from a parent file with the `INHERIT` key. Mappings are deep-merged, while lists are replaced in full.

The `!ENV` YAML tag reads values from environment variables, and the `!relative` tag resolves paths relative to the current Markdown file or the site.

## Themes

MkDocs includes two built-in themes:

- **`mkdocs`**: The default theme. It supports options such as `color_mode`, `user_color_mode_toggle`, `nav_style`, `highlightjs`, `hljs_style`, `analytics`, `shortcuts`, and `navigation_depth`.
- **`readthedocs`**: A clone of the Read the Docs theme. Its options include `include_homepage_in_sidebar`, `prev_next_buttons_location`, `collapse_navigation`, `titles_only`, `sticky_navigation`, and `logo`.

Custom themes can be created in a `custom_dir` directory. Themes can also be packaged for distribution. The developer guide describes the template variables, filters such as `url`, `tojson`, and `script_tag`, and the layout for packaged themes.

To override parts of an existing theme, set `theme.custom_dir` and provide files with matching names. The `main.html` template can override named blocks in the parent theme.

## Plugins and Hooks

Plugins are Python packages that subclass `mkdocs.plugins.BasePlugin` and register under the `mkdocs.plugins` entry point. The only plugin registered by MkDocs itself is `search`. A plugin is enabled by listing it under `plugins:` in `mkdocs.yml`. Its options are nested beneath its name.

Plugins respond to build events such as `on_config`, `on_pre_build`, `on_files`, `on_nav`, `on_page_markdown`, and `on_post_build`. Priorities can be set with `event_priority`. Plugins are expected to log through the `mkdocs.plugins.` logger namespace.

## Documentation

The MkDocs documentation source lives in `docs/`, with sections for getting started, the user guide, the developer guide, and the "about" pages. The site is built with MkDocs itself, and its configuration is in `mkdocs.yml`.

## Development

The main development tool is [Hatch](https://hatch.pypa.io/), which manages environments and runs commands defined in `pyproject.toml`. The project uses [Hatchling](https://hatch.pypa.io/latest/) as its build backend. `setup.py` is no longer supported for installation.

To install a local clone in editable mode, use:

```bash
pip install --editable .
```

Useful Hatch commands:

- `hatch run all`: Runs style fixes, type checks, unit tests, lint checks, and integration tests.
- `hatch run style:fix`: Formats code with Black and isort, then applies Ruff fixes.
- `hatch run types:check`: Runs mypy on the `mkdocs` package.
- `hatch run lint:check`: Runs markdownlint, jshint, CSS checks, and codespell.
- `hatch run docs:serve`: Serves the MkDocs documentation locally.

Code style is configured in `pyproject.toml`: Black with a line length of 100, isort with the Black profile, and Ruff with an extensive rule selection.

Translations of the built-in themes use Babel (`pybabel`). The contributing guide describes how to update the `messages.pot` files with `pybabel extract` and how to create or update locales.

## Testing

Tests are written with `unittest` and are discovered from files matching `*tests.py` under `mkdocs/`. Run them with:

```bash
hatch run test:test
```

Integration tests, which build sample projects in `mkdocs/tests/integration/`, run with:

```bash
hatch run integration:test
```

The test matrix covers Python 3.8 through 3.12 and PyPy 3, with default and minimum-version dependency sets. Coverage is collected with `coverage` through the `_coverage` script, and `.codecov.yml` sets a project coverage target of 90%.

GitHub Actions workflows in `.github/workflows/` run the CI, autofix, docs, and release deployment jobs.

## Contributing

Contributions are welcome in the form of code, documentation, bug reports, and reviews. Before opening a large pull request, the contributing guide recommends opening an issue for early feedback. Pull requests should include tests and documentation for new features. Commits should avoid force-pushes, and changes to `release-notes.md` should not be included, since release notes are written later.

Participants are expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

## License

MkDocs is released under the BSD 2-Clause license. The `LICENSE` file contains the license text, and `pyproject.toml` declares `BSD-2-Clause`. The copyright notice is held by Tom Christie.

The documentation's license page also states that the bundled ReadTheDocs theme is used under license from the ReadTheDocs projects.

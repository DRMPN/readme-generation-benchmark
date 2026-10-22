# MkDocs

Project documentation with Markdown.

MkDocs is a static site generator for building project documentation. Documentation source files are written in Markdown and configured with a single YAML file (`mkdocs.yml`). It includes a built-in development server with live reloading and a built-in search feature.

- Documentation: <https://www.mkdocs.org/>
- Source: <https://github.com/mkdocs/mkdocs>
- Issues: <https://github.com/mkdocs/mkdocs/issues>
- Release notes: <https://www.mkdocs.org/about/release-notes/>

## Requirements

- Python 3.8 or newer (CPython and PyPy are listed as supported in the package classifiers)
- pip

## Installation

Install MkDocs from PyPI:

```bash
pip install mkdocs
```

Check the installation:

```bash
mkdocs --version
```

Optional internationalization support for themes is available through the `i18n` extra, which installs Babel:

```bash
pip install 'mkdocs[i18n]'
```

## Quick start

Create a new project:

```bash
mkdocs new my-project
cd my-project
```

This creates a `mkdocs.yml` configuration file and a `docs/` directory containing `index.md`:

```text
my-project/
├── mkdocs.yml    # The configuration file.
└── docs/
    └── index.md  # The documentation homepage.
```

Start the development server, which rebuilds and reloads the site as you edit files:

```bash
mkdocs serve
```

By default the site is served at <http://127.0.0.1:8000/>.

Build the static site:

```bash
mkdocs build
```

The output is written to the `site/` directory.

## Commands

| Command | Description |
| --- | --- |
| `mkdocs new <dir>` | Create a new project with a starter `mkdocs.yml` and `docs/index.md`. |
| `mkdocs serve` | Build the site and run the built-in development server with live reloading. |
| `mkdocs build` | Build the documentation site into `site/` (or the directory set by `--site-dir`). |
| `mkdocs gh-deploy` | Build the site and deploy it to a GitHub Pages branch (`gh-pages` by default). |
| `mkdocs get-deps` | Print the PyPI packages required by the plugins declared in `mkdocs.yml`. |

Run `mkdocs --help` for all commands, or `mkdocs <command> --help` for the options of a specific command. Some commonly used options:

- `-f, --config-file`: use a specific configuration file.
- `-t, --theme`: select the theme to use.
- `-s, --strict`: abort the build on any warning.
- `-d, --site-dir`: set the output directory (for `build` and `gh-deploy`).
- `-a, --dev-addr <IP:PORT>`: set the address for `serve` (default `127.0.0.1:8000`).
- `-o, --open`: open the site in a browser after the initial build (`serve`).
- `--no-livereload`: disable live reloading in `serve`.

## Configuration

MkDocs is configured with a `mkdocs.yml` file in the project root. The `site_name` option is the only required setting. A minimal example:

```yaml
site_name: My Docs
nav:
  - Home: index.md
  - About: about.md
theme: readthedocs
```

Documentation for all configuration options, including `nav`, `theme`, `docs_dir`, `site_dir`, `site_url`, `plugins`, and `markdown_extensions`, is available in the [configuration guide](https://www.mkdocs.org/user-guide/configuration/).

## Themes

MkDocs ships with two built-in themes:

- `mkdocs` (default)
- `readthedocs`

Third-party themes are listed on the [MkDocs Themes wiki page](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes) and in the [MkDocs Catalog](https://github.com/mkdocs/catalog). Custom themes can be created by following the [theme developer guide](https://www.mkdocs.org/dev-guide/themes/).

## Plugins

MkDocs supports plugins, which are declared in the `plugins` section of `mkdocs.yml`. The built-in `search` plugin is included in the package. Other plugins are installed separately; use `mkdocs get-deps` to list the packages required by the plugins in your configuration. Plugin development is described in the [plugin developer guide](https://www.mkdocs.org/dev-guide/plugins/).

## Deployment

`mkdocs build` produces static HTML, CSS, and JavaScript files that can be hosted on any static file host. Deployment options include:

- **GitHub Pages**: `mkdocs gh-deploy` builds the site and pushes it to a branch of your repository using [ghp-import](https://github.com/davisp/ghp-import).
- **Read the Docs**: supports MkDocs out of the box.
- **Other hosts**: upload the contents of the `site/` directory to any web server.

See the [deployment guide](https://www.mkdocs.org/user-guide/deploying-your-docs/) for details, including notes on viewing the built site directly from the file system (`file://`).

## Documentation

The full documentation is available at <https://www.mkdocs.org/>. It includes:

- [Getting Started](https://www.mkdocs.org/getting-started/): an introductory tutorial.
- [Installation Guide](https://www.mkdocs.org/user-guide/installation/).
- [User Guide](https://www.mkdocs.org/user-guide/): CLI, configuration, writing docs, themes, and deployment.
- [Developer Guide](https://www.mkdocs.org/dev-guide/): plugins, themes, translations, and the Python API.

To preview the documentation source in this repository, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Development

This project uses [Hatch](https://hatch.pypa.io/) for development tasks. Install it with `pipx install hatch` or `pip install hatch`.

To install a local clone in editable mode:

```bash
pip install --editable .
```

Common tasks:

```bash
hatch run test:test          # Unit tests
hatch run integration:test   # Integration tests
hatch run style:fix          # Format and lint-fix (Black, isort, Ruff)
hatch run types:check        # Type checking (mypy)
hatch run lint:check         # Markdown, JS, CSS, and spelling checks
hatch run all                # Run all of the above
```

Tests are run against the Python versions listed in `.github/workflows/ci.yml`. Pull requests are checked by GitHub Actions.

## Contributing

Contributions are welcome, including code patches, documentation improvements, and bug reports. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. For large changes, open an issue first to discuss the approach.

Everyone participating in the project is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

## Getting help

- [GitHub Discussions](https://github.com/mkdocs/mkdocs/discussions) for questions.
- [GitHub Issues](https://github.com/mkdocs/mkdocs/issues) for bug reports and feature requests.

## License

MkDocs is released under the BSD 2-Clause License. See [LICENSE](LICENSE) for the full text.

Copyright © 2014-present, Tom Christie.

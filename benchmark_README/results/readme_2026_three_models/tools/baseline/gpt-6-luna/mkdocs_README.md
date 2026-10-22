# MkDocs

MkDocs is a fast, simple static site generator for project documentation. Write pages in Markdown, configure the site in a YAML file, and build a directory of static files that can be hosted on GitHub Pages or another static-file host.

MkDocs includes a live-reloading development server, client-side search, and two built-in themes: `mkdocs` and `readthedocs`. You can extend or customize sites with Markdown extensions, plugins, and themes.

- **Documentation:** <https://www.mkdocs.org/>
- **Source code:** <https://github.com/mkdocs/mkdocs>
- **Issues:** <https://github.com/mkdocs/mkdocs/issues>
- **Discussions:** <https://github.com/mkdocs/mkdocs/discussions>
- **Release notes:** <https://www.mkdocs.org/about/release-notes/>

## Installation

MkDocs requires Python 3.8 or later and pip. Install the package with:

```bash
python -m pip install mkdocs
```

Check that the command is available:

```bash
mkdocs --version
```

Theme localization support is optional. To install the Babel dependency used for localization, install the `i18n` extra:

```bash
python -m pip install 'mkdocs[i18n]'
```

For Windows, if the `mkdocs` command is not on your PATH, you can invoke it as a Python module:

```bash
python -m mkdocs --help
```

## Create and preview a site

Create a starter project, then move into its directory:

```bash
mkdocs new my-project
cd my-project
```

A new project contains an `mkdocs.yml` configuration file and a `docs/` directory with an initial `index.md` page. Start the local development server from the directory containing `mkdocs.yml`:

```bash
mkdocs serve
```

By default, the site is served at <http://127.0.0.1:8000/>. The server watches the documentation and configuration, rebuilds when they change, and refreshes the browser.

Add Markdown pages and other assets under `docs/`. For example, a project might contain:

```text
mkdocs.yml
docs/
    index.md
    about.md
    img/
        diagram.png
```

Markdown files become pages, and other files in the documentation directory are copied to the generated site. Use relative Markdown links to connect pages and regular Markdown image syntax to include images.

## Build and deploy

Build the site with:

```bash
mkdocs build
```

The generated site is written to `site/` by default. This output consists of static files; upload the contents of the output directory to a host that serves static files. If using version control, the generated `site/` directory is typically excluded from the source repository.

For GitHub Pages, run the deployment command from the project repository:

```bash
mkdocs gh-deploy
```

This builds the documentation and deploys it to the `gh-pages` branch by default. Use `mkdocs gh-deploy --help` to see deployment options. Review changes with `mkdocs serve` or `mkdocs build` before deploying; the command publishes the generated files directly.

## Configuration

MkDocs reads settings from `mkdocs.yml` in the project directory by default. The only required setting is `site_name`. A minimal configuration is:

```yaml
site_name: Example Project
```

The documentation source directory defaults to `docs`, and the generated site directory defaults to `site`. Navigation can be declared explicitly; paths in `nav` are relative to `docs_dir`:

```yaml
site_name: Example Project
nav:
  - Home: index.md
  - About: about.md
theme:
  name: mkdocs
```

If `nav` is omitted, MkDocs creates navigation from the Markdown files it finds. The built-in `search` plugin is enabled by default. If you define a `plugins` list, defaults are no longer automatically included; list `search` explicitly if you want to keep it.

Configuration also supports options for themes, Markdown extensions, plugins, extra CSS and JavaScript, output URLs, and link validation. Values can be read from environment variables using the `!ENV` YAML tag. See the [configuration guide](https://www.mkdocs.org/user-guide/configuration/) for available settings and examples.

Use `mkdocs --help` for the command list and `mkdocs <command> --help` for options for a specific command. Common commands include:

- `mkdocs new <directory>` — create a project.
- `mkdocs serve` — preview and rebuild the site locally.
- `mkdocs build` — generate the static site.
- `mkdocs gh-deploy` — deploy to GitHub Pages.
- `mkdocs get-deps` — print PyPI packages inferred from the configured themes, plugins, and Markdown extensions.

## Themes, plugins, and extensions

The built-in themes are `mkdocs` and `readthedocs`; select one with the `theme` setting. Third-party themes and plugins are Python packages and must be installed before being enabled in the configuration. MkDocs also supports custom theme directories and plugin-like hooks defined in local Python files.

Python-Markdown extensions can be enabled through `markdown_extensions`. The built-in search plugin uses Lunr.js and supports configurable languages and indexing behavior. For full instructions on writing documentation, selecting and customizing themes, plugins, localization, and deployment, see the [User Guide](https://www.mkdocs.org/user-guide/).

## Development

Contributions to MkDocs are welcome, including code, documentation improvements, bug reports, and patch reviews. The development workflow uses [Hatch](https://hatch.pypa.io/) to manage environments and run checks. Install Hatch, clone the repository, and run commands from the repository root.

To run the full set of configured checks:

```bash
hatch run all
```

The project also provides focused commands:

```bash
hatch run test:test
hatch run integration:test
hatch run style:fix
hatch run types:check
hatch run lint:check
```

The unit test command uses Python’s `unittest` discovery. The integration command runs the integration suite. Style checks include Python formatting and Ruff linting; type checking uses mypy. Other lint checks cover Markdown, JavaScript, CSS, and spelling. The test and integration environments are configured for Python 3.8 through 3.12 and PyPy 3.

To preview changes to MkDocs’ own documentation:

```bash
hatch run docs:serve
```

Resolve documentation warnings before submitting changes. See [CONTRIBUTING.md](CONTRIBUTING.md) for issue-reporting guidance, pull request expectations, and translation contribution instructions. For bug reports, include the MkDocs version, platform, relevant configuration and files, expected behavior, and actual behavior; include the full error message and traceback when applicable.

## License

MkDocs is licensed under the BSD 2-Clause License. See [LICENSE](LICENSE) for the copyright notice, redistribution conditions, and disclaimer.

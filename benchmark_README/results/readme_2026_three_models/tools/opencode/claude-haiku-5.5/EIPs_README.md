# Ethereum Improvement Proposals (EIPs)

This repository holds the source text of the Ethereum Improvement Proposals (EIPs) and the Jekyll site that publishes them at <https://eips.ethereum.org>.

An EIP is a design document that describes a standard, feature, process, or piece of information for the Ethereum ecosystem. EIPs are the main channel for proposing changes, collecting technical feedback, and recording design decisions. See [EIP-1](EIPS/eip-1.md) for the full process.

ERC (application-level) proposals were moved to a separate repository, [ethereum/ERCs](https://github.com/ethereum/ercs). The build workflows copy those ERC files into this site and rename them from `erc-*` to `eip-*`. ERC files are therefore not stored in this repository.

## Repository layout

| Path | Contents |
| --- | --- |
| `EIPS/` | One Markdown file per EIP, named `eip-<number>.md`. |
| `assets/eip-<number>/` | Supporting files for individual EIPs, such as images, test vectors, and reference code. |
| `eip-template.md` | Template for new EIPs. |
| `_layouts/`, `_includes/`, `_data/` | Jekyll layout, partials, and data files (for example, `_data/statuses.yaml`). |
| `assets/css/` | Stylesheets for the site. |
| `rss/` | Generated RSS feeds, including feeds for all EIPs, Last Call EIPs, and non-ERC EIPs. |
| `*.html` (for example, `all.html`, `core.html`, `erc.html`) | Index pages for the site, grouped by category or type. |
| `config/` | Linting and link-check configuration (`eipw.toml`, `mlc_config.json`, `eip-editors.yml`, and others). |
| `.github/` | Issue and pull request templates, `CONTRIBUTING.md`, `CODEOWNERS`, and GitHub Actions workflows. |
| `_config.yml`, `Gemfile`, `Gemfile.lock` | Jekyll site configuration and Ruby dependencies. |
| `CNAME` | Custom domain for GitHub Pages (`eips.ethereum.org`). |
| `LICENSE.md` | License for the content (CC0 1.0 Universal). |

## EIP categories and statuses

Each EIP has a `type` in its preamble:

- **Standards Track**: changes that affect most or all Ethereum implementations. Standards Track EIPs have a `category` of Core, Networking, or Interface. The template also lists ERC.
- **Meta**: process-related proposals.
- **Informational**: design issues or general guidance. These do not propose a new feature.

The lifecycle statuses are defined in `_data/statuses.yaml` and [EIP-1](EIPS/eip-1.md): Idea, Draft, Review, Last Call, Final, Stagnant, Withdrawn, and Living. Only Draft, Review, Last Call, Final, Stagnant, Withdrawn, and Living are accepted in an EIP's `status` header.

## Contributing

1. Read [EIP-1](EIPS/eip-1.md). It covers the process, required sections, and header format.
2. Discuss the idea first. EIP-1 recommends opening a thread on the [Ethereum Magicians forum](https://ethereum-magicians.org/).
3. Copy [`eip-template.md`](eip-template.md) and fill in the preamble and sections. The template comments suggest naming the file `eip-draft_<title_abbrev>.md` until an editor assigns a number.
4. Put any supporting files in `assets/eip-<number>/`. Link to them with relative paths. External links are generally not allowed in the body of an EIP, per the template.
5. Open a pull request against this repository. The pull request template describes the automatic merge criteria for some edits to existing Draft EIPs.

Refer to other proposals in the form `EIP-N` or `ERC-N`. The EIP validator flags other forms such as `EIPN` or `EIP N`.

## Checks run on pull requests

The continuous integration workflow (`.github/workflows/ci.yml`) runs on pull requests and includes these checks:

- **Jekyll build and HTML check**: builds the site with `jekyll build` and runs HTMLProofer on the output for links, images, scripts, and OpenGraph tags. External links are not checked in this step.
- **Link check**: checks links in modified Markdown files using `config/mlc_config.json`.
- **Spell check**: runs `codespell` on changed files, using `config/.codespell-whitelist`.
- **EIP validation**: runs `eipw` with the rules in `config/eipw.toml`. It checks preamble fields, required sections, status transitions, and reference formatting.
- **Markdown lint**: runs `markdownlint-cli2` on changed EIP Markdown files, using `config/.markdownlint.yaml`.

Other workflows handle deployment and housekeeping:

- `jekyll.yml` builds and deploys the site to GitHub Pages on pushes to `master`, and also runs on a schedule.
- `auto-review-bot.yml` and `auto-review-trigger.yml` run the EIP review bot, which reads `config/eip-editors.yml`.
- `auto-stagnate-bot.yml` runs a weekly job that marks EIPs as stagnant. `stale.yml` runs daily and marks inactive issues and pull requests as stale.
- `jekyll-label-bot.yml` applies labels to pull requests using `config/.jekyll-labels.yml`.
- `post-ci.yml` adds a comment and a `w-ci` label to a pull request when the CI run fails.

## Building the site locally

The site uses Jekyll with the `github-pages` gem set, as pinned in `Gemfile`. CI uses Ruby 3.1.

```sh
bundle install
bundle exec jekyll serve
```

The CI build first copies ERC files from `ethereum/ERCs` into the site. A local build from this repository alone does not include them.

The `Gemfile` also includes `html-proofer`, which the HTML check in CI uses.

`_config.yml` excludes `README.md` from the Jekyll build, so this file is not published on the site.

## License

The content of this repository is released under [CC0 1.0 Universal](LICENSE.md). Each EIP's copyright section, as required by EIP-1, waives copyright and related rights through CC0.

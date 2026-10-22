# Ethereum Improvement Proposals (EIPs)

This repository contains the text of Ethereum Improvement Proposals (EIPs): design documents that describe new features, standards, processes, or general information for the Ethereum community. Each proposal is a Markdown file maintained in a versioned repository, so its revision history serves as a record of how the proposal changed. The repository also builds a static website from these files.

## Overview

According to `EIPS/eip-1.md`, an EIP is "a design document providing information to the Ethereum community, or describing a new feature for Ethereum or its processes or environment." EIP-1 defines three types of proposal:

- **Standards Track**: changes that affect most or all Ethereum implementations, such as network protocol changes, block or transaction validity rules, or application standards. Standards Track EIPs have the categories `Core`, `Networking`, `Interface`, or `ERC`.
- **Meta**: proposals that describe or change a process surrounding Ethereum, such as procedures, guidelines, or development tooling.
- **Informational**: proposals that describe a design issue or provide general guidelines, without proposing a new feature.

EIP-1 also defines these lifecycle statuses: `Idea`, `Draft`, `Review`, `Last Call`, `Final`, `Stagnant`, `Withdrawn`, and `Living`. The `_data/statuses.yaml` file in this repository is consistent with that status vocabulary.

Some proposals in the repository have been moved. For example, `EIPS/eip-1046.md` contains only front matter and the sentence "This file was moved to https://github.com/ethereum/ercs/blob/master/ERCS/erc-1046.md". The pull request template also states that ERC-related pull requests now occur in the `ethereum/ercs` repository.

## Repository Contents

| Path | Purpose |
|---|---|
| `EIPS/` | Markdown source for each EIP, named `eip-N.md` |
| `assets/eip-N/` | Images, diagrams, test vectors, and supporting files for each EIP |
| `eip-template.md` | Template for new proposals |
| `LICENSE.md` | CC0 1.0 Universal license text |
| `_config.yml`, `Gemfile`, `Gemfile.lock` | Jekyll site configuration and Ruby dependencies |
| `_layouts/`, `_includes/`, `_data/` | Jekyll layouts, partials, and data files |
| `index.html`, `core.html`, `erc.html`, `networking.html`, `interface.html`, `meta.html`, `informational.html`, `all.html` | Website index pages by category or type |
| `rss/` | RSS feeds, including `all.xml`, `erc.xml`, `last-call.xml`, and `nonerc.xml` |
| `404.html`, `CNAME` | Site error page and custom domain file |
| `config/` | Linting, validation, editor, and label configuration |
| `.github/` | Workflows, issue and pull request templates, contributor guidance, and ownership |

## Setup

The site is a Jekyll project, and its Ruby dependencies are declared in `Gemfile` and pinned in `Gemfile.lock`. To build or preview the site locally, install Ruby and Bundler, then install the dependencies from the repository root with `bundle install`. Jekyll then builds the site from the configuration in `_config.yml`.

The repository also includes a `.gitattributes` file and a `.gitignore` file. The supplied files do not show their contents, so this README does not describe specific rules they define.

## Usage

### Reading EIPs

Browse the Markdown files in `EIPS/`, or use the generated website and RSS feeds. Each EIP begins with a YAML front-matter preamble that includes its number, title, status, type, author, and creation date. Optional fields include `category`, `requires`, `discussions-to`, and `last-call-deadline`.

### Writing a new EIP

Follow these steps, based on EIP-1 and the template:

1. Discuss the idea first. EIP-1 recommends opening a thread on the [Ethereum Magicians forum](https://ethereum-magicians.org/) before writing a formal EIP.
2. Copy `eip-template.md` and fill in the preamble. Titles should be a few words, and descriptions should be one short sentence. EIP-1 limits titles to 44 characters and descriptions to 140 characters, and neither should include the EIP number.
3. Use an abbreviated draft filename. The template says to use `eip-draft_title_abbrev.md`. An editor assigns the final EIP number.
4. Include the required sections. EIP-1 lists Abstract, Specification, Rationale, Security Considerations, and Copyright as required. Motivation, Backwards Compatibility, Test Cases, and Reference Implementation are optional in some cases. Core proposals that affect consensus need test cases.
5. Follow the Copyright wording. EIP-1 requires the line `Copyright and related rights waived via [CC0](../LICENSE.md).`
6. Use RFC 2119 and RFC 8174 key words where appropriate, and insert the standard sentence at the beginning of the Specification section.
7. Put supporting files in `assets/eip-N/`, and link to them with relative paths such as `../assets/eip-1/image.png`.
8. Open a pull request using the repository's template.

### Linking rules

EIP-1 says external links generally should not be included, because external resources may change or disappear. Permitted exceptions include specific Ethereum specification repositories, W3C recommendations, WHATWG snapshots, IETF RFCs, and some other sources. In most of these cases, the URL must be pinned to a specific commit or dated snapshot. Links to other EIPs should use relative paths, such as `./eip-1.md`, and the first reference to an EIP should be a link.

### Pull requests and issues

The pull request template describes an automated merge bot. According to the template, the bot may merge a pull request immediately if it edits only existing draft proposals, the build passes, and the contributor's GitHub username or email appears in the `author` header. The issue templates direct users to open pull requests for drafts and issues for early discussion.

## Configuration

The `config/` directory contains the following files:

- `.codespell-whitelist`: words that the spell checker should accept.
- `.markdownlint.yaml`: Markdown linting rules.
- `eipw.toml`: configuration for the EIP validation tool.
- `eip-editors.yml`: the list of EIP editors.
- `mlc_config.json`: configuration for a Markdown link checker.
- `.jekyll-labels.yml`: label configuration used by a Jekyll-related bot.

The supplied files do not include the contents of these configuration files, so their specific settings are not documented here.

The `_config.yml` file configures the Jekyll site, and `_data/statuses.yaml` supplies status data. The `CNAME` file indicates a custom domain for the published site.

Dependency updates are managed by Renovate through `.github/renovate.json`. Ownership of files is defined in `.github/CODEOWNERS`.

## Development

### Contributor guidance

`.github/CONTRIBUTING.md` points contributors to EIP-1 for guidelines. The contributing and issue guidance in `.github/ISSUE_TEMPLATE.md` describes the expected path from an idea, to discussion, to a draft pull request. EIP-1 states that each EIP needs a champion, also called the author, who writes the proposal, shepherds discussion, and builds consensus.

### Editors

EIP-1 lists the current EIP editors and emeritus editors. It also says that people who want to become editors should consult EIP-5069. Editors check proposals for readiness, title accuracy, language, and markup, and they assign EIP numbers and merge pull requests. EIP-1 states that editors do not judge the technical merit of proposals.

### Automation

The `.github/workflows/` directory contains the following workflows:

- `ci.yml` and `post-ci.yml`: continuous integration tasks.
- `jekyll.yml`: Jekyll site build.
- `jekyll-label-bot.yml`: labeling related to the site.
- `auto-review-bot.yml` and `auto-review-trigger.yml`: review automation.
- `auto-stagnate-bot.yml` and `stale.yml`: handling inactive proposals.

EIP-1 says that a Draft, Review, or Last Call proposal that is inactive for six months or more moves to `Stagnant`, and its authors and editors are notified of this status change. The names of the stale and stagnation workflows suggest they implement this rule, but the workflow contents were not supplied.

Repository hygiene files include `.gitattributes`, `.gitignore`, and `.github/PULL_REQUEST_TEMPLATE.md`.

## Testing and Validation

The supplied files do not show a general test command for the whole repository. Validation appears in several forms:

- **Continuous integration** runs through the workflows in `.github/workflows/`. The contents of `ci.yml` and `post-ci.yml` are not supplied.
- **Document linting and checks** are configured through `.markdownlint.yaml`, `.codespell-whitelist`, `eipw.toml`, and `mlc_config.json`.
- **Proposal-specific tests** are included in some `assets/` folders. Examples include `assets/eip-4881/test_deposit_snapshot.py`, `assets/eip-6475/tests.py`, `assets/eip-7495/tests.py`, and `assets/eip-7932/test_cases/generate_test_cases.py`. These files support individual proposals and are not a repository-wide suite.
- **Test vectors** are provided as data files for some proposals, such as `assets/eip-1057/test-vectors.md` and the JSON files in `assets/eip-2537/`.

To validate a proposal you have written, check that its front matter is complete, that it follows the template, that its links match the rules in EIP-1, and that its supporting files are in the correct `assets/eip-N/` directory.

## License

The repository content is released under the **Creative Commons CC0 1.0 Universal** public domain dedication, as stated in `LICENSE.md`. According to that file, the author waives copyright and related rights to the extent permitted by law. The license also disclaims warranties and states that Creative Commons is not a party to the document.

EIP-1 requires each EIP to carry the CC0 copyright waiver line. The CC0 waiver applies to the proposal text, and the document notes that some related materials keep their own licenses. For example, the reference ProgPoW mining implementation linked from `EIPS/eip-1057.md` is described there as a derivative of ethminer and retains the GPL license.

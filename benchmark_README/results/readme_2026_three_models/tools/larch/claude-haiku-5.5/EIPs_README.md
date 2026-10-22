# EIPs-et8th4j6

> **Note:** This README was written from the file listing alone, not from the file contents. The structure and conventions described below are inferred from file names and match the upstream [ethereum/EIPs](https://github.com/ethereum/EIPs) repository. Verify details against the actual source before relying on them.

## Overview

This repository is a snapshot of the Ethereum Improvement Proposals (EIPs) collection, along with the tooling that renders, validates, and publishes them. It contains:

- **The proposals themselves**: several hundred `eip-*.md` and `erc-*` documents covering Ethereum protocol changes, application-layer standards, and process documents.
- **Generated indexes and feeds** in HTML and XML, used for the website and for tooling.
- **A Jekyll-based static site** (layouts, includes, styles, and configuration) that renders the proposals into a browsable website.
- **Supporting assets** for individual proposals: diagrams, PDFs of research papers, test vectors, JSON fixtures, and reference code in several languages.
- **Configuration** for linting, editor permissions, and link checking.

Although the project name suggests a Python project, the repository is primarily a documentation repository. Python is used for a number of helper and analysis scripts, but the bulk of the content is Markdown.

## Repository Structure

The listing is flat, so the layout below groups files by role rather than by directory.

### 1. EIP documents

| Pattern | Description |
|---|---|
| `eip-N.md` | Individual Ethereum Improvement Proposals, numbered from 1 upward |
| `erc-N.md` | Application-level standards (ERCs), which are EIPs in the "ERC" category |
| `eip-template.md` / `template-eip.md` | Templates for authoring new proposals |
| `eip-editors.yml` | List of EIP editors and their GitHub handles |

Examples of notable proposals in this snapshot:

- **Process:** `eip-1.md` (EIP purpose and guidelines), `eip-2.md`, `eip-3.md`
- **Core protocol:** `eip-155.md` (replay protection), `eip-170.md` (contract code size limit), `eip-1559.md` (fee market), `eip-2930.md`, `eip-4844.md` (blob transactions), `eip-7702.md`, `eip-7002.md`, `eip-6110.md`
- **Networking:** `eip-2124.md` (fork identifiers), `eip-778.md`-style node records
- **Interface and signing:** `eip-712.md` (typed structured data), `eip-1193.md` (provider API), `eip-155.md`
- **Application standards:** `eip-20.md` (ERC-20 tokens), `eip-721.md` (ERC-721 NFTs), `eip-1155.md` (multi-token standard), `eip-165.md` (interface detection), `eip-4337.md` (account abstraction), `eip-137.md` (ENS)

Many EIPs also carry a status (Draft, Review, Last Call, Final, Stagnant, Withdrawn, Living) tracked in `statuses.yaml`.

### 2. Generated indexes and feeds

These files are produced by the build pipeline from the EIP front matter. Avoid editing them by hand.

| File | Purpose |
|---|---|
| `all.xml`, `all.html` | Index of all proposals |
| `erc.xml`, `erc.html` | ERC-category proposals |
| `nonerc.xml`, `nonerc-last-call.xml` | Non-ERC proposals (all and in Last Call) |
| `last-call.xml`, `erc-last-call.xml` | Proposals currently in Last Call |
| `eip.html` | Main EIP index page |
| `eiptable.html`, `eipnums.html` | Tabular and numeric index views |
| `core.html`, `networking.html`, `interface.html`, `informational.html`, `meta.html` | Per-category pages |

### 3. Website (Jekyll)

| File | Purpose |
|---|---|
| `_config.yml` | Jekyll configuration |
| `Gemfile`, `Gemfile.lock` | Ruby dependencies for building the site |
| `header.html`, `head.html`, `toc.html`, `social.html`, `authorlist.html`, `anchor_headings.html` | Page partials and includes |
| `style.scss`, `override.css` | Styles |
| `index.html`, `404.html`, `CNAME` | Site entry point, error page, and custom domain |

### 4. Validation and tooling configuration

| File | Purpose |
|---|---|
| `eipw.toml` | Configuration for the EIP linter (`eipw`), which checks front matter and formatting |
| `mlc_config.json` | Configuration for the markdown link checker |
| `eip-editors.yml` | Editor roster used by automation |
| `semver.md` | Versioning guidance |

### 5. Assets and supporting material

Each proposal may have a companion directory of assets. Notable examples:

- **Diagrams and images:** `diagram1.png`, `diagram2.png`, `base_fee_1.png`, `degradation.png`, `walletconnect-flow.png`, `tree_structure.png`, and many others
- **Test vectors:** `test-vectors.md`, `test-vectors-0.9.3.json`, `test_vectors.txt`, and the `fail-*_bls.json` / `*_bls.json` files for BLS12-381 precompiles (EIP-2537)
- **Test cases:** `test_cases.yaml`, `test-cases.md`, `transactions.json`, `precompile.json`
- **Research papers (PDF):** Casper, GHOST, Fraud and Data Availability Proofs, Poseidon hash security analyses, NFS factoring papers, `TR1559.pdf`, and `ef-Discouragement-Attacks.pdf`
- **Gas analysis:** `gas-cost-estimator*.pdf`, `final_gas_schedule_comparison.csv`, `gas_and_calldata_sample.csv`, `fee_analysis.md`
- **Patches:** `0001-unlimit-code-size.patch`, `tests.patch`, `remerkleable.patch`, `geth.diff`

### 6. Reference code

Assets include code in several languages:

- **Python:** `eip_4881.py`, `deposit_snapshot.py`, `test_deposit_snapshot.py`, `eth2_ws_calc.py`, `stable_container.py`, `ssz_types.py`, `rlp_types.py`, `tx_hashes.py`, `convert.py`, `convert_tests.py`, `generate_test_cases.py`, `progressive.py`, `optional.py`, `tests.py`
- **Solidity:** `ERC1155.sol`, `ERC1155WithTotals.sol`, `IERC1155.sol`, `Salary.sol`, `SalaryWithDAO.sol`, `BaseLock.sol`, `Extsload.sol`, `Example.sol`, and others
- **Go:** `decimal_float.go`, `decimal_float_test.go`, `uint256_wrapped.go`, `gasEVMPlusEmulate.go`
- **Yul:** `BlackScholes.yul`, `Neuron.yul`
- **JavaScript:** `Example.js`

Treat these as illustrative reference implementations, not production code. Check each one's license and test status before reuse.

## Getting Started

### Prerequisites

- Git
- Ruby and Bundler (for the Jekyll site)
- Python 3.8+ (for the helper scripts)
- Optional: Node.js or Go if you want to run the associated reference code

### Clone

```bash
git clone <repository-url> EIPs-et8th4j6
cd EIPs-et8th4j6
```

### Run the website locally

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000`.

### Run Python helpers

Install dependencies as required by each script (none are declared at the top level in this listing). For example:

```bash
python3 eip_4881.py
python3 test_deposit_snapshot.py
```

Check each script's header or imports before running it.

## Writing or Updating an EIP

1. Copy `eip-template.md` (or `template-eip.md`) to a new file named `eip-<number>.md` or `erc-<number>.md`.
2. Fill in the YAML front matter: `eip`, `title`, `description`, `author`, `status`, `type`, `category` (where applicable), `created`, and `requires` as needed.
3. Write the specification using RFC 2119 keywords (MUST, SHOULD, MAY) where normative language is needed.
4. Place any supporting images, data, or test vectors in an appropriately named asset location.
5. Run the linter (`eipw`) using the settings in `eipw.toml` and fix any reported issues.
6. Check links with the configuration in `mlc_config.json`.
7. Open a pull request.

Refer to `eip-1.md` for the full process, including the status lifecycle and the roles of editors.

## Proposal Lifecycle

Proposals move through these stages, as described in EIP-1:

- **Idea / Draft:** Initial work, open to discussion
- **Review:** Author believes the proposal is complete and seeks peer review
- **Last Call:** Final review period with a deadline; changes restart the clock
- **Final:** Accepted and implemented as a standard
- **Living:** Continuously updated, with no finality
- **Stagnant:** Inactive for an extended period
- **Withdrawn:** Author has withdrawn the proposal

Current statuses are tracked in `statuses.yaml` and reflected in the generated indexes.

## Categories and Types

- **Standards Track:** Core, Networking, Interface, and ERC subcategories
- **Meta:** Changes to the process or to other EIPs
- **Informational:** General guidance, design rationale, or background without a normative requirement

## Contributing

- Read `eip-1.md` before opening a proposal.
- Keep proposals focused on a single concern.
- Use the templates and linter to avoid common formatting errors.
- Discuss substantive changes on the relevant forum or issue tracker before submitting a pull request.
- Respect the editor process; editors merge changes and assign numbers.

## License

Most EIP content is released under **CC0 1.0 Universal** (public domain dedication). Code samples and third-party material in the assets (research PDFs, papers, and some reference code) remain under their own licenses. See `LICENSE.md` for the repository license and check individual files for additional terms.

## Caveats

- The EIP number sequence has gaps; not all numbers correspond to files in this snapshot.
- Generated files (`*.xml`, `*.html` indexes) may be stale relative to the Markdown sources until the build is re-run.
- Reference code and test vectors have not been verified in this README. Run their associated tests before using them.
- The project name `EIPs-et8th4j6` does not appear to correspond to any upstream project; it appears to be a local or renamed copy.

## Acknowledgements

The EIP process and its authors, editors, reviewers, and the wider Ethereum community who produce and discuss these proposals.

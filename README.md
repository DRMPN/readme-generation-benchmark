# README Generation Benchmark

This repository contains a benchmark runner for comparing five README-generation methods on 48 GitHub repositories at pinned commits. The dataset has 30 repositories labeled `Common` and 18 labeled `Scientific`. Each enabled method runs against each of three configured generation models, for up to 720 generation cells (5 methods × 3 models × 48 repositories), followed by GEval scoring. A configured experiment is not evidence that every cell completed; consult its status and coverage files before drawing conclusions.

## What is compared

The notebook enables these methods by default:

| Method | Runner behavior |
| --- | --- |
| `baseline` | Sends a fixed prompt, a deterministic repository file tree, and prioritized text files directly to the selected model. The complete prompt is capped at 64,000 `cl100k_base` tokens. |
| `osa` | Runs OSA's advanced README workflow with the selected model routed through OpenRouter. |
| `readmeready` | Indexes the repository with ReadMeReady and asks it to generate a README with configured sections. Its embedding model is `sentence-transformers/all-mpnet-base-v2`. |
| `larch` | Builds context using LArch's `file_names` context creator, then generates and post-processes a README. |
| `opencode` | Runs the OpenCode CLI with a README-writing agent. Shell, `webfetch`, and task permissions were denied, but the retained logs show that `execute` could fetch upstream pages in three GLM sessions. |

Generation uses these OpenRouter model IDs by default:

- `openai/gpt-6-luna`
- `anthropic/claude-haiku-5.5`
- `z-ai/glm-5.3-flash`

The scoring phase uses `openai/gpt-6-sol` through DeepEval GEval. The evaluator compares each generated README (with a JSON representation of the repository structure) as the actual output against the repository's original README as the expected output. Its criteria cover consistency with the provided structure, project overview, setup, examples, dependencies, and readability. GEval is an LLM-based evaluator, not a guarantee of factual correctness.

## Requirements and installation

The provided installer targets Linux, requires Python 3.12 and Git, and supports the OpenCode binary on Linux x86_64 or arm64. From the repository root:

```bash
bash scripts/install_tools.sh
```

The installer creates `benchmark_README/.venv`, checks out pinned upstream source revisions into `.tools/src/`, creates separate virtual environments for OSA, LArch, and ReadMeReady under `.tools/venvs/`, installs the Linux OpenCode 2 CLI under `.tools/opencode/`, and runs the verification script. Tool versions, source URLs, and commit SHAs are recorded in [`benchmark_README/tool_versions.json`](benchmark_README/tool_versions.json). The checked-in `OSA/`, `larch_eval/`, and `ReadMeReady_eval/` directories are repository copies; the benchmark installer and runners use the pinned sources under `.tools/src/`.

The pinned ReadMeReady checkout receives the tracked [local patch](scripts/patches/readmeready-output-paths.patch) during installation. It keeps generated summaries separate from input files, handles UTF-16 source text, and uses the configured concurrency limit for independent file and folder summaries. OpenCode runs in a disposable clone and receives that clone as its working directory.

Set the OpenRouter key in a root-level `.env` file:

```dotenv
OPENROUTER_API_KEY=your-key
```

The key is needed for generation and scoring. `GIT_TOKEN` or `GITHUB_TOKEN` is optional and can be used for private GitHub repositories or to address GitHub rate limits. The verification script reports whether the OpenRouter key is present; it does not print its value.

Check the installation and key presence with:

```bash
python3 scripts/verify_install.py
```

This is a read-only startup/configuration check. It imports the tools, checks their pinned revisions and command-line startup, checks benchmark imports and OpenRouter configurations, and checks for the API key. It does not generate or score READMEs.

## Run the experiment

Open [`benchmark_README/README_benchmark.ipynb`](benchmark_README/README_benchmark.ipynb) using the `benchmark_README/.venv` Python interpreter. The notebook's configuration cell selects the phase, methods, models, run name, and optional repository limit. Run each phase separately and in order:

1. **`prepare`** (the default): fetches the dataset repositories at their specified commits, saves each root README as the evaluation reference, and creates a local sanitized Git snapshot without that README. It also records repository structure and preparation status. This phase makes no model calls.
2. **`generate`**: runs each enabled method/model/repository combination. Every method gets a fresh isolated worktree of the sanitized snapshot, so it does not receive the original README or another method's generated files.
3. **`score`**: uses GEval to score successful generated outputs against their original READMEs and the recorded repository structures.
4. **`report`**: writes the aggregate tables and coverage information without making model calls.

Change only the `phase` value in the notebook configuration between runs. The default configuration enables all five methods, uses all three models, and processes all repositories. The optional `limit_repos` setting can limit work during a run; reports require three distinct models and all five methods.

After preparation, the resumable command `benchmark_README/.venv/bin/python scripts/run_full_benchmark.py` runs the three model branches concurrently, scores successful outputs as they become available, and exports the final table. It keeps progress in the same run directory.

The secondary G-Eval pass with `z-ai/glm-5.3-flash` is complete: it scored the
same 691 retained outputs without regenerating them. Its [paired table and
coverage](benchmark_README/results/readme_2026_three_models_glm_judge/evaluation/results.md)
and [paper discussion](benchmark_README/paper/readme_experiment.md) use the same
rubric and provenance exclusions as the GPT-6 Sol run. To inspect saved score
coverage without an API call, use `benchmark_README/.venv/bin/python scripts/run_glm_judge.py --status`; `--run` resumes any missing scores.

The standalone preparation helper can materialize the default run's inputs without model calls:

```bash
python3 scripts/prepare_inputs.py
```

The experiment name and default output location are `readme_2026_three_models` and `benchmark_README/results/readme_2026_three_models/`. The compact record of this completed run is published under [`benchmark_README/results/`](benchmark_README/results/README.md); downloaded source trees and temporary workspaces remain local. Empty generated files are rejected; other formatting differences are left for GEval to assess. Preparation, tool, and scoring status are recorded in `preflight_status.csv`, `tool_status.csv`, and `evaluation/eval_rows.csv`, respectively.

## Scoring and reports

The report's mean scores use **complete cases**: a repository is included in the cross-method means only when all 15 method/model combinations have valid scores in the 0–1 range, a successful final generation status, a retained output file, and no audit-confirmed upstream reference retrieval. The completed run has 34 such repositories (22 Common, 12 Scientific). The excluded cases and supporting logs are recorded in [`reference_access.csv`](benchmark_README/results/readme_2026_three_models/evaluation/reference_access.csv). The report also provides coverage counts so incomplete runs are visible; it does not fill in missing scores. API cost totals are reported only when numeric cost metadata is present for baseline generation or judge calls. Costs for other generation tools are not inferred.

Files written under `benchmark_README/results/<run-name>/evaluation/` include:

- `eval_rows.csv` — per-output GEval scores, reasons, and recorded judge usage.
- `complete_case_summary.csv` — method/model means over the common complete repository set, by repository group.
- `coverage.csv` — complete repositories versus total repositories by group.
- `cell_coverage.csv` — valid-score counts per group, model, and method.
- `results.md` — a Markdown summary table and recorded cost/coverage information.
- `final_summary.csv` — per-method/model aggregate rows from scoring, before complete-case filtering.
- `reference_access.csv` — audited upstream README retrievals excluded from the paired table.

Generation outputs are stored under `tools/<method>/<model-label>/`; logs and preparation artifacts are also kept in the run directory. Older run directories are not overwritten by default; change the notebook's reset options deliberately if you intend to replace existing artifacts.

## Repository layout

- `benchmark_README/README_benchmark.ipynb` — phase-based experiment notebook.
- `benchmark_README/src/` — repository preparation, generation runners, the direct baseline, GEval evaluation, and reporting code.
- `benchmark_README/data/repo_list.csv` — repository URLs, pinned commit SHAs, dates, names, and group labels.
- `benchmark_README/paper/readme_experiment.md` — manuscript-ready methods, results, limitations, prompts, repository list, and cost assumptions.
- `benchmark_README/tool_versions.json` — pinned upstream tool revisions and OpenCode version.
- `benchmark_README/requirements*.txt` — benchmark and ReadMeReady environment dependencies.
- `scripts/install_tools.sh` — Linux environment and pinned-tool installer.
- `scripts/verify_install.py` — read-only installation checks.
- `scripts/prepare_inputs.py` — standalone input preparation helper.
- `OSA/`, `larch_eval/`, `ReadMeReady_eval/` — checked-in project copies, separate from the pinned `.tools/src/` sources used by the benchmark.

## License

The benchmark repository is distributed under the [MIT License](LICENSE). The compared tools and dataset repositories retain their own licenses and terms.

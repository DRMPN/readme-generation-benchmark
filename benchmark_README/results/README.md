# Published README benchmark record

The `readme_2026_three_models/` directory contains the compact record for the
48-repository, three-model, five-method experiment. It contains 691 retained
generated READMEs, the original README references, 48 repository structures,
generation and scoring records, and run logs. The [paper section and appendix](../paper/readme_experiment.md)
describe the protocol and results; [the pinned dataset](../data/repo_list.csv)
identifies the source repository and commit for each reference.

The `readme_2026_three_models_glm_judge/` directory records a second G-Eval
pass over those same 691 generated READMEs, using `z-ai/glm-5.3-flash` as the
judge. Its `evaluation/` directory contains the 691 per-output scores and
reasons, paired means, and coverage; `run_manifest.json` identifies the source
run, `input_manifest.csv` hashes the reused source artifacts, and
`judge_run.log` records progress and retries. Generated READMEs and
reference files are shared with the primary run, so they are not duplicated
here. Table 2 of the paper section reports the paired GLM-judge means.

| Path | Contents |
| --- | --- |
| `evaluation/eval_rows.csv` | Raw per-output judge scores, reasons, and returned usage metadata; includes stale and malformed rows for audit. |
| `evaluation/reference_access.csv` | Three observed GLM/OpenCode retrievals of upstream README content, with paths to the supporting logs. |
| `evaluation/complete_case_summary.csv`, `coverage.csv`, `cell_coverage.csv`, `results.md` | Published paired means and coverage. The paired means use 34 repositories after provenance exclusions. Raw per-cell coverage still counts all valid, retained scores. |
| `tool_status.csv`, `preflight_status.csv` | Final generation state and pinned input-preparation state. |
| `tools/<method>/<model>/` | Retained generated README files; baseline JSON sidecars also contain generation usage metadata. |
| `original_readmes/`, `repo_structures/` | Reference READMEs and repository structures used by the judge. |
| `logs/`, `full_run*.log` | Per-cell and top-level execution logs, including unsuccessful attempts. |

The 6.7 GB of downloaded source repositories, sanitized local inputs, and
ReadMeReady intermediate workspaces are omitted. Their pinned revisions and
the input-preparation procedure are recorded in the dataset and code. The
three original READMEs mentioned in `reference_access.csv` remain in the raw
record; the published paired table excludes `ChatGLM-6B` and
`system-design-primer` because their OpenCode logs show remote reference
retrieval. `PyTorch-GAN` was already incomplete. No raw score or log was
deleted to make this adjustment.

The raw CSVs contain absolute paths from the machine that ran the experiment.
For browsing them, replace the prefix through `readme_2026_three_models/`
with this directory. The report exporter resolves these paths after a clone.
To reproduce the published table without model calls, install the benchmark
environment, then use the notebook's `report` phase. Use a new run name for a
new generation experiment so these published records remain intact.

The reference READMEs come from the pinned third-party repositories. Their
original licenses and attribution remain with those projects; the benchmark's
MIT license applies to the benchmark code.

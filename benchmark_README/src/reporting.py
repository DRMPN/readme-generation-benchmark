"""Complete-case README benchmark tables; never calls a model."""

import json
from pathlib import Path

import pandas as pd

METHODS = ("baseline", "readmeready", "larch", "osa", "opencode")
METHOD_LABELS = ("Base", "RR", "LArch", "OSA", "OC")
GROUPS = ("Common", "Scientific", "All")


def _artifact_path(recorded_path: str, run_dir: Path) -> Path:
    """Locate a recorded artifact after the public run is cloned elsewhere."""
    recorded = Path(str(recorded_path))
    if not recorded.is_absolute():
        return run_dir / recorded
    if recorded.is_file():
        return recorded
    try:
        suffix = recorded.parts[recorded.parts.index(run_dir.name) + 1:]
    except ValueError:
        return recorded
    return run_dir.joinpath(*suffix)


def export_table(repo_df: pd.DataFrame, paths, models: list[str], judge_model: str) -> dict:
    eval_path = paths.evaluation_dir / "eval_rows.csv"
    status_path = paths.experiment_dir / "tool_status.csv"
    if not eval_path.is_file() or not status_path.is_file():
        raise FileNotFoundError("Generation and GEval rows are required before reporting")
    evaluated = pd.read_csv(eval_path)
    statuses = pd.read_csv(status_path)
    expected = {(m, method) for m in models for method in METHODS}
    if len(models) != 3 or len(expected) != 15:
        raise ValueError("The report requires three distinct models and five methods")
    evaluated = evaluated[evaluated["judge_model"] == judge_model].copy()
    evaluated = evaluated[evaluated["model"].isin(models) & evaluated["tool"].isin(METHODS)]
    judge_rows = evaluated.copy()
    evaluated["score"] = pd.to_numeric(evaluated["score"], errors="coerce")
    evaluated = evaluated[evaluated["score"].between(0, 1, inclusive="both")]
    # A later failed generation attempt can remove an output while leaving its
    # earlier GEval row behind. Only report scores with a retained artifact.
    retained = statuses.loc[statuses["status"] == "done", ["repo_slug", "model", "tool", "output_path"]]
    retained = retained[retained["output_path"].map(
        lambda value: _artifact_path(value, paths.experiment_dir).is_file())]
    evaluated = evaluated.merge(retained[["repo_slug", "model", "tool"]],
                                on=["repo_slug", "model", "tool"], how="inner")
    evaluated = evaluated.drop_duplicates(["repo_slug", "model", "tool"], keep="last")
    # A generator can retrieve the reference from upstream even when the local
    # README is hidden. Audit-confirmed cases are excluded as whole repositories
    # so every reported method is averaged over the same source set.
    audit_path = paths.evaluation_dir / "reference_access.csv"
    excluded = set()
    if audit_path.is_file():
        audit = pd.read_csv(audit_path)
        excluded = set(audit.loc[audit["exclude_from_paired_table"].eq(1), "repo_slug"])
    labels = repo_df[["repo_slug", "repo_type"]].drop_duplicates()
    complete = []
    for slug in labels["repo_slug"]:
        subset = evaluated[evaluated["repo_slug"] == slug]
        if slug not in excluded and set(zip(subset["model"], subset["tool"])) == expected:
            complete.append(slug)
    complete_rows = evaluated[evaluated["repo_slug"].isin(complete)].merge(labels, on="repo_slug", suffixes=("", "_dataset"))
    complete_rows["repo_type"] = complete_rows["repo_type_dataset"]
    table_rows = []
    coverage_rows = []
    cell_coverage_rows = []
    for group in GROUPS:
        group_slugs = set(labels["repo_slug"] if group == "All" else labels.loc[labels["repo_type"] == group, "repo_slug"])
        selected = complete_rows[complete_rows["repo_slug"].isin(group_slugs)]
        valid_in_group = evaluated[evaluated["repo_slug"].isin(group_slugs)]
        coverage_rows.append({"repo_type": group, "total_repositories": len(group_slugs),
                              "complete_repositories": len(group_slugs & set(complete))})
        for model in models:
            for method in METHODS:
                scores = selected[(selected["model"] == model) & (selected["tool"] == method)]["score"]
                observed = valid_in_group[(valid_in_group["model"] == model) & (valid_in_group["tool"] == method)]
                cell_coverage_rows.append({"repo_type": group, "model": model, "tool": method,
                                           "valid_scores": len(observed), "total_repositories": len(group_slugs)})
                table_rows.append({"repo_type": group, "model": model, "tool": method,
                                   "mean_score": scores.mean() if len(scores) else float("nan"),
                                   "evaluated": len(scores)})
    summary = pd.DataFrame(table_rows)
    coverage = pd.DataFrame(coverage_rows)
    paths.evaluation_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(paths.evaluation_dir / "complete_case_summary.csv", index=False)
    coverage.to_csv(paths.evaluation_dir / "coverage.csv", index=False)
    pd.DataFrame(cell_coverage_rows).to_csv(paths.evaluation_dir / "cell_coverage.csv", index=False)
    headers = ["Repo type"] + [f"{model.split('/')[-1]} {label}" for model in models for label in METHOD_LABELS]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for group in GROUPS:
        cells = [group]
        group_rows = summary[summary["repo_type"] == group]
        for model in models:
            model_rows = group_rows[group_rows["model"] == model]
            best = model_rows["mean_score"].max()
            for method in METHODS:
                value = model_rows.loc[model_rows["tool"] == method, "mean_score"].iloc[0]
                cell = "—" if pd.isna(value) else f"{value:.2f}"
                if pd.notna(value) and value == best:
                    cell = f"**{cell}**"
                cells.append(cell)
        lines.append("| " + " | ".join(cells) + " |")
    lines += ["", f"GEval judge: `{judge_model}`. Means use the same complete repositories across all 15 cells.",
              f"Repositories with observed upstream-reference access are excluded from the paired means ({len(excluded)} flagged; see `reference_access.csv`).", "",
              "| Repo type | Complete / total |", "| --- | --- |"]
    for row in coverage.itertuples():
        lines.append(f"| {row.repo_type} | {row.complete_repositories} / {row.total_repositories} |")
    lines += ["", "Raw per-cell valid-score coverage, before provenance exclusions, is saved in `cell_coverage.csv`."]
    # API usage metadata is only counted where OpenRouter returned a numeric cost.
    baseline_usages = []
    for row in statuses.itertuples():
        meta = _artifact_path(row.output_path, paths.experiment_dir).with_suffix(".json")
        if row.tool == "baseline" and row.status == "done" and meta.is_file():
            usage = json.loads(meta.read_text(encoding="utf-8")).get("usage", {})
            baseline_usages.append(usage.get("cost"))
    judge_usages = []
    for raw in judge_rows.get("judge_usage", pd.Series(dtype=str)).dropna():
        for usage in json.loads(raw):
            judge_usages.append(usage.get("cost"))
    def cost_line(label, values):
        present = []
        for value in values:
            try:
                if value is not None:
                    present.append(float(value))
            except (TypeError, ValueError):
                pass
        return f"| {label} | {len(present)} / {len(values)} | ${sum(present):.4f} |" if present else f"| {label} | 0 / {len(values)} | unavailable |"
    lines += ["", "| Cost source | Priced calls / recorded calls | Recorded USD |", "| --- | --- | ---: |",
              cost_line("Baseline generation", baseline_usages), cost_line("GEval judge", judge_usages),
              "", "Other tools do not yet expose per-call costs in their output; no cost is inferred from token counts."]
    markdown = "\n".join(lines) + "\n"
    (paths.evaluation_dir / "results.md").write_text(markdown, encoding="utf-8")
    return {"complete_repositories": complete, "coverage": coverage, "summary": summary, "markdown": markdown}

"""Score retained README outputs with GLM 5.3 Flash in a separate run."""

import argparse
import csv
import hashlib
import json
import shutil
import sys
import time
import traceback
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "benchmark_README"))

from src.evaluation import evaluate_outputs  # noqa: E402
from src.notebook_utils import build_paths, load_env_file, read_repo_table  # noqa: E402
from src.reporting import export_table  # noqa: E402

SOURCE_NAME = "readme_2026_three_models"
TARGET_NAME = "readme_2026_three_models_glm_judge"
JUDGE_MODEL = "z-ai/glm-5.3-flash"
MODELS = ["openai/gpt-6-luna", "anthropic/claude-haiku-5.5", "z-ai/glm-5.3-flash"]
JUDGE = {"api": "openrouter", "model": JUDGE_MODEL, "base_url": "https://openrouter.ai/api/v1"}
EXPECTED_OUTPUTS = 691


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _link_source(target: Path, source_name: str, directory: str) -> None:
    expected = Path("..") / source_name / directory
    if target.is_symlink():
        if target.readlink() != expected:
            raise RuntimeError(f"Unexpected link target: {target}")
    elif target.exists():
        raise RuntimeError(f"Expected a source link at {target}")
    else:
        target.symlink_to(expected, target_is_directory=True)


def prepare() -> tuple:
    source = build_paths(SOURCE_NAME)
    target = build_paths(TARGET_NAME)
    status_source = source.experiment_dir / "tool_status.csv"
    if not status_source.is_file():
        raise FileNotFoundError(status_source)

    statuses = pd.read_csv(status_source)
    if len(statuses) != 720:
        raise RuntimeError(f"Expected 720 generation statuses, found {len(statuses)}")
    done = statuses[statuses["status"] == "done"]
    if len(done) != EXPECTED_OUTPUTS or not done["output_path"].map(lambda value: Path(value).is_file()).all():
        raise RuntimeError("The 691 retained source READMEs are not all available")

    target.experiment_dir.mkdir(parents=True, exist_ok=True)
    target.evaluation_dir.mkdir(parents=True, exist_ok=True)
    for directory in ("tools", "original_readmes", "repo_structures", "logs"):
        _link_source(target.experiment_dir / directory, SOURCE_NAME, directory)

    expected_manifest = {
        "source_run": SOURCE_NAME,
        "judge_run": TARGET_NAME,
        "judge_model": JUDGE_MODEL,
        "generation_reused": True,
        "retained_outputs": EXPECTED_OUTPUTS,
        "source_tool_status_sha256": _sha256(status_source),
    }
    manifest_path = target.experiment_dir / "run_manifest.json"
    if manifest_path.is_file():
        if json.loads(manifest_path.read_text(encoding="utf-8")) != expected_manifest:
            raise RuntimeError("Existing judge run has different source artifacts or configuration")
    else:
        manifest_path.write_text(json.dumps(expected_manifest, indent=2) + "\n", encoding="utf-8")

    for column in ("output_path", "log_path"):
        statuses[column] = statuses[column].map(
            lambda value: str(Path(value).relative_to(source.experiment_dir))
        )
    target_status = target.experiment_dir / "tool_status.csv"
    if target_status.is_file():
        existing = pd.read_csv(target_status)
        if not existing.equals(statuses):
            raise RuntimeError("Existing judge run has a different generation status snapshot")
    else:
        statuses.to_csv(target_status, index=False)

    for name in ("preflight_status.csv",):
        src = source.experiment_dir / name
        dst = target.experiment_dir / name
        if not dst.exists():
            shutil.copy2(src, dst)
    audit_source = source.evaluation_dir / "reference_access.csv"
    audit_target = target.evaluation_dir / "reference_access.csv"
    if not audit_target.exists():
        shutil.copy2(audit_source, audit_target)
    elif _sha256(audit_target) != _sha256(audit_source):
        raise RuntimeError("Reference-access audit differs from the source run")

    input_manifest = target.experiment_dir / "input_manifest.csv"
    if not input_manifest.exists():
        paths = [Path(value) for value in done["output_path"]]
        paths += sorted(source.original_readmes_dir.glob("*_original_README*"))
        paths += sorted(source.structures_dir.glob("*_struct.json"))
        with input_manifest.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(("source_relative_path", "sha256"))
            for path in paths:
                writer.writerow((str(path.relative_to(source.experiment_dir)), _sha256(path)))
    else:
        with input_manifest.open(newline="", encoding="utf-8") as stream:
            records = list(csv.DictReader(stream))
        if len(records) != EXPECTED_OUTPUTS + 48 + 48:
            raise RuntimeError("Incomplete input manifest")
        for record in records:
            path = source.experiment_dir / record["source_relative_path"]
            if not path.is_file() or _sha256(path) != record["sha256"]:
                raise RuntimeError(f"Source artifact changed: {path}")

    return source, target


def progress(target) -> tuple[int, float]:
    path = target.evaluation_dir / "eval_rows.csv"
    if not path.is_file():
        return 0, 0.0
    rows = pd.read_csv(path)
    scores = pd.to_numeric(rows.get("score"), errors="coerce")
    valid = rows[rows["judge_model"].eq(JUDGE_MODEL) & scores.between(0, 1)]
    count = len(valid.drop_duplicates(["tool", "model", "repo_slug"]))
    cost = 0.0
    for usage_text in rows.get("judge_usage", []):
        if isinstance(usage_text, str):
            try:
                cost += sum(float(item.get("cost") or 0) for item in json.loads(usage_text))
            except (ValueError, TypeError):
                pass
    return count, cost


def run(max_new_rows: int | None, max_passes: int) -> None:
    load_env_file()
    _, target = prepare()
    experiment = {"judge": JUDGE}
    for pass_number in range(1, max_passes + 1):
        print(f"Pass {pass_number}/{max_passes} started at {datetime.now(timezone.utc).isoformat()}", flush=True)
        evaluate_outputs(target, experiment, max_new_rows=max_new_rows)
        count, cost = progress(target)
        print(f"Progress: {count}/{EXPECTED_OUTPUTS} valid scores; recorded judge cost ${cost:.4f}", flush=True)
        if max_new_rows is not None or count == EXPECTED_OUTPUTS:
            break
        if pass_number < max_passes:
            time.sleep(30)
    if max_new_rows is None:
        result = export_table(read_repo_table("data/repo_list.csv"), target, MODELS, JUDGE_MODEL)
        print(f"Complete paired repositories: {len(result['complete_repositories'])}/48", flush=True)
        count, _ = progress(target)
        if count != EXPECTED_OUTPUTS:
            raise RuntimeError(f"Only {count}/{EXPECTED_OUTPUTS} retained outputs received valid scores")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--smoke", action="store_true", help="score one output and checkpoint it")
    group.add_argument("--run", action="store_true", help="resume all remaining outputs")
    group.add_argument("--status", action="store_true", help="show saved progress without API calls")
    args = parser.parse_args()
    target = build_paths(TARGET_NAME)
    if args.status:
        count, cost = progress(target)
        print(f"GLM judge: {count}/{EXPECTED_OUTPUTS} valid scores; recorded judge cost ${cost:.4f}")
    elif args.smoke:
        run(max_new_rows=1, max_passes=1)
    else:
        target.experiment_dir.mkdir(parents=True, exist_ok=True)
        with (target.experiment_dir / "judge_run.log").open("a", buffering=1, encoding="utf-8") as log:
            with redirect_stdout(log), redirect_stderr(log):
                try:
                    run(max_new_rows=None, max_passes=3)
                except Exception:
                    traceback.print_exc()
                    raise


if __name__ == "__main__":
    main()

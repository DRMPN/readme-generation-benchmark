"""Materialize pinned, README-free repository snapshots. No model calls."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "benchmark_README"))
from src.notebook_utils import build_paths, ensure_directories, load_env_file, prepare_repositories, read_repo_table

load_env_file()
paths = build_paths("readme_2026_three_models")
ensure_directories(paths)
repos = read_repo_table("data/repo_list.csv")
result = prepare_repositories(repos, paths)
failed = result[result["status"] != "done"]
print(f"Prepared {len(result) - len(failed)} / {len(result)} pinned inputs")
if not failed.empty:
    print("Failed slugs:", ", ".join(failed["repo_slug"]))
    raise SystemExit(1)

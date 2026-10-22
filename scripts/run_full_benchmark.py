"""Resume the prepared 48-repository README benchmark, then score and report."""

import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "benchmark_README"))

from src.evaluation import evaluate_outputs  # noqa: E402
from src.notebook_utils import build_paths, load_env_file, read_repo_table  # noqa: E402
from src.reporting import export_table  # noqa: E402
from src.tool_runners import GENERATORS, run_selected_tools  # noqa: E402

RUN_NAME = "readme_2026_three_models"
MODELS = ["openai/gpt-6-luna", "anthropic/claude-haiku-5.5", "z-ai/glm-5.3-flash"]
JUDGE = {"api": "openrouter", "model": "openai/gpt-6-sol",
         "base_url": "https://openrouter.ai/api/v1"}


def main() -> None:
    load_env_file()
    paths = build_paths(RUN_NAME)
    repos = read_repo_table("data/repo_list.csv")
    if len(repos) != 48 or any(not (paths.inputs_dir / slug / ".git").is_dir()
                                for slug in repos["repo_slug"]):
        raise RuntimeError("All 48 sanitized inputs must be prepared before the full run")
    if not (paths.original_readmes_dir.is_dir() and paths.structures_dir.is_dir()):
        raise RuntimeError("Original READMEs and repository structures are required for GEval")
    experiment = {"judge": JUDGE, "models": MODELS,
                  "tools": {name: {"enabled": True} for name in GENERATORS}}

    print(f"Resuming {len(repos)} repositories, {len(MODELS) * len(GENERATORS)} cells each", flush=True)
    with ThreadPoolExecutor(max_workers=len(MODELS)) as pool:
        futures = [pool.submit(run_selected_tools, repos, paths,
                               {**experiment, "models": [model]}) for model in MODELS]
        while not all(future.done() for future in futures):
            if (paths.experiment_dir / "tool_status.csv").is_file():
                evaluate_outputs(paths, experiment)
            if not all(future.done() for future in futures):
                time.sleep(30)
        for future in futures:
            future.result()

    evaluate_outputs(paths, experiment)
    result = export_table(repos, paths, MODELS, JUDGE["model"])
    print(result["markdown"], flush=True)
    print(f"Complete repositories: {len(result['complete_repositories'])} / {len(repos)}", flush=True)


if __name__ == "__main__":
    main()

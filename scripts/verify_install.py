"""Read-only preparation checks. No repository generation or model requests."""
import json
import ast
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSIONS = json.loads((ROOT / "benchmark_README" / "tool_versions.json").read_text())


def check(cmd, *, env=None):
    result = subprocess.run([str(x) for x in cmd], cwd=ROOT, env=env,
                            capture_output=True, text=True, timeout=90)
    if result.returncode:
        raise RuntimeError(f"Startup failed: {cmd[0]} ({result.returncode})\n{result.stderr[-500:]}")
    return result.stdout.strip()


for name, module in [("osa", "osa_tool.run"), ("larch", "larch"),
                     ("readmeready", "readme_ready.index.index")]:
    source_name = {"osa": "OSA", "larch": "larch", "readmeready": "ReadMeReady"}[name]
    source = ROOT / ".tools" / "src" / source_name
    sha = check(["git", "-C", source, "rev-parse", "HEAD"])
    assert sha == VERSIONS[name]["commit"], f"{name} commit mismatch"
    if name == "readmeready":
        patch = ROOT / VERSIONS[name]["local_patch"]
        check(["git", "-C", source, "apply", "--reverse", "--check", patch])
    py = ROOT / ".tools" / "venvs" / name / "bin" / "python"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(source)
    if name == "readmeready":
        env["OPENAI_API_KEY"] = "placeholder"
    check([py, "-c", f"import {module}; print('ok')"], env=env)
    if name == "osa":
        check([py, "-m", "osa_tool.run", "--help"], env=env)
        check([py, "-c", "from osa_tool.config.settings import ConfigManager; ConfigManager(); print('config ok')"], env=env)
    elif name == "larch":
        check([ROOT / ".tools" / "venvs" / "larch" / "bin" / "larch", "--help"], env=env)
    elif name == "readmeready":
        # Upstream's CLI is interactive and has no --help action. Import its
        # entry point and the modules the adapter invokes without prompting.
        check([py, "-c", "import readme_ready.__main__; import readme_ready.index.index; import readme_ready.query.query"], env=env)
    mode = "import/entrypoint OK" if name == "readmeready" else "import/CLI startup OK"
    print(f"{name}: {VERSIONS[name]['version']} {sha[:12]} {mode}")

opencode = ROOT / ".tools" / "opencode" / "opencode"
opencode_env = {**os.environ, "XDG_DATA_HOME": str(ROOT / ".tools" / "opencode_state" / "data"),
                "XDG_CONFIG_HOME": str(ROOT / ".tools" / "opencode_state" / "config"),
                "XDG_CACHE_HOME": str(ROOT / ".tools" / "opencode_state" / "cache")}
version = check([opencode, "--version"], env=opencode_env)
assert VERSIONS["opencode_2"]["version"] in version, version
check([opencode, "run", "--help"], env=opencode_env)
benchmark = ROOT / "benchmark_README" / ".venv" / "bin" / "python"
models = ("openai/gpt-6-luna", "anthropic/claude-haiku-5.5", "z-ai/glm-5.3-flash")
for model in models:
    config_path = ROOT / ".tools" / "config_checks" / (model.split("/")[-1] + ".toml")
    check([benchmark, "-c",
        "from pathlib import Path; from src.notebook_utils import build_paths; from src.tool_runners import _osa_config; "
        "_osa_config(build_paths('readme_2026_three_models'), " + repr(model) + ", Path(" + repr(str(config_path)) + "))"],
        env={**os.environ, "PYTHONPATH": str(ROOT / "benchmark_README")})
    osa_env = {**os.environ, "PYTHONPATH": str(ROOT / ".tools" / "src" / "OSA")}
    check([ROOT / ".tools" / "venvs" / "osa" / "bin" / "python", "-c",
           "from argparse import Namespace; from osa_tool.config.settings import ConfigManager; "
           "c=ConfigManager(Namespace(config_file=" + repr(str(config_path)) + ")); "
           "assert c.config.llm.default.model == " + repr(model) + "; "
           "assert c.config.llm.default.fallback_models == []"], env=osa_env)
print("OSA benchmark configs: three model routes OK")
config_json = check([benchmark, "-c",
    "import json; from src.tool_runners import _opencode_config; print(json.dumps(_opencode_config('openai/gpt-6-luna')))"],
    env={**os.environ, "PYTHONPATH": str(ROOT / "benchmark_README")})
config_env = {**opencode_env, "OPENROUTER_API_KEY": "placeholder",
              "OPENCODE_CONFIG_CONTENT": config_json}
check([opencode, "debug", "config"], env=config_env)
assert "readme-benchmark" in check([opencode, "debug", "agents"], env=config_env)
print(f"OpenCode 2: {version} startup OK")
check([benchmark, "-c", "import pandas, tiktoken, deepeval; import src.tool_runners, src.evaluation, src.reporting; print('ok')"],
      env={**os.environ, "PYTHONPATH": str(ROOT / "benchmark_README")})
print("benchmark: imports OK")
runner_path = ROOT / "benchmark_README" / "src" / "tool_runners.py"
runner_tree = ast.parse(runner_path.read_text(encoding="utf-8"))
for node in ast.walk(runner_tree):
    if isinstance(node, ast.Constant) and isinstance(node.value, str) and "import " in node.value and "\n" in node.value:
        compile(node.value, str(runner_path), "exec")
print("embedded adapters: syntax OK")
presence = check([benchmark, "-c",
    "import os; from src.notebook_utils import load_env_file; load_env_file(); print('present' if os.getenv('OPENROUTER_API_KEY') else 'absent')"],
    env={**os.environ, "PYTHONPATH": str(ROOT / "benchmark_README")})
assert presence == "present", "OPENROUTER_API_KEY is absent"
print("OPENROUTER_API_KEY: present")

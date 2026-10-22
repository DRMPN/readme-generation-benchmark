"""Isolated generation runners. Importing this module never starts an experiment."""

import json
import fcntl
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from .baseline import build_baseline_input
from .notebook_utils import BenchmarkPaths, isolated_input, model_label, utc_now_iso

OPENROUTER_URL = "https://openrouter.ai/api/v1"
TIMEOUT = 60 * 30


def _key() -> str:
    key = os.getenv("OPENROUTER_API_KEY", "")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is required")
    return key


def _env(paths: BenchmarkPaths) -> dict[str, str]:
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = _key()
    env["OPENAI_BASE_URL"] = OPENROUTER_URL
    env["OPENAI_API_BASE"] = OPENROUTER_URL
    env["HF_HOME"] = str(paths.workspace_root / ".tools" / "hf_cache")
    state = paths.workspace_root / ".tools" / "opencode_state"
    env["XDG_DATA_HOME"] = str(state / "data")
    env["XDG_CONFIG_HOME"] = str(state / "config")
    env["XDG_CACHE_HOME"] = str(state / "cache")
    return env


def _python(paths: BenchmarkPaths, tool: str) -> Path:
    path = paths.workspace_root / ".tools" / "venvs" / tool / "bin" / "python"
    if not path.is_file():
        raise FileNotFoundError(f"Missing {tool} environment: {path}; run scripts/install_tools.sh")
    return path


def _source(paths: BenchmarkPaths, tool: str) -> Path:
    path = paths.workspace_root / ".tools" / "src" / tool
    if not path.is_dir():
        raise FileNotFoundError(f"Missing {tool} source: {path}; run scripts/install_tools.sh")
    return path


def _redact(text: str) -> str:
    for key in (os.getenv("OPENROUTER_API_KEY", ""), os.getenv("OPENAI_API_KEY", "")):
        if key:
            text = text.replace(key, "<REDACTED>")
    return text


def _run(cmd: list[str | Path], cwd: Path, log: Path, env: dict[str, str]) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            [str(x) for x in cmd], cwd=cwd, env=env, capture_output=True,
            text=True, timeout=TIMEOUT, encoding="utf-8", errors="replace",
        )
    except subprocess.TimeoutExpired as exc:
        log.write_text(f"Timed out after {TIMEOUT} seconds\n", encoding="utf-8")
        raise RuntimeError(f"Timed out after {TIMEOUT} seconds") from exc
    log.write_text(_redact(result.stdout + "\n--- stderr ---\n" + result.stderr), encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"Exit {result.returncode}; see {log}")


def _chat(model: str, prompt: str) -> dict[str, Any]:
    response = requests.post(
        OPENROUTER_URL + "/chat/completions",
        headers={"Authorization": "Bearer " + _key(), "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}]},
        timeout=TIMEOUT,
    )
    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter HTTP {response.status_code}: {_redact(response.text[:500])}")
    return response.json()


def _content(payload: dict[str, Any]) -> str:
    value = payload["choices"][0]["message"].get("content")
    if isinstance(value, list):
        value = "".join(part.get("text", "") for part in value if isinstance(part, dict))
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Provider returned an empty README")
    return value.strip() + "\n"


def _osa_config(paths: BenchmarkPaths, model: str, dest: Path) -> None:
    source = _source(paths, "OSA") / "osa_tool" / "config" / "settings" / "config.toml"
    data = source.read_text(encoding="utf-8")
    changes = {
        'api = "host"': 'api = "openai"',
        'model = "gpt-5.6-luna"': f"model = {json.dumps(model)}",
        'fallback_models = ["google/gemini-3-flash-preview", "deepseek/deepseek-v3.2", "x-ai/grok-4.1-fast", "openai/gpt-oss-120b"]': 'fallback_models = []',
        'allowed_providers = ["google-vertex", "azure"]': 'allowed_providers = []',
    }
    for old, new in changes.items():
        if old not in data:
            raise ValueError(f"OSA config format changed: {old}")
        data = data.replace(old, new, 1)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(data, encoding="utf-8")


def _generate_osa(paths: BenchmarkPaths, model: str, repo: Path, output: Path, log: Path) -> None:
    config = output.parent / "osa_config.toml"
    _osa_config(paths, model, config)
    env = _env(paths)
    env["PYTHONPATH"] = str(_source(paths, "OSA"))
    # Patch only the connector construction: current OSA defaults send sampling
    # arguments that GPT-6 and Claude Haiku 5.5 reject. Keep OSA's own workflow.
    wrapper = """\
from osa_tool.core.llm.llm import ProtollmHandler
from protollm.connectors import create_llm_connector
def configure(self, model_name):
    self.client = create_llm_connector(model_url=self._build_model_url(model_name))
ProtollmHandler._configure_api = configure
from osa_tool.run import main
main()
"""
    cmd = [
        _python(paths, "osa"), "-c", wrapper, "--repository", str(repo),
        "--config-file", str(config), "--mode", "advanced", "--web-mode", "--readme",
        "--no-fork", "--no-pull-request", "--api", "openai",
        "--base-url", OPENROUTER_URL, "--model", model, "--model-readme", model,
        "--model-general", model,
    ]
    _run(cmd, paths.workspace_root, log, env)
    generated = repo / "README.md"
    if not generated.is_file():
        raise RuntimeError("OSA did not create README.md")
    shutil.copy2(generated, output)


def _generate_larch(paths: BenchmarkPaths, model: str, repo: Path, output: Path, log: Path) -> None:
    env = _env(paths)
    env["PYTHONPATH"] = str(_source(paths, "larch"))
    script = """\
import sys
from pathlib import Path
import requests
from transformers import GPT2TokenizerFast
from larch.context_creator import ContextCreatorName, Directory
from larch.generator.base import BaseGenerator
from larch.postprocessor import postprocess
class OpenRouterGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(GPT2TokenizerFast.from_pretrained('gpt2'), 65536, False)
    def generate(self, context, prompt, max_length):
        import os
        response = requests.post('https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': 'Bearer ' + os.environ['OPENROUTER_API_KEY']},
            json={'model': sys.argv[3], 'messages': [{'role': 'user', 'content': context + prompt}]},
            timeout=1800)
        response.raise_for_status()
        value = response.json()['choices'][0]['message']['content']
        if not value:
            raise RuntimeError('Empty LArch output')
        return prompt + value, value
repo = Path(sys.argv[1]); output = Path(sys.argv[2]); generator = OpenRouterGenerator()
creator = ContextCreatorName('file_names').get_module()
context = creator.create_context(Directory.from_directory(str(repo)),
    use_prompt=True, tokenizer=generator.tokenizer, max_tokens=60000, project_name=repo.name)
seed = '# README\\n\\nWrite a complete README from this repository.\\n'
generated, diff = generator.generate(context, seed, max_length=4000)
generated, _ = postprocess(generated, diff)
if generated.startswith(seed): generated = generated[len(seed):]
output.write_text(generated.strip() + '\\n', encoding='utf-8')
"""
    _run([_python(paths, "larch"), "-c", script, repo, output, model], paths.workspace_root, log, env)


def _generate_readmeready(paths: BenchmarkPaths, model: str, repo: Path, output: Path, log: Path) -> None:
    env = _env(paths)
    env["PYTHONPATH"] = str(_source(paths, "ReadMeReady"))
    script = """\
import sys, shutil, importlib
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from readme_ready.types import AutodocReadmeConfig, AutodocRepoConfig, AutodocUserConfig, LLMModels
from readme_ready.utils import llm_utils
model = LLMModels.GPT4
llm_utils.models[model].llm = ChatOpenAI(model=sys.argv[3], api_key=__import__('os').environ['OPENROUTER_API_KEY'], base_url='https://openrouter.ai/api/v1')
llm_utils.models[model].max_length = 64000
def local_embeddings(_model, device):
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2',
        model_kwargs={'device': None if device == 'auto' else device},
        encode_kwargs={'normalize_embeddings': True})
llm_utils.get_embeddings = local_embeddings
process_repository = importlib.import_module('readme_ready.index.process_repository')
select_model = importlib.import_module('readme_ready.index.select_model')
vector_store = importlib.import_module('readme_ready.index.create_vector_store')
chat_chain = importlib.import_module('readme_ready.query.create_chat_chain')
query = importlib.import_module('readme_ready.query.query')
process_repository.select_model = lambda prompts, llms, models, priority: models[model]
select_model.select_model = process_repository.select_model
vector_store.get_embeddings = local_embeddings
query.get_embeddings = local_embeddings
chat_chain.get_openai_chat_model = lambda *args, **kwargs: llm_utils.models[model].llm
repo = Path(sys.argv[1]); output = Path(sys.argv[2]); project_name = output.stem.removesuffix('_README'); work = output.parent / '_work' / project_name
if work.exists(): shutil.rmtree(work)
work.mkdir(parents=True, exist_ok=True)
config = AutodocRepoConfig(name=project_name, repository_url='file://' + str(repo), root=str(repo),
    output=str(work), llms=[model], priority=None, max_concurrent_calls=8, add_questions=False,
    ignore=['.*', '*package-lock.json', 'node_modules', '*dist*', '*build*', '*test*', '*.svg', '*.md', '*.mdx'],
    file_prompt='Write a concise technical explanation of this code file in markdown.',
    folder_prompt='Write a concise technical explanation of this folder in markdown.',
    chat_prompt='', content_type='code', target_audience='developer', link_hosted=False,
    peft_model_path=None, device='cpu')
index = importlib.import_module('readme_ready.index.index')
index.index(config)
query.generate_readme(config, AutodocUserConfig(llms=[model]),
    AutodocReadmeConfig('Description,Requirements,Installation,Usage,Contributing,License'))
files = sorted((work / 'docs' / 'data').glob('README_*.md'))
if not files: raise RuntimeError('ReadMeReady produced no README')
shutil.copy2(files[0], output)
"""
    _run([_python(paths, "readmeready"), "-c", script, repo, output, model], paths.workspace_root, log, env)


def _opencode_binary(paths: BenchmarkPaths) -> Path:
    path = paths.workspace_root / ".tools" / "opencode" / "opencode"
    if not path.is_file():
        raise FileNotFoundError(f"OpenCode 2 CLI not installed: {path}")
    return path


def _opencode_config(model: str) -> dict[str, Any]:
    return {
        "$schema": "https://opencode.ai/config.json",
        "provider": {"openrouter": {"npm": "@ai-sdk/openai-compatible", "name": "OpenRouter",
            "options": {"baseURL": OPENROUTER_URL, "apiKey": "{env:OPENROUTER_API_KEY}"},
            "models": {model: {"name": model}}}},
        "agent": {"readme-benchmark": {"model": "openrouter/" + model,
            "permission": {"read": "allow", "glob": "allow", "grep": "allow",
                "edit": "allow", "bash": "deny", "webfetch": "deny", "task": "deny"}}},
    }


def _generate_opencode(paths: BenchmarkPaths, model: str, repo: Path, output: Path, log: Path) -> None:
    # OpenCode 2 uses standalone mode and writes only in its disposable worktree.
    if paths.workspace_root in repo.parents or not (repo / ".git").is_dir():
        raise ValueError("OpenCode requires a separate clone outside the benchmark workspace")
    config = _opencode_config(model)
    env = _env(paths)
    # OpenCode 2's run handler resolves the project from PWD. subprocess cwd
    # alone is insufficient when the parent process exports a stale PWD.
    env["PWD"] = str(repo)
    env["OPENCODE_CONFIG_CONTENT"] = json.dumps(config)
    env["OPENCODE_DISABLE_AUTOUPDATE"] = "1"
    prompt = (
        "Inspect this repository and write a complete, accurate README.md. "
        "Create only README.md in the current directory. Start with a level-one heading. "
        "Do not invent unsupported claims."
    )
    _run([_opencode_binary(paths), "run", "--standalone", "--model", "openrouter/" + model,
          "--agent", "readme-benchmark", prompt], repo, log, env)
    generated = repo / "README.md"
    if not generated.is_file():
        raise RuntimeError("OpenCode did not create README.md")
    shutil.copy2(generated, output)


def _generate_baseline(model: str, repo: Path, output: Path) -> None:
    prompt, manifest = build_baseline_input(repo)
    payload = _chat(model, prompt)
    output.write_text(_content(payload), encoding="utf-8")
    metadata = {"model": model, "input": manifest, "usage": payload.get("usage", {}),
                "provider_generation_id": payload.get("id")}
    output.with_suffix(".json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


GENERATORS = {
    "baseline": _generate_baseline,
    "osa": _generate_osa,
    "readmeready": _generate_readmeready,
    "larch": _generate_larch,
    "opencode": _generate_opencode,
}


def run_selected_tools(repo_df: pd.DataFrame, paths: BenchmarkPaths, experiment: dict[str, Any]) -> pd.DataFrame:
    """Run enabled cells sequentially; each receives a fresh sanitized worktree."""
    old_path = paths.experiment_dir / "tool_status.csv"
    lock_path = paths.experiment_dir / "tool_status.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    reset = bool(experiment.get("reset", {}).get("tool_outputs", False))
    for model in experiment["models"]:
        for tool, generator in GENERATORS.items():
            if not experiment.get("tools", {}).get(tool, {}).get("enabled", False):
                continue
            for item in repo_df.itertuples():
                slug = item.repo_slug
                output = paths.tools_dir / tool / model_label(model) / f"{slug}_README.md"
                log = paths.logs_dir / tool / model_label(model) / f"{slug}.log"
                output.parent.mkdir(parents=True, exist_ok=True)
                start = time.monotonic()
                started_at = utc_now_iso()
                status, error = "done", ""
                try:
                    if reset or not output.is_file():
                        with isolated_input(paths, slug, external_clone=tool == "opencode") as repo:
                            if tool == "baseline":
                                generator(model, repo, output)
                                log.parent.mkdir(parents=True, exist_ok=True)
                                log.write_text(output.with_suffix(".json").read_text(encoding="utf-8"), encoding="utf-8")
                            else:
                                generator(paths, model, repo, output, log)
                    if not output.is_file() or not output.read_text(encoding="utf-8").strip():
                        raise ValueError("Output is missing or empty")
                except Exception as exc:
                    status, error = "failed", _redact(str(exc))
                    output.unlink(missing_ok=True)
                    log.parent.mkdir(parents=True, exist_ok=True)
                    if not log.is_file():
                        log.write_text(error + "\n", encoding="utf-8")
                row = {"tool": tool, "model": model, "model_label": model_label(model),
                    "repo_slug": slug, "repo_type": item.repo_type, "status": status,
                    "started_at": started_at, "finished_at": utc_now_iso(),
                    "duration_sec": round(time.monotonic() - start, 3),
                    "output_path": str(output), "log_path": str(log), "error": error}
                with lock_path.open("w") as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX)
                    current = pd.read_csv(old_path) if old_path.is_file() else pd.DataFrame()
                    frame = pd.concat([current, pd.DataFrame([row])], ignore_index=True)
                    frame = frame.drop_duplicates(["tool", "model", "repo_slug"], keep="last")
                    temp_path = old_path.with_suffix(".csv.tmp")
                    frame.to_csv(temp_path, index=False)
                    os.replace(temp_path, old_path)
                print(f"Generation {model} {tool} {slug}: {status}", flush=True)
    return pd.read_csv(old_path) if old_path.is_file() else pd.DataFrame()

"""Deterministic, bounded repository text for the direct LLM baseline."""

import subprocess
from pathlib import Path

import tiktoken


MAX_INPUT_TOKENS = 64_000
MAX_FILE_TOKENS = 10_000
MAX_FILE_BYTES = 250_000
TEXT_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java",
    ".kt", ".c", ".cc", ".cpp", ".h", ".hpp", ".cs", ".rb", ".sh",
    ".sql", ".toml", ".yaml", ".yml", ".json", ".xml", ".ini",
    ".cfg", ".txt", ".md", ".rst", ".tex", ".ipynb",
}
MANIFESTS = {
    "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "package.json",
    "cargo.toml", "go.mod", "pom.xml", "build.gradle", "makefile", "dockerfile",
    "compose.yaml", "docker-compose.yml", "environment.yml", "license",
}
ENTRYPOINTS = {"main.py", "app.py", "__main__.py", "index.js", "index.ts", "cli.py"}
SKIP_NAMES = {".env", ".env.local", "id_rsa", "id_ed25519"}


def _tracked_paths(repo_dir: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"], cwd=repo_dir, capture_output=True, check=True
    )
    return [p.decode("utf-8", errors="surrogateescape") for p in proc.stdout.split(b"\0") if p]


def _priority(path: str) -> tuple[int, int, str]:
    name = Path(path).name.lower()
    if name in MANIFESTS or name.startswith("requirements"):
        rank = 0
    elif name in ENTRYPOINTS:
        rank = 1
    elif Path(path).suffix.lower() in {".md", ".rst", ".tex"}:
        rank = 2
    elif "test" not in Path(path).parts:
        rank = 3
    else:
        rank = 4
    return rank, len(Path(path).parts), path


def build_baseline_input(repo_dir: Path) -> tuple[str, dict]:
    """Return one prompt and the file-selection manifest, within 64k tokens."""
    encoder = tiktoken.get_encoding("cl100k_base")
    paths = _tracked_paths(repo_dir)
    preamble = (
        "Create a complete README.md for this project from the repository text below. "
        "Describe only information supported by the supplied files. Include relevant "
        "overview, setup, usage, configuration, development, testing, and license sections. "
        "Return only Markdown, starting with a level-one heading. Aim for 800-1500 words.\n\n"
        "Repository file tree:\n"
    )
    tokens = encoder.encode(preamble)
    tree_lines = []
    for path in sorted(paths):
        line = f"{path}\n"
        line_tokens = encoder.encode(line)
        if len(tokens) + len(line_tokens) > MAX_INPUT_TOKENS // 4:
            break
        tree_lines.append(line)
        tokens.extend(line_tokens)
    parts = [preamble, *tree_lines, "\nSelected file contents:\n"]
    tokens.extend(encoder.encode(parts[-1]))
    selected = []
    skipped = []
    for rel in sorted(paths, key=_priority):
        path = repo_dir / rel
        name = path.name.lower()
        if (not path.is_file() or path.is_symlink() or name in SKIP_NAMES
                or name.startswith("readme") and path.parent == repo_dir
                or path.suffix.lower() not in TEXT_SUFFIXES and name not in MANIFESTS):
            skipped.append(rel)
            continue
        with path.open("rb") as handle:
            raw = handle.read(MAX_FILE_BYTES + 1)
        if b"\0" in raw:
            skipped.append(rel)
            continue
        try:
            content = raw[:MAX_FILE_BYTES].decode("utf-8")
        except UnicodeDecodeError:
            skipped.append(rel)
            continue
        block_prefix = f"\n--- {rel} ---\n"
        prefix_tokens = encoder.encode(block_prefix)
        content_tokens = encoder.encode(content)[:MAX_FILE_TOKENS]
        available = MAX_INPUT_TOKENS - len(tokens) - len(prefix_tokens) - 2
        if available <= 0:
            skipped.append(rel)
            continue
        included_tokens = content_tokens[:available]
        parts.append(block_prefix + encoder.decode(included_tokens) + "\n")
        tokens.extend(prefix_tokens)
        tokens.extend(included_tokens)
        tokens.extend(encoder.encode("\n"))
        selected.append({"path": rel, "tokens": len(included_tokens), "truncated": len(raw) > MAX_FILE_BYTES or len(included_tokens) < len(encoder.encode(content))})
    prompt = "".join(parts)
    # Exact final count includes tokenizer boundary effects between blocks.
    encoded = encoder.encode(prompt)
    if len(encoded) > MAX_INPUT_TOKENS:
        prompt = encoder.decode(encoded[:MAX_INPUT_TOKENS])
    manifest = {
        "tokenizer": "cl100k_base",
        "token_limit": MAX_INPUT_TOKENS,
        "tokens": len(encoder.encode(prompt)),
        "tree_files": len(tree_lines),
        "tracked_files": len(paths),
        "selected": selected,
        "skipped": skipped,
    }
    return prompt, manifest

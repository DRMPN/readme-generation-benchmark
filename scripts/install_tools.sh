#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 -c 'import sys; assert sys.version_info[:2] == (3, 12), "Python 3.12 is required"'
SRC="$ROOT/.tools/src"
VENV="$ROOT/.tools/venvs"
mkdir -p "$SRC" "$VENV"
python3 -m venv "$ROOT/benchmark_README/.venv"
"$ROOT/benchmark_README/.venv/bin/python" -m pip install -U pip
"$ROOT/benchmark_README/.venv/bin/python" -m pip install -r "$ROOT/benchmark_README/requirements.txt"
install_source() {
  local name="$1" url="$2" sha="$3"
  if [[ ! -d "$SRC/$name/.git" ]]; then git clone "$url" "$SRC/$name"; fi
  git -C "$SRC/$name" fetch --tags origin
  git -C "$SRC/$name" checkout --detach "$sha"
  [[ "$(git -C "$SRC/$name" rev-parse HEAD)" == "$sha" ]]
}
make_venv() {
  local name="$1"
  python3 -m venv "$VENV/$name"
  "$VENV/$name/bin/python" -m pip install -U pip wheel
}
install_source OSA https://github.com/aimclub/OSA.git 17c347e8648654aee37b741859cfc871e9b46f30
install_source larch https://github.com/hitachi-nlp/larch.git 832d36512531c4a55bc3395c7a67bc9d2c7ccdf4
install_source ReadMeReady https://github.com/souradipp76/ReadMeReady.git 6c45438c7bce05351f4e91a06af3ab38e236aa0f
readmeready_patch="$ROOT/scripts/patches/readmeready-output-paths.patch"
if git -C "$SRC/ReadMeReady" apply --check "$readmeready_patch"; then
  git -C "$SRC/ReadMeReady" apply "$readmeready_patch"
elif ! git -C "$SRC/ReadMeReady" apply --reverse --check "$readmeready_patch"; then
  echo "ReadMeReady output-path patch does not match the pinned checkout" >&2
  exit 1
fi
make_venv osa
"$VENV/osa/bin/python" -m pip install -r "$SRC/OSA/requirements.txt"
"$VENV/osa/bin/python" -m pip install -e "$SRC/OSA" --no-deps
make_venv larch
"$VENV/larch/bin/python" -m pip install -e "$SRC/larch" --no-deps
"$VENV/larch/bin/python" -m pip install 'torch==2.14.1+cpu' --index-url https://download.pytorch.org/whl/cpu
"$VENV/larch/bin/python" -m pip install 'transformers>=4.50,<5' 'numpy>=1.26,<2' 'networkx>=2.8' 'requests>=2.31' 'tiktoken>=0.8' 'pydantic>=1.10,<2' 'fastapi<0.110' yaspin tqdm joblib xgboost-cpu snorkel click
make_venv readmeready
"$VENV/readmeready/bin/python" -m pip install -e "$SRC/ReadMeReady" --no-deps
"$VENV/readmeready/bin/python" -m pip install 'torch==2.14.1+cpu' --index-url https://download.pytorch.org/whl/cpu
"$VENV/readmeready/bin/python" -m pip install -r "$ROOT/benchmark_README/requirements-readmeready.txt"
python3 "$ROOT/scripts/install_opencode.py"
python3 "$ROOT/scripts/verify_install.py"

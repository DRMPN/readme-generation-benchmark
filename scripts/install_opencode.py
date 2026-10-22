"""Install pinned OpenCode 2 Linux binary from its npm release tarball."""
import io
import json
import platform
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = "2.1.2"
ARCH = {"x86_64": "x64", "aarch64": "arm64"}.get(platform.machine())
if ARCH is None or platform.system() != "Linux":
    raise SystemExit("This installer supports Linux x86_64 and arm64")
package = f"@opencode/cli-linux-{ARCH}"
# The metadata tarball URL is authoritative and handles npm filename changes.
meta_url = f"https://registry.npmjs.org/{package.replace('/', '%2f')}/{VERSION}"
with urllib.request.urlopen(meta_url, timeout=30) as response:
    meta = json.load(response)
with urllib.request.urlopen(meta["dist"]["tarball"], timeout=120) as response:
    payload = response.read()
dest = ROOT / ".tools" / "opencode"
dest.mkdir(parents=True, exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
    matches = [m for m in archive.getmembers() if m.isfile() and m.name.endswith("/opencode")]
    if len(matches) != 1:
        raise RuntimeError("OpenCode package has no unique binary")
    with archive.extractfile(matches[0]) as source, (dest / "opencode").open("wb") as target:
        target.write(source.read())
(dest / "opencode").chmod(0o755)
(dest / "version.txt").write_text(VERSION + "\n")
print(f"Installed OpenCode 2 {VERSION}")

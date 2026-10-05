"""Verify archive completeness and checksums without executing archived code."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--staged', action='store_true', help='Also verify exact staged Git blob bytes')
args = parser.parse_args()
inventory = json.loads((ROOT / "inventory.json").read_text(encoding="utf-8"))
expected = {item["path"] for item in inventory["files"]}
actual = {p.relative_to(ROOT).as_posix() for folder in ("skills", "plugins") for p in (ROOT / folder).rglob("*") if p.is_file()}
errors = []
if expected != actual:
    errors.append(f"Manifest mismatch: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
for item in inventory["files"]:
    path = ROOT / item["path"]
    if not path.resolve().is_relative_to(ROOT) or not path.is_file():
        errors.append(f"Missing or unsafe path: {item['path']}")
        continue
    if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
        errors.append(f"Checksum mismatch: {item['path']}")
for item in inventory["skills"] + inventory["agent_interfaces"]:
    if item["path"] not in expected:
        errors.append(f"Untracked catalog entry: {item['path']}")
image_metadata = ROOT / 'assets/images/metadata.json'
if image_metadata.is_file():
    artwork = json.loads(image_metadata.read_text(encoding='utf-8'))
    for key in ('asset', 'generation_prompt', 'correction_prompt'):
        path = ROOT / artwork[key]
        if not path.resolve().is_relative_to(ROOT) or not path.is_file():
            errors.append(f"Missing or unsafe image resource: {artwork[key]}")
    image = ROOT / artwork['asset']
    if image.is_file() and hashlib.sha256(image.read_bytes()).hexdigest() != artwork['sha256']:
        errors.append('Generated overview checksum mismatch')
    if artwork['skills'] != len(inventory['skills']) or artwork['agent_interfaces'] != len(inventory['agent_interfaces']):
        errors.append('Overview artwork counts differ from the skill inventory; refresh the image and metadata')
if args.staged:
    result = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT,
                            input=''.join(f":{item['path']}\n" for item in inventory['files']).encode(),
                            capture_output=True, check=True)
    cursor = 0
    for item in inventory['files']:
        end = result.stdout.index(b'\n', cursor)
        header = result.stdout[cursor:end].split()
        if len(header) != 3 or header[1] != b'blob':
            raise SystemExit(f"Missing staged blob: {item['path']}")
        size = int(header[2])
        data = result.stdout[end + 1:end + 1 + size]
        cursor = end + 2 + size
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            errors.append(f"Staged checksum mismatch: {item['path']}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Verified {len(expected)} files, {len(inventory['skills'])} skills, and {len(inventory['agent_interfaces'])} agent interfaces.")

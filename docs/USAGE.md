# Installation and maintenance

## Verify the snapshot

Run `python scripts/verify.py` from the repository root. It checks file completeness and SHA-256 checksums without executing archived skill scripts. This verifies the archive's consistency, not the availability of external tools.

## Install a custom skill

Inspect the skill instructions and copy an individual package into your Codex skills directory. For the custom dark-tech-cover skill, use PowerShell:

```powershell
$skillHome = Join-Path $env:USERPROFILE '.codex/skills'
$target = Join-Path $skillHome 'dark-tech-cover'
if (Test-Path -LiteralPath $target) { throw 'Skill already exists; compare it before replacing.' }
New-Item -ItemType Directory -Force -Path $skillHome | Out-Null
Copy-Item -LiteralPath './skills/custom/dark-tech-cover' -Destination $target -Recurse
```

Reload your Codex session after installation. Keep scripts, assets, references, and agent YAML files with the skill package.

## Built-in and plugin skills

The `skills/system` directory is a snapshot for reference and recovery. Review differences before replacing any built-in skill.

Plugin packages retain their versioned directory layout because some skills reference resources outside their own skill directory. Use the original plugin installation mechanism to enable plugin services. Copying a `SKILL.md` file alone does not connect an app or provide MCP tools.

The YAML files indexed in [AGENTS.md](AGENTS.md) are skill interface metadata. They do not configure standalone Codex agents. No standalone agent definitions were available to export.

## Refresh the archive

```powershell
python scripts/snapshot.py --snapshot-date YYYY-MM-DD
python scripts/catalog_images.py
python scripts/verify.py
git diff --stat
git diff -- docs inventory.json
```

The importer reads the current user's `.codex/skills` directory and versioned `openai-curated-remote` plugin cache. Override the source with `--codex-home PATH` if needed. It copies only skill packages and supporting plugin resource directories, then regenerates both indexes and the manifest.

The importer refuses to replace files whose contents differ. Review changed packages explicitly before importing an update; new plugin versions can coexist with older snapshots. It does not remove existing packages automatically.

The image catalog indexes original package images without moving them. Repository artwork, generation prompts, and provenance live under `assets/images/`. When skill counts change, update the overview artwork and its documentation as well; verification checks its checksum and inventory counts.

Before committing a refresh, review new files for credentials, personal data, large generated assets, and applicable source terms. Preserve bundled licenses and original package structure.

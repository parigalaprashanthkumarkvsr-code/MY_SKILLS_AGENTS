"""Archive installed skill packages and generate a portable, verifiable catalog."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"__pycache__", ".git", "node_modules", ".DS_Store", ".codex-system-skills.marker"}


def copy_tree(source: Path, target: Path) -> None:
    for item in sorted(source.rglob("*")):
        relative = item.relative_to(source)
        if any(part in EXCLUDED for part in relative.parts) or item.suffix == ".pyc":
            continue
        if item.is_symlink():
            raise ValueError(f"Refusing symbolic link: {relative}")
        if item.is_file():
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists() and destination.read_bytes() != item.read_bytes():
                raise ValueError(f"Existing file differs; review before replacing: {destination}")
            shutil.copy2(item, destination)
            assert destination.read_bytes() == item.read_bytes()


def metadata(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8-sig")
    frontmatter = content.split("---", 2)[1]
    result = {}
    for key in ("name", "description"):
        match = re.search(rf"^{key}:\s*(.+)$", frontmatter, re.MULTILINE)
        if not match:
            raise ValueError(f"Missing {key}: {path}")
        result[key] = match.group(1).strip().strip('"').strip("'")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--snapshot-date", default=date.today().isoformat())
    args = parser.parse_args()
    provenance = {}
    local = args.codex_home / "skills"
    for skill in sorted(local.rglob("SKILL.md")):
        relative = skill.parent.relative_to(local)
        group = "system" if relative.parts[0] == ".system" else "custom"
        destination = ROOT / "skills" / group / skill.parent.name
        copy_tree(skill.parent, destination)
        provenance[(destination / "SKILL.md").relative_to(ROOT).as_posix()] = {
            "group": group, "source": f"$CODEX_HOME/skills/{relative.as_posix()}"
        }

    cache = args.codex_home / "plugins" / "cache" / "openai-curated-remote"
    if cache.exists():
        for plugin in sorted(cache.iterdir()):
            if not plugin.is_dir():
                continue
            for version in sorted(plugin.iterdir()):
                if not version.is_dir() or not (version / "skills").is_dir():
                    continue
                destination = ROOT / "plugins" / plugin.name / version.name
                # Retain package-level resources for relative links, without installation state.
                for component in ("skills", "references", "scripts", "assets", "tests"):
                    if (version / component).is_dir():
                        copy_tree(version / component, destination / component)
                for item in version.iterdir():
                    if item.is_file() and (item.name == "README.md" or "license" in item.name.lower() or "notice" in item.name.lower()):
                        destination.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, destination / item.name)
                for skill in (destination / "skills").rglob("SKILL.md"):
                    provenance[skill.relative_to(ROOT).as_posix()] = {
                        "group": "plugin", "plugin": plugin.name, "version": version.name,
                        "source": f"openai-curated-remote/{plugin.name}/{version.name}/skills/{skill.parent.name}",
                    }

    skills = []
    agents = []
    for relative, origin in sorted(provenance.items()):
        path = ROOT / relative
        skills.append({**metadata(path), "path": relative, **origin})
        for agent in sorted((path.parent / "agents").glob("*.yaml")):
            agents.append({"skill": skills[-1]["name"], "path": agent.relative_to(ROOT).as_posix(), "kind": "skill-interface-metadata"})

    files = []
    for folder in ("skills", "plugins"):
        for path in sorted((ROOT / folder).rglob("*")):
            if path.is_file():
                files.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size,
                              "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    inventory = {"schema_version": 1, "snapshot_date": args.snapshot_date,
                 "skills": skills, "agent_interfaces": agents, "standalone_agents": [], "files": files}
    (ROOT / "inventory.json").write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    rows = ["# Skill catalog", "", f"Snapshot: {args.snapshot_date}. {len(skills)} skills.", "", "| Skill | Origin | Purpose |", "| --- | --- | --- |"]
    for skill in skills:
        origin = skill.get("plugin", skill["group"])
        description = skill["description"].replace("|", "\\|")
        rows.append(f"| [{skill['name']}](../{skill['path']}) | {origin} | {description} |")
    (docs / "CATALOG.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    rows = ["# Agent interface index", "", f"{len(agents)} YAML interface definitions accompany the archived skills.", "",
            "These files describe skill names, prompts, policies, and dependencies. They are not standalone running agents or Codex agent role configurations.", "",
            "No custom standalone agent definitions were found in the inspected standard user agent locations or the Codex configuration. Session agents are temporary and are not exported.", "",
            "The review-agent skill is included in the system skills archive. Its original invocation policy is preserved.", "", "| Skill | Definition |", "| --- | --- |"]
    rows.extend(f"| {agent['skill']} | [openai.yaml](../{agent['path']}) |" for agent in agents)
    (docs / "AGENTS.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Archived {len(skills)} skills, {len(agents)} agent interfaces, and {len(files)} files.")


if __name__ == "__main__":
    main()

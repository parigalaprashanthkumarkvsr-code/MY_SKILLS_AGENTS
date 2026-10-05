# My Skills & Agents

A versioned archive of my installed Codex skills, supporting resources, and skill agent interfaces. It brings custom workflows, built-in skills, and cached plugin skills into one documented collection.

**[Browse skills](docs/CATALOG.md)** · **[Browse agent interfaces](docs/AGENTS.md)** · **[Installation and maintenance](docs/USAGE.md)** · **[Source and license notes](THIRD_PARTY_NOTICES.md)**

## Repository layout

```text
skills/
  custom/                 Personal skill packages
  system/                 Built-in skill snapshots
plugins/
  <plugin>/<version>/     Plugin skills and supporting resources
docs/
  CATALOG.md              Complete skill directory
  AGENTS.md               Agent interface directory
  USAGE.md                Installation and maintenance guide
scripts/
  snapshot.py             Import installed packages and generate indexes
  verify.py               Verify archive files against SHA-256 checksums
inventory.json            Source provenance, catalog, and file checksums
```

## What's included

- **Custom:** dark technical artwork and Remotion B-roll workflows.
- **System:** image generation, OpenAI documentation, skill creation, skill installation, and code review.
- **Plugins:** Sites, ChatGPT Pets, plugin management, and OpenAI document templates.
- **Agent interfaces:** original `agents/openai.yaml` files retained alongside their skills.

The catalog includes cached packages that may not be enabled in a particular session. No standalone custom agent configurations were found during this snapshot. Plugin skills may require their original connectors and runtime tools; this archive does not provide those services.

## Quick start

```powershell
git clone https://github.com/parigalaprashanthkumarkvsr-code/MY_SKILLS_AGENTS.git
Set-Location MY_SKILLS_AGENTS
python scripts/verify.py
```

Start with the [skill catalog](docs/CATALOG.md), then follow the [usage guide](docs/USAGE.md) to install an individual skill or refresh the archive.

## Archive policy

Packages retain their original instructions, assets, scripts, references, and bundled license files. Plugin directory layouts preserve relative references to shared resources. Account credentials, session history, local configuration, installation state, and generated user work are excluded.

The archive is for backup, inspection, and controlled reuse. Upstream content remains subject to its original terms; see [third-party notices](THIRD_PARTY_NOTICES.md).

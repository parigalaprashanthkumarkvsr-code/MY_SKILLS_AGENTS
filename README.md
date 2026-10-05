# My Skills & Agents

![Blue-and-white overview of 34 skills across Creative, Core tools, Sites, ChatGPT Pets, Plugin management, and Document templates, with 28 agent interfaces](assets/images/generated/skills-overview-blue-white-v1.png)

A versioned archive of my installed Codex skills, supporting resources, and skill agent interfaces. It brings custom workflows, built-in skills, and cached plugin skills into one documented collection.

**[Browse skills](docs/CATALOG.md)** · **[Browse agent interfaces](docs/AGENTS.md)** · **[Installation and maintenance](docs/USAGE.md)** · **[Source and license notes](THIRD_PARTY_NOTICES.md)**

## Repository layout

```text
assets/images/
  generated/              Blue-and-white repository overview
  prompts/                Original generation and correction prompts
skills/
  custom/                 Personal skill packages
  system/                 Built-in skill snapshots
plugins/
  <plugin>/<version>/     Plugin skills and supporting resources
docs/
  CATALOG.md              Complete skill directory
  AGENTS.md               Agent interface directory
  USAGE.md                Installation and maintenance guide
  IMAGES.md               Image references, previews, and provenance
scripts/
  snapshot.py             Import installed packages and generate indexes
  verify.py               Verify archive files against SHA-256 checksums
inventory.json            Source provenance, catalog, and file checksums
```

## What's included

| Skill group | Count | Skills |
| --- | ---: | --- |
| Creative | 1 | `dark-tech-cover` |
| Core tools | 5 | `imagegen`, `openai-docs`, `skill-creator`, `skill-installer`, `review-agent` |
| Sites | 4 | `sites-building`, `sites-hosting`, `sites-mcp`, `sites-preview-troubleshooting` |
| ChatGPT Pets | 3 | `create-pet`, `pets`, `update-pet` |
| Plugin management | 1 | `plugin-management` |
| Document templates | 20 | Analytics Dashboard, Business Review, Design Report, Experiment Analysis, Financial Budget, Investment Committee Memo, Legal Memorandum, Market Trends Report, Minimal Letterhead, Operating Calendar, Operating Review, Project Kickoff, Project Tracker, Sales Pipeline, Simple Dark Mode, Simple Light Mode, Strategy Memorandum, System Design, Team Alignment, Three Statement Forecast |

**Total: 34 skills and 28 agent interfaces.** Original `agents/openai.yaml` files accompany their skill packages. The [complete catalog](docs/CATALOG.md) links every skill to its instructions.

See the [image reference library](docs/IMAGES.md) for the overview artwork, original creative reference, template previews, and package icons. Generated repository artwork lives under `assets/images/`; upstream skill images stay next to their packages so their original references remain valid.

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

# Contributing

Keep each skill self-contained, with its original `SKILL.md`, references, scripts, assets, and agent interface files. Preserve shared plugin resources and version directories.

For an archive refresh, use the importer described in [the usage guide](docs/USAGE.md). Review the resulting diff and retain source and licensing information.

Run `python scripts/verify.py` before opening a change. Explain which packages changed, their source versions, and any missing dependencies. Do not commit account configuration, credentials, session data, or generated user artifacts.

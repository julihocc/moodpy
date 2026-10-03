# MoodPy repository instructions

Follow [AGENTS.md](../AGENTS.md). The current agent authoring interface is documented
in [docs/authoring-guide.md](../docs/authoring-guide.md); the verified recipe catalog
identifies supported starting points.

Use callable constraints and injected RNGs. Build question banks through build_bank(),
render fully formatted text with template=False, and validate snapshots before export.
Preview and XML must use the same snapshots. Preserve legacy interfaces and existing
submodule changes. Report local checks separately from a live Moodle import.

Install with python -m pip install -e '.[dev]' for maintenance. Run pytest and verify
the built wheel using [the development guide](../docs/development.md).
Current navigation is in [docs/README.md](../docs/README.md). Keep generated outputs
in artifacts/. Do not treat docs/archive/, examples/legacy/, or scripts/legacy/
as current instructions or rely on their example-count, coverage, or release claims.

# MoodPy repository instructions

Follow [AGENTS.md](../AGENTS.md). The current agent authoring interface is documented
in [docs/authoring-guide.md](../docs/authoring-guide.md); the verified recipe catalog
identifies supported starting points.

Use callable constraints and injected RNGs. Build question banks through build_bank(),
render fully formatted text with template=False, and validate snapshots before export.
Preview and XML must use the same snapshots. Preserve legacy interfaces and existing
submodule changes. Report local checks separately from a live Moodle import.

Install with python -m pip install -e '.[dev]' for maintenance. Run pytest and verify
the built wheel. Do not rely on historical example-count, coverage, or release claims.

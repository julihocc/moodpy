# Repository tools

Run `python scripts/check_environment.py` after installing MoodPy. Add
`--require-wheel` to verify a wheel installation instead of an editable checkout.
The checker reports runtime dependencies and version agreement, then generates and
validates one question from each core recipe without writing a bundle.

The [development guide](../docs/development.md) covers tests and package builds.
The live Moodle harness remains in `.github/moodle/` with its CI workflow; see the
[Moodle checklist](../docs/moodle-import-checklist.md) for the local runner.

Old migration, deployment, and GitHub automation scripts live in
[legacy/](legacy/README.md) and are not maintained entry points.

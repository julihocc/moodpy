# Developing MoodPy

Read [AGENTS.md](../AGENTS.md) for repository rules and the
[architecture](architecture.md) for module responsibilities. Preserve public
interfaces and existing local changes, including submodule worktrees.

From the repository root, create an environment and install the package:

```bash
python -m venv .venv
# POSIX shells; on Windows use .venv\Scripts\activate instead.
. .venv/bin/activate
python -m pip install -e '.[dev]' build
python scripts/check_environment.py
```

Python 3.8–3.14 is covered by CI. NumPy, SciPy, matplotlib, and tabulate are runtime
dependencies. Core development does not require submodules, Docker, or credentials.
The optional generator package has separate setup and tests in its README.

Run the core checks and a representative bank:

```bash
python -m pytest
python -m unittest tests.test_bank
python examples/agent_workflow/author_bank.py --seed 42 --samples 2 --output artifacts/dev-bank
```

Use a fresh output directory for each run, or explicitly request `--overwrite` to
replace a known bundle. Keep generated banks in `artifacts/`. Add regressions when
changing sampling, answer formatting, feedback, validation, or export. Legacy
examples contain unfinished migrations and are not part of core test discovery.

To check packaging, build a source archive and wheel, then install the wheel into
a separate environment. POSIX example:

```bash
python -m build
python -m venv /tmp/moodpy-wheel-check
/tmp/moodpy-wheel-check/bin/python -m pip install dist/*.whl pytest pytest-cov
/tmp/moodpy-wheel-check/bin/python scripts/check_environment.py --require-wheel
MOODPY_TEST_INSTALLED=1 /tmp/moodpy-wheel-check/bin/python -m pytest
/tmp/moodpy-wheel-check/bin/python examples/agent_workflow/author_bank.py --seed 42 --samples 2 --output artifacts/wheel-bank
```

`MOODPY_TEST_INSTALLED=1` prevents the test configuration from inserting `src/` on
the import path. The environment checker also rejects editable or repository source
imports when `--require-wheel` is set. It checks dependencies, runtime/distribution
version agreement, and generation of all four core families. Source archives contain
the supported template, guidance, test suite, and Moodle compatibility harness;
they exclude historical archives and generated outputs.

For actual Moodle testing, follow the
[compatibility runner instructions](moodle-import-checklist.md). Recorded local
runs passed on Moodle 4.5 and 5.0–5.2; report exact tested revisions, and distinguish
them from checks in Python and from the manual web-interface checklist.

Record changes under `Unreleased` in `CHANGELOG.md`. Package metadata and
`moodpy.__version__` must agree; the current version is 3.0.1. Commit related changes
in logical chunks. GitHub publishing is gated by package tests, bank smoke checks,
generator tests, and Moodle compatibility jobs. Creating tags, GitHub releases, or
publishing packages requires an explicit release request; retired deployment and
GitHub scripts are retained only for historical reference.

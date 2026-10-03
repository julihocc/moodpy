# Working with MoodPy

MoodPy turns Python question recipes into a reproducible Moodle question-bank
bundle. Start with [the authoring guide](docs/authoring-guide.md).

## Creating educational content

1. Read the authoring guide and [verified recipe catalog](docs/verified-recipes.md).
2. Establish objectives, audience, language, topics, family counts, bounds,
   tolerances, and feedback expectations with the educator. Save decisions in brief.md.
3. Copy examples/agent_workflow/author_bank.py and its brief into a working folder.
   Use the installed package and injected RNG; keep family IDs stable.
4. Draft representative questions with solutions and discuss them with the educator.
   Incorporate feedback before generating the requested full bank. Existing explicit
   instructions or completed reviews carry forward; do not ask repeatedly.
5. Build, validate, and export through build_bank(). Deliver the XML, teacher
   preview, manifest, sources, import instructions, and ZIP.
6. Report local validation separately from a successful live Moodle import.

The verified catalog is the supported starting point. The [generator catalog](generators/CATALOG.md)
lists migrated recipes with mathematical tests; read generators/README.md for setup.
Examples in examples/legacy/, archived generator notebooks, and library/ are legacy references
requiring independent verification. Do not
execute arbitrary legacy scripts or use txt2arr() on untrusted input. Recipes are
trusted executable Python, not a sandboxed data format.

## Maintaining the package

- Read [the development guide](docs/development.md) and [architecture](docs/architecture.md).
- Preserve existing public interfaces. Keep library tests independent of submodules.
- Leave existing local changes and submodule contents untouched unless specifically requested.
- Core reliability checks: python -m unittest tests.test_bank; full suite: pytest.
  Install the package with python -m pip install -e '.[dev]' first.
- Test constraints, feedback freshness, reproducibility, answer syntax, XML, and
  bundle regeneration whenever changing the authoring workflow.
- Verify the built wheel with MOODPY_TEST_INSTALLED=1 so repository source imports
  cannot hide missing packaged modules.
- Record changes under Unreleased. Keep pyproject.toml and runtime versions aligned.
- Do not publish, upload to Moodle, or run scripts/legacy/create_github_issues.sh
  as a side effect of authoring or testing.

README.md and [the documentation index](docs/README.md) describe the current layout.
Keep generated outputs in artifacts/. Historical migration plans and status
documents in docs/archive/, examples/legacy/, and scripts/legacy/ are background,
not executable instructions. Preserve archival source content when reorganizing it.

# MoodPy architecture

The public package lives in `src/moodpy/`. Its imports and existing `Generator`,
`Cloze`, financial, graphics, and tools interfaces remain available. The supported
authoring workflow uses these modules:

| Module | Responsibility |
|---|---|
| `generator.py` | Parameter sampling, derived values, constraints, exercise and feedback rendering |
| `tools.py` | Numerical and short-answer Cloze helpers, plus legacy utilities |
| `bank.py` | Typed question families, reproducible generation, snapshots, validation, bundle export |
| `recipes.py` | Four verified core recipe factories |
| `cloze.py` | Existing batch and preview interface sharing the generator's sampling logic |

`build_bank()` derives an independent NumPy random stream from the bank seed and
each stable family ID. The family factory creates a `Generator` using that stream;
its rendering callback writes the exercise and feedback after valid parameters
have been sampled. Constraint rejections and duplicate question texts consume a
bounded attempt budget for each variant.

The resulting bank stores rendered snapshots and parameter values. Validation,
XML generation, HTML preview, and bundle export read those snapshots without
sampling again. Each export includes source files, hashes, runtime versions, and
regeneration instructions. See the [authoring guide](authoring-guide.md) for the
API contract, supported answer syntax, and error handling.

`tests/` covers core behavior without either Git submodule. The compatibility
harness in `.github/moodle/` exercises Moodle's actual importer and grader; the
Python test suite alone cannot establish a successful Moodle import.

`examples/agent_workflow/` is the portable supported template. Historical examples
live in `examples/legacy/`, old plans in `docs/archive/`, and retired maintenance
scripts in `scripts/legacy/`. These archives are excluded from source releases.
The `generators/` and `library/` repositories retain their own layouts and histories.
Generated banks and other local outputs belong in the ignored `artifacts/` folder.

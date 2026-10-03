# MoodPy

Create parametric Moodle question banks with an educator and an agent. Agree on
the learning goals, review representative questions together, then generate
randomized variants with reusable Python sources.

Start with [AGENTS.md](AGENTS.md), [the authoring guide](docs/authoring-guide.md),
and [verified recipes](docs/verified-recipes.md).

## Install

From a matching repository checkout, using Python 3.8 or newer:

```bash
python -m pip install -e '.[dev]'
```

Dependencies are NumPy, matplotlib, tabulate, and SciPy. The agent needs workspace
access and Python execution. Git submodules and an OpenAI API key are not required
for the supported authoring workflow.

## Generate a reviewed question-bank bundle

The portable template contains arithmetic, algebra, compound-interest, and
short-answer families. Copy it and its brief into your authoring folder, adapt
them to the educator's decisions, and review sample questions before bulk generation.

```bash
python examples/agent_workflow/author_bank.py --seed 42 --samples 2 --output artifacts/sample
python examples/agent_workflow/author_bank.py --seed 42 --output artifacts/full-bank
```

The full example produces 40 questions with topic categories. Each bundle includes:

- bank.xml for Moodle question-bank import.
- preview.html with blanks and expandable teacher solutions.
- manifest.json with counts, seed, versions, sampled parameters, validation, and source hashes.
- sources/ with the Python recipe and brief.md.
- README.md with regeneration and import instructions, plus bundle.zip for delivery.

The preview contains teacher answers. XML and preview use the same saved questions;
export does not resample. Local checks validate supported syntax and XML structure,
not educational suitability or mathematical truth. CI is configured to import a generated bank
into disposable Moodle instances (4.5 LTS and 5.0–5.2) and check Moodle's Cloze grader
against independently calculated answers for the four core recipes and all 31
migrated generator families. [Recorded local Moodle runs](docs/moodle-compat-results/2026-10-03/README.md)
passed on all four branch snapshots: 101 questions and 266 answer fields per version.
Publishing still requires the compatibility CI jobs to pass.
The [manual checklist](docs/moodle-import-checklist.md) covers the web-interface path
and remains useful for checking a specific Moodle installation.

## Python interface

The [generator submodule](generators/README.md) also provides 31 migrated notebook
topics with independent mathematical tests and a portable bank CLI. Its
[catalog](generators/CATALOG.md) indexes all original notebooks and distinguishes
working replacements from unfinished templates and scratch references.

```python
from moodpy import build_bank
from moodpy.recipes import arithmetic_family, linear_equations_family

bank = build_bank(
    [arithmetic_family(10), linear_equations_family(10)],
    title="Algebra practice",
    seed=42,
)
print(bank.validate())
```

Supply your own QuestionFamily(id, title, category, count, generator_factory,
exercise_fn, tags=()). The factory receives a NumPy RNG and returns a Generator.
The callback sets the exercise and feedback from its current parameters. Use NM()
and STxt() for supported Cloze fields and template=False for fully rendered text.

Export with bank.export_bundle(output_dir, source_files=[recipe_path, brief_path]).
Sources must include a Python recipe and brief.md. Existing bundles require explicit
overwrite=True; unrelated files are preserved. Independent family seeds preserve
sample prefixes when other counts change. Identical reproduction requires unchanged
sources, dependency versions, and use of the injected RNG.

See the authoring guide for the full API, CLI regeneration contract, constraints,
tolerances, literal mathematical braces, and failure handling.

## Existing library users

Generator, Cloze, NM, STxt, tools, matfin, and graphics remain available. Legacy
Cloze batches and previews now enforce requirements and refresh feedback templates.
Requirements must be callables or booleans; string requirements raise an error.
Missing template values also raise errors instead of silently exporting unresolved text.

The new bank API supports numerical and short-answer Cloze fields emitted by NM()
and STxt(). Other question types, connected tools, automated Moodle uploads, and
quiz-activity configuration are outside this milestone.

## Repository and verification

src/moodpy/ contains the library and verified recipes. examples/agent_workflow/
contains the portable template. tests/ covers legacy behavior and the new workflow.
Other examples and the generators/ and library/ submodules are legacy references
requiring independent verification; they are not a catalog of working recipes.

```bash
pytest
python -m unittest tests.test_bank
```

CI tests Python 3.8–3.14 using an installed wheel, then runs a bank smoke check.
Publishing requires those checks. Do not initialize submodules just to run core tests.

MoodPy uses the MIT license. Contributions should preserve the public API, update
canonical guidance, and include regressions for changes to generation or export.

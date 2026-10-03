# Verified recipe catalog

These factories are shipped in moodpy.recipes and exercised by mathematical and
export regressions in tests/test_bank.py. Run them through the portable CLI at
examples/agent_workflow/author_bank.py. Verification covers local generation,
solutions, and XML structure. Separately, [recorded Moodle runs](moodle-compat-results/2026-10-03/README.md)
verified the actual importer and grader on Moodle 4.5 and 5.0–5.2.

| Factory | Objective | Answer policy | Default category |
|---|---|---|---|
| arithmetic_family(count=10) | Add distinct integers from 1–99 | Exact integer | Mathematics/Arithmetic |
| linear_equations_family(count=10) | Solve ax+b=c with a and x nonzero | Exact integer | Mathematics/Algebra |
| compound_interest_family(count=10) | Calculate annual compound growth | Cents, 0.1% relative tolerance | Finance/Compound interest |
| short_answer_family(count=10) | Classify an integer by sign | Case-insensitive positive/negative/zero | Mathematics/Short answer |

Use these as starting points, not an automatically suitable assessment for every
learner. Adapt the wording, objectives, bounds, counts, and tolerance with the educator.

## Legacy references

Scripts in examples/legacy/ and archived notebooks in generators/ or library/ require
independent verification before reuse. Some contain Sage syntax, missing dependencies,
old Moodle APIs, or migration TODOs. Several do not parse as Python. Their presence
is not a claim that they run or produce correct questions.

The historical arithmetic, linear-equation, and compound-interest demos can be used
for comparison, but the catalog above defines the supported agent workflow.
Advanced financial helpers are not certified by this milestone; the compound-interest
recipe calculates its formula directly. Do not reuse txt2arr() with untrusted input.

Do not initialize or modify submodules merely to author a question bank. Keep
independently reviewed adaptations as new Python recipes and record their sources
and educational assumptions in the quiz brief.

## Migrated notebook recipes

The separate [generator package](../generators/README.md) adds 31 mathematically
tested families from the teaching notebooks. Its [catalog](../generators/CATALOG.md)
maps every original notebook to a replacement, scratch reference, or unfinished
template. Install this MoodPy checkout and the generator package before use.
The recorded Moodle compatibility runs also cover all 31 migrated families.
Python-only checks and successful live Moodle imports remain distinct evidence.

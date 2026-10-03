# Create a Moodle question bank with an agent

An educator and an agent design the assessment together. The educator supplies
learning goals and reviews questions; the agent writes and runs Python recipes.
MoodPy produces a reusable question bank for Moodle import.

## Set up the workspace

Give the agent access to this repository or install its matching package version:

```bash
python -m pip install -e '.[dev]'
python scripts/check_environment.py
```

Python 3.8 or newer is supported. Dependencies must be available in the workspace;
network restrictions may prevent installation. No OpenAI API key or connected
Moodle account is required. ChatGPT Work can use files and code tools available
in its execution environment; actual access depends on workspace settings.
[Official Work documentation](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview)

The core authoring workflow needs neither Git submodule. Other agentic apps can
follow the same guide through Python execution.

## Agree on the quiz brief

Create brief.md beside the Python recipe. Record:

| Decision | What to establish |
|---|---|
| Learning objectives | What learners should demonstrate |
| Audience and difficulty | Prior knowledge, learner level, progression |
| Language | Wording, accepted short answers, units and notation |
| Topics and counts | Stable family IDs, topic categories, variants per family |
| Parameter bounds | Distributions and constraints that keep questions valid |
| Answer policy | Exact or approximate answers, tolerance, rounding and units |
| Feedback | Explanations, worked solutions, misconceptions to address |
| Review | Educator feedback and the revisions incorporated |

A family is one question pattern with randomized variants. Ten variants of four
families create 40 bank questions; this does not itself configure a 40-question
Moodle quiz. Distinguish the bank size from intended quiz selection.

## Draft representative questions together

Start from [verified recipes](verified-recipes.md). Copy
examples/agent_workflow/author_bank.py and brief.md into a working folder, then run:

```bash
python author_bank.py --seed 42 --samples 2 --output artifacts/sample
```

Show representative questions, answers, and explanations to the educator. Discuss
content, mathematical validity, difficulty, wording, tolerances, and ambiguous
answers. Revise the recipe and brief from the discussion, then generate the agreed
counts. Reuse earlier review decisions instead of restarting the conversation.

An example prompt for the agent:

> Help me design a Spanish algebra quiz for first-year students. I want three
> question families and ten variants per family. Review representative questions
> and worked solutions with me before generating a Moodle bank. Save the recipe
> and decisions so we can revise the quiz later.

## Write a Python recipe

The stable interface separates question design, generation, and export:

```python
from pathlib import Path
from moodpy import build_bank
from moodpy.recipes import arithmetic_family, linear_equations_family

bank = build_bank(
    [arithmetic_family(count=10), linear_equations_family(count=10)],
    title="Algebra practice",
    seed=42,
)
bank.validate().raise_for_errors()
paths = bank.export_bundle(
    "artifacts/algebra",
    source_files=[Path(__file__), Path(__file__).with_name("brief.md")],
)
print(paths.archive)
```

For new content, create a QuestionFamily(id, title, category, count,
generator_factory, exercise_fn, tags=()). The factory receives a NumPy RNG and
returns a Generator; the rendering callback receives the current Generator.
Use the factory's RNG in parameter lambdas. Define derived values in dependency
order and callable requirements for valid combinations.

```python
from moodpy import Generator, QuestionFamily, NM

def factory(rng):
    gen = Generator()
    gen.lambdas = {"a": lambda _: int(rng.integers(2, 20))}
    gen.derived = {"answer": lambda d: d["a"] ** 2}
    gen.requirements = [lambda: gen.parameters["answer"] < 300]
    return gen

def render(gen):
    d = gen.parameters
    gen.set_exercise(
        f"<p>Square {d['a']}: {NM(d['answer'], entero=True)}</p>",
        template=False,
    )
    gen.set_feedback(f"<p>{d['a']}² = {d['answer']}.</p>", template=False)

squares = QuestionFamily("squares", "Integer squares", "Algebra/Squares",
                         5, factory, render, tags=("powers",))
```

Use template=False for fully rendered strings, including literal LaTeX braces.
The legacy template mode remains available for `{d[key]}` placeholders and raises
errors for missing values. Derived answer strings may be inserted through such
slots; do not freeze an answer before sampling a batch.

Rules for dependable recipes:

- Use NM() for numerical fields and STxt() for one case-insensitive short answer.
  Use general feedback for explanations; alternatives and inline answer feedback
  are outside the supported bank subset.
- STxt() preserves literal punctuation through HTML entities and escapes literal
  asterisks, so an asterisk does not become an accept-any-response wildcard.
  This follows Moodle's [Cloze decoder](https://github.com/moodle/moodle/blob/MOODLE_405_STABLE/question/type/multianswer/questiontype.php)
  and [short-answer matcher](https://github.com/moodle/moodle/blob/MOODLE_405_STABLE/question/type/shortanswer/question.php).
- NM(error=...) sets relative tolerance: abs(answer) × error. Percent mode converts
  0.85 to 85 percentage points. Integer mode uses an exact integer answer.
- Do not use string requirements, ambient random state, clocks, or unbounded loops.
  Attempt budgets bound sampling and duplicates; they cannot interrupt user callbacks.
- Set complete question text and any feedback for every rendering. Callback feedback
  is cleared between candidates. Requirements apply before rendering.
- Keep parameters as finite JSON-compatible values. NumPy arrays/scalars are
  normalized; convert symbolic objects explicitly for the manifest.
- Provide enough distinct variants within the bounds. Constraint rejections and
  duplicate rendered text share the per-variant attempt limit (default 10,000).
- Category paths are relative to the course, such as Algebra/Equations. IDs contain
  letters, numbers, hyphens, or underscores and must remain stable across revisions.
- Mathematical correctness requires recipe checks and educator review. Structural
  validation cannot prove that a solution is correct.

## Generate and deliver the bundle

The template accepts --seed and --output. --samples or --count optionally overrides
all family counts; customize make_families() for different counts by topic.

```bash
python author_bank.py --seed 42 --output artifacts/full-bank
```

The exported directory contains bank.xml, preview.html, manifest.json, README.md,
sources/, and bundle.zip. Provide the ZIP and direct preview/XML links to the
educator where the agent app supports file delivery.

Preview, validation, and export use saved snapshots without resampling. The offline
HTML preview replaces answer fields with blanks and offers expandable teacher
solutions. It includes answers and must be treated as teacher material. LaTeX
remains visible source notation in this preview; Moodle renders mathematics through
its configured filters. New banks use the existing 0.5 question penalty convention;
quiz settings remain a Moodle responsibility.

Local checks validate metadata, supported answer fields, placeholders, distinctness,
counts, finite snapshots, and well-formed XML. Errors identify a family and variant.
An invalid or incomplete bank is rejected before export. Overwriting an existing
bundle requires --overwrite (or overwrite=True); unrelated files are preserved.

## Revise or regenerate later

Keep family IDs and the seed to preserve representative variants when increasing
counts. Each family has its own stream, so other families' counts/order do not
change its variants. Reproduction assumes the same recipe, Python/NumPy/MoodPy
versions, and injected RNG use; manifest.json records versions and source hashes.

From the exported directory:

```bash
python sources/author_bank.py --manifest manifest.json --seed 42 --output regenerated-bank
```

The --manifest option restores exported counts, title, seed, and attempt budget.
Custom recipes should preserve this CLI contract. Edit sources/brief.md and the
recipe for a revision, then export to a new directory and review the changes.

Import bank.xml through the Moodle question bank's Import screen with category
import enabled. Follow the [manual import checklist](moodle-import-checklist.md).
An XML import adds bank questions; create and configure the quiz activity separately.
A local validation pass must never be reported as a successful live Moodle import.

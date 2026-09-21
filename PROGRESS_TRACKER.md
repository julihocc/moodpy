# MoodPy Progress Tracker

**Last updated:** 2026-09-21  
**Default branch:** `main`  
**Package version on main:** `3.0.1` (prepared; GitHub Release / production PyPI postponed)

## Current status

MoodPy is a modern `src/moodpy/` package that generates parametric Moodle cloze questions and exports Moodle XML. Core engine fixes from 2026-06-30 (batch generation, lambda requirements, NumPy 1.24+, `fig2str`, `exercise_fn`) are on `main` and documented under CHANGELOG `[3.0.1]`.

| Area | State |
|------|--------|
| Package layout | `src/moodpy/` (generator, cloze, tools, matfin, graphics) |
| Tests | 78/78 passing locally; CI on push/PR (Python 3.10–3.13) via `.github/workflows/test.yml` |
| Coverage | ~70% overall (strong on generator/cloze; weaker on graphics/matfin/tools) |
| Examples | 62 scripts under `examples/` (math, stats, finance, engineering, …) |
| TestPyPI | `moodpy` 3.0.0 present |
| Production PyPI | Not published yet (issue #5) |
| Docs site | ReadTheDocs URL retired; use GitHub README |
| Submodules | `generators/` → moodpy-generators; `library/` → moodpy-library (need `git submodule update --init`) |

## Recently completed

- **PR #12** — CI test workflow + prepare 3.0.1 version/changelog (issue #4 closed)
- **PR #13** — Repo hygiene: description/topics, remove TESTING artifacts, gitignore, docs URL (issue #7 closed)
- **2026-06-30** — Engine bugfixes + docs (see CHANGELOG 3.0.1)

## Open work (GitHub)

### Paused (publish)

- [#3](https://github.com/julihocc/moodpy/issues/3) Cut GitHub Release `v3.0.1`
- [#5](https://github.com/julihocc/moodpy/issues/5) Publish to production PyPI (`PYPI_API_TOKEN` required)

### P1

- [#6](https://github.com/julihocc/moodpy/issues/6) Refresh trackers (this document)
- [#8](https://github.com/julihocc/moodpy/issues/8) Document/verify git submodules

### P2

- [#9](https://github.com/julihocc/moodpy/issues/9) Advanced mathematics generator migration
- [#10](https://github.com/julihocc/moodpy/issues/10) Raise coverage on graphics / matfin / tools
- [#11](https://github.com/julihocc/moodpy/issues/11) Clear Sage → MoodPy TODOs in examples

## Historical note

Older copies of this file (Sep 2025) tracked a “70/136 generators / Phase 7” migration on branch `refactora-as-package`. That branch is obsolete; **`main` is the source of truth.** Generator migration continues via issues #9–#11 rather than the old phase checklist.

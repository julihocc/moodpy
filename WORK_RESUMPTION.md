# MoodPy work resumption

**Last updated:** 2026-09-21  
**Work from:** `main` only (ignore old paths like `refactora-as-package` or personal worktree dirs)

## Quick start

```bash
git clone --recurse-submodules https://github.com/julihocc/moodpy.git
cd moodpy
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

Smoke check:

```bash
python -c "from moodpy import Generator, Cloze; print('MoodPy OK')"
```

## What’s true on main right now

- Version in `pyproject.toml`: **3.0.1**
- CI: `.github/workflows/test.yml` (3.10–3.13)
- Publish: `.github/workflows/publish.yml` on GitHub Release (needs `PYPI_API_TOKEN`)
- Publishing to production PyPI is **postponed** until the token is configured

## Suggested next tasks

1. [#8](https://github.com/julihocc/moodpy/issues/8) — submodule docs/verification  
2. [#9](https://github.com/julihocc/moodpy/issues/9) / [#11](https://github.com/julihocc/moodpy/issues/11) — content migration & Sage cleanup  
3. When ready: [#3](https://github.com/julihocc/moodpy/issues/3) + [#5](https://github.com/julihocc/moodpy/issues/5) — Release `v3.0.1` + PyPI  

Do **not** run the old `./create_github_issues.sh` (stale 2025 milestones). Live backlog is the open GitHub issues above.

## Useful docs

- `README.md` — usage (Pattern A / Pattern B)
- `CHANGELOG.md` — 3.0.1 engine fixes
- `ARCHITECTURE.md` / `DEVELOPMENT.md` — deeper design and contributing
- `PROGRESS_TRACKER.md` — status snapshot

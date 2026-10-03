---
mode: agent
---

Read AGENTS.md and docs/development.md. For an explicitly requested package
publication, use the gated .github/workflows/publish.yml workflow. Check the
requested target (TestPyPI or PyPI), release version, and successful package, bank,
generator, and Moodle compatibility jobs. Do not use scripts/legacy/ deployment
scripts, bypass release gates, commit build artifacts, or change account credentials.
Tagging and GitHub release publication must stay within the user's authorization.

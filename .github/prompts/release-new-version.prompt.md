---
mode: agent
---

Read AGENTS.md and docs/development.md. Prepare release notes and validate the
requested version against package/runtime metadata. Confirm the release commit
passes package, bank, generator, and Moodle compatibility checks. Create or publish
a GitHub release only within the user's authorized scope. The publishing workflow
uses a published release to publish to PyPI; account for that effect before
publishing the release. Do not bypass failing release gates or include build artifacts
in Git commits.

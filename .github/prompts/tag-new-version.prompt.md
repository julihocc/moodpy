---
mode: agent
---

Read AGENTS.md and docs/development.md. Use the release version explicitly
requested by the user. Update package/runtime versions together, refresh relevant
release documentation, and run package and bank checks before creating the tag.
Preserve unrelated worktree and submodule edits. Push tags only when authorized.
Do not create a GitHub release or publish packages as a side effect of tagging.

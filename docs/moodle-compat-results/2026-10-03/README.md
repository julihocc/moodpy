# Real Moodle compatibility results — 2026-10-03

All four stable-branch snapshots passed imports and grading in disposable, actual
Moodle installations using PHP 8.3.35 and PostgreSQL 16.15. These runs were executed
locally with Docker Desktop's Linux engine. They are independent of GitHub Actions;
no successful CI run or browser import is claimed here.

| Branch | Reported release | Moodle commit | Outcome |
| --- | --- | --- | --- |
| 4.5 | 4.5.15 (Build: 20261005) | [215f4438](https://github.com/moodle/moodle/commit/215f44380bdc3ccf852a3a22e34f8423ff64033a) | [Passed, 2,933 assertions](4.5/moodpy-moodle-compat-junit.xml) |
| 5.0 | 5.0.11 (Build: 20261005) | [744cc0c1](https://github.com/moodle/moodle/commit/744cc0c19013e7be831dca24fafd6501d7eb8348) | [Passed, 2,933 assertions](5.0/moodpy-moodle-compat-junit.xml) |
| 5.1 | 5.1.8 (Build: 20261005) | [cc0bf17d](https://github.com/moodle/moodle/commit/cc0bf17da8b5fbd290faf95b2b14a03d64331923) | [Passed, 2,933 assertions](5.1/moodpy-moodle-compat-junit.xml) |
| 5.2 | 5.2.4 (Build: 20261005) | [2df605b1](https://github.com/moodle/moodle/commit/2df605b1e093248e8f8d1e2fc081fb3b1f65665f) | [Passed, 2,933 assertions](5.2/moodpy-moodle-compat-junit.xml) |

Release strings come from each checked-out branch's `version.php`, including the
upcoming build date. The commit links identify the exact snapshots tested; these
results do not establish compatibility with every historical patch release.

Each version imported the same two banks: four core families with eight questions,
and all 31 migrated generator families with 93 questions. Together these contain
101 questions and 266 embedded answer fields. Moodle verified category hierarchies,
counts, names, tags, feedback, field types, independently calculated correct
answers, incorrect answers, case-insensitive short answers, and responses inside
and outside numerical tolerances. Each version passed two tests with 2,933 assertions,
zero failures, zero errors, and zero skipped tests.

[summary.json](summary.json) records versions, revisions, fixture counts, seed,
dependency versions, and SHA-256 hashes. The `fixtures/` directory preserves the
exact XML, manifest, and independent expectations used by every version. Per-version
directories contain the unmodified PHPUnit report and runtime/revision reports.
The engine wheel matched all eight current engine Python source files. The generator
wheel was also tested from a clean committed source snapshot; 14 generator tests
passed. The core installed-wheel suite passed 97 tests, with nine optional graphics
tests skipped because Matplotlib was absent. Local Python was 3.14.4; the advertised
3.8–3.14 CI matrix is configured but has not been executed in this local session.

The test harness setup was corrected during these runs: maturity constants for
version reporting, explicit test-category creation, newer Moodle CLI paths, and TCP
PostgreSQL readiness. The final category setup was copied into each disposable
site before its PHPUnit test began. The mathematical grading assertions and bank
fixtures remained unchanged.

Repeat these checks using [the local runner instructions](../../moodle-import-checklist.md#repeat-the-server-checks-locally).
The [manual checklist](../../moodle-import-checklist.md) still covers the browser
import form, visual mathematics, site-specific configuration, and quiz activity setup.
All test containers, test volumes, and test networks were removed after the runs.

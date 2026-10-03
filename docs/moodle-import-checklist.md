# Manual Moodle import check

The compatibility workflow in `.github/workflows/moodle-compat.yml` is configured to create
disposable Moodle sites for 4.5 LTS and 5.0–5.2, import the representative bank with
Moodle's `qformat_xml` importer, and check stored question categories, tags,
feedback, answer fields, numerical tolerance, and correct/incorrect grading against
answers calculated independently from the recipe inputs. It checks full category
paths and values inside and outside numerical tolerances. Each version imports the
four core MoodPy recipes and all 31 migrated generator families, including questions
with multiple numerical and short-answer fields. Grading expectations come from
independent mathematical calculations, with the manifest hash checked to prevent
mixing fixtures. This is
server-side integration coverage; it does not exercise the browser import form or
prove compatibility with every Moodle theme, plugin, database, or site setting.

No existing Moodle installation or educator credentials are needed. Push the
generator submodule commits to its remote before pushing the containing repository
to GitHub, then open **Actions → Moodle import compatibility →
Run workflow**. It also runs for pull requests and pushes to main. With an authenticated
GitHub CLI, the equivalent commands are:

```bash
gh workflow run moodle-compat.yml --ref main
gh run list --workflow moodle-compat.yml
gh run view RUN_ID --log-failed
gh run download RUN_ID
```

The four version jobs run independently. A version is verified only when its
**Import the bank and grade Cloze answers with Moodle** step passes. A setup failure
does not establish an import failure or a successful compatibility check. Download
the reports to retain the PHPUnit result, exact Moodle/PHP version, Moodle and Docker
repository commits, and bank manifest. Stable branches advance, so record the exact
commit tested rather than claiming that all historical patch releases passed.

## Repeat the server checks locally

A running Linux Docker engine is sufficient; no existing Moodle site or account
is needed. Install the current engine and migrated recipes, generate both banks,
then calculate their independent grading expectations:

```bash
python -m pip install . './generators[test]'
python examples/agent_workflow/author_bank.py --seed 42 --samples 2 --output artifacts/core-bank
python -m moodpy_generators --seed 42 --count 3 --output artifacts/migrated-bank
python .github/moodle/generate_expectations.py --bank artifacts/core-bank
python .github/moodle/generate_expectations.py --bank artifacts/migrated-bank --generator-tests generators/tests
python .github/moodle/run_local.py --core-bank artifacts/core-bank \
  --migrated-bank artifacts/migrated-bank --output artifacts/moodle-reports
```

Use `--versions 4.5` to run one branch. The default runs 4.5 and 5.0–5.2. From
WSL without Docker integration, `--docker /path/to/docker.exe` uses Windows Docker
Desktop's Linux engine. The runner transfers files through stdin and named volumes,
so host bind-path conversion is unnecessary. It downloads public Moodle code and
dependencies, creates isolated test containers, and removes only its own containers,
volumes, and networks. It saves logs, PHPUnit XML, exact runtime and revision
reports, and copies of both banks with their manifests and grading expectations.
Each output directory must be new.

[Recorded local runs](moodle-compat-results/2026-10-03/README.md) passed the real
importer and grader on all four stable-branch snapshots on 2026-10-03, using 101
questions and 266 answer fields per version. The retained reports identify the exact
commits, runtime versions, fixtures, and assertions. These results came from local
Docker sites; GitHub Actions has not been run in this session. Publishing still
requires all four compatibility CI jobs to succeed.

The matrix uses PHP 8.3 and PostgreSQL 16, meeting the
[Moodle 5.2 server requirements](https://moodledev.io/general/releases/5.2#server-requirements).

Record the Moodle version, date, tester, bank seed, source hashes, and outcome.
This checklist is a live check performed by the educator or an authorized tester.
Do not mark it complete merely because local XML validation passed.

1. Import bank.xml in the course question bank using Moodle XML and enable
   **Get category from file**.
2. Compare imported category paths and question counts with manifest.json.
3. Preview representative questions from each family, including boundary values.
4. For numerical fields, submit the correct answer and values just inside/outside
   the declared tolerance. Check units, rounding, percentages, and integer answers.
5. For short answers, submit the accepted text, a differently cased equivalent,
   and an incorrect answer. Check reserved characters if the recipe uses them.
6. Check Spanish/Unicode content, mathematical rendering, and general feedback.
7. Create a quiz activity separately, select questions from the imported bank,
   and configure grade, timing, attempts, and feedback visibility as intended.
8. Record failures and revise the Python recipe or report the issue. Regenerate
   the bank, reimport, and repeat affected checks.

Reference: [Moodle XML format](https://docs.moodle.org/405/en/Moodle_XML_format).

Manual browser check: **Not performed** in this session. Record the actual outcome
when completing this checklist. Automated server checks confirm only the recorded
Moodle snapshots and covered import/grading path.

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

No existing Moodle installation or educator credentials are needed. After committing
and pushing the workflow to GitHub, open **Actions → Moodle import compatibility →
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

The workflow currently has no recorded successful Moodle run in this repository.
Local Python tests and XML parsing do not change that status. Publishing requires
all four compatibility jobs to succeed.

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

Result: **Not performed** until the tester records the actual outcome. Automated CI
results confirm only the covered Moodle branches and import path.

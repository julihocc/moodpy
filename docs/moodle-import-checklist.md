# Manual Moodle import check

Automated compatibility coverage in `.github/workflows/moodle-compat.yml` creates
disposable Moodle sites for 4.5 LTS and 5.0–5.2, imports the representative bank with
Moodle's `qformat_xml` importer, and checks stored question categories, tags,
feedback, answer fields, numerical tolerance, and correct/incorrect grading. This is
server-side integration coverage; it does not exercise the browser import form or
prove compatibility with every Moodle theme, plugin, database, or site setting.

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

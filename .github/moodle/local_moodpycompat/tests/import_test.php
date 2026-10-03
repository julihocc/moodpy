<?php
// This file is copied into a disposable Moodle checkout by moodle-compat.yml.
namespace local_moodpycompat;

defined('MOODLE_INTERNAL') || die();

global $CFG;
require_once($CFG->libdir . '/questionlib.php');
require_once($CFG->dirroot . '/question/format.php');
require_once($CFG->dirroot . '/question/format/xml/format.php');

/** Import and grade an actual MoodPy bundle using Moodle's own code. */
final class import_test extends \advanced_testcase {
    public function test_bundle_imports_and_grades_in_moodle(): void {
        $this->assert_bank_imports_and_grades(__DIR__ . '/fixtures/core');
    }

    public function test_migrated_topics_import_and_grade_in_moodle(): void {
        $this->assert_bank_imports_and_grades(__DIR__ . '/fixtures/migrated');
    }

    private function assert_bank_imports_and_grades(string $fixture): void {
        global $DB;

        $this->resetAfterTest();
        $this->setAdminUser();

        $manifest = json_decode(
            file_get_contents($fixture . '/manifest.json'),
            true,
            512,
            JSON_THROW_ON_ERROR
        );
        $expectations = json_decode(file_get_contents($fixture . '/expectations.json'), true, 512, JSON_THROW_ON_ERROR);
        $this->assertSame('moodpy-moodle-expectations-v1', $expectations['format']);
        $this->assertSame(hash_file('sha256', $fixture . '/manifest.json'), $expectations['manifest_sha256']);
        $expectedcount = count($manifest['questions']);
        $this->assertGreaterThan(0, $expectedcount, 'The MoodPy fixture must contain questions.');

        $course = $this->getDataGenerator()->create_course();
        // A quiz module exists throughout the covered Moodle versions and has a
        // genuine module-level question bank context in each of them.
        $quiz = $this->getDataGenerator()->create_module('quiz', ['course' => $course->id]);
        $modulecontext = \context_module::instance($quiz->cmid);
        $category = $this->getDataGenerator()->get_plugin_generator('core_question')->create_question_category([
            'contextid' => $modulecontext->id,
        ]);

        $format = new \qformat_xml();
        $format->setContexts([
            \context_course::instance($course->id),
            $modulecontext,
        ]);
        $format->setCourse($course);
        $format->setCategory($category);
        $format->setFilename($fixture . '/bank.xml');
        $format->setRealfilename('bank.xml');
        $format->setMatchgrades('error');
        $format->setCatfromfile(true);
        // Match the documented import workflow: read categories from the file,
        // while keeping them in the selected question bank context.
        $format->setContextfromfile(false);
        $format->setStoponerror(true);
        $format->set_display_progress(false);

        ob_start();
        try {
            $imported = $format->importprocess();
        } finally {
            $importoutput = ob_get_clean();
        }
        $this->assertTrue($imported, "Moodle's Moodle XML importer rejected bank.xml:\n" . $importoutput);
        $this->assertSame(0, $format->importerrors, $importoutput);
        $this->assertCount($expectedcount, $format->questionids, 'Moodle imported the wrong number of questions.');

        $questionids = array_map('intval', $format->questionids);
        $records = $DB->get_records_list('question', 'id', $questionids);
        $this->assertCount($expectedcount, $records);

        $expectedcategorycounts = [];
        $families = [];
        $snapshots = [];
        foreach ($manifest['families'] as $family) {
            $families[$family['id']] = $family;
            $expectedcategorycounts[$family['category']] = ($expectedcategorycounts[$family['category']] ?? 0)
                + $family['count'];
        }
        foreach ($manifest['questions'] as $snapshot) {
            $family = $families[$snapshot['family_id']];
            $name = sprintf('%s [%03d]', $family['title'], $snapshot['variant']);
            $snapshots[$name] = $snapshot;
        }
        $xml = simplexml_load_file($fixture . '/bank.xml');
        $this->assertNotFalse($xml);
        $feedback = [];
        foreach ($xml->question as $xmlquestion) {
            if ((string) $xmlquestion['type'] === 'cloze') {
                $feedback[(string) $xmlquestion->name->text] = trim((string) $xmlquestion->generalfeedback->text);
            }
        }
        ksort($expectedcategorycounts);
        $actualcategorycounts = [];
        $sawnumerical = false;
        $sawshortanswer = false;
        $sawtolerance = false;
        $sawcaseinsensitive = false;

        foreach ($questionids as $questionid) {
            $record = $records[$questionid];
            $this->assertSame('multianswer', $record->qtype);
            $this->assertArrayHasKey($record->name, $snapshots, 'Moodle changed or duplicated a question name.');
            $snapshot = $snapshots[$record->name];
            unset($snapshots[$record->name]);
            $family = $families[$snapshot['family_id']];
            $this->assertNotEmpty($record->generalfeedback, 'Imported teacher feedback must be present.');
            $this->assertSame($feedback[$record->name], trim($record->generalfeedback), 'Moodle changed the exported feedback.');

            // Since Moodle 4.0, categories belong to bank entries, not to question rows.
            $questioncategory = $DB->get_record_sql(
                'SELECT qc.*
                   FROM {question_categories} qc
                   JOIN {question_bank_entries} qbe ON qbe.questioncategoryid = qc.id
                   JOIN {question_versions} qv ON qv.questionbankentryid = qbe.id
                  WHERE qv.questionid = :questionid',
                ['questionid' => $questionid],
                MUST_EXIST
            );
            $this->assertSame((int) $modulecontext->id, (int) $questioncategory->contextid);
            $path = [];
            while ((int) $questioncategory->parent !== 0) {
                array_unshift($path, $questioncategory->name);
                $questioncategory = $DB->get_record('question_categories', ['id' => $questioncategory->parent], '*', MUST_EXIST);
            }
            $categorypath = implode('/', $path);
            $this->assertSame($family['category'], $categorypath);
            $actualcategorycounts[$categorypath] = ($actualcategorycounts[$categorypath] ?? 0) + 1;

            $tags = $DB->get_fieldset_sql(
                'SELECT t.rawname
                   FROM {tag_instance} ti
                   JOIN {tag} t ON t.id = ti.tagid
                  WHERE ti.component = :component
                    AND ti.itemtype = :itemtype
                    AND ti.itemid = :itemid',
                ['component' => 'core_question', 'itemtype' => 'question', 'itemid' => $questionid]
            );
            foreach ($family['tags'] as $tag) {
                $this->assertContains($tag, $tags, 'Moodle did not import this question\'s tag.');
            }

            $question = \question_bank::load_question($questionid);
            $this->assertInstanceOf(\qtype_multianswer_question::class, $question);
            $fields = $expectations['questions'][$snapshot['id']];
            $this->assertCount(count($fields), $question->subquestions, 'Moodle changed the expected answer field count.');

            foreach ($question->subquestions as $subquestion) {
                $type = $subquestion->qtype->name();
                $this->assertContains($type, ['numerical', 'shortanswer']);
                $sawnumerical = $sawnumerical || $type === 'numerical';
                $sawshortanswer = $sawshortanswer || $type === 'shortanswer';
            }

            // These values are independently calculated from the sampled inputs
            // by generate_expectations.py, never extracted from XML answer fields.
            $correct = [];
            $position = 0;
            foreach ($question->subquestions as $index => $subquestion) {
                $this->assertSame($fields[$position]['kind'], $subquestion->qtype->name());
                $correct['sub' . $index . '_answer'] = (string) $fields[$position]['answer'];
                $position++;
            }
            [$fraction] = $question->grade_response($correct);
            $this->assertEqualsWithDelta(1.0, (float) $fraction, 1.0e-9, 'Moodle rejected the independently calculated answer for ' . $record->name);

            $wrong = array_fill_keys(array_keys($correct), 'moodpy definitely incorrect');
            [$wrongfraction] = $question->grade_response($wrong);
            $this->assertLessThan(1.0, (float) $wrongfraction, 'Moodle awarded full credit for an incorrect response.');

            $position = 0;
            foreach ($question->subquestions as $index => $subquestion) {
                $expectedanswer = $fields[$position]['answer'];
                $expectedtolerance = $fields[$position]['tolerance'];
                $position++;
                if ($subquestion instanceof \qtype_shortanswer_question) {
                    $shortanswer = (string) $expectedanswer;
                    if ($shortanswer !== '' && strtolower($shortanswer) === $shortanswer
                            && strtoupper($shortanswer) !== $shortanswer) {
                        $uppercase = $correct;
                        $uppercase['sub' . $index . '_answer'] = strtoupper($shortanswer);
                        [$casefraction] = $question->grade_response($uppercase);
                        $this->assertEqualsWithDelta(
                            1.0,
                            (float) $casefraction,
                            1.0e-9,
                            'Moodle did not accept the short answer with changed casing.'
                        );
                        $sawcaseinsensitive = true;
                    }
                }

                if (!($subquestion instanceof \qtype_numerical_question)) {
                    continue;
                }
                foreach ($subquestion->answers as $answer) {
                    if ($answer->fraction >= 1.0) {
                        $delta = max(1.0e-7, abs((float) $expectedanswer) * 2.0e-8);
                        $this->assertEqualsWithDelta((float) $expectedanswer, (float) $answer->answer, $delta);
                        $this->assertEqualsWithDelta((float) $expectedtolerance, (float) $answer->tolerance, max(1.0e-9, $delta * 0.001));
                    }
                    if ($answer->fraction < 1.0 || $answer->tolerance <= 0) {
                        continue;
                    }
                    $within = $correct;
                    $within['sub' . $index . '_answer'] = (string) (
                        (float) $expectedanswer + $answer->tolerance / 2
                    );
                    [$withinfraction] = $question->grade_response($within);
                    $this->assertEqualsWithDelta(
                        1.0,
                        (float) $withinfraction,
                        1.0e-9,
                        'Moodle did not apply the exported numerical tolerance.'
                    );
                    $sawtolerance = true;
                    $outside = $correct;
                    $outside['sub' . $index . '_answer'] = (string) ($expectedanswer + $answer->tolerance * 2);
                    [$outsidefraction] = $question->grade_response($outside);
                    $this->assertLessThan(1.0, (float) $outsidefraction, 'Moodle awarded full credit outside the declared tolerance.');
                    [$subfraction] = $subquestion->grade_response(['answer' => $outside['sub' . $index . '_answer']]);
                    $this->assertEqualsWithDelta(0.0, (float) $subfraction, 1.0e-9, 'Moodle accepted an embedded answer outside its tolerance.');
                    break;
                }
            }
        }

        ksort($actualcategorycounts);
        $this->assertSame($expectedcategorycounts, $actualcategorycounts, 'Moodle imported questions into the wrong topic categories.');
        $this->assertEmpty($snapshots, 'Moodle missed a manifest question.');
        $this->assertTrue($sawnumerical, 'The fixture must exercise Moodle numerical Cloze fields.');
        $this->assertTrue($sawshortanswer, 'The fixture must exercise Moodle short-answer Cloze fields.');
        $this->assertTrue($sawtolerance, 'The fixture must exercise Moodle numerical tolerance grading.');
        $this->assertTrue($sawcaseinsensitive, 'The fixture must exercise Moodle short-answer casing.');
    }
}

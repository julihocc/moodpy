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
        global $DB;

        $this->resetAfterTest();
        $this->setAdminUser();

        $fixture = __DIR__ . '/fixtures';
        $manifest = json_decode(
            file_get_contents($fixture . '/manifest.json'),
            true,
            512,
            JSON_THROW_ON_ERROR
        );
        $expectedcount = count($manifest['questions']);
        $this->assertGreaterThan(0, $expectedcount, 'The MoodPy fixture must contain questions.');

        $course = $this->getDataGenerator()->create_course();
        // A quiz module exists throughout the covered Moodle versions and has a
        // genuine module-level question bank context in each of them.
        $quiz = $this->getDataGenerator()->create_module('quiz', ['course' => $course->id]);
        $modulecontext = \context_module::instance($quiz->cmid);
        $category = \question_get_default_category($modulecontext->id, true);

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
        // while keeping them in the selected course question bank context.
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

        $categorynames = [];
        $expectedcategorycounts = [];
        $expectedtags = [];
        foreach ($manifest['families'] as $family) {
            $path = explode('/', $family['category']);
            $categoryname = end($path);
            $categorynames[] = $categoryname;
            $expectedcategorycounts[$categoryname] = ($expectedcategorycounts[$categoryname] ?? 0)
                + $family['count'];
            $expectedtags = array_merge($expectedtags, $family['tags']);
        }
        ksort($expectedcategorycounts);
        $actualcategorycounts = [];
        $actualtags = [];
        $sawnumerical = false;
        $sawshortanswer = false;
        $sawtolerance = false;
        $sawcaseinsensitive = false;

        foreach ($questionids as $questionid) {
            $record = $records[$questionid];
            $this->assertSame('multianswer', $record->qtype);
            $this->assertNotEmpty($record->generalfeedback, 'Imported teacher feedback must be present.');

            $questioncategory = $DB->get_record(
                'question_categories',
                ['id' => $record->category],
                '*',
                MUST_EXIST
            );
            $this->assertContains($questioncategory->name, $categorynames);
            $actualcategorycounts[$questioncategory->name] =
                ($actualcategorycounts[$questioncategory->name] ?? 0) + 1;

            $tags = $DB->get_fieldset_sql(
                'SELECT t.rawname
                   FROM {tag_instance} ti
                   JOIN {tag} t ON t.id = ti.tagid
                  WHERE ti.component = :component
                    AND ti.itemtype = :itemtype
                    AND ti.itemid = :itemid',
                ['component' => 'core_question', 'itemtype' => 'question', 'itemid' => $questionid]
            );
            $actualtags = array_merge($actualtags, $tags);

            $question = \question_bank::load_question($questionid);
            $this->assertInstanceOf(\qtype_multianswer_question::class, $question);
            $this->assertNotEmpty($question->subquestions, 'Moodle must load each embedded answer field.');

            foreach ($question->subquestions as $subquestion) {
                $type = $subquestion->qtype->name();
                $this->assertContains($type, ['numerical', 'shortanswer']);
                $sawnumerical = $sawnumerical || $type === 'numerical';
                $sawshortanswer = $sawshortanswer || $type === 'shortanswer';
            }

            $correct = $question->get_correct_response();
            $this->assertNotEmpty($correct);
            [$fraction] = $question->grade_response($correct);
            $this->assertEqualsWithDelta(1.0, (float) $fraction, 1.0e-9, 'Moodle rejected its stored correct response.');

            $wrong = array_fill_keys(array_keys($correct), 'moodpy definitely incorrect');
            [$wrongfraction] = $question->grade_response($wrong);
            $this->assertLessThan(1.0, (float) $wrongfraction, 'Moodle awarded full credit for an incorrect response.');

            foreach ($question->subquestions as $index => $subquestion) {
                if ($subquestion instanceof \qtype_shortanswer_question) {
                    $shortanswer = $subquestion->get_correct_response()['answer'] ?? '';
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
                    if ($answer->fraction < 1.0 || $answer->tolerance <= 0) {
                        continue;
                    }
                    $within = $correct;
                    $within['sub' . $index . '_answer'] = (string) (
                        (float) $answer->answer + $answer->tolerance / 2
                    );
                    [$withinfraction] = $question->grade_response($within);
                    $this->assertEqualsWithDelta(
                        1.0,
                        (float) $withinfraction,
                        1.0e-9,
                        'Moodle did not apply the exported numerical tolerance.'
                    );
                    $sawtolerance = true;
                    break 2;
                }
            }
        }

        ksort($actualcategorycounts);
        $this->assertSame($expectedcategorycounts, $actualcategorycounts, 'Moodle imported questions into the wrong topic categories.');
        foreach (array_unique($expectedtags) as $tag) {
            $this->assertContains($tag, $actualtags, 'Moodle did not import the MoodPy question tag.');
        }
        $this->assertTrue($sawnumerical, 'The fixture must exercise Moodle numerical Cloze fields.');
        $this->assertTrue($sawshortanswer, 'The fixture must exercise Moodle short-answer Cloze fields.');
        $this->assertTrue($sawtolerance, 'The fixture must exercise Moodle numerical tolerance grading.');
        $this->assertTrue($sawcaseinsensitive, 'The fixture must exercise Moodle short-answer casing.');
    }
}

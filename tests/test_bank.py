"""Behavior regressions runnable by pytest or Python's unittest runner."""

import contextlib
import io
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from dataclasses import replace
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np

import moodpy
from moodpy import BankValidationError, Cloze, Generator, QuestionFamily, build_bank
from moodpy.bank import parse_answers
from moodpy.generator import GenerationError
from moodpy.recipes import (
    arithmetic_family,
    compound_interest_family,
    linear_equations_family,
    short_answer_family,
)
from moodpy.tools import NM, STxt

ROOT = Path(__file__).resolve().parents[1]


def family(count=3, identity="numbers", values=None, requirements=None, renderer=None):
    def factory(rng):
        gen = Generator()
        if values is None:
            gen.lambdas = {"x": lambda _: int(rng.integers(1, 1000000))}
        else:
            sequence = iter(values)
            gen.lambdas = {"x": lambda _: next(sequence)}
        gen.requirements = (
            [lambda: requirements(gen.parameters["x"])] if requirements else [True]
        )
        return gen

    def render(gen):
        x = gen.parameters["x"]
        gen.set_exercise("<p>x = {}</p>".format(NM(x, entero=True)), template=False)
        gen.set_feedback("<p>Answer: {}</p>".format(x), template=False)

    return QuestionFamily(
        identity,
        "Numbers & symbols",
        "Course/Numbers & symbols",
        count,
        factory,
        renderer or render,
        ("test & verify",),
    )


class TestBank(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.recipe = self.root / "recipe.py"
        self.recipe.write_text("# recipe source\n", encoding="utf-8")
        self.brief = self.root / "brief.md"
        self.brief.write_text("# Educator decisions\n", encoding="utf-8")

    def build(self, families=None, **kwargs):
        return build_bank(
            families or [family()], title="Bank & Unicode ñ", seed=42, **kwargs
        )

    def export(self, bank=None, **kwargs):
        return (bank or self.build()).export_bundle(
            self.root / "bank", source_files=[self.recipe, self.brief], **kwargs
        )

    def test_multiple_categories_counts_names_tags(self):
        bank = self.build(
            [family(2), replace(family(3, "other"), category="Another/Topic")]
        )
        root = ET.fromstring(bank.to_xml())
        self.assertEqual(len(root.findall("question[@type='cloze']")), 5)
        self.assertEqual(
            [
                q.findtext("category/text")
                for q in root.findall("question[@type='category']")
            ],
            ["$course$/Course/Numbers & symbols", "$course$/Another/Topic"],
        )
        self.assertEqual(
            root.findtext("question[@type='cloze']/name/text"),
            "Numbers & symbols [001]",
        )
        self.assertEqual(
            root.findtext("question[@type='cloze']/tags/tag/text"), "test & verify"
        )
        self.assertTrue(bank.validate().valid)

    def test_seed_reproducibility_and_difference(self):
        one, two = self.build(), self.build()
        self.assertEqual(one.questions, two.questions)
        self.assertEqual(one.to_xml(), two.to_xml())
        self.assertEqual(one.to_preview(), two.to_preview())
        changed = build_bank([family()], title=one.title, seed=43)
        self.assertNotEqual(one.questions, changed.questions)

    def test_family_independence_and_sample_prefix(self):
        sample = self.build([family(2), family(2, "other")])
        full = self.build([family(7, "other"), family(5)])
        for identity in ["numbers", "other"]:
            original = [q for q in sample.questions if q.family_id == identity]
            expanded = [q for q in full.questions if q.family_id == identity]
            self.assertEqual(original, expanded[:2])

    def test_shared_budget_for_constraints_and_duplicates(self):
        bank = self.build(
            [family(2, values=[0, 1, 1, 2], requirements=lambda x: x > 0)],
            max_attempts=2,
        )
        self.assertEqual([q.parameters["x"] for q in bank.questions], [1, 2])
        with self.assertRaisesRegex(
            BankValidationError, "family numbers variant 1.*2 attempts"
        ):
            self.build(
                [family(1, values=[0, 0], requirements=lambda x: x > 0)], max_attempts=2
            )
        with self.assertRaisesRegex(
            BankValidationError, "family numbers variant 2.*2 attempts"
        ):
            self.build([family(2, values=[1, 1, 1])], max_attempts=2)

    def test_invalid_metadata(self):
        for change in [
            dict(id="bad id"),
            dict(count=0),
            dict(count=True),
            dict(category="../outside"),
            dict(category="$course$/Topic"),
            dict(category="/Topic"),
            dict(tags="one tag"),
            dict(title=""),
            dict(generator_factory=None),
            dict(exercise_fn=None),
        ]:
            with self.subTest(change=change), self.assertRaises(BankValidationError):
                self.build([replace(family(), **change)])
        for kwargs in [
            dict(seed=-1),
            dict(seed=True),
            dict(max_attempts=0),
            dict(max_attempts=True),
        ]:
            with self.subTest(kwargs=kwargs), self.assertRaises(BankValidationError):
                build_bank([family()], title="Bank", **dict({"seed": 42}, **kwargs))
        with self.assertRaisesRegex(BankValidationError, "unique"):
            self.build([family(), family()])
        with self.assertRaises(BankValidationError):
            build_bank([], title="Bank", seed=42)

    def test_snapshots_and_defensive_parameters(self):
        calls = []

        def render(gen):
            calls.append(1)
            gen.set_exercise(NM(gen.parameters["x"]), template=False)

        bank = self.build([family(renderer=render)])
        saved = bank.questions[0].parameters["x"]
        bank.questions[0].parameters["x"] = -999
        self.assertEqual(bank.questions[0].parameters["x"], saved)
        bank.validate()
        bank.to_xml()
        bank.to_preview()
        self.export(bank)
        self.assertEqual(len(calls), 3)

    def test_numpy_snapshot_normalization(self):
        def factory(rng):
            gen = Generator()
            gen.lambdas = {"x": lambda _: rng.integers(1, 100, size=2)}
            return gen

        def render(gen):
            gen.set_exercise(NM(gen.parameters["x"].sum()), template=False)

        bank = self.build(
            [QuestionFamily("array", "Array", "Array", 1, factory, render)]
        )
        self.assertIsInstance(bank.questions[0].parameters["x"], list)
        self.assertTrue(
            all(isinstance(x, int) for x in bank.questions[0].parameters["x"])
        )

    def test_contextual_rendering_errors(self):
        def broken(gen):
            gen.set_exercise("Missing {d[typo]}")

        with self.assertRaisesRegex(
            BankValidationError, "family numbers variant 1.*typo"
        ):
            self.build([family(renderer=broken)])

        def unresolved(gen):
            gen.set_exercise("Unresolved {d[x]} " + NM(1), template=False)

        with self.assertRaisesRegex(BankValidationError, "unresolved"):
            self.build([family(renderer=unresolved)])

    def test_missing_or_unsupported_answers(self):
        for text in [
            "No answer field",
            "{1:MULTICHOICE:=a~b}",
            "{1:NM:=nan:0}",
            "{1:NM:=2:-1}",
            "{1:NM:=inf:0}",
            "{1:NM:=2:inf}",
            "{1:NM:=+1:0}",
            "{1:NM:=1_000:0}",
            "{1:NM:=1e309:0}",
            "{1:NM:=2",
            "{0:NM:=1}",
            "{1:SHORTANSWER:=a~b}",
        ]:

            def render(gen, text=text):
                gen.set_exercise(text, template=False)

            with self.subTest(text=text), self.assertRaises(BankValidationError):
                self.build([family(1, renderer=render)])

    def test_cdata_and_xml_characters(self):
        def render(gen):
            gen.set_exercise("<p>ñ &amp; the literal ]]></p>" + NM(1), template=False)
            gen.set_feedback("Feedback ]]>", template=False)

        bank = self.build([family(1, renderer=render)])
        root = ET.fromstring(bank.to_xml())
        question = root.find("question[@type='cloze']")
        self.assertIn("]]>", question.findtext("questiontext/text"))
        self.assertEqual(
            question.findtext("generalfeedback/text").strip(), "Feedback ]]>"
        )
        with self.assertRaises(BankValidationError):
            self.build([replace(family(), title="invalid\x00")])

    def test_preview_blanks_and_solutions_match_xml(self):
        bank = self.build()
        preview = bank.to_preview()
        root = ET.fromstring(bank.to_xml())
        self.assertEqual(preview.count('class="blank"'), 3)
        for question, node in zip(
            bank.questions, root.findall("question[@type='cloze']")
        ):
            self.assertEqual(
                node.findtext("questiontext/text").strip(), question.text.strip()
            )
            self.assertIn('data-question-id="{}"'.format(question.id), preview)
            self.assertIn(
                "<li>{}".format(parse_answers(question.text)[0].answer), preview
            )
            self.assertNotIn("{1:NM:", preview)
        self.assertIn("Teacher solution", preview)

    def test_feedback_callback_does_not_leak(self):
        def render(gen):
            gen.set_exercise(NM(gen.parameters["x"]), template=False)
            if gen.counter == 1:
                gen.set_feedback("first solution", template=False)

        bank = self.build([family(2, renderer=render)])
        self.assertEqual(bank.questions[0].feedback, "first solution")
        self.assertEqual(bank.questions[1].feedback, "")

    def test_bundle_sources_manifest_and_zip(self):
        bank = self.build()
        paths = self.export(bank)
        self.assertEqual(
            (paths.directory / "sources/recipe.py").read_bytes(),
            self.recipe.read_bytes(),
        )
        manifest = json.loads(paths.manifest.read_text())
        self.assertEqual(manifest["seed"], 42)
        self.assertEqual(manifest["families"][0]["count"], 3)
        self.assertEqual(
            manifest["questions"][0]["parameters"], bank.questions[0].parameters
        )
        self.assertEqual(manifest["versions"]["moodpy"], "3.0.1")
        self.assertEqual(manifest["validation"]["live_moodle_import"], "not tested")
        with zipfile.ZipFile(paths.archive) as archive:
            self.assertEqual(
                set(archive.namelist()),
                {
                    "bank.xml",
                    "preview.html",
                    "manifest.json",
                    "README.md",
                    "sources/recipe.py",
                    "sources/brief.md",
                },
            )
            for name in archive.namelist():
                self.assertEqual(
                    archive.read(name), (paths.directory / name).read_bytes()
                )

    def test_reproducible_archive(self):
        first = self.export()
        second = self.build().export_bundle(
            self.root / "second", source_files=[self.recipe, self.brief]
        )
        self.assertEqual(first.archive.read_bytes(), second.archive.read_bytes())

    def test_export_preflight_and_overwrite(self):
        first = self.export()
        original = first.xml.read_bytes()
        with self.assertRaises(FileExistsError):
            self.export()
        (first.directory / "keep.txt").write_text("keep me")
        replacement = self.build([family(1)])
        self.export(replacement, overwrite=True)
        self.assertEqual((first.directory / "keep.txt").read_text(), "keep me")
        self.assertNotEqual(first.xml.read_bytes(), original)
        new_recipe = self.root / "unrelated.py"
        new_recipe.write_text("new source")
        (first.directory / "sources/unrelated.py").write_text("existing unrelated file")
        with self.assertRaises(FileExistsError):
            replacement.export_bundle(
                first.directory, source_files=[new_recipe, self.brief], overwrite=True
            )
        self.assertEqual(
            (first.directory / "sources/unrelated.py").read_text(),
            "existing unrelated file",
        )

    def test_reject_symlink_destinations(self):
        paths = self.export()
        outside = self.root / "outside"
        outside.write_text("preserve")
        paths.xml.unlink()
        try:
            paths.xml.symlink_to(outside)
        except OSError:
            self.skipTest("symlinks unavailable")
        with self.assertRaises(FileExistsError):
            self.export(overwrite=True)
        self.assertEqual(outside.read_text(), "preserve")

    def test_no_output_on_invalid_bank_or_sources(self):
        bank = self.build()
        broken = replace(bank, questions=bank.questions[:-1])
        with self.assertRaisesRegex(BankValidationError, "incomplete"):
            self.export(broken)
        self.assertFalse((self.root / "bank").exists())

        with self.assertRaises(BankValidationError):
            bank.export_bundle(self.root / "bank", source_files=[self.recipe])
        self.assertFalse((self.root / "bank").exists())
        duplicate = self.root / "other/recipe.py"
        duplicate.parent.mkdir()
        duplicate.write_text("duplicate")
        with self.assertRaises(BankValidationError):
            bank.export_bundle(
                self.root / "bank", source_files=[self.recipe, duplicate, self.brief]
            )
        self.assertFalse((self.root / "bank").exists())

    def test_validation_reports_damaged_metadata_and_snapshots(self):
        bank = self.build()
        for damaged in [
            replace(bank, max_attempts=0),
            replace(bank, families=(replace(bank.families[0], count="bad"),)),
            replace(bank, questions=(replace(bank.questions[0], feedback=None),)),
            replace(
                bank, questions=(replace(bank.questions[0], parameters_json="[]"),)
            ),
            replace(
                bank, questions=(replace(bank.questions[0], parameters_json="bad"),)
            ),
        ]:
            with self.subTest(damaged=damaged):
                self.assertFalse(damaged.validate().valid)
                with self.assertRaises(BankValidationError):
                    self.export(damaged)
                self.assertFalse((self.root / "bank").exists())

    def test_verified_recipes_answers(self):
        bank = self.build(
            [
                arithmetic_family(5),
                linear_equations_family(5),
                compound_interest_family(5),
                short_answer_family(5),
            ]
        )
        self.assertEqual(
            len(ET.fromstring(bank.to_xml()).findall("question[@type='cloze']")), 20
        )
        for question in bank.questions:
            d = question.parameters
            answer = parse_answers(question.text)[0].answer
            if question.family_id == "addition":
                self.assertEqual(int(answer), d["a"] + d["b"])
                self.assertNotEqual(d["a"], d["b"])
            elif question.family_id == "linear":
                self.assertEqual(d["a"] * int(answer) + d["b"], d["c"])
                self.assertNotEqual(d["x"], 0)
            elif question.family_id == "compound":
                self.assertEqual(
                    float(answer), round(d["P"] * (1 + d["rate"]) ** d["years"], 2)
                )
                self.assertGreaterEqual(d["years"], 2)
            else:
                expected = (
                    "positive" if d["n"] > 0 else "negative" if d["n"] < 0 else "zero"
                )
                self.assertEqual(answer, expected)

    def test_regenerate_exported_sources_with_manifest(self):
        env = os.environ.copy()
        script = ROOT / "examples/agent_workflow/author_bank.py"
        destination = self.root / "sample"
        run = subprocess.run(
            [
                sys.executable,
                str(script),
                "--seed",
                "17",
                "--samples",
                "2",
                "--output",
                str(destination),
            ],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        regenerated = self.root / "regenerated"
        run = subprocess.run(
            [
                sys.executable,
                str(destination / "sources/author_bank.py"),
                "--manifest",
                str(destination / "manifest.json"),
                "--output",
                str(regenerated),
            ],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        for name in ["bank.xml", "preview.html", "manifest.json", "bundle.zip"]:
            self.assertEqual(
                (destination / name).read_bytes(), (regenerated / name).read_bytes()
            )

    def test_package_version_consistency(self):
        configured = re.search(
            r'^version\s*=\s*"([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.M
        ).group(1)
        self.assertEqual(moodpy.__version__, configured)
        self.assertEqual(
            moodpy.VERSION, tuple(int(part) for part in configured.split("."))
        )
        from importlib import metadata

        try:
            installed = metadata.version("moodpy")
        except metadata.PackageNotFoundError:
            installed = None
        if installed is not None:
            self.assertEqual(installed, configured)


class TestGenerationRegressions(unittest.TestCase):
    def test_failure_recovery_and_string_requirement_rejection(self):
        gen = Generator()
        gen.lambdas = {"x": lambda _: 1}
        gen.requirements = [False]
        with contextlib.redirect_stdout(io.StringIO()):
            gen.test_parameters(max_steps=2)
        self.assertIsNone(gen.parameters)
        gen.requirements = [True]
        gen.test_parameters()
        self.assertEqual(gen.parameters, {"x": 1})
        gen.requirements = ["x > 0"]
        with self.assertRaises(TypeError):
            gen.test_parameters()

    def test_templates_refresh_exercise_and_feedback(self):
        gen = Generator()
        gen.lambdas = {"x": lambda _: next(values)}
        values = iter([1, 2, 3])
        gen.reload_parameters()
        gen.set_exercise("x={d[x]} {1:NM:=1}")
        gen.set_feedback("solution={d[x]}")
        gen.generate()
        self.assertIn("x=2", gen.exercise_text)
        self.assertEqual(gen.feedback_text, "solution=2")
        gen.generate()
        self.assertIn("x=3", gen.exercise_text)
        self.assertEqual(gen.feedback_text, "solution=3")

    def test_literal_math_braces_and_template_errors(self):
        gen = Generator()
        text = r"\(\frac{a}{b}\) " + NM(1)
        gen.set_exercise(text, template=False)
        gen.set_feedback(r"\frac{1}{2}", template=False)
        self.assertIn(text, gen.exercise_text)
        self.assertEqual(gen.feedback_text, r"\frac{1}{2}")
        with self.assertRaises(KeyError):
            gen.set_exercise("{d[missing]}")

    def test_numeric_percent_finite_and_tolerances(self):
        answer = parse_answers(NM(0.85, percent=True))[0]
        self.assertEqual(float(answer.answer), 85.0)
        self.assertAlmostEqual(answer.tolerance, 0.085)
        for value in [float("nan"), float("inf"), -float("inf")]:
            with self.assertRaises(ValueError):
                NM(value)
        for error in [-0.1, float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                NM(1, error=error)
        self.assertEqual(NM(0, round_zero=True), "{1:NM:=0:0.00001}")

    def test_short_answer_reserved_characters_round_trip(self):
        answer = r"a~b=c#d:e{f}\g & ñ * &lt; \# \} \* \\#"
        encoded = STxt(answer)
        self.assertEqual(parse_answers(encoded)[0].answer, answer)
        # Independently check the decode order used by Moodle's Cloze/short-
        # answer code, rather than only testing our encoder against our parser.
        decoded = html.unescape(encoded[len("{1:SHORTANSWER:=") : -1])
        decoded = decoded.replace(r"\}", "}").replace(r"\#", "#")
        self.assertIsNone(re.search(r"(?<!\\)\*", decoded))
        self.assertEqual(decoded.replace(r"\*", "*"), answer)
        gen = Generator()
        gen.parameters = {"x": 7}
        gen.set_exercise("{d[x]} " + encoded)
        self.assertIn(encoded, gen.exercise_text)
        self.assertIn("7 ", gen.exercise_text)
        for invalid in ["", " \t\n"]:
            with self.assertRaises(ValueError):
                STxt(invalid)

    def test_legacy_batch_and_preview_enforce_constraints(self):
        original = Path.cwd()
        with tempfile.TemporaryDirectory() as temp:
            os.chdir(temp)
            try:
                for preview in [False, True]:
                    gen = Generator()
                    sequence = iter([0, 1, 0, 2])
                    gen.lambdas = {"x": lambda _: next(sequence)}
                    gen.requirements = [lambda: gen.parameters["x"] > 0]

                    def render(current):
                        current.set_exercise(
                            NM(current.parameters["x"]), template=False
                        )

                    cloze = Cloze()
                    cloze.set_info("Math & science", "1", "constraints")
                    cloze.set_generator(gen)
                    with contextlib.redirect_stdout(io.StringIO()):
                        if preview:
                            cloze.testing(2, render)
                        else:
                            cloze.get_exercises(2, render)
                    if not preview:
                        root = ET.parse(cloze.path)
                        self.assertEqual(len(root.findall("question")), 2)
                    self.assertEqual(gen.parameters["x"], 2)
            finally:
                os.chdir(original)

    def test_legacy_exhaustion_does_not_write_partial_batch(self):
        cloze = Cloze()
        cloze.generator.lambdas = {"x": lambda _: 1}
        cloze.generator.requirements = [False]
        with self.assertRaises(GenerationError):
            cloze.get_exercises(1)
        self.assertEqual(cloze.xml, [])


if __name__ == "__main__":
    unittest.main()

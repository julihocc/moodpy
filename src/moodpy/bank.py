"""Reproducible, validated Moodle banks authored by educators and agents.

Python recipes are trusted executable code. Validation covers the supported
Cloze subset and XML structure, not mathematical truth or a live Moodle import.
"""

import hashlib
import html
import json
import math
import os
import platform
import re
import shlex
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, Union
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

import numpy as np

from .generator import Generator, cdata, feedback, questiontext

_FORMAT = "moodpy-bank-v1"
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*\Z")
_SLOT = re.compile(r"(?<!\\)\{d\[[^\]]*\]")
_FIELD_START = re.compile(r"\{[0-9]+:")
_NUMBER = re.compile(r"-?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][-+]?[0-9]+)?\Z")
_RESERVED = "\\~=#:{}*"
_ENTITY = re.compile(r"&(?:#[0-9]+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);")


class BankValidationError(ValueError):
    """Invalid metadata, unsupported content, or exhausted generation."""


@dataclass(frozen=True)
class QuestionFamily:
    id: str
    title: str
    category: str
    count: int
    generator_factory: Callable[[np.random.Generator], Generator]
    exercise_fn: Callable[[Generator], None]
    tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class FamilyMetadata:
    id: str
    title: str
    category: str
    count: int
    tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class AnswerField:
    start: int
    end: int
    kind: str
    answer: str
    tolerance: Optional[float] = None


@dataclass(frozen=True)
class GeneratedQuestion:
    id: str
    family_id: str
    variant: int
    title: str
    category: str
    text: str
    feedback: str
    tags: Tuple[str, ...]
    parameters_json: str = field(repr=False)

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return a defensive copy of the JSON-normalized parameter snapshot."""
        return json.loads(self.parameters_json)


@dataclass(frozen=True)
class ValidationReport:
    valid: bool
    question_count: int
    issues: Tuple[str, ...] = ()

    def raise_for_errors(self) -> None:
        if not self.valid:
            raise BankValidationError("; ".join(self.issues))


@dataclass(frozen=True)
class BundlePaths:
    directory: Path
    xml: Path
    preview: Path
    manifest: Path
    archive: Path


def _text(value: str, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise BankValidationError(label + " must be a nonempty string")
    if any(
        not (
            ch in "\t\n\r"
            or 0x20 <= ord(ch) <= 0xD7FF
            or 0xE000 <= ord(ch) <= 0xFFFD
            or 0x10000 <= ord(ch) <= 0x10FFFF
        )
        for ch in value
    ):
        raise BankValidationError(label + " contains an invalid XML character")


def _metadata(family: Union[QuestionFamily, FamilyMetadata]) -> None:
    if not isinstance(family.id, str) or not _ID.fullmatch(family.id):
        raise BankValidationError(
            "family id must contain only letters, numbers, '-' or '_'"
        )
    _text(family.title, "family title")
    _text(family.category, "category")
    if any(
        part in ("", ".", "..") or "$" in part for part in family.category.split("/")
    ):
        raise BankValidationError("category must be a relative course category path")
    if (
        isinstance(family.count, bool)
        or not isinstance(family.count, int)
        or family.count < 1
    ):
        raise BankValidationError("family count must be a positive integer")
    if isinstance(family.tags, str):
        raise BankValidationError("tags must be a sequence of strings")
    for tag in family.tags:
        _text(tag, "tag")


def _unescape_answer(value: str) -> str:
    result = []
    pos = 0
    while pos < len(value):
        ch = value[pos]
        entity = _ENTITY.match(value, pos)
        if entity is not None:
            result.append(entity.group())
            pos = entity.end()
            continue
        if ch == "\\":
            pos += 1
            if pos == len(value) or value[pos] not in "*#}":
                raise BankValidationError("unsupported short-answer escape")
            result.append("\\" + value[pos])
        elif ch in _RESERVED:
            raise BankValidationError(
                "short-answer reserved characters must be escaped with STxt()"
            )
        else:
            result.append(ch)
        pos += 1
    decoded = html.unescape("".join(result)).replace("\\}", "}").replace("\\#", "#")
    if re.search(r"(?<!\\)\*", decoded):
        raise BankValidationError(
            "short-answer wildcards are unsupported; use STxt() for literal asterisks"
        )
    answer = decoded.replace("\\*", "*")
    if not answer.strip():
        raise BankValidationError("short answer must not be empty")
    return answer


def parse_answers(text: str) -> Tuple[AnswerField, ...]:
    """Parse only single-correct-answer NM/NUMERICAL and SHORTANSWER/SA fields.

    The supported subset is exactly the syntax produced by NM() and STxt(),
    with positive integer weights. Alternatives and inline feedback are rejected.
    Mathematical braces outside answer fields are ordinary text.
    """
    fields = []
    pos = 0
    while True:
        match = _FIELD_START.search(text, pos)
        if match is None:
            break
        end = match.end()
        while end < len(text):
            if text[end] == "\\":
                end += 2
            elif text[end] == "}":
                break
            else:
                end += 1
        if end >= len(text):
            raise BankValidationError("unterminated Cloze answer field")
        body = text[match.start() + 1 : end]
        pieces = body.split(":", 2)
        if len(pieces) != 3 or int(pieces[0]) < 1 or not pieces[2].startswith("="):
            raise BankValidationError(
                "expected a positive weight and one '=answer' Cloze field"
            )
        kind, value = pieces[1], pieces[2][1:]
        if kind in ("NM", "NUMERICAL"):
            numbers = value.split(":")
            if len(numbers) not in (1, 2):
                raise BankValidationError("unsupported numerical answer syntax")
            if any(not _NUMBER.fullmatch(number) for number in numbers):
                raise BankValidationError("unsupported numerical literal; use NM()")
            try:
                answer = float(numbers[0])
                tolerance = float(numbers[1]) if len(numbers) == 2 else 0.0
            except ValueError as error:
                raise BankValidationError(
                    "numerical answer and tolerance must be numbers"
                ) from error
            if (
                not math.isfinite(answer)
                or not math.isfinite(tolerance)
                or tolerance < 0
            ):
                raise BankValidationError(
                    "numerical answer and tolerance must be finite; tolerance >= 0"
                )
            field_value = AnswerField(
                match.start(), end + 1, "numerical", numbers[0], tolerance
            )
        elif kind in ("SHORTANSWER", "SA"):
            field_value = AnswerField(
                match.start(), end + 1, "shortanswer", _unescape_answer(value)
            )
        else:
            raise BankValidationError(
                "unsupported Cloze type {!r}; use NM() or STxt()".format(kind)
            )
        fields.append(field_value)
        pos = end + 1
    if not fields:
        raise BankValidationError(
            "question must contain at least one NM() or STxt() answer field"
        )
    return tuple(fields)


def _normalize(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return _normalize(value.tolist())
    if isinstance(value, np.generic):
        return _normalize(value.item())
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise BankValidationError("parameter snapshot keys must be strings")
        return {key: _normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return value
    raise BankValidationError(
        "parameters must be finite JSON values; convert symbolic objects explicitly"
    )


def _json(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    )


def _question_check(question: GeneratedQuestion) -> None:
    _text(question.text, "question text")
    if question.feedback:
        _text(question.feedback, "feedback")
    if _SLOT.search(question.text) or _SLOT.search(question.feedback):
        raise BankValidationError("unresolved {d[key]} placeholder")
    parse_answers(question.text)
    parameters = question.parameters
    if not isinstance(parameters, dict):
        raise BankValidationError("parameter snapshot must be an object")
    _normalize(parameters)


@dataclass(frozen=True)
class QuestionBank:
    title: str
    seed: int
    families: Tuple[FamilyMetadata, ...]
    questions: Tuple[GeneratedQuestion, ...]
    max_attempts: int = 10000

    def validate(self) -> ValidationReport:
        """Validate snapshots without invoking recipe code or sampling."""
        issues = []
        try:
            _text(self.title, "bank title")
            if (
                isinstance(self.seed, bool)
                or not isinstance(self.seed, int)
                or self.seed < 0
            ):
                raise BankValidationError("seed must be a nonnegative integer")
            if (
                isinstance(self.max_attempts, bool)
                or not isinstance(self.max_attempts, int)
                or self.max_attempts < 1
            ):
                raise BankValidationError("max_attempts must be a positive integer")
            if not self.families:
                raise BankValidationError("bank must contain at least one family")
            for family in self.families:
                _metadata(family)
            if len({f.id for f in self.families}) != len(self.families):
                raise BankValidationError("family IDs must be unique")
        except (ValueError, TypeError) as error:
            issues.append(str(error))
        if issues:
            return ValidationReport(False, len(self.questions), tuple(issues))
        families = {f.id: f for f in self.families}
        seen_ids = set()
        seen_text = set()
        variants = {f.id: set() for f in self.families}
        for question in self.questions:
            context = "family {} variant {}: ".format(
                question.family_id, question.variant
            )
            try:
                _question_check(question)
                family = families.get(question.family_id)
                if family is None:
                    raise BankValidationError("unknown family")
                if (
                    isinstance(question.variant, bool)
                    or not isinstance(question.variant, int)
                    or not 1 <= question.variant <= family.count
                ):
                    raise BankValidationError("variant index outside requested count")
                expected_id = "{}-{:03d}".format(family.id, question.variant)
                if (
                    question.id != expected_id
                    or question.title
                    != "{} [{:03d}]".format(family.title, question.variant)
                ):
                    raise BankValidationError(
                        "question ID/title does not match its family and variant"
                    )
                if question.category != family.category or question.tags != family.tags:
                    raise BankValidationError(
                        "question category/tags do not match its family"
                    )
                if (
                    question.id in seen_ids
                    or (question.family_id, question.text) in seen_text
                ):
                    raise BankValidationError("duplicate question ID or rendered text")
                seen_ids.add(question.id)
                seen_text.add((question.family_id, question.text))
                variants[family.id].add(question.variant)
            except (ValueError, TypeError) as error:
                issues.append(context + str(error))
        for family in self.families:
            if variants[family.id] != set(range(1, family.count + 1)):
                issues.append(
                    "family {}: incomplete bank (expected {} variants)".format(
                        family.id, family.count
                    )
                )
        if not issues:
            try:
                ET.fromstring(self._xml())
            except (ET.ParseError, ValueError, TypeError) as error:
                issues.append("XML: " + str(error))
        return ValidationReport(not issues, len(self.questions), tuple(issues))

    def _xml(self) -> str:
        parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
        category = None
        for question in self.questions:
            if category != question.category:
                category = question.category
                parts.append(
                    '<question type="category"><category><text>{}</text></category></question>'.format(
                        escape("$course$/" + category)
                    )
                )
            parts.extend(
                [
                    '<question type="cloze">',
                    "<name><text>{}</text></name>".format(escape(question.title)),
                    questiontext(cdata(question.text)),
                    feedback(cdata(question.feedback)),
                    "<penalty>0.5</penalty><hidden>0</hidden>",
                    "<tags>",
                ]
            )
            parts.extend(
                "<tag><text>{}</text></tag>".format(escape(tag))
                for tag in question.tags
            )
            parts.extend(["</tags>", "</question>"])
        parts.append("</quiz>\n")
        return "\n".join(parts)

    def to_xml(self) -> str:
        self.validate().raise_for_errors()
        return self._xml()

    def to_preview(self) -> str:
        """Offline teacher preview; LaTeX remains readable source notation."""
        self.validate().raise_for_errors()
        parts = [
            '<!doctype html><html><head><meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "<title>{}</title>".format(html.escape(self.title)),
            "<style>body{font:18px system-ui;max-width:900px;margin:2rem auto;padding:0 1rem}"
            "article{border-top:1px solid #aaa;padding:1rem 0}.blank{display:inline-block;"
            "min-width:6em;border-bottom:2px solid #555}details{margin-top:1em}</style></head><body>",
            "<h1>{}</h1>".format(html.escape(self.title)),
            "<p>Teacher preview: contains solutions. Seed {}. LaTeX is shown as source notation.</p>".format(
                self.seed
            ),
        ]
        for question in self.questions:
            fields = parse_answers(question.text)
            chunks, start = [], 0
            for answer in fields:
                chunks.append(question.text[start : answer.start])
                chunks.append('<span class="blank" aria-label="answer">&nbsp;</span>')
                start = answer.end
            chunks.append(question.text[start:])
            parts.extend(
                [
                    '<article id="{}" data-question-id="{}">'.format(
                        question.id, question.id
                    ),
                    "<h2>{}</h2><p>{}</p>".format(
                        html.escape(question.title), html.escape(question.category)
                    ),
                    "".join(chunks),
                    "<details><summary>Teacher solution</summary><ol>",
                ]
            )
            for answer in fields:
                suffix = (
                    " (tolerance: {})".format(answer.tolerance)
                    if answer.tolerance is not None
                    else ""
                )
                parts.append("<li>{}{}</li>".format(html.escape(answer.answer), suffix))
            parts.extend(["</ol>", question.feedback, "</details></article>"])
        parts.append("</body></html>\n")
        return "\n".join(parts)

    def export_bundle(
        self,
        output_dir: Union[str, Path],
        *,
        source_files: Iterable[Union[str, Path]],
        overwrite: bool = False,
    ) -> BundlePaths:
        """Validate, stage, then write only managed bundle files and a ZIP.

        Existing bundles require overwrite=True. Unrelated files are preserved;
        source-name collisions and symlink destinations are rejected.
        """
        self.validate().raise_for_errors()
        payload = {
            "bank.xml": self._xml().encode("utf-8"),
            "preview.html": self.to_preview().encode("utf-8"),
        }
        hashes = {}
        recipes = []
        for source in source_files:
            path = Path(source)
            name = "sources/" + path.name
            if name in hashes:
                raise BankValidationError(
                    "source filenames must be unique: " + path.name
                )
            payload[name] = path.read_bytes()
            hashes[name] = hashlib.sha256(payload[name]).hexdigest()
            if path.suffix == ".py":
                recipes.append(path.name)
        if not recipes or "sources/brief.md" not in hashes:
            raise BankValidationError(
                "source_files must include a Python recipe and brief.md"
            )
        from . import __version__
        from importlib import metadata

        try:
            installed_version = metadata.version("moodpy")
        except metadata.PackageNotFoundError:
            installed_version = None
        report = self.validate()
        manifest = {
            "format": _FORMAT,
            "title": self.title,
            "seed": self.seed,
            "max_attempts": self.max_attempts,
            "versions": {
                "moodpy": __version__,
                "installed_moodpy": installed_version,
                "python": platform.python_version(),
                "numpy": np.__version__,
            },
            "families": [
                dict(
                    id=f.id,
                    title=f.title,
                    category=f.category,
                    count=f.count,
                    tags=f.tags,
                )
                for f in self.families
            ],
            "questions": [
                dict(
                    id=q.id,
                    family_id=q.family_id,
                    variant=q.variant,
                    parameters=q.parameters,
                )
                for q in self.questions
            ],
            "validation": {
                "valid": report.valid,
                "question_count": report.question_count,
                "issues": report.issues,
                "live_moodle_import": "not tested",
            },
            "sources": hashes,
        }
        payload["manifest.json"] = _json(manifest).encode("utf-8")
        recipe = recipes[0]
        instructions = """# {title}

This bundle contains {count} Cloze questions. The teacher preview includes answers.
Local XML and supported Cloze syntax were checked; a live Moodle import was not tested.

## Regenerate

Use the recorded Python, NumPy, and MoodPy versions from manifest.json. If this
MoodPy version is not published, install the matching repository checkout with
`python -m pip install -e /path/to/moodpy`. From this bundle directory, the supplied
CLI authoring template can be rerun with:

```bash
python {recipe} --manifest manifest.json --seed {seed} --output regenerated-bank
```

Custom recipes must preserve this CLI contract and use the injected RNG.
Read sources/brief.md for objectives, family counts, bounds, and review decisions.

## Import and verify in Moodle

1. Open the course question bank and its Import screen; choose Moodle XML.
2. Import bank.xml with **Get category from file** enabled.
3. Check question counts and topic categories.
4. Preview numerical fields: test the correct answer and values inside/outside tolerance.
5. Preview short-answer fields: test accepted text and an incorrect response.
6. Check Unicode, mathematical notation, and feedback. Record the Moodle version and outcome.
7. Create/configure the quiz activity separately and select questions from the bank.

Bundle overwrite replaces only managed files and preserves unrelated files.
""".format(
            title=self.title,
            count=len(self.questions),
            recipe=shlex.quote("sources/" + recipe),
            seed=self.seed,
        )
        payload["README.md"] = instructions.encode("utf-8")
        output = Path(output_dir).absolute()
        if output.is_symlink() or (output.exists() and not output.is_dir()):
            raise FileExistsError("output must be a directory, not a file or symlink")
        old_managed = set()
        if output.exists() and any(output.iterdir()):
            if not overwrite:
                raise FileExistsError(
                    "bundle already exists; choose a new output or overwrite=True"
                )
            old_manifest = output / "manifest.json"
            if old_manifest.is_symlink():
                raise FileExistsError("cannot overwrite a symlink manifest")
            try:
                previous = json.loads(old_manifest.read_text(encoding="utf-8"))
                if previous["format"] != _FORMAT:
                    raise ValueError("unknown format")
                old_managed = {
                    "bank.xml",
                    "preview.html",
                    "manifest.json",
                    "README.md",
                    "bundle.zip",
                }
                old_managed.update(previous["sources"])
            except (OSError, ValueError, KeyError, TypeError) as error:
                raise FileExistsError(
                    "overwrite requires an existing MoodPy bundle"
                ) from error
        names = set(payload) | {"bundle.zip"}
        if (output / "sources").is_symlink():
            raise FileExistsError("cannot overwrite a symlink source directory")
        for name in names:
            target = output / name
            if target.is_symlink() or (
                target.exists() and (target.is_dir() or name not in old_managed)
            ):
                raise FileExistsError("unmanaged or symlink destination: " + name)
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix=".moodpy-", dir=str(output.parent)
        ) as staging:
            stage = Path(staging) / "bundle"
            stage.mkdir()
            for name, content in payload.items():
                target = stage / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            with zipfile.ZipFile(
                stage / "bundle.zip", "w", zipfile.ZIP_DEFLATED
            ) as archive:
                for name in sorted(payload):
                    # Fixed timestamps make identical payloads reproducible archives.
                    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info, payload[name])
            if not output.exists():
                os.replace(stage, output)
            else:
                (output / "sources").mkdir(exist_ok=True)
                for name in sorted(names):
                    os.replace(stage / name, output / name)
        return BundlePaths(
            output,
            output / "bank.xml",
            output / "preview.html",
            output / "manifest.json",
            output / "bundle.zip",
        )


def build_bank(
    families: Iterable[QuestionFamily],
    *,
    title: str,
    seed: int,
    max_attempts: int = 10000,
) -> QuestionBank:
    """Build complete snapshots with independent seeded streams for each family."""
    _text(title, "bank title")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise BankValidationError("seed must be a nonnegative integer")
    if (
        isinstance(max_attempts, bool)
        or not isinstance(max_attempts, int)
        or max_attempts < 1
    ):
        raise BankValidationError("max_attempts must be a positive integer")
    families = tuple(families)
    if not families:
        raise BankValidationError("bank must contain at least one family")
    ids, metadata, questions = set(), [], []
    for family in families:
        if not isinstance(family, QuestionFamily):
            raise BankValidationError("families must contain QuestionFamily instances")
        try:
            _metadata(family)
            if family.id in ids:
                raise BankValidationError("family IDs must be unique")
            if not callable(family.generator_factory) or not callable(
                family.exercise_fn
            ):
                raise BankValidationError("factory and exercise_fn must be callable")
            ids.add(family.id)
            metadata.append(
                FamilyMetadata(
                    family.id,
                    family.title,
                    family.category,
                    family.count,
                    tuple(family.tags),
                )
            )
            digest = hashlib.sha256(
                json.dumps([seed, family.id]).encode("utf-8")
            ).digest()
            rng = np.random.Generator(np.random.PCG64(int.from_bytes(digest, "big")))
            gen = family.generator_factory(rng)
            if not isinstance(gen, Generator):
                raise BankValidationError("generator_factory must return a Generator")
        except Exception as error:
            raise BankValidationError(
                "family {!r}: {}".format(family.id, error)
            ) from error
        seen = set()
        for variant in range(1, family.count + 1):
            try:
                gen.set_counter(variant)
                gen.generate(
                    family.exercise_fn,
                    max_steps=max_attempts,
                    accept=lambda current: current.exercise_text not in seen,
                )
                question = GeneratedQuestion(
                    "{}-{:03d}".format(family.id, variant),
                    family.id,
                    variant,
                    "{} [{:03d}]".format(family.title, variant),
                    family.category,
                    gen.exercise_text,
                    gen.feedback_text or "",
                    tuple(family.tags),
                    _json(_normalize(gen.parameters)),
                )
                _question_check(question)
                seen.add(question.text)
                questions.append(question)
            except Exception as error:
                raise BankValidationError(
                    "family {} variant {}: {}".format(family.id, variant, error)
                ) from error
    bank = QuestionBank(title, seed, tuple(metadata), tuple(questions), max_attempts)
    bank.validate().raise_for_errors()
    return bank

"""Shared bounded sampling and rendering for legacy exports and question banks."""

import re


class GenerationError(ValueError):
    """No acceptable question could be generated within the attempt budget."""


def feedback(cdata_text):
    return '<generalfeedback format="html">\n' + cdata_text + "</generalfeedback>\n"


def questiontext(cdata_text):
    return '<questiontext format="html">\n' + cdata_text + "</questiontext>\n"


def cdata(exercise_text):
    safe = exercise_text.replace("]]>", "]]]]><![CDATA[>")
    return "<text>\n<![CDATA[\n" + safe + "\n]]>\n</text>"


def _format_template(text, data):
    # Protect complete Moodle fields, including escaped closing braces.
    protected = re.sub(
        r"\{\d+:(?:\\.|[^\\}])*\}",
        lambda match: match.group().replace("{", "{{").replace("}", "}}"),
        text,
    )
    return protected.format(d=data)


class Generator:
    def __init__(self, counter=0):
        self.counter = counter
        self.header = ""
        self.lambdas = {}
        self.derived = {}
        self.parameters = {}
        self.data = {}
        self.exercise_text = ""
        self.exercise_template = None
        self.feedback_text = None
        self.feedback_template = None
        self.print = False
        self.requirements = [True]

    def reload_parameters(self):
        self.parameters = {}
        for key, fn in self.lambdas.items():
            self.parameters[key] = fn(key)

    def calculate_derived(self):
        """Compute derived values in dictionary insertion order."""
        for key, fn in self.derived.items():
            self.parameters[key] = fn(self.parameters)

    def _check_requirements(self):
        results = []
        for requirement in self.requirements:
            if callable(requirement):
                results.append(bool(requirement()))
            elif isinstance(requirement, bool):
                results.append(requirement)
            else:
                raise TypeError(
                    "requirements must be callables or booleans, not strings"
                )
        return all(results)

    def generate(
        self,
        exercise_fn=None,
        *,
        max_steps=10000,
        accept=None,
        render=True,
        debug=False,
    ):
        """Sample and render one question with a shared, finite attempt budget.

        ``accept(gen)`` can reject rendered duplicates. Callback and requirement
        errors propagate immediately; rejected candidates consume retries.
        User callbacks themselves must terminate.
        """
        if (
            isinstance(max_steps, bool)
            or not isinstance(max_steps, int)
            or max_steps < 1
        ):
            raise ValueError("max_steps must be a positive integer")
        for step in range(max_steps):
            self.reload_parameters()
            self.calculate_derived()
            if debug:
                print(step, self.parameters)
            if not self._check_requirements():
                continue
            if render:
                if exercise_fn is not None:
                    self.exercise_text = ""
                    self.feedback_text = None
                    self.exercise_template = None
                    self.feedback_template = None
                    exercise_fn(self)
                else:
                    if self.exercise_template is not None:
                        self.set_exercise(self.exercise_template)
                    if self.feedback_template is not None:
                        self.set_feedback(self.feedback_template)
            if accept is None or accept(self):
                return self.parameters
        raise GenerationError(
            "no acceptable candidate after {} attempts".format(max_steps)
        )

    def test_parameters(self, max_steps=10000, debug=False):
        """Retain the legacy ``parameters=None`` signal on exhaustion."""
        try:
            self.generate(max_steps=max_steps, render=False, debug=debug)
        except GenerationError:
            self.parameters = None
            print("requirements not satisfied")

    def set_exercise(self, text, *, template=True):
        """Render ``{d[key]}`` slots, or store literal text with template=False."""
        self.data = self.parameters.copy()
        formatted = _format_template(text, self.data) if template else text
        self.exercise_template = text if template else None
        self.exercise_text = "\n        {}\n        {}\n        ".format(
            self.header, formatted
        )

    def set_feedback(self, text, *, template=True):
        """Set parameterized feedback or already-rendered literal feedback."""
        self.data = self.parameters.copy()
        self.feedback_text = _format_template(text, self.data) if template else text
        self.feedback_template = text if template else None

    def set_counter(self, counter):
        self.counter = counter

    def get_exercise(self):
        text = "\n{}\n        \n        ".format(self.exercise_text)
        if self.feedback_text:
            text += self.feedback_text
        return text

    def statement(self):
        result = questiontext(cdata(self.exercise_text))
        if self.feedback_text is not None:
            result += feedback(cdata(self.feedback_text))
        return result

    def print_args(self):
        text = "\n        {}\n{}\n Exercise {}\n        ".format(
            64 * "-", 64 * "-", self.counter
        )
        for key, value in self.parameters.items():
            text += "{}\n \t key:\t {} \n \t value: \t {}".format(4 * "-", key, value)
        return text

import re


def feedback(cdata_text):
    return "<generalfeedback format=\"html\">\n" + cdata_text + "</generalfeedback>\n"


def questiontext(cdata_text):
    return "<questiontext format=\"html\">\n" + cdata_text + "</questiontext>\n"


def cdata(exercise_text):
    return "<text>\n<![CDATA[\n" + exercise_text + "\n]]>\n</text>"


def _escape_moodle_braces(text):
    """Temporarily replace {N:TYPE:...} Moodle answer blocks so .format() ignores them."""
    return re.sub(r'\{(\d+:[^}]+)\}', r'<<MOODLE:\1>>', text)


def _restore_moodle_braces(text):
    """Restore Moodle answer blocks after .format() substitution."""
    return re.sub(r'<<MOODLE:(\d+:[^>]+)>>', r'{\1}', text)


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
        for k, f in self.lambdas.items():
            self.parameters[k] = f(k)

    def calculate_derived(self):
        """Calculate derived parameters based on current parameters."""
        for k, f in self.derived.items():
            self.parameters[k] = f(self.parameters)

    def test_parameters(self, max_steps=10000, debug=False):
        """Find valid parameters satisfying all requirements, re-sampling each attempt.

        Requirements must be callable (lambda functions returning bool).
        """
        step = 0
        while step < max_steps:
            self.reload_parameters()
            if self.derived:
                self.calculate_derived()
            if debug:
                print(step, self.parameters)
            reqs = [r() if callable(r) else bool(r) for r in self.requirements]
            if all(reqs):
                if debug:
                    print("Valid parameters found:", self.parameters)
                break
            step += 1
        if step == max_steps:
            self.parameters = None
            print("requirements not satisfied")

    def set_exercise(self, text):
        """Set exercise text, storing the raw template for re-use in batch generation.

        Use {d[key]} placeholders for parameter substitution.
        Moodle answer syntax like {1:NM:=42:0.1} is preserved correctly.
        """
        self.exercise_template = text
        self.data = self.parameters.copy()
        escaped = _escape_moodle_braces(text)
        try:
            formatted = escaped.format(d=self.data)
            formatted = _restore_moodle_braces(formatted)
        except (KeyError, IndexError):
            formatted = text
        self.exercise_text = "\n        {0}\n        {1}\n        ".format(self.header, formatted)

    def set_feedback(self, text):
        """Set feedback text, storing the raw template for re-use in batch generation."""
        self.feedback_template = text
        self.data = self.parameters.copy()
        escaped = _escape_moodle_braces(text)
        try:
            formatted = escaped.format(d=self.data)
            self.feedback_text = _restore_moodle_braces(formatted)
        except (KeyError, IndexError):
            self.feedback_text = text

    def set_counter(self, counter):
        self.counter = counter

    def get_exercise(self):
        text = "\n{}\n        \n        ".format(self.exercise_text)
        if self.feedback_text:
            text += self.feedback_text
        return text

    def statement(self):
        if self.feedback_text is None:
            s1 = questiontext(cdata(self.exercise_text))
            pretty_text = "\n            {}\n            ".format(s1)
        else:
            s1 = questiontext(cdata(self.exercise_text))
            s2 = feedback(cdata(self.feedback_text))
            pretty_text = "\n            {}\n            {}\n            ".format(s1, s2)
        return pretty_text

    def print_args(self):
        args_text = "\n        {}\n{}\n Exercise {}\n        ".format(
            64 * "-", 64 * "-", self.counter
        )
        for k, v in self.parameters.items():
            newline = "{}\n \t key:\t {} \n \t value: \t {}".format(4 * "-", k, v)
            args_text += newline
        return args_text

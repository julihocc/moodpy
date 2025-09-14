def feedback(cdata_text):
    return "<generalfeedback format=\"html\">\n" + cdata_text + "</generalfeedback>\n"


def questiontext(cdata_text):
    return "<questiontext format=\"html\">\n" + cdata_text + "</questiontext>\n"


def cdata(exercise_text):
    return "<text>\n<![CDATA[\n" + exercise_text + "\n]]>\n</text>"


class Generator:
    def __init__(self, counter=0):
        self.counter = counter
        self.header = ""
        self.lambdas = {}
        self.derived = {}  # For derived parameter calculations
        self.parameters = {}
        self.data = {}
        self.exercise_text = ""
        self.feedback_text = None
        self.print = False
        self.requirements = [True]

    def reload_parameters(self):
        for k, f in self.lambdas.items():
            self.parameters[k] = f(k)
    
    def calculate_derived(self):
        """Calculate derived parameters based on current parameters."""
        for k, f in self.derived.items():
            self.parameters[k] = f(self.parameters)

    def test_parameters(self, max_steps=10000, debug = False):
        step = 0
        while step < max_steps:
            if debug:
                print(step)
                print(self.parameters)
            for k, v in self.parameters.items():
                self.parameters[k] = v
            if all(self.requirements):
                if debug: print(self.parameters)
                break
            else:
                step += 1
        if step == max_steps:
            self.parameters = None
            print("requierements not satisfied")

    def set_exercise(self, text):
        # Update data dictionary to include parameters for compatibility
        self.data = self.parameters.copy()
        
        # Try to format with data, fallback to raw text if formatting not needed
        try:
            formatted_text = text.format(d=self.data)
        except (KeyError, IndexError):
            formatted_text = text
            
        self.exercise_text = """
        {0}
        {1}
        """.format(self.header, formatted_text)

    def set_feedback(self, text):
        # Update data dictionary to include parameters for compatibility
        self.data = self.parameters.copy()
        
        # Try to format with data, fallback to raw text if formatting not needed
        try:
            self.feedback_text = text.format(d=self.data)
        except (KeyError, IndexError):
            self.feedback_text = text

    def set_counter(self, counter):
        self.counter = counter

    def get_exercise(self):
        text = """
{}
        
        """.format(self.exercise_text)
        if self.feedback_text:
            text += self.feedback_text
        return text

    def statement(self):
        if self.feedback_text is None:
            s1 = questiontext(cdata(self.exercise_text))
            pretty_text = """
            {}
            """.format(s1)
        else:
            s1 = questiontext(cdata(self.exercise_text))
            s2 = feedback(cdata(self.feedback_text))
            pretty_text = """
            {}
            {}
            """.format(s1, s2)
        return pretty_text

    def print_args(self):
        args_text = """
        {}\n{}\n Exercise {}
        """.format(64 * "-", 64 * "-", self.counter)

        for k, v in self.parameters.items():
            newline = "{}\n \t key:\t {} \n \t value: \t {}".format(4 * "-", k, v)
            args_text += newline

        return args_text


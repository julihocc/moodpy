class Generator:
    def __init__(self, header, counter=0):
        self.counter = counter
        self.header = header
        self.parameters = {}
        self.exercise_text = ""
        self.feedback_text = None
        self.print = False

    def feedback(self, cdata_text):
        return "<generalfeedback format=\"html\">\n" + cdata_text + "</generalfeedback>\n"

    def questiontext(self, cdata_text):
        return "<questiontext format=\"html\">\n" + cdata_text + "</questiontext>\n"

    def cdata(self, exercise_text):
        return "<text>\n<![CDATA[\n" + exercise_text + "\n]]>\n</text>"

    def set_parameter(self, key, value):
        self.parameters[key] = value
        
    def set_exercise(self, text):
        self.exercise_text = self.header + text.format(p=self.parameters)

    def set_feedback(self, text):
        self.feedback_text = text.format(p=self.parameters)

    def set_counter(self, counter):
        self.counter = counter

    def get_exercise(self):
        print(self.exercise_text)
        if self.feedback_text:
            print(self.feedback_text)

    def statement(self):
        if self.feedback_text is None:
            s1 = self.questiontext(self.cdata(self.exercise_text))
            pretty_text = """
            {}
            """.format(s1)
        else:
            s1 = self.questiontext(self.cdata(self.exercise_text))
            s2 = self.feedback(self.cdata(self.feedback_text))
            pretty_text = """
            {}
            {}
            """.format(s1, s2)
        return pretty_text

    def print_args(self):
        print(
            "{}\n{}\n Exercise {}".format(64 * "-", 64 * "-", self.counter)
        )
        for k, v in self.parameters.items():
            print("{}\n \t key:\t {} \n \t value: \t {}".format(4 * "-", k, v))
        print(2 * "\n")
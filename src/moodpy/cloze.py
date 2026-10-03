"""Backward-compatible Cloze exports using the shared generation engine."""

import datetime as dt
import os
from xml.sax.saxutils import escape

from .generator import Generator


class Cloze:
    def __init__(self):
        self.counter = 1
        self.num_question = 1
        self.penalty = 0.5
        self.impr = False
        self.foldername = None
        self.label = None
        self.header = " "
        self.generator = Generator()
        self.tiempo = (
            str(dt.datetime.now()).replace(":", "").replace(".", "").replace("-", "")
        )
        self.filename = None
        self.path = None
        self.xml = []

    def set_generator(self, gen):
        gen.header = self.header
        self.generator = gen

    def set_info(self, materia="", clave="", tema=""):
        self.header = "<h1> {} </h1> \n <h2> {} </h2>".format(
            escape(materia.title()), escape(tema.title())
        )
        self.generator.header = self.header
        self.label = "\n{}\nActividad {}\n{}\n".format(
            materia.upper(), clave, tema.casefold()
        )
        self.foldername = "{}_{}_{}".format(materia.upper(), clave, tema.casefold())
        self.filename = (
            (self.foldername + " " + self.tiempo + ".xml").replace(" ", "_").lower()
        )
        os.makedirs(self.foldername, exist_ok=True)
        self.path = os.path.join(self.foldername, self.filename)

    def get_info(self):
        print("DATETIME: ", self.tiempo)
        print("FOLDERNAME: ", self.foldername)
        print("FILENAME: ", self.filename)

    def format_num(self, places=3):
        return str(self.num_question).zfill(places)

    def testing(self, n, exercise_fn=None):
        temp = "TESTING-" + self.filename.replace(".xml", ".txt")
        parts = []
        for _ in range(n):
            self.generator.set_counter(self.counter)
            self.generator.generate(exercise_fn)
            print(self.generator.parameters)
            parts.extend([self.generator.print_args(), self.generator.get_exercise()])
            self.counter += 1
        with open(temp, "w", encoding="utf-8") as handle:
            handle.write("".join(parts))

    def _question(self, statement):
        num = self.format_num()
        name = escape("Pregunta {} {} {}".format(num, self.foldername, self.tiempo))
        return "\n".join(
            [
                "<!-- question: {}  -->".format(num),
                '<question type="cloze">',
                "<name>",
                "<text>{}</text>".format(name),
                "</name>",
                statement,
                "<penalty>{}</penalty>".format(self.penalty),
                "<hidden>0</hidden>",
                "</question>",
            ]
        )

    def create_question(self):
        """Return the current question without writing or resampling."""
        return self._question(self.generator.statement())

    def save(self):
        self.to_moodle_xml()

    def to_moodle_xml(self):
        assert self.xml
        parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
        for statement in self.xml:
            parts.append(self._question(statement))
            self.num_question += 1
        parts.append("</quiz>\n")
        with open(self.path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(parts))
        print("Ending: {}".format(dt.datetime.now()))
        print("Folder: {}".format(self.foldername))
        print("Filename: {}".format(self.filename))
        print("Number of exercises: {}".format(len(self.xml)))

    def get_exercises(self, cuantos, exercise_fn=None):
        """Generate constraint-valid exercises and export the accumulated bank."""
        assert cuantos > 0
        pending = []
        for _ in range(cuantos):
            self.generator.generate(exercise_fn)
            pending.append(self.generator.statement())
        self.xml.extend(pending)
        self.to_moodle_xml()

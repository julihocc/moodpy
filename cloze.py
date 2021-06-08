# -*- coding: utf-8 -*-

import datetime as dt
import os
from generator import Generator


def format_num(n, places=3):
    n = str(n)
    s = ""
    for _ in range(places - len(n)):
        s += "0"
    return s + n


class Cloze:
    def __init__(self):
        self.counter = 1
        self.num_question = 1
        self.penalty = 0.5
        self.impr = False
        self.foldername = None
        self.path = os.getcwd()
        self.label = None
        self.header = " "
        self.generator = Generator()

    def set_generator(self, gen):
        gen.header = self.header
        self.generator = gen

    def set_label(self, materia="",
                  clave="",
                  tema="",
                  subtema=None,
                  instituto="",
                  semestre=""):
        label = "{}_{}_{}".format(instituto.upper(), semestre, clave)
        # label = "{} {} {}".format("www", clave, tema.title())
        header = "<h1> {} </h1> \n <h2> {} </h2>".format(materia.title(), tema.title())
        if subtema is not None:
            header = header + f'\n <h3> {subtema} </h3>'
        self.label = label
        self.header = header

    def get_header(self):
        print(self.label)
        print(self.header)

    def testing(self, n):
        for k in range(n):
            self.generator.set_counter(self.counter)
            args_text = self.generator.print_args()
            exe_text = self.generator.get_exercise()
            print(args_text + exe_text)
            self.counter += 1

    def get_info(self):
        output = """
        Ubicación: \n\t {}
        Fecha/Hora: \n\t {}
        """.format(self.path, dt.datetime.now())
        print(output)

    def to_moodle_xml(self, mihtml):
        N = len(mihtml)
        assert N != 0
        tiempo = str(dt.datetime.now()).replace(":", "").replace(".", "").replace('-', '')
        filename = (self.foldername + " " + tiempo + ".xml").replace(" ", "_").lower()

        if not os.path.isdir(self.foldername):
            os.makedirs(self.foldername)
        filename = os.path.join(self.foldername, filename)
        print('filename: ', filename)
        # arx = open(filename, "w")
        arx = open(filename, "w", encoding="utf-8")

        arx.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        arx.write("<quiz>\n")
        for k in range(N):
            exercise_text = mihtml[k]
            ahora = str(dt.datetime.now())
            num = format_num(self.num_question)
            # cambiar el número de pregunta
            # arx.write("<!-- question: 0000000  -->" + "\n")
            arx.write("<!-- question: {}  --> \n".format(num))
            arx.write("<question type=\"cloze\">\n")
            arx.write("<name>\n")
            # arx.write("<text>" + leyenda + "-" + ahora + "</text>" + "\n")
            pregunta = "<text>Pregunta {} {} {}</text>\n".format(num,
                                                                 self.foldername,
                                                                 ahora)
            pregunta_utf = pregunta  # .encode()
            arx.write(pregunta_utf)
            arx.write("</name>\n")
            arx.write(exercise_text)
            arx.write("<penalty>{}</penalty>\n".format(str(self.penalty)))
            arx.write("<hidden>0</hidden>\n")
            arx.write("</question>\n")
            self.num_question += 1
        arx.write("</quiz>")
        arx.write(4 * "\n")
        arx.close()

        print(32 * "-*")
        print("Finalizado: {}".format(dt.datetime.now()))
        print("Folder: {}".format(self.foldername))
        print("Filename: {}".format(filename))
        print("#exes: {}".format(k))

    def get_exercises(self, cuantos):
        assert cuantos > 0
        mihtml = []
        for k in range(cuantos):
            exercise_text = self.generator.statement()
            mihtml.append(exercise_text)
        self.to_moodle_xml(mihtml)

    # def quick(self, cuantos=0, xml=None):
    #     if xml:
    #         self.master(cuantos)
    #     elif not xml:
    #         output = self.generator.statement()
    #         print(output)
    #         # return generator(impr=kwargs["impr"], self.header=kwargs["self.header"])
    #     else:
    #         print("xml should be bool")

    # def roll_over(self, generator, lista, print_list=False, save=True):
    #     assert len(lista) > 0
    #     mihtml = []
    #     for _ in lista:
    #         exercise_text = generator()
    #         mihtml.append(exercise_text)
    #     if save:
    #         self.exe_to_moodle(mihtml)
    #     if print_list:
    #         # print(mihtml)
    #         for _ in mihtml:
    #             print(_)
    #
    # def quick_over(self, generator, lista):
    #     if len(lista) > 0:
    #         self.master(generator, lista)
    #     else:
    #         print(generator())

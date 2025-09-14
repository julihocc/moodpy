# -*- coding: utf-8 -*-

import datetime as dt
import os
from .generator import Generator

class Cloze:
    def __init__(self):
        self.counter = 1
        self.num_question = 1
        self.penalty = 0.5
        self.impr = False
        self.foldername= None
        self.path = os.getcwd()
        self.label = None
        self.header = " "
        self.generator = Generator()
        self.tiempo = str(dt.datetime.now()).replace(":", "").replace(".", "").replace('-', '')
        self.filename = None
        self.path = None
        self.xml = []

    def set_generator(self, gen):
        gen.header = self.header
        self.generator = gen

    def set_info(self, materia="",
                  clave="",
                  tema=""):
        #self.label = "{}_{}_{}".format(instituto.upper(), semestre, clave)
        self.header = "<h1> {} </h1> \n <h2> {} </h2>".format(materia.title(), tema.title())
        self.label = """
        {}
        Actividad {}
        {}
        """.format(materia.upper(), clave, tema.casefold())
        self.foldername = "{}_{}_{}".format(materia.upper(), clave, tema.casefold())
        self.foldername = "{}_{}_{}".format(materia.upper(), clave, tema.casefold())
        self.filename = (self.foldername + " " + self.tiempo + ".xml").replace(" ", "_").lower()
        if not os.path.isdir(self.foldername):
            os.makedirs(self.foldername)
        self.path = os.path.join(self.foldername, self.filename)

    def get_info(self):
        #print("LABEL: ", self.label)
        #print("HEADER: ", self.header)
        print("DATETIME: ", self.tiempo)
        print("FOLDERNAME: ", self.foldername)
        print("FILENAME: ", self.filename)

    def format_num(self, places=3):
        n = str(self.num_question)
        s = ""
        for _ in range(places - len(n)):
            s += "0"
        return s + n

    def testing(self, n):
        temp = os.path.join(self.foldername, "TESTING-"+self.filename.replace(".xml", ".txt"))
        arx = open(temp, "w", encoding="utf-8")
        for k in range(n):
            self.generator.set_counter(self.counter)
            self.generator.reload_parameters()
            print(self.generator.parameters)
            args_text = self.generator.print_args()
            exe_text = self.generator.get_exercise()
            #print(args_text + exe_text)
            arx.write(args_text)
            arx.write(exe_text)
            self.counter += 1
        arx.close()

    def to_moodle_xml(self):
        N = len(self.xml)
        assert N != 0
        # arx = open(self.filename, "w")
        arx = open(self.path, "w", encoding="utf-8")
        arx.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        arx.write("<quiz>\n")
        for k in range(N):
            exercise_text = self.xml[k]
            num = self.format_num()
            # cambiar el número de pregunta
            # arx.write("<!-- question: 0000000  -->" + "\n")
            arx.write("<!-- question: {}  --> \n".format(num))
            arx.write("<question type=\"cloze\">\n")
            arx.write("<name>\n")
            # arx.write("<text>" + leyenda + "-" + ahora + "</text>" + "\n")
            pregunta = "<text>Pregunta {} {} {}</text>\n".format(num,
                                                                 self.foldername,
                                                                 self.tiempo)
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
        print("Ending: {}".format(dt.datetime.now()))
        print("Folder: {}".format(self.foldername))
        print("Filename: {}".format(self.filename))
        print("Number of exercises: {}".format(N))

    def get_exercises(self, cuantos):
        assert cuantos > 0
        for k in range(cuantos):
            self.generator.reload_parameters()
            exercise_text = self.generator.statement()
            self.xml.append(exercise_text)
        self.to_moodle_xml()

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

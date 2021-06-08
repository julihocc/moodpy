# -*- coding: utf-8 -*-

import datetime as dt
import os


def format_num(n, places=3):
    n = str(n)
    s = ""
    for _ in range(places - len(n)):
        s += "0"
    return s + n


def feedback(cdata_text):
    return "<generalfeedback format=\"html\">\n" + cdata_text + "</generalfeedback>\n"


def questiontext(cdata_text):
    return "<questiontext format=\"html\">\n" + cdata_text + "</questiontext>\n"


def cdata(ejercicio):
    return "<text>\n<![CDATA[\n" + ejercicio + "\n]]>\n</text>"


def print_args(lista_dictionaries, counter=None, impr=True, for_print=None):
    if impr or counter in for_print:
        print(
            "{}\n{}\n Exercise {}".format(64 * "-", 64 * "-", counter)
        )
    for lab, dic in lista_dictionaries:
        if impr or counter in for_print:
            print("{}\n Dictionary : {}".format(8 * "-", lab))
        for k, v in dic.items():
            if impr or counter in for_print:
                print("{}\n \t key:\t {} \n \t value: \t {}".format(4 *
                                                                    "-", k, v))
            else:
                pass
    if impr or counter in for_print:
        print(2 * "\n")


class Cloze:
    def __init__(self):
        self.counter = 0
        self.num_question = 1
        self.foldername = None
        self.path = os.getcwd()
        self.label = None
        self.mi_cabecera = " "
        self.data = None
        self.tex = None
        self.answers = None
        self.feedback_text = None
        self.ejercicio = None
        self.retroalimentacion = None

    def set_label(self, materia="",
                   clave="",
                   tema="",
                   subtema=None,
                   instituto="",
                   semestre=""):
        label = "{}_{}_{}".format(instituto.upper(), semestre, clave)
        # label = "{} {} {}".format("www", clave, tema.title())
        mi_cabecera = "<h1> {} </h1> \n <h2> {} </h2>".format(materia.title(), tema.title())
        if subtema is not None:
            mi_cabecera = mi_cabecera + f'\n <h3> {subtema} </h3>'
        self.label = label
        self.mi_cabecera = mi_cabecera

    def get_header(self):
        print(self.label)
        print(self.mi_cabecera)

    def set_exercise(self, text):
        self.ejercicio = self.mi_cabecera + text.format(d=self.data, t=self.tex, a=self.answers, f=self.feedback_text)

    def get_exercise(self):
        print(self.ejercicio)
        if self.retroalimentacion:
            print(self.retroalimentacion)

    def set_feedback(self, text):
        self.retroalimentacion = text.format(d=self.data, t=self.tex, a=self.answers, f=self.feedback_text)

    def pretty(self):
        if self.retroalimentacion is None:
            s1 = questiontext(cdata(self.ejercicio))
            pretty_text = """
            {}
            """.format(s1)
        else:
            s1 = questiontext(cdata(self.ejercicio))
            s2 = feedback(cdata(self.retroalimentacion))
            pretty_text = """
            {}
            {}
            """.format(s1, s2)
        return pretty_text

    def generador(self):
        if self.feedback_text is None:
            self.feedback_text = {}
        if self.answers is None:
            self.answers = {}
        if self.tex is None:
            self.tex = {}
        if self.data is None:
            self.data = {}

        return self.pretty()

    def testing(self, n, impr=True, for_print=None):
        if for_print is None:
            for_print = []
        for k in range(n):
            lista_dictionaries = self.generador().items()
            print_args(lista_dictionaries, impr=impr, for_print=for_print)
            self.counter += 1

    def get_info(self):
        output = """
        Ubicación: \n\t {}
        Fecha/Hora: \n\t {}
        """.format(self.path, dt.datetime.now())
        print(output)

    def exe_to_moodle(self, foldername, mihtml, penalizacion=0.5):
        k = len(mihtml)
        assert k != 0
        foldername = str(foldername)
        tiempo = str(dt.datetime.now()).replace(":", "").replace(".", "").replace('-', '')
        filename = (foldername + " " + tiempo + ".xml").replace(" ", "_").lower()

        if not os.path.isdir(foldername):
            os.makedirs(foldername)
        filename = os.path.join(foldername, filename)
        print('filename: ', filename)
        # arx = open(filename, "w")
        arx = open(filename, "w", encoding="utf-8")

        arx.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        arx.write("<quiz>\n")
        for k in range(k):
            ejercicio = mihtml[k]
            ahora = str(dt.datetime.now())
            num = format_num(self.num_question)
            # cambiar el número de pregunta
            # arx.write("<!-- question: 0000000  -->" + "\n")
            arx.write("<!-- question: {}  --> \n".format(num))
            arx.write("<question type=\"cloze\">\n")
            arx.write("<name>\n")
            # arx.write("<text>" + leyenda + "-" + ahora + "</text>" + "\n")
            pregunta = "<text>Pregunta {} {} {}</text>\n".format(num,
                                                                 foldername,
                                                                 ahora)
            pregunta_utf = pregunta  # .encode()
            arx.write(pregunta_utf)
            arx.write("</name>\n")
            arx.write(ejercicio)
            arx.write("<penalty>{}</penalty>\n".format(str(penalizacion)))
            arx.write("<hidden>0</hidden>\n")
            arx.write("</question>\n")
            self.num_question += 1
        arx.write("</quiz>")
        arx.write(4 * "\n")
        arx.close()

        print(32 * "-*")
        print("Finalizado: {}".format(dt.datetime.now()))
        print("Folder: {}".format(foldername))
        print("Filename: {}".format(filename))
        print("#exes: {}".format(k))

    def master(self, generador, ubicacion, cuantos, cabecera):
        assert cuantos > 0
        mihtml = []
        for k in range(cuantos):
            ejercicio = generador(cabecera)
            mihtml.append(ejercicio)
        self.exe_to_moodle(ubicacion, mihtml)

    def quick(self, generador, ubicacion="./", cuantos=0, xml=None, cabecera="Empty header"):
        if xml:
            self.master(generador, ubicacion, cuantos, cabecera)
        elif not xml:
            output = generador(cabecera, impr=True)
            print(output)
            # return generador(impr=kwargs["impr"], cabecera=kwargs["cabecera"])
        else:
            print("xml should be bool")

    def roll_over(self, generador, lista, donde, impr=False, print_list=False, save=True, cabecera=""):
        assert len(lista) > 0
        mihtml = []
        for params in lista:
            ejercicio = generador(params, impr, cabecera)
            mihtml.append(ejercicio)
        if save:
            self.exe_to_moodle(donde, mihtml)
        if print_list:
            # print(mihtml)
            for _ in mihtml:
                print(_)

    def quick_over(self, generador, lista, donde, impr=0, cabecera=""):
        if len(lista) > 0:
            self.master(generador, lista, donde, impr)
        else:
            print(generador(impr, cabecera))

# -*- coding: utf-8 -*-

import datetime as dt
import numpy as np
import os

counter = 0
num_question = 1

def format_num(n):
    n = str(n)
    l = len(n)
    s = ""
    for _ in range(4-l):
        s+="0"
    return s+n

def ExeToMoodle(leyenda, mihtml, mifb=[], penal=0.5):
    global num_question # para enumerar preguntas
    K = len(mihtml)
    assert K != 0
    leyenda = str(leyenda)
    print(32 * "-*")
    print("Finalizado: {}".format(dt.datetime.now()))
    tiempo = str(dt.datetime.now()).replace(":", "-").replace(".", "-")
    foldername = leyenda
    print("Folder: {}".format(foldername))
    filename = (leyenda + " " + tiempo + ".xml").replace(" ", "_").lower()
    print("Filename: {}".format(filename))
    print("#exes: {}".format(K))

    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    filename = os.path.join(foldername, filename)
    arx = open(filename, "w")  # ,  encoding="utf-8")

    arx.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    arx.write("<quiz>\n")
    for k in range(K):
        ejercicio = mihtml[k]
        ahora = str(dt.datetime.now())
        num = format_num(num_question)
        # cambiar el número de pregunta
        # arx.write("<!-- question: 0000000  -->" + "\n")
        arx.write("<!-- question: {}  --> \n".format(num))
        arx.write("<question type=\"cloze\">\n")
        arx.write("<name>\n")
        #arx.write("<text>" + leyenda + "-" + ahora + "</text>" + "\n")
        arx.write("<text>Pregunta {} {} {}</text>\n".format(num,leyenda,ahora))
        arx.write("</name>\n")
        arx.write(ejercicio)
        arx.write("<penalty>{}</penalty>\n".format(str(penal)))
        arx.write("<hidden>0</hidden>\n")
        arx.write("</question>\n")
        num_question+=1
    arx.write("</quiz>")
    arx.write(4*"\n")
    arx.close()


def pretty(exercise, retro=None):
    if retro is None:
        s1 = questiontext(cdata(exercise))
        pretty = """
        {}
        """.format(s1)
    else:
        s1 = questiontext(cdata(exercise))
        s2 = feedback(cdata(retro))
        pretty = """
        {}
        {}
        """.format(s1, s2)
    return pretty


def feedback(cdata):
    return "<generalfeedback format=\"html\">\n" + cdata + "</generalfeedback>\n"


def questiontext(cdata):
    return "<questiontext format=\"html\">\n" + cdata + "</questiontext>\n"


def cdata(ejercicio):
    return "<text>\n<![CDATA[\n" + ejercicio + "\n]]>\n</text>"


def master_old(generador, donde, bloques, impr=False, cabecera=""):
    assert bloques > 0
    mihtml = []
    for k in range(bloques):
        ejercicio = generador(impr, cabecera)
        mihtml.append(ejercicio)
    ExeToMoodle(donde, mihtml)


def quick_old(generador, donde, ready, impr=0, cabecera=""):
    if ready:
        master(generador, donde, ready, impr, cabecera)
    else:
        print(generador(impr=impr, cabecera=cabecera))

def master(generador, donde, bloques, **kwargs):
    assert bloques > 0
    mihtml = []
    for k in range(bloques):
        ejercicio = generador(**kwargs)
        mihtml.append(ejercicio)
    ExeToMoodle(donde, mihtml)

def quick(generador, donde, ready, **kwargs):
    if ready:
        master(generador, donde, ready, **kwargs)
    else:
        print(generador(impr=kwargs["impr"], cabecera=kwargs["cabecera"]))


def rollOver(generador, lista, donde, impr=False, print_list=False, save=True, cabecera=""):
    assert len(lista) > 0
    mihtml = []
    for params in lista:
        ejercicio = generador(params, impr, cabecera)
        mihtml.append(ejercicio)
    if save:
        ExeToMoodle(donde, mihtml)
    if print_list:
        # print(mihtml)
        for _ in mihtml:
            print(_)


def quickOver(generador, lista, donde, impr=0, cabecera=""):
    if len(lista) > 0:
        master(generador, lista, donde, impr, cabecera)
    else:
        print(generador(impr, cabecera))

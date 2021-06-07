# -*- coding: utf-8 -*-

import datetime as dt
import numpy as np
import os

###to numeric question
def NM(x, entero=False, percent=False, error=0.001):
    if entero:
        x = int(x)
        sx = str(x)
        stol=str(0)
        return "{1:NM:="+sx+"}"
    if percent:
        x+=x*100.0
    else:
        sx = str(1.0*x)
        tol = x*error
        stol = str(tol)
        #print sx, type(sx)
        #
        #print(x,type(x))
        if np.isclose(0,x):            
            return "{1:NM:=0:0.00001}"
        else:
            return "{1:NM:="+sx+":"+stol+"}"

def ExeToMoodle(leyenda, mihtml, mifb=[], penal = 0.5):
    K = len(mihtml)
    assert K!=0
    leyenda=str(leyenda)
    print(32*"-")
    print("Finalizado: {}".format(dt.datetime.now()))
    tiempo=str(dt.datetime.now()).replace(":","-").replace(".","-")
    foldername=leyenda
    print("Folder: {}".format(foldername))
    filename=(leyenda+" "+tiempo+".xml").replace(" ","_").lower()
    print("Filename: {}".format(filename))
    print("#exes: {}".format(K))

    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    filename = os.path.join(foldername, filename)
    arx = open(filename, "w")#,  encoding="utf-8")

    arx.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    arx.write("<quiz>\n")
    for k in range(K):
      ejercicio=mihtml[k]
      ahora=str(dt.datetime.now())
      arx.write("<!-- question: 0000000  -->"+"\n")
      arx.write("<question type=\"cloze\">\n")
      arx.write("<name>\n")
      arx.write("<text>"+leyenda+"-"+ahora+"</text>"+"\n")
      arx.write("</name>\n")
      arx.write(ejercicio)
      arx.write("<penalty>{}</penalty>\n".format(str(penal)))
      arx.write("<hidden>0</hidden>\n")
      arx.write("</question>\n")
    arx.write("</quiz>\n")
    arx.close()

def pretty(exercise, retro=None, im1="", im2=""):
    if retro is None:
        s1 = questiontext(cdata(exercise)+im1)
        pretty="""
        {}
        """.format(s1)
    else:
        s1 = questiontext(cdata(exercise)+im1)
        s2 = feedback(cdata(retro)+im2)
        pretty="""
        {}
        {}
        """.format(s1,s2)
    return pretty

def feedback(cdata):
    return "<generalfeedback format=\"html\">\n"+cdata+"</generalfeedback>\n"

def questiontext(cdata):
    return "<questiontext format=\"html\">\n"+cdata+"</questiontext>\n"

def cdata(ejercicio):
    return "<text>\n<![CDATA[\n"+ejercicio+"\n]]>\n</text>"

def master(generador, donde, bloques, impr = False, cabecera=""):
    assert bloques > 0
    mihtml=[]
    for k in range(bloques):
        ejercicio = generador(impr, cabecera)
        mihtml.append(ejercicio)
    ExeToMoodle(donde, mihtml)

def quick(generador, donde, ready, impr=0, cabecera=""):
    if ready:
        master(generador, donde, ready, impr, cabecera)
    else:
        print(generador(impr, cabecera))

def rollOver(generador, lista, donde, impr=False, print_list = False, save=True, cabecera=""):
    assert len(lista) > 0
    mihtml=[]
    for params in lista:
        ejercicio = generador(params, impr, cabecera)
        mihtml.append(ejercicio)
    if save:
        ExeToMoodle(donde, mihtml)
    if print_list:
        #print(mihtml)
        for _ in mihtml:
            print(_)

def quickOver(generador, lista, donde, impr=0, cabecera=""):
    if len(lista)>0:
        master(generador, lista, donde, impr, cabecera)
    else:
        print(generador(impr, cabecera))

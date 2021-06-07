# -*- coding: utf-8 -*-

import datetime as dt
import time
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

def wrint(frase, archivo, prueba=0):
  if prueba:
    print(frase)
  else:
    archivo.write(frase+"\n")

def toIm1(nom_grafica):
    return "</p>\n<p>\n<img src=\"@@PLUGINFILE@@/"+nom_grafica+"\" alt=\"\" width=\"783\" height=\"585\" />\n"

def toIm2(nom_grafica, cod_grafica):
    return "<file name=\""+nom_grafica+"\" path=\"/\" encoding=\"base64\">"+cod_grafica+"</file>"


def ExeToMoodle(leyenda, mihtml, mifb=[], penal = 0.5):
    K = len(mihtml)
    assert K!=0
    leyenda=str(leyenda)
    print(32*"-")
    print("Done: {}".format(dt.datetime.now()))
        #print(time.time())
    tiempo=str(time.time())
    foldername=leyenda
    print("Folder: {}".format(foldername))
    filename=leyenda+"-"+tiempo+".xml"
    print("Filename: {}".format(filename))
    print("#exes: {}".format(K))
    #print nombre

    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    filename = os.path.join(foldername, filename)
    arx = open(filename, "w")#,  encoding="utf-8")

    arx.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    arx.write("<quiz>\n")
    for k in range(K):
      ejercicio=mihtml[k]
      ahora=str(time.time())
      arx.write("<!-- question: 0000000  -->"+"\n")
      arx.write("<question type=\"cloze\">\n")
      arx.write("<name>\n")
      arx.write("<text>"+leyenda+"-"+ahora+"</text>"+"\n")
      arx.write("</name>\n")
      #arx.write("<questiontext format=\"html\">\n")
      arx.write(ejercicio)
      #arx.write("</questiontext>\n")
      #arx.write("<generalfeedback format=\"html\">\n")
      #arx.write("<text><![CDATA[<pre> </pre>]]></text>\n")
      #arx.write("</generalfeedback>\n")
      arx.write("<penalty>{}</penalty>\n".format(str(penal)))
      arx.write("<hidden>0</hidden>\n")
      arx.write("</question>\n")
    arx.write("</quiz>\n")
    arx.close()

def pretty(arg1, arg2="", im1="", im2=""):
    s1 = questiontext(cdata(arg1)+im1)
    s2 = feedback(cdata(arg2)+im2)
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

def keys2str(dic):
    dic2 = {}
    for _ in dic.keys():
        dic2[str(_)]=dic[_]
    return dic2

def sol2ans(sol, rat=False):
    ans = {}
    if rat:
        for s in sol.keys():
            print(s, type(s))
            xq = sol[s].as_numer_denom()
            num = "{}n".format(s)
            den = "{}d".format(s)
            print(num,den, xq)
            code = "{}= xq[0]".format(num)
            exec(code)
            code = "ans[\"{}\"]=NM(xn, entero=True)".format(num)
            exec(code)
            code = "ans[\"{}\"]=NM(xd, entero=True)".format(den)
            exec(code)
    return ans

def indSols():
    indicaciones = " <ul> <li> Simplifique las fracciones. </li> \
    <li> Si una solución es entera, utilice el denominador igual con uno. </li> \
    <li> Si la fracción es negativa, indique el signo en el numerador. </li> \
    <li> Ingrese las soluciones de menor a mayor </li> </ul>"
    return indicaciones

def indFrac():
    indicaciones = " <ul> <li> Simplifique las fracciones. </li> \
    <li> Si la fracción representa entero, utilice el denominador igual con uno. </li> \
    <li> Si la fracción es negativa, indique el signo en el numerador. </li> \
    </ul>"
    return indicaciones

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

def rollOver(generador, lista, donde, impr = False, save=True, cabecera=""):
    assert len(lista) > 0
    mihtml=[]
    for params in lista:
        ejercicio = generador(params, impr, cabecera)
        mihtml.append(ejercicio)
    if save:
        ExeToMoodle(donde, mihtml)
    if impr:
        print(mihtml)

def quickOver(generador, lista, donde, impr=0, cabecera=""):
    if len(lista)>0:
        master(generador, lista, donde, impr, cabecera)
    else:
        print(generador(impr, cabecera))
        
def tagImg(nom_graf, alt="imagen", width="600", height="400"):
    code = """<p>
    <img src=\"@@PLUGINFILE@@/{}\" alt=\"{}\" width=\"{}\" height=\"{}\" />
    </p>""".format(nom_graf,alt,width,height)
    return code

def fileImg(nom_graf, cod_graf):
    code = """
    <file name=\"{}\" path=\"/\" encoding=\"base64\">{}</file>
    """.format(nom_graf, cod_graf)
    return code

def encodePlot(*args):
    plt.plot(*args)
    tiempo=str(time.time())
    filename=tiempo+".png"
    foldername="./temp"
    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    folderFile = os.path.join(foldername, filename)
    plt.savefig(folderFile)
    plt.close()
    with open(folderFile, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    return filename, encoded

def encodeGraf(graf):
    #plt.plot(*args)
    tiempo=str(time.time())
    filename=tiempo+".png"
    foldername="./temp"
    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    folderFile = os.path.join(foldername, filename)
    graf.save(folderFile)
    with open(folderFile, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    return filename, encoded

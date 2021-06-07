# -*- coding: utf-8 -*-

"""
tools

herramientas de uso común para desarrollar librerías Moodpy
"""

import datetime as dt
import numpy as np
import os
import matplotlib.pyplot as plt

counter = 0

def txt2arr(temp, array=True):
    arr = ' '.join(temp.split()).replace(" ",",")
    x = {}
    exec("x[None] = {}".format(arr))    
    if array:
        return np.array(x[None])
    else: 
        return x[None]

def round_normal(m=0,s=1,size=1,a=-np.inf, b=np.inf, d=0):
    """
    m: mean
    s: standart deviation
    n: size of the array
    a: lower bound
    b: upper bound
    d: round to d decimals
    """
    while True:
        x = np.around(np.random.normal(loc=m, scale=s, size=size), d)
        if np.all( (a<=x) & (x<=b) ):
            return x
        
def int_normal(m=0,s=1,size=1,a=-np.inf, b=np.inf):
    """
    m: mean
    s: standart deviation
    n: size of the array
    a: lower bound
    b: upper bound    
    """
    x = round_normal(m=m, s=s, size=size, a=a, b=b)
    return x.astype("int")

def matlabfy(A, vector=False):
    M = "["
    for i in range(A.nrows()):
        row = ""
        for j in range(A.ncols()):
            row+=str(A[i,j])+","
        if vector:
            M+=row[:-1]+";"
        else:
            M+=row[:-1]+";\n"
    if vector:
        M = M[:-1]+"]"
    else:
        M = M[:-2]+"]"
    return M

def show_latex(a):
    ax = plt.axes([0,0,0.3,0.3]) #left,bottom,width,height
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.text(0.4,0.4,'$%s$' %a,size=50,color="green")

def print_args(lista_dictionarios, counter=None, impr=True, for_print=[]):
    if impr or counter in for_print:
        print(
        "{}\n{}\n Exercise {}".format(64 * "-", 64 * "-", counter)
        )
    for lab, dic in lista_dictionarios:
        if impr or counter in for_print: print(
            "{}\n Dictionary : {}".format(8 * "-", lab))
        for k, v in dic.items():
            if impr or counter in for_print:
                print("{}\n \t key:\t {} \n \t value: \t {}".format(4 *
                                                                      "-", k, v))
            else:
                pass
    if impr or counter in for_print:
        print(2 * "\n")

def testing(n, generador, impr=True, for_print=[]):
    global counter
    for k in range(n):
        lista_dictionarios = generador().items()
        print_args(lista_dictionarios, counter=counter, impr=impr, for_print=for_print)
        counter +=1

def make_label(materia = "",
               clave = "",
               tema = "",
               subtema=None,
               instituto="",
               semestre=""):
    label = "{}_{}_{}".format(instituto.upper(),semestre,clave)
    #label = "{} {} {}".format("www", clave, tema.title())
    miCabecera = "<h1> {} </h1> \n <h2> {} </h2>".format(materia.title(), tema.title())
    if subtema is not None:
        miCabecera = miCabecera+f'\n <h3> {subtema} </h3>'
    return label, miCabecera


###to numeric question
def NM(x, entero=False, percent=False, error=0.001, round_zero=False):
    if entero:
        x = int(x)
        sx = str(x)
        stol = str(0)
        return "{1:NM:=" + sx + "}"
    if percent:
        x += x * 100.0
    else:
        sx = str(1.0 * x)
        tol = x * error
        if tol<0:
            tol = -tol
        stol = str(tol)
        # print sx, type(sx)
        #
        # print(x,type(x))
        if np.isclose(0, x) and round_zero:
            return "{1:NM:=0:0.00001}"
        else:
            return "{1:NM:=" + sx + ":" + stol + "}"

import os
path = os.getcwd()

def test():
    output = """
    Ubicación: \n\t {}
    Fecha/Hora: \n\t {}
    """.format(path, dt.datetime.now())
    print(output)
    

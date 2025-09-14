"""
{} {} {}

Migrated from legacy generator: 303-1 Transformada Inversa I-checkpoint.py
Subject Area: mathematics

This module contains educational content generators for MoodPy v3.0.0.
"""

import moodpy
from moodpy import Generator, Cloze
import numpy as np
import numpy.random as rnd

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass




import sys
ruta = r"D:\juliho.castillo@yahoo.com\MOODPY\moodpy"
sys.path.append(ruta)

import moodpy as me
import numpy as np
np.random.seed(123)
sage.misc.html._old_and_deprecated_behavior = False



"""
CAMBIAR CLAVE Y TEMA!!!
"""
MATERIA = "XXX"
CLAVE = "000"
TEMA = "---"
label = "{} {} {}".format(MATERIA, CLAVE, TEMA.title())
miCabecera = "<h1> {} </h1>".format(TEMA.title())
print("<h1>"+label+"</h1>")
print(miCabecera)



"""
Funciones
"""






"""
Ejercicios
"""




def gen_exercise(impr=False, cabecera=""):
    data ={}
    tex = {}
    answers = {}
    feedback = {}

    
    ejercicio = cabecera + r"""

    """.format(d=data, t=tex, a=answers, f=feedback)
    
    retroalimentacion = """
    
    """.format(d=data, t=tex, a=answers, f=feedback)
    
    return me.pretty(ejercicio, retroalimentacion)



# print(html("<h1>"+label+"</h1>"))
# me.quick(gen_exercise, label, 0, impr=True, cabecera=miCabecera)



# me.quick(gen_exercise, label, 5, impr=True, cabecera=miCabecera)



# me.quick(gen_exercise, label, 500, impr=False, cabecera=miCabecera)

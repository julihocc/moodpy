"""
{} {} {}

Migrated from legacy generator: Mate Financiera 105 Rendimiento Anual Efectivo-checkpoint.py
Subject Area: finance

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

# -*- coding: utf-8 -*-



# **Esta es una plantilla**
# **¡NO MODIFICAR PARA USO CORRIENTE!**



import moodpy as me
import numpy as np
np.random.seed(123)
# sage.misc.html._old_and_deprecated_behavior = False  # TODO: Replace Sage functionality



"""
CAMBIAR CLAVE Y TEMA!!!
"""
MATERIA = "Matemáticas Financieras"
CLAVE = "000"
TEMA = "---"
label = "{} {} {}".format(MATERIA, CLAVE, TEMA.upper())
miCabecera = "<h1> {} </h1>".format(TEMA.title())
print("<h1>"+label+"</h1>")
print(miCabecera)




# Funciones






# Generador de ejercicios



def gen_exercise(impr=False, cabecera=""):
    data ={}
    answers = {}
    feedback = {}
    
    ejercicio = cabecera + """
    
    """.format(a=answers, d=data)
    
    retroalimentacion = """
    
    """.format(f=feedback)
    
    return me.pretty(ejercicio, retroalimentacion)
    
# print(html("<h1>"+label+"</h1>"))  # TODO: Convert HTML output for MoodPy
me.quick(gen_exercise, label, 0, impr=True, cabecera=miCabecera)



# me.quick(gen_exercise, label, 5, impr=True, cabecera=miCabecera)



# me.quick(gen_exercise, label, 50, impr=True, cabecera=miCabecera)



# me.quick(gen_exercise, label, 500, impr=False, cabecera=miCabecera)

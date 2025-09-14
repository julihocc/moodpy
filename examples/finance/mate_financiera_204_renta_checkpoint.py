"""
{} {} {}

Migrated from legacy generator: Mate Financiera 204 Renta-checkpoint.py
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



import moodpy as me
import numpy as np
np.random.seed(123)
# sage.misc.html._old_and_deprecated_behavior = False  # TODO: Replace Sage functionality



"""
CAMBIAR CLAVE Y TEMA!!!
"""
MATERIA = "Matemáticas Financieras"
CLAVE = "204"
TEMA = "Amortización"
label = "{} {} {}".format(MATERIA, CLAVE, TEMA.upper())
miCabecera = "<h1> {} </h1>".format(TEMA.title())
print("<h1>"+label+"</h1>")
print(miCabecera)



# Funciones



frec = {1:"anualmente", 2:"semestralmente", 3:"cuatrimestral", 4:"trimestralmente", 6:"bimestralmente", 12: "mensualmente"}




def gen_params():
    A = np.random.poisson(100)*1000
    f = np.random.choice(list(frec.keys()))
    T = np.random.poisson(10)
    r100 = np.around(
        np.random.normal(10,2.5), 2
    )
    if A>0 and T>1 and r100>0:
        return A,f,T,r100




def alpha(i, N):
    return (1-(1+i)^(-N))/i




def trans_params(A,f,T,r100):
    N = T*f
    r = r100/100
    i = r/f
    return i, N, r




def get_R(A,f,T,r100):
    i, N, r =  trans_params(A,f,T,r100)
    R = A/alpha(i, N)
    return R




"""
Test
"""
A,f,T,r100 = gen_params()
print(A,f,T,r100)
R = get_R(A,f,T,r100)
print(R)




# Generador de ejercicios



def gen_exercise(impr=False, cabecera = ""):
    data = {}
    answers = {}
    A,f,T,r100 = gen_params()
    if impr: print(A,f,T,r100)
    R = get_R(A,f,T,r100)
    if impr: print(R)    
    data["A"] = A
    data["frec"] = frec[f]
    data["T"] = T
    data["r100"] = r100
    answers["R"] = me.NM(R)
    
    ejercicio = cabecera + """
    <p>
    Se contrae una deuda con un valor presente de ${d[A]}, que se 
    pagará en {d[T]} años, a una tasa de interés de {d[r100]}%, compuesta
    {d[frec]}. 
    </p>
    <p>
    ¿Cuál es el monto \\(R\\) del pago que se debe hacer {d[frec]}, 
    para cubrir dicha deuda?
    </p>
    <p>
    \\(R=\\){a[R]}
    </p>
    """.format(a=answers, d=data)
    
    retroalimentacion = """
    <iframe width="560" height="315" 
    src="https://www.youtube.com/embed/videoseries?list=PLblwZNylw7eGFRCMf9ocguZzS3YzvLy7e" 
    frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; 
    picture-in-picture" allowfullscreen></iframe>
    """
    
    return me.pretty(ejercicio, retroalimentacion)
    
# print(html("<h1>"+label+"</h1>"))  # TODO: Convert HTML output for MoodPy
me.quick(gen_exercise, label, 0, impr=True, cabecera=miCabecera)



me.quick(gen_exercise, label, 5, impr=True, cabecera=miCabecera)



me.quick(gen_exercise, label, 500, impr=False, cabecera=miCabecera)




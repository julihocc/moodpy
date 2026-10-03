"""
MOODPY_{}_{}_{}

Migrated from legacy generator: Matemáticas Financieras 301 Tablas de amortización-Copy1-checkpoint.py
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
CLAVE = "301"
TEMA = "Tablas de Amortización"
label = "MOODPY_{}_{}_{}".format(MATERIA, CLAVE, TEMA.upper())
miCabecera = "<h1> {} </h1>".format(TEMA.title())
print("<h1>"+label+"</h1>")
print(miCabecera)



frec = {1:"anualmente", 2:"semestralmente", 3:"cuatrimestral", 4:"trimestralmente", 6:"bimestralmente", 12: "mensualmente"}




def get_params():
    while True:
        A = np.random.poisson(100)*100
        r = np.around(np.random.poisson(10)/100.0,2)
        f = np.random.choice(list(frec.keys()))
        _N = np.random.poisson(10)
        T = np.around(_N/f).astype(int)
        if np.prod([A, r, f, T])!=0:
            return A, r, f, T

A,r,f,T = get_params()
print(A,r,f,T)




def gen_table(A,r,f,T):
    
    tabla = [
        ["Periodo", "Capital insoluto", "Interés vencido", "Pago", "Capital pagado", "Capital al vencimiento"]
    ]
    
    N = (T*f).astype(int)
    i = r/f
    a = (1-(1+i)^-N)/i#; print(a)
    R = 1.0*A/a#; print(R)
    
    capital_vencimiento = {}
    capital_insoluto = {}
    interes_vencido = {}
    capital_pagado ={}

    capital_vencimiento[0] = A
    
    for periodo in range(1,N+1):
        capital_insoluto[periodo] = capital_vencimiento[periodo-1]
        interes_vencido[periodo] = capital_insoluto[periodo] * i
        capital_pagado[periodo] = R - interes_vencido[periodo]
        capital_vencimiento[periodo] = capital_insoluto[periodo]-capital_pagado[periodo]
        tabla.append([
            str(periodo),
            me.NM(capital_insoluto[periodo]),
            me.NM(interes_vencido[periodo]),
            me.NM(R),
            me.NM(capital_pagado[periodo]),
            me.NM(capital_vencimiento[periodo])     
        ])
    
    return tabla

tab = gen_table(A,r,f,T)
# show(html(table(tab, header_row=True, header_column=True, frame=True)))  # TODO: Convert HTML output for MoodPy
# print(html(table(tab, header_row=True, header_column=True, frame=True)))  # TODO: Convert HTML output for MoodPy



params = get_params()
tab = gen_table(*params)
#print(tab)









def gen_exercise(impr=False, cabecera=""):
    
    params = get_params()
    #print(params)
    keys = ["A","r","f","T"]
    data = dict(zip(keys,params))
    data["r100"] = data["r"]*100
    data["frec"] = frec[data["f"]]
    answers = {}
    tab = gen_table(*params)
#     answers["tab"] = html(table(tab, header_row=True, header_column=True, frame=True))  # TODO: Convert HTML output for MoodPy
    feedback = {}
    
    ejercicio = cabecera + """
    Se pide un préstamo de ${d[A]}, al {d[r100]}% anual, compuesto {d[frec]}, pagadero a {d[T]} años. 
    Complete la correspondiente tabla de amortización:
    <p>
    {a[tab]}
    </p>
    """.format(a=answers, d=data)
    
    retroalimentacion = """
    
    """.format(f=feedback)
    
    return me.pretty(ejercicio, retroalimentacion)
    
# print(html("<h1>"+label+"</h1>"))  # TODO: Convert HTML output for MoodPy
me.quick(gen_exercise, label, 0, impr=True, cabecera=miCabecera)



me.quick(gen_exercise, label, 5, impr=True, cabecera=miCabecera)



me.quick(gen_exercise, label, 50, impr=True, cabecera=miCabecera)



me.quick(gen_exercise, label, 100, impr=False, cabecera=miCabecera)



me.quick(gen_exercise, label, 100, impr=False, cabecera=miCabecera)

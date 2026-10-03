"""
MOODPY MAN 101 PRECIO DE EQUILIBRIO

Migrated from legacy generator: MOODPY MAN 101 PRECIO DE EQUILIBRIO.py
Subject Area: economics

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




import moodpy as me
import numpy as np
import numpy.random as rnd
sage.misc.html._old_and_deprecated_behavior = False



label = "MOODPY MAN 101 PRECIO DE EQUILIBRIO"
miCabecera = "<h1> Precio de equilibrio </h1>"
print(html("<h1>"+label+"</h1>"))
print(html(miCabecera))




def gen_params():
    u_eq = np.random.poisson(100)
    p_s = np.random.poisson(1000)    
    S(u) = p_s*u
    p_eq = S(u_eq)
    p_d = -np.random.poisson(1000)  
    D(u) = p_eq + p_d*(u-u_eq)
    u_null = -p_eq/p_d +u_eq
    malla = np.arange(0, u_null, 1)
    n = 4
    while 1:
        unidades_us = np.random.choice(malla, n, replace=False)
        if u_eq not in unidades_us:
            break
    while 1:
        unidades = np.sort(unidades_us)
        if not(u_eq in unidades):
            break
    return u_eq, unidades, S, D




def gen(impr, cabecera=""):
    #creamos los diccionarios que alimentan el ejercicio
    data = {}
    answers = {}
    # diseño del ejercicio
    tabla = [["Unidades", "Precio de oferta", "Precio de Demanda"]]
    oferta = []
    demanda = []
    u_eq, unidades, S, D = gen_params()
    assert np.isclose(float(S(u_eq)), float(D(u_eq)))
    answers["u_eq"] = me.NM(S(u_eq))
    answers["S"] = latex(S(u))
    answers["D"] = latex(D(u))
    for u0 in unidades:
        s = S(u0)#round(S(u0),2)
        d = D(u0)#round(D(u0),2)
        oferta.append([u0, s])
        demanda.append([u0, d])
        tabla.append([str(u0), "\$"+str(s), "\$"+str(d)])
    tablaHTML = html(table(tabla, frame=True))
    data["tablaHTML"] = tablaHTML
    # diseño del enunciado
    ejercicio = cabecera + """
    <p>
Considere la siguiente tabla \n
{data[tablaHTML]}
\n
<p> Calcule el precio de equilibrio: {answers[u_eq]} </p>
</p>
    """.format(data=data, answers=answers)
    retroalimentacion = """
La función de oferta es \(S(u)={answers[S]}\), 
mientras que la función de demanda es \(D(u)={answers[D]}\).
    """.format(answers=answers)
    
    if impr:
        print(html(ejercicio+retroalimentacion))
    return me.pretty(ejercicio, retroalimentacion)

np.random.seed(2)
print(html("<h1>"+label+"</h1>"))
print(html(miCabecera))
me.quick(gen, label, 0, impr=True, cabecera=miCabecera)



np.random.seed(12)
me.quick(gen, label, 5, impr=True, cabecera=miCabecera)



np.random.seed(123)
me.quick(gen, label, 200, impr=False, cabecera=miCabecera)

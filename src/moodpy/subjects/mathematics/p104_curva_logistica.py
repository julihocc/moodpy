"""
P104_curva_logistica

Migrated from legacy generator: P104_curva_logistica-checkpoint.py
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




import numpy as np
import moodpy01 as me




def gen(impr):
    x,y = var("x,y")    
    
    while True:
        U = np.random.poisson(100)
        B = np.random.poisson(9)
        a = np.random.random()
        a = np.around(a,2)/100
        if a>0 and U>a and B>0:
            u(x) = U/(1+B*exp(-U*a*x))
            break    
    
    f(x,y) = a*y*(U-y)
     
    while True:
        x0 = np.around(np.random.random(),2)
        if x0>0:
            break
    y0 = u(x0)
    
    data = {"x0":latex(x0), "y0":latex(y0)}
    
    tex = {}
    tex["ode"] = "\\frac{ dy }{ dx }="+latex(f(x,y))
    tex["ics"] = "x_0={s[x0]},y_0={s[y0]}".format(s=data)
    
    while True:
        x1 = np.around(np.random.random(),4)
        if x1>0:
            break
    y1 = u(x1).n()
    
    ans = {"x1":x1, "y1":me.NM(y1)}
    tex["sol"] = "y="+latex(u(x))
    
    ejercicio = """
    <h1> Ecuaciones diferenciales ordinarias </h1>
    <h2> Caso separable: Curva logística </h2>
    <p>
    Encuentre la solución \(y(x)\) de la siguiente ecuación diferencial separable 
    $${tex[ode]}$$ 
    con condición inicial \({tex[ics]}\). 
    </p>
    <h3> Control </h3>
    <p> Verifique su respuesta evaluando en el punto dado:</p>
    <p>
    \(y({a[x1]})=\){a[y1]}
    </p>
    """.format(tex=tex, a=ans)
    
    retroalimentacion = """
    La solución del problema de valor inicial está dada por 
    $$ {tex[sol]}. $$
    
    La gráfica de esta función se conoce como <em> curva logistica. </em>
    """.format(tex=tex)
    return me.pretty(ejercicio, retroalimentacion)

np.random.seed(1)
label = "P104_curva_logistica"
show(label)
me.quick(gen, label, 0, impr=True)



np.random.seed(12)
me.quick(gen, label, 5)



np.random.seed(123)
me.quick(gen, label, 10*12)

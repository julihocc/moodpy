"""
P102_edo_separable

Migrated from legacy generator: P103_curva_aprendizaje-checkpoint.py
Subject Area: business

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
        a,b,c = np.random.randint(-10,10,size=3)
        if a!=0 or b!=0:
            G(x) = a*x^2/2+b*x+c
            break
    u(x) = exp(G(x))
    
    f(x,y) = y*G.diff(x)
     
    x0 = np.random.randint(-10,10)   
    y0 = u(x0)
    
    data = {"x0":latex(x0), "y0":latex(y0)}
    
    tex = {}
    tex["ode"] = "\\frac{ dy }{ dx }="+latex(f(x,y))
    tex["ics"] = "x_0={s[x0]},y_0={s[y0]}".format(s=data)
    
    x1 = np.random.randint(-10,10)
    y1 = u(x1).n()
    
    ans = {"x1":x1, "y1":me.NM(y1)}
    tex["sol"] = "y="+latex(u(x))
    
    ejercicio = """
    <h1> Ecuaciones diferenciales ordinarias </h1>
    <h2> Caso separable, ejemplo 2 </h2>
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
    $$ {tex[sol]} $$.
    """.format(tex=tex)
    return me.pretty(ejercicio, retroalimentacion)

np.random.seed(1)
label = "P102_edo_separable"
show(label)
me.quick(gen, label, 0, impr=True)



me.quick(gen, label, 5)



me.quick(gen, label, 10*12)

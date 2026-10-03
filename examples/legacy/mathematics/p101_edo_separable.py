"""
P101_edo_separable

Migrated from legacy generator: P101_edo_separable-checkpoint.py
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
import moodpy as me



#prototipo
# Variables: x,y
# Note: Convert to proper symbolic math as needed
a,b,c = np.random.randint(-10,10,size=3)
g1 = lambda x,y: a*x^2+b*x+c
a,b,c = np.random.randint(-10,10,size=3)
g2 = lambda x,y: a*y^2+b*y+c
g = lambda x,y: g1(x)+g2(y)
x0,y0 = np.random.randint(-100,100,size=2)
g = lambda x,y: g(x,y)-g(x0,y0)
a = lambda x,y: g1.diff(x)
b = lambda x,y: g2.diff(y)
f = lambda x,y: -a(x,y)/b(x,y)
edo = "y'="+latex(f(x,y))
print edo
show(edo)
print g(x0,y0)
show(g(x,y))




def gen(impr):
    # Variables: x,y
# Note: Convert to proper symbolic math as needed    
    
    while True:
        a,b,c = np.random.randint(-10,10,size=3)
        if a!=0 and b!=0:
            g1 = lambda x,y: a*x^2+b*x+c
            break
    while True:
        a,b,c = np.random.randint(-10,10,size=3)
        if a!=0 or b!=0:
            g2 = lambda x,y: a*y^2+b*y+c
            break
            
    g = lambda x,y: g1(x)+g2(y)
    a = lambda x,y: g.diff(x)
    b = lambda x,y: g.diff(y)
    f = lambda x,y: -a(x,y)/b(x,y)
    
    while True:
        x0,y0 = np.random.randint(-10,10,size=2)   
        if b(x0,y0)!=0:
            break
    data = {"x0":x0, "y0":y0}
    
    g = lambda x,y: g(x,y)-g(x0,y0)
    assert g(x0,y0)==0
    
    tex = {}
    tex["ode"] = "\\frac{ dy }{ dx }="+latex(f(x,y))
    tex["ics"] = "x_0={s[x0]},y_0={s[y0]}".format(s=data)
    tex["level"] = "g = lambda x,y: 0".format(s=data)
    
    while True:
        x1,y1,x2,y2 = np.random.randint(-10,10,size=4)
        if g(x1,y1)!=0:
            break
    
    g = lambda x,y: g(x,y)/g(x1,y1)
    tex["g"] = latex(g(x,y))
    assert g(x1,y1)==1
    
    if impr: show(g(x,y))
    
    check = {}
    check["p1"] = "g({},{})".format(x1,y1)
    check["p2"] = "g({},{})".format(x2,y2)
    ans = {}    
    ans["p2"] = me.NM(g(x2,y2))
    
    ejercicio = """
    <h1> Ecuaciones diferenciales ordinarias </h1>
    <h2> Caso separable, ejemplo 1 </h2>
    <p>
    Encuentre la solución \({tex[level]}\) de la siguiente ecuación diferencial separable 
    $${tex[ode]}$$ 
    con condición inicial \({tex[ics]}\). 
    </p>
    <h3> Control </h3>
    <p> <em>Normalice</em> su respuesta de manera que \({ch[p1]}=1\). 
    Verifique su respuesta evaluando en el punto dado:</p>
    <p>
    \({ch[p2]}=\){a[p2]}
    </p>
    """.format(tex=tex, ch=check, a=ans)
    
    retroalimentacion = """
    La solución normalizada está dada por 
    $${t[g]}=0$$.
    """.format(t=tex)
    return me.pretty(ejercicio, retroalimentacion)

np.random.seed(1)
label = "P101_edo_separable"
show(label)
me.quick(gen, label, 0, impr=True)



np.random.seed(12)
me.quick(gen, label, 0, impr=True)



me.quick(gen, label, 0, impr=True)



me.quick(gen, label, 0, impr=True)



me.quick(gen, label, 5)



me.quick(gen, label, 10*12)

"""
P205_edo2_ekx

Migrated from legacy generator: P205_edo2_ekx.py
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
import moodpy02 as me




def gen(impr):
    
    tex = {}
    data = {}
    ans = {}
    
    # Variables: x
# Note: Convert to proper symbolic math as needed
    u = function("u")(x)
    b,c= np.random.randint(-2,3,size=2)    
    while True:
        A,k = np.random.randint(-10,10+1,size=2)
        if A!=0 and k!=0:
            break
    phi = lambda x: A*exp(k*x)
    ode = u.diff(x,2)(x)+b*u.diff(x)(x)+c*u(x)==phi(x)
    tex["ode"] = latex(ode)
    x1 = 1 + np.around(np.random.random(), 2)
    data["x1"] = x1
    while True:
        y0,y00 = np.random.randint(-2,3,size=2)
        if y0!=0 or y00!=0:
            break
    myics = [0,y0,y00]
    tex["y0"] = "u = lambda 0: {}".format(y0)
    tex["y00"] = "u'(0)={}".format(y00)
    f = lambda x: desolve(ode,u, ics=myics)
    if f(x)!=0:
        f = lambda x: f(x).simplify_full()
    ans["f1"] = me.NM(f(x1).n())
    
    tex["y"] = latex(f(x))
        
    ejercicio = """
    <h1> EDOs lineales de 2o Orden </h1>
    <h2> Coeficientes indeterminados: \( \\phi = lambda x: Ae^{{kx}} \) </h2>
    <p> Encuentre la solución \(u(x)\) de la siguiente ecuación diferencial
    \({tex[ode]}\) con condiciones iniciales \({tex[y0]}, \; {tex[y00]}\)
    y evalue en el punto dado:</p>
    <pre>
    u = lambda {data[x1]}: {ans[f1]}
    </pre>
    """.format(tex=tex, data=data, ans=ans)
    
    retroalimentacion = """
    La solución del problema de condiciones iniciales es
    \(u = lambda x: {tex[y]}\)
    """.format(tex=tex, data=data, ans=ans)
            
    if impr:
#         show(html(ejercicio))  # TODO: Convert HTML output for MoodPy
#         show(html(retroalimentacion))  # TODO: Convert HTML output for MoodPy
    
    return me.pretty(ejercicio, retroalimentacion)

np.random.seed(1)
label = "P205_edo2_ekx"
# show(html("<h1>"+label+"</h1>"))  # TODO: Convert HTML output for MoodPy
me.quick(gen, label, 0, impr=True)



np.random.seed(12)
me.quick(gen, label, 10, impr=True)



np.random.seed(123)
me.quick(gen, label, 15*15, impr=True)

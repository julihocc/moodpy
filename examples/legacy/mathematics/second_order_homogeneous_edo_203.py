"""
MOODPY_{}_{}_{}

Migrated from legacy generator: EDO 203 Segundo Orden (Homogéneas)-checkpoint.py
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




import moodpy as me
import numpy as np
np.random.seed(123)
# sage.misc.html._old_and_deprecated_behavior = False  # TODO: Replace Sage functionality



"""
CAMBIAR CLAVE Y TEMA!!!
"""
MATERIA = "EDO"
CLAVE = "203"
TEMA = "Ecuaciones de Segundo Orden (Homogéneas)"
label = "MOODPY_{}_{}_{}".format(MATERIA, CLAVE, TEMA.upper())
miCabecera = "<h1> {} </h1>".format(TEMA.title())
print("<h1>"+label+"</h1>")
print(miCabecera)




def get_params():
    x1 = np.random.normal(1,.25)
    while True:
        ics = np.random.normal(0,1,size=2)
        ok = not np.any(np.isclose(ics,np.zeros(2)))
        if ok:
            y0,y00 = ics
            break        
    return np.round([y0, y00, x1],2)

y0,y00,x1 = get_params()
print(y0,y00,x1)




def get_desolve(y0,y00):
    # Variables: x
# Note: Convert to proper symbolic math as needed
    u = function("y")(x)
    b,c= np.around(np.random.normal(0,10,size=2),0)
    L = u.diff(x,2)+b*u.diff(x)+c*u
    phi = lambda x: 0
    ode = L==phi(x)
    #show(ode)
    myics = [0,y0,y00]
    #print(myics)
    try:
        f = lambda x: desolve(ode,u, ics=myics)
    except:
        print("No se puede resolver")
    if f(x)!=0:
        f = lambda x: f.simplify_full().expand()
    #show(f(x))
    return ode, f

problem = get_desolve(y0,y00)
print(problem)




def tex_ode(ode):
    tex = str(latex(ode))
    #print(tex)
    first = r"\frac{\partial}{\partial x}y\left(x\right)"
    second = r"\frac{\partial^{2}}{(\partial x)^{2}}y\left(x\right)"
    tex = tex.replace(first, r"y'(x)").replace(second, r"y''(x)")
    #print(tex)
    return tex

tex = tex_ode(problem[0])
show(LatexExpr(tex))




def gen_exercise(impr=False, cabecera=""):
    data ={}
    answer = {}
    feedback = {}
    tex = {}
    
    y0,y00,x1 = get_params()
    ode, f = get_desolve(y0,y00)
        
    tex["ode"] = tex_ode(ode)
    tex["y0"] = latex(y0)
    tex["y00"] = latex(y00)
    tex["f"] = latex(f(x))
    data["x1"] = x1
    f1 = f(x1).n()
    #print("f1=",f1)
    #print(me.NM(f1))
    answer["y1"] = me.NM(f1)
    
    ejercicio = cabecera + """
    <p> Encuentre la solución \(y(x)\) de la siguiente ecuación diferencial
    \({t[ode]}\) con condiciones iniciales \(y = lambda 0: {t[y0]}, \; y'(0)={t[y00]}\)
    y evalue en el punto dado:</p>
    <pre>
    y = lambda {d[x1]}: {a[y1]}
    </pre>    
    """.format(d=data,a=answer,f=feedback,t=tex)
    
    retroalimentacion = """
      La solución del problema de condiciones iniciales es
    \(y = lambda x: {t[f]}\)  
    """.format(d=data,a=answer,f=feedback,t=tex)
    
    return me.pretty(ejercicio, retroalimentacion)

# print(html("<h1>"+label+"</h1>"))  # TODO: Convert HTML output for MoodPy
me.quick(gen_exercise, label, 0, impr=True, cabecera=miCabecera)



me.quick(gen_exercise, label, 5, impr=True, cabecera=miCabecera)



me.quick(gen_exercise, label, 500, impr=False, cabecera=miCabecera)




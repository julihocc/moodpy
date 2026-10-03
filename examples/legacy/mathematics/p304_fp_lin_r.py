"""
P304_fp_lin_r

Migrated from legacy generator: P304_fp_lin_r.py
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




import moodpy02B as me
import numpy as np



label = "P304_fp_lin_r"
forma = "" 
cabecera = """
<h1> Fracciones parciales </h1>
<h2> Factores lineales repetidos </h2>
""".format(forma)
# show(html("<h1>"+label+"</h1>"))  # TODO: Convert HTML output for MoodPy
# show(html(cabecera))  # TODO: Convert HTML output for MoodPy




def gen(impr, cabecera=""):
    
    data = {}
    ans = {}
    tex = {}
    
    # Variables: x
# Note: Convert to proper symbolic math as needed
    ### 
    
    a = np.random.randint(-10,10)

    while True:
        A = np.random.randint(-10,10, size = 3)
        if A[0]*A[1]*A[2]!=0:
            break

    F = A[0]/(x-a)+A[1]/(x-a)^2+A[2]/(x-a)^3
    F = F.factor()

    F = latex(F)
    d0 = latex(x-a)
    d1 = latex((x-a)^2)
    d2 = latex((x-a)^3)
    setting = """
    {} = \\frac{{A_0}}{{({})}}+\\frac{{A_1}}{{{}}}+\\frac{{A_2}}{{{}}}
    """.format(F, d0,d1,d2)
    
    tex["set"] = setting
    
    ans["A0"] = me.NM(A[0], entero=True)
    ans["A1"] = me.NM(A[1], entero=True)
    ans["A2"] = me.NM(A[2], entero=True)
    
    ### OUTPUT
    
    ejercicio = cabecera + """
    <p> Determine los coeficientes en el siguiente desarrollo en fracciones parciales
    $${tex[set]}$$ <p>
    <p>
    \(A_0 =\) {ans[A0]} <br>
    \(A_1 =\) {ans[A1]} <br>
    \(A_2 =\) {ans[A2]}
    </p>
    """.format(tex=tex, data=data, ans=ans)
    

    retroalimentacion = """
    Consulta "Precálculo" de J. Stewart, sección 9.8, caso 2.
    """.format(tex=tex)
    if impr:
#         show(html(ejercicio+retroalimentacion))  # TODO: Convert HTML output for MoodPy
    return me.pretty(ejercicio, retroalimentacion)

np.random.seed(1)
#show(html("<h1>"+label+"</h1>"))
#print(cabecera)
me.quick(gen, label, 0, impr=True, cabecera=cabecera)



np.random.seed(12)
me.quick(gen, label, 5, impr=True)



np.random.seed(123)
me.quick(gen, label, 500, impr=False)

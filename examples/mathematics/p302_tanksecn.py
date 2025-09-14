"""
P302_tanksecn

Migrated from legacy generator: P302_tanksecn.py
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



label = "P302_tanksecn"
forma = "\\tan^k(u) \sec^n(u)"
cabecera = """
Integrando de la forma \(f = lambda u: {}\)
""".format(forma)
# show(html("<h1>"+label+"</h1>"))  # TODO: Convert HTML output for MoodPy
# show(html(cabecera))  # TODO: Convert HTML output for MoodPy
print(cabecera)




def gen(impr, cabecera=""):
    
    data = {}
    ans = {}
    tex = {}
    
    ### Definición de antiderivada
    # Variables: x
# Note: Convert to proper symbolic math as needed
    while True:
        n = int(np.random.poisson(2))
        k = int(np.random.poisson(2))
        if n!=0 or k!=0:
            break
        
    while True:
        #a = round(2.0*pi*np.random.random(),2)
        #b = round(a + 2.0*pi*np.random.random(),2)
        #a = np.random.poisson(2)*1
        c = 1+np.random.poisson(5)
        a = -pi/(4*c)
        b = pi/(4*c)
        if impr:
            print a,b,type(a),type(b)
        if b>a and c!=0:
            break       
    
    f = lambda x: (tan(c*x))^k * (sec(c*x))^n
    print(f)
    F = lambda x: integral(f,x)
    #I = numerical_integral(f,a,b)
            
    I = (F(b)-F(a))/(b-a); I = I.n()
    
    ### grafica    
    g = Graphics()
    if impr:
        #show(u)
        show(f)
        print latex(f(x))
        show(F)
        print(f(x),a,b)
        
    if a<=b:
        if 0<=I:
            g += plot(f,(x,a,b), fill=True, fillcolor="blue", fillalpha=0.1)
        else:
            g += plot(f,(x,a,b), fill=True, fillcolor="red", fillalpha=0.1)
    else:
        if 0<=I:
            g += plot(f,(x,b,a), fill=True, fillcolor="blue", fillalpha=0.1)
        else:
            g += plot(f,(x,b,a), fill=True, fillcolor="red", fillalpha=0.1)
        
    #xx = np.linspace(a,b,1000)    
    xx = a + (b-a)*np.linspace(0,1,1000)
    m = min([f(u) for u in xx])
    M = max([f(u) for u in xx])
    g.ymin(m)
    g.ymax(M)
    g.set_aspect_ratio("automatic")
    
    if impr:
        show(g)

    filename, encoded = me.encodeGraf(g)
    im = me.tagImg(filename)    
    s = me.fileImg(filename, encoded)
    
    ### HTML
    
    tex["forma"] = forma
    data["im"] = im    
    ans["I"]=me.NM(I.n())
    tex["f"] = latex(f(x))
    tex["F"] = latex(F(x))
    
    if a<=b:
        tex["intervalo"] = "[{},{}]".format(latex(a),latex(b))
    else:
        tex["intervalo"] = "[{},{}]".format(latex(b),latex(a))    
        
    cabecera = """
    <h1> Integrales por tabla</h1>
    <h2> Integrando de la forma \(f = lambda u: {tex[forma]}\)</h2>
    """.format(tex=tex)
        
    ejercicio = cabecera + """
    <p> Encuentre el valor promedio de la función \(f = lambda x: {tex[f]}\) en el intervalo \({tex[intervalo]}\).</p>
    {data[im]}
    <pre> Valor promedio = {ans[I]} </pre>
    """.format(tex=tex, data=data, ans=ans)
    
    F = lambda x: f.integral(x)(x)
    tex["F"] = latex(F(x))
    
    retroalimentacion = """
    Una antiderivada para \({tex[f]}\) está dada por \(F = lambda x: {tex[F]}\). 
    """.format(tex=tex)
    if impr:
#         show(html(ejercicio+retroalimentacion))  # TODO: Convert HTML output for MoodPy
    return me.pretty(ejercicio, retroalimentacion, im1=s)

#np.random.seed(1)
#show(html("<h1>"+label+"</h1>"))
#print(cabecera)
me.quick(gen, label, 0, impr=True, cabecera=cabecera)



#np.random.seed(12)
#me.quick(gen, label, 5, impr=True)



#np.random.seed(123)
#me.quick(gen, label, 95, impr=False)

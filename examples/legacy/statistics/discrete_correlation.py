"""
PEP201_corr_discreta

Migrated from legacy generator: PEP201_corr_discreta.py
Subject Area: statistics

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



label = "PEP201_corr_discreta"
miCabecera = "<h1> Cálculo de estadísticos para variables aleatorias discretas </h1>"
print(html("<h1>"+label+"</h1>"))
print(html(miCabecera))




def gen(impr, cabecera=""):
    
    def htable(tab):
        return html(table(tab, frame=True))
    
    data = {}
    ans = {}
    tex = {}
    
    #x,y = var("x,y")
    
    par = 2+rnd.poisson(8)
    while True:        
        a,b,c,d,e,g = rnd.randint(par, size = 6)
        if a+b+c+d+e+g>0:
            break
    
    x,y = var("x,y")
    
    f_(x,y)= a*x**2 + b*y**2 + c*x*y + d*x + e*y + g 
    
    xmin = rnd.randint(1,2+rnd.poisson(par))
    delx = 2+rnd.poisson(par)
    xmax = xmin + delx
    xint = range(xmin, xmax+1)
    tex["xint"] = "["+str(xmin)+","+str(xmax)+"]"
    
    ymin = rnd.randint(1,2+rnd.poisson(par))
    dely = 2+rnd.poisson(par)
    ymax = ymin + dely
    yint = range(ymin, ymax+1)
    tex["yint"] = "["+str(ymin)+","+str(ymax)+"]"
        
    k = np.sum(np.array([[f_(u,v) for u in xint] for v in yint]))
    #print c,type(c)
    c = 1./k
    ans["c"] = me.NM(c)
        
    f(x,y) = f_(x,y)/k
    
    tex["fep"] = latex(f_(x,y))
    tex["f"] = latex(f(x,y))
    #show(tex["f_"])
    #print f(x,y)
    
    #print np.sum(np.array([[f(u,v) for u in xint] for v in yint]))
    
   
    def estat(g, dig = 5):
        es = np.sum(np.array([[g(u,v)*f(u,v).n() for u in xint] 
                                for v in yint]))
        return es
    
    respuestas = [["---Estadístico---", "Valor"]]
    
    mx = estat(lambda x,y:x)#; print mx
    my = estat(lambda x,y:y)#; print my
    sx = sqrt(estat(lambda x,y:(x-mx)**2))
    sy = sqrt(estat(lambda x,y:(y-my)**2))
    sxy = estat(lambda x,y: (x-mx)*(y-my))
    r = sxy/(sx*sy)
    
    midict = {0:["a","b"]}

    func = {0: ["$\mu_X$", lambda x,y: x] }
    func[1] = ["$\mu_Y$", lambda x,y:y]
    func[2] = ["$E(XY)$", lambda x,y: x*y]
    func[3] = ["$E(X^2)$", lambda x,y: x*x]
    func[4] = ["$E(Y^2)$", lambda x,y: y*y]
    func[5] = ["$\sigma^2_X", lambda x,y: (x-mx)**2]
    func[6] = ["$\sigma^2_Y", lambda x,y: (y-my)**2]
    func[7] = ["$\sigma_{XY}", lambda x,y: (x-mx)*(y-my)]
    func[8] = ["$\sigma_X", sx]
    func[9] = ["$\sigma_Y", sy]
    func[10] = ["$\\rho$", r]
    
    for k in range(8):
        respuestas.append([func[k][0], me.NM(estat(func[k][1]))])
        
    for k in [8,9,10]:
        respuestas.append([func[k][0], me.NM(func[k][1])])
        
    ans["res"] = htable(respuestas)
    
    ejercicio = cabecera + """
    <p>
    Supongamos que \(X,Y\) son variables aleatorias discretas, 
    con una función de densidad \(f(x,y)\) tal que 
    $$f(x,y)=c*({tex[fep]})$$ si
    \(x \in {tex[xint]}, y \in {tex[yint]}\) y \(0\) en cualesquiera
    otros puntos. 
    </p>
    
    <p> Calcule la contantes de normalización <br>
    \(c=\){ans[c]} </p>
    
    <p> Calcule los siguientes estadísticos
    {ans[res]} </p>
    """.format(tex=tex, data=data, ans=ans)

    retroalimentacion = """

    """.format(tex=tex)
    
    if impr:
        show(html(ejercicio+retroalimentacion))
    return me.pretty(ejercicio, retroalimentacion)

np.random.seed(2)
show(html("<h1>"+label+"</h1>"))
show(html(miCabecera))
me.quick(gen, label, 0, impr=True, cabecera=miCabecera)



np.random.seed(12)
me.quick(gen, label, 5, impr=True, cabecera=miCabecera)



np.random.seed(123)
me.quick(gen, label, 15*15, impr=False, cabecera=miCabecera)

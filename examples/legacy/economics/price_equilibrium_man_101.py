"""
MOODPY MAN 101 PRECIO DE EQUILIBRIO

Migrated from legacy generator: MOODPY MAN 101 PRECIO DE EQUILIBRIO.ipynb
Subject Area: economics

This module contains educational content generators for MoodPy v3.0.0.
"""

import moodpy as me
import numpy as np

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

label = "MOODPY MAN 101 PRECIO DE EQUILIBRIO"
miCabecera = "<h1> Precio de equilibrio </h1>"

def gen_params():
    u_eq = np.random.poisson(100)
    p_s = np.random.poisson(1000)    
    # S(u) = p_s*u - supply function
    p_eq = p_s * u_eq  # equilibrium price
    p_d = -np.random.poisson(1000)  
    # D(u) = p_eq + p_d*(u-u_eq) - demand function
    u_null = -p_eq/p_d + u_eq
    malla = np.arange(0, u_null, 1)
    n = 4
    while True:
        unidades_us = np.random.choice(malla, n, replace=False)
        if u_eq not in unidades_us:
            break
    while True:
        unidades = np.sort(unidades_us)
        if u_eq not in unidades:
            break
    return u_eq, unidades, p_s, p_eq, p_d

def supply_function(u, p_s):
    return p_s * u

def demand_function(u, u_eq, p_eq, p_d):
    return p_eq + p_d * (u - u_eq)

def gen(impr, cabecera=""):
    # Create dictionaries that feed the exercise
    data = {}
    answers = {}
    
    # Exercise design
    tabla = [["Unidades", "Precio de oferta", "Precio de Demanda"]]
    oferta = []
    demanda = []
    
    u_eq, unidades, p_s, p_eq, p_d = gen_params()
    
    # Verify equilibrium condition
    supply_eq = supply_function(u_eq, p_s)
    demand_eq = demand_function(u_eq, u_eq, p_eq, p_d)
    assert np.isclose(float(supply_eq), float(demand_eq))
    
    answers["p_eq"] = me.NM(p_eq)
    answers["u_eq"] = me.NM(u_eq, entero=True)
    
    # Build supply and demand function representations
    supply_latex = f"{p_s}u"
    demand_latex = f"{p_eq} + {p_d}(u - {u_eq})"
    answers["S"] = supply_latex
    answers["D"] = demand_latex
    
    for u0 in unidades:
        s = supply_function(u0, p_s)
        d = demand_function(u0, u_eq, p_eq, p_d)
        oferta.append([u0, s])
        demanda.append([u0, d])
        tabla.append([str(u0), f"${s:.0f}", f"${d:.0f}"])
    
    # Create HTML table
    table_rows = ""
    for row in tabla:
        if row == tabla[0]:  # Header row
            table_rows += "<tr style='background-color: #f2f2f2;'>"
            for cell in row:
                table_rows += f"<th>{cell}</th>"
            table_rows += "</tr>"
        else:
            table_rows += "<tr>"
            for cell in row:
                table_rows += f"<td>{cell}</td>"
            table_rows += "</tr>"
    
    tabla_html = f"<table border='1' cellpadding='5' cellspacing='0'>{table_rows}</table>"
    data["tablaHTML"] = tabla_html
    
    # Exercise statement design
    ejercicio = cabecera + f"""
    <p>
    Considere la siguiente tabla de precios de oferta y demanda:
    </p>
    {data["tablaHTML"]}
    <p>
    Determine el precio de equilibrio del mercado: {answers["p_eq"]}
    </p>
    <p>
    Determine las unidades de equilibrio: {answers["u_eq"]}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    La función de oferta es S(u) = {answers["S"]}, 
    mientras que la función de demanda es D(u) = {answers["D"]}.
    </p>
    <p>
    El equilibrio se encuentra donde S(u) = D(u), es decir, en el punto
    ({answers["u_eq"]}, {answers["p_eq"]}).
    </p>
    """
    
    if impr:
        print(f"<h1>{label}</h1>")
        print(miCabecera)
        print(ejercicio + retroalimentacion)
    
    return me.pretty(ejercicio, retroalimentacion)

if __name__ == "__main__":
    np.random.seed(2)
    print(f"<h1>{label}</h1>")
    print(miCabecera)
    me.quick(gen, label, 0, impr=True, cabecera=miCabecera)
    
    np.random.seed(12)
    me.quick(gen, label, 5, impr=True, cabecera=miCabecera)
    
    np.random.seed(123)
    me.quick(gen, label, 200, impr=False, cabecera=miCabecera)
"""
Discrete Correlation Analysis - PEP201

Migrated from legacy generator: PEP201_corr_discreta.ipynb
Subject Area: statistics

This module contains educational content generators for discrete variable correlation 
analysis and joint probability distribution calculations.
"""

import moodpy as me
import numpy as np
import numpy.random as rnd

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

label = "PEP201_CORR_DISCRETA"
miCabecera = "<h1> Cálculo de estadísticos para variables aleatorias discretas </h1>"

def create_html_table(data, headers=None):
    """Create HTML table from data array."""
    html = "<table border='1' cellpadding='5' cellspacing='0'>"
    
    if headers:
        html += "<tr style='background-color: #f2f2f2;'>"
        for header in headers:
            html += f"<th>{header}</th>"
        html += "</tr>"
    
    for row in data:
        html += "<tr>"
        for cell in row:
            html += f"<td>{cell}</td>"
        html += "</tr>"
    
    html += "</table>"
    return html

def gen(impr, cabecera=""):
    """Generate discrete correlation analysis problem."""
    
    data = {}
    ans = {}
    tex = {}
    
    # Generate parameters for joint probability function
    par = 2 + rnd.poisson(8)
    while True:        
        a, b, c, d, e, g = rnd.randint(-par, par+1, size=6)
        if abs(a) + abs(b) + abs(c) + abs(d) + abs(e) + abs(g) > 0:
            break
    
    # Define joint probability function f(x,y) = ax² + by² + cxy + dx + ey + g
    def f_xy(x, y):
        return a*x**2 + b*y**2 + c*x*y + d*x + e*y + g
    
    # Define domains for X and Y
    xmin = rnd.randint(1, 2 + rnd.poisson(par))
    delx = 2 + rnd.poisson(par)
    xmax = xmin + delx
    xint = list(range(xmin, xmax + 1))
    tex["xint"] = f"[{xmin}, {xmax}]"
    
    ymin = rnd.randint(1, 2 + rnd.poisson(par))
    dely = 2 + rnd.poisson(par)
    ymax = ymin + dely
    yint = list(range(ymin, ymax + 1))
    tex["yint"] = f"[{ymin}, {ymax}]"
    
    # Calculate normalization constant
    k = sum(f_xy(u, v) for u in xint for v in yint if f_xy(u, v) > 0)
    if k <= 0:
        k = 1  # Fallback to avoid division by zero
    
    c_norm = 1.0 / k
    ans["c"] = me.NM(c_norm)
    
    # Calculate marginal distributions
    px = {}  # P(X = x)
    py = {}  # P(Y = y)
    
    for x in xint:
        px[x] = sum(c_norm * max(0, f_xy(x, y)) for y in yint)
    
    for y in yint:
        py[y] = sum(c_norm * max(0, f_xy(x, y)) for x in xint)
    
    # Calculate expected values
    E_X = sum(x * px[x] for x in xint)
    E_Y = sum(y * py[y] for y in yint)
    
    ans["E_X"] = me.NM(E_X)
    ans["E_Y"] = me.NM(E_Y)
    
    # Calculate second moments
    E_X2 = sum(x**2 * px[x] for x in xint)
    E_Y2 = sum(y**2 * py[y] for y in yint)
    E_XY = sum(x * y * c_norm * max(0, f_xy(x, y)) for x in xint for y in yint)
    
    # Calculate variances
    Var_X = E_X2 - E_X**2
    Var_Y = E_Y2 - E_Y**2
    
    ans["Var_X"] = me.NM(Var_X)
    ans["Var_Y"] = me.NM(Var_Y)
    
    # Calculate covariance and correlation
    Cov_XY = E_XY - E_X * E_Y
    
    if Var_X > 0 and Var_Y > 0:
        Corr_XY = Cov_XY / (np.sqrt(Var_X) * np.sqrt(Var_Y))
    else:
        Corr_XY = 0
    
    ans["Cov_XY"] = me.NM(Cov_XY)
    ans["Corr_XY"] = me.NM(Corr_XY)
    
    # Create joint probability table
    joint_table = [["Y\\X"] + [str(x) for x in xint]]
    for y in yint:
        row = [str(y)]
        for x in xint:
            prob = c_norm * max(0, f_xy(x, y))
            row.append(f"{prob:.4f}")
        joint_table.append(row)
    
    data["joint_table"] = create_html_table(joint_table)
    
    # Store function coefficients
    tex["function"] = f"f(x,y) = {a}x² + {b}y² + {c}xy + {d}x + {e}y + {g}"
    
    ejercicio = cabecera + f"""
    <p>
    Considere las variables aleatorias discretas X e Y con función de probabilidad conjunta:
    </p>
    <p>
    {tex["function"]}
    </p>
    <p>
    donde X ∈ {tex["xint"]} y Y ∈ {tex["yint"]}.
    </p>
    <p>
    <strong>Tabla de probabilidades conjuntas:</strong>
    </p>
    {data["joint_table"]}
    <p>
    Calcule los siguientes estadísticos:
    </p>
    <p>
    Constante de normalización c: {ans["c"]} <br>
    E[X]: {ans["E_X"]} <br>
    E[Y]: {ans["E_Y"]} <br>
    Var(X): {ans["Var_X"]} <br>
    Var(Y): {ans["Var_Y"]} <br>
    Cov(X,Y): {ans["Cov_XY"]} <br>
    Corr(X,Y): {ans["Corr_XY"]}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Solución paso a paso:</strong>
    </p>
    <p>
    1. <strong>Normalización:</strong> La constante c se calcula como c = 1/Σf(x,y) = {c_norm:.6f}
    </p>
    <p>
    2. <strong>Esperanzas:</strong>
    <br>E[X] = Σx·P(X=x) = {E_X:.4f}
    <br>E[Y] = Σy·P(Y=y) = {E_Y:.4f}
    </p>
    <p>
    3. <strong>Varianzas:</strong>
    <br>Var(X) = E[X²] - (E[X])² = {Var_X:.4f}
    <br>Var(Y) = E[Y²] - (E[Y])² = {Var_Y:.4f}
    </p>
    <p>
    4. <strong>Covarianza:</strong>
    <br>Cov(X,Y) = E[XY] - E[X]E[Y] = {Cov_XY:.4f}
    </p>
    <p>
    5. <strong>Correlación:</strong>
    <br>Corr(X,Y) = Cov(X,Y)/√(Var(X)Var(Y)) = {Corr_XY:.4f}
    </p>
    """
    
    if impr:
        print(f"<h1>{label}</h1>")
        print(miCabecera)
        print(ejercicio + retroalimentacion)
        print(64*"-")
    
    return me.pretty(ejercicio, retroalimentacion)

if __name__ == "__main__":
    print(f"<h1>{label}</h1>")
    print(miCabecera)
    me.quick(gen, label, 0, impr=True, cabecera=miCabecera)
    
    me.quick(gen, label, 5, impr=True, cabecera=miCabecera)
    
    me.quick(gen, label, 50, impr=False, cabecera=miCabecera)
"""
Correlation Matrix Analysis

Migrated from legacy generator: matrizDeCorrelacion-Copy1.ipynb
Subject Area: statistics

This module contains educational content generators for correlation matrix analysis,
statistical inference, and multivariate statistical methods.
"""

import moodpy as me
import numpy as np
import numpy.random as rnd
from scipy import stats

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

label = "CORRELATION_MATRIX_ANALYSIS"
miCabecera = """
<h1> Análisis de Matriz de Correlación </h1>
<h2> Métodos Estadísticos Multivariados </h2>
"""

def correlation_coefficient(x, y):
    """Calculate Pearson correlation coefficient."""
    xm = np.mean(x)
    ym = np.mean(y)
    cxy = np.sum((x - xm) * (y - ym))
    cxx = np.sum((x - xm)**2)
    cyy = np.sum((y - ym)**2)
    
    if cxx == 0 or cyy == 0:
        return 0
    return cxy / np.sqrt(cxx * cyy)

def generate_correlated_data(n=30, correlation_target=0.5):
    """Generate correlated data with specified target correlation."""
    # Generate independent normal data
    x = np.random.normal(50, 15, n)
    noise = np.random.normal(0, 10, n)
    
    # Create correlated y variable
    y = correlation_target * (x - np.mean(x)) / np.std(x) * 12 + np.random.normal(45, 12, n) + noise * (1 - abs(correlation_target))
    
    return x, y

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
            if isinstance(cell, (int, float)):
                html += f"<td>{cell:.2f}</td>"
            else:
                html += f"<td>{cell}</td>"
        html += "</tr>"
    
    html += "</table>"
    return html

def gen(impr, cabecera=""):
    """Generate correlation matrix analysis problem."""
    
    data = {}
    ans = {}
    
    # Generate sample size
    n = 20 + rnd.poisson(15)
    
    # Generate correlation targets
    target_corr_xy = np.random.uniform(-0.8, 0.8)
    target_corr_xz = np.random.uniform(-0.6, 0.6)
    target_corr_yz = np.random.uniform(-0.7, 0.7)
    
    # Generate three correlated variables
    x = np.random.normal(50, 12, n)
    
    # Generate Y correlated with X
    y = target_corr_xy * (x - np.mean(x)) / np.std(x) * 10 + np.random.normal(45, 10, n)
    
    # Generate Z with partial correlation to both X and Y
    z = (target_corr_xz * (x - np.mean(x)) / np.std(x) * 8 + 
         target_corr_yz * (y - np.mean(y)) / np.std(y) * 8 + 
         np.random.normal(40, 8, n))
    
    # Calculate actual correlations
    corr_xy = correlation_coefficient(x, y)
    corr_xz = correlation_coefficient(x, z)  
    corr_yz = correlation_coefficient(y, z)
    
    # Store answers
    ans["n"] = me.NM(n, entero=True)
    ans["corr_xy"] = me.NM(corr_xy, error=0.001)
    ans["corr_xz"] = me.NM(corr_xz, error=0.001)
    ans["corr_yz"] = me.NM(corr_yz, error=0.001)
    
    # Calculate means and standard deviations
    mean_x, std_x = np.mean(x), np.std(x, ddof=1)
    mean_y, std_y = np.mean(y), np.std(y, ddof=1)
    mean_z, std_z = np.mean(z), np.std(z, ddof=1)
    
    ans["mean_x"] = me.NM(mean_x, error=0.01)
    ans["mean_y"] = me.NM(mean_y, error=0.01)
    ans["mean_z"] = me.NM(mean_z, error=0.01)
    ans["std_x"] = me.NM(std_x, error=0.01)
    ans["std_y"] = me.NM(std_y, error=0.01)
    ans["std_z"] = me.NM(std_z, error=0.01)
    
    # Create data table (first 10 observations)
    data_table = [["Obs", "X", "Y", "Z"]]
    for i in range(min(10, n)):
        data_table.append([i+1, f"{x[i]:.2f}", f"{y[i]:.2f}", f"{z[i]:.2f}"])
    data_table.append(["...", "...", "...", "..."])
    
    data["data_table"] = create_html_table(data_table)
    
    # Create correlation matrix
    corr_matrix = [
        ["", "X", "Y", "Z"],
        ["X", "1.000", f"{corr_xy:.3f}", f"{corr_xz:.3f}"],
        ["Y", f"{corr_xy:.3f}", "1.000", f"{corr_yz:.3f}"],
        ["Z", f"{corr_xz:.3f}", f"{corr_yz:.3f}", "1.000"]
    ]
    
    data["corr_matrix"] = create_html_table(corr_matrix)
    
    # Statistical significance tests (simplified)
    t_stat_xy = corr_xy * np.sqrt((n-2)/(1-corr_xy**2)) if abs(corr_xy) < 0.99 else 0
    t_stat_xz = corr_xz * np.sqrt((n-2)/(1-corr_xz**2)) if abs(corr_xz) < 0.99 else 0
    t_stat_yz = corr_yz * np.sqrt((n-2)/(1-corr_yz**2)) if abs(corr_yz) < 0.99 else 0
    
    ans["t_xy"] = me.NM(t_stat_xy, error=0.01)
    ans["t_xz"] = me.NM(t_stat_xz, error=0.01) 
    ans["t_yz"] = me.NM(t_stat_yz, error=0.01)
    
    ejercicio = cabecera + f"""
    <p>
    Se recolectaron datos de tres variables X, Y, Z en una muestra de {n} observaciones.
    A continuación se muestran las primeras 10 observaciones:
    </p>
    {data["data_table"]}
    <p>
    <strong>Matriz de Correlación:</strong>
    </p>
    {data["corr_matrix"]}
    <p>
    Calcule los siguientes estadísticos descriptivos:
    </p>
    <p>
    <strong>Medias:</strong><br>
    Media de X: {ans["mean_x"]} <br>
    Media de Y: {ans["mean_y"]} <br>
    Media de Z: {ans["mean_z"]}
    </p>
    <p>
    <strong>Desviaciones estándar:</strong><br>
    s_X: {ans["std_x"]} <br>
    s_Y: {ans["std_y"]} <br>
    s_Z: {ans["std_z"]}
    </p>
    <p>
    <strong>Coeficientes de correlación:</strong><br>
    r(X,Y): {ans["corr_xy"]} <br>
    r(X,Z): {ans["corr_xz"]} <br>
    r(Y,Z): {ans["corr_yz"]}
    </p>
    <p>
    <strong>Estadísticos t para prueba de significancia:</strong><br>
    t(X,Y): {ans["t_xy"]} <br>
    t(X,Z): {ans["t_xz"]} <br>
    t(Y,Z): {ans["t_yz"]}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Interpretación de resultados:</strong>
    </p>
    <p>
    1. <strong>Correlaciones:</strong>
    <br>• r(X,Y) = {corr_xy:.3f}: {"Correlación positiva" if corr_xy > 0 else "Correlación negativa"} {"fuerte" if abs(corr_xy) > 0.7 else "moderada" if abs(corr_xy) > 0.3 else "débil"}
    <br>• r(X,Z) = {corr_xz:.3f}: {"Correlación positiva" if corr_xz > 0 else "Correlación negativa"} {"fuerte" if abs(corr_xz) > 0.7 else "moderada" if abs(corr_xz) > 0.3 else "débil"}
    <br>• r(Y,Z) = {corr_yz:.3f}: {"Correlación positiva" if corr_yz > 0 else "Correlación negativa"} {"fuerte" if abs(corr_yz) > 0.7 else "moderada" if abs(corr_yz) > 0.3 else "débil"}
    </p>
    <p>
    2. <strong>Fórmula del coeficiente de correlación:</strong>
    <br>r = Σ(xi - x̄)(yi - ȳ) / √[Σ(xi - x̄)²Σ(yi - ȳ)²]
    </p>
    <p>
    3. <strong>Prueba de significancia:</strong>
    <br>Estadístico t = r√(n-2)/√(1-r²) con {n-2} grados de libertad
    <br>Para α = 0.05, valor crítico ≈ ±{stats.t.ppf(0.975, n-2):.3f}
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
    
    me.quick(gen, label, 25, impr=False, cabecera=miCabecera)
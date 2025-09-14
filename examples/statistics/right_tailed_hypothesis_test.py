"""
Right-Tailed Hypothesis Testing

Migrated from legacy generator: pruebaDeHipotesis-ColaDerecha-Copy1-checkpoint.ipynb
Subject Area: statistics

This module contains educational content generators for right-tailed hypothesis testing,
statistical inference, and z-test calculations.
"""

import moodpy as me
import numpy as np
import numpy.random as rnd
from scipy import stats

label = "RIGHT_TAILED_HYPOTHESIS_TEST"
miCabecera = """
<h1> Prueba de Hipótesis de Cola Derecha </h1>
<h2> Inferencia Estadística - Prueba Z </h2>
"""

def gen(impr, cabecera=""):
    """Generate right-tailed hypothesis test problem."""
    
    # Generate random parameters
    alpha_values = [0.01, 0.05, 0.10]
    alpha = rnd.choice(alpha_values)
    
    # Population parameters
    mu_0 = rnd.randint(20, 200)  # Null hypothesis mean
    sigma = rnd.randint(3, 25)   # Population standard deviation
    n = rnd.randint(30, 500)     # Sample size
    
    # Generate sample data with slight bias for realistic test
    bias_factor = rnd.normal(0, 0.5)  # Small random bias
    sample_mean = mu_0 + bias_factor
    
    # Calculate test statistic
    z_stat = (sample_mean - mu_0) / (sigma / np.sqrt(n))
    
    # Calculate p-value for right-tailed test
    p_value = 1 - stats.norm.cdf(z_stat)
    
    # Critical value for right-tailed test
    z_critical = stats.norm.ppf(1 - alpha)
    
    # Decision
    reject_null = p_value < alpha
    mc_answer = "{1:MC:=rechaza~acepta}" if reject_null else "{1:MC:acepta~=rechaza}"
    
    ejercicio = cabecera + f"""
    <p>
    Se desea probar la siguiente hipótesis sobre la media poblacional μ:
    </p>
    <p>
    <strong>Hipótesis nula H₀:</strong> μ = {mu_0}<br>
    <strong>Hipótesis alternativa H₁:</strong> μ > {mu_0} (cola derecha)
    </p>
    <p>
    <strong>Datos del problema:</strong><br>
    • Desviación estándar poblacional: σ = {sigma}<br>
    • Tamaño de la muestra: n = {n}<br>
    • Media muestral observada: x̄ = {sample_mean:.4f}<br>
    • Nivel de significancia: α = {alpha}
    </p>
    <p>
    Calcule los siguientes estadísticos para completar la prueba de hipótesis:
    </p>
    <p>
    <strong>1. Estadístico de prueba Z:</strong> {me.NM(z_stat, error=0.001)}
    </p>
    <p>
    <strong>2. Valor crítico Z_{alpha}:</strong> {me.NM(z_critical, error=0.001)}
    </p>
    <p>
    <strong>3. Valor p:</strong> {me.NM(p_value, error=0.0001)}
    </p>
    <p>
    <strong>4. Decisión - La hipótesis nula H₀ se:</strong> {mc_answer}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Solución paso a paso:</strong>
    </p>
    <p>
    <strong>1. Estadístico de prueba:</strong><br>
    Z = (x̄ - μ₀) / (σ/√n)<br>
    Z = ({sample_mean:.4f} - {mu_0}) / ({sigma}/√{n})<br>
    Z = {sample_mean - mu_0:.4f} / {sigma/np.sqrt(n):.4f}<br>
    Z = {z_stat:.4f}
    </p>
    <p>
    <strong>2. Valor crítico:</strong><br>
    Para α = {alpha} en prueba de cola derecha:<br>
    Z₀.₀₅ = {z_critical:.4f}
    </p>
    <p>
    <strong>3. Valor p:</strong><br>
    p = P(Z > {z_stat:.4f}) = 1 - Φ({z_stat:.4f})<br>
    p = {p_value:.4f}
    </p>
    <p>
    <strong>4. Criterios de decisión:</strong><br>
    • Criterio del valor p: {"p < α" if reject_null else "p ≥ α"} ({p_value:.4f} {"<" if reject_null else "≥"} {alpha})<br>
    • Criterio del estadístico: {"Z > Z_crítico" if z_stat > z_critical else "Z ≤ Z_crítico"} ({z_stat:.4f} {">" if z_stat > z_critical else "≤"} {z_critical:.4f})
    </p>
    <p>
    <strong>Conclusión:</strong> {"Se rechaza H₀" if reject_null else "No se rechaza H₀"}. 
    {"Hay evidencia suficiente para concluir que μ > " + str(mu_0) if reject_null else "No hay evidencia suficiente para concluir que μ > " + str(mu_0)}.
    </p>
    <p>
    <strong>Interpretación práctica:</strong><br>
    Con un nivel de confianza del {(1-alpha)*100}%, 
    {"podemos afirmar que la media poblacional es significativamente mayor que " + str(mu_0) if reject_null else "no podemos afirmar que la media poblacional sea significativamente mayor que " + str(mu_0)}.
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
"""
Two-Tailed Hypothesis Testing

Subject Area: statistics

This module contains educational content generators for two-tailed hypothesis testing,
statistical inference, and z-test calculations with bilateral critical regions.
"""

import moodpy as me
import numpy as np
import numpy.random as rnd
from scipy import stats

label = "TWO_TAILED_HYPOTHESIS_TEST"
miCabecera = """
<h1> Prueba de Hipótesis de Dos Colas </h1>
<h2> Inferencia Estadística - Prueba Z Bilateral </h2>
"""

def gen(impr, cabecera=""):
    """Generate two-tailed hypothesis test problem."""
    
    # Generate random parameters
    alpha_values = [0.01, 0.05, 0.10]
    alpha = rnd.choice(alpha_values)
    
    # Population parameters
    mu_0 = rnd.randint(20, 200)  # Null hypothesis mean
    sigma = rnd.randint(3, 25)   # Population standard deviation
    n = rnd.randint(30, 500)     # Sample size
    
    # Generate sample data with random bias (positive or negative)
    bias_factor = rnd.normal(0, 0.8)  # Random bias for two-tail test
    sample_mean = mu_0 + bias_factor
    
    # Calculate test statistic
    z_stat = (sample_mean - mu_0) / (sigma / np.sqrt(n))
    
    # Calculate p-value for two-tailed test
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # Critical values for two-tailed test
    z_critical = stats.norm.ppf(1 - alpha/2)
    
    # Decision
    reject_null = p_value < alpha
    mc_answer = "{1:MC:acepta~=rechaza}" if reject_null else "{1:MC:=acepta~rechaza}"
    
    # Determine which tail the test statistic falls in
    tail_description = "derecha" if z_stat > 0 else "izquierda"
    
    ejercicio = cabecera + f"""
    <p>
    Considere la variable aleatoria $\\bar{{X}} = \\frac{{1}}{{n}}\\sum_{{i=1}}^{{n}} X_i$ 
    donde $X_i, i=1,...,n$ son variables aleatorias idénticamente distribuidas tales que 
    $E(X_i) = \\mu$ y $Var(X_i) = \\sigma^2$.
    </p>
    <p>
    Dada la siguiente información para una prueba de hipótesis bilateral:
    </p>
    <ul>
    <li><strong>Hipótesis nula H₀:</strong> μ = {mu_0}</li>
    <li><strong>Hipótesis alternativa H₁:</strong> μ ≠ {mu_0} (dos colas)</li>
    <li><strong>Observe que la hipótesis alternativa indica diferencia en cualquier dirección</strong></li>
    <li>Desviación estándar poblacional: σ = {sigma}</li>
    <li>Tamaño de la muestra: n = {n}</li>
    <li>Valor del estimador: x̄ = {sample_mean:.4f}</li>
    <li>Nivel de significancia: α = {alpha}</li>
    </ul>
    <p>
    Encuentre los siguientes estadísticos:
    </p>
    <p>
    <strong>1. Estadístico de prueba Z:</strong> {me.NM(z_stat, error=0.001)}
    </p>
    <p>
    <strong>2. Valores críticos Z_{{α/2}}:</strong> ±{me.NM(z_critical, error=0.001)}
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
    <strong>2. Valores críticos (dos colas):</strong><br>
    Para α = {alpha} en prueba de dos colas: α/2 = {alpha/2}<br>
    Z_{{α/2}} = ±{z_critical:.4f}<br>
    Región de rechazo: Z < -{z_critical:.4f} o Z > {z_critical:.4f}
    </p>
    <p>
    <strong>3. Valor p (bilateral):</strong><br>
    p = 2 × P(Z > |{z_stat:.4f}|) = 2 × P(Z > {abs(z_stat):.4f})<br>
    p = 2 × (1 - Φ({abs(z_stat):.4f}))<br>
    p = 2 × {(1 - stats.norm.cdf(abs(z_stat))):.4f}<br>
    p = {p_value:.4f}
    </p>
    <p>
    <strong>4. Criterios de decisión:</strong><br>
    • Criterio del valor p: {"p < α" if reject_null else "p ≥ α"} ({p_value:.4f} {"<" if reject_null else "≥"} {alpha})<br>
    • Criterio del estadístico: {"|Z| > Z_crítico" if abs(z_stat) > z_critical else "|Z| ≤ Z_crítico"} (|{z_stat:.4f}| = {abs(z_stat):.4f} {">" if abs(z_stat) > z_critical else "≤"} {z_critical:.4f})
    </p>
    <p>
    <strong>Análisis del estadístico:</strong><br>
    El estadístico Z = {z_stat:.4f} cae en la cola {tail_description} de la distribución.
    {"Está en la región de rechazo" if reject_null else "No está en la región de rechazo"}.
    </p>
    <p>
    <strong>Conclusión:</strong> {"Se rechaza H₀" if reject_null else "No se rechaza H₀"}. 
    {"Hay evidencia suficiente para concluir que μ ≠ " + str(mu_0) if reject_null else "No hay evidencia suficiente para concluir que μ ≠ " + str(mu_0)}.
    </p>
    <p>
    <strong>Interpretación práctica:</strong><br>
    Con un nivel de confianza del {(1-alpha)*100}%, 
    {"podemos afirmar que la media poblacional es significativamente diferente de " + str(mu_0) if reject_null else "no podemos afirmar que la media poblacional sea significativamente diferente de " + str(mu_0)}.
    </p>
    <p>
    <strong>Características de la prueba bilateral:</strong><br>
    • Se divide α entre las dos colas: α/2 = {alpha/2} en cada cola<br>
    • El valor p se calcula como el doble del área en la cola más extrema<br>
    • Detectamos diferencias en cualquier dirección (mayor o menor que μ₀)<br>
    • Es más conservadora que las pruebas de una cola para el mismo α
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
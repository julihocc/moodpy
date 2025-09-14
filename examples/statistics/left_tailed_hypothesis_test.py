"""
Left-Tailed Hypothesis Testing

Migrated from legacy generator: Valores-p (prueba de cola izquierda)-Copy1-checkpoint.ipynb
Subject Area: statistics

This module contains educational content generators for left-tailed hypothesis testing,
statistical inference, and z-test calculations with left-tail critical regions.
"""

import moodpy as me
import numpy as np
import numpy.random as rnd
from scipy import stats

label = "LEFT_TAILED_HYPOTHESIS_TEST"
miCabecera = """
<h1> Prueba de Hipótesis de Cola Izquierda </h1>
<h2> Inferencia Estadística - Prueba Z </h2>
"""

def gen(impr, cabecera=""):
    """Generate left-tailed hypothesis test problem."""
    
    # Generate random parameters
    alpha_values = [0.01, 0.05, 0.10]
    alpha = rnd.choice(alpha_values)
    
    # Population parameters
    mu_0 = rnd.randint(20, 200)  # Null hypothesis mean
    sigma = rnd.randint(3, 25)   # Population standard deviation
    n = rnd.poisson(40) + 20     # Sample size (ensure minimum 20)
    
    # Generate sample data with slight negative bias for realistic left-tail test
    bias_factor = rnd.normal(-0.5, 0.5)  # Negative bias for left-tail
    sample_mean = mu_0 + bias_factor
    
    # Calculate test statistic
    z_stat = (sample_mean - mu_0) / (sigma / np.sqrt(n))
    
    # Calculate p-value for left-tailed test
    p_value = stats.norm.cdf(z_stat)
    
    # Critical value for left-tailed test
    z_critical = stats.norm.ppf(alpha)
    
    # Decision
    reject_null = p_value < alpha
    mc_answer = "{1:MC:acepta~=rechaza}" if reject_null else "{1:MC:=acepta~rechaza}"
    
    ejercicio = cabecera + f"""
    <p>
    Considere la variable aleatoria $\\bar{{X}} = \\frac{{1}}{{n}}\\sum_{{i=1}}^{{n}} X_i$ 
    donde $X_i, i=1,...,n$ son variables aleatorias idénticamente distribuidas tales que 
    $E(X_i) = \\mu$ y $Var(X_i) = \\sigma^2$.
    </p>
    <p>
    Dada la siguiente información para una prueba de hipótesis:
    </p>
    <ul>
    <li><strong>Hipótesis nula H₀:</strong> μ = {mu_0}</li>
    <li><strong>Hipótesis alternativa H₁:</strong> μ < {mu_0} (cola izquierda)</li>
    <li><strong>Observe que la desigualdad en la hipótesis alternativa indica cola izquierda</strong></li>
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
    <strong>2. Valor crítico Z_α:</strong> {me.NM(z_critical, error=0.001)}
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
    <strong>2. Valor crítico (cola izquierda):</strong><br>
    Para α = {alpha} en prueba de cola izquierda:<br>
    Z_α = {z_critical:.4f} (valor negativo porque es cola izquierda)
    </p>
    <p>
    <strong>3. Valor p:</strong><br>
    p = P(Z < {z_stat:.4f}) = Φ({z_stat:.4f})<br>
    p = {p_value:.4f}
    </p>
    <p>
    <strong>4. Criterios de decisión:</strong><br>
    • Criterio del valor p: {"p < α" if reject_null else "p ≥ α"} ({p_value:.4f} {"<" if reject_null else "≥"} {alpha})<br>
    • Criterio del estadístico: {"Z < Z_crítico" if z_stat < z_critical else "Z ≥ Z_crítico"} ({z_stat:.4f} {"<" if z_stat < z_critical else "≥"} {z_critical:.4f})
    </p>
    <p>
    <strong>Región de rechazo:</strong><br>
    En una prueba de cola izquierda, rechazamos H₀ si Z < Z_α = {z_critical:.4f}
    </p>
    <p>
    <strong>Conclusión:</strong> {"Se rechaza H₀" if reject_null else "No se rechaza H₀"}. 
    {"Hay evidencia suficiente para concluir que μ < " + str(mu_0) if reject_null else "No hay evidencia suficiente para concluir que μ < " + str(mu_0)}.
    </p>
    <p>
    <strong>Interpretación práctica:</strong><br>
    Con un nivel de confianza del {(1-alpha)*100}%, 
    {"podemos afirmar que la media poblacional es significativamente menor que " + str(mu_0) if reject_null else "no podemos afirmar que la media poblacional sea significativamente menor que " + str(mu_0)}.
    </p>
    <p>
    <strong>Nota importante:</strong><br>
    En las pruebas de cola izquierda, buscamos evidencia de que el parámetro es <em>menor</em> 
    que el valor especificado en H₀. El valor p representa la probabilidad de observar 
    un estadístico de prueba igual o menor al calculado, asumiendo que H₀ es verdadera.
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
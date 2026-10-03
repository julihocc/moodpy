"""
P-Value Calculation and Interpretation

Subject Area: statistics

This module contains educational content generators for p-value calculations,
statistical significance interpretation, and hypothesis testing decision making.
"""

import moodpy as me
import numpy.random as rnd
from scipy import stats

label = "P_VALUE_ANALYSIS"
miCabecera = """
<h1> Análisis de Valores P </h1>
<h2> Interpretación de Significancia Estadística </h2>
"""

def gen(impr, cabecera=""):
    """Generate p-value analysis problem."""
    
    # Generate random parameters
    alpha_values = [0.01, 0.05, 0.10]
    alpha = rnd.choice(alpha_values)
    
    # Choose test type
    test_types = ['right', 'left', 'two']
    test_type = rnd.choice(test_types)
    
    # Population parameters
    mu_0 = rnd.randint(20, 150)
    n = rnd.randint(25, 200)
    
    # Generate realistic z-statistic based on test type
    if test_type == 'right':
        z_stat = rnd.normal(1.2, 1.5)  # Bias toward positive values
        alt_hypothesis = f"μ > {mu_0}"
        p_calculation = "P(Z > z)"
        p_value = 1 - stats.norm.cdf(z_stat)
    elif test_type == 'left':
        z_stat = rnd.normal(-1.2, 1.5)  # Bias toward negative values  
        alt_hypothesis = f"μ < {mu_0}"
        p_calculation = "P(Z < z)"
        p_value = stats.norm.cdf(z_stat)
    else:  # two-tailed
        z_stat = rnd.normal(0, 2.0)  # Centered around 0
        alt_hypothesis = f"μ ≠ {mu_0}"
        p_calculation = "2 × P(Z > |z|)"
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # Ensure realistic p-values
    p_value = max(0.0001, min(0.9999, p_value))
    

    
    # Decision
    reject_null = p_value < alpha
    decision_text = "rechaza" if reject_null else "acepta"
    
    # Effect size interpretation
    if abs(z_stat) < 0.5:
        effect_size = "muy pequeño"
    elif abs(z_stat) < 1.0:
        effect_size = "pequeño"
    elif abs(z_stat) < 2.0:
        effect_size = "moderado"
    else:
        effect_size = "grande"
    
    # Significance interpretation
    if p_value < 0.001:
        significance_level = "altamente significativo"
    elif p_value < 0.01:
        significance_level = "muy significativo"
    elif p_value < 0.05:
        significance_level = "significativo"
    elif p_value < 0.10:
        significance_level = "marginalmente significativo"
    else:
        significance_level = "no significativo"
    
    test_type_spanish = {
        'right': 'cola derecha',
        'left': 'cola izquierda', 
        'two': 'dos colas'
    }[test_type]
    
    ejercicio = cabecera + f"""
    <p>
    Un investigador realizó una prueba de hipótesis sobre la media poblacional μ y obtuvo 
    los siguientes resultados:
    </p>
    <ul>
    <li><strong>Hipótesis nula H₀:</strong> μ = {mu_0}</li>
    <li><strong>Hipótesis alternativa H₁:</strong> {alt_hypothesis}</li>
    <li><strong>Tipo de prueba:</strong> {test_type_spanish}</li>
    <li>Estadístico de prueba: Z = {z_stat:.4f}</li>
    <li>Tamaño de muestra: n = {n}</li>
    <li>Nivel de significancia: α = {alpha}</li>
    </ul>
    <p>
    Analice los siguientes aspectos:
    </p>
    <p>
    <strong>1. Valor p:</strong> {me.NM(p_value, error=0.0001)}
    </p>
    <p>
    <strong>2. Conclusión estadística:</strong> 
    Con α = {alpha}, la hipótesis nula se {me.MC(decision_text + "~" + ("acepta" if decision_text == "rechaza" else "rechaza"), correct=decision_text)}
    </p>
    <p>
    <strong>3. Nivel de significancia observado:</strong> {me.MC(significance_level + "~moderadamente significativo~no significativo", correct=significance_level)}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Análisis completo del valor p:</strong>
    </p>
    <p>
    <strong>1. Cálculo del valor p:</strong><br>
    Para una prueba de {test_type_spanish}:<br>
    p = {p_calculation} = {p_value:.4f}
    </p>
    <p>
    <strong>2. Interpretación del valor p:</strong><br>
    El valor p = {p_value:.4f} representa la probabilidad de obtener un estadístico 
    de prueba igual o más extremo que Z = {z_stat:.4f}, asumiendo que H₀ es verdadera.
    </p>
    <p>
    <strong>3. Comparación con α:</strong><br>
    • Valor p = {p_value:.4f}<br>
    • Nivel de significancia α = {alpha}<br>
    • Resultado: p {"<" if p_value < alpha else "≥"} α, por lo tanto {"rechazamos" if reject_null else "no rechazamos"} H₀
    </p>
    <p>
    <strong>4. Niveles de significancia:</strong><br>
    • p < 0.001: Altamente significativo (***)<br>
    • p < 0.01: Muy significativo (**)<br>
    • p < 0.05: Significativo (*)<br>
    • p < 0.10: Marginalmente significativo (.)<br>
    • p ≥ 0.10: No significativo
    </p>
    <p>
    <strong>5. Interpretación práctica:</strong><br>
    Este resultado es <strong>{significance_level}</strong>. 
    {"Hay evidencia estadística suficiente para concluir que la media poblacional es significativamente diferente del valor hipotético." if reject_null else "No hay evidencia estadística suficiente para concluir que la media poblacional sea diferente del valor hipotético."}
    </p>
    <p>
    <strong>6. Tamaño del efecto:</strong><br>
    Con Z = {z_stat:.4f}, el tamaño del efecto es <strong>{effect_size}</strong>.
    {"Esto indica una diferencia prácticamente importante además de estadísticamente significativa." if abs(z_stat) > 1.5 and reject_null else "La significancia estadística no implica necesariamente importancia práctica." if reject_null else ""}
    </p>
    <p>
    <strong>7. Consideraciones importantes:</strong><br>
    • Un valor p pequeño NO mide la magnitud del efecto<br>
    • La significancia estadística depende del tamaño de muestra<br>
    • Siempre considere el contexto práctico junto con la significancia estadística<br>
    • Un resultado no significativo no "prueba" que H₀ sea verdadera
    </p>
    <p>
    <strong>8. Reporte de resultados:</strong><br>
    "Con un tamaño de muestra de n = {n}, se encontró que Z = {z_stat:.4f}, 
    p = {p_value:.4f}. {"Este resultado es estadísticamente significativo" if reject_null else "Este resultado no es estadísticamente significativo"} 
    al nivel α = {alpha}."
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
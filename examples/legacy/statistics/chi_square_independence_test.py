"""
Chi-Square Test of Independence

Migrated from legacy generator: generoVsMaterias.ipynb
Subject Area: statistics

This module contains educational content generators for chi-square tests of independence,
contingency table analysis, and categorical data analysis.
"""

import moodpy as me
import numpy as np
import numpy.random as rnd
from scipy import stats

label = "CHI_SQUARE_INDEPENDENCE_TEST"
miCabecera = """
<h1> Prueba Chi-Cuadrado de Independencia </h1>
<h2> Análisis de Tablas de Contingencia </h2>
"""

def create_contingency_table(observed, row_labels, col_labels, title="Tabla de Contingencia"):
    """Create HTML contingency table."""
    html = f"<p><strong>{title}</strong></p>"
    html += "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse;'>"
    
    # Header row
    html += "<tr style='background-color: #f2f2f2;'>"
    html += "<th></th>"
    for col_label in col_labels:
        html += f"<th>{col_label}</th>"
    html += "<th><strong>Total</strong></th>"
    html += "</tr>"
    
    # Data rows
    row_totals = np.sum(observed, axis=1)
    for i, row_label in enumerate(row_labels):
        html += "<tr>"
        html += f"<th style='background-color: #f2f2f2;'>{row_label}</th>"
        for j in range(len(col_labels)):
            html += f"<td style='text-align: center;'>{int(observed[i][j])}</td>"
        html += f"<td style='text-align: center; font-weight: bold;'>{int(row_totals[i])}</td>"
        html += "</tr>"
    
    # Total row
    col_totals = np.sum(observed, axis=0)
    grand_total = np.sum(observed)
    html += "<tr style='background-color: #f2f2f2; font-weight: bold;'>"
    html += "<th>Total</th>"
    for total in col_totals:
        html += f"<td style='text-align: center;'>{int(total)}</td>"
    html += f"<td style='text-align: center;'>{int(grand_total)}</td>"
    html += "</tr>"
    
    html += "</table>"
    return html

def calculate_expected_frequencies(observed):
    """Calculate expected frequencies for chi-square test."""
    row_totals = np.sum(observed, axis=1)
    col_totals = np.sum(observed, axis=0)
    grand_total = np.sum(observed)
    
    expected = np.zeros_like(observed, dtype=float)
    for i in range(observed.shape[0]):
        for j in range(observed.shape[1]):
            expected[i][j] = (row_totals[i] * col_totals[j]) / grand_total
    
    return expected

def gen(impr, cabecera=""):
    """Generate chi-square test of independence problem."""
    
    # Generate random significance level
    alpha_values = [0.01, 0.05, 0.10]
    alpha = rnd.choice(alpha_values)
    
    # Generate contingency table with realistic educational context
    # Using Poisson distribution to ensure positive integers
    observed = rnd.poisson(25, size=(2, 3)).astype(float)
    
    # Ensure minimum expected frequency > 5 for chi-square validity
    while np.min(observed) < 5:
        observed = rnd.poisson(25, size=(2, 3)).astype(float)
    
    # Calculate expected frequencies
    expected = calculate_expected_frequencies(observed)
    
    # Calculate chi-square statistic
    chi_square = np.sum((observed - expected)**2 / expected)
    
    # Degrees of freedom
    df = (observed.shape[0] - 1) * (observed.shape[1] - 1)
    
    # Calculate p-value
    p_value = 1 - stats.chi2.cdf(chi_square, df)
    
    # Critical value
    chi_critical = stats.chi2.ppf(1 - alpha, df)
    
    # Decision
    reject_null = p_value < alpha
    mc_answer = "{1:MC:acepta~=rechaza}" if reject_null else "{1:MC:=acepta~rechaza}"
    
    # Labels for the table
    row_labels = ["Hombres", "Mujeres"]
    col_labels = ["Matemáticas", "Artes", "Comercio"]
    
    # Create tables
    observed_table = create_contingency_table(observed, row_labels, col_labels, "Frecuencias Observadas")
    expected_table = create_contingency_table(expected, row_labels, col_labels, "Frecuencias Esperadas")
    
    ejercicio = cabecera + f"""
    <p>
    Un investigador desea determinar si existe relación entre el género de los estudiantes 
    y su elección de materia principal. Se recolectaron los siguientes datos de una muestra 
    de estudiantes universitarios:
    </p>
    {observed_table}
    <p>
    <strong>Hipótesis:</strong><br>
    • H₀: La elección de materia es independiente del género<br>
    • H₁: La elección de materia NO es independiente del género
    </p>
    <p>
    Con un nivel de significancia α = {alpha}, determine:
    </p>
    <p>
    <strong>1. Estadístico chi-cuadrado:</strong> {me.NM(chi_square, error=0.001)}
    </p>
    <p>
    <strong>2. Grados de libertad:</strong> {me.NM(df, entero=True)}
    </p>
    <p>
    <strong>3. Valor crítico χ²₀.₀₅:</strong> {me.NM(chi_critical, error=0.001)}
    </p>
    <p>
    <strong>4. Valor p:</strong> {me.NM(p_value, error=0.0001)}
    </p>
    <p>
    <strong>5. Decisión - La hipótesis nula H₀ se:</strong> {mc_answer}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Solución paso a paso:</strong>
    </p>
    <p>
    <strong>1. Frecuencias esperadas:</strong><br>
    Bajo la hipótesis de independencia: E(i,j) = (Total fila i × Total columna j) / Total general
    </p>
    {expected_table}
    <p>
    <strong>2. Estadístico chi-cuadrado:</strong><br>
    χ² = Σ[(Observado - Esperado)² / Esperado]<br>
    χ² = {chi_square:.4f}
    </p>
    <p>
    <strong>Cálculo detallado:</strong><br>
    """
    
    # Add detailed calculation
    for i in range(2):
        for j in range(3):
            contrib = (observed[i,j] - expected[i,j])**2 / expected[i,j]
            retroalimentacion += f"• Celda ({row_labels[i]}, {col_labels[j]}): ({observed[i,j]:.0f} - {expected[i,j]:.2f})² / {expected[i,j]:.2f} = {contrib:.4f}<br>"
    
    retroalimentacion += f"""
    </p>
    <p>
    <strong>3. Grados de libertad:</strong><br>
    df = (filas - 1) × (columnas - 1) = (2 - 1) × (3 - 1) = {df}
    </p>
    <p>
    <strong>4. Valor crítico:</strong><br>
    Para α = {alpha} y df = {df}: χ²crítico = {chi_critical:.4f}
    </p>
    <p>
    <strong>5. Valor p:</strong><br>
    p = P(χ² > {chi_square:.4f}) = {p_value:.4f}
    </p>
    <p>
    <strong>6. Criterios de decisión:</strong><br>
    • Criterio del valor p: {"p < α" if reject_null else "p ≥ α"} ({p_value:.4f} {"<" if reject_null else "≥"} {alpha})<br>
    • Criterio del estadístico: {"χ² > χ²crítico" if chi_square > chi_critical else "χ² ≤ χ²crítico"} ({chi_square:.4f} {">" if chi_square > chi_critical else "≤"} {chi_critical:.4f})
    </p>
    <p>
    <strong>Conclusión:</strong> {"Se rechaza H₀" if reject_null else "No se rechaza H₀"}. 
    {"Existe evidencia suficiente para concluir que la elección de materia SÍ depende del género" if reject_null else "No hay evidencia suficiente para concluir que la elección de materia dependa del género"}.
    </p>
    <p>
    <strong>Interpretación práctica:</strong><br>
    Con un nivel de confianza del {(1-alpha)*100}%, 
    {"podemos afirmar que existe una asociación significativa entre el género y la elección de materia principal" if reject_null else "no podemos afirmar que exista una asociación significativa entre el género y la elección de materia principal"}.
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
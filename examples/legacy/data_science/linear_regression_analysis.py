"""
Linear Regression Analysis and Least Squares Optimization

Subject Area: data_science

This module contains educational content generators for linear regression analysis,
least squares optimization, and parameter estimation in data science applications.
"""

import moodpy as me
import numpy.random as rnd
import numpy as np

label = "LINEAR_REGRESSION_ANALYSIS"
miCabecera = """
<h1> Análisis de Regresión Lineal </h1>
<h2> Optimización por Mínimos Cuadrados </h2>
"""

def generate_regression_data(n=30):
    """Generate regression data with known parameters."""
    # True parameters
    true_alpha = rnd.randint(-50, 50)  # True intercept
    true_beta = rnd.uniform(-3, 3)     # True slope
    
    # Generate x values
    x_mean = rnd.randint(-20, 20)
    x_std = rnd.randint(8, 15)
    x = rnd.normal(x_mean, x_std, n)
    
    # Generate noise
    noise_std = rnd.randint(5, 12)
    noise = rnd.normal(0, noise_std, n)
    
    # Generate y values with linear relationship plus noise
    y = true_alpha + true_beta * x + noise
    
    return x, y, true_alpha, true_beta, x_mean, x_std, noise_std

def calculate_regression_coefficients(x, y):
    """Calculate least squares regression coefficients."""
    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    # Calculate beta (slope) using least squares formula
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean)**2)
    beta = numerator / denominator
    
    # Calculate alpha (intercept)
    alpha = y_mean - beta * x_mean
    
    return alpha, beta, x_mean, y_mean, numerator, denominator

def calculate_regression_statistics(x, y, alpha, beta):
    """Calculate regression statistics."""
    n = len(x)
    y_pred = alpha + beta * x
    
    # Sum of squares
    ss_total = np.sum((y - np.mean(y))**2)
    ss_residual = np.sum((y - y_pred)**2)
    ss_regression = ss_total - ss_residual
    
    # R-squared
    r_squared = ss_regression / ss_total if ss_total > 0 else 0
    
    # Correlation coefficient
    correlation = np.sqrt(r_squared) if beta > 0 else -np.sqrt(r_squared)
    
    # Standard error of regression
    mse = ss_residual / (n - 2) if n > 2 else 0
    std_error = np.sqrt(mse)
    
    return r_squared, correlation, ss_total, ss_residual, ss_regression, std_error

def gen(impr, cabecera=""):
    """Generate linear regression analysis problem."""
    
    # Choose problem type
    problem_types = ['basic_regression', 'optimization_theory', 'model_evaluation', 'prediction_analysis']
    problem_type = rnd.choice(problem_types)
    
    if problem_type == 'basic_regression':
        # Generate regression data
        n = rnd.randint(25, 35)
        x, y, true_alpha, true_beta, x_mean_pop, x_std_pop, noise_std = generate_regression_data(n)
        
        # Calculate regression coefficients
        alpha, beta, x_mean, y_mean, numerator, denominator = calculate_regression_coefficients(x, y)
        
        # Calculate statistics
        r_squared, correlation, ss_total, ss_residual, ss_regression, std_error = calculate_regression_statistics(x, y, alpha, beta)
        
        ejercicio = cabecera + f"""
        <p>
        Se recolectaron {n} puntos de datos para analizar la relación entre las variables X e Y.
        Los datos muestran la siguiente información estadística:
        </p>
        <p>
        <strong>Estadísticas descriptivas:</strong><br>
        • Media de X: $\\bar{{x}} = {x_mean:.3f}$<br>
        • Media de Y: $\\bar{{y}} = {y_mean:.3f}$<br>
        • Tamaño de muestra: $n = {n}$
        </p>
        <p>
        <strong>Cálculos para regresión lineal:</strong><br>
        • $\\sum(x_i - \\bar{{x}})(y_i - \\bar{{y}}) = {numerator:.3f}$<br>
        • $\\sum(x_i - \\bar{{x}})^2 = {denominator:.3f}$
        </p>
        <p>
        Calcule los parámetros de la regresión lineal $y = \\alpha + \\beta x$:
        </p>
        <p>
        <strong>1. Coeficiente de pendiente (β):</strong> $\\beta = $ {me.NM(beta, error=0.001)}
        </p>
        <p>
        <strong>2. Intercepto (α):</strong> $\\alpha = $ {me.NM(alpha, error=0.001)}
        </p>
        <p>
        <strong>3. Coeficiente de determinación:</strong> $R^2 = $ {me.NM(r_squared, error=0.001)}
        </p>
        <p>
        <strong>4. Coeficiente de correlación:</strong> $r = $ {me.NM(correlation, error=0.001)}
        </p>
        <p>
        <strong>5. Error estándar de la regresión:</strong> $s_e = $ {me.NM(std_error, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución paso a paso - Método de Mínimos Cuadrados:</strong>
        </p>
        <p>
        <strong>1. Fórmula del coeficiente de pendiente:</strong><br>
        $\\beta = \\frac{{\\sum(x_i - \\bar{{x}})(y_i - \\bar{{y}})}}{{\\sum(x_i - \\bar{{x}})^2}}$<br>
        $\\beta = \\frac{{{numerator:.3f}}}{{{denominator:.3f}}} = {beta:.6f}$
        </p>
        <p>
        <strong>2. Fórmula del intercepto:</strong><br>
        $\\alpha = \\bar{{y}} - \\beta\\bar{{x}}$<br>
        $\\alpha = {y_mean:.3f} - ({beta:.6f})({x_mean:.3f})$<br>
        $\\alpha = {y_mean:.3f} - {beta*x_mean:.3f} = {alpha:.6f}$
        </p>
        <p>
        <strong>3. Ecuación de regresión:</strong><br>
        $y = {alpha:.3f} + {beta:.3f}x$
        </p>
        <p>
        <strong>4. Análisis de bondad de ajuste:</strong><br>
        Suma de cuadrados total: $SS_{{total}} = {ss_total:.3f}$<br>
        Suma de cuadrados residual: $SS_{{residual}} = {ss_residual:.3f}$<br>
        Suma de cuadrados de regresión: $SS_{{regression}} = {ss_regression:.3f}$<br>
        $R^2 = \\frac{{SS_{{regression}}}}{{SS_{{total}}}} = \\frac{{{ss_regression:.3f}}}{{{ss_total:.3f}}} = {r_squared:.6f}$
        </p>
        <p>
        <strong>5. Interpretación estadística:</strong><br>
        • El modelo explica el {r_squared*100:.1f}% de la variabilidad en Y<br>
        • La correlación es {'positiva' if correlation > 0 else 'negativa'} con magnitud {abs(correlation):.3f}<br>
        • El error estándar de {std_error:.3f} indica la precisión típica de las predicciones
        </p>
        <p>
        <strong>Aplicaciones en Data Science:</strong><br>
        La regresión lineal es fundamental para modelado predictivo, análisis de tendencias,
        y comprensión de relaciones entre variables en datasets complejos.
        </p>
        """
    
    elif problem_type == 'optimization_theory':
        # Focus on the optimization aspect of least squares
        n = rnd.randint(20, 30)
        x, y, true_alpha, true_beta, x_mean_pop, x_std_pop, noise_std = generate_regression_data(n)
        
        # Calculate regression coefficients
        alpha, beta, x_mean, y_mean, numerator, denominator = calculate_regression_coefficients(x, y)
        
        # Calculate derivatives for optimization
        sum_x = np.sum(x)
        sum_y = np.sum(y)
        sum_xy = np.sum(x * y)
        sum_x2 = np.sum(x**2)
        
        # Normal equations coefficients
        determinant = n * sum_x2 - sum_x**2
        
        ejercicio = cabecera + f"""
        <p>
        En el problema de regresión lineal, buscamos minimizar la función de costo:
        </p>
        <p>
        $J(\\alpha, \\beta) = \\frac{{1}}{{2n}} \\sum_{{i=1}}^n (y_i - \\alpha - \\beta x_i)^2$
        </p>
        <p>
        Con los siguientes datos de {n} observaciones:
        </p>
        <p>
        • $\\sum x_i = {sum_x:.3f}$<br>
        • $\\sum y_i = {sum_y:.3f}$<br>
        • $\\sum x_i y_i = {sum_xy:.3f}$<br>
        • $\\sum x_i^2 = {sum_x2:.3f}$
        </p>
        <p>
        Resuelva el sistema de ecuaciones normales para encontrar los parámetros óptimos:
        </p>
        <p>
        <strong>1. Determinante del sistema:</strong> $\\Delta = $ {me.NM(determinant, error=0.001)}
        </p>
        <p>
        <strong>2. Parámetro α óptimo:</strong> $\\alpha^* = $ {me.NM(alpha, error=0.001)}
        </p>
        <p>
        <strong>3. Parámetro β óptimo:</strong> $\\beta^* = $ {me.NM(beta, error=0.001)}
        </p>
        <p>
        <strong>4. Valor mínimo de la función de costo:</strong> $J_{min} = $ {me.NM(np.sum((y - alpha - beta*x)**2)/(2*n), error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Teoría de Optimización - Método de Mínimos Cuadrados:</strong>
        </p>
        <p>
        <strong>1. Derivadas parciales de la función de costo:</strong><br>
        $\\frac{{\\partial J}}{{\\partial \\alpha}} = -\\frac{{1}}{{n}} \\sum_{{i=1}}^n (y_i - \\alpha - \\beta x_i) = 0$<br>
        $\\frac{{\\partial J}}{{\\partial \\beta}} = -\\frac{{1}}{{n}} \\sum_{{i=1}}^n x_i(y_i - \\alpha - \\beta x_i) = 0$
        </p>
        <p>
        <strong>2. Sistema de ecuaciones normales:</strong><br>
        $n\\alpha + \\beta\\sum x_i = \\sum y_i$<br>
        $\\alpha\\sum x_i + \\beta\\sum x_i^2 = \\sum x_i y_i$<br><br>
        En forma matricial:<br>
        $\\begin{{pmatrix}} {n} & {sum_x:.1f} \\\\ {sum_x:.1f} & {sum_x2:.1f} \\end{{pmatrix}} \\begin{{pmatrix}} \\alpha \\\\ \\beta \\end{{pmatrix}} = \\begin{{pmatrix}} {sum_y:.1f} \\\\ {sum_xy:.1f} \\end{{pmatrix}}$
        </p>
        <p>
        <strong>3. Solución por regla de Cramer:</strong><br>
        Determinante: $\\Delta = {n} \\times {sum_x2:.1f} - {sum_x:.1f}^2 = {determinant:.3f}$<br>
        $\\alpha^* = \\frac{{{sum_y:.1f} \\times {sum_x2:.1f} - {sum_x:.1f} \\times {sum_xy:.1f}}}{{{determinant:.3f}}} = {alpha:.6f}$<br>
        $\\beta^* = \\frac{{{n} \\times {sum_xy:.1f} - {sum_x:.1f} \\times {sum_y:.1f}}}{{{determinant:.3f}}} = {beta:.6f}$
        </p>
        <p>
        <strong>4. Verificación de condición de segundo orden:</strong><br>
        La matriz Hessiana es positiva definida:<br>
        $H = \\begin{{pmatrix}} n & \\sum x_i \\\\ \\sum x_i & \\sum x_i^2 \\end{{pmatrix}}$<br>
        $\\det(H) = {determinant:.3f} > 0$ y $n = {n} > 0$, confirmando un mínimo global.
        </p>
        <p>
        <strong>Principios de optimización:</strong><br>
        • Condición de primer orden: gradiente igual a cero<br>
        • Condición de segundo orden: Hessiana positiva definida<br>
        • Solución única garantizada por convexidad de la función objetivo
        </p>
        """
    
    elif problem_type == 'model_evaluation':
        # Focus on model evaluation and diagnostics
        n = rnd.randint(25, 35)
        x, y, true_alpha, true_beta, x_mean_pop, x_std_pop, noise_std = generate_regression_data(n)
        
        # Calculate regression coefficients and statistics
        alpha, beta, x_mean, y_mean, numerator, denominator = calculate_regression_coefficients(x, y)
        r_squared, correlation, ss_total, ss_residual, ss_regression, std_error = calculate_regression_statistics(x, y, alpha, beta)
        
        # Additional evaluation metrics
        y_pred = alpha + beta * x
        residuals = y - y_pred
        mean_absolute_error = np.mean(np.abs(residuals))
        root_mean_square_error = np.sqrt(np.mean(residuals**2))
        
        # F-statistic for overall model significance
        f_statistic = (ss_regression / 1) / (ss_residual / (n - 2)) if n > 2 else 0
        
        # Standard errors of coefficients
        s_xx = np.sum((x - x_mean)**2)
        se_beta = std_error / np.sqrt(s_xx) if s_xx > 0 else 0
        se_alpha = std_error * np.sqrt(1/n + x_mean**2/s_xx) if s_xx > 0 else 0
        
        ejercicio = cabecera + f"""
        <p>
        Se ajustó un modelo de regresión lineal con {n} observaciones.
        Los resultados del ajuste son:
        </p>
        <p>
        <strong>Modelo estimado:</strong> $\\hat{{y}} = {alpha:.3f} + {beta:.3f}x$
        </p>
        <p>
        <strong>Información estadística:</strong><br>
        • $SS_{{total}} = {ss_total:.3f}$<br>
        • $SS_{{residual}} = {ss_residual:.3f}$<br>
        • $SS_{{regression}} = {ss_regression:.3f}$<br>
        • Grados de libertad del error: ${n-2}$
        </p>
        <p>
        Calcule las siguientes métricas de evaluación del modelo:
        </p>
        <p>
        <strong>1. Coeficiente de determinación:</strong> $R^2 = $ {me.NM(r_squared, error=0.001)}
        </p>
        <p>
        <strong>2. Error cuadrático medio raíz:</strong> $RMSE = $ {me.NM(root_mean_square_error, error=0.001)}
        </p>
        <p>
        <strong>3. Error absoluto medio:</strong> $MAE = $ {me.NM(mean_absolute_error, error=0.001)}
        </p>
        <p>
        <strong>4. Estadístico F del modelo:</strong> $F = $ {me.NM(f_statistic, error=0.001)}
        </p>
        <p>
        <strong>5. Error estándar de β:</strong> $SE(\\beta) = $ {me.NM(se_beta, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Evaluación del Modelo de Regresión:</strong>
        </p>
        <p>
        <strong>1. Coeficiente de determinación (R²):</strong><br>
        $R^2 = \\frac{{SS_{{regression}}}}{{SS_{{total}}}} = \\frac{{{ss_regression:.3f}}}{{{ss_total:.3f}}} = {r_squared:.6f}$<br>
        Interpretación: El modelo explica el {r_squared*100:.1f}% de la variabilidad en Y.
        </p>
        <p>
        <strong>2. Métricas de error:</strong><br>
        $RMSE = \\sqrt{{\\frac{{SS_{{residual}}}}{{n}}}} = \\sqrt{{\\frac{{{ss_residual:.3f}}}{{{n}}}}} = {root_mean_square_error:.6f}$<br>
        $MAE = \\frac{{1}}{{n}}\\sum|y_i - \\hat{{y}}_i| = {mean_absolute_error:.6f}$<br>
        RMSE penaliza más los errores grandes que MAE.
        </p>
        <p>
        <strong>3. Prueba de significancia global:</strong><br>
        $F = \\frac{{MS_{{regression}}}}{{MS_{{residual}}}} = \\frac{{SS_{{regression}}/1}}{{SS_{{residual}}/(n-2)}}$<br>
        $F = \\frac{{{ss_regression:.3f}/1}}{{{ss_residual:.3f}/{n-2}}} = {f_statistic:.6f}$<br>
        Con F({1},{n-2}) bajo H₀: β = 0
        </p>
        <p>
        <strong>4. Errores estándar de los coeficientes:</strong><br>
        $SE(\\beta) = \\frac{{s_e}}{{\\sqrt{{\\sum(x_i - \\bar{{x}})^2}}}} = \\frac{{{std_error:.3f}}}{{\\sqrt{{{s_xx:.3f}}}}} = {se_beta:.6f}$<br>
        $SE(\\alpha) = s_e\\sqrt{{\\frac{{1}}{{n}} + \\frac{{\\bar{{x}}^2}}{{\\sum(x_i - \\bar{{x}})^2}}}} = {se_alpha:.6f}$
        </p>
        <p>
        <strong>5. Criterios de evaluación:</strong><br>
        • R² alto (> 0.7): Buen ajuste<br>
        • RMSE bajo: Predicciones precisas<br>
        • F significativo: Modelo útil estadísticamente<br>
        • Errores estándar pequeños: Coeficientes precisos
        </p>
        <p>
        <strong>Aplicaciones en Data Science:</strong><br>
        La evaluación rigurosa de modelos es crucial para validar la capacidad predictiva
        y la confiabilidad de los algoritmos de machine learning.
        </p>
        """
    
    else:  # prediction_analysis
        # Focus on prediction and confidence intervals
        n = rnd.randint(20, 30)
        x, y, true_alpha, true_beta, x_mean_pop, x_std_pop, noise_std = generate_regression_data(n)
        
        # Calculate regression coefficients and statistics
        alpha, beta, x_mean, y_mean, numerator, denominator = calculate_regression_coefficients(x, y)
        r_squared, correlation, ss_total, ss_residual, ss_regression, std_error = calculate_regression_statistics(x, y, alpha, beta)
        
        # Prediction point
        x_pred = rnd.randint(int(x_mean - 10), int(x_mean + 10))
        y_pred = alpha + beta * x_pred
        
        # Standard error for prediction
        s_xx = np.sum((x - x_mean)**2)
        se_pred = std_error * np.sqrt(1 + 1/n + (x_pred - x_mean)**2/s_xx) if s_xx > 0 else 0
        se_mean = std_error * np.sqrt(1/n + (x_pred - x_mean)**2/s_xx) if s_xx > 0 else 0
        
        # Confidence intervals (assuming t-distribution with n-2 df)
        # Using approximate t-value of 2 for simplicity
        t_value = 2.0
        ci_pred_lower = y_pred - t_value * se_pred
        ci_pred_upper = y_pred + t_value * se_pred
        ci_mean_lower = y_pred - t_value * se_mean
        ci_mean_upper = y_pred + t_value * se_mean
        
        ejercicio = cabecera + f"""
        <p>
        Se ajustó un modelo de regresión lineal: $\\hat{{y}} = {alpha:.3f} + {beta:.3f}x$
        </p>
        <p>
        <strong>Estadísticas del modelo:</strong><br>
        • Error estándar de la regresión: $s_e = {std_error:.3f}$<br>
        • Media de X: $\\bar{{x}} = {x_mean:.3f}$<br>
        • $\\sum(x_i - \\bar{{x}})^2 = {s_xx:.3f}$<br>
        • Tamaño de muestra: $n = {n}$
        </p>
        <p>
        Para el punto de predicción $x = {x_pred}$, calcule:
        </p>
        <p>
        <strong>1. Valor predicho:</strong> $\\hat{{y}} = $ {me.NM(y_pred, error=0.001)}
        </p>
        <p>
        <strong>2. Error estándar de predicción individual:</strong> $SE_{{pred}} = $ {me.NM(se_pred, error=0.001)}
        </p>
        <p>
        <strong>3. Error estándar de la media predicha:</strong> $SE_{{mean}} = $ {me.NM(se_mean, error=0.001)}
        </p>
        <p>
        <strong>4. Límite inferior IC predicción (95%):</strong> {me.NM(ci_pred_lower, error=0.001)}
        </p>
        <p>
        <strong>5. Límite superior IC predicción (95%):</strong> {me.NM(ci_pred_upper, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Análisis de Predicción e Intervalos de Confianza:</strong>
        </p>
        <p>
        <strong>1. Predicción puntual:</strong><br>
        $\\hat{{y}} = {alpha:.3f} + {beta:.3f} \\times {x_pred} = {y_pred:.6f}$
        </p>
        <p>
        <strong>2. Error estándar para predicción individual:</strong><br>
        $SE_{{pred}} = s_e \\sqrt{{1 + \\frac{{1}}{{n}} + \\frac{{(x_0 - \\bar{{x}})^2}}{{\\sum(x_i - \\bar{{x}})^2}}}}$<br>
        $SE_{{pred}} = {std_error:.3f} \\sqrt{{1 + \\frac{{1}}{{{n}}} + \\frac{{({x_pred} - {x_mean:.3f})^2}}{{{s_xx:.3f}}}}}$<br>
        $SE_{{pred}} = {std_error:.3f} \\sqrt{{1 + {1/n:.6f} + {(x_pred - x_mean)**2/s_xx:.6f}}} = {se_pred:.6f}$
        </p>
        <p>
        <strong>3. Error estándar para la media predicha:</strong><br>
        $SE_{{mean}} = s_e \\sqrt{{\\frac{{1}}{{n}} + \\frac{{(x_0 - \\bar{{x}})^2}}{{\\sum(x_i - \\bar{{x}})^2}}}}$<br>
        $SE_{{mean}} = {std_error:.3f} \\sqrt{{{1/n:.6f} + {(x_pred - x_mean)**2/s_xx:.6f}}} = {se_mean:.6f}$
        </p>
        <p>
        <strong>4. Intervalos de confianza (95%, t ≈ 2):</strong><br>
        <strong>Predicción individual:</strong><br>
        $[{y_pred:.3f} \\pm 2 \\times {se_pred:.3f}] = [{ci_pred_lower:.3f}, {ci_pred_upper:.3f}]$<br>
        <strong>Media condicional:</strong><br>
        $[{y_pred:.3f} \\pm 2 \\times {se_mean:.3f}] = [{ci_mean_lower:.3f}, {ci_mean_upper:.3f}]$
        </p>
        <p>
        <strong>5. Interpretación de los intervalos:</strong><br>
        • IC para predicción individual: 95% de confianza de que una nueva observación caerá en este rango<br>
        • IC para media: 95% de confianza de que la media poblacional condicional está en este rango<br>
        • El IC de predicción es más amplio porque incluye la variabilidad individual
        </p>
        <p>
        <strong>Factores que afectan la precisión:</strong><br>
        • Distancia de x₀ a x̄: mayor distancia → mayor incertidumbre<br>
        • Tamaño de muestra: n mayor → menor incertidumbre<br>
        • Variabilidad de X: mayor dispersión → menor incertidumbre en predicción
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
"""
Curve Fitting and Learning Models

Subject Area: data_science

This module contains educational content generators for curve fitting analysis,
learning curves, and logistic growth models in machine learning applications.
"""

import moodpy as me
import numpy.random as rnd
import numpy as np

label = "CURVE_FITTING_ANALYSIS"
miCabecera = """
<h1> Análisis de Curvas de Aprendizaje </h1>
<h2> Modelos de Crecimiento y Ajuste </h2>
"""

def generate_learning_curve_data(n=50):
    """Generate learning curve data following exponential approach to asymptote."""
    # Parameters for learning curve: y = L(1 - e^(-kx))
    L = rnd.randint(85, 95)  # Learning asymptote (final performance)
    k = rnd.uniform(0.05, 0.15)  # Learning rate constant
    
    # Generate training size points (x-axis)
    x_max = rnd.randint(800, 1200)
    x = np.linspace(50, x_max, n)
    
    # Generate learning curve with noise
    noise_std = rnd.uniform(2, 5)
    noise = rnd.normal(0, noise_std, n)
    y_true = L * (1 - np.exp(-k * x))
    y = y_true + noise
    
    # Ensure performance doesn't exceed 100% or go below initial performance
    initial_performance = rnd.randint(20, 35)
    y = np.clip(y, initial_performance, 100)
    
    return x, y, L, k, x_max, noise_std, initial_performance

def generate_logistic_curve_data(n=40):
    """Generate logistic growth curve data."""
    # Parameters for logistic curve: y = L / (1 + e^(-k(x-x0)))
    L = rnd.randint(900, 1100)  # Carrying capacity
    k = rnd.uniform(0.1, 0.3)   # Growth rate
    x0 = rnd.randint(15, 25)    # Inflection point
    
    # Generate time points
    x_max = rnd.randint(40, 60)
    x = np.linspace(0, x_max, n)
    
    # Generate logistic curve with noise
    noise_std = rnd.uniform(15, 25)
    noise = rnd.normal(0, noise_std, n)
    y_true = L / (1 + np.exp(-k * (x - x0)))
    y = y_true + noise
    
    # Ensure non-negative values
    y = np.clip(y, 0, None)
    
    return x, y, L, k, x0, x_max, noise_std

def fit_exponential_model(x, y):
    """Fit exponential learning model y = L(1 - e^(-kx)) using linearization."""
    # Transform to linear form: ln(L - y) = ln(L) - kx
    # First estimate L as maximum y value plus some margin
    L_est = np.max(y) * 1.1
    
    # Handle cases where y approaches L
    y_transformed = np.clip(L_est - y, 1e-6, None)
    ln_y = np.log(y_transformed)
    
    # Linear regression on ln(L - y) = ln(L) - kx
    n = len(x)
    x_mean = np.mean(x)
    ln_y_mean = np.mean(ln_y)
    
    # Calculate slope (-k) and intercept (ln(L))
    numerator = np.sum((x - x_mean) * (ln_y - ln_y_mean))
    denominator = np.sum((x - x_mean)**2)
    
    if denominator > 0:
        k_est = -numerator / denominator  # Note the negative sign
        ln_L_est = ln_y_mean + k_est * x_mean
        L_fitted = np.exp(ln_L_est)
    else:
        k_est = 0.1
        L_fitted = L_est
    
    return L_fitted, k_est, x_mean, ln_y_mean, numerator, denominator

def fit_logistic_model(x, y):
    """Fit logistic model using linearization around inflection point."""
    # Find approximate inflection point (maximum growth rate)
    if len(y) > 2:
        growth_rate = np.diff(y)
        if len(growth_rate) > 0:
            inflection_idx = np.argmax(growth_rate)
            x0_est = x[inflection_idx]
        else:
            x0_est = np.mean(x)
    else:
        x0_est = np.mean(x)
    
    # Estimate carrying capacity L
    L_est = np.max(y) * 1.2
    
    # Transform to linear form: ln(y/(L-y)) = k(x-x0)
    y_ratio = y / (L_est - y)
    # Handle edge cases
    y_ratio = np.clip(y_ratio, 1e-6, 1e6)
    ln_ratio = np.log(y_ratio)
    
    # Linear regression
    x_centered = x - x0_est
    x_mean = np.mean(x_centered)
    ln_ratio_mean = np.mean(ln_ratio)
    
    numerator = np.sum((x_centered - x_mean) * (ln_ratio - ln_ratio_mean))
    denominator = np.sum((x_centered - x_mean)**2)
    
    if denominator > 0:
        k_est = numerator / denominator
    else:
        k_est = 0.2
        
    return L_est, k_est, x0_est

def calculate_curve_statistics(x, y, y_pred):
    """Calculate fit statistics for curve models."""
    n = len(y)
    
    # Sum of squares
    ss_total = np.sum((y - np.mean(y))**2)
    ss_residual = np.sum((y - y_pred)**2)
    ss_regression = ss_total - ss_residual
    
    # R-squared
    r_squared = ss_regression / ss_total if ss_total > 0 else 0
    
    # Root mean square error
    rmse = np.sqrt(ss_residual / n) if n > 0 else 0
    
    # Mean absolute percentage error
    mape = np.mean(np.abs((y - y_pred) / y)) * 100 if np.all(y != 0) else 0
    
    return r_squared, rmse, mape, ss_total, ss_residual

def gen(impr, cabecera=""):
    """Generate curve fitting analysis problem."""
    
    # Choose problem type
    problem_types = ['learning_curve', 'logistic_growth', 'curve_comparison', 'model_validation']
    problem_type = rnd.choice(problem_types)
    
    if problem_type == 'learning_curve':
        # Generate learning curve data
        n = rnd.randint(20, 30)
        x, y, L_true, k_true, x_max, noise_std, initial_perf = generate_learning_curve_data(n)
        
        # Fit exponential learning model
        L_fit, k_fit, x_mean, ln_y_mean, numerator, denominator = fit_exponential_model(x, y)
        
        # Calculate predictions and statistics
        y_pred = L_fit * (1 - np.exp(-k_fit * x))
        r_squared, rmse, mape, ss_total, ss_residual = calculate_curve_statistics(x, y, y_pred)
        
        # Calculate key learning metrics
        performance_at_half_data = L_fit * (1 - np.exp(-k_fit * x_max/2))
        time_to_90_percent = -np.log(0.1) / k_fit if k_fit > 0 else float('inf')
        
        ejercicio = cabecera + f"""
        <p>
        Se recolectaron {n} puntos de datos sobre el rendimiento de un algoritmo de 
        machine learning en función del tamaño del conjunto de entrenamiento.
        </p>
        <p>
        El modelo de curva de aprendizaje es: $y = L(1 - e^{{-kx}})$
        </p>
        <p>
        <strong>Datos del ajuste:</strong><br>
        • Tamaño máximo de entrenamiento: {x_max} ejemplos<br>
        • Media de tamaños de entrenamiento: $\\bar{{x}} = {x_mean:.1f}$<br>
        • Suma de productos cruzados: $\\sum(x_i - \\bar{{x}})(\\ln(L - y_i) - \\overline{{\\ln(L - y)}}) = {numerator:.3f}$<br>
        • Suma de cuadrados de X: $\\sum(x_i - \\bar{{x}})^2 = {denominator:.1f}$
        </p>
        <p>
        Determine los parámetros del modelo de aprendizaje:
        </p>
        <p>
        <strong>1. Rendimiento asintótico (L):</strong> {me.NM(L_fit, error=0.1)}%
        </p>
        <p>
        <strong>2. Tasa de aprendizaje (k):</strong> {me.NM(k_fit, error=0.001)}
        </p>
        <p>
        <strong>3. Coeficiente de determinación:</strong> $R^2 = $ {me.NM(r_squared, error=0.001)}
        </p>
        <p>
        <strong>4. Error cuadrático medio raíz:</strong> $RMSE = $ {me.NM(rmse, error=0.01)}
        </p>
        <p>
        <strong>5. Rendimiento con {int(x_max/2)} ejemplos:</strong> {me.NM(performance_at_half_data, error=0.1)}%
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución - Análisis de Curva de Aprendizaje:</strong>
        </p>
        <p>
        <strong>1. Modelo exponencial de aprendizaje:</strong><br>
        $y = L(1 - e^{{-kx}})$ donde:<br>
        • L = rendimiento máximo teórico<br>
        • k = tasa de aprendizaje (velocidad de convergencia)<br>
        • x = tamaño del conjunto de entrenamiento
        </p>
        <p>
        <strong>2. Linearización del modelo:</strong><br>
        $L - y = Le^{{-kx}}$<br>
        $\\ln(L - y) = \\ln(L) - kx$<br>
        Regresión lineal: $\\ln(L - y) = a + bx$ donde $b = -k$
        </p>
        <p>
        <strong>3. Estimación de parámetros:</strong><br>
        Tasa de aprendizaje: k = -{numerator:.3f} / {denominator:.1f} = {k_fit:.6f}<br>
        Rendimiento asintótico: L = {L_fit:.1f}% (estimado como límite superior ajustado)
        </p>
        <p>
        <strong>4. Interpretación de resultados:</strong><br>
        • Rendimiento asintótico: {L_fit:.1f}% (límite teórico del algoritmo)<br>
        • Tasa de aprendizaje: {k_fit:.4f} (velocidad de mejora por ejemplo)<br>
        • R² = {r_squared:.3f}: El modelo explica el {r_squared*100:.1f}% de la variabilidad<br>
        • RMSE = {rmse:.2f}%: Error típico en las predicciones
        </p>
        <p>
        <strong>5. Métricas de eficiencia de aprendizaje:</strong><br>
        • Rendimiento con {int(x_max/2)} ejemplos: {performance_at_half_data:.1f}%<br>
        • Ejemplos para alcanzar 90% del rendimiento máximo: {time_to_90_percent:.0f}<br>
        • Eficiencia del algoritmo: {'Alta' if k_fit > 0.01 else 'Moderada' if k_fit > 0.005 else 'Baja'}
        </p>
        <p>
        <strong>Aplicaciones en Machine Learning:</strong><br>
        Las curvas de aprendizaje son esenciales para determinar si un modelo se beneficiaría
        de más datos de entrenamiento y para comparar la eficiencia de diferentes algoritmos.
        </p>
        """
    
    elif problem_type == 'logistic_growth':
        # Generate logistic growth data
        n = rnd.randint(25, 35)
        x, y, L_true, k_true, x0_true, x_max, noise_std = generate_logistic_curve_data(n)
        
        # Fit logistic model
        L_fit, k_fit, x0_fit = fit_logistic_model(x, y)
        
        # Calculate predictions and statistics
        y_pred = L_fit / (1 + np.exp(-k_fit * (x - x0_fit)))
        r_squared, rmse, mape, ss_total, ss_residual = calculate_curve_statistics(x, y, y_pred)
        
        # Calculate growth characteristics
        max_growth_rate = (L_fit * k_fit) / 4  # At inflection point
        growth_at_inflection = L_fit / 2
        
        ejercicio = cabecera + f"""
        <p>
        Se analizó el crecimiento de usuarios de una plataforma digital durante {n} períodos.
        Los datos siguen un patrón de crecimiento logístico.
        </p>
        <p>
        El modelo logístico es: $y = \\frac{{L}}{{1 + e^{{-k(x-x_0)}}}}$
        </p>
        <p>
        <strong>Información del ajuste:</strong><br>
        • Período máximo observado: {x_max} unidades<br>
        • Punto de inflexión estimado: $x_0 = {x0_fit:.1f}$<br>
        • Capacidad de carga estimada: $L = {L_fit:.0f}$ usuarios<br>
        • Tasa de crecimiento: $k = {k_fit:.3f}$
        </p>
        <p>
        Calcule las características del crecimiento logístico:
        </p>
        <p>
        <strong>1. Capacidad de carga (L):</strong> {me.NM(L_fit, error=1)} usuarios
        </p>
        <p>
        <strong>2. Tasa de crecimiento (k):</strong> {me.NM(k_fit, error=0.001)}
        </p>
        <p>
        <strong>3. Punto de inflexión (x₀):</strong> {me.NM(x0_fit, error=0.1)}
        </p>
        <p>
        <strong>4. Tasa máxima de crecimiento:</strong> {me.NM(max_growth_rate, error=0.1)} usuarios/período
        </p>
        <p>
        <strong>5. Coeficiente de determinación:</strong> $R^2 = $ {me.NM(r_squared, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución - Modelo de Crecimiento Logístico:</strong>
        </p>
        <p>
        <strong>1. Ecuación logística:</strong><br>
        $y = \\frac{{L}}{{1 + e^{{-k(x-x_0)}}}}$ donde:<br>
        • L = capacidad de carga (límite superior)<br>
        • k = tasa de crecimiento intrínseca<br>
        • x₀ = punto de inflexión (momento de máximo crecimiento)
        </p>
        <p>
        <strong>2. Parámetros estimados:</strong><br>
        • Capacidad de carga: L = {L_fit:.0f} usuarios<br>
        • Tasa de crecimiento: k = {k_fit:.3f}<br>
        • Punto de inflexión: x₀ = {x0_fit:.1f} períodos
        </p>
        <p>
        <strong>3. Características del crecimiento:</strong><br>
        • En el punto de inflexión (x = {x0_fit:.1f}): y = L/2 = {growth_at_inflection:.0f} usuarios<br>
        • Tasa máxima de crecimiento: $\\frac{{dN}}{{dt}}|_{{max}} = \\frac{{Lk}}{{4}} = {max_growth_rate:.1f}$ usuarios/período<br>
        • El crecimiento es más rápido entre x = {x0_fit-2:.1f} y x = {x0_fit+2:.1f}
        </p>
        <p>
        <strong>4. Fases del crecimiento logístico:</strong><br>
        • Fase exponencial (x < {x0_fit:.1f}): Crecimiento acelerado<br>
        • Punto de inflexión (x = {x0_fit:.1f}): Máxima tasa de crecimiento<br>
        • Fase de saturación (x > {x0_fit:.1f}): Crecimiento desacelerado hacia L
        </p>
        <p>
        <strong>5. Validación del modelo:</strong><br>
        • R² = {r_squared:.3f}: {'Excelente' if r_squared > 0.9 else 'Bueno' if r_squared > 0.8 else 'Aceptable'} ajuste<br>
        • RMSE = {rmse:.1f}: Error promedio de {rmse/L_fit*100:.1f}% respecto a la capacidad<br>
        • MAPE = {mape:.1f}%: Error porcentual absoluto medio
        </p>
        <p>
        <strong>Aplicaciones en Data Science:</strong><br>
        Los modelos logísticos son fundamentales para predecir adopción de tecnologías,
        crecimiento de usuarios, propagación viral, y saturación de mercados.
        </p>
        """
    
    elif problem_type == 'curve_comparison':
        # Compare exponential vs logistic models
        n = rnd.randint(25, 30)
        
        # Generate data that could fit either model
        if rnd.random() < 0.5:
            x, y, L_true, k_true, x_max, noise_std, initial_perf = generate_learning_curve_data(n)
        else:
            x, y, L_true, k_true, x0_true, x_max, noise_std = generate_logistic_curve_data(n)
        
        # Fit both models
        L_exp, k_exp, x_mean, ln_y_mean, num_exp, den_exp = fit_exponential_model(x, y)
        L_log, k_log, x0_log = fit_logistic_model(x, y)
        
        # Calculate predictions for both models
        y_pred_exp = L_exp * (1 - np.exp(-k_exp * x))
        y_pred_log = L_log / (1 + np.exp(-k_log * (x - x0_log)))
        
        # Calculate statistics for both models
        r2_exp, rmse_exp, mape_exp, ss_total, ss_res_exp = calculate_curve_statistics(x, y, y_pred_exp)
        r2_log, rmse_log, mape_log, _, ss_res_log = calculate_curve_statistics(x, y, y_pred_log)
        
        # Model selection criteria
        aic_exp = n * np.log(ss_res_exp/n) + 2 * 2  # 2 parameters
        aic_log = n * np.log(ss_res_log/n) + 2 * 3  # 3 parameters
        
        best_model = "exponential" if aic_exp < aic_log else "logistic"
        aic_difference = abs(aic_exp - aic_log)
        
        ejercicio = cabecera + f"""
        <p>
        Se desea determinar cuál modelo se ajusta mejor a {n} observaciones de crecimiento:
        modelo exponencial $y = L(1 - e^{{-kx}})$ o modelo logístico $y = \\frac{{L}}{{1 + e^{{-k(x-x_0)}}}}$.
        </p>
        <p>
        <strong>Resultados del ajuste exponencial:</strong><br>
        • L = {L_exp:.1f}, k = {k_exp:.4f}<br>
        • $R^2 = {r2_exp:.4f}$, RMSE = {rmse_exp:.2f}
        </p>
        <p>
        <strong>Resultados del ajuste logístico:</strong><br>
        • L = {L_log:.1f}, k = {k_log:.4f}, x₀ = {x0_log:.1f}<br>
        • $R^2 = {r2_log:.4f}$, RMSE = {rmse_log:.2f}
        </p>
        <p>
        Compare los modelos usando criterios de selección:
        </p>
        <p>
        <strong>1. AIC del modelo exponencial:</strong> {me.NM(aic_exp, error=0.01)}
        </p>
        <p>
        <strong>2. AIC del modelo logístico:</strong> {me.NM(aic_log, error=0.01)}
        </p>
        <p>
        <strong>3. Diferencia AIC:</strong> $\\Delta AIC = $ {me.NM(aic_difference, error=0.01)}
        </p>
        <p>
        <strong>4. Mejor modelo según AIC:</strong> {me.STxt(best_model)}
        </p>
        <p>
        <strong>5. R² del mejor modelo:</strong> {me.NM(r2_exp if best_model == "exponential" else r2_log, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Comparación de Modelos - Criterios de Selección:</strong>
        </p>
        <p>
        <strong>1. Criterio de Información de Akaike (AIC):</strong><br>
        $AIC = n \\ln\\left(\\frac{{RSS}}{{n}}\\right) + 2p$ donde p = número de parámetros<br>
        <strong>Modelo exponencial:</strong> AIC = {n} × ln({ss_res_exp:.1f}/{n}) + 2×2 = {aic_exp:.2f}<br>
        <strong>Modelo logístico:</strong> AIC = {n} × ln({ss_res_log:.1f}/{n}) + 2×3 = {aic_log:.2f}
        </p>
        <p>
        <strong>2. Interpretación de la diferencia AIC:</strong><br>
        ΔAI C = |{aic_exp:.2f} - {aic_log:.2f}| = {aic_difference:.2f}<br>
        • ΔAIC < 2: {'✓' if aic_difference < 2 else '✗'} Modelos equivalentes<br>
        • 2 ≤ ΔAIC < 7: {'✓' if 2 <= aic_difference < 7 else '✗'} Evidencia moderada<br>
        • ΔAIC ≥ 7: {'✓' if aic_difference >= 7 else '✗'} Evidencia fuerte
        </p>
        <p>
        <strong>3. Comparación de métricas:</strong><br>
        <table style="border-collapse: collapse; width: 100%;">
        <tr><th style="border: 1px solid black; padding: 5px;">Métrica</th><th style="border: 1px solid black; padding: 5px;">Exponencial</th><th style="border: 1px solid black; padding: 5px;">Logístico</th></tr>
        <tr><td style="border: 1px solid black; padding: 5px;">R²</td><td style="border: 1px solid black; padding: 5px;">{r2_exp:.4f}</td><td style="border: 1px solid black; padding: 5px;">{r2_log:.4f}</td></tr>
        <tr><td style="border: 1px solid black; padding: 5px;">RMSE</td><td style="border: 1px solid black; padding: 5px;">{rmse_exp:.2f}</td><td style="border: 1px solid black; padding: 5px;">{rmse_log:.2f}</td></tr>
        <tr><td style="border: 1px solid black; padding: 5px;">AIC</td><td style="border: 1px solid black; padding: 5px;">{aic_exp:.2f}</td><td style="border: 1px solid black; padding: 5px;">{aic_log:.2f}</td></tr>
        </table>
        </p>
        <p>
        <strong>4. Recomendación de modelo:</strong><br>
        El modelo <strong>{best_model}</strong> es preferible porque:<br>
        • Tiene menor AIC ({aic_exp:.2f} vs {aic_log:.2f})<br>
        • {'Mejor' if (r2_exp > r2_log and best_model == 'exponential') or (r2_log > r2_exp and best_model == 'logistic') else 'Similar'} R² ({r2_exp:.3f} vs {r2_log:.3f})<br>
        • {'Menor' if (rmse_exp < rmse_log and best_model == 'exponential') or (rmse_log < rmse_exp and best_model == 'logistic') else 'Similar'} RMSE ({rmse_exp:.2f} vs {rmse_log:.2f})
        </p>
        <p>
        <strong>5. Consideraciones prácticas:</strong><br>
        • El modelo exponencial asume crecimiento hacia un límite sin punto de inflexión<br>
        • El modelo logístico incluye una fase de crecimiento acelerado seguida de desaceleración<br>
        • La elección también debe considerar el contexto teórico del problema
        </p>
        """
    
    else:  # model_validation
        # Cross-validation and residual analysis
        n = rnd.randint(30, 40)
        x, y, L_true, k_true, x_max, noise_std, initial_perf = generate_learning_curve_data(n)
        
        # Fit model
        L_fit, k_fit, x_mean, ln_y_mean, numerator, denominator = fit_exponential_model(x, y)
        y_pred = L_fit * (1 - np.exp(-k_fit * x))
        
        # Calculate residuals and diagnostic statistics
        residuals = y - y_pred
        
        # Durbin-Watson test statistic for autocorrelation
        dw_statistic = np.sum(np.diff(residuals)**2) / np.sum(residuals**2) if np.sum(residuals**2) > 0 else 2.0
        
        # Normality tests
        mean_residual = np.mean(residuals)
        std_residual = np.std(residuals)
        skewness = np.mean(((residuals - mean_residual) / std_residual)**3) if std_residual > 0 else 0
        kurtosis = np.mean(((residuals - mean_residual) / std_residual)**4) if std_residual > 0 else 3
        
        # Heteroskedasticity check
        correlation_resid_pred = np.corrcoef(np.abs(residuals), y_pred)[0,1] if len(residuals) > 1 else 0
        
        # Calculate fit statistics
        r_squared, rmse, mape, ss_total, ss_residual = calculate_curve_statistics(x, y, y_pred)
        
        ejercicio = cabecera + f"""
        <p>
        Se ajustó un modelo exponencial de curva de aprendizaje a {n} observaciones.
        Se requiere validar la calidad del ajuste mediante análisis residual.
        </p>
        <p>
        <strong>Modelo ajustado:</strong> $\\hat{{y}} = {L_fit:.1f}(1 - e^{{-{k_fit:.4f}x}})$
        </p>
        <p>
        <strong>Estadísticas de los residuos:</strong><br>
        • Media de residuos: $\\bar{{e}} = {mean_residual:.3f}$<br>
        • Desviación estándar: $s_e = {std_residual:.3f}$<br>
        • Coeficiente de asimetría: {skewness:.3f}<br>
        • Coeficiente de curtosis: {kurtosis:.3f}
        </p>
        <p>
        Calcule las métricas de validación del modelo:
        </p>
        <p>
        <strong>1. Coeficiente de determinación:</strong> $R^2 = $ {me.NM(r_squared, error=0.001)}
        </p>
        <p>
        <strong>2. Estadístico Durbin-Watson:</strong> $DW = $ {me.NM(dw_statistic, error=0.01)}
        </p>
        <p>
        <strong>3. Coeficiente de asimetría:</strong> {me.NM(skewness, error=0.01)}
        </p>
        <p>
        <strong>4. Correlación |residuos|-predicción:</strong> {me.NM(correlation_resid_pred, error=0.01)}
        </p>
        <p>
        <strong>5. Error estándar relativo:</strong> {me.NM(rmse/np.mean(y)*100, error=0.1)}%
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Validación del Modelo - Análisis de Residuos:</strong>
        </p>
        <p>
        <strong>1. Bondad de ajuste:</strong><br>
        $R^2 = {r_squared:.4f}$ indica que el modelo explica el {r_squared*100:.1f}% de la variabilidad<br>
        Interpretación: {'Excelente' if r_squared > 0.9 else 'Bueno' if r_squared > 0.8 else 'Aceptable' if r_squared > 0.7 else 'Deficiente'} ajuste
        </p>
        <p>
        <strong>2. Prueba de autocorrelación (Durbin-Watson):</strong><br>
        $DW = \\frac{{\\sum_{{i=2}}^n (e_i - e_{{i-1}})^2}}{{\\sum_{{i=1}}^n e_i^2}} = {dw_statistic:.3f}$<br>
        Interpretación:<br>
        • DW ≈ 2: {'✓' if 1.5 < dw_statistic < 2.5 else '✗'} No autocorrelación (ideal)<br>
        • DW < 1.5: {'✓' if dw_statistic < 1.5 else '✗'} Autocorrelación positiva<br>
        • DW > 2.5: {'✓' if dw_statistic > 2.5 else '✗'} Autocorrelación negativa
        </p>
        <p>
        <strong>3. Normalidad de residuos:</strong><br>
        • Asimetría = {skewness:.3f} {'(Normal)' if abs(skewness) < 0.5 else '(Asimétrico)' if abs(skewness) < 1 else '(Muy asimétrico)'}<br>
        • Curtosis = {kurtosis:.3f} {'(Normal)' if 2 < kurtosis < 4 else '(Leptocúrtica)' if kurtosis > 4 else '(Platicúrtica)'}<br>
        • Media de residuos = {mean_residual:.4f} {'≈ 0 ✓' if abs(mean_residual) < 0.1 else '≠ 0 ⚠'}
        </p>
        <p>
        <strong>4. Homocedasticidad:</strong><br>
        Correlación |residuos|-predicción = {correlation_resid_pred:.3f}<br>
        Interpretación:<br>
        • |r| < 0.3: {'✓' if abs(correlation_resid_pred) < 0.3 else '✗'} Varianza constante (ideal)<br>
        • |r| ≥ 0.3: {'✓' if abs(correlation_resid_pred) >= 0.3 else '✗'} Heterocedasticidad presente
        </p>
        <p>
        <strong>5. Error relativo:</strong><br>
        Error estándar relativo = {rmse/np.mean(y)*100:.1f}%<br>
        {'Excelente' if rmse/np.mean(y) < 0.05 else 'Bueno' if rmse/np.mean(y) < 0.1 else 'Aceptable' if rmse/np.mean(y) < 0.15 else 'Deficiente'} precisión relativa
        </p>
        <p>
        <strong>6. Diagnóstico general:</strong><br>
        El modelo {'cumple' if r_squared > 0.8 and abs(mean_residual) < 0.1 and 1.5 < dw_statistic < 2.5 else 'no cumple completamente'} los supuestos de regresión:<br>
        • Linealidad: {'✓' if r_squared > 0.8 else '⚠'}<br>
        • Independencia: {'✓' if 1.5 < dw_statistic < 2.5 else '⚠'}<br>
        • Normalidad: {'✓' if abs(skewness) < 0.5 and 2 < kurtosis < 4 else '⚠'}<br>
        • Homocedasticidad: {'✓' if abs(correlation_resid_pred) < 0.3 else '⚠'}
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
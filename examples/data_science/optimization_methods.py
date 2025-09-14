"""
Optimization Methods and Parameter Estimation

Subject Area: data_science

This module contains educational content generators for numerical optimization,
gradient descent, and parameter estimation in machine learning contexts.
"""

import moodpy as me
import numpy.random as rnd
import numpy as np

label = "OPTIMIZATION_METHODS"
miCabecera = """
<h1> Métodos de Optimización </h1>
<h2> Estimación de Parámetros y Descenso de Gradiente </h2>
"""

def generate_quadratic_function():
    """Generate a quadratic function for optimization."""
    # Parameters for f(x) = ax^2 + bx + c
    a = rnd.uniform(0.5, 3.0)  # Ensure convex function (a > 0)
    b = rnd.uniform(-10, 10)
    c = rnd.uniform(-20, 20)
    
    # Optimal point: x* = -b/(2a)
    x_optimal = -b / (2 * a)
    f_optimal = a * x_optimal**2 + b * x_optimal + c
    
    return a, b, c, x_optimal, f_optimal

def generate_multivariable_quadratic():
    """Generate a 2D quadratic function for optimization."""
    # Parameters for f(x,y) = ax^2 + by^2 + cxy + dx + ey + f
    a = rnd.uniform(1, 3)    # x^2 coefficient
    b = rnd.uniform(1, 3)    # y^2 coefficient  
    c = rnd.uniform(-1, 1)   # xy coefficient (small for convexity)
    d = rnd.uniform(-5, 5)   # x coefficient
    e = rnd.uniform(-5, 5)   # y coefficient
    f = rnd.uniform(-10, 10) # constant term
    
    # Ensure positive definite Hessian for convexity
    determinant = 4*a*b - c**2
    if determinant <= 0:
        c = 0  # Remove cross term to ensure convexity
        determinant = 4*a*b
    
    # Optimal point from gradient = 0
    # 2ax + cy + d = 0
    # cx + 2by + e = 0
    if determinant > 0:
        x_optimal = (c*e - 2*b*d) / determinant
        y_optimal = (c*d - 2*a*e) / determinant
    else:
        x_optimal = 0
        y_optimal = 0
    
    f_optimal = (a*x_optimal**2 + b*y_optimal**2 + c*x_optimal*y_optimal + 
                 d*x_optimal + e*y_optimal + f)
    
    return a, b, c, d, e, f, x_optimal, y_optimal, f_optimal, determinant

def gradient_descent_1d(a, b, c, x0, learning_rate, max_iterations=100):
    """Perform gradient descent on 1D quadratic function."""
    x = x0
    trajectory = [x]
    f_values = [a*x**2 + b*x + c]
    
    for i in range(max_iterations):
        # Gradient: f'(x) = 2ax + b
        gradient = 2*a*x + b
        
        # Update step
        x_new = x - learning_rate * gradient
        f_new = a*x_new**2 + b*x_new + c
        
        trajectory.append(x_new)
        f_values.append(f_new)
        
        # Check convergence
        if abs(x_new - x) < 1e-6:
            break
            
        x = x_new
    
    return x, f_new, trajectory, f_values, i+1

def newton_method_1d(a, b, c, x0, max_iterations=20):
    """Perform Newton's method on 1D quadratic function."""
    x = x0
    trajectory = [x]
    
    for i in range(max_iterations):
        # First derivative: f'(x) = 2ax + b
        gradient = 2*a*x + b
        
        # Second derivative: f''(x) = 2a
        hessian = 2*a
        
        if abs(hessian) < 1e-10:
            break
            
        # Newton update: x_{k+1} = x_k - f'(x_k)/f''(x_k)
        x_new = x - gradient / hessian
        trajectory.append(x_new)
        
        # Check convergence
        if abs(x_new - x) < 1e-10:
            break
            
        x = x_new
    
    f_final = a*x**2 + b*x + c
    return x, f_final, trajectory, i+1

def analyze_learning_rate_stability(a, b, c, x0, learning_rates):
    """Analyze stability of gradient descent for different learning rates."""
    results = {}
    
    for lr in learning_rates:
        x_final, f_final, trajectory, f_values, iterations = gradient_descent_1d(a, b, c, x0, lr)
        
        # Check if converged (last few values are similar)
        if len(f_values) >= 3:
            converged = abs(f_values[-1] - f_values[-2]) < 1e-6
        else:
            converged = True
            
        # Check for oscillation or divergence
        if len(f_values) >= 5:
            recent_values = f_values[-5:]
            oscillating = max(recent_values) - min(recent_values) > abs(f_values[0] - f_values[-1])
        else:
            oscillating = False
            
        results[lr] = {
            'final_x': x_final,
            'final_f': f_final,
            'iterations': iterations,
            'converged': converged,
            'oscillating': oscillating
        }
    
    return results

def gen(impr, cabecera=""):
    """Generate optimization methods problem."""
    
    # Choose problem type
    problem_types = ['gradient_descent_1d', 'newton_method', 'learning_rate_analysis', 'multivariable_optimization']
    problem_type = rnd.choice(problem_types)
    
    if problem_type == 'gradient_descent_1d':
        # Generate quadratic function and perform gradient descent
        a, b, c, x_optimal, f_optimal = generate_quadratic_function()
        
        # Starting point and learning rate
        x0 = rnd.uniform(-5, 5)
        learning_rate = rnd.uniform(0.01, 0.1)
        
        # Perform gradient descent
        x_final, f_final, trajectory, f_values, iterations = gradient_descent_1d(a, b, c, x0, learning_rate)
        
        # Calculate some intermediate values
        x1 = trajectory[1] if len(trajectory) > 1 else x0
        f1 = f_values[1] if len(f_values) > 1 else f_values[0]
        gradient0 = 2*a*x0 + b
        
        ejercicio = cabecera + f"""
        <p>
        Se desea minimizar la función cuadrática $f(x) = {a:.3f}x^2 + {b:.3f}x + {c:.3f}$
        usando el método de descenso de gradiente.
        </p>
        <p>
        <strong>Parámetros del algoritmo:</strong><br>
        • Punto inicial: $x_0 = {x0:.3f}$<br>
        • Tasa de aprendizaje: $\\alpha = {learning_rate:.3f}$<br>
        • Función objetivo: $f(x) = {a:.3f}x^2 + {b:.3f}x + {c:.3f}$
        </p>
        <p>
        <strong>Análisis del descenso de gradiente:</strong>
        </p>
        <p>
        <strong>1. Gradiente en x₀:</strong> $f'(x_0) = $ {me.NM(gradient0, error=0.001)}
        </p>
        <p>
        <strong>2. Primera iteración x₁:</strong> $x_1 = $ {me.NM(x1, error=0.001)}
        </p>
        <p>
        <strong>3. Valor de función en x₁:</strong> $f(x_1) = $ {me.NM(f1, error=0.001)}
        </p>
        <p>
        <strong>4. Solución final (después de {iterations} iteraciones):</strong> $x^* \\approx $ {me.NM(x_final, error=0.001)}
        </p>
        <p>
        <strong>5. Valor mínimo encontrado:</strong> $f(x^*) \\approx $ {me.NM(f_final, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución - Descenso de Gradiente en 1D:</strong>
        </p>
        <p>
        <strong>1. Algoritmo de descenso de gradiente:</strong><br>
        $x_{{k+1}} = x_k - \\alpha \\nabla f(x_k)$<br>
        Para función cuadrática: $\\nabla f(x) = f'(x) = {2*a:.3f}x + {b:.3f}$
        </p>
        <p>
        <strong>2. Primera iteración:</strong><br>
        $f'(x_0) = {2*a:.3f} \\times {x0:.3f} + {b:.3f} = {gradient0:.6f}$<br>
        $x_1 = x_0 - \\alpha f'(x_0) = {x0:.3f} - {learning_rate:.3f} \\times {gradient0:.6f}$<br>
        $x_1 = {x0:.3f} - {learning_rate*gradient0:.6f} = {x1:.6f}$<br>
        $f(x_1) = {a:.3f} \\times {x1:.3f}^2 + {b:.3f} \\times {x1:.3f} + {c:.3f} = {f1:.6f}$
        </p>
        <p>
        <strong>3. Solución analítica:</strong><br>
        Para función cuadrática $f(x) = ax^2 + bx + c$ con $a > 0$:<br>
        Mínimo en: $x^* = -\\frac{{b}}{{2a}} = -\\frac{{{b:.3f}}}{{2 \\times {a:.3f}}} = {x_optimal:.6f}$<br>
        Valor mínimo: $f(x^*) = {f_optimal:.6f}$
        </p>
        <p>
        <strong>4. Convergencia del algoritmo:</strong><br>
        • Punto final: $x^* \\approx {x_final:.6f}$ (error: {abs(x_final - x_optimal):.6f})<br>
        • Valor final: $f(x^*) \\approx {f_final:.6f}$ (error: {abs(f_final - f_optimal):.6f})<br>
        • Iteraciones necesarias: {iterations}<br>
        • Tasa de convergencia: {'Rápida' if iterations < 20 else 'Moderada' if iterations < 50 else 'Lenta'}
        </p>
        <p>
        <strong>5. Análisis de la tasa de aprendizaje:</strong><br>
        • α = {learning_rate:.3f} {'(apropiada)' if 0.01 <= learning_rate <= 0.1 else '(revisar)'}<br>
        • Para estabilidad en funciones cuadráticas: $\\alpha < \\frac{{2}}{{L}}$ donde $L = 2a = {2*a:.3f}$<br>
        • Límite teórico: $\\alpha < {2/(2*a):.3f}$ {'✓' if learning_rate < 2/(2*a) else '⚠'}
        </p>
        <p>
        <strong>Principios de optimización:</strong><br>
        El descenso de gradiente es un método iterativo fundamental que se mueve
        en dirección opuesta al gradiente, garantizando convergencia local en
        funciones convexas con tasas de aprendizaje apropiadas.
        </p>
        """
    
    elif problem_type == 'newton_method':
        # Newton's method comparison
        a, b, c, x_optimal, f_optimal = generate_quadratic_function()
        
        x0 = rnd.uniform(-3, 3)
        x_final_newton, f_final_newton, trajectory_newton, iterations_newton = newton_method_1d(a, b, c, x0)
        
        # Also run gradient descent for comparison
        learning_rate = 0.05
        x_final_gd, f_final_gd, trajectory_gd, f_values_gd, iterations_gd = gradient_descent_1d(a, b, c, x0, learning_rate)
        
        # Calculate first Newton step manually
        gradient0 = 2*a*x0 + b
        hessian0 = 2*a
        x1_newton = x0 - gradient0/hessian0 if hessian0 != 0 else x0
        
        ejercicio = cabecera + f"""
        <p>
        Compare el método de Newton con descenso de gradiente para minimizar:
        $f(x) = {a:.3f}x^2 + {b:.3f}x + {c:.3f}$
        </p>
        <p>
        <strong>Punto inicial común:</strong> $x_0 = {x0:.3f}$
        </p>
        <p>
        <strong>Información para método de Newton:</strong><br>
        • Primera derivada: $f'(x) = {2*a:.3f}x + {b:.3f}$<br>
        • Segunda derivada: $f''(x) = {2*a:.3f}$<br>
        • Gradiente en x₀: $f'(x_0) = {gradient0:.3f}$<br>
        • Hessiano en x₀: $f''(x_0) = {hessian0:.3f}$
        </p>
        <p>
        Compare ambos métodos:
        </p>
        <p>
        <strong>1. Primera iteración Newton:</strong> $x_1^{{Newton}} = $ {me.NM(x1_newton, error=0.001)}
        </p>
        <p>
        <strong>2. Iteraciones Newton hasta convergencia:</strong> {me.NM(iterations_newton, entero=True)}
        </p>
        <p>
        <strong>3. Solución final Newton:</strong> $x^*_{{Newton}} = $ {me.NM(x_final_newton, error=0.001)}
        </p>
        <p>
        <strong>4. Iteraciones descenso gradiente (α=0.05):</strong> {me.NM(iterations_gd, entero=True)}
        </p>
        <p>
        <strong>5. Diferencia en precisión:</strong> {me.NM(abs(x_final_newton - x_optimal) - abs(x_final_gd - x_optimal), error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Comparación: Método de Newton vs Descenso de Gradiente:</strong>
        </p>
        <p>
        <strong>1. Método de Newton:</strong><br>
        Fórmula: $x_{{k+1}} = x_k - \\frac{{f'(x_k)}}{{f''(x_k)}}$<br>
        Primera iteración:<br>
        $x_1 = x_0 - \\frac{{f'(x_0)}}{{f''(x_0)}} = {x0:.3f} - \\frac{{{gradient0:.3f}}}{{{hessian0:.3f}}} = {x0:.3f} - {gradient0/hessian0:.6f} = {x1_newton:.6f}$
        </p>
        <p>
        <strong>2. Convergencia Newton:</strong><br>
        • Iteraciones: {iterations_newton} {'(convergencia cuadrática)' if iterations_newton <= 3 else '(verificar implementación)'}<br>
        • Solución: $x^* = {x_final_newton:.6f}$<br>
        • Error absoluto: $|x^* - x_{{analítico}}| = {abs(x_final_newton - x_optimal):.8f}$<br>
        • {'✓ Convergencia exacta' if abs(x_final_newton - x_optimal) < 1e-10 else '⚠ Convergencia numérica'}
        </p>
        <p>
        <strong>3. Comparación con descenso de gradiente:</strong><br>
        <table style="border-collapse: collapse; width: 100%;">
        <tr><th style="border: 1px solid black; padding: 5px;">Método</th><th style="border: 1px solid black; padding: 5px;">Iteraciones</th><th style="border: 1px solid black; padding: 5px;">Error final</th><th style="border: 1px solid black; padding: 5px;">Convergencia</th></tr>
        <tr><td style="border: 1px solid black; padding: 5px;">Newton</td><td style="border: 1px solid black; padding: 5px;">{iterations_newton}</td><td style="border: 1px solid black; padding: 5px;">{abs(x_final_newton - x_optimal):.2e}</td><td style="border: 1px solid black; padding: 5px;">Cuadrática</td></tr>
        <tr><td style="border: 1px solid black; padding: 5px;">Grad. Desc.</td><td style="border: 1px solid black; padding: 5px;">{iterations_gd}</td><td style="border: 1px solid black; padding: 5px;">{abs(x_final_gd - x_optimal):.2e}</td><td style="border: 1px solid black; padding: 5px;">Lineal</td></tr>
        </table>
        </p>
        <p>
        <strong>4. Ventajas del método de Newton:</strong><br>
        • Convergencia cuadrática (muy rápida cerca del óptimo)<br>
        • Para funciones cuadrráticas: convergencia exacta en 1 iteración<br>
        • No requiere ajustar tasa de aprendizaje<br>
        • Utiliza información de segunda derivada (curvatura)
        </p>
        <p>
        <strong>5. Consideraciones prácticas:</strong><br>
        • Newton requiere calcular/invertir Hessiano (costoso en alta dimensión)<br>
        • Descenso de gradiente es más simple y escalable<br>
        • Newton puede fallar si Hessiano no es positivo definido<br>
        • Híbridos: quasi-Newton (BFGS, L-BFGS) combinan ventajas de ambos
        </p>
        """
    
    elif problem_type == 'learning_rate_analysis':
        # Learning rate stability analysis
        a, b, c, x_optimal, f_optimal = generate_quadratic_function()
        x0 = rnd.uniform(-3, 3)
        
        # Theoretical maximum stable learning rate
        max_stable_lr = 2 / (2 * a)  # For quadratic functions
        
        # Choose specific learning rates for analysis
        lr_small = 0.01
        lr_good = min(0.1, max_stable_lr * 0.8)
        lr_large = max_stable_lr * 1.5
        
        # Run specific cases
        x_small, f_small, traj_small, vals_small, iter_small = gradient_descent_1d(a, b, c, x0, lr_small)
        x_good, f_good, traj_good, vals_good, iter_good = gradient_descent_1d(a, b, c, x0, lr_good)
        
        ejercicio = cabecera + f"""
        <p>
        Analice el efecto de la tasa de aprendizaje en la convergencia del descenso de gradiente
        para la función $f(x) = {a:.3f}x^2 + {b:.3f}x + {c:.3f}$.
        </p>
        <p>
        <strong>Punto inicial:</strong> $x_0 = {x0:.3f}$<br>
        <strong>Límite teórico de estabilidad:</strong> $\\alpha_{{max}} = \\frac{{2}}{{2a}} = {max_stable_lr:.3f}$
        </p>
        <p>
        <strong>Resultados con diferentes tasas de aprendizaje:</strong><br>
        • α = {lr_small}: {iter_small} iteraciones, x* = {x_small:.4f}<br>
        • α = {lr_good:.3f}: {iter_good} iteraciones, x* = {x_good:.4f}<br>
        • α = {lr_large:.3f}: {'Inestable' if lr_large > max_stable_lr else 'Estable'}
        </p>
        <p>
        Determine las características de convergencia:
        </p>
        <p>
        <strong>1. Límite máximo estable:</strong> $\\alpha_{{max}} = $ {me.NM(max_stable_lr, error=0.001)}
        </p>
        <p>
        <strong>2. Iteraciones con α = {lr_small}:</strong> {me.NM(iter_small, entero=True)}
        </p>
        <p>
        <strong>3. Iteraciones con α = {lr_good:.3f}:</strong> {me.NM(iter_good, entero=True)}
        </p>
        <p>
        <strong>4. Error final con α = {lr_small}:</strong> {me.NM(abs(x_small - x_optimal), error=0.001)}
        </p>
        <p>
        <strong>5. Mejora en eficiencia:</strong> {me.NM((iter_small - iter_good)/iter_small * 100, error=0.1)}%
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Análisis de Tasa de Aprendizaje:</strong>
        </p>
        <p>
        <strong>1. Teoría de estabilidad:</strong><br>
        Para función cuadrática $f(x) = ax^2 + bx + c$ con $a > 0$:<br>
        • Hessiano: $H = f''(x) = 2a = {2*a:.3f}$<br>
        • Condición de estabilidad: $\\alpha < \\frac{{2}}{{L}}$ donde $L$ es la constante de Lipschitz<br>
        • Límite máximo: $\\alpha_{{max}} = \\frac{{2}}{{2a}} = \\frac{{2}}{{{2*a:.3f}}} = {max_stable_lr:.6f}$
        </p>
        <p>
        <strong>2. Análisis de convergencia:</strong><br>
        <table style="border-collapse: collapse; width: 100%;">
        <tr><th style="border: 1px solid black; padding: 5px;">α</th><th style="border: 1px solid black; padding: 5px;">Iteraciones</th><th style="border: 1px solid black; padding: 5px;">Error final</th><th style="border: 1px solid black; padding: 5px;">Comportamiento</th></tr>
        <tr><td style="border: 1px solid black; padding: 5px;">{lr_small}</td><td style="border: 1px solid black; padding: 5px;">{iter_small}</td><td style="border: 1px solid black; padding: 5px;">{abs(x_small - x_optimal):.2e}</td><td style="border: 1px solid black; padding: 5px;">Lento pero estable</td></tr>
        <tr><td style="border: 1px solid black; padding: 5px;">{lr_good:.3f}</td><td style="border: 1px solid black; padding: 5px;">{iter_good}</td><td style="border: 1px solid black; padding: 5px;">{abs(x_good - x_optimal):.2e}</td><td style="border: 1px solid black; padding: 5px;">Óptimo</td></tr>
        <tr><td style="border: 1px solid black; padding: 5px;">{lr_large:.3f}</td><td style="border: 1px solid black; padding: 5px;">—</td><td style="border: 1px solid black; padding: 5px;">—</td><td style="border: 1px solid black; padding: 5px;">{'Diverge' if lr_large > max_stable_lr else 'Oscila'}</td></tr>
        </table>
        </p>
        <p>
        <strong>3. Eficiencia relativa:</strong><br>
        Mejora con α óptimo: $\\frac{{{iter_small} - {iter_good}}}{{{iter_small}}} \\times 100\\% = {(iter_small - iter_good)/iter_small * 100:.1f}\\%$<br>
        • α muy pequeño: convergencia lenta pero segura<br>
        • α óptimo: máxima eficiencia dentro del rango estable<br>
        • α muy grande: inestabilidad o divergencia
        </p>
        <p>
        <strong>4. Reglas prácticas para elegir α:</strong><br>
        • Empezar con α = 0.01 y ajustar según comportamiento<br>
        • Si converge lentamente: aumentar α gradualmente<br>
        • Si oscila o diverge: reducir α significativamente<br>
        • Para funciones cuadráticas: α ≈ 0.5 × αₘₐₓ es usualmente óptimo
        </p>
        <p>
        <strong>5. Estrategias adaptativas:</strong><br>
        • Learning rate scheduling: reducir α durante entrenamiento<br>
        • Adam, RMSprop: ajustan α automáticamente por parámetro<br>
        • Line search: buscar α óptimo en cada iteración<br>
        • Backtracking: reducir α si no hay mejora suficiente
        </p>
        """
    
    else:  # multivariable_optimization
        # 2D optimization problem
        a, b, c, d, e, f, x_opt, y_opt, f_opt, det = generate_multivariable_quadratic()
        
        # Starting point
        x0 = rnd.uniform(-2, 2)
        y0 = rnd.uniform(-2, 2)
        
        # Calculate gradient and Hessian at starting point
        grad_x0 = 2*a*x0 + c*y0 + d
        grad_y0 = c*x0 + 2*b*y0 + e
        grad_norm0 = np.sqrt(grad_x0**2 + grad_y0**2)
        
        # Hessian matrix
        H11, H12, H21, H22 = 2*a, c, c, 2*b
        det_hessian = H11*H22 - H12*H21
        trace_hessian = H11 + H22
        
        # Eigenvalues of Hessian (for 2x2 matrix)
        discriminant = trace_hessian**2 - 4*det_hessian
        if discriminant >= 0:
            lambda1 = (trace_hessian + np.sqrt(discriminant)) / 2
            lambda2 = (trace_hessian - np.sqrt(discriminant)) / 2
        else:
            lambda1 = lambda2 = trace_hessian / 2  # Complex eigenvalues
        
        # Condition number
        if lambda2 != 0:
            condition_number = lambda1 / lambda2 if lambda2 > 0 else float('inf')
        else:
            condition_number = float('inf')
        
        ejercicio = cabecera + f"""
        <p>
        Optimice la función cuadrática de dos variables:
        $f(x,y) = {a:.2f}x^2 + {b:.2f}y^2 + {c:.2f}xy + {d:.2f}x + {e:.2f}y + {f:.2f}$
        </p>
        <p>
        <strong>Punto inicial:</strong> $(x_0, y_0) = ({x0:.3f}, {y0:.3f})$
        </p>
        <p>
        <strong>Análisis del gradiente en el punto inicial:</strong><br>
        • $\\frac{{\\partial f}}{{\\partial x}}|_0 = {2*a:.2f}x_0 + {c:.2f}y_0 + {d:.2f} = {grad_x0:.3f}$<br>
        • $\\frac{{\\partial f}}{{\\partial y}}|_0 = {c:.2f}x_0 + {2*b:.2f}y_0 + {e:.2f} = {grad_y0:.3f}$<br>
        • $||\\nabla f||_0 = {grad_norm0:.3f}$
        </p>
        <p>
        <strong>Matriz Hessiana:</strong><br>
        $H = \\begin{{pmatrix}} {H11:.2f} & {H12:.2f} \\\\ {H21:.2f} & {H22:.2f} \\end{{pmatrix}}$
        </p>
        <p>
        Determine las propiedades de optimización:
        </p>
        <p>
        <strong>1. Punto óptimo x*:</strong> {me.NM(x_opt, error=0.001)}
        </p>
        <p>
        <strong>2. Punto óptimo y*:</strong> {me.NM(y_opt, error=0.001)}
        </p>
        <p>
        <strong>3. Valor mínimo f(x*,y*):</strong> {me.NM(f_opt, error=0.001)}
        </p>
        <p>
        <strong>4. Determinante del Hessiano:</strong> {me.NM(det_hessian, error=0.001)}
        </p>
        <p>
        <strong>5. Número de condición:</strong> {me.NM(condition_number if condition_number != float('inf') else 1000, error=0.1)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Optimización Multivariable - Análisis Completo:</strong>
        </p>
        <p>
        <strong>1. Condiciones de optimalidad:</strong><br>
        Para encontrar el mínimo, igualamos el gradiente a cero:<br>
        $\\frac{{\\partial f}}{{\\partial x}} = {2*a:.2f}x + {c:.2f}y + {d:.2f} = 0$<br>
        $\\frac{{\\partial f}}{{\\partial y}} = {c:.2f}x + {2*b:.2f}y + {e:.2f} = 0$
        </p>
        <p>
        <strong>2. Solución del sistema lineal:</strong><br>
        Sistema en forma matricial:<br>
        $\\begin{{pmatrix}} {2*a:.2f} & {c:.2f} \\\\ {c:.2f} & {2*b:.2f} \\end{{pmatrix}} \\begin{{pmatrix}} x \\\\ y \\end{{pmatrix}} = \\begin{{pmatrix}} {-d:.2f} \\\\ {-e:.2f} \\end{{pmatrix}}$<br>
        <br>
        Determinante: $\\Delta = {2*a:.2f} \\times {2*b:.2f} - {c:.2f}^2 = {det_hessian:.3f}$<br>
        $x^* = \\frac{{({-d:.2f}) \\times {2*b:.2f} - ({c:.2f}) \\times ({-e:.2f})}}{{{det_hessian:.3f}}} = {x_opt:.6f}$<br>  
        $y^* = \\frac{{({2*a:.2f}) \\times ({-e:.2f}) - ({c:.2f}) \\times ({-d:.2f})}}{{{det_hessian:.3f}}} = {y_opt:.6f}$
        </p>
        <p>
        <strong>3. Análisis de la matriz Hessiana:</strong><br>
        $H = \\begin{{pmatrix}} {H11:.2f} & {H12:.2f} \\\\ {H21:.2f} & {H22:.2f} \\end{{pmatrix}}$<br>
        • Determinante: $\\det(H) = {det_hessian:.3f}$ {'> 0 ✓' if det_hessian > 0 else '≤ 0 ⚠'}<br>
        • Traza: $\\text{{tr}}(H) = {trace_hessian:.3f}$ {'> 0 ✓' if trace_hessian > 0 else '≤ 0 ⚠'}<br>
        • Eigenvalores: $\\lambda_1 = {lambda1:.3f}$, $\\lambda_2 = {lambda2:.3f}$<br>
        • Clasificación: {'Mínimo definido positivo' if det_hessian > 0 and trace_hessian > 0 else 'Punto silla o indefinido'}
        </p>
        <p>
        <strong>4. Número de condición y convergencia:</strong><br>
        $\\kappa(H) = \\frac{{\\lambda_{{max}}}}{{\\lambda_{{min}}}} = \\frac{{{lambda1:.3f}}}{{{lambda2:.3f}}} = {condition_number:.1f}$<br>
        Interpretación:<br>
        • κ < 10: {'✓' if condition_number < 10 else '✗'} Bien condicionado (convergencia rápida)<br>
        • 10 ≤ κ < 100: {'✓' if 10 <= condition_number < 100 else '✗'} Moderadamente condicionado<br>
        • κ ≥ 100: {'✓' if condition_number >= 100 else '✗'} Mal condicionado (convergencia lenta)
        </p>
        <p>
        <strong>5. Valor mínimo de la función:</strong><br>
        $f(x^*, y^*) = {a:.2f} \\times {x_opt:.3f}^2 + {b:.2f} \\times {y_opt:.3f}^2 + {c:.2f} \\times {x_opt:.3f} \\times {y_opt:.3f}$<br>
        $\\quad\\quad\\quad + {d:.2f} \\times {x_opt:.3f} + {e:.2f} \\times {y_opt:.3f} + {f:.2f} = {f_opt:.6f}$
        </p>
        <p>
        <strong>6. Estrategias de optimización:</strong><br>
        • Gradiente conjugado: eficiente para matrices mal condicionadas<br>
        • Precondicionamiento: mejorar número de condición<br>
        • Newton multidimensional: usar información completa del Hessiano<br>
        • Quasi-Newton: aproximar Hessiano sin calcularlo explícitamente
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
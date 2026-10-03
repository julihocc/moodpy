"""
Differential Equations for Engineering

Subject Area: engineering

This module contains educational content generators for ordinary differential equations,
partial differential equations, and engineering applications in system analysis.
"""

import moodpy as me
import numpy.random as rnd
import math

label = "DIFFERENTIAL_EQUATIONS"
miCabecera = """
<h1> Ecuaciones Diferenciales </h1>
<h2> Aplicaciones en Sistemas de Ingeniería </h2>
"""

def gen(impr, cabecera=""):
    """Generate differential equations problem."""
    
    # Choose problem type
    problem_types = ['first_order_ode', 'second_order_ode', 'system_analysis', 'laplace_applications']
    problem_type = rnd.choice(problem_types)
    
    if problem_type == 'first_order_ode':
        # Generate first-order linear ODE: dy/dx + p(x)y = q(x)
        # Simple case: dy/dx + ay = b (constant coefficients)
        a = rnd.randint(1, 5)
        b = rnd.randint(2, 8)
        
        # Initial condition
        y0 = rnd.randint(1, 6)
        
        # Analytical solution: y = (b/a) + (y0 - b/a)e^(-ax)
        # Particular solution: yp = b/a
        # Homogeneous solution: yh = Ce^(-ax)
        yp = b / a
        C = y0 - yp
        
        # Value at x = 1
        x_eval = 1
        y_at_1 = yp + C * math.exp(-a * x_eval)
        
        # Steady-state value (as x → ∞)
        steady_state = yp
        
        # Time constant τ = 1/a
        time_constant = 1 / a
        
        ejercicio = cabecera + f"""
        <p>
        Resuelva la ecuación diferencial de primer orden:
        </p>
        <p>
        $\\frac{{dy}}{{dx}} + {a}y = {b}$
        </p>
        <p>
        con condición inicial: $y(0) = {y0}$
        </p>
        <p>
        Determine:
        </p>
        <p>
        <strong>1. Solución particular:</strong> $y_p = $ {me.NM(yp, error=0.001)}
        </p>
        <p>
        <strong>2. Constante de integración:</strong> $C = $ {me.NM(C, error=0.001)}
        </p>
        <p>
        <strong>3. Valor en x = 1:</strong> $y(1) = $ {me.NM(y_at_1, error=0.001)}
        </p>
        <p>
        <strong>4. Valor en estado estacionario:</strong> $y_{{\infty}} = $ {me.NM(steady_state, error=0.001)}
        </p>
        <p>
        <strong>5. Constante de tiempo:</strong> $\\tau = $ {me.NM(time_constant, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución paso a paso:</strong>
        </p>
        <p>
        <strong>1. Identificación del tipo:</strong><br>
        Esta es una EDO lineal de primer orden con coeficientes constantes:<br>
        $\\frac{{dy}}{{dx}} + {a}y = {b}$
        </p>
        <p>
        <strong>2. Solución de la ecuación homogénea:</strong><br>
        $\\frac{{dy}}{{dx}} + {a}y = 0$<br>
        $\\frac{{dy}}{{y}} = -{a}dx$<br>
        $\\ln|y| = -{a}x + \\ln|C|$<br>
        $y_h = Ce^{{-{a}x}}$
        </p>
        <p>
        <strong>3. Solución particular:</strong><br>
        Para el término constante {b}, probamos $y_p = $ constante<br>
        $\\frac{{dy_p}}{{dx}} = 0$<br>
        $0 + {a}y_p = {b}$<br>
        $y_p = \\frac{{{b}}}{{{a}}} = {yp:.6f}$
        </p>
        <p>
        <strong>4. Solución general:</strong><br>
        $y(x) = y_h + y_p = Ce^{{-{a}x}} + {yp:.6f}$
        </p>
        <p>
        <strong>5. Aplicación de condición inicial:</strong><br>
        $y(0) = {y0}$<br>
        $Ce^{{-{a} \\cdot 0}} + {yp:.6f} = {y0}$<br>
        $C + {yp:.6f} = {y0}$<br>
        $C = {y0} - {yp:.6f} = {C:.6f}$
        </p>
        <p>
        <strong>6. Solución específica:</strong><br>
        $y(x) = {yp:.6f} + {C:.6f}e^{{-{a}x}}$
        </p>
        <p>
        <strong>7. Evaluaciones:</strong><br>
        $y(1) = {yp:.6f} + {C:.6f}e^{{-{a}}} = {yp:.6f} + {C:.6f} \\times {math.exp(-a):.6f} = {y_at_1:.6f}$<br>
        $y_{{\infty}} = \\lim_{{x \\to \\infty}} y(x) = {yp:.6f}$ (término exponencial → 0)
        </p>
        <p>
        <strong>8. Constante de tiempo:</strong><br>
        $\\tau = \\frac{{1}}{{a}} = \\frac{{1}}{{{a}}} = {time_constant:.6f}$<br>
        En $t = \\tau$, la respuesta exponencial decae a $1/e \\approx 36.8\\%$ de su valor inicial.
        </p>
        <p>
        <strong>Aplicaciones en ingeniería:</strong><br>
        Esta ecuación modela circuitos RC, enfriamiento de Newton, decaimiento radioactivo,
        y respuesta de sistemas de primer orden en control automático.
        </p>
        """
    
    elif problem_type == 'second_order_ode':
        # Second-order ODE with constant coefficients: ay'' + by' + cy = 0
        # Choose coefficients for different types of roots
        response_type = rnd.choice(['overdamped', 'critically_damped', 'underdamped'])
        
        if response_type == 'overdamped':
            # Two distinct real roots
            r1 = -rnd.randint(1, 3)
            r2 = -rnd.randint(4, 6)
            # ay'' + by' + cy = 0 where r1, r2 are roots of ar² + br + c = 0
            a = 1
            b = -(r1 + r2)
            c = r1 * r2
        elif response_type == 'critically_damped':
            # Repeated real root
            r = -rnd.randint(2, 4)
            a = 1
            b = -2 * r
            c = r * r
        else:  # underdamped
            # Complex conjugate roots: -α ± jβ
            alpha = rnd.randint(1, 3)
            beta = rnd.randint(2, 4)
            a = 1
            b = 2 * alpha
            c = alpha**2 + beta**2
        
        # Initial conditions
        y0 = rnd.randint(1, 5)
        dy0 = rnd.randint(-3, 3)
        
        # Calculate discriminant
        discriminant = b**2 - 4*a*c
        
        ejercicio = cabecera + f"""
        <p>
        Analice la ecuación diferencial de segundo orden:
        </p>
        <p>
        ${a}y'' + {b}y' + {c}y = 0$
        </p>
        <p>
        con condiciones iniciales: $y(0) = {y0}$, $y'(0) = {dy0}$
        </p>
        <p>
        Determine:
        </p>
        <p>
        <strong>1. Discriminante:</strong> $\\Delta = b^2 - 4ac = $ {me.NM(discriminant, error=0.001)}
        </p>
        <p>
        <strong>2. Tipo de respuesta:</strong> {me.MC("Sobreamortiguada~Críticamente amortiguada~Subamortiguada", correct=response_type.replace('_', ' ').title())}
        </p>
        """
        
        if response_type == 'overdamped':
            ejercicio += f"""
            <p>
            <strong>3. Primera raíz:</strong> $r_1 = $ {me.NM(r1, error=0.001)}
            </p>
            <p>
            <strong>4. Segunda raíz:</strong> $r_2 = $ {me.NM(r2, error=0.001)}
            </p>
            """
        elif response_type == 'critically_damped':
            ejercicio += f"""
            <p>
            <strong>3. Raíz repetida:</strong> $r = $ {me.NM(r, error=0.001)}
            </p>
            <p>
            <strong>4. Multiplicidad:</strong> {me.NM(2, error=0.001)}
            </p>
            """
        else:  # underdamped
            ejercicio += f"""
            <p>
            <strong>3. Parte real de las raíces:</strong> $\\alpha = $ {me.NM(-alpha, error=0.001)}
            </p>
            <p>
            <strong>4. Parte imaginaria:</strong> $\\beta = $ {me.NM(beta, error=0.001)}
            </p>
            """
        
        retroalimentacion = f"""
        <p>
        <strong>Análisis de la ecuación característica:</strong>
        </p>
        <p>
        <strong>1. Ecuación característica:</strong><br>
        Para la EDO ${a}y'' + {b}y' + {c}y = 0$<br>
        La ecuación característica es: ${a}r^2 + {b}r + {c} = 0$
        </p>
        <p>
        <strong>2. Discriminante:</strong><br>
        $\\Delta = b^2 - 4ac = {b}^2 - 4({a})({c}) = {b**2} - {4*a*c} = {discriminant}$
        </p>
        """
        
        if response_type == 'overdamped':
            retroalimentacion += f"""
            <p>
            <strong>3. Caso sobreamortiguado (Δ > 0):</strong><br>
            Dos raíces reales distintas:<br>
            $r_1 = \\frac{{-b + \\sqrt{{\\Delta}}}}{{2a}} = \\frac{{-{b} + \\sqrt{{{discriminant}}}}}{{2({a})}} = {r1}$<br>
            $r_2 = \\frac{{-b - \\sqrt{{\\Delta}}}}{{2a}} = \\frac{{-{b} - \\sqrt{{{discriminant}}}}}{{2({a})}} = {r2}$
            </p>
            <p>
            <strong>4. Solución general:</strong><br>
            $y(t) = C_1 e^{{{r1}t}} + C_2 e^{{{r2}t}}$
            </p>
            <p>
            <strong>5. Comportamiento:</strong><br>
            Ambas raíces son negativas, por lo que la solución decae exponencialmente
            sin oscilaciones. El sistema regresa al equilibrio sin sobreimpulso.
            </p>
            """
        elif response_type == 'critically_damped':
            retroalimentacion += f"""
            <p>
            <strong>3. Caso críticamente amortiguado (Δ = 0):</strong><br>
            Una raíz real repetida:<br>
            $r = \\frac{{-b}}{{2a}} = \\frac{{-{b}}}{{2({a})}} = {r}$
            </p>
            <p>
            <strong>4. Solución general:</strong><br>
            $y(t) = (C_1 + C_2 t) e^{{{r}t}}$
            </p>
            <p>
            <strong>5. Comportamiento:</strong><br>
            La solución decae exponencialmente sin oscilaciones, pero más lentamente
            que el caso sobreamortiguado debido al factor $t$.
            </p>
            """
        else:  # underdamped
            retroalimentacion += f"""
            <p>
            <strong>3. Caso subamortiguado (Δ < 0):</strong><br>
            Dos raíces complejas conjugadas:<br>
            $r_{{1,2}} = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}} = \\frac{{-{b} \\pm \\sqrt{{{discriminant}}}}}{{2({a})}}$<br>
            $= \\frac{{-{b} \\pm j\\sqrt{{{abs(discriminant)}}}}}{{2}} = -{alpha} \\pm j{beta}$
            </p>
            <p>
            <strong>4. Solución general:</strong><br>
            $y(t) = e^{{-{alpha}t}}(C_1 \\cos({beta}t) + C_2 \\sin({beta}t))$<br>
            o en forma alternativa:<br>
            $y(t) = A e^{{-{alpha}t}} \\cos({beta}t + \\phi)$
            </p>
            <p>
            <strong>5. Comportamiento:</strong><br>
            La solución oscila con frecuencia ${beta}$ rad/s mientras decae
            exponencialmente con constante de tiempo $\\tau = 1/{alpha}$ s.
            </p>
            """
        
        retroalimentacion += f"""
        <p>
        <strong>6. Aplicación de condiciones iniciales:</strong><br>
        Con $y(0) = {y0}$ y $y'(0) = {dy0}$, se pueden determinar las constantes
        $C_1$ y $C_2$ resolviendo el sistema de ecuaciones resultante.
        </p>
        <p>
        <strong>Aplicaciones en ingeniería:</strong><br>
        • Sistemas masa-resorte-amortiguador<br>
        • Circuitos RLC<br>
        • Sistemas de control de segundo orden<br>
        • Análisis de vibraciones mecánicas<br>
        • Respuesta dinámica de estructuras
        </p>
        """
    
    elif problem_type == 'system_analysis':
        # System of first-order ODEs (2x2 system)
        # dx/dt = ax + by, dy/dt = cx + dy
        # Choose coefficients for stable system
        a = rnd.randint(-3, -1)
        b = rnd.randint(-2, 2)
        c = rnd.randint(-2, 2)
        d = rnd.randint(-3, -1)
        
        # Ensure we don't have b = c = 0 (decoupled system)
        if b == 0 and c == 0:
            b = rnd.choice([-1, 1])
        
        # Calculate eigenvalues of coefficient matrix
        # det(A - λI) = (a-λ)(d-λ) - bc = λ² - (a+d)λ + (ad-bc) = 0
        trace = a + d
        determinant = a * d - b * c
        discriminant = trace**2 - 4 * determinant
        
        if discriminant >= 0:
            lambda1 = (trace + math.sqrt(discriminant)) / 2
            lambda2 = (trace - math.sqrt(discriminant)) / 2
        else:
            real_part = trace / 2
            imag_part = math.sqrt(abs(discriminant)) / 2
            lambda1 = complex(real_part, imag_part)
            lambda2 = complex(real_part, -imag_part)
        
        # System stability
        is_stable = (trace < 0 and determinant > 0)
        
        ejercicio = cabecera + f"""
        <p>
        Analice el sistema de ecuaciones diferenciales:
        </p>
        <p>
        $\\frac{{dx}}{{dt}} = {a}x + {b}y$<br>
        $\\frac{{dy}}{{dt}} = {c}x + {d}y$
        </p>
        <p>
        Determine las propiedades del sistema:
        </p>
        <p>
        <strong>1. Traza de la matriz de coeficientes:</strong> $\\text{{tr}}(A) = $ {me.NM(trace, error=0.001)}
        </p>
        <p>
        <strong>2. Determinante de la matriz:</strong> $\\det(A) = $ {me.NM(determinant, error=0.001)}
        </p>
        <p>
        <strong>3. Discriminante:</strong> $\\Delta = $ {me.NM(discriminant, error=0.001)}
        </p>
        """
        
        if isinstance(lambda1, complex):
            ejercicio += f"""
            <p>
            <strong>4. Parte real de eigenvalores:</strong> $\\text{{Re}}(\\lambda) = $ {me.NM(lambda1.real, error=0.001)}
            </p>
            <p>
            <strong>5. Parte imaginaria:</strong> $\\text{{Im}}(\\lambda) = $ ±{me.NM(abs(lambda1.imag), error=0.001)}
            </p>
            """
        else:
            ejercicio += f"""
            <p>
            <strong>4. Primer eigenvalor:</strong> $\\lambda_1 = $ {me.NM(lambda1, error=0.001)}
            </p>
            <p>
            <strong>5. Segundo eigenvalor:</strong> $\\lambda_2 = $ {me.NM(lambda2, error=0.001)}
            </p>
            """
        
        ejercicio += f"""
        <p>
        <strong>6. El sistema es:</strong> {me.MC("Estable~Inestable~Marginalmente estable", correct="Estable" if is_stable else "Inestable")}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Análisis del sistema lineal:</strong>
        </p>
        <p>
        <strong>1. Matriz de coeficientes:</strong><br>
        $A = \\begin{{pmatrix}} {a} & {b} \\\\ {c} & {d} \\end{{pmatrix}}$
        </p>
        <p>
        <strong>2. Propiedades de la matriz:</strong><br>
        Traza: $\\text{{tr}}(A) = {a} + {d} = {trace}$<br>
        Determinante: $\\det(A) = {a} \\cdot {d} - {b} \\cdot {c} = {a*d} - {b*c} = {determinant}$
        </p>
        <p>
        <strong>3. Ecuación característica:</strong><br>
        $\\det(A - \\lambda I) = \\lambda^2 - \\text{{tr}}(A)\\lambda + \\det(A) = 0$<br>
        $\\lambda^2 - {trace}\\lambda + {determinant} = 0$
        </p>
        <p>
        <strong>4. Discriminante:</strong><br>
        $\\Delta = \\text{{tr}}(A)^2 - 4\\det(A) = {trace}^2 - 4({determinant}) = {trace**2} - {4*determinant} = {discriminant}$
        </p>
        """
        
        if isinstance(lambda1, complex):
            retroalimentacion += f"""
            <p>
            <strong>5. Eigenvalores complejos:</strong><br>
            $\\lambda_{{1,2}} = \\frac{{\\text{{tr}}(A) \\pm \\sqrt{{\\Delta}}}}{{2}} = \\frac{{{trace} \\pm \\sqrt{{{discriminant}}}}}{{2}}$<br>
            $= \\frac{{{trace} \\pm j\\sqrt{{{abs(discriminant)}}}}}{{2}} = {lambda1.real:.6f} \\pm j{abs(lambda1.imag):.6f}$
            </p>
            <p>
            <strong>6. Comportamiento del sistema:</strong><br>
            Eigenvalores complejos indican comportamiento oscilatorio.<br>
            • Parte real < 0: Oscilaciones amortiguadas (espiral estable)<br>
            • Parte real > 0: Oscilaciones crecientes (espiral inestable)<br>
            • Parte real = 0: Oscilaciones constantes (centro)
            </p>
            """
        else:
            retroalimentacion += f"""
            <p>
            <strong>5. Eigenvalores reales:</strong><br>
            $\\lambda_1 = \\frac{{{trace} + \\sqrt{{{discriminant}}}}}{{2}} = {lambda1:.6f}$<br>
            $\\lambda_2 = \\frac{{{trace} - \\sqrt{{{discriminant}}}}}{{2}} = {lambda2:.6f}$
            </p>
            <p>
            <strong>6. Comportamiento del sistema:</strong><br>
            Eigenvalores reales indican comportamiento exponencial.<br>
            • Ambos < 0: Nodo estable<br>
            • Ambos > 0: Nodo inestable<br>
            • Signos opuestos: Punto de silla (inestable)
            </p>
            """
        
        retroalimentacion += f"""
        <p>
        <strong>7. Criterio de estabilidad:</strong><br>
        El sistema es estable si y solo si:<br>
        • $\\text{{tr}}(A) < 0$ y $\\det(A) > 0$<br>
        En este caso: $\\text{{tr}}(A) = {trace}$ {'< 0' if trace < 0 else '≥ 0'} y $\\det(A) = {determinant}$ {'> 0' if determinant > 0 else '≤ 0'}<br>
        Por lo tanto, el sistema es {'estable' if is_stable else 'inestable'}.
        </p>
        <p>
        <strong>Aplicaciones:</strong><br>
        • Modelos depredador-presa en ecología<br>
        • Análisis de circuitos acoplados<br>
        • Sistemas de control multivariable<br>
        • Dinámicas poblacionales<br>
        • Modelos económicos de interacción
        </p>
        """
    
    else:  # laplace_applications
        # Laplace transform application to solve ODEs
        # Simple second-order ODE with Laplace transforms
        a = rnd.randint(1, 3)
        b = rnd.randint(2, 5)
        
        # ODE: y'' + ay' + by = 0 with y(0) = y0, y'(0) = v0
        y0 = rnd.randint(1, 4)
        v0 = rnd.randint(0, 3)
        
        # Laplace transform: s²Y(s) - sy(0) - y'(0) + a(sY(s) - y(0)) + bY(s) = 0
        # (s² + as + b)Y(s) = sy(0) + y'(0) + ay(0) = sy0 + v0 + ay0
        numerator_coeff_s = y0
        numerator_coeff_const = v0 + a * y0
        
        # Characteristic polynomial: s² + as + b
        discriminant = a**2 - 4*b
        
        ejercicio = cabecera + f"""
        <p>
        Use la transformada de Laplace para resolver:
        </p>
        <p>
        $y'' + {a}y' + {b}y = 0$
        </p>
        <p>
        con condiciones iniciales: $y(0) = {y0}$, $y'(0) = {v0}$
        </p>
        <p>
        Determine:
        </p>
        <p>
        <strong>1. Coeficiente de s en el numerador:</strong> {me.NM(numerator_coeff_s, error=0.001)}
        </p>
        <p>
        <strong>2. Término constante en el numerador:</strong> {me.NM(numerator_coeff_const, error=0.001)}
        </p>
        <p>
        <strong>3. Discriminante del denominador:</strong> $\\Delta = $ {me.NM(discriminant, error=0.001)}
        </p>
        <p>
        <strong>4. Coeficiente de $s^2$ en denominador:</strong> {me.NM(1, error=0.001)}
        </p>
        <p>
        <strong>5. Coeficiente de $s$ en denominador:</strong> {me.NM(a, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución usando transformada de Laplace:</strong>
        </p>
        <p>
        <strong>1. Transformada de la ecuación:</strong><br>
        $\\mathcal{{L}}\\{{y''\\}} + {a}\\mathcal{{L}}\\{{y'\\}} + {b}\\mathcal{{L}}\\{{y\\}} = 0$<br>
        $[s^2Y(s) - sy(0) - y'(0)] + {a}[sY(s) - y(0)] + {b}Y(s) = 0$
        </p>
        <p>
        <strong>2. Sustitución de condiciones iniciales:</strong><br>
        $[s^2Y(s) - s({y0}) - {v0}] + {a}[sY(s) - {y0}] + {b}Y(s) = 0$<br>
        $s^2Y(s) - {y0}s - {v0} + {a}sY(s) - {a*y0} + {b}Y(s) = 0$
        </p>
        <p>
        <strong>3. Factorización:</strong><br>
        $(s^2 + {a}s + {b})Y(s) = {y0}s + {v0} + {a*y0}$<br>
        $(s^2 + {a}s + {b})Y(s) = {numerator_coeff_s}s + {numerator_coeff_const}$
        </p>
        <p>
        <strong>4. Función de transferencia:</strong><br>
        $Y(s) = \\frac{{{numerator_coeff_s}s + {numerator_coeff_const}}}{{s^2 + {a}s + {b}}}$
        </p>
        <p>
        <strong>5. Análisis del denominador:</strong><br>
        El polinomio característico es $s^2 + {a}s + {b}$<br>
        Discriminante: $\\Delta = {a}^2 - 4(1)({b}) = {a**2} - {4*b} = {discriminant}$
        </p>
        """
        
        if discriminant > 0:
            r1 = (-a + math.sqrt(discriminant)) / 2
            r2 = (-a - math.sqrt(discriminant)) / 2
            retroalimentacion += f"""
            <p>
            <strong>6. Caso: Δ > 0 (raíces reales distintas)</strong><br>
            $s_1 = \\frac{{-{a} + \\sqrt{{{discriminant}}}}}{{2}} = {r1:.6f}$<br>
            $s_2 = \\frac{{-{a} - \\sqrt{{{discriminant}}}}}{{2}} = {r2:.6f}$<br>
            Descomposición en fracciones parciales:<br>
            $Y(s) = \\frac{{A}}{{s - {r1:.3f}}} + \\frac{{B}}{{s - {r2:.3f}}}$<br>
            Transformada inversa: $y(t) = Ae^{{{r1:.3f}t}} + Be^{{{r2:.3f}t}}$
            </p>
            """
        elif discriminant == 0:
            r = -a / 2
            retroalimentacion += f"""
            <p>
            <strong>6. Caso: Δ = 0 (raíz real repetida)</strong><br>
            $s = \\frac{{-{a}}}{{2}} = {r}$ (multiplicidad 2)<br>
            $Y(s) = \\frac{{{numerator_coeff_s}s + {numerator_coeff_const}}}{{(s - {r})^2}}$<br>
            Transformada inversa: $y(t) = (At + B)e^{{{r}t}}$
            </p>
            """
        else:
            alpha = -a / 2
            beta = math.sqrt(abs(discriminant)) / 2
            retroalimentacion += f"""
            <p>
            <strong>6. Caso: Δ < 0 (raíces complejas)</strong><br>
            $s_{{1,2}} = \\frac{{-{a} \\pm j\\sqrt{{{abs(discriminant)}}}}}{{2}} = {alpha:.3f} \\pm j{beta:.3f}$<br>
            $Y(s) = \\frac{{{numerator_coeff_s}s + {numerator_coeff_const}}}{{(s + {-alpha:.3f})^2 + {beta:.3f}^2}}$<br>
            Transformada inversa: $y(t) = e^{{{alpha:.3f}t}}[A\\cos({beta:.3f}t) + B\\sin({beta:.3f}t)]$
            </p>
            """
        
        retroalimentacion += """
        <p>
        <strong>7. Ventajas del método de Laplace:</strong><br>
        • Convierte EDOs en ecuaciones algebraicas<br>
        • Incorpora automáticamente las condiciones iniciales<br>
        • Facilita el análisis de sistemas complejos<br>
        • Permite análisis en el dominio de la frecuencia
        </p>
        <p>
        <strong>Aplicaciones en ingeniería:</strong><br>
        • Análisis de circuitos eléctricos<br>
        • Sistemas de control automático<br>
        • Procesamiento de señales<br>
        • Análisis de vibraciones<br>
        • Modelado de sistemas dinámicos
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
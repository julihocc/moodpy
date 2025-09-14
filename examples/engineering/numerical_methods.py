"""
Numerical Methods Analysis

Subject Area: engineering

This module contains educational content generators for numerical analysis methods
including root finding, numerical integration, and iterative solution techniques.
"""

import moodpy as me
import numpy.random as rnd

label = "NUMERICAL_METHODS"
miCabecera = """
<h1> Métodos Numéricos </h1>
<h2> Análisis Numérico y Métodos Iterativos </h2>
"""

def newton_raphson_method(f, df, x0, tolerance=1e-6, max_iterations=10):
    """Perform Newton-Raphson method iterations."""
    iterations = []
    x = x0
    
    for i in range(max_iterations):
        fx = f(x)
        dfx = df(x)
        
        if abs(dfx) < 1e-12:  # Avoid division by zero
            break
            
        x_new = x - fx / dfx
        iterations.append({
            'iteration': i + 1,
            'x': x,
            'f_x': fx,
            'df_x': dfx,
            'x_new': x_new,
            'error': abs(x_new - x)
        })
        
        if abs(x_new - x) < tolerance:
            break
            
        x = x_new
    
    return iterations

def bisection_method(f, a, b, tolerance=1e-6, max_iterations=10):
    """Perform bisection method iterations."""
    iterations = []
    
    if f(a) * f(b) > 0:
        return iterations  # No root in interval
    
    for i in range(max_iterations):
        c = (a + b) / 2
        fc = f(c)
        fa = f(a)
        fb = f(b)
        
        iterations.append({
            'iteration': i + 1,
            'a': a,
            'b': b,
            'c': c,
            'f_a': fa,
            'f_b': fb,
            'f_c': fc,
            'interval_width': b - a
        })
        
        if abs(fc) < tolerance or (b - a) / 2 < tolerance:
            break
            
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    
    return iterations

def trapezoidal_rule(f, a, b, n):
    """Calculate numerical integration using trapezoidal rule."""
    h = (b - a) / n
    x_values = [a + i * h for i in range(n + 1)]
    y_values = [f(x) for x in x_values]
    
    # Trapezoidal rule: (h/2) * [f(x0) + 2*f(x1) + 2*f(x2) + ... + 2*f(xn-1) + f(xn)]
    integral = h / 2 * (y_values[0] + 2 * sum(y_values[1:-1]) + y_values[-1])
    
    return integral, x_values, y_values

def gen(impr, cabecera=""):
    """Generate numerical methods problem."""
    
    # Choose method type
    methods = ['newton_raphson', 'bisection', 'trapezoidal']
    method = rnd.choice(methods)
    
    if method == 'newton_raphson':
        # Generate a polynomial function
        # f(x) = ax^3 + bx^2 + cx + d
        a = rnd.choice([-2, -1, 1, 2])
        b = rnd.randint(-5, 5)
        c = rnd.randint(-10, 10)
        d = rnd.randint(-15, 15)
        
        def f(x):
            return a*x**3 + b*x**2 + c*x + d
        
        def df(x):  # Derivative
            return 3*a*x**2 + 2*b*x + c
        
        # Initial guess
        x0 = rnd.uniform(-3, 3)
        
        # Perform iterations
        iterations = newton_raphson_method(f, df, x0, tolerance=1e-4, max_iterations=5)
        
        if not iterations:
            iterations = [{'iteration': 1, 'x': x0, 'f_x': f(x0), 'df_x': df(x0), 'x_new': x0, 'error': 0}]
        
        final_result = iterations[-1]['x_new'] if iterations else x0
        
        # Format polynomial
        def format_polynomial():
            terms = []
            if a != 0:
                if a == 1:
                    terms.append("x^3")
                elif a == -1:
                    terms.append("-x^3")
                else:
                    terms.append(f"{a}x^3")
            if b != 0:
                if b > 0 and terms:
                    if b == 1:
                        terms.append("+x^2")
                    else:
                        terms.append(f"+{b}x^2")
                else:
                    if b == 1:
                        terms.append("x^2")
                    elif b == -1:
                        terms.append("-x^2")
                    else:
                        terms.append(f"{b}x^2")
            if c != 0:
                if c > 0 and terms:
                    if c == 1:
                        terms.append("+x")
                    else:
                        terms.append(f"+{c}x")
                else:
                    if c == 1:
                        terms.append("x")
                    elif c == -1:
                        terms.append("-x")
                    else:
                        terms.append(f"{c}x")
            if d != 0:
                if d > 0 and terms:
                    terms.append(f"+{d}")
                else:
                    terms.append(str(d))
            return "".join(terms) if terms else "0"
        
        polynomial = format_polynomial()
        
        ejercicio = cabecera + f"""
        <p>
        Use el método de Newton-Raphson para encontrar una raíz de la función:
        </p>
        <p>
        $$f(x) = {polynomial}$$
        </p>
        <p>
        <strong>Valor inicial:</strong> $x_0 = {x0:.4f}$
        </p>
        <p>
        Complete las siguientes iteraciones:
        </p>
        <p>
        <strong>Primera iteración ($x_1$):</strong> {me.NM(iterations[0]['x_new'], error=0.0001)}
        </p>
        {"<p><strong>Segunda iteración ($x_2$):</strong> " + str(me.NM(iterations[1]['x_new'], error=0.0001)) + "</p>" if len(iterations) > 1 else ""}
        {"<p><strong>Tercera iteración ($x_3$):</strong> " + str(me.NM(iterations[2]['x_new'], error=0.0001)) + "</p>" if len(iterations) > 2 else ""}
        <p>
        <strong>Raíz aproximada:</strong> {me.NM(final_result, error=0.0001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Método de Newton-Raphson:</strong>
        </p>
        <p>
        La fórmula iterativa es: $x_{{n+1}} = x_n - \\frac{{f(x_n)}}{{f'(x_n)}}$
        </p>
        <p>
        <strong>Derivada:</strong> $f'(x) = {3*a}x^2 + {2*b}x + {c}$
        </p>"""
        
        for i, iter_data in enumerate(iterations[:3]):
            retroalimentacion += f"""
        <p>
        <strong>Iteración {iter_data['iteration']}:</strong><br>
        $x_{i} = {iter_data['x']:.6f}$<br>
        $f(x_{i}) = {iter_data['f_x']:.6f}$<br>
        $f'(x_{i}) = {iter_data['df_x']:.6f}$<br>
        $x_{i+1} = {iter_data['x']:.6f} - \\frac{{{iter_data['f_x']:.6f}}}{{{iter_data['df_x']:.6f}}} = {iter_data['x_new']:.6f}$
        </p>"""
        
        retroalimentacion += f"""
        <p>
        <strong>Verificación:</strong> $f({final_result:.4f}) = {f(final_result):.6f}$ 
        (debería estar cerca de 0)
        </p>
        <p>
        <strong>Convergencia:</strong> El método de Newton-Raphson converge cuadráticamente 
        cuando la aproximación inicial está cerca de la raíz y $f'(x) \\neq 0$.
        </p>"""
    
    elif method == 'bisection':
        # Generate a function with a root in the interval
        # f(x) = ax^2 + bx + c
        a = rnd.choice([-2, -1, 1, 2])
        b = rnd.randint(-8, 8)
        c = rnd.randint(-10, 10)
        
        def f(x):
            return a*x**2 + b*x + c
        
        # Find an interval [a, b] where f(a) and f(b) have opposite signs
        left = -5
        right = 5
        while f(left) * f(right) > 0 and left < right - 0.1:
            left += 0.5
            right -= 0.5
        
        if f(left) * f(right) > 0:
            left, right = -2, 2  # Fallback interval
        
        iterations = bisection_method(f, left, right, tolerance=1e-4, max_iterations=5)
        
        if not iterations:
            iterations = [{'iteration': 1, 'a': left, 'b': right, 'c': (left+right)/2, 
                          'f_a': f(left), 'f_b': f(right), 'f_c': f((left+right)/2), 
                          'interval_width': right - left}]
        
        final_root = iterations[-1]['c'] if iterations else (left + right) / 2
        
        polynomial = f"{a}x^2 + {b}x + {c}" if b >= 0 else f"{a}x^2 - {abs(b)}x + {c}" if c >= 0 else f"{a}x^2 - {abs(b)}x - {abs(c)}"
        
        ejercicio = cabecera + f"""
        <p>
        Use el método de bisección para encontrar una raíz de la función:
        </p>
        <p>
        $$f(x) = {polynomial}$$
        </p>
        <p>
        <strong>Intervalo inicial:</strong> $[{left:.2f}, {right:.2f}]$
        </p>
        <p>
        Complete las siguientes iteraciones:
        </p>
        <p>
        <strong>Primera iteración:</strong> $c_1 = $ {me.NM(iterations[0]['c'], error=0.0001)}
        </p>
        {"<p><strong>Segunda iteración:</strong> $c_2 = $ " + str(me.NM(iterations[1]['c'], error=0.0001)) + "</p>" if len(iterations) > 1 else ""}
        {"<p><strong>Tercera iteración:</strong> $c_3 = $ " + str(me.NM(iterations[2]['c'], error=0.0001)) + "</p>" if len(iterations) > 2 else ""}
        <p>
        <strong>Raíz aproximada:</strong> {me.NM(final_root, error=0.0001)}
        </p>
        """
        
        retroalimentacion = """
        <p>
        <strong>Método de Bisección:</strong>
        </p>
        <p>
        El método se basa en el Teorema del Valor Intermedio. Si $f(a) \\cdot f(b) < 0$, 
        entonces existe una raíz en el intervalo $[a,b]$.
        </p>"""
        
        for i, iter_data in enumerate(iterations[:3]):
            retroalimentacion += f"""
        <p>
        <strong>Iteración {iter_data['iteration']}:</strong><br>
        Intervalo: $[{iter_data['a']:.4f}, {iter_data['b']:.4f}]$<br>
        Punto medio: $c = \\frac{{{iter_data['a']:.4f} + {iter_data['b']:.4f}}}{{2}} = {iter_data['c']:.4f}$<br>
        $f({iter_data['a']:.4f}) = {iter_data['f_a']:.4f}$<br>
        $f({iter_data['c']:.4f}) = {iter_data['f_c']:.4f}$<br>
        $f({iter_data['b']:.4f}) = {iter_data['f_b']:.4f}$<br>
        Ancho del intervalo: ${iter_data['interval_width']:.4f}$
        </p>"""
        
        retroalimentacion += f"""
        <p>
        <strong>Verificación:</strong> $f({final_root:.4f}) = {f(final_root):.6f}$
        </p>
        <p>
        <strong>Convergencia:</strong> El método de bisección converge linealmente 
        y siempre encuentra una raíz si existe en el intervalo inicial.
        </p>"""
    
    else:  # trapezoidal
        # Generate integration problem
        # f(x) = ax^2 + bx + c
        a = rnd.randint(1, 5)
        b = rnd.randint(-5, 5)
        c = rnd.randint(-10, 10)
        
        def f(x):
            return a*x**2 + b*x + c
        
        # Integration limits
        x_a = rnd.randint(-3, 0)
        x_b = rnd.randint(1, 4)
        
        # Number of intervals
        n = rnd.choice([4, 6, 8])
        
        integral_approx, x_values, y_values = trapezoidal_rule(f, x_a, x_b, n)
        
        # Exact integral for comparison
        def exact_integral(a_coeff, b_coeff, c_coeff, lower, upper):
            return (a_coeff/3)*(upper**3 - lower**3) + (b_coeff/2)*(upper**2 - lower**2) + c_coeff*(upper - lower)
        
        exact_value = exact_integral(a, b, c, x_a, x_b)
        error = abs(integral_approx - exact_value)
        
        polynomial = f"{a}x^2 + {b}x + {c}" if b >= 0 else f"{a}x^2 - {abs(b)}x + {c}" if c >= 0 else f"{a}x^2 - {abs(b)}x - {abs(c)}"
        
        ejercicio = cabecera + f"""
        <p>
        Use la regla del trapecio para aproximar la integral:
        </p>
        <p>
        $$\\int_{{{x_a}}}^{{{x_b}}} ({polynomial}) \\, dx$$
        </p>
        <p>
        <strong>Número de intervalos:</strong> $n = {n}$
        </p>
        <p>
        <strong>Paso:</strong> $h = \\frac{{{x_b} - ({x_a})}}{{{n}}} = $ {me.NM((x_b - x_a)/n, error=0.001)}
        </p>
        <p>
        <strong>Aproximación de la integral:</strong> {me.NM(integral_approx, error=0.001)}
        </p>
        <p>
        <strong>Valor exacto:</strong> {me.NM(exact_value, error=0.001)}
        </p>
        <p>
        <strong>Error absoluto:</strong> {me.NM(error, error=0.0001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Regla del Trapecio:</strong>
        </p>
        <p>
        La fórmula es: $\\int_a^b f(x)dx \\approx \\frac{{h}}{{2}}[f(x_0) + 2f(x_1) + 2f(x_2) + \\ldots + 2f(x_{{n-1}}) + f(x_n)]$
        </p>
        <p>
        <strong>Puntos de evaluación:</strong><br>
        $h = {(x_b - x_a)/n:.4f}$
        </p>"""
        
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            retroalimentacion += f"$x_{i} = {x:.4f}, \\quad f(x_{i}) = {y:.4f}$<br>"
        
        retroalimentacion += f"""
        <p>
        <strong>Cálculo:</strong><br>
        $I \\approx \\frac{{{(x_b - x_a)/n:.4f}}}{{2}}[{y_values[0]:.2f} + 2({sum(y_values[1:-1]):.2f}) + {y_values[-1]:.2f}]$<br>
        $I \\approx {integral_approx:.6f}$
        </p>
        <p>
        <strong>Integral exacta:</strong><br>
        $\\int ({polynomial}) dx = \\frac{{{a}}}{{3}}x^3 + \\frac{{{b}}}{{2}}x^2 + {c}x$<br>
        Evaluada en los límites: ${exact_value:.6f}$
        </p>
        <p>
        <strong>Error de truncamiento:</strong> El error en la regla del trapecio es 
        proporcional a $h^2$, donde $h$ es el tamaño del paso.
        </p>"""
    
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
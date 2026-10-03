"""
Inverse Laplace Transform Analysis

Migrated from legacy generator: 303-3 Transformada Inversa III-checkpoint.ipynb
Subject Area: engineering

This module contains educational content generators for inverse Laplace transforms,
differential equation solutions, and engineering system analysis.
"""

import moodpy as me
import numpy.random as rnd
import math

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

label = "INVERSE_LAPLACE_TRANSFORM"
miCabecera = """
<h1> Transformada Inversa de Laplace </h1>
<h2> Ecuaciones Diferenciales y Sistemas de Ingeniería </h2>
"""

def generate_exponential_sinusoidal():
    """Generate exponential-sinusoidal function for Laplace transform."""
    # Parameters for exp(bt) * (c1*cos(at) + c2*sin(at))
    b = rnd.choice([-3, -2, -1, 1, 2, 3])  # Exponential coefficient
    a = rnd.randint(2, 8)  # Frequency
    c1 = round(rnd.normal(0, 5), 1)  # Cosine coefficient
    c2 = round(rnd.normal(0, 5), 1)  # Sine coefficient
    
    # Ensure non-zero coefficients
    if abs(c1) < 0.1:
        c1 = rnd.choice([-2, -1, 1, 2])
    if abs(c2) < 0.1:
        c2 = rnd.choice([-2, -1, 1, 2])
    
    return a, b, c1, c2

def laplace_transform_exp_sinusoidal(a, b, c1, c2):
    """Calculate Laplace transform of exp(bt)(c1*cos(at) + c2*sin(at))."""
    # L{exp(bt)*cos(at)} = (s-b)/((s-b)^2 + a^2)
    # L{exp(bt)*sin(at)} = a/((s-b)^2 + a^2)
    
    # Numerator: c1*(s-b) + c2*a
    num_s_coeff = c1  # Coefficient of s
    num_const = -c1*b + c2*a  # Constant term
    
    # Denominator: (s-b)^2 + a^2 = s^2 - 2bs + b^2 + a^2
    den_s2_coeff = 1
    den_s_coeff = -2*b
    den_const = b**2 + a**2
    
    return (num_s_coeff, num_const), (den_s2_coeff, den_s_coeff, den_const)

def format_polynomial(coeffs, var='s'):
    """Format polynomial from coefficients."""
    if len(coeffs) == 2:  # Linear: as + b
        a, b = coeffs
        terms = []
        if a != 0:
            if a == 1:
                terms.append(var)
            elif a == -1:
                terms.append(f"-{var}")
            else:
                terms.append(f"{a}{var}")
        if b != 0:
            if b > 0 and terms:
                terms.append(f"+{b}")
            else:
                terms.append(str(b))
        return " ".join(terms) if terms else "0"
    
    elif len(coeffs) == 3:  # Quadratic: as^2 + bs + c
        a, b, c = coeffs
        terms = []
        if a != 0:
            if a == 1:
                terms.append(f"{var}^2")
            elif a == -1:
                terms.append(f"-{var}^2")
            else:
                terms.append(f"{a}{var}^2")
        if b != 0:
            if b > 0 and terms:
                if b == 1:
                    terms.append(f"+{var}")
                else:
                    terms.append(f"+{b}{var}")
            else:
                if b == -1:
                    terms.append(f"-{var}")
                else:
                    terms.append(f"{b}{var}")
        if c != 0:
            if c > 0 and terms:
                terms.append(f"+{c}")
            else:
                terms.append(str(c))
        return " ".join(terms) if terms else "0"
    
    return "polynomial"

def format_time_function(a, b, c1, c2):
    """Format the time domain function."""
    exp_part = f"e^{{{b}t}}" if b != 1 else "e^t"
    if b == -1:
        exp_part = "e^{-t}"
    elif b == 0:
        exp_part = ""
    
    trig_terms = []
    if c1 != 0:
        if c1 == 1:
            trig_terms.append(f"\\cos({a}t)")
        elif c1 == -1:
            trig_terms.append(f"-\\cos({a}t)")
        else:
            trig_terms.append(f"{c1}\\cos({a}t)")
    
    if c2 != 0:
        if c2 > 0 and trig_terms:
            if c2 == 1:
                trig_terms.append(f"+\\sin({a}t)")
            else:
                trig_terms.append(f"+{c2}\\sin({a}t)")
        else:
            if c2 == 1:
                trig_terms.append(f"\\sin({a}t)")
            elif c2 == -1:
                trig_terms.append(f"-\\sin({a}t)")
            else:
                trig_terms.append(f"{c2}\\sin({a}t)")
    
    trig_part = "".join(trig_terms)
    if not trig_part:
        trig_part = "1"
    
    if b == 0:
        return trig_part
    else:
        return f"({trig_part}){exp_part}"

def evaluate_function_at_point(a, b, c1, c2, t_val):
    """Evaluate f(t) = exp(bt)(c1*cos(at) + c2*sin(at)) at given point."""
    exp_part = math.exp(b * t_val)
    cos_part = c1 * math.cos(a * t_val)
    sin_part = c2 * math.sin(a * t_val)
    return exp_part * (cos_part + sin_part)

def gen(impr, cabecera=""):
    """Generate inverse Laplace transform problem."""
    
    # Generate function parameters
    a, b, c1, c2 = generate_exponential_sinusoidal()
    
    # Calculate Laplace transform
    (num_s_coeff, num_const), (den_s2_coeff, den_s_coeff, den_const) = laplace_transform_exp_sinusoidal(a, b, c1, c2)
    
    # Format polynomials
    numerator = format_polynomial([num_s_coeff, num_const])
    denominator = format_polynomial([den_s2_coeff, den_s_coeff, den_const])
    
    # Time domain function
    time_function = format_time_function(a, b, c1, c2)
    
    # Generate evaluation point
    t_points = [0, 0.5, 1, 1.5, 2, math.pi/4, math.pi/2]
    t_val = rnd.choice(t_points)
    if t_val == math.pi/4:
        t_display = "\\pi/4"
    elif t_val == math.pi/2:
        t_display = "\\pi/2"
    else:
        t_display = str(t_val)
    
    # Evaluate function at the point
    function_value = evaluate_function_at_point(a, b, c1, c2, t_val)
    
    ejercicio = cabecera + f"""
    <p>
    Encuentre la transformada inversa de Laplace $f(t)$ de la siguiente función $F(s)$:
    </p>
    <p>
    $$F(s) = \\frac{{{numerator}}}{{{denominator}}}$$
    </p>
    <p>
    Una vez encontrada $f(t)$, evalúe la función en el punto dado:
    </p>
    <p>
    <strong>Evalúe:</strong> $f({t_display}) = $ {me.NM(function_value, error=0.001)}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Solución paso a paso:</strong>
    </p>
    <p>
    <strong>1. Identificación del tipo de transformada:</strong><br>
    La función $F(s) = \\frac{{{numerator}}}{{{denominator}}}$ tiene la forma de una transformada 
    de funciones exponencial-sinusoidales.
    </p>
    <p>
    <strong>2. Forma estándar:</strong><br>
    Para funciones del tipo $e^{{bt}}(c_1\\cos(at) + c_2\\sin(at))$, la transformada de Laplace es:
    $$\\mathcal{{L}}\\{{e^{{bt}}\\cos(at)\\}} = \\frac{{s-b}}{{(s-b)^2 + a^2}}$$
    $$\\mathcal{{L}}\\{{e^{{bt}}\\sin(at)\\}} = \\frac{{a}}{{(s-b)^2 + a^2}}$$
    </p>
    <p>
    <strong>3. Parámetros identificados:</strong><br>
    • $a = {a}$ (frecuencia de las funciones trigonométricas)<br>
    • $b = {b}$ (coeficiente exponencial)<br>
    • $c_1 = {c1}$ (coeficiente del coseno)<br>
    • $c_2 = {c2}$ (coeficiente del seno)
    </p>
    <p>
    <strong>4. Transformada inversa:</strong><br>
    $$f(t) = {time_function}$$
    </p>
    <p>
    <strong>5. Evaluación en $t = {t_display}$:</strong><br>
    $f({t_display}) = {function_value:.6f}$
    </p>
    <p>
    <strong>Verificación de la forma:</strong><br>
    • El denominador $(s-b)^2 + a^2 = (s-{b})^2 + {a}^2 = {denominator}$<br>
    • El numerador combina los términos de coseno y seno: ${numerator}$<br>
    • La función resultante es una oscilación amortiguada/amplificada según el signo de $b$
    </p>
    <p>
    <strong>Interpretación física:</strong><br>
    {"Esta función representa un sistema oscilatorio amortiguado" if b < 0 else "Esta función representa un sistema oscilatorio con amplitud creciente" if b > 0 else "Esta función representa un sistema oscilatorio puro"}, 
    típico en circuitos RLC, sistemas mecánicos con resortes y amortiguadores, 
    o sistemas de control en ingeniería.
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
"""
Complex Number Analysis

Subject Area: engineering

This module contains educational content generators for complex number operations,
polar form conversions, and engineering applications of complex analysis.
"""

import moodpy as me
import numpy.random as rnd
import math
import cmath

label = "COMPLEX_NUMBER_ANALYSIS"
miCabecera = """
<h1> Análisis de Números Complejos </h1>
<h2> Forma Rectangular, Polar y Aplicaciones de Ingeniería </h2>
"""

def gen(impr, cabecera=""):
    """Generate complex number analysis problem."""
    
    # Generate two complex numbers for operations
    # First complex number in rectangular form
    a1 = rnd.randint(-10, 10)
    b1 = rnd.randint(-10, 10)
    if a1 == 0 and b1 == 0:
        a1, b1 = rnd.choice([1, -1]), rnd.choice([1, -1])
    
    # Second complex number in rectangular form
    a2 = rnd.randint(-8, 8)
    b2 = rnd.randint(-8, 8)
    if a2 == 0 and b2 == 0:
        a2, b2 = rnd.choice([1, -1]), rnd.choice([1, -1])
    
    z1 = complex(a1, b1)
    z2 = complex(a2, b2)
    
    # Calculate operations
    z_sum = z1 + z2
    z_product = z1 * z2
    z_quotient = z1 / z2 if z2 != 0 else complex(1, 0)
    
    # Polar form of z1
    r1 = abs(z1)
    theta1 = cmath.phase(z1)
    theta1_degrees = math.degrees(theta1)
    
    # Polar form of z2
    r2 = abs(z2)
    theta2 = cmath.phase(z2)
    
    # Complex conjugate
    z1_conjugate = z1.conjugate()
    
    def format_complex(z):
        """Format complex number for display."""
        real, imag = z.real, z.imag
        if abs(imag) < 1e-10:
            return f"{real:.3f}"
        elif abs(real) < 1e-10:
            if abs(imag - 1) < 1e-10:
                return "i"
            elif abs(imag + 1) < 1e-10:
                return "-i"
            else:
                return f"{imag:.3f}i"
        else:
            if imag > 0:
                if abs(imag - 1) < 1e-10:
                    return f"{real:.3f} + i"
                else:
                    return f"{real:.3f} + {imag:.3f}i"
            else:
                if abs(imag + 1) < 1e-10:
                    return f"{real:.3f} - i"
                else:
                    return f"{real:.3f} - {abs(imag):.3f}i"
    
    def format_complex_display(a, b):
        """Format complex number for problem display."""
        if b == 0:
            return str(a)
        elif a == 0:
            if b == 1:
                return "i"
            elif b == -1:
                return "-i"
            else:
                return f"{b}i"
        else:
            if b > 0:
                if b == 1:
                    return f"{a} + i"
                else:
                    return f"{a} + {b}i"
            else:
                if b == -1:
                    return f"{a} - i"
                else:
                    return f"{a} - {abs(b)}i"
    
    z1_display = format_complex_display(a1, b1)
    z2_display = format_complex_display(a2, b2)
    
    ejercicio = cabecera + f"""
    <p>
    Dados los números complejos:
    </p>
    <p>
    $z_1 = {z1_display}$ <br>
    $z_2 = {z2_display}$
    </p>
    <p>
    Calcule las siguientes operaciones y conversiones:
    </p>
    <p>
    <strong>1. Suma:</strong> $z_1 + z_2 = $ {me.NM(z_sum.real, error=0.001)} + {me.NM(z_sum.imag, error=0.001)}i
    </p>
    <p>
    <strong>2. Producto:</strong> $z_1 \\cdot z_2 = $ {me.NM(z_product.real, error=0.001)} + {me.NM(z_product.imag, error=0.001)}i
    </p>
    <p>
    <strong>3. Cociente:</strong> $\\frac{{z_1}}{{z_2}} = $ {me.NM(z_quotient.real, error=0.001)} + {me.NM(z_quotient.imag, error=0.001)}i
    </p>
    <p>
    <strong>4. Módulo de $z_1$:</strong> $|z_1| = $ {me.NM(r1, error=0.001)}
    </p>
    <p>
    <strong>5. Argumento de $z_1$ (en radianes):</strong> $\\arg(z_1) = $ {me.NM(theta1, error=0.001)}
    </p>
    <p>
    <strong>6. Argumento de $z_1$ (en grados):</strong> $\\arg(z_1) = $ {me.NM(theta1_degrees, error=0.1)}°
    </p>
    <p>
    <strong>7. Conjugado de $z_1$:</strong> $\\overline{{z_1}} = $ {me.NM(z1_conjugate.real, error=0.001)} + {me.NM(z1_conjugate.imag, error=0.001)}i
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Solución paso a paso:</strong>
    </p>
    <p>
    <strong>1. Suma de números complejos:</strong><br>
    $z_1 + z_2 = ({a1}) + ({b1})i + ({a2}) + ({b2})i$<br>
    $= ({a1} + {a2}) + ({b1} + {b2})i$<br>
    $= {format_complex(z_sum)}$
    </p>
    <p>
    <strong>2. Producto de números complejos:</strong><br>
    $z_1 \\cdot z_2 = ({a1} + {b1}i)({a2} + {b2}i)$<br>
    $= {a1} \\cdot {a2} + {a1} \\cdot {b2}i + {b1}i \\cdot {a2} + {b1}i \\cdot {b2}i$<br>
    $= {a1*a2} + {a1*b2}i + {b1*a2}i + {b1*b2}i^2$<br>
    $= {a1*a2} + {a1*b2}i + {b1*a2}i - {b1*b2}$ (ya que $i^2 = -1$)<br>
    $= ({a1*a2} - {b1*b2}) + ({a1*b2} + {b1*a2})i$<br>
    $= {format_complex(z_product)}$
    </p>
    <p>
    <strong>3. División de números complejos:</strong><br>
    $\\frac{{z_1}}{{z_2}} = \\frac{{{a1} + {b1}i}}{{{a2} + {b2}i}}$<br>
    Multiplicamos numerador y denominador por el conjugado del denominador:<br>
    $= \\frac{{({a1} + {b1}i)({a2} - {b2}i)}}{{({a2} + {b2}i)({a2} - {b2}i)}}$<br>
    $= \\frac{{{a1*a2 + b1*b2} + ({b1*a2 - a1*b2})i}}{{{a2**2 + b2**2}}}$<br>
    $= {format_complex(z_quotient)}$
    </p>
    <p>
    <strong>4. Módulo (magnitud):</strong><br>
    $|z_1| = \\sqrt{{a^2 + b^2}} = \\sqrt{{{a1}^2 + {b1}^2}} = \\sqrt{{{a1**2} + {b1**2}}} = {r1:.6f}$
    </p>
    <p>
    <strong>5. Argumento (ángulo):</strong><br>
    $\\arg(z_1) = \\arctan\\left(\\frac{{b}}{{a}}\\right) = \\arctan\\left(\\frac{{{b1}}}{{{a1}}}\\right)$<br>
    {"Considerando el cuadrante apropiado: " if a1 != 0 else ""}$\\theta = {theta1:.6f}$ radianes<br>
    En grados: $\\theta = {theta1_degrees:.2f}°$
    </p>
    <p>
    <strong>6. Forma polar de $z_1$:</strong><br>
    $z_1 = r(\\cos\\theta + i\\sin\\theta) = {r1:.3f}(\\cos({theta1_degrees:.1f}°) + i\\sin({theta1_degrees:.1f}°))$<br>
    $z_1 = {r1:.3f}e^{{i{theta1:.3f}}}$ (forma exponencial)
    </p>
    <p>
    <strong>7. Conjugado complejo:</strong><br>
    $\\overline{{z_1}} = {a1} - ({b1})i = {format_complex(z1_conjugate)}$<br>
    El conjugado se obtiene cambiando el signo de la parte imaginaria.
    </p>
    <p>
    <strong>Propiedades importantes:</strong><br>
    • $z_1 \\cdot \\overline{{z_1}} = |z_1|^2 = {r1**2:.3f}$<br>
    • $|z_1 \\cdot z_2| = |z_1| \\cdot |z_2| = {r1:.3f} \\cdot {r2:.3f} = {r1*r2:.3f}$<br>
    • $\\arg(z_1 \\cdot z_2) = \\arg(z_1) + \\arg(z_2) = {theta1:.3f} + {theta2:.3f} = {theta1+theta2:.3f}$ rad
    </p>
    <p>
    <strong>Aplicaciones en ingeniería:</strong><br>
    Los números complejos son fundamentales en análisis de circuitos AC, 
    procesamiento de señales, sistemas de control, y análisis de vibraciones. 
    La forma polar es especialmente útil para representar fasores en 
    análisis de corriente alterna.
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
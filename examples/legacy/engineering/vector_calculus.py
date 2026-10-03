"""
Vector Calculus Analysis

Subject Area: engineering

This module contains educational content generators for vector operations,
line integrals, surface integrals, and engineering applications of vector calculus.
"""

import moodpy as me
import numpy.random as rnd
import math

label = "VECTOR_CALCULUS"
miCabecera = """
<h1> Cálculo Vectorial </h1>
<h2> Operaciones Vectoriales y Aplicaciones de Ingeniería </h2>
"""

def gen(impr, cabecera=""):
    """Generate vector calculus problem."""
    
    # Choose problem type
    problem_types = ['dot_product', 'cross_product', 'line_integral', 'gradient']
    problem_type = rnd.choice(problem_types)
    
    if problem_type == 'dot_product':
        # Generate two 3D vectors
        v1 = [rnd.randint(-8, 8) for _ in range(3)]
        v2 = [rnd.randint(-8, 8) for _ in range(3)]
        
        # Ensure vectors are not zero
        if all(x == 0 for x in v1):
            v1[0] = rnd.choice([-1, 1])
        if all(x == 0 for x in v2):
            v2[0] = rnd.choice([-1, 1])
        
        # Calculate dot product
        dot_product = sum(v1[i] * v2[i] for i in range(3))
        
        # Calculate magnitudes
        magnitude_v1 = math.sqrt(sum(x**2 for x in v1))
        magnitude_v2 = math.sqrt(sum(x**2 for x in v2))
        
        # Calculate angle between vectors
        if magnitude_v1 * magnitude_v2 != 0:
            cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
            # Clamp to [-1, 1] to avoid floating point errors
            cos_theta = max(-1, min(1, cos_theta))
            angle_rad = math.acos(cos_theta)
            angle_deg = math.degrees(angle_rad)
        else:
            angle_rad = angle_deg = 0
        
        # Check if vectors are orthogonal
        is_orthogonal = abs(dot_product) < 1e-10
        
        def format_vector(v):
            return f"({v[0]}, {v[1]}, {v[2]})"
        
        ejercicio = cabecera + f"""
        <p>
        Dados los vectores:
        </p>
        <p>
        $\\vec{{v_1}} = {format_vector(v1)}$ <br>
        $\\vec{{v_2}} = {format_vector(v2)}$
        </p>
        <p>
        Calcule las siguientes operaciones vectoriales:
        </p>
        <p>
        <strong>1. Producto punto:</strong> $\\vec{{v_1}} \\cdot \\vec{{v_2}} = $ {me.NM(dot_product, error=0.001)}
        </p>
        <p>
        <strong>2. Magnitud de $\\vec{{v_1}}$:</strong> $|\\vec{{v_1}}| = $ {me.NM(magnitude_v1, error=0.001)}
        </p>
        <p>
        <strong>3. Magnitud de $\\vec{{v_2}}$:</strong> $|\\vec{{v_2}}| = $ {me.NM(magnitude_v2, error=0.001)}
        </p>
        <p>
        <strong>4. Ángulo entre vectores (radianes):</strong> $\\theta = $ {me.NM(angle_rad, error=0.001)}
        </p>
        <p>
        <strong>5. Ángulo entre vectores (grados):</strong> $\\theta = $ {me.NM(angle_deg, error=0.1)}°
        </p>
        <p>
        <strong>6. Los vectores son:</strong> {me.MC("ortogonales~paralelos~ninguno", correct="ortogonales" if is_orthogonal else "ninguno")}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución paso a paso:</strong>
        </p>
        <p>
        <strong>1. Producto punto (escalar):</strong><br>
        $\\vec{{v_1}} \\cdot \\vec{{v_2}} = v_{{1x}}v_{{2x}} + v_{{1y}}v_{{2y}} + v_{{1z}}v_{{2z}}$<br>
        $= ({v1[0]})({v2[0]}) + ({v1[1]})({v2[1]}) + ({v1[2]})({v2[2]})$<br>
        $= {v1[0]*v2[0]} + {v1[1]*v2[1]} + {v1[2]*v2[2]}$<br>
        $= {dot_product}$
        </p>
        <p>
        <strong>2. Magnitud de vectores:</strong><br>
        $|\\vec{{v_1}}| = \\sqrt{{v_{{1x}}^2 + v_{{1y}}^2 + v_{{1z}}^2}} = \\sqrt{{{v1[0]}^2 + {v1[1]}^2 + {v1[2]}^2}} = \\sqrt{{{sum(x**2 for x in v1)}}} = {magnitude_v1:.6f}$<br>
        $|\\vec{{v_2}}| = \\sqrt{{v_{{2x}}^2 + v_{{2y}}^2 + v_{{2z}}^2}} = \\sqrt{{{v2[0]}^2 + {v2[1]}^2 + {v2[2]}^2}} = \\sqrt{{{sum(x**2 for x in v2)}}} = {magnitude_v2:.6f}$
        </p>
        <p>
        <strong>3. Ángulo entre vectores:</strong><br>
        $\\cos(\\theta) = \\frac{{\\vec{{v_1}} \\cdot \\vec{{v_2}}}}{{|\\vec{{v_1}}||\\vec{{v_2}}|}} = \\frac{{{dot_product}}}{{{magnitude_v1:.6f} \\times {magnitude_v2:.6f}}} = {cos_theta:.6f}$<br>
        $\\theta = \\arccos({cos_theta:.6f}) = {angle_rad:.6f}$ radianes $= {angle_deg:.2f}°$
        </p>
        <p>
        <strong>4. Interpretación geométrica:</strong><br>
        • Si $\\vec{{v_1}} \\cdot \\vec{{v_2}} > 0$: Los vectores forman un ángulo agudo<br>
        • Si $\\vec{{v_1}} \\cdot \\vec{{v_2}} < 0$: Los vectores forman un ángulo obtuso<br>
        • Si $\\vec{{v_1}} \\cdot \\vec{{v_2}} = 0$: Los vectores son ortogonales (perpendiculares)
        </p>
        <p>
        <strong>En este caso:</strong> {"Los vectores son ortogonales" if is_orthogonal else f"Los vectores forman un ángulo de {angle_deg:.1f}°"}
        </p>
        <p>
        <strong>Aplicaciones en ingeniería:</strong><br>
        El producto punto se usa para calcular trabajo mecánico, proyecciones vectoriales,
        componentes de fuerzas, y determinar perpendicularidad en diseño estructural.
        </p>
        """
    
    elif problem_type == 'cross_product':
        # Generate two 3D vectors
        v1 = [rnd.randint(-6, 6) for _ in range(3)]
        v2 = [rnd.randint(-6, 6) for _ in range(3)]
        
        # Ensure vectors are not zero or parallel
        if all(x == 0 for x in v1):
            v1 = [1, 0, 0]
        if all(x == 0 for x in v2):
            v2 = [0, 1, 0]
        
        # Calculate cross product: v1 × v2
        cross_product = [
            v1[1]*v2[2] - v1[2]*v2[1],  # i component
            v1[2]*v2[0] - v1[0]*v2[2],  # j component
            v1[0]*v2[1] - v1[1]*v2[0]   # k component
        ]
        
        # Calculate magnitude of cross product
        cross_magnitude = math.sqrt(sum(x**2 for x in cross_product))
        
        # Calculate magnitudes of original vectors
        magnitude_v1 = math.sqrt(sum(x**2 for x in v1))
        magnitude_v2 = math.sqrt(sum(x**2 for x in v2))
        
        # Calculate area of parallelogram
        area_parallelogram = cross_magnitude
        
        def format_vector(v):
            return f"({v[0]}, {v[1]}, {v[2]})"
        
        ejercicio = cabecera + f"""
        <p>
        Dados los vectores:
        </p>
        <p>
        $\\vec{{v_1}} = {format_vector(v1)}$ <br>
        $\\vec{{v_2}} = {format_vector(v2)}$
        </p>
        <p>
        Calcule las siguientes operaciones:
        </p>
        <p>
        <strong>1. Producto cruz $\\vec{{v_1}} \\times \\vec{{v_2}}$:</strong><br>
        Componente i: {me.NM(cross_product[0], error=0.001)}<br>
        Componente j: {me.NM(cross_product[1], error=0.001)}<br>
        Componente k: {me.NM(cross_product[2], error=0.001)}
        </p>
        <p>
        <strong>2. Magnitud del producto cruz:</strong> $|\\vec{{v_1}} \\times \\vec{{v_2}}| = $ {me.NM(cross_magnitude, error=0.001)}
        </p>
        <p>
        <strong>3. Área del paralelogramo:</strong> {me.NM(area_parallelogram, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución paso a paso:</strong>
        </p>
        <p>
        <strong>1. Producto cruz usando determinante:</strong><br>
        $\\vec{{v_1}} \\times \\vec{{v_2}} = \\begin{{vmatrix}}
        \\vec{{i}} & \\vec{{j}} & \\vec{{k}} \\\\
        {v1[0]} & {v1[1]} & {v1[2]} \\\\
        {v2[0]} & {v2[1]} & {v2[2]}
        \\end{{vmatrix}}$
        </p>
        <p>
        <strong>Componente i:</strong> $({v1[1]})({v2[2]}) - ({v1[2]})({v2[1]}) = {v1[1]*v2[2]} - {v1[2]*v2[1]} = {cross_product[0]}$<br>
        <strong>Componente j:</strong> $-[({v1[0]})({v2[2]}) - ({v1[2]})({v2[0]})] = -[{v1[0]*v2[2]} - {v1[2]*v2[0]}] = {cross_product[1]}$<br>
        <strong>Componente k:</strong> $({v1[0]})({v2[1]}) - ({v1[1]})({v2[0]}) = {v1[0]*v2[1]} - {v1[1]*v2[0]} = {cross_product[2]}$
        </p>
        <p>
        <strong>Resultado:</strong> $\\vec{{v_1}} \\times \\vec{{v_2}} = {format_vector(cross_product)}$
        </p>
        <p>
        <strong>2. Magnitud:</strong><br>
        $|\\vec{{v_1}} \\times \\vec{{v_2}}| = \\sqrt{{{cross_product[0]}^2 + {cross_product[1]}^2 + {cross_product[2]}^2}} = \\sqrt{{{sum(x**2 for x in cross_product)}}} = {cross_magnitude:.6f}$
        </p>
        <p>
        <strong>3. Interpretación geométrica:</strong><br>
        • El producto cruz es perpendicular a ambos vectores originales<br>
        • Su magnitud representa el área del paralelogramo formado por los vectores<br>
        • La dirección sigue la regla de la mano derecha
        </p>
        <p>
        <strong>Verificación de perpendicularidad:</strong><br>
        $(\\vec{{v_1}} \\times \\vec{{v_2}}) \\cdot \\vec{{v_1}} = {sum(cross_product[i] * v1[i] for i in range(3))}$ (debe ser 0)<br>
        $(\\vec{{v_1}} \\times \\vec{{v_2}}) \\cdot \\vec{{v_2}} = {sum(cross_product[i] * v2[i] for i in range(3))}$ (debe ser 0)
        </p>
        <p>
        <strong>Aplicaciones en ingeniería:</strong><br>
        El producto cruz se usa para calcular momentos de fuerza, velocidad angular,
        campos magnéticos, y determinar direcciones perpendiculares en el espacio 3D.
        </p>
        """
    
    elif problem_type == 'line_integral':
        # Generate a simple vector field F = (P, Q) and a path
        # F(x,y) = (ax + by, cx + dy) along path r(t) = (t, t²) from t=0 to t=1
        a, b, c, d = [rnd.randint(-3, 3) for _ in range(4)]
        if a == b == c == d == 0:
            a, c = 1, 1
        
        # Path: r(t) = (t, t²), r'(t) = (1, 2t)
        # F(r(t)) = (at + bt², ct + dt²)
        # F·dr = (at + bt²)·1 + (ct + dt²)·2t = at + bt² + 2ct² + 2dt³
        
        # Integral from 0 to 1: ∫[at + bt² + 2ct² + 2dt³]dt
        # = [at²/2 + bt³/3 + 2ct³/3 + 2dt⁴/4] from 0 to 1
        # = a/2 + b/3 + 2c/3 + d/2
        
        line_integral = a/2 + b/3 + 2*c/3 + d/2
        
        def format_field_component(coeff, var):
            if coeff == 0:
                return "0"
            elif coeff == 1:
                return var
            elif coeff == -1:
                return f"-{var}"
            else:
                return f"{coeff}{var}"
        
        P = f"{format_field_component(a, 'x')} + {format_field_component(b, 'y')}" if b != 0 else format_field_component(a, 'x')
        Q = f"{format_field_component(c, 'x')} + {format_field_component(d, 'y')}" if d != 0 else format_field_component(c, 'x')
        
        ejercicio = cabecera + f"""
        <p>
        Calcule la integral de línea del campo vectorial:
        </p>
        <p>
        $\\vec{{F}}(x,y) = ({P}, {Q})$
        </p>
        <p>
        a lo largo de la curva $\\vec{{r}}(t) = (t, t^2)$ desde $t = 0$ hasta $t = 1$.
        </p>
        <p>
        <strong>Integral de línea:</strong> $\\int_C \\vec{{F}} \\cdot d\\vec{{r}} = $ {me.NM(line_integral, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución paso a paso:</strong>
        </p>
        <p>
        <strong>1. Parametrización de la curva:</strong><br>
        $\\vec{{r}}(t) = (t, t^2)$ para $t \\in [0, 1]$<br>
        $\\frac{{d\\vec{{r}}}}{{dt}} = (1, 2t)$<br>
        $d\\vec{{r}} = (1, 2t)dt$
        </p>
        <p>
        <strong>2. Campo vectorial en la curva:</strong><br>
        $\\vec{{F}}(\\vec{{r}}(t)) = \\vec{{F}}(t, t^2) = ({a}t + {b}t^2, {c}t + {d}t^2)$
        </p>
        <p>
        <strong>3. Producto punto:</strong><br>
        $\\vec{{F}} \\cdot d\\vec{{r}} = ({a}t + {b}t^2) \\cdot 1 + ({c}t + {d}t^2) \\cdot 2t$<br>
        $= {a}t + {b}t^2 + 2{c}t^2 + 2{d}t^3$<br>
        $= {a}t + {b + 2*c}t^2 + {2*d}t^3$
        </p>
        <p>
        <strong>4. Integración:</strong><br>
        $\\int_0^1 [{a}t + {b + 2*c}t^2 + {2*d}t^3] dt$<br>
        $= \\left[{a}\\frac{{t^2}}{{2}} + {b + 2*c}\\frac{{t^3}}{{3}} + {2*d}\\frac{{t^4}}{{4}}\\right]_0^1$<br>
        $= \\frac{{{a}}}{{2}} + \\frac{{{b + 2*c}}}{{3}} + \\frac{{{2*d}}}{{4}}$<br>
        $= {a/2} + {(b + 2*c)/3:.6f} + {d/2} = {line_integral:.6f}$
        </p>
        <p>
        <strong>Interpretación física:</strong><br>
        La integral de línea representa el trabajo realizado por el campo de fuerzas
        $\\vec{{F}}$ al mover una partícula a lo largo de la curva especificada.
        </p>
        <p>
        <strong>Aplicaciones en ingeniería:</strong><br>
        Las integrales de línea se usan para calcular trabajo en campos de fuerzas,
        circulación de fluidos, y potencial eléctrico en campos electromagnéticos.
        </p>
        """
    
    else:  # gradient
        # Generate a scalar function f(x,y) = ax² + bxy + cy²
        a, b, c = [rnd.randint(-5, 5) for _ in range(3)]
        if a == b == c == 0:
            a, c = 1, 1
        
        # Point of evaluation
        x0, y0 = rnd.randint(-3, 3), rnd.randint(-3, 3)
        
        # Gradient: ∇f = (∂f/∂x, ∂f/∂y) = (2ax + by, bx + 2cy)
        grad_x = 2*a*x0 + b*y0
        grad_y = b*x0 + 2*c*y0
        
        # Magnitude of gradient
        grad_magnitude = math.sqrt(grad_x**2 + grad_y**2)
        
        # Function value at point
        f_value = a*x0**2 + b*x0*y0 + c*y0**2
        
        # Direction of steepest ascent (unit vector)
        if grad_magnitude != 0:
            unit_x = grad_x / grad_magnitude
            unit_y = grad_y / grad_magnitude
        else:
            unit_x = unit_y = 0
        
        def format_function():
            terms = []
            if a != 0:
                if a == 1:
                    terms.append("x^2")
                elif a == -1:
                    terms.append("-x^2")
                else:
                    terms.append(f"{a}x^2")
            if b != 0:
                if b > 0 and terms:
                    if b == 1:
                        terms.append("+xy")
                    else:
                        terms.append(f"+{b}xy")
                else:
                    if b == 1:
                        terms.append("xy")
                    elif b == -1:
                        terms.append("-xy")
                    else:
                        terms.append(f"{b}xy")
            if c != 0:
                if c > 0 and terms:
                    if c == 1:
                        terms.append("+y^2")
                    else:
                        terms.append(f"+{c}y^2")
                else:
                    if c == 1:
                        terms.append("y^2")
                    elif c == -1:
                        terms.append("-y^2")
                    else:
                        terms.append(f"{c}y^2")
            return "".join(terms) if terms else "0"
        
        function_str = format_function()
        
        ejercicio = cabecera + f"""
        <p>
        Dada la función escalar:
        </p>
        <p>
        $f(x,y) = {function_str}$
        </p>
        <p>
        Calcule el gradiente en el punto $({x0}, {y0})$:
        </p>
        <p>
        <strong>1. Gradiente:</strong> $\\nabla f({x0}, {y0}) = $ ({me.NM(grad_x, error=0.001)}, {me.NM(grad_y, error=0.001)})
        </p>
        <p>
        <strong>2. Magnitud del gradiente:</strong> $|\\nabla f| = $ {me.NM(grad_magnitude, error=0.001)}
        </p>
        <p>
        <strong>3. Valor de la función:</strong> $f({x0}, {y0}) = $ {me.NM(f_value, error=0.001)}
        </p>
        <p>
        <strong>4. Dirección de máximo crecimiento (unitario):</strong> ({me.NM(unit_x, error=0.001)}, {me.NM(unit_y, error=0.001)})
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución paso a paso:</strong>
        </p>
        <p>
        <strong>1. Cálculo de derivadas parciales:</strong><br>
        $\\frac{{\\partial f}}{{\\partial x}} = \\frac{{\\partial}}{{\\partial x}}({function_str}) = {2*a}x + {b}y$<br>
        $\\frac{{\\partial f}}{{\\partial y}} = \\frac{{\\partial}}{{\\partial y}}({function_str}) = {b}x + {2*c}y$
        </p>
        <p>
        <strong>2. Evaluación en el punto ({x0}, {y0}):</strong><br>
        $\\frac{{\\partial f}}{{\\partial x}}({x0}, {y0}) = {2*a}({x0}) + {b}({y0}) = {2*a*x0} + {b*y0} = {grad_x}$<br>
        $\\frac{{\\partial f}}{{\\partial y}}({x0}, {y0}) = {b}({x0}) + {2*c}({y0}) = {b*x0} + {2*c*y0} = {grad_y}$
        </p>
        <p>
        <strong>3. Vector gradiente:</strong><br>
        $\\nabla f({x0}, {y0}) = ({grad_x}, {grad_y})$
        </p>
        <p>
        <strong>4. Magnitud:</strong><br>
        $|\\nabla f| = \\sqrt{{{grad_x}^2 + {grad_y}^2}} = \\sqrt{{{grad_x**2} + {grad_y**2}}} = {grad_magnitude:.6f}$
        </p>
        <p>
        <strong>5. Vector unitario (dirección de máximo crecimiento):</strong><br>
        $\\hat{{u}} = \\frac{{\\nabla f}}{{|\\nabla f|}} = \\frac{{({grad_x}, {grad_y})}}{{{grad_magnitude:.6f}}} = ({unit_x:.6f}, {unit_y:.6f})$
        </p>
        <p>
        <strong>Interpretación geométrica:</strong><br>
        • El gradiente apunta en la dirección de máximo crecimiento de la función<br>
        • Su magnitud indica qué tan rápido crece la función en esa dirección<br>
        • Es perpendicular a las curvas de nivel de la función
        </p>
        <p>
        <strong>Aplicaciones en ingeniería:</strong><br>
        El gradiente se usa en optimización, análisis de campos de temperatura,
        gradientes de presión en fluidos, y algoritmos de descenso del gradiente.
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
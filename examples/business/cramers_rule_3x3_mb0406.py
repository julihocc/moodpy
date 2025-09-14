"""
Business Mathematics - Cramer's Rule 3x3 Systems

Migrated from legacy generator: MB0406 Cramer 3x3-checkpoint.ipynb
Subject Area: business

This module contains educational content generators for MoodPy v3.0.0.
Educational focus: Complex linear systems in business optimization and resource allocation.
"""

import moodpy as me
import numpy as np

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

label = "MB0406_CRAMER_3x3"
miCabecera = """
<h1> Sistemas Lineales 3x3 - Regla de Cramer </h1>
<h2> Optimización de Recursos Empresariales </h2>
"""

def generate_3x3_system():
    """Generate a 3x3 linear system with unique solution."""
    max_attempts = 200
    
    for _ in range(max_attempts):
        # Generate coefficient matrix and constants
        c = np.random.randint(low=-5, high=6, size=12)
        c = c.reshape((3, 4))
        
        # Extract coefficient matrix and check determinant
        A = c[:, 0:3]  # 3x3 coefficient matrix
        b = c[:, 3]    # constants vector
        
        det_A = np.linalg.det(A)
        
        # Ensure system has unique solution (det != 0)
        if abs(det_A) >= 2:
            try:
                # Calculate solution
                solution = np.linalg.solve(A, b)
                x, y, z = solution
                
                # Prefer solutions that are reasonable for business contexts
                if (abs(x) < 50 and abs(y) < 50 and abs(z) < 50 and
                    abs(x - round(x, 1)) < 0.1 and 
                    abs(y - round(y, 1)) < 0.1 and 
                    abs(z - round(z, 1)) < 0.1):
                    return A, b, x, y, z, det_A
            except np.linalg.LinAlgError:
                continue
    
    # Fallback: simple system that definitely works
    A = np.array([[2, 1, 0], [1, 2, 1], [0, 1, 2]])
    b = np.array([3, 4, 3])
    solution = np.linalg.solve(A, b)
    x, y, z = solution
    det_A = np.linalg.det(A)
    
    return A, b, x, y, z, det_A

def gen(impr, cabecera=""):
    """Generate a 3x3 Cramer's rule problem with business context."""
    
    A, b, x, y, z, det_A = generate_3x3_system()
    
    data = {}
    for i in range(3):
        for j in range(3):
            data[f"a{i+1}{j+1}"] = int(A[i, j])
        data[f"b{i+1}"] = int(b[i])
    
    answers = {}
    answers["x"] = me.NM(x, error=0.01)
    answers["y"] = me.NM(y, error=0.01) 
    answers["z"] = me.NM(z, error=0.01)
    answers["det_A"] = me.NM(det_A, error=0.01)
    
    # Create business context narrative
    contexts = [
        ("productos", "líneas de producción", "recursos disponibles"),
        ("departamentos", "presupuestos asignados", "objetivos financieros"),
        ("proyectos", "equipos de trabajo", "metas de rentabilidad"),
        ("servicios", "centros de costo", "límites presupuestarios")
    ]
    
    context = contexts[np.random.randint(0, len(contexts))]
    tipo, organizacion, restriccion = context
    
    ejercicio = cabecera + f"""
    <p>
    Una empresa debe optimizar la asignación de recursos para tres {tipo}
    (A, B, C) considerando múltiples {restriccion}. El sistema de ecuaciones 
    que modela las restricciones es:
    </p>
    <p>
    {data["a11"]}A + {data["a12"]}B + {data["a13"]}C = {data["b1"]} <br>
    {data["a21"]}A + {data["a22"]}B + {data["a23"]}C = {data["b2"]} <br>
    {data["a31"]}A + {data["a32"]}B + {data["a33"]}C = {data["b3"]}
    </p>
    <p>
    Utilice la regla de Cramer para determinar la asignación óptima:
    </p>
    <p>
    Asignación para A: {answers["x"]} <br>
    Asignación para B: {answers["y"]} <br>
    Asignación para C: {answers["z"]}
    </p>
    <p>
    Determinante del sistema: {answers["det_A"]}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Solución usando la Regla de Cramer para sistemas 3×3:</strong>
    </p>
    <p>
    El determinante principal del sistema es: D = {det_A:.2f}
    </p>
    <p>
    Como D ≠ 0, el sistema tiene solución única.
    </p>
    <p>
    Aplicando la regla de Cramer:
    </p>
    <p>
    A = D_A/D = {x:.2f} <br>
    B = D_B/D = {y:.2f} <br>
    C = D_C/D = {z:.2f}
    </p>
    <p>
    <strong>Interpretación empresarial:</strong> La asignación óptima de recursos
    permite satisfacer todas las restricciones del sistema mientras maximiza
    la eficiencia operativa.
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
    
    me.quick(gen, label, 50, impr=False, cabecera=miCabecera)
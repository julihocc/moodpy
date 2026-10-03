"""
Business Mathematics - Cramer's Rule 2x2 Systems

Migrated from legacy generator: MB0405 Cramer 2x2-checkpoint.ipynb  
Subject Area: business

This module contains educational content generators for MoodPy v3.0.0.
Educational focus: Linear systems solving in business optimization contexts.
"""

import moodpy as me
import numpy as np

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

label = "MB0405_CRAMER_2x2"
miCabecera = """
<h1> Sistemas Lineales 2x2 - Regla de Cramer </h1>
<h2> Aplicaciones en Administración </h2>
"""

def generate_system():
    """Generate a 2x2 linear system with unique solution."""
    max_attempts = 100
    
    for _ in range(max_attempts):
        # Generate coefficient matrix and constants
        c = np.random.randint(low=-8, high=9, size=6)
        c = c.reshape((2, 3))
        
        # Extract coefficient matrix and check determinant
        A = c[:, 0:2]  # 2x2 coefficient matrix
        b = c[:, 2]    # constants vector
        
        det_A = np.linalg.det(A)
        
        # Ensure system has unique solution (det != 0)
        if abs(det_A) >= 1:
            # Calculate solution using Cramer's rule
            det_x = np.linalg.det(np.column_stack([b, A[:, 1]]))
            det_y = np.linalg.det(np.column_stack([A[:, 0], b]))
            
            x = det_x / det_A
            y = det_y / det_A
            
            # Prefer integer or half-integer solutions for educational clarity
            if abs(x - round(x, 1)) < 0.01 and abs(y - round(y, 1)) < 0.01:
                return A, b, x, y, det_A, det_x, det_y
    
    # Fallback: simple system that definitely works
    A = np.array([[2, 1], [1, 3]])
    b = np.array([7, 10])
    det_A = np.linalg.det(A)
    det_x = np.linalg.det(np.column_stack([b, A[:, 1]]))
    det_y = np.linalg.det(np.column_stack([A[:, 0], b]))
    x = det_x / det_A
    y = det_y / det_A
    
    return A, b, x, y, det_A, det_x, det_y

def gen(impr, cabecera=""):
    """Generate a Cramer's rule problem with business context."""
    
    A, b, x, y, det_A, det_x, det_y = generate_system()
    
    data = {}
    data["a11"] = int(A[0, 0])
    data["a12"] = int(A[0, 1])  
    data["b1"] = int(b[0])
    data["a21"] = int(A[1, 0])
    data["a22"] = int(A[1, 1])
    data["b2"] = int(b[1])
    
    answers = {}
    answers["x"] = me.NM(x, error=0.01)
    answers["y"] = me.NM(y, error=0.01)
    answers["det_A"] = me.NM(det_A, error=0.01)
    
    # Create business context narrative
    contexts = [
        ("productos", "ganancias", "unidades producidas", "utilidad total"),
        ("servicios", "ingresos", "clientes atendidos", "facturación total"), 
        ("inversiones", "rendimientos", "capital invertido", "retorno esperado"),
        ("recursos", "costos", "recursos utilizados", "costo total")
    ]
    
    context = contexts[np.random.randint(0, len(contexts))]
    tipo, resultado, variable, objetivo = context
    
    ejercicio = cabecera + f"""
    <p>
    Una empresa debe optimizar su producción de dos {tipo} (A y B) sujeta a restricciones de recursos.
    El sistema de ecuaciones que modela el problema es:
    </p>
    <p>
    {data["a11"]}A + {data["a12"]}B = {data["b1"]}
    </p>
    <p>
    {data["a21"]}A + {data["a22"]}B = {data["b2"]}
    </p>
    <p>
    Utilice la regla de Cramer para determinar las cantidades óptimas:
    </p>
    <p>
    Cantidad del producto A: {answers["x"]}
    </p>
    <p>
    Cantidad del producto B: {answers["y"]}
    </p>
    <p>
    Determinante del sistema: {answers["det_A"]}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Solución usando la Regla de Cramer:</strong>
    </p>
    <p>
    Para el sistema:
    </p>
    <p>
    {data["a11"]}A + {data["a12"]}B = {data["b1"]} <br>
    {data["a21"]}A + {data["a22"]}B = {data["b2"]}
    </p>
    <p>
    Determinante principal: D = {data["a11"]}×{data["a22"]} - {data["a12"]}×{data["a21"]} = {det_A:.0f}
    </p>
    <p>
    Determinante para A: D_A = {data["b1"]}×{data["a22"]} - {data["a12"]}×{data["b2"]} = {det_x:.0f}
    </p>
    <p>
    Determinante para B: D_B = {data["a11"]}×{data["b2"]} - {data["b1"]}×{data["a21"]} = {det_y:.0f}
    </p>
    <p>
    Por tanto: A = D_A/D = {x:.2f}, B = D_B/D = {y:.2f}
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
    
    me.quick(gen, label, 100, impr=False, cabecera=miCabecera)
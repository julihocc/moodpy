"""
Business Optimization - Profit Maximization

Created for MoodPy v3.0.0 - Management/Economics Applications
Subject Area: economics

This module contains educational content generators for profit maximization problems
using linear programming and optimization techniques.
"""

import moodpy as me
import numpy as np

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

label = "MAN_102_MAXIMIZAR_GANANCIA"
miCabecera = """
<h1> Maximización de Ganancias </h1>
<h2> Optimización Empresarial </h2>
"""

def generate_profit_problem():
    """Generate a profit maximization problem with constraints."""
    
    # Generate profit coefficients for two products
    profit_A = np.random.randint(15, 50)  # Profit per unit of product A
    profit_B = np.random.randint(10, 45)  # Profit per unit of product B
    
    # Generate resource constraints
    # Resource 1 (e.g., labor hours)
    resource1_A = np.random.randint(2, 8)  # Units of resource 1 per unit A
    resource1_B = np.random.randint(1, 6)  # Units of resource 1 per unit B
    resource1_limit = np.random.randint(80, 200)  # Total available resource 1
    
    # Resource 2 (e.g., raw materials)
    resource2_A = np.random.randint(1, 5)  # Units of resource 2 per unit A
    resource2_B = np.random.randint(2, 7)  # Units of resource 2 per unit B  
    resource2_limit = np.random.randint(70, 180)  # Total available resource 2
    
    # Calculate corner points of feasible region
    # Corner point 1: Origin (0, 0)
    corner1 = (0, 0)
    profit1 = 0
    
    # Corner point 2: Maximum A on resource 1 constraint
    max_A_res1 = resource1_limit / resource1_A
    corner2_A = min(max_A_res1, resource2_limit / resource2_A)
    corner2 = (corner2_A, 0)
    profit2 = profit_A * corner2_A
    
    # Corner point 3: Maximum B on resource constraints
    max_B_res1 = resource1_limit / resource1_B
    max_B_res2 = resource2_limit / resource2_B
    corner3_B = min(max_B_res1, max_B_res2)
    corner3 = (0, corner3_B)
    profit3 = profit_B * corner3_B
    
    # Corner point 4: Intersection of both constraints
    # Solve system: resource1_A*x + resource1_B*y = resource1_limit
    #               resource2_A*x + resource2_B*y = resource2_limit
    try:
        A_matrix = np.array([[resource1_A, resource1_B], 
                            [resource2_A, resource2_B]])
        b_vector = np.array([resource1_limit, resource2_limit])
        intersection = np.linalg.solve(A_matrix, b_vector)
        
        if intersection[0] >= 0 and intersection[1] >= 0:
            corner4 = tuple(intersection)
            profit4 = profit_A * intersection[0] + profit_B * intersection[1]
        else:
            corner4 = None
            profit4 = -np.inf
    except np.linalg.LinAlgError:
        corner4 = None
        profit4 = -np.inf
    
    # Find optimal solution
    profits = [profit1, profit2, profit3, profit4]
    corners = [corner1, corner2, corner3, corner4]
    
    valid_profits = [p for p in profits if p != -np.inf]
    
    if valid_profits:
        max_profit = max(valid_profits)
        optimal_idx = profits.index(max_profit)
        optimal_point = corners[optimal_idx]
    else:
        optimal_point = (0, 0)
        max_profit = 0
    
    return {
        'profit_A': profit_A,
        'profit_B': profit_B,
        'resource1_A': resource1_A,
        'resource1_B': resource1_B, 
        'resource1_limit': resource1_limit,
        'resource2_A': resource2_A,
        'resource2_B': resource2_B,
        'resource2_limit': resource2_limit,
        'optimal_A': optimal_point[0],
        'optimal_B': optimal_point[1],
        'max_profit': max_profit
    }

def gen(impr, cabecera=""):
    """Generate a profit maximization problem."""
    
    problem = generate_profit_problem()
    
    answers = {}
    answers["optimal_A"] = me.NM(problem['optimal_A'], error=0.01)
    answers["optimal_B"] = me.NM(problem['optimal_B'], error=0.01)
    answers["max_profit"] = me.NM(problem['max_profit'], error=0.01)
    
    # Generate business context
    products = [
        ("computadoras", "tablets"),
        ("sillas", "mesas"),
        ("camisas", "pantalones"),
        ("teléfonos", "auriculares"),
        ("pasteles", "galletas")
    ]
    
    resources = [
        ("horas de trabajo", "kg de material"),
        ("horas máquina", "metros de tela"),
        ("minutos de procesamiento", "unidades de componente"),
        ("horas de ensamble", "litros de material"),
        ("turnos de producción", "cajas de insumos")
    ]
    
    product_pair = products[np.random.randint(0, len(products))]
    resource_pair = resources[np.random.randint(0, len(resources))]
    
    ejercicio = cabecera + f"""
    <p>
    Una empresa manufactura dos productos: {product_pair[0]} (A) y {product_pair[1]} (B).
    Las ganancias por unidad son ${problem['profit_A']} para A y ${problem['profit_B']} para B.
    </p>
    <p>
    La empresa tiene las siguientes restricciones de recursos:
    </p>
    <p>
    • {resource_pair[0].title()}: {problem['resource1_A']}A + {problem['resource1_B']}B ≤ {problem['resource1_limit']}
    </p>
    <p>
    • {resource_pair[1].title()}: {problem['resource2_A']}A + {problem['resource2_B']}B ≤ {problem['resource2_limit']}
    </p>
    <p>
    Determine la combinación óptima de productos para maximizar las ganancias:
    </p>
    <p>
    Cantidad óptima de A: {answers["optimal_A"]} <br>
    Cantidad óptima de B: {answers["optimal_B"]} <br>
    Ganancia máxima: ${answers["max_profit"]}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Método de solución - Programación Lineal:</strong>
    </p>
    <p>
    Función objetivo: Maximizar Z = {problem['profit_A']}A + {problem['profit_B']}B
    </p>
    <p>
    Sujeto a:
    </p>
    <p>
    {problem['resource1_A']}A + {problem['resource1_B']}B ≤ {problem['resource1_limit']} <br>
    {problem['resource2_A']}A + {problem['resource2_B']}B ≤ {problem['resource2_limit']} <br>
    A ≥ 0, B ≥ 0
    </p>
    <p>
    <strong>Solución óptima:</strong>
    </p>
    <p>
    A* = {problem['optimal_A']:.2f} unidades <br>
    B* = {problem['optimal_B']:.2f} unidades <br>
    Ganancia máxima = ${problem['max_profit']:.2f}
    </p>
    <p>
    Esta solución se encuentra en un vértice de la región factible,
    según el teorema fundamental de la programación lineal.
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
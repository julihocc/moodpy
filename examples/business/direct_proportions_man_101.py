"""
Proporciones Directas - Management Mathematics

Migrated from legacy generator: 2019-2_MAN_MOODPY_101_PROPORCIONES-DIRECTAS.ipynb
Subject Area: business

This module contains educational content generators for MoodPy v3.0.0.
Educational focus: Direct proportions in business recipes and scaling problems.
"""

import moodpy as me
import numpy as np
from fractions import Fraction

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

label = "2019-2_MAN_MOODPY_101_PROPORCIONES-DIRECTAS"
miCabecera = """
<h1> Proporciones directas </h1>
"""

def gen_rational(min_val=1, max_val=10, denominator_max=5):
    """Generate a random rational number as a fraction."""
    numerator = np.random.randint(min_val, max_val + 1)
    denominator = np.random.randint(2, denominator_max + 1)
    return Fraction(numerator, denominator)

def gen(impr, cabecera=""): 
    """Generate a direct proportions problem for business/cooking context."""
    
    # Generate random rational numbers for recipe proportions
    harina = 0
    while harina == 0 or harina >= 4:        
        harina = gen_rational(1, 3, 3)
    
    leche = 0
    while leche == 0 or leche >= 4:        
        leche = gen_rational(1, 3, 3)
    
    # Generate multiplier for scaling up the recipe
    multiplier = np.random.randint(2, 8)
    x = multiplier * harina.denominator * leche.denominator
    x = Fraction(x, harina.denominator)  # Total flour amount
    
    # Calculate proportional amount of milk needed
    y = x * leche / harina
    y_decimal = float(y)
    
    data = {}
    data["harina"] = str(harina)
    data["leche"] = str(leche)
    data["total_harina"] = str(x)
    data["respuesta"] = me.NM(y_decimal, error=0.001)
    
    ejercicio = cabecera + f"""
    <p>
    En una receta de repostería, se necesita {data["harina"]} tazas de harina
    por cada {data["leche"]} tazas de leche.
    </p>
    <p>
    ¿Cuántas tazas de leche se requieren para {data["total_harina"]} tazas de harina?
    </p>
    <p>
    Ingrese su respuesta con aproximación a tres cifras significativas: {data["respuesta"]}
    </p>
    """
    
    retroalimentacion = f"""
    <p>
    <strong>Solución:</strong>
    </p>
    <p>
    Establecemos la proporción directa:
    </p>
    <p>
    {data["harina"]} tazas harina : {data["leche"]} tazas leche = {data["total_harina"]} tazas harina : x tazas leche
    </p>
    <p>
    Resolviendo la proporción:
    </p>
    <p>
    x = ({data["total_harina"]} × {data["leche"]}) ÷ {data["harina"]} = {y_decimal:.3f} tazas de leche
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
#!/usr/bin/env python3
"""
Supply/Demand Equilibrium Point Generator

Reconstructed from: library/2019-2_MAN_MOODPY/MOODPY MAN 101 PRECIO DE EQUILIBRIO.ipynb

This generator creates problems about finding equilibrium prices and quantities 
for supply and demand functions with parametric coefficients.

The mathematical model:
- Supply function: S(u) = p_s * u
- Demand function: D(u) = p_eq + p_d * (u - u_eq)
- Equilibrium occurs when S(u_eq) = D(u_eq)

Original Pattern Analysis:
- u_eq ~ Poisson(100) for realistic market quantities
- p_s ~ Uniform[1, 10] for supply slope
- p_d ~ Uniform[-10, -1] for demand slope (negative for downward slope)
- p_eq calculated to ensure equilibrium at u_eq
"""

import numpy as np
from scipy.stats import poisson
from tabulate import tabulate
import sys
import os

# Add parent directory to path to import MoodPy modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator import Generator
from cloze import Cloze


class EquilibriumPointGenerator(Generator):
    """Generator for supply/demand equilibrium point problems."""
    
    def __init__(self):
        super().__init__()
        self.set_lambdas()
        
    def set_lambdas(self):
        """Define parameter generation functions following original patterns."""
        self.lambdas = {
            # Equilibrium quantity from Poisson distribution (realistic market size)
            "u_eq": lambda k: int(poisson.rvs(100)),
            
            # Supply slope coefficient (positive)
            "p_s": lambda k: np.random.uniform(1, 10),
            
            # Demand slope coefficient (negative for downward slope)
            "p_d": lambda k: np.random.uniform(-10, -1),
            
            # Sample quantities for verification table
            "u1": lambda k: int(np.random.uniform(50, 150)),
            "u2": lambda k: int(np.random.uniform(50, 150)),
            "u3": lambda k: int(np.random.uniform(50, 150)),
            "u4": lambda k: int(np.random.uniform(50, 150)),
            "u5": lambda k: int(np.random.uniform(50, 150)),
        }
        
        # Requirements to ensure valid economic model
        self.requirements = [
            "d['u_eq'] > 50",  # Reasonable market size
            "d['u_eq'] < 200", # Not too large
            "d['p_s'] > 0",    # Upward sloping supply
            "d['p_d'] < 0",    # Downward sloping demand
            "d['u1'] != d['u2']",  # Distinct sample points
            "d['u2'] != d['u3']",
            "d['u3'] != d['u4']",
            "d['u4'] != d['u5']",
        ]
        
    def calculate_derived_parameters(self):
        """Calculate equilibrium price and other derived values."""
        if self.parameters is None:
            return
            
        d = self.parameters
        
        # Calculate equilibrium price: p_eq such that S(u_eq) = D(u_eq)
        # S(u_eq) = p_s * u_eq
        # D(u_eq) = p_eq + p_d * (u_eq - u_eq) = p_eq
        # Therefore: p_eq = p_s * u_eq
        d['p_eq'] = d['p_s'] * d['u_eq']
        
        # Calculate supply and demand values at sample points
        sample_points = ['u1', 'u2', 'u3', 'u4', 'u5']
        for u_key in sample_points:
            u_val = d[u_key]
            d[f's_{u_key}'] = d['p_s'] * u_val  # Supply function
            d[f'd_{u_key}'] = d['p_eq'] + d['p_d'] * (u_val - d['u_eq'])  # Demand function
            
    def generate_table_html(self):
        """Generate HTML table showing supply and demand at sample points."""
        if self.parameters is None:
            return ""
            
        d = self.parameters
        
        # Prepare table data
        table_data = [
            ["Cantidad (u)", "Oferta S(u)", "Demanda D(u)"]
        ]
        
        sample_points = ['u1', 'u2', 'u3', 'u4', 'u5']
        for u_key in sample_points:
            u_val = d[u_key]
            s_val = d[f's_{u_key}']
            d_val = d[f'd_{u_key}']
            table_data.append([
                f"{u_val}",
                f"${s_val:.2f}",
                f"${d_val:.2f}"
            ])
            
        # Convert to HTML table
        return tabulate(table_data, headers="firstrow", tablefmt="html")
        
    def set_exercise(self):
        """Generate the complete exercise text with mathematical problem."""
        if self.parameters is None:
            return
            
        self.calculate_derived_parameters()
        table_html = self.generate_table_html()
        
        d = self.parameters
        
        exercise_text = f"""
        <h1>Microeconomía</h1>
        <h2>Punto de Equilibrio</h2>
        
        <p>
        Una empresa ha determinado que las funciones de oferta y demanda para su producto son:
        </p>
        
        <ul>
        <li><strong>Función de Oferta:</strong> \\(S(u) = {d['p_s']:.2f} \\cdot u\\)</li>
        <li><strong>Función de Demanda:</strong> \\(D(u) = {d['p_eq']:.2f} + {d['p_d']:.2f} \\cdot (u - {d['u_eq']})\\)</li>
        </ul>
        
        <p>
        donde \\(u\\) representa la cantidad y los precios están en pesos mexicanos.
        </p>
        
        <h3>Pregunta</h3>
        <p>
        Determine el punto de equilibrio (cantidad y precio) donde la oferta iguala a la demanda.
        </p>
        
        <p>
        <strong>Cantidad de equilibrio:</strong> {{1:NM:={d['u_eq']}:{d['u_eq'] * 0.01}}} unidades<br>
        <strong>Precio de equilibrio:</strong> ${{1:NM:={d['p_eq']:.2f}:{d['p_eq'] * 0.01:.2f}}}
        </p>
        
        <h3>Verificación</h3>
        <p>
        Compruebe su respuesta evaluando las funciones en los siguientes puntos:
        </p>
        
        {table_html}
        
        <p>
        <em>Nota: En el equilibrio, S(u) = D(u). Las diferencias en otros puntos muestran 
        el exceso de oferta o demanda.</em>
        </p>
        """
        
        super().set_exercise(exercise_text)


def main():
    """Demonstration of the equilibrium point generator."""
    print("=== MoodPy v3.0.0 - Equilibrium Point Generator ===\n")
    
    # Create generator
    gen = EquilibriumPointGenerator()
    
    # Generate parameters
    print("Generating random parameters...")
    gen.reload_parameters()
    gen.test_parameters()
    
    if gen.parameters is None:
        print("ERROR: Could not generate valid parameters")
        return
        
    print("Parameters generated successfully!")
    print(f"- Equilibrium quantity: {gen.parameters['u_eq']} units")
    print(f"- Supply slope: {gen.parameters['p_s']:.3f}")
    print(f"- Demand slope: {gen.parameters['p_d']:.3f}")
    print(f"- Equilibrium price: ${gen.parameters['p_eq']:.2f}")
    
    # Generate exercise
    gen.set_exercise()
    print("\nGenerate exercise successful!")
    print("Preview (first 200 characters):")
    print(gen.exercise[:200] + "..." if len(gen.exercise) > 200 else gen.exercise)
    
    # Optional: Create XML export
    print("\n" + "="*60)
    print("Creating Moodle XML export...")
    
    cloze = Cloze()
    cloze.generator = gen
    cloze.set_info("MICROECONOMÍA", "MIC", "Punto de Equilibrio")
    
    # Generate 3 sample questions
    cloze.testing(n=3)
    print("Sample questions generated successfully!")
    print("Check TESTING-*.txt file for output")


if __name__ == "__main__":
    main()
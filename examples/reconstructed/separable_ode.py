#!/usr/bin/env python3
"""
Separable Ordinary Differential Equations Generator

Reconstructed from: library/2018-1 Ecuaciones Diferenciales/P101_edo_separable/

This generator creates problems about solving separable ODEs with initial conditions.
The general form is: dy/dx = f(x)/g(y) where f(x) and g(y) are separable functions.

Mathematical Pattern Analysis from XML:
- Form: dy/dx = (ax + b)/(cy + d) 
- Initial conditions: (x0, y0)
- Solution verification at test points
- Implicit solution: ∫g(y)dy = ∫f(x)dx + C

The reconstructed patterns show:
- Linear numerator: ax + b with random coefficients
- Linear denominator: cy + d with random coefficients  
- Random initial conditions
- Verification points for solution checking
"""

import numpy as np
import sys
import os

# Add src directory to path to import MoodPy modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from moodpy.generator import Generator
from moodpy.cloze import Cloze


class SeparableODEGenerator(Generator):
    """Generator for separable ordinary differential equation problems."""
    
    def __init__(self):
        super().__init__()
        self.set_lambdas()
        
    def set_lambdas(self):
        """Define parameter generation functions based on XML pattern analysis."""
        self.lambdas = {
            # Numerator coefficients: ax + b
            "a": lambda k: np.random.randint(1, 11),  # Coefficient of x
            "b": lambda k: np.random.randint(-10, 11),  # Constant term
            
            # Denominator coefficients: cy + d  
            "c": lambda k: np.random.randint(1, 17),  # Coefficient of y
            "d": lambda k: np.random.randint(-10, 11),  # Constant term
            
            # Initial conditions
            "x0": lambda k: np.random.randint(-10, 11),
            "y0": lambda k: np.random.randint(-10, 11),
            
            # Test points for verification
            "x_test1": lambda k: np.random.randint(-10, 11),
            "y_test1": lambda k: np.random.randint(-10, 11),
            "x_test2": lambda k: np.random.randint(-10, 11),
            "y_test2": lambda k: np.random.randint(-10, 11),
        }
        
        # Requirements for valid mathematical problem
        self.requirements = [
            "d['c'] != 0",  # Avoid division by zero in denominator
            "d['c'] * d['y0'] + d['d'] != 0",  # Denominator non-zero at initial condition
            "d['x0'] != d['x_test1']",  # Distinct test points
            "d['x0'] != d['x_test2']",
            "d['x_test1'] != d['x_test2']",
            "d['y0'] != d['y_test1']",
            "d['y0'] != d['y_test2']",
            "d['y_test1'] != d['y_test2']",
        ]
        
    def calculate_solution_constant(self) -> float:
        """Calculate the integration constant C from initial conditions."""
        if self.parameters is None:
            return 0.0
            
        d = self.parameters
        
        # For separable ODE dy/dx = (ax + b)/(cy + d)
        # Separating: (cy + d)dy = (ax + b)dx
        # Integrating: ∫(cy + d)dy = ∫(ax + b)dx + C
        # Left side: (c/2)y² + dy
        # Right side: (a/2)x² + bx + C
        
        # At initial condition (x0, y0):
        # (c/2)y0² + d*y0 = (a/2)x0² + b*x0 + C
        # Therefore: C = (c/2)y0² + d*y0 - (a/2)x0² - b*x0
        
        left_initial = (d['c']/2) * d['y0']**2 + d['d'] * d['y0']
        right_initial = (d['a']/2) * d['x0']**2 + d['b'] * d['x0']
        
        return left_initial - right_initial
        
    def evaluate_implicit_solution(self, x: float, y: float) -> float:
        """Evaluate the implicit solution g(x,y) = C at given point."""
        if self.parameters is None:
            return 0.0
            
        d = self.parameters
        
        # g(x,y) = (c/2)y² + dy - (a/2)x² - bx
        left_side = (d['c']/2) * y**2 + d['d'] * y
        right_side = (d['a']/2) * x**2 + d['b'] * x
        
        return left_side - right_side
        
    def format_numerator(self) -> str:
        """Format the numerator (ax + b) with proper signs."""
        if self.parameters is None:
            return "x"
            
        d = self.parameters
        
        if d['b'] == 0:
            return f"{d['a']} \\, x" if d['a'] != 1 else "x"
        elif d['b'] > 0:
            coeff = f"{d['a']} \\, " if d['a'] != 1 else ""
            return f"{coeff}x + {d['b']}"
        else:
            coeff = f"{d['a']} \\, " if d['a'] != 1 else ""
            return f"{coeff}x - {abs(d['b'])}"
            
    def format_denominator(self) -> str:
        """Format the denominator (cy + d) with proper signs."""
        if self.parameters is None:
            return "y"
            
        d = self.parameters
        
        if d['d'] == 0:
            return f"{d['c']} \\, y" if d['c'] != 1 else "y"
        elif d['d'] > 0:
            coeff = f"{d['c']} \\, " if d['c'] != 1 else ""
            return f"{coeff}y + {d['d']}"
        else:
            coeff = f"{d['c']} \\, " if d['c'] != 1 else ""
            return f"{coeff}y - {abs(d['d'])}"
    
    def set_exercise(self):
        """Generate the complete exercise text with mathematical problem."""
        if self.parameters is None:
            return
            
        d = self.parameters
        
        # Calculate solution constant and test values
        C = self.calculate_solution_constant()
        test1_value = self.evaluate_implicit_solution(d['x_test1'], d['y_test1'])
        test2_value = self.evaluate_implicit_solution(d['x_test2'], d['y_test2'])
        
        # Format equation components
        numerator = self.format_numerator()
        denominator = self.format_denominator()
        
        exercise_text = f"""
        <h1>Ecuaciones diferenciales ordinarias</h1>
        <h2>Caso separable</h2>
        
        <p>
        Encuentre la solución \\(g(x,y)={C:.0f}\\) de la siguiente ecuación diferencial separable:
        </p>
        
        <p>
        $$\\frac{{dy}}{{dx}} = \\frac{{{numerator}}}{{{denominator}}}$$
        </p>
        
        <p>
        con condición inicial \\(x_0={d['x0']}, y_0={d['y0']}\\).
        </p>
        
        <h3>Control</h3>
        <p>
        <em>Verifique su respuesta evaluando en los puntos dados:</em>
        </p>
        
        <ul>
        <li>\\(g({d['x_test1']}, {d['y_test1']}) = \\) {{1:NM:={test1_value:.1f}:{abs(test1_value) * 0.03:.2f}}}</li>
        <li>\\(g({d['x_test2']}, {d['y_test2']}) = \\) {{1:NM:={test2_value:.1f}:{abs(test2_value) * 0.03:.2f}}}</li>
        </ul>
        
        <h3>Método de solución</h3>
        <p>
        <em>Sugerencia: Separe variables e integre ambos lados.</em>
        </p>
        <ol>
        <li>Separe variables: \\(({denominator}) dy = ({numerator}) dx\\)</li>
        <li>Integre ambos lados</li>
        <li>Use la condición inicial para encontrar la constante</li>
        <li>Exprese como \\(g(x,y) = C\\)</li>
        </ol>
        """
        
        super().set_exercise(exercise_text)


def main():
    """Demonstration of the separable ODE generator."""
    print("=== MoodPy v3.0.0 - Separable ODE Generator ===\n")
    
    # Create generator
    gen = SeparableODEGenerator()
    
    # Generate parameters
    print("Generating random parameters...")
    gen.reload_parameters()
    gen.test_parameters()
    
    if gen.parameters is None:
        print("ERROR: Could not generate valid parameters")
        return
        
    print("Parameters generated successfully!")
    d = gen.parameters
    print(f"- ODE: dy/dx = ({d['a']}x + {d['b']})/({d['c']}y + {d['d']})")
    print(f"- Initial condition: ({d['x0']}, {d['y0']})")
    print(f"- Solution constant: {gen.calculate_solution_constant():.2f}")
    
    # Generate exercise
    gen.set_exercise()
    print("\nGenerate exercise successful!")
    print("Preview (first 300 characters):")
    print(gen.exercise[:300] + "..." if len(gen.exercise) > 300 else gen.exercise)
    
    # Optional: Create XML export
    print("\n" + "="*60)
    print("Creating Moodle XML export...")
    
    cloze = Cloze()
    cloze.generator = gen
    cloze.set_info("ECUACIONES DIFERENCIALES", "EDO", "Separable")
    
    # Generate 3 sample questions
    cloze.testing(n=3)
    print("Sample questions generated successfully!")
    print("Check TESTING-*.txt file for output")


if __name__ == "__main__":
    main()
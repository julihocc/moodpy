#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linear Equations Generator

This example demonstrates how to create parametric linear equation problems
using MoodPy. Students are asked to solve equations of the form ax + b = c.

Domain: Mathematics
Topic: Algebra - Linear Equations
Level: Basic
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import numpy as np
from moodpy import Generator, Cloze
from moodpy.tools import NM


def create_linear_equations_generator():
    """
    Create a generator for linear equation problems.
    
    Generates problems of the form: ax + b = c, solve for x
    Where x = (c - b) / a
    """
    gen = Generator()
    
    # Define parameter generation lambdas
    gen.lambdas = {
        "a": lambda k: np.random.choice([i for i in range(-10, 11) if i != 0]),  # coefficient (non-zero)
        "b": lambda k: np.random.randint(-20, 21),  # constant term
        "x": lambda k: np.random.randint(-10, 11)   # solution value
    }
    
    # Define derived calculations
    gen.derived = {
        "c": lambda d: d["a"] * d["x"] + d["b"]  # c = ax + b
    }
    
    # Add requirements to ensure reasonable problems
    gen.requirements = []  # No special requirements for this example
    
    return gen


def set_exercise_text(gen):
    """Set the exercise text with formatting."""
    
    # Construct the equation display
    # Handle signs for better readability
    a_val = gen.parameters["a"]
    b_val = gen.parameters["b"] 
    c_val = gen.parameters["c"]
    x_val = gen.parameters["x"]
    
    # Format the equation nicely
    if a_val == 1:
        a_str = ""
    elif a_val == -1:
        a_str = "-"
    else:
        a_str = str(a_val)
    
    if b_val >= 0:
        b_str = f" + {b_val}"
    else:
        b_str = f" - {abs(b_val)}"
    
    equation = f"{a_str}x{b_str} = {c_val}"
    
    # Create the exercise text
    exercise_text = f"""
    <p><strong>Solve for x:</strong></p>
    <p style="text-align: center; font-size: 1.2em; margin: 20px;">
        ${equation}$
    </p>
    <p>Enter your answer: {NM(x_val)}</p>
    """
    
    # Create feedback
    feedback_text = f"""
    <h3>Solution:</h3>
    <p>Starting with: ${equation}$</p>
    <p>Subtract {b_val} from both sides: ${a_str}x = {c_val - b_val}$</p>
    <p>Divide by {a_val}: $x = \\frac{{{c_val - b_val}}}{{{a_val}}} = {x_val}$</p>
    """
    
    gen.set_exercise(exercise_text)
    gen.set_feedback(feedback_text)


def main():
    """
    Main function to demonstrate the linear equations generator.
    """
    print("=== Linear Equations Generator Example ===\n")
    
    # Create generator
    gen = create_linear_equations_generator()
    
    # Generate parameters
    gen.reload_parameters()
    gen.calculate_derived()
    
    # Set exercise text  
    set_exercise_text(gen)
    
    # Display the generated question
    print("Generated Parameters:")
    for key, value in gen.parameters.items():
        print(f"  {key} = {value}")
    
    print(f"\nEquation: {gen.parameters['a']}x + {gen.parameters['b']} = {gen.parameters['c']}")
    print(f"Solution: x = {gen.parameters['x']}")
    
    # Create XML export
    print("\n=== Creating XML Export ===")
    
    cloze = Cloze()
    cloze.set_info("MATHEMATICS", "ALG101", "linear_equations")
    cloze.set_generator(gen)
    
    print(f"Output folder: {cloze.foldername}")
    print(f"Output file: {cloze.filename}")
    
    # Generate test questions
    print("\n=== Testing Mode (5 questions) ===")
    cloze.testing(n=5)
    
    # Generate XML file with 10 questions
    print("\n=== Generating XML (10 questions) ===")
    cloze.get_exercises(cuantos=10)
    
    print(f"XML file created: {cloze.path}")
    print("✅ Linear equations generator example completed!")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MoodPy Examples Demonstration

This script demonstrates the key features of MoodPy v3.0.0 for creating
parametric Moodle cloze-type questions across different domains.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
from moodpy import Generator, Cloze
from moodpy.tools import NM


def demo_basic_arithmetic():
    """Demonstrate basic arithmetic question generation."""
    print("1. Basic Arithmetic Generator")
    print("-" * 30)
    
    # Create generator
    gen = Generator()
    
    # Define parameters
    gen.lambdas = {
        "a": lambda k: np.random.randint(5, 25),
        "b": lambda k: np.random.randint(5, 25),
        "operation": lambda k: np.random.choice(["+", "-", "*"])
    }
    
    # Generate parameters
    gen.reload_parameters()
    
    # Calculate result based on operation
    a, b = gen.parameters["a"], gen.parameters["b"]
    op = gen.parameters["operation"]
    
    if op == "+":
        result = a + b
        op_name = "addition"
    elif op == "-":
        result = a - b
        op_name = "subtraction"
    else:  # multiplication
        result = a * b
        op_name = "multiplication"
    
    # Create exercise
    exercise_text = f"""
    <h3>Basic {op_name.title()}</h3>
    <p>Calculate the following:</p>
    <p style="text-align: center; font-size: 1.2em; margin: 20px;">
        <strong>{a} {op} {b} = ?</strong>
    </p>
    <p>Answer: {NM(result)}</p>
    """
    
    gen.set_exercise(exercise_text)
    
    # Display result
    print(f"Generated: {a} {op} {b} = {result}")
    print(f"Operation: {op_name}")
    print("✅ Basic arithmetic generator created")
    
    return gen


def demo_xml_export():
    """Demonstrate XML export functionality."""
    print("\n2. XML Export Demonstration")
    print("-" * 30)
    
    # Create a simple generator for export
    gen = Generator()
    gen.lambdas = {
        "x": lambda k: np.random.randint(10, 100),
        "y": lambda k: np.random.randint(10, 100)
    }
    gen.reload_parameters()
    
    x, y = gen.parameters["x"], gen.parameters["y"]
    gen.set_exercise(f"What is {x} × {y}? Answer: {NM(x * y)}")
    
    # Create cloze instance
    cloze = Cloze()
    cloze.set_info("DEMO", "001", "showcase")
    cloze.set_generator(gen)
    
    print(f"Output folder: {cloze.foldername}")
    print(f"Output file: {cloze.filename}")
    
    # Generate test questions (commented out to avoid file creation in demo)
    print("Testing mode available: cloze.testing(n=3)")
    print("XML generation available: cloze.get_exercises(cuantos=5)")
    print("✅ XML export configured")


def demo_package_features():
    """Demonstrate key package features."""
    print("\n3. Package Features Overview")
    print("-" * 30)
    
    print("📦 MoodPy v3.0.0 Features:")
    print("  ✅ Modern Python packaging (src/ layout)")
    print("  ✅ Graceful dependency handling")
    print("  ✅ Comprehensive test suite")
    print("  ✅ Rich examples across domains")
    print("  ✅ Financial mathematics support")
    print("  ✅ Statistical generators")
    print("  ✅ LaTeX and HTML formatting")
    print("  ✅ XML export for Moodle")


def main():
    """Main demonstration function."""
    print("=" * 60)
    print("🎓 MoodPy v3.0.0 - Question Generator Demo")
    print("=" * 60)
    
    # Run demonstrations
    demo_basic_arithmetic()
    demo_xml_export()
    demo_package_features()
    
    print("\n" + "=" * 60)
    print("📚 Explore More Examples:")
    print("=" * 60)
    print("  🔹 examples/basic/arithmetic.py - Simple arithmetic")
    print("  🔹 examples/mathematics/linear_equations.py - Algebra")
    print("  🔹 examples/mathematics/statistics.py - Statistics")
    print("  🔹 examples/finance/compound_interest.py - Finance")
    print("  🔹 examples/README.md - Complete documentation")
    
    print("\n🚀 Ready for PyPI publication!")


if __name__ == "__main__":
    main()

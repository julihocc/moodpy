#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compound Interest Calculator Generator

This example demonstrates how to create parametric compound interest problems
using MoodPy. Students calculate final amount using the compound interest formula.

Domain: Finance
Topic: Compound Interest
Level: Intermediate
Formula: A = P(1 + r)^t
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import numpy as np
from moodpy import Generator, Cloze
from moodpy.tools import NM
from moodpy.matfin import frec, per, tempo


def create_compound_interest_generator():
    """
    Create a generator for compound interest problems.
    
    Uses the formula: A = P(1 + r)^t
    Where:
    - P = Principal amount
    - r = Annual interest rate (as decimal)
    - t = Time in years
    - A = Final amount
    """
    gen = Generator()
    
    # Define parameter generation lambdas
    gen.lambdas = {
        "P": lambda k: np.random.randint(1000, 50000),        # Principal ($1,000-$50,000)
        "r_percent": lambda k: np.random.uniform(3.0, 15.0), # Interest rate (3%-15%)
        "t": lambda k: np.random.randint(1, 20)              # Time (1-20 years)
    }
    
    # Define derived calculations
    gen.derived = {
        "r": lambda d: d["r_percent"] / 100.0,              # Convert percentage to decimal
        "A": lambda d: d["P"] * (1 + d["r"]) ** d["t"]      # Compound interest formula
    }
    
    # Add requirements for reasonable problems
    gen.requirements = []
    
    return gen


def set_exercise_text(gen):
    """Set the exercise text with formatting."""
    
    P = gen.parameters["P"]
    r_percent = gen.parameters["r_percent"]
    t = gen.parameters["t"]
    A = gen.parameters["A"]
    
    # Create the exercise text
    exercise_text = f"""
    <h3>Compound Interest Problem</h3>
    <p>Calculate the final amount for an investment using compound interest.</p>
    
    <div style="background-color: #f0f8ff; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50;">
        <p><strong>Given:</strong></p>
        <ul>
            <li>Principal amount (P): ${P:,.2f}</li>
            <li>Annual interest rate (r): {r_percent:.1f}%</li>
            <li>Time period (t): {t} years</li>
        </ul>
    </div>
    
    <p><strong>Formula:</strong> A = P(1 + r)^t</p>
    
    <p>What is the final amount after {t} years?</p>
    <p><strong>Answer:</strong> $ {NM(A, error=0.01)}</p>
    """
    
    # Create detailed feedback
    r_decimal = gen.parameters["r"]
    feedback_text = f"""
    <h3>Solution:</h3>
    
    <p><strong>Step 1:</strong> Identify the values</p>
    <ul>
        <li>P = ${P:,.2f}</li>
        <li>r = {r_percent:.1f}% = {r_decimal:.4f} (as decimal)</li>
        <li>t = {t} years</li>
    </ul>
    
    <p><strong>Step 2:</strong> Apply the compound interest formula</p>
    <p>A = P(1 + r)^t</p>
    <p>A = ${P:,.2f} × (1 + {r_decimal:.4f})^{t}</p>
    <p>A = ${P:,.2f} × (1.{int(r_decimal*10000):04d})^{t}</p>
    <p>A = ${P:,.2f} × {(1 + r_decimal)**t:.6f}</p>
    <p>A = ${A:,.2f}</p>
    
    <p><strong>Answer:</strong> The final amount after {t} years is <strong>${A:,.2f}</strong></p>
    """
    
    gen.set_exercise(exercise_text)
    gen.set_feedback(feedback_text)


def create_frequency_based_generator():
    """
    Create a more advanced generator with different compounding frequencies.
    """
    gen = Generator()
    
    # Define parameter generation lambdas
    gen.lambdas = {
        "P": lambda k: np.random.randint(5000, 100000),
        "r_percent": lambda k: np.random.uniform(2.5, 12.0),
        "t": lambda k: np.random.randint(2, 15),
        "freq_key": lambda k: np.random.choice(["mensual", "trimestral", "semestral", "anual"])
    }
    
    # Define derived calculations  
    gen.derived = {
        "r": lambda d: d["r_percent"] / 100.0,
        "n": lambda d: frec[d["freq_key"]],  # Compounding frequency per year
        "A": lambda d: d["P"] * (1 + d["r"]/d["n"]) ** (d["n"] * d["t"])
    }
    
    return gen


def main():
    """
    Main function to demonstrate the compound interest generator.
    """
    print("=== Compound Interest Generator Example ===\n")
    
    # Example 1: Basic compound interest
    print("1. Basic Compound Interest")
    print("-" * 30)
    
    gen1 = create_compound_interest_generator()
    gen1.reload_parameters()
    gen1.calculate_derived()
    set_exercise_text(gen1)
    
    print("Generated Parameters:")
    for key, value in gen1.parameters.items():
        if key == "A":
            print(f"  {key} = ${value:,.2f}")
        elif key == "P":
            print(f"  {key} = ${value:,.2f}")
        elif key == "r_percent":
            print(f"  {key} = {value:.1f}%")
        else:
            print(f"  {key} = {value}")
    
    # Example 2: Create XML export
    print(f"\n2. XML Export")
    print("-" * 30)
    
    cloze = Cloze()
    cloze.set_info("FINANCE", "FIN201", "compound_interest")
    cloze.set_generator(gen1)
    
    print(f"Output folder: {cloze.foldername}")
    print(f"Output file: {cloze.filename}")
    
    # Testing mode
    print(f"\n3. Testing Mode (3 questions)")
    print("-" * 30)
    cloze.testing(n=3)
    
    # Generate XML
    print(f"\n4. Generating XML (5 questions)")
    print("-" * 30)
    cloze.get_exercises(cuantos=5)
    
    print(f"XML file created: {cloze.path}")
    
    # Example 3: Advanced generator with frequencies
    print(f"\n5. Advanced: Different Compounding Frequencies")
    print("-" * 50)
    
    gen2 = create_frequency_based_generator()
    gen2.reload_parameters()
    gen2.calculate_derived()
    
    print("Advanced Parameters:")
    for key, value in gen2.parameters.items():
        if key in ["A", "P"]:
            print(f"  {key} = ${value:,.2f}")
        elif key == "r_percent":
            print(f"  {key} = {value:.1f}%")
        elif key == "freq_key":
            print(f"  {key} = {value} (n={frec[value]} times per year)")
        else:
            print(f"  {key} = {value}")
    
    print("✅ Compound interest generator example completed!")


if __name__ == "__main__":
    main()
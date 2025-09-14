#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic Arithmetic Example

A simple example demonstrating basic arithmetic question generation.
This example shows the fundamental MoodPy workflow:
1. Create a Generator
2. Define parameters with lambda functions  
3. Generate random values
4. Create exercise text
5. Export to Moodle XML

Educational Objective:
    Practice basic arithmetic operations with randomly generated numbers.
"""

import numpy as np
from moodpy import Generator, Cloze, tools


def create_addition_generator():
    """
    Create a generator for simple addition problems.
    
    Returns:
        Generator: Configured generator for addition exercises
    """
    gen = Generator()
    
    # Define random parameters
    gen.lambdas = {
        "a": lambda k: np.random.randint(1, 50),
        "b": lambda k: np.random.randint(1, 50)
    }
    
    # Generate values
    gen.reload_parameters()
    gen.test_parameters()
    
    # Calculate answer
    answer = gen.parameters['a'] + gen.parameters['b']
    
    # Create exercise text with Moodle numerical answer format
    exercise_text = f"""
    <p>Calculate the following sum:</p>
    <p><strong>{gen.parameters['a']} + {gen.parameters['b']} = </strong> {{1:NM:={answer}:0.1}}</p>
    """
    
    gen.set_exercise(exercise_text)
    
    # Optional feedback
    feedback_text = f"""
    <p><strong>Solution:</strong></p>
    <p>{gen.parameters['a']} + {gen.parameters['b']} = {answer}</p>
    """
    gen.set_feedback(feedback_text)
    
    return gen


def create_multiplication_generator():
    """
    Create a generator for multiplication problems.
    
    Returns:
        Generator: Configured generator for multiplication exercises
    """
    gen = Generator()
    
    # Define random parameters with constraints
    gen.lambdas = {
        "a": lambda k: np.random.randint(2, 12),  # Multiplication tables 2-12
        "b": lambda k: np.random.randint(2, 12)
    }
    
    # Add requirement that numbers are different
    gen.requirements = ["d['a'] != d['b']"]
    
    # Generate values
    gen.reload_parameters()
    gen.test_parameters()
    
    # Calculate answer
    answer = gen.parameters['a'] * gen.parameters['b']
    
    # Create exercise text
    exercise_text = f"""
    <p>Calculate the following product:</p>
    <p><strong>{gen.parameters['a']} × {gen.parameters['b']} = </strong> {{1:NM:={answer}:0}}</p>
    """
    
    gen.set_exercise(exercise_text)
    
    return gen


def demo_basic_arithmetic():
    """
    Demonstrate basic arithmetic question generation.
    
    This function shows how to:
    - Create generators for different operations
    - Use Cloze to export multiple questions
    - Organize output files
    """
    print("=== MoodPy Basic Arithmetic Demo ===\n")
    
    # Create addition questions
    print("Generating addition questions...")
    cloze_add = Cloze()
    cloze_add.set_info("MATH", "101", "addition")
    
    for i in range(3):
        gen = create_addition_generator()
        cloze_add.generator = gen
        print(f"Addition {i+1}: {gen.parameters['a']} + {gen.parameters['b']} = {gen.parameters['a'] + gen.parameters['b']}")
    
    # Generate XML for addition
    cloze_add.get_exercises(cuantos=5)
    print(f"Addition XML saved to: {cloze_add.path}\n")
    
    # Create multiplication questions  
    print("Generating multiplication questions...")
    cloze_mult = Cloze()
    cloze_mult.set_info("MATH", "102", "multiplication")
    
    for i in range(3):
        gen = create_multiplication_generator()
        cloze_mult.generator = gen
        print(f"Multiplication {i+1}: {gen.parameters['a']} × {gen.parameters['b']} = {gen.parameters['a'] * gen.parameters['b']}")
    
    # Generate XML for multiplication
    cloze_mult.get_exercises(cuantos=5)
    print(f"Multiplication XML saved to: {cloze_mult.path}")


if __name__ == "__main__":
    demo_basic_arithmetic()
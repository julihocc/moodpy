#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linear Equations Generator — canonical showcase example

Generates parametric problems of the form: ax + b = c, solve for x.
Demonstrates Pattern B (exercise_fn) because NM() answer format must be
computed fresh each iteration from the current random parameters.

Run from repo root after `pip install -e .`:
    python examples/mathematics/linear_equations.py
"""

import numpy as np
from moodpy import Generator, Cloze
from moodpy.tools import NM


def make_generator():
    """Configure a Generator for ax + b = c problems."""
    gen = Generator()

    # Primary random parameters
    gen.lambdas = {
        "a": lambda k: np.random.choice([i for i in range(-10, 11) if i != 0]),
        "b": lambda k: np.random.randint(-20, 21),
        "x": lambda k: np.random.randint(-10, 11),
    }

    # c is derived: c = a*x + b
    gen.derived = {
        "c": lambda d: int(d["a"] * d["x"] + d["b"]),
    }

    # Keep only problems with a non-trivial solution
    gen.requirements = [
        lambda: gen.parameters["x"] != 0,
        lambda: gen.parameters["c"] != gen.parameters["b"],  # avoid trivial a=0 cases
    ]

    return gen


def build_exercise(gen):
    """Build one unique exercise from the current parameter values.

    Called by Cloze.get_exercises() after each reload_parameters() + calculate_derived().
    """
    a = gen.parameters["a"]
    b = gen.parameters["b"]
    c = gen.parameters["c"]
    x = gen.parameters["x"]

    # Pretty-print the equation
    a_str = "" if a == 1 else ("-" if a == -1 else str(a))
    b_str = f" + {b}" if b >= 0 else f" - {abs(b)}"
    equation = f"{a_str}x{b_str} = {c}"

    gen.set_exercise(
        f"<p><strong>Solve for x:</strong></p>"
        f"<p style='text-align:center; font-size:1.2em;'>${equation}$</p>"
        f"<p>Answer: {NM(x)}</p>"
    )
    gen.set_feedback(
        f"<h3>Solution</h3>"
        f"<p>From ${equation}$:</p>"
        f"<p>Subtract {b}: ${a_str}x = {c - b}$</p>"
        f"<p>Divide by {a}: $x = {x}$</p>"
    )


def main():
    print("=== Linear Equations Generator ===\n")

    gen = make_generator()

    cloze = Cloze()
    cloze.set_info("MATHEMATICS", "ALG101", "linear_equations")
    cloze.set_generator(gen)

    # Optional: preview a few exercises as text before committing to XML
    print("Preview (testing mode, 3 questions):")
    cloze.testing(n=3, exercise_fn=build_exercise)

    # Generate 10 unique randomized questions → XML file
    print("\nGenerating 10 exercises → XML:")
    cloze.get_exercises(cuantos=10, exercise_fn=build_exercise)
    print(f"XML saved: {cloze.path}")


if __name__ == "__main__":
    main()

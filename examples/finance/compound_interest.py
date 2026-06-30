#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compound Interest Generator

Generates parametric compound interest problems using A = P(1 + r)^t.
Demonstrates Pattern B (exercise_fn) with derived parameters — the answer A
must be computed fresh each question, so it cannot live in a static template.

Run from repo root after `pip install -e .`:
    python examples/finance/compound_interest.py
"""

import numpy as np
from moodpy import Generator, Cloze
from moodpy.tools import NM


def make_generator():
    gen = Generator()

    gen.lambdas = {
        "P": lambda k: int(np.random.randint(1000, 50000) / 100) * 100,  # round to hundreds
        "r_percent": lambda k: round(np.random.uniform(3.0, 15.0), 1),
        "t": lambda k: int(np.random.randint(1, 21)),
    }

    # Derived: compute r (decimal) and A (final amount) from primaries
    gen.derived = {
        "r": lambda d: round(d["r_percent"] / 100.0, 6),
        "A": lambda d: round(d["P"] * (1 + d["r"]) ** d["t"], 2),
    }

    gen.requirements = [
        lambda: gen.parameters["t"] >= 2,
        lambda: gen.parameters["A"] > gen.parameters["P"],  # sanity: positive rate
    ]

    return gen


def build_exercise(gen):
    """Build one compound interest question from current parameters."""
    P = gen.parameters["P"]
    r_pct = gen.parameters["r_percent"]
    t = gen.parameters["t"]
    r = gen.parameters["r"]
    A = gen.parameters["A"]

    gen.set_exercise(
        f"<h3>Compound Interest</h3>"
        f"<p>An investment of <strong>${P:,.2f}</strong> earns "
        f"<strong>{r_pct}% annual interest</strong> compounded annually.</p>"
        f"<p>What is the total amount after <strong>{t} years</strong>?</p>"
        f"<p>Formula: A = P(1 + r)^t</p>"
        f"<p>Answer: $ {NM(A, error=0.01)}</p>"
    )
    gen.set_feedback(
        f"<h3>Solution</h3>"
        f"<p>A = {P:,.2f} × (1 + {r:.4f})^{t}</p>"
        f"<p>A = {P:,.2f} × {(1 + r)**t:.6f}</p>"
        f"<p><strong>A = ${A:,.2f}</strong></p>"
    )


def main():
    print("=== Compound Interest Generator ===\n")

    gen = make_generator()

    cloze = Cloze()
    cloze.set_info("FINANCE", "FIN201", "compound_interest")
    cloze.set_generator(gen)

    print("Preview (3 questions, text mode):")
    cloze.testing(n=3, exercise_fn=build_exercise)

    print("\nGenerating 10 exercises → XML:")
    cloze.get_exercises(cuantos=10, exercise_fn=build_exercise)
    print(f"XML saved: {cloze.path}")


if __name__ == "__main__":
    main()

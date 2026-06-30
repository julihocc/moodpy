#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic Arithmetic Example

Demonstrates both template patterns for batch exercise generation:

Pattern A (string template): use {d[key]} placeholders — good for display-only values.
Pattern B (exercise_fn): pass a function to get_exercises() — required when NM() answers
depend on computed values (avoids Python format/Moodle brace collision).
"""

import numpy as np
from moodpy import Generator, Cloze
from moodpy.tools import NM


# ---------------------------------------------------------------------------
# Pattern A: String template (simple display, no NM() in template string)
# ---------------------------------------------------------------------------

def make_addition_generator():
    gen = Generator()
    gen.lambdas = {
        "a": lambda k: np.random.randint(1, 50),
        "b": lambda k: np.random.randint(1, 50),
    }
    gen.derived = {
        "answer": lambda d: int(d["a"] + d["b"]),
    }
    # Requirements are lambda functions — strings don't work
    gen.requirements = [
        lambda: gen.parameters["a"] != gen.parameters["b"],
    ]
    return gen


def demo_addition_template():
    """Pattern A: set_exercise() once with {d[key]} placeholders."""
    print("--- Pattern A: String template (addition) ---")

    gen = make_addition_generator()
    # One initial reload so set_exercise() has values to render the preview
    gen.reload_parameters()
    gen.calculate_derived()

    # Template uses {d[key]} — re-substituted each question in get_exercises()
    # NOTE: do NOT embed NM() calls in the template string; use Pattern B for that
    gen.set_exercise(
        "<p>Calculate: <strong>{d[a]} + {d[b]} = ?</strong></p>"
        "<p>Answer: {d[answer]}</p>"
    )

    cloze = Cloze()
    cloze.set_info("MATH", "101", "addition")
    cloze.set_generator(gen)
    cloze.get_exercises(cuantos=5)  # produces 5 DIFFERENT questions
    print(f"Saved: {cloze.path}\n")


# ---------------------------------------------------------------------------
# Pattern B: exercise_fn (required when NM() answers are in the exercise)
# ---------------------------------------------------------------------------

def make_multiplication_generator():
    gen = Generator()
    gen.lambdas = {
        "a": lambda k: np.random.randint(2, 13),
        "b": lambda k: np.random.randint(2, 13),
    }
    gen.requirements = [
        lambda: gen.parameters["a"] != gen.parameters["b"],
    ]
    return gen


def build_multiplication_exercise(gen):
    """Called by get_exercises() after each reload — builds a fresh unique question."""
    a = gen.parameters["a"]
    b = gen.parameters["b"]
    answer = a * b
    gen.set_exercise(
        f"<p>Calculate: <strong>{a} × {b} = </strong>{NM(answer, entero=True)}</p>"
    )
    gen.set_feedback(
        f"<p><strong>Solution:</strong> {a} × {b} = {answer}</p>"
    )


def demo_multiplication_fn():
    """Pattern B: exercise_fn passed to get_exercises()."""
    print("--- Pattern B: exercise_fn (multiplication with NM answers) ---")

    gen = make_multiplication_generator()

    cloze = Cloze()
    cloze.set_info("MATH", "102", "multiplication")
    cloze.set_generator(gen)
    # exercise_fn is called each iteration with freshly reloaded parameters
    cloze.get_exercises(cuantos=5, exercise_fn=build_multiplication_exercise)
    print(f"Saved: {cloze.path}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== MoodPy Basic Arithmetic Demo ===\n")
    demo_addition_template()
    demo_multiplication_fn()
    print("Done. Open the XML files in the generated folders and verify each question differs.")

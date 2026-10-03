"""Verified starting recipes; copy and adapt them to the educator's brief."""

from .bank import QuestionFamily
from .generator import Generator
from .tools import NM, STxt


def arithmetic_family(count=10):
    """Addition of distinct positive integers, with an exact answer."""

    def factory(rng):
        gen = Generator()
        gen.lambdas = {
            "a": lambda _: int(rng.integers(1, 100)),
            "b": lambda _: int(rng.integers(1, 100)),
        }
        gen.requirements = [lambda: gen.parameters["a"] != gen.parameters["b"]]
        gen.derived = {"answer": lambda d: d["a"] + d["b"]}
        return gen

    def render(gen):
        d = gen.parameters
        gen.set_exercise(
            "<p>{} + {} = {}</p>".format(d["a"], d["b"], NM(d["answer"], entero=True)),
            template=False,
        )
        gen.set_feedback(
            "<p>Add the two integers: {} + {} = {}.</p>".format(
                d["a"], d["b"], d["answer"]
            ),
            template=False,
        )

    return QuestionFamily(
        "addition",
        "Integer addition",
        "Mathematics/Arithmetic",
        count,
        factory,
        render,
        ("addition",),
    )


def linear_equations_family(count=10):
    """Solve ax+b=c with a nonzero coefficient and nonzero integer solution."""

    def factory(rng):
        gen = Generator()
        gen.lambdas = {
            "a": lambda _: int(rng.integers(-10, 11)),
            "b": lambda _: int(rng.integers(-20, 21)),
            "x": lambda _: int(rng.integers(-10, 11)),
        }
        gen.requirements = [
            lambda: gen.parameters["a"] != 0,
            lambda: gen.parameters["x"] != 0,
        ]
        gen.derived = {"c": lambda d: d["a"] * d["x"] + d["b"]}
        return gen

    def render(gen):
        d = gen.parameters
        equation = "{}x {} {} = {}".format(
            d["a"], "+" if d["b"] >= 0 else "-", abs(d["b"]), d["c"]
        )
        gen.set_exercise(
            "<p>Solve {}.</p><p>x = {}</p>".format(equation, NM(d["x"], entero=True)),
            template=False,
        )
        gen.set_feedback(
            "<p>Subtract {} and divide by {}: x = ({} - {}) / {} = {}.</p>".format(
                d["b"], d["a"], d["c"], d["b"], d["a"], d["x"]
            ),
            template=False,
        )

    return QuestionFamily(
        "linear",
        "Linear equation",
        "Mathematics/Algebra",
        count,
        factory,
        render,
        ("linear-equations",),
    )


def compound_interest_family(count=10):
    """Annual compounding, rounded to cents, with 0.1% relative tolerance."""

    def factory(rng):
        gen = Generator()
        gen.lambdas = {
            "P": lambda _: int(rng.integers(10, 501)) * 100,
            "rate_percent": lambda _: int(rng.integers(30, 151)) / 10,
            "years": lambda _: int(rng.integers(1, 21)),
        }
        gen.derived = {
            "rate": lambda d: d["rate_percent"] / 100,
            "amount": lambda d: round(d["P"] * (1 + d["rate"]) ** d["years"], 2),
        }
        gen.requirements = [lambda: gen.parameters["years"] >= 2]
        return gen

    def render(gen):
        d = gen.parameters
        gen.set_exercise(
            "<p>Invest ${:,.2f} at {}% annually, compounded once a year, for {} years.</p>"
            "<p>Find the final amount in dollars: {}</p>".format(
                d["P"], d["rate_percent"], d["years"], NM(d["amount"], error=0.001)
            ),
            template=False,
        )
        gen.set_feedback(
            "<p>A = P(1 + r)<sup>t</sup> = {}(1 + {})<sup>{}</sup> = ${:,.2f}.</p>".format(
                d["P"], d["rate"], d["years"], d["amount"]
            ),
            template=False,
        )

    return QuestionFamily(
        "compound",
        "Compound interest",
        "Finance/Compound interest",
        count,
        factory,
        render,
        ("annual-compounding",),
    )


def short_answer_family(count=10):
    """Classify an integer as positive, negative, or zero (case insensitive)."""

    def factory(rng):
        gen = Generator()
        gen.lambdas = {"n": lambda _: int(rng.integers(-1000, 1001))}
        gen.derived = {
            "answer": lambda d: (
                "positive" if d["n"] > 0 else "negative" if d["n"] < 0 else "zero"
            )
        }
        return gen

    def render(gen):
        d = gen.parameters
        gen.set_exercise(
            "<p>Classify {} as positive, negative, or zero: {}</p>".format(
                d["n"], STxt(d["answer"])
            ),
            template=False,
        )
        gen.set_feedback("<p>{} is {}.</p>".format(d["n"], d["answer"]), template=False)

    return QuestionFamily(
        "sign",
        "Integer sign",
        "Mathematics/Short answer",
        count,
        factory,
        render,
        ("integer-sign",),
    )

"""Calculate Moodle grading expectations from inputs, independently of XML answers."""

import argparse
import hashlib
import importlib.util
import json
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path


def core_answers(question):
    d, family = question["parameters"], question["family_id"]
    if family == "addition":
        return [dict(kind="numerical", answer=d["a"] + d["b"], tolerance=0)]
    if family == "linear":
        return [dict(kind="numerical", answer=(d["c"] - d["b"]) / d["a"], tolerance=0)]
    if family == "compound":
        amount = (
            Decimal(d["P"]) * (1 + Decimal(str(d["rate_percent"])) / 100) ** d["years"]
        )
        answer = float(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN))
        return [dict(kind="numerical", answer=answer, tolerance=abs(answer) * 0.001)]
    if family == "sign":
        return [
            dict(
                kind="shortanswer",
                answer=(
                    "positive" if d["n"] > 0 else "negative" if d["n"] < 0 else "zero"
                ),
                tolerance=None,
            )
        ]
    raise ValueError("missing core grading oracle for " + family)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", required=True, type=Path)
    parser.add_argument("--generator-tests", type=Path)
    args = parser.parse_args()
    manifest_bytes = (args.bank / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    oracle = None
    if args.generator_tests:
        spec = importlib.util.spec_from_file_location(
            "generator_grading_oracles", args.generator_tests / "test_recipes.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        oracle = module.expected_answers
    expectations = {}
    for question in manifest["questions"]:
        if oracle is None:
            fields = core_answers(question)
        else:
            values = oracle(question["family_id"], question["parameters"]["inputs"])
            fields = [
                (
                    dict(kind="shortanswer", answer=v, tolerance=None)
                    if isinstance(v, str)
                    else dict(
                        kind="numerical",
                        answer=float(v),
                        tolerance=0.00001 if abs(v) <= 1e-8 else abs(v) * 0.001,
                    )
                )
                for v in values
            ]
        expectations[question["id"]] = fields
    payload = dict(
        format="moodpy-moodle-expectations-v1",
        manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),
        questions=expectations,
    )
    (args.bank / "expectations.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(
        "Calculated independent grading expectations for {} questions.".format(
            len(expectations)
        )
    )


if __name__ == "__main__":
    main()

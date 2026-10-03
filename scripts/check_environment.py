#!/usr/bin/env python3
"""Check the installed MoodPy environment and supported core recipes."""

import argparse
import importlib
import json
import sys
from importlib import metadata
from pathlib import Path
from xml.etree import ElementTree


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-wheel", action="store_true", help="reject editable/source imports"
    )
    args = parser.parse_args()
    try:
        print("Python: {}".format(sys.version.split()[0]))
        for package in ("numpy", "scipy", "matplotlib", "tabulate"):
            importlib.import_module(package)
            print("{}: {}".format(package, metadata.version(package)))

        import moodpy
        from moodpy.recipes import (
            arithmetic_family,
            compound_interest_family,
            linear_equations_family,
            short_answer_family,
        )

        distribution = metadata.distribution("moodpy")
        if moodpy.__version__ != distribution.version:
            raise ValueError(
                "MoodPy runtime and installed distribution versions differ"
            )
        location = Path(moodpy.__file__).resolve()
        if args.require_wheel:
            direct_url = json.loads(distribution.read_text("direct_url.json") or "{}")
            source = Path(__file__).resolve().parents[1] / "src"
            if (
                direct_url.get("dir_info", {}).get("editable")
                or source in location.parents
            ):
                raise ValueError(
                    "Expected an installed wheel; MoodPy resolves to source"
                )
            installed = Path(distribution.locate_file("moodpy/__init__.py")).resolve()
            if location != installed:
                raise ValueError(
                    "MoodPy import differs from the installed distribution"
                )
        print("MoodPy: {} ({})".format(moodpy.__version__, location))

        bank = moodpy.build_bank(
            [
                factory(1)
                for factory in (
                    arithmetic_family,
                    linear_equations_family,
                    compound_interest_family,
                    short_answer_family,
                )
            ],
            title="Environment check",
            seed=42,
        )
        bank.validate().raise_for_errors()
        root = ElementTree.fromstring(bank.to_xml())
        if len(root.findall("question[@type='cloze']")) != 4:
            raise ValueError("Expected one question from each core recipe")
        print(
            "Core recipe generation, validation, and XML parsing: passed (4 questions)"
        )
        return 0
    except Exception as error:
        print("Environment check failed: {}".format(error), file=sys.stderr)
        print(
            "Install the matching package and its runtime dependencies in this environment.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())

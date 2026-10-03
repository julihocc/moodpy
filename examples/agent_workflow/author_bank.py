#!/usr/bin/env python3
"""Copy this CLI recipe, then adapt its families to the educator's brief.

Uses the installed MoodPy package. No repository-relative import or submodule
is required. --manifest restores counts and build settings during regeneration.
"""

import argparse
import json
from dataclasses import replace
from pathlib import Path

from moodpy import build_bank
from moodpy.recipes import (
    arithmetic_family,
    linear_equations_family,
    compound_interest_family,
    short_answer_family,
)


def make_families():
    # Add custom QuestionFamily instances here. Keep IDs stable across revisions.
    return [
        arithmetic_family(),
        linear_equations_family(),
        compound_interest_family(),
        short_answer_family(),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", type=Path, required=True)
    counts = parser.add_mutually_exclusive_group()
    counts.add_argument(
        "--samples", type=int, help="representative variants per family"
    )
    counts.add_argument(
        "--count", type=int, help="override variant counts for all families"
    )
    parser.add_argument(
        "--manifest", type=Path, help="restore an exported bank configuration"
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    title, seed, max_attempts = "Example course question bank", 42, 10000
    families = make_families()
    if args.manifest:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if manifest.get("format") != "moodpy-bank-v1":
            parser.error("manifest must be a MoodPy bank manifest")
        requested = {family["id"]: family["count"] for family in manifest["families"]}
        if set(requested) != {family.id for family in families}:
            parser.error("manifest family IDs must match the recipe")
        families = [replace(family, count=requested[family.id]) for family in families]
        title, seed = manifest["title"], manifest["seed"]
        max_attempts = manifest["max_attempts"]
    count = args.samples if args.samples is not None else args.count
    if count is not None:
        families = [replace(family, count=count) for family in families]
    if args.seed is not None:
        seed = args.seed
    bank = build_bank(families, title=title, seed=seed, max_attempts=max_attempts)
    source = Path(__file__).resolve()
    paths = bank.export_bundle(
        args.output,
        source_files=[source, source.with_name("brief.md")],
        overwrite=args.overwrite,
    )
    print("Generated {} questions; seed {}.".format(len(bank.questions), bank.seed))
    print("Teacher preview: {}".format(paths.preview))
    print("Moodle XML: {}".format(paths.xml))
    print("Reusable bundle: {}".format(paths.archive))
    print("Local validation passed. Live Moodle import has not been tested.")


if __name__ == "__main__":
    main()

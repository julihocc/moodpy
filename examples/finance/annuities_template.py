"""
Mate Financiera 203 Anualidades-checkpoint

Migrated from legacy generator: Mate Financiera 203 Anualidades-checkpoint.py
Subject Area: finance

This module contains educational content generators for MoodPy v3.0.0.
"""

import moodpy
from moodpy import Generator, Cloze
import numpy as np
import numpy.random as rnd

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass


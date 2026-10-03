"""
TEST MAN 102 MAXIMIZAR GANANCIA-checkpoint

Migrated from legacy generator: TEST MAN 102 MAXIMIZAR GANANCIA-checkpoint.py
Subject Area: economics

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


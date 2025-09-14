# -*- coding: utf-8 -*-
"""
MoodPy v3.0.0 - Python library for generating parametric Moodle cloze questions

This library provides tools for creating parametric exercises with mathematical
and financial content that can be exported to Moodle XML format.

Key Features:
    - Parametric exercise generation with lambda functions
    - Moodle XML export with proper formatting
    - Mathematical and financial content generators
    - Image integration with matplotlib support
    - Batch processing and file organization

Example:
    >>> from moodpy import Generator, Cloze
    >>> gen = Generator()
    >>> gen.lambdas = {"x": lambda k: np.random.randint(1, 10)}
    >>> gen.reload_parameters()
    >>> gen.set_exercise("What is 2 + {d[x]}?")
    >>> cloze = Cloze()
    >>> cloze.generator = gen
    >>> cloze.get_exercises(cuantos=5)
"""

import warnings

# Core imports
from .generator import Generator
from .cloze import Cloze
from . import tools
from . import matfin
from . import subjects

__version__ = "3.0.0"
__author__ = "Julio Cesar Hernandez Ochoa"
__email__ = "julihocc@gmail.com"
__license__ = "MIT"

# Version info tuple for programmatic access
VERSION = (3, 0, 0)

# Optional imports with graceful degradation
try:
    from . import graphics
    _HAS_GRAPHICS = True
except ImportError as e:
    graphics = None
    _HAS_GRAPHICS = False
    import warnings
    warnings.warn(
        f"Graphics module could not be imported: {e}. "
        "Install matplotlib for full graphics support.",
        ImportWarning
    )

# Public API
__all__ = [
    'Generator',
    'Cloze', 
    'tools',
    'matfin',
    'graphics',
    'subjects',
    '__version__',
    'VERSION'
]

def get_version():
    """Return the version string."""
    return __version__

def has_graphics():
    """Check if graphics module is available."""
    return _HAS_GRAPHICS
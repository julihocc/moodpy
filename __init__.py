# -*- coding: utf-8 -*-
"""
MoodPy - Python library for generating randomized Moodle cloze-type questions

This library provides tools for creating parametric exercises with mathematical
and financial content that can be exported to Moodle XML format.
"""

__version__ = "2.0.0"
__author__ = "Julio Cesar Hernandez Ochoa"
__email__ = "julihocc@gmail.com"
__license__ = "MIT"

# Core imports
from .generator import Generator
from .cloze import Cloze
from . import tools
from . import matfin

# Optional imports with graceful degradation
try:
    from . import graphics
except ImportError:
    graphics = None

__all__ = [
    'Generator',
    'Cloze', 
    'tools',
    'matfin',
    'graphics'
]
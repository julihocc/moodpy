"""
MoodPy Subjects Package

This package contains educational generators organized by subject area,
migrated from the legacy generators collection.

Subject Areas:
- economics: Management and economic equilibrium generators
- mathematics: Pure mathematics including differential equations
- finance: Financial mathematics and calculations  
- statistics: Probability and statistical analysis
- business: Business mathematics applications
"""

from . import economics
from . import mathematics  
from . import finance
from . import statistics
from . import business

__all__ = [
    'economics',
    'mathematics', 
    'finance',
    'statistics',
    'business'
]
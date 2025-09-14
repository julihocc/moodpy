#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test configuration for pytest.

This module provides common fixtures and configuration for the MoodPy test suite.
"""

import sys
import os
import pytest

# Add src to Python path for testing
test_dir = os.path.dirname(__file__)
src_dir = os.path.join(os.path.dirname(test_dir), 'src')
sys.path.insert(0, src_dir)

# Import dependencies for testing
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import matplotlib
    matplotlib.use('Agg')  # Set non-interactive backend first
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


@pytest.fixture
def sample_generator():
    """Provide a basic Generator instance for testing."""
    from moodpy import Generator
    gen = Generator()
    gen.lambdas = {
        "a": lambda k: 5,
        "b": lambda k: 10,
        "x": lambda k: np.random.randint(1, 20) if HAS_NUMPY else 15
    }
    gen.reload_parameters()
    return gen


@pytest.fixture
def sample_cloze():
    """Provide a basic Cloze instance for testing."""
    from moodpy import Cloze
    cloze = Cloze()
    cloze.set_info("TEST", "001", "sample")
    return cloze


# Skip markers for missing dependencies
skipif_no_numpy = pytest.mark.skipif(not HAS_NUMPY, reason="numpy not available")
skipif_no_matplotlib = pytest.mark.skipif(not HAS_MATPLOTLIB, reason="matplotlib not available")
skipif_no_tabulate = pytest.mark.skipif(not HAS_TABULATE, reason="tabulate not available")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Generator class functionality.

This module contains unit tests for the core Generator class,
testing parametric exercise generation, parameter validation,
and XML formatting capabilities.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch

# Import from the new package structure
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from moodpy import Generator


class TestGenerator:
    """Test cases for the Generator class."""
    
    def test_generator_initialization(self):
        """Test that Generator initializes correctly."""
        gen = Generator()
        
        assert gen.counter == 0
        assert gen.header == ""
        assert gen.lambdas == {}
        assert gen.parameters == {}
        assert gen.data == {}
        assert gen.exercise_text == ""
        assert gen.feedback_text is None
        assert gen.print is False
        assert gen.requirements == [True]
    
    def test_parameter_generation(self):
        """Test parameter generation with lambda functions."""
        gen = Generator()
        
        # Define simple lambda functions
        gen.lambdas = {
            "a": lambda k: 5,
            "b": lambda k: 10
        }
        
        # Generate parameters
        gen.reload_parameters()
        
        assert "a" in gen.parameters
        assert "b" in gen.parameters
        assert gen.parameters["a"] == 5
        assert gen.parameters["b"] == 10
    
    def test_parameter_validation_success(self):
        """Test successful parameter validation."""
        gen = Generator()
        
        gen.lambdas = {
            "x": lambda k: np.random.randint(1, 10)
        }
        gen.requirements = ["d['x'] > 0", "d['x'] < 10"]
        
        gen.reload_parameters()
        gen.test_parameters()
        
        assert gen.parameters is not None
        assert 0 < gen.parameters["x"] < 10
    
    def test_parameter_validation_failure(self):
        """Test parameter validation failure."""
        gen = Generator()
        
        gen.lambdas = {
            "x": lambda k: 5
        }
        # Impossible requirement
        gen.requirements = ["d['x'] > 10"]
        
        gen.reload_parameters()
        gen.test_parameters()
        
        assert gen.parameters is None
    
    def test_exercise_text_setting(self):
        """Test setting exercise text with parameter substitution."""
        gen = Generator()
        
        gen.parameters = {"a": 5, "b": 3}
        gen.data = gen.parameters
        
        exercise_text = "What is {d[a]} + {d[b]}?"
        gen.set_exercise(exercise_text)
        
        assert "What is 5 + 3?" in gen.exercise_text
    
    def test_feedback_setting(self):
        """Test setting feedback text."""
        gen = Generator()
        
        gen.parameters = {"a": 5, "b": 3}
        gen.data = gen.parameters
        
        feedback_text = "The answer is {d[a]} + {d[b]} = 8"
        gen.set_feedback(feedback_text)
        
        assert "The answer is 5 + 3 = 8" in gen.feedback_text
    
    def test_counter_setting(self):
        """Test setting counter value."""
        gen = Generator()
        
        gen.set_counter(42)
        
        assert gen.counter == 42
    
    def test_statement_generation_without_feedback(self):
        """Test XML statement generation without feedback."""
        gen = Generator()
        
        gen.exercise_text = "<p>Test question</p>"
        
        statement = gen.statement()
        
        assert "<questiontext format=\"html\">" in statement
        assert "<![CDATA[" in statement
        assert "<p>Test question</p>" in statement
        assert "<generalfeedback format=\"html\">" not in statement
    
    def test_statement_generation_with_feedback(self):
        """Test XML statement generation with feedback."""
        gen = Generator()
        
        gen.exercise_text = "<p>Test question</p>"
        gen.feedback_text = "<p>Test feedback</p>"
        
        statement = gen.statement()
        
        assert "<questiontext format=\"html\">" in statement
        assert "<generalfeedback format=\"html\">" in statement
        assert "<![CDATA[" in statement
        assert "<p>Test question</p>" in statement
        assert "<p>Test feedback</p>" in statement
    
    def test_print_args(self):
        """Test parameter printing functionality."""
        gen = Generator()
        
        gen.counter = 1
        gen.parameters = {"a": 5, "b": 3}
        
        args_text = gen.print_args()
        
        assert "Exercise 1" in args_text
        assert "key:\t a" in args_text
        assert "value: \t 5" in args_text
        assert "key:\t b" in args_text
        assert "value: \t 3" in args_text


if __name__ == "__main__":
    pytest.main([__file__])
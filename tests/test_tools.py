#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test tools module functionality.

This module contains unit tests for the tools utility functions,
testing random number generation, array manipulation, and Moodle formatting.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from moodpy.tools import NM, round_normal, int_normal, txt2arr
from moodpy.generator import cdata

# Test dependencies conditionally
numpy = pytest.importorskip("numpy", reason="numpy not available")


class TestToolsFunctions:
    """Test cases for tools utility functions."""
    
    def test_cdata_basic(self):
        """Test CDATA wrapper function."""
        text = "<p>Hello World</p>"
        result = cdata(text)
        
        assert result.startswith("<![CDATA[")
        assert result.endswith("]]>")
        assert "<p>Hello World</p>" in result
    
    def test_cdata_with_special_chars(self):
        """Test CDATA with special XML characters."""
        text = '<script>alert("test & stuff");</script>'
        result = cdata(text)
        
        assert result.startswith("<![CDATA[")
        assert result.endswith("]]>")
        assert '<script>alert("test & stuff");</script>' in result
    
    def test_cdata_empty_string(self):
        """Test CDATA with empty string."""
        result = cdata("")
        assert result == "<![CDATA[]]>"
    
    def test_nm_basic_float(self):
        """Test NM function with basic float."""
        result = NM(42.5)
        
        assert result.startswith("{1:NM:=")
        assert "42.5" in result
        assert result.endswith("}")
        # Should have tolerance
        assert ":" in result.split("=")[1]
    
    def test_nm_with_custom_error(self):
        """Test NM function with custom error tolerance."""
        result = NM(100.0, error=0.01)
        
        assert result.startswith("{1:NM:=")
        assert "100" in result
        assert "0.01" in result
        assert result.endswith("}")
    
    def test_nm_integer_mode(self):
        """Test NM function in integer mode."""
        result = NM(42, entero=True)
        
        assert result.startswith("{1:NM:=")
        assert "42" in result
        assert result.endswith("}")
        # Integer mode should not have decimal places
        assert "42.0" not in result or "42:" in result
    
    def test_nm_negative_number(self):
        """Test NM function with negative number."""
        result = NM(-15.5)
        
        assert result.startswith("{1:NM:=")
        assert "-15.5" in result
        assert result.endswith("}")
    
    def test_nm_zero(self):
        """Test NM function with zero."""
        result = NM(0)
        
        assert result.startswith("{1:NM:=")
        assert "0" in result
        assert result.endswith("}")
    
    def test_round_normal_basic(self):
        """Test round_normal function basic functionality."""
        # Test with reasonable parameters
        result = round_normal(50, 10, 0, 100, 2)
        
        assert isinstance(result, float)
        assert 0 <= result <= 100
        assert len(str(result).split('.')[1]) <= 2  # Max 2 decimal places
    
    def test_round_normal_bounds(self):
        """Test round_normal respects bounds."""
        # Generate multiple samples to test bounds
        for _ in range(10):
            result = round_normal(50, 5, 40, 60, 1)
            assert 40 <= result <= 60
    
    def test_round_normal_decimals(self):
        """Test round_normal decimal places."""
        result = round_normal(10, 2, 0, 20, 3)
        
        # Check decimal places
        decimal_places = len(str(result).split('.')[1]) if '.' in str(result) else 0
        assert decimal_places <= 3
    
    def test_int_normal_basic(self):
        """Test int_normal function basic functionality."""
        result = int_normal(50, 10, 0, 100)
        
        assert isinstance(result, int)
        assert 0 <= result <= 100
    
    def test_int_normal_bounds(self):
        """Test int_normal respects bounds."""
        # Generate multiple samples to test bounds
        for _ in range(10):
            result = int_normal(50, 5, 40, 60)
            assert 40 <= result <= 60
            assert isinstance(result, int)
    
    def test_txt2arr_basic_list(self):
        """Test txt2arr with basic list string."""
        result = txt2arr("[1, 2, 3, 4, 5]")
        
        assert isinstance(result, numpy.ndarray)
        numpy.testing.assert_array_equal(result, numpy.array([1, 2, 3, 4, 5]))
    
    def test_txt2arr_range(self):
        """Test txt2arr with range expression."""
        result = txt2arr("list(range(1, 6))")
        
        assert isinstance(result, numpy.ndarray)
        numpy.testing.assert_array_equal(result, numpy.array([1, 2, 3, 4, 5]))
    
    def test_txt2arr_numpy_arange(self):
        """Test txt2arr with numpy arange."""
        result = txt2arr("np.arange(0, 10, 2)")
        
        assert isinstance(result, numpy.ndarray)
        numpy.testing.assert_array_equal(result, numpy.array([0, 2, 4, 6, 8]))
    
    def test_txt2arr_numpy_linspace(self):
        """Test txt2arr with numpy linspace."""
        result = txt2arr("np.linspace(0, 1, 3)")
        
        assert isinstance(result, numpy.ndarray)
        numpy.testing.assert_array_almost_equal(result, numpy.array([0.0, 0.5, 1.0]))
    
    def test_txt2arr_invalid_expression(self):
        """Test txt2arr with invalid expression."""
        with pytest.raises((ValueError, NameError, SyntaxError)):
            txt2arr("invalid_expression_that_should_fail")
    
    def test_txt2arr_empty_list(self):
        """Test txt2arr with empty list."""
        result = txt2arr("[]")
        
        assert isinstance(result, numpy.ndarray)
        assert len(result) == 0
    
    def test_txt2arr_nested_operations(self):
        """Test txt2arr with nested operations."""
        result = txt2arr("[x**2 for x in range(1, 4)]")
        
        assert isinstance(result, numpy.ndarray)
        numpy.testing.assert_array_equal(result, numpy.array([1, 4, 9]))


class TestToolsIntegration:
    """Integration tests for tools functions."""
    
    def test_nm_in_cdata(self):
        """Test NM function output in CDATA context."""
        nm_result = NM(42.5, error=0.1)
        cdata_result = cdata(f"<p>Answer: {nm_result}</p>")
        
        assert "<![CDATA[" in cdata_result
        assert "{1:NM:=" in cdata_result
        assert "42.5" in cdata_result
        assert "]]>" in cdata_result
    
    def test_random_functions_reproducibility(self):
        """Test that random functions can be made reproducible."""
        # Set numpy random seed for reproducibility
        numpy.random.seed(42)
        result1 = round_normal(50, 10, 0, 100, 2)
        
        numpy.random.seed(42)
        result2 = round_normal(50, 10, 0, 100, 2)
        
        assert result1 == result2
    
    def test_txt2arr_with_random_operations(self):
        """Test txt2arr with random number operations."""
        # This should work with numpy random functions
        result = txt2arr("np.random.randint(1, 10, 5)")
        
        assert isinstance(result, numpy.ndarray)
        assert len(result) == 5
        assert all(1 <= x <= 10 for x in result)


if __name__ == "__main__":
    pytest.main([__file__])
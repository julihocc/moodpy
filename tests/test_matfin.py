#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test matfin module functionality.

This module contains unit tests for the financial mathematics functions,
testing cash flow generation, interest calculations, and table formatting.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from moodpy.matfin import frec, per, tempo, gen_flux

# Test dependencies conditionally
numpy = pytest.importorskip("numpy", reason="numpy not available")
tabulate_available = True
try:
    from tabulate import tabulate
except ImportError:
    tabulate_available = False


class TestMatfinConstants:
    """Test cases for matfin constants and dictionaries."""
    
    def test_frec_dictionary(self):
        """Test frequency dictionary completeness."""
        # Check that all expected keys exist
        expected_keys = ['diario', 'semanal', 'mensual', 'bimestral', 
                        'trimestral', 'semestral', 'anual']
        
        for key in expected_keys:
            assert key in frec, f"Missing key '{key}' in frec dictionary"
        
        # Check that values are reasonable
        assert frec['diario'] == 365
        assert frec['mensual'] == 12
        assert frec['anual'] == 1
    
    def test_per_dictionary(self):
        """Test period dictionary completeness."""
        # Check that all expected keys exist
        expected_keys = ['dia', 'semana', 'mes', 'bimestre', 
                        'trimestre', 'semestre', 'año']
        
        for key in expected_keys:
            assert key in per, f"Missing key '{key}' in per dictionary"
        
        # Check that values are reasonable fractions
        assert per['año'] == 1.0
        assert per['mes'] == 1.0/12
        assert per['dia'] == 1.0/365
    
    def test_tempo_dictionary(self):
        """Test tempo dictionary completeness."""
        # Check that all expected keys exist
        expected_keys = ['dias', 'semanas', 'meses', 'bimestres', 
                        'trimestres', 'semestres', 'años']
        
        for key in expected_keys:
            assert key in tempo, f"Missing key '{key}' in tempo dictionary"
        
        # Check that values are reasonable
        assert tempo['años'] == 1
        assert tempo['meses'] == 12
        assert tempo['dias'] == 365


class TestGenFlux:
    """Test cases for cash flow generation function."""
    
    def test_gen_flux_basic(self):
        """Test basic cash flow generation."""
        result = gen_flux(n=5, mu=1000, sigma=100)
        
        assert isinstance(result, numpy.ndarray)
        assert len(result) == 5
        assert all(isinstance(x, (int, float)) for x in result)
    
    def test_gen_flux_positive_values(self):
        """Test that gen_flux generates reasonable positive values."""
        # Generate multiple samples to test statistical properties
        result = gen_flux(n=100, mu=1000, sigma=50)
        
        # Most values should be positive with mu=1000, sigma=50
        positive_count = sum(1 for x in result if x > 0)
        assert positive_count > 90  # Should be mostly positive
    
    def test_gen_flux_different_distributions(self):
        """Test gen_flux with different distribution parameters."""
        # Test with small sigma - should be close to mu
        tight_result = gen_flux(n=10, mu=500, sigma=10)
        
        # All values should be reasonably close to mu
        for value in tight_result:
            assert abs(value - 500) < 100  # Within reasonable bounds
    
    def test_gen_flux_reproducibility(self):
        """Test that gen_flux can be made reproducible."""
        # Set numpy random seed for reproducibility
        numpy.random.seed(42)
        result1 = gen_flux(n=5, mu=1000, sigma=100)
        
        numpy.random.seed(42)
        result2 = gen_flux(n=5, mu=1000, sigma=100)
        
        numpy.testing.assert_array_equal(result1, result2)
    
    def test_gen_flux_edge_cases(self):
        """Test gen_flux with edge cases."""
        # Test with n=1
        result = gen_flux(n=1, mu=100, sigma=10)
        assert len(result) == 1
        
        # Test with zero sigma (should return mu exactly, depending on implementation)
        result_zero_sigma = gen_flux(n=3, mu=100, sigma=0)
        assert len(result_zero_sigma) == 3


class TestMatfinIntegration:
    """Integration tests for matfin module."""
    
    def test_frequency_period_consistency(self):
        """Test consistency between frequency and period dictionaries."""
        # Check that frequencies and periods are inverse relationships where applicable
        assert frec['anual'] * per['año'] == 365  # Days per year
        assert frec['mensual'] * per['mes'] == 1.0  # Months per year normalization
    
    def test_tempo_consistency(self):
        """Test consistency in tempo dictionary."""
        # Check that tempo values make sense relative to each other
        assert tempo['años'] < tempo['meses']
        assert tempo['meses'] < tempo['dias']
    
    @pytest.mark.skipif(not tabulate_available, reason="tabulate not available")
    def test_tabulate_integration(self):
        """Test that tabulate integration works when available."""
        # Generate sample cash flows
        flows = gen_flux(n=5, mu=1000, sigma=100)
        periods = list(range(1, 6))
        
        # Create table data
        table_data = list(zip(periods, flows))
        
        # Test tabulate functionality
        result = tabulate(table_data, headers=['Period', 'Cash Flow'], tablefmt='html')
        
        assert isinstance(result, str)
        assert '<table>' in result
        assert 'Period' in result
        assert 'Cash Flow' in result
    
    def test_cash_flow_statistical_properties(self):
        """Test statistical properties of generated cash flows."""
        # Generate large sample
        flows = gen_flux(n=1000, mu=1000, sigma=100)
        
        # Test mean is approximately correct
        sample_mean = numpy.mean(flows)
        assert abs(sample_mean - 1000) < 50  # Within reasonable tolerance
        
        # Test standard deviation is approximately correct
        sample_std = numpy.std(flows)
        assert abs(sample_std - 100) < 20  # Within reasonable tolerance


class TestMatfinEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_gen_flux_invalid_parameters(self):
        """Test gen_flux with invalid parameters."""
        # Test with negative n - should handle gracefully or raise error
        with pytest.raises((ValueError, TypeError)):
            gen_flux(n=-1, mu=1000, sigma=100)
        
        # Test with n=0 - should return empty array or handle gracefully
        result = gen_flux(n=0, mu=1000, sigma=100)
        assert len(result) == 0 or result is None
    
    def test_dictionary_key_types(self):
        """Test that dictionary keys are strings."""
        for key in frec.keys():
            assert isinstance(key, str)
        
        for key in per.keys():
            assert isinstance(key, str)
        
        for key in tempo.keys():
            assert isinstance(key, str)
    
    def test_dictionary_value_types(self):
        """Test that dictionary values are numeric."""
        for value in frec.values():
            assert isinstance(value, (int, float))
            assert value > 0
        
        for value in per.values():
            assert isinstance(value, (int, float))
            assert value > 0
        
        for value in tempo.values():
            assert isinstance(value, (int, float))
            assert value > 0


if __name__ == "__main__":
    pytest.main([__file__])
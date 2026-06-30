#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test matfin module functionality.

Tests the financial mathematics functions against their actual API:
- frec/per/tempo: integer-keyed dictionaries (1, 2, 4, 6, 12 → Spanish labels)
- gen_flux(f, N_mean, j, ...): cash flow generator returning a dict with F, F0, N, T
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

    def test_frec_dictionary_keys(self):
        """Test frequency dictionary has expected integer keys."""
        # frec maps integer frequencies → Spanish adverbs
        expected_keys = [1, 2, 4, 6, 12]
        for key in expected_keys:
            assert key in frec, f"Missing key {key!r} in frec"

    def test_frec_dictionary_values_are_strings(self):
        """Test frequency dictionary values are non-empty strings."""
        for k, v in frec.items():
            assert isinstance(k, int), f"key {k!r} should be int"
            assert isinstance(v, str) and len(v) > 0, f"value for key {k!r} should be non-empty str"

    def test_per_dictionary_keys(self):
        """Test period dictionary has expected integer keys."""
        expected_keys = [1, 2, 4, 6, 12]
        for key in expected_keys:
            assert key in per, f"Missing key {key!r} in per"

    def test_per_dictionary_values_are_strings(self):
        """Test period dictionary values are non-empty strings."""
        for k, v in per.items():
            assert isinstance(k, int)
            assert isinstance(v, str) and len(v) > 0

    def test_tempo_dictionary_keys(self):
        """Test tempo dictionary has expected integer keys."""
        expected_keys = [1, 2, 4, 6, 12]
        for key in expected_keys:
            assert key in tempo, f"Missing key {key!r} in tempo"

    def test_tempo_dictionary_values_are_strings(self):
        """Test tempo dictionary values are non-empty strings."""
        for k, v in tempo.items():
            assert isinstance(k, int)
            assert isinstance(v, str) and len(v) > 0


class TestGenFlux:
    """Test cases for cash flow generation function."""

    def test_gen_flux_returns_dict(self):
        """gen_flux returns a dict with expected keys."""
        result = gen_flux(f=12, N_mean=24, j=0.01)
        assert isinstance(result, dict)
        assert "F" in result
        assert "F0" in result
        assert "N" in result

    def test_gen_flux_cash_flow_length(self):
        """F array length equals N + 1 (includes initial investment)."""
        result = gen_flux(f=12, N_mean=24, j=0.01)
        assert len(result["F"]) == result["N"] + 1

    def test_gen_flux_initial_investment_negative(self):
        """Initial investment F0 should be negative (outflow)."""
        result = gen_flux(f=12, N_mean=24, j=0.01)
        assert result["F0"] < 0

    def test_gen_flux_f_starts_with_F0(self):
        """Cash flow array F starts with initial investment F0."""
        result = gen_flux(f=12, N_mean=24, j=0.01)
        assert result["F"][0] == result["F0"]

    def test_gen_flux_normal_simulation(self):
        """Normal simulation produces numeric cash flows."""
        result = gen_flux(f=4, N_mean=8, j=0.02, sim="normal")
        future_flows = result["F"][1:]
        assert all(isinstance(float(x), float) for x in future_flows)

    def test_gen_flux_poisson_simulation(self):
        """Poisson simulation produces non-negative future cash flows."""
        result = gen_flux(f=4, N_mean=8, j=0.02, sim="poisson")
        future_flows = result["F"][1:]
        assert numpy.all(future_flows >= 0)


class TestMatfinIntegration:
    """Integration tests for matfin module."""

    def test_frec_per_keys_match(self):
        """frec and per should have the same set of integer keys."""
        assert set(frec.keys()) == set(per.keys())

    def test_tempo_per_keys_match(self):
        """tempo and per should have the same set of integer keys."""
        assert set(tempo.keys()) == set(per.keys())

    @pytest.mark.skipif(not tabulate_available, reason="tabulate not available")
    def test_tab_flux_returns_html(self):
        """tab_flux_vertical produces an HTML table string."""
        from moodpy.matfin import tab_flux_vertical
        result = gen_flux(f=12, N_mean=12, j=0.01)
        tab_result = tab_flux_vertical(result["F"], f=12, fmt="html")
        assert "tab" in tab_result
        assert isinstance(tab_result["tab"], str)
        assert "<table>" in tab_result["tab"]


if __name__ == "__main__":
    pytest.main([__file__])

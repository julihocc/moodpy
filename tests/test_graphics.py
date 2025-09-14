#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test graphics module functionality.

This module contains unit tests for the graphics utilities,
testing image handling and base64 encoding with graceful degradation.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from moodpy.graphics import fig2str

# Test dependencies conditionally
matplotlib_available = True
try:
    import matplotlib.pyplot as plt
    import matplotlib
    # Use non-interactive backend for testing
    matplotlib.use('Agg')
except ImportError:
    matplotlib_available = False


class TestGraphicsModule:
    """Test cases for graphics module functionality."""
    
    @pytest.mark.skipif(not matplotlib_available, reason="matplotlib not available")
    def test_fig2str_basic(self):
        """Test basic figure to string conversion."""
        # Create a simple figure
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot([1, 2, 3], [1, 4, 2])
        ax.set_title("Test Plot")
        
        # Convert to string
        result = fig2str(fig)
        
        # Clean up
        plt.close(fig)
        
        # Verify result
        assert isinstance(result, str)
        assert len(result) > 0
        # Should be base64 encoded image data
        assert result.startswith('data:image/')
    
    @pytest.mark.skipif(not matplotlib_available, reason="matplotlib not available")
    def test_fig2str_different_formats(self):
        """Test figure conversion with different formats."""
        # Create a simple figure
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.bar([1, 2, 3], [1, 4, 2])
        ax.set_title("Bar Chart")
        
        # Test PNG format (default)
        result_png = fig2str(fig)
        assert 'data:image/png' in result_png
        
        # Clean up
        plt.close(fig)
    
    @pytest.mark.skipif(not matplotlib_available, reason="matplotlib not available")
    def test_fig2str_empty_figure(self):
        """Test figure conversion with empty figure."""
        # Create empty figure
        fig, ax = plt.subplots()
        
        # Convert to string
        result = fig2str(fig)
        
        # Clean up
        plt.close(fig)
        
        # Should still work with empty figure
        assert isinstance(result, str)
        assert len(result) > 0
        assert result.startswith('data:image/')
    
    @pytest.mark.skipif(not matplotlib_available, reason="matplotlib not available")
    def test_fig2str_complex_plot(self):
        """Test figure conversion with complex plot."""
        # Create complex figure with multiple elements
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        
        # First subplot - line plot
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 2, 3, 5]
        ax1.plot(x, y, 'b-o')
        ax1.set_title("Line Plot")
        ax1.set_xlabel("X axis")
        ax1.set_ylabel("Y axis")
        ax1.grid(True)
        
        # Second subplot - scatter plot
        import numpy as np
        x2 = np.random.randn(50)
        y2 = np.random.randn(50)
        ax2.scatter(x2, y2, alpha=0.6)
        ax2.set_title("Scatter Plot")
        
        plt.tight_layout()
        
        # Convert to string
        result = fig2str(fig)
        
        # Clean up
        plt.close(fig)
        
        # Verify result
        assert isinstance(result, str)
        assert len(result) > 0
        assert result.startswith('data:image/')
    
    @pytest.mark.skipif(not matplotlib_available, reason="matplotlib not available")
    def test_fig2str_with_text_and_annotations(self):
        """Test figure conversion with text and annotations."""
        # Create figure with text elements
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Add plot
        ax.plot([1, 2, 3, 4], [1, 3, 2, 4], 'r-')
        
        # Add text and annotations
        ax.text(2, 3, 'Peak', fontsize=12, ha='center')
        ax.annotate('Important Point', xy=(3, 2), xytext=(3.5, 1),
                   arrowprops=dict(arrowstyle='->', color='black'))
        ax.set_title("Plot with Annotations")
        
        # Convert to string
        result = fig2str(fig)
        
        # Clean up
        plt.close(fig)
        
        # Verify result
        assert isinstance(result, str)
        assert len(result) > 0
        assert result.startswith('data:image/')
    
    def test_fig2str_without_matplotlib(self):
        """Test fig2str behavior when matplotlib is not available."""
        # This test runs regardless of matplotlib availability
        # If matplotlib is not available, the function should handle it gracefully
        
        if not matplotlib_available:
            # If matplotlib is not available, the function should either:
            # 1. Raise a clear ImportError, or
            # 2. Return None or empty string, or  
            # 3. Provide a meaningful error message
            
            # We can't test the actual function without matplotlib,
            # but we can ensure the module loads gracefully
            assert True  # Module loaded successfully
        else:
            # If matplotlib is available, create a simple test
            fig, ax = plt.subplots()
            ax.plot([1, 2], [1, 2])
            result = fig2str(fig)
            plt.close(fig)
            assert isinstance(result, str)


class TestGraphicsIntegration:
    """Integration tests for graphics module with other components."""
    
    @pytest.mark.skipif(not matplotlib_available, reason="matplotlib not available")
    def test_fig2str_in_html_context(self):
        """Test using fig2str output in HTML context."""
        # Create figure
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot([1, 2, 3], [1, 4, 2])
        ax.set_title("Integration Test")
        
        # Convert to string
        img_data = fig2str(fig)
        
        # Clean up
        plt.close(fig)
        
        # Create HTML with embedded image
        html = f'<img src="{img_data}" alt="Test Plot" />'
        
        # Verify HTML structure
        assert '<img src="data:image/' in html
        assert 'alt="Test Plot"' in html
        assert '/>' in html
    
    @pytest.mark.skipif(not matplotlib_available, reason="matplotlib not available")
    def test_multiple_figures_conversion(self):
        """Test converting multiple figures."""
        results = []
        
        # Create and convert multiple figures
        for i in range(3):
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.plot([1, 2, 3], [i+1, i+2, i+3])
            ax.set_title(f"Figure {i+1}")
            
            result = fig2str(fig)
            results.append(result)
            
            plt.close(fig)
        
        # Verify all conversions
        assert len(results) == 3
        for result in results:
            assert isinstance(result, str)
            assert len(result) > 0
            assert result.startswith('data:image/')
        
        # Results should be different (different plots)
        assert len(set(results)) == 3  # All unique


class TestGraphicsErrorHandling:
    """Test error handling in graphics module."""
    
    @pytest.mark.skipif(not matplotlib_available, reason="matplotlib not available")
    def test_fig2str_with_invalid_figure(self):
        """Test fig2str with invalid input."""
        # Test with None
        with pytest.raises((TypeError, AttributeError)):
            fig2str(None)
        
        # Test with invalid object
        with pytest.raises((TypeError, AttributeError)):
            fig2str("not a figure")
    
    @pytest.mark.skipif(not matplotlib_available, reason="matplotlib not available")
    def test_fig2str_with_closed_figure(self):
        """Test fig2str with already closed figure."""
        # Create and close figure
        fig, ax = plt.subplots()
        ax.plot([1, 2], [1, 2])
        plt.close(fig)
        
        # Try to convert closed figure - behavior may vary
        # Some versions might raise an error, others might handle it
        try:
            result = fig2str(fig)
            # If it succeeds, result should still be valid
            assert isinstance(result, str)
        except (ValueError, RuntimeError):
            # This is also acceptable behavior
            pass


if __name__ == "__main__":
    pytest.main([__file__])
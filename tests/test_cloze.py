#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Cloze class functionality.

This module contains unit tests for the Cloze class,
testing XML export, file management, and batch processing capabilities.
"""

import pytest
import os
import tempfile

# Import from the new package structure
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from moodpy import Cloze, Generator


class TestCloze:
    """Test cases for the Cloze class."""
    
    def test_cloze_initialization(self):
        """Test that Cloze initializes correctly."""
        cloze = Cloze()
        
        assert cloze.counter == 1
        assert cloze.num_question == 1
        assert cloze.penalty == 0.5
        assert cloze.impr is False
        assert cloze.foldername is None
        assert cloze.label is None
        assert cloze.header == " "
        assert isinstance(cloze.generator, Generator)
        assert cloze.filename is None
        assert cloze.path is None
        assert cloze.xml == []
    
    def test_set_generator(self):
        """Test setting a custom generator."""
        cloze = Cloze()
        gen = Generator()
        gen.counter = 42
        
        cloze.set_generator(gen)
        
        assert cloze.generator == gen
        assert cloze.generator.header == cloze.header
    
    def test_set_info(self):
        """Test setting course information."""
        cloze = Cloze()
        
        cloze.set_info("MATHEMATICS", "101", "algebra")
        
        assert "MATHEMATICS" in cloze.header
        assert "Algebra" in cloze.header  # Title case
        assert "MATHEMATICS_101_algebra" in cloze.foldername
        assert cloze.filename is not None
        assert cloze.filename.endswith(".xml")
        assert cloze.filename.startswith("mathematics_101_algebra")
        assert cloze.path is not None
    
    def test_get_info(self, capsys):
        """Test information display."""
        cloze = Cloze()
        cloze.set_info("TEST", "001", "sample")
        
        cloze.get_info()
        
        captured = capsys.readouterr()
        assert "DATETIME:" in captured.out
        assert "FOLDERNAME:" in captured.out
        assert "FILENAME:" in captured.out
    
    def test_create_question_html(self):
        """Test HTML question creation."""
        cloze = Cloze()
        cloze.set_info("TEST", "001", "sample")
        
        # Create a simple generator
        gen = Generator()
        gen.exercise_text = "<p>Test question</p>"
        cloze.generator = gen
        
        html = cloze.create_question()
        
        assert "<question type=\"cloze\">" in html
        assert "<name>" in html
        assert "<questiontext format=\"html\">" in html
        assert "<![CDATA[" in html
        assert "<p>Test question</p>" in html
        assert "<penalty>0.5</penalty>" in html
    
    def test_create_question_with_feedback(self):
        """Test HTML question creation with feedback."""
        cloze = Cloze()
        cloze.set_info("TEST", "001", "sample")
        
        # Create generator with feedback
        gen = Generator()
        gen.exercise_text = "<p>Test question</p>"
        gen.feedback_text = "<p>Test feedback</p>"
        cloze.generator = gen
        
        html = cloze.create_question()
        
        assert "<generalfeedback format=\"html\">" in html
        assert "<p>Test feedback</p>" in html
    
    def test_save_file_creation(self):
        """Test file saving functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                cloze = Cloze()
                cloze.set_info("TEST", "001", "sample")
                
                # Create test content
                test_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<quiz>\n</quiz>"
                cloze.xml = [test_content]
                
                cloze.save()
                
                # Check if directory was created
                assert os.path.exists(cloze.foldername)
                
                # Check if file was created
                assert os.path.exists(cloze.path)
                
                # Check file content
                with open(cloze.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" in content
                    assert "<quiz>" in content
                    
            finally:
                os.chdir(original_cwd)
    
    def test_testing_mode(self):
        """Test testing mode functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                cloze = Cloze()
                cloze.set_info("TEST", "001", "sample")
                
                # Create a simple generator
                gen = Generator()
                gen.lambdas = {"x": lambda k: 42}
                gen.reload_parameters()
                gen.set_exercise("Test with value {d[x]}")
                cloze.generator = gen
                
                cloze.testing(n=2)
                
                # Check if testing file was created
                testing_files = [f for f in os.listdir('.') if f.startswith('TESTING-')]
                assert len(testing_files) == 1
                
                # Check file content
                with open(testing_files[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert "Test with value 42" in content
                    
            finally:
                os.chdir(original_cwd)
    
    def test_batch_exercise_generation(self):
        """Test batch exercise generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                cloze = Cloze()
                cloze.set_info("TEST", "001", "sample")
                
                # Create a simple generator
                gen = Generator()
                gen.lambdas = {"x": lambda k: 42}
                gen.reload_parameters()
                gen.set_exercise("Test with value {d[x]}")
                cloze.generator = gen
                
                cloze.get_exercises(cuantos=3)
                
                # Check if XML file was created
                assert os.path.exists(cloze.path)
                
                # Check file content
                with open(cloze.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert content.count("<question type=\"cloze\">") == 3
                    assert "Test with value 42" in content
                    
            finally:
                os.chdir(original_cwd)
    
    def test_xml_structure(self):
        """Test XML structure compliance."""
        cloze = Cloze()
        cloze.set_info("TEST", "001", "sample")
        
        # Create generator
        gen = Generator()
        gen.exercise_text = "<p>Sample question</p>"
        cloze.generator = gen
        
        html = cloze.create_question()
        
        # Check XML structure elements
        assert html.startswith("<!-- question:")
        assert "<question type=\"cloze\">" in html
        assert "<name>" in html and "</name>" in html
        assert "<questiontext format=\"html\">" in html
        assert "</questiontext>" in html
        assert "<penalty>" in html and "</penalty>" in html
        assert "<hidden>0</hidden>" in html
        assert html.endswith("</question>")


if __name__ == "__main__":
    pytest.main([__file__])
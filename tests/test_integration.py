#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration tests for MoodPy package.

This module contains integration tests that verify the end-to-end functionality
of the MoodPy package, including complete question generation workflows.
"""

import pytest
import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from moodpy import Generator, Cloze

# Test dependencies conditionally
numpy = pytest.importorskip("numpy", reason="numpy not available")


class TestMoodPyIntegration:
    """Integration tests for complete MoodPy workflows."""
    
    def test_basic_question_generation_workflow(self):
        """Test complete basic question generation workflow."""
        # Create generator
        gen = Generator()
        
        # Set up basic parameters
        gen.lambdas = {
            "a": lambda k: numpy.random.randint(1, 10),
            "b": lambda k: numpy.random.randint(1, 10)
        }
        
        # Generate parameters
        gen.reload_parameters()
        
        # Verify parameters were generated
        assert gen.parameters is not None
        assert "a" in gen.parameters
        assert "b" in gen.parameters
        assert 1 <= gen.parameters["a"] <= 10
        assert 1 <= gen.parameters["b"] <= 10
        
        # Set exercise text
        exercise_text = "What is {d[a]} + {d[b]}? Answer: {1:NM:=" + str(gen.parameters["a"] + gen.parameters["b"]) + ":0.1}"
        gen.set_exercise(exercise_text)
        
        # Verify exercise text was set
        assert gen.exercise_text is not None
        assert str(gen.parameters["a"]) in gen.exercise_text
        assert str(gen.parameters["b"]) in gen.exercise_text
    
    def test_complete_xml_export_workflow(self):
        """Test complete XML export workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Create cloze instance
                cloze = Cloze()
                cloze.set_info("MATH", "101", "basic")
                
                # Create generator with simple problem
                gen = Generator()
                gen.lambdas = {"x": lambda k: 5}  # Fixed value for predictable test
                gen.reload_parameters()
                gen.set_exercise("Value is {d[x]}. Answer: {1:NM:=5:0.1}")
                
                # Set generator in cloze
                cloze.set_generator(gen)
                
                # Generate questions
                cloze.get_exercises(cuantos=2)
                
                # Verify file was created
                assert os.path.exists(cloze.path)
                
                # Verify file content
                with open(cloze.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert "<?xml version" in content
                    assert "<quiz>" in content
                    assert "</quiz>" in content
                    assert "<question type=\"cloze\">" in content
                    assert "Value is 5" in content
                    assert "{1:NM:=5:0.1}" in content
                    # Should have 2 questions
                    assert content.count("<question type=\"cloze\">") == 2
                    
            finally:
                os.chdir(original_cwd)
    
    def test_parametric_generation_with_requirements(self):
        """Test parametric generation with requirements validation."""
        gen = Generator()
        
        # Set up parameters with requirements
        gen.lambdas = {
            "a": lambda k: numpy.random.randint(1, 100),
            "b": lambda k: numpy.random.randint(1, 100)
        }
        
        # Add requirement that a > b
        gen.requirements = ["d['a'] > d['b']"]
        
        # Test parameters (should find valid combination)
        gen.test_parameters()
        
        # Verify parameters meet requirements
        assert gen.parameters is not None
        assert gen.parameters["a"] > gen.parameters["b"]
    
    def test_testing_mode_workflow(self):
        """Test testing mode for development."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Create cloze and set up
                cloze = Cloze()
                cloze.set_info("TEST", "001", "dev")
                
                # Create simple generator
                gen = Generator()
                gen.lambdas = {"value": lambda k: 42}
                gen.reload_parameters()
                gen.set_exercise("Test value: {d[value]}")
                
                cloze.set_generator(gen)
                
                # Run in testing mode
                cloze.testing(n=3)
                
                # Find testing file
                testing_files = [f for f in os.listdir('.') if f.startswith('TESTING-')]
                assert len(testing_files) == 1
                
                # Check content
                with open(testing_files[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert "Test value: 42" in content
                    # Should have 3 instances
                    assert content.count("Test value: 42") == 3
                    
            finally:
                os.chdir(original_cwd)
    
    def test_mathematical_problem_workflow(self):
        """Test mathematical problem generation workflow."""
        gen = Generator()
        
        # Set up mathematical problem: solve ax + b = c for x
        gen.lambdas = {
            "a": lambda k: numpy.random.randint(2, 10),  # Avoid a=1 or a=0
            "b": lambda k: numpy.random.randint(-20, 20),
            "x": lambda k: numpy.random.randint(-10, 10)
        }
        
        # Calculate c = ax + b
        gen.derived = {
            "c": lambda d: d["a"] * d["x"] + d["b"]
        }
        
        # Generate and test parameters
        gen.reload_parameters()
        gen.calculate_derived()
        
        # Verify derived calculation
        expected_c = gen.parameters["a"] * gen.parameters["x"] + gen.parameters["b"]
        assert gen.parameters["c"] == expected_c
        
        # Create problem text
        problem = f"Solve for x: {gen.parameters['a']}x + {gen.parameters['b']} = {gen.parameters['c']}"
        answer = "{1:NM:=" + str(gen.parameters["x"]) + ":0.1}"
        
        gen.set_exercise(f"{problem} Answer: {answer}")
        
        assert gen.exercise_text is not None
        assert str(gen.parameters["a"]) in gen.exercise_text
        assert str(gen.parameters["c"]) in gen.exercise_text
    
    def test_financial_mathematics_workflow(self):
        """Test financial mathematics problem workflow."""
        
        gen = Generator()
        
        # Set up compound interest problem
        gen.lambdas = {
            "P": lambda k: numpy.random.randint(1000, 10000),  # Principal
            "r": lambda k: numpy.random.uniform(0.05, 0.15),   # Annual rate
            "t": lambda k: numpy.random.randint(1, 10)         # Years
        }
        
        # Calculate compound interest A = P(1 + r)^t
        gen.derived = {
            "A": lambda d: d["P"] * (1 + d["r"]) ** d["t"]
        }
        
        gen.reload_parameters()
        gen.calculate_derived()
        
        # Verify calculation
        expected_A = gen.parameters["P"] * (1 + gen.parameters["r"]) ** gen.parameters["t"]
        assert abs(gen.parameters["A"] - expected_A) < 0.01
        
        # Create problem
        problem = f"Calculate compound interest: P=${gen.parameters['P']:.2f}, r={gen.parameters['r']:.2%}, t={gen.parameters['t']} years"
        answer = "{1:NM:=" + f"{gen.parameters['A']:.2f}" + ":0.01}"
        
        gen.set_exercise(f"{problem} Answer: {answer}")
        
        assert gen.exercise_text is not None
        assert f"${gen.parameters['P']:.2f}" in gen.exercise_text
    
    def test_error_handling_workflow(self):
        """Test error handling in complete workflow."""
        gen = Generator()
        
        # Set up impossible requirements
        gen.lambdas = {
            "a": lambda k: numpy.random.randint(1, 5),
            "b": lambda k: numpy.random.randint(1, 5)
        }
        
        # Impossible requirement
        gen.requirements = ["d['a'] > 10"]  # a is always <= 5
        
        # This should fail to find valid parameters
        gen.test_parameters()
        
        # Should handle failure gracefully
        assert gen.parameters is None  # or some other expected behavior
    
    def test_multiple_question_types_workflow(self):
        """Test generating different types of questions in sequence."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                cloze = Cloze()
                cloze.set_info("MIXED", "999", "comprehensive")
                
                # Create different generators for different problem types
                questions_created = 0
                
                # Type 1: Simple arithmetic
                gen1 = Generator()
                gen1.lambdas = {"a": lambda k: numpy.random.randint(1, 10), "b": lambda k: numpy.random.randint(1, 10)}
                gen1.reload_parameters()
                gen1.set_exercise(f"What is {gen1.parameters['a']} + {gen1.parameters['b']}? Answer: {{1:NM:={gen1.parameters['a'] + gen1.parameters['b']}:0.1}}")
                
                cloze.set_generator(gen1)
                questions_created += 1
                
                # Generate one question
                cloze.get_exercises(cuantos=1)
                
                # Verify file exists and has content
                assert os.path.exists(cloze.path)
                
                with open(cloze.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert "<question type=\"cloze\">" in content
                    assert questions_created == 1
                    
            finally:
                os.chdir(original_cwd)


class TestMoodPyEdgeCases:
    """Test edge cases in MoodPy integration."""
    
    def test_empty_parameters_workflow(self):
        """Test workflow with no parameters."""
        gen = Generator()
        
        # Set exercise without parameters
        gen.set_exercise("Static question with no variables. Answer: {1:NM:=42:0.1}")
        
        assert gen.exercise_text is not None
        assert "Static question" in gen.exercise_text
        assert "{1:NM:=42:0.1}" in gen.exercise_text
    
    def test_unicode_content_workflow(self):
        """Test workflow with Unicode content (Spanish/mathematical symbols)."""
        gen = Generator()
        
        # Set up with Spanish content and mathematical symbols
        gen.lambdas = {"α": lambda k: 3.14159}
        gen.reload_parameters()
        gen.set_exercise("El valor de α es {d[α]:.3f}. ¿Cuál es el área? Respuesta: {1:NM:=9.870:0.001}")
        
        assert gen.exercise_text is not None
        assert "α" in gen.exercise_text
        assert "¿Cuál" in gen.exercise_text
        assert "Respuesta" in gen.exercise_text


if __name__ == "__main__":
    pytest.main([__file__])
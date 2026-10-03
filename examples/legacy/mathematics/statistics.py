#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probability and Statistics Generator

This example demonstrates how to create parametric probability problems
using MoodPy, focusing on normal distribution and hypothesis testing.

Domain: Mathematics
Topic: Statistics and Probability  
Level: Advanced
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import numpy as np
from moodpy import Generator, Cloze
from moodpy.tools import NM, round_normal


def create_normal_distribution_generator():
    """
    Create a generator for normal distribution problems.
    
    Students calculate probabilities and z-scores for normal distributions.
    """
    gen = Generator()
    
    # Define parameter generation lambdas
    gen.lambdas = {
        "mu": lambda k: round_normal(100, 20, a=50, b=200, d=1),      # Mean (50-200)
        "sigma": lambda k: round_normal(15, 5, a=5, b=30, d=1),       # Std dev (5-30)
        "x": lambda k: round_normal(100, 25, a=30, b=250, d=1)        # Value to evaluate
    }
    
    # Define derived calculations
    gen.derived = {
        "z_score": lambda d: (d["x"] - d["mu"]) / d["sigma"],         # Z-score calculation
        "probability": lambda d: 0.5 * (1 + np.sign(d["z_score"]) * 
                                        min(0.4999, abs(d["z_score"]) * 0.3413))  # Approximation
    }
    
    return gen


def set_normal_distribution_exercise(gen):
    """Set exercise text for normal distribution problems."""
    
    mu = gen.parameters["mu"]
    sigma = gen.parameters["sigma"] 
    x = gen.parameters["x"]
    z_score = gen.parameters["z_score"]
    
    exercise_text = f"""
    <h3>Normal Distribution Problem</h3>
    
    <p>A normally distributed variable has the following parameters:</p>
    <div style="background-color: #f0f8ff; padding: 15px; margin: 10px 0;">
        <ul>
            <li>Mean (μ) = {mu}</li>
            <li>Standard deviation (σ) = {sigma}</li>
        </ul>
    </div>
    
    <p><strong>Question:</strong> Calculate the z-score for the value x = {x}</p>
    
    <p><strong>Formula:</strong> z = (x - μ) / σ</p>
    
    <p>Enter the z-score (round to 2 decimal places): {NM(z_score, error=0.01)}</p>
    """
    
    feedback_text = f"""
    <h3>Solution:</h3>
    
    <p><strong>Step 1:</strong> Identify the values</p>
    <ul>
        <li>x = {x}</li>
        <li>μ = {mu}</li>
        <li>σ = {sigma}</li>
    </ul>
    
    <p><strong>Step 2:</strong> Apply the z-score formula</p>
    <p>z = (x - μ) / σ</p>
    <p>z = ({x} - {mu}) / {sigma}</p>
    <p>z = {x - mu} / {sigma}</p>
    <p>z = {z_score:.3f}</p>
    <p>z ≈ {z_score:.2f} (rounded to 2 decimal places)</p>
    
    <p><strong>Interpretation:</strong> 
    {'This value is above the mean.' if z_score > 0 else 'This value is below the mean.' if z_score < 0 else 'This value equals the mean.'}
    </p>
    """
    
    gen.set_exercise(exercise_text)
    gen.set_feedback(feedback_text)


def create_hypothesis_test_generator():
    """
    Create a generator for hypothesis testing problems.
    """
    gen = Generator()
    
    # Define parameter generation lambdas
    gen.lambdas = {
        "n": lambda k: np.random.randint(25, 200),                    # Sample size
        "sample_mean": lambda k: round_normal(50, 10, a=20, b=100, d=2),  # Sample mean
        "pop_mean": lambda k: round_normal(50, 8, a=25, b=90, d=1),   # Population mean (H0)
        "sigma": lambda k: round_normal(12, 3, a=5, b=25, d=1),       # Population std dev
        "alpha": lambda k: np.random.choice([0.01, 0.05, 0.10])      # Significance level
    }
    
    # Define derived calculations
    gen.derived = {
        "standard_error": lambda d: d["sigma"] / np.sqrt(d["n"]),    # Standard error
        "z_test": lambda d: (d["sample_mean"] - d["pop_mean"]) / d["standard_error"],  # Test statistic
        "critical_value": lambda d: 1.96 if d["alpha"] == 0.05 else (2.58 if d["alpha"] == 0.01 else 1.64)
    }
    
    return gen


def create_data_analysis_generator():
    """
    Create a generator that works with sample data.
    """
    gen = Generator()
    
    # Generate sample dataset
    gen.lambdas = {
        "data_size": lambda k: np.random.randint(8, 15),
        "base_value": lambda k: np.random.randint(20, 80)
    }
    
    # Generate actual data points
    gen.derived = {
        "dataset": lambda d: [d["base_value"] + np.random.randint(-10, 11) for _ in range(d["data_size"])],
        "mean": lambda d: np.mean(d["dataset"]),
        "median": lambda d: np.median(d["dataset"]),
        "std_dev": lambda d: np.std(d["dataset"], ddof=1)  # Sample standard deviation
    }
    
    return gen


def set_data_analysis_exercise(gen):
    """Set exercise text for data analysis problems."""
    
    dataset = gen.parameters["dataset"]
    mean_val = gen.parameters["mean"]
    median_val = gen.parameters["median"]
    std_val = gen.parameters["std_dev"]
    
    # Format the dataset nicely
    data_str = ", ".join(map(str, sorted(dataset)))
    
    exercise_text = f"""
    <h3>Descriptive Statistics Problem</h3>
    
    <p>Given the following dataset:</p>
    <div style="background-color: #f9f9f9; padding: 10px; margin: 10px 0; font-family: monospace;">
        {data_str}
    </div>
    
    <p><strong>Calculate the following statistics:</strong></p>
    
    <ol>
        <li>Sample mean: {NM(mean_val, error=0.01)}</li>
        <li>Sample median: {NM(median_val, error=0.01)}</li>
        <li>Sample standard deviation: {NM(std_val, error=0.01)}</li>
    </ol>
    """
    
    # Create step-by-step feedback
    sorted_data = sorted(dataset)
    n = len(dataset)
    sum_val = sum(dataset)
    
    feedback_text = f"""
    <h3>Solution:</h3>
    
    <p><strong>Dataset (sorted):</strong> {", ".join(map(str, sorted_data))}</p>
    <p><strong>Sample size (n):</strong> {n}</p>
    
    <h4>1. Sample Mean</h4>
    <p>Mean = Σx / n = ({sum_val}) / {n} = {mean_val:.2f}</p>
    
    <h4>2. Sample Median</h4>
    <p>Since n = {n} ({'even' if n % 2 == 0 else 'odd'}), the median is:
    {f"({sorted_data[n//2-1]} + {sorted_data[n//2]}) / 2 = {median_val:.1f}" if n % 2 == 0 else f"{sorted_data[n//2]} = {median_val:.1f}"}
    </p>
    
    <h4>3. Sample Standard Deviation</h4>
    <p>s = √[Σ(x - x̄)² / (n-1)]</p>
    <p>After calculations: s = {std_val:.2f}</p>
    """
    
    gen.set_exercise(exercise_text)
    gen.set_feedback(feedback_text)


def main():
    """
    Main function to demonstrate statistics generators.
    """
    print("=== Statistics and Probability Generator Examples ===\n")
    
    # Example 1: Normal distribution
    print("1. Normal Distribution Z-Score")
    print("-" * 35)
    
    gen1 = create_normal_distribution_generator()
    gen1.reload_parameters()
    gen1.calculate_derived()
    set_normal_distribution_exercise(gen1)
    
    print("Generated Parameters:")
    for key, value in gen1.parameters.items():
        if key == "z_score":
            print(f"  {key} = {value:.3f}")
        elif key == "probability":
            print(f"  {key} = {value:.4f}")
        else:
            print(f"  {key} = {value}")
    
    # Example 2: Data analysis
    print("\n2. Descriptive Statistics") 
    print("-" * 35)
    
    gen2 = create_data_analysis_generator()
    gen2.reload_parameters()
    gen2.calculate_derived()
    set_data_analysis_exercise(gen2)
    
    print("Generated Dataset:")
    print(f"  Data: {gen2.parameters['dataset']}")
    print(f"  Mean: {gen2.parameters['mean']:.2f}")
    print(f"  Median: {gen2.parameters['median']:.1f}")
    print(f"  Std Dev: {gen2.parameters['std_dev']:.2f}")
    
    # Example 3: XML Export
    print("\n3. XML Export")
    print("-" * 35)
    
    cloze = Cloze()
    cloze.set_info("STATISTICS", "STAT301", "descriptive_statistics")
    cloze.set_generator(gen2)
    
    print(f"Output folder: {cloze.foldername}")
    
    # Generate a few test questions
    print("\n4. Testing Mode (3 questions)")
    print("-" * 35)
    cloze.testing(n=3)
    
    # Generate XML file
    print("\n5. Generating XML (8 questions)")
    print("-" * 35)
    cloze.get_exercises(cuantos=8)
    
    print(f"XML file created: {cloze.path}")
    print("✅ Statistics generator examples completed!")


if __name__ == "__main__":
    main()
# MoodPy Examples

This directory contains comprehensive examples demonstrating how to use MoodPy to create parametric question generators for Moodle. Each example showcases different domains, complexity levels, and MoodPy features.

## Directory Structure

```
examples/
├── README.md              # This file
├── __init__.py            # Package initialization
├── demo.py               # Quick demonstration script
├── basic/                # Basic examples for beginners
│   ├── __init__.py
│   └── arithmetic.py     # Simple arithmetic operations
├── business/             # Business mathematics applications
│   └── separable_differential_equations.py
├── economics/            # Economic modeling and analysis
│   ├── supply_demand_equilibrium.py      # Market equilibrium
│   ├── profit_maximization.py            # Business optimization
│   └── market_equilibrium_point.py       # Reconstructed equilibrium
├── finance/              # Financial mathematics and calculations
│   ├── __init__.py
│   ├── compound_interest.py              # Compound interest calculations
│   ├── net_present_value_calculator.py   # NPV analysis (reconstructed)
│   ├── investment_term_template.py       # Investment period template  
│   ├── annual_effective_return_template.py # Annual return template
│   ├── annuities_template.py             # Annuities template
│   └── empty_template.py                 # Blank finance template
├── mathematics/          # Pure mathematics (EDOs, transforms, functions)
│   ├── __init__.py
│   ├── linear_equations.py               # Algebra: ax + b = c
│   ├── statistics.py                     # Statistics and probability
│   ├── separable_differential_equations.py # First-order separable EDOs
│   ├── separable_ode_reconstructed.py    # Reconstructed separable ODE
│   ├── logistic_growth_curve.py          # Population growth modeling
│   ├── second_order_homogeneous_edo.py   # Homogeneous 2nd order EDOs
│   ├── second_order_edo_exponential_kernel.py # 2nd order EDOs with e^(kx)
│   ├── linear_function_non_rational.py   # Linear functions (non-rational)
│   ├── linear_function_rational.py       # Linear functions (rational)
│   └── inverse_laplace_transform.py      # Laplace transform inversions
├── physics/              # Physics problems (future expansion)
│   ├── __init__.py
│   └── README.md         # Physics content planning
└── statistics/           # Statistical analysis and probability
    └── discrete_correlation.py           # Discrete correlation analysis
```

## Getting Started

### Quick Demo
Run the main demo to see MoodPy in action:
```bash
python examples/demo.py
```

### Individual Examples
Each example can be run independently:
```bash
python examples/basic/arithmetic.py
python examples/mathematics/linear_equations.py
python examples/finance/compound_interest.py
python examples/mathematics/statistics.py
python examples/economics/market_equilibrium_point.py
python examples/finance/net_present_value_calculator.py
python examples/mathematics/separable_ode_reconstructed.py
```

## Example Categories

### 1. Basic Examples (`basic/`)
Perfect for beginners learning MoodPy fundamentals.

- **arithmetic.py**: Simple arithmetic operations (addition, subtraction, multiplication, division)
- Demonstrates: Parameter generation, basic exercise formatting, XML export

### 2. Mathematics Examples (`mathematics/`)
More complex mathematical problem generators.

- **linear_equations.py**: Solve linear equations of the form ax + b = c
  - Features: Derived parameters, equation formatting, step-by-step solutions
  - Level: Beginner to Intermediate

- **statistics.py**: Statistics and probability problems
  - Features: Normal distributions, z-scores, descriptive statistics
  - Level: Advanced
  - Includes: Dataset generation, statistical calculations, hypothesis testing

### 3. Finance Examples (`finance/`)
Financial mathematics and business applications.

- **compound_interest.py**: Compound interest calculations
  - Features: Financial formulas, currency formatting, multiple compounding frequencies
  - Level: Intermediate
  - Uses: MoodPy's matfin module for financial calculations

### 4. Reconstructed Examples (`reconstructed/`)
Examples reverse-engineered from the extensive XML library in `library/`.
*Note: This section will be populated in Phase 5 of the refactoring plan.*

## Common Patterns

### Basic Generator Structure
```python
from moodpy import Generator, Cloze
from moodpy.tools import NM

# 1. Create generator
gen = Generator()

# 2. Define parameters
gen.lambdas = {
    "a": lambda k: np.random.randint(1, 10),
    "b": lambda k: np.random.randint(1, 10)
}

# 3. Generate parameters
gen.reload_parameters()

# 4. Set exercise text
gen.set_exercise("What is {d[a]} + {d[b]}? Answer: " + NM(gen.parameters["a"] + gen.parameters["b"]))

# 5. Create XML export
cloze = Cloze()
cloze.set_info("SUBJECT", "CODE", "topic")
cloze.set_generator(gen)
cloze.get_exercises(cuantos=10)
```

### Advanced Features

#### Derived Parameters
```python
gen.derived = {
    "sum": lambda d: d["a"] + d["b"],
    "product": lambda d: d["a"] * d["b"]
}
gen.calculate_derived()
```

#### Parameter Requirements
```python
gen.requirements = ["d['a'] > d['b']", "d['sum'] < 100"]
gen.test_parameters()  # Find valid parameter combinations
```

#### Rich Exercise Formatting
```python
exercise_text = f"""
<h3>Problem Title</h3>
<p>Given the following data:</p>
<div style="background-color: #f0f8ff; padding: 15px;">
    <ul>
        <li>Value A: {gen.parameters['a']}</li>
        <li>Value B: {gen.parameters['b']}</li>
    </ul>
</div>
<p>Calculate: {NM(answer_value, error=0.01)}</p>
"""
```

## MoodPy Features Demonstrated

### Core Functionality
- **Parameter Generation**: Random value creation with constraints
- **Derived Calculations**: Computing dependent values
- **Exercise Formatting**: HTML and LaTeX mathematical expressions
- **XML Export**: Moodle-compatible question format
- **Testing Mode**: Development and debugging support

### Utility Functions  
- **NM()**: Numerical answer formatting for Moodle
- **round_normal()**: Bounded normal random numbers
- **cdata()**: XML CDATA wrapping
- **Mathematical formatting**: LaTeX integration

### Financial Mathematics
- **frec, per, tempo**: Financial frequency dictionaries
- **gen_flux()**: Cash flow generation
- **Compound interest formulas**: A = P(1+r)^t variations

## Development Workflow

### 1. Testing Your Generator
```python
# Test with verbose output
cloze.testing(n=5)  # Creates TESTING-*.txt file

# Check parameters
print("Generated Parameters:", gen.parameters)
```

### 2. XML Generation
```python
# Set output information
cloze.set_info("MATHEMATICS", "ALG101", "linear_equations")

# Generate questions
cloze.get_exercises(cuantos=20)  # Creates XML file
```

### 3. Validation
- Check XML file validity
- Import into Moodle test course
- Verify question rendering and grading

## Best Practices

1. **Parameter Validation**: Always test parameter combinations
2. **Error Handling**: Use appropriate error tolerances in NM()
3. **Rich Feedback**: Provide step-by-step solutions
4. **Testing**: Use testing mode during development
5. **Documentation**: Comment complex calculations
6. **Formatting**: Use HTML/CSS for better presentation

## Advanced Topics

### Custom Parameter Generation
```python
gen.lambdas = {
    "type": lambda k: np.random.choice(["linear", "quadratic", "exponential"]),
    "coeffs": lambda k: generate_coefficients_based_on_type(gen.parameters.get("type"))
}
```

### Conditional Exercise Generation
```python
def set_exercise_text(gen):
    if gen.parameters["type"] == "linear":
        return create_linear_exercise(gen)
    elif gen.parameters["type"] == "quadratic":
        return create_quadratic_exercise(gen)
    # ... etc
```

### Graphics Integration
```python
from moodpy.graphics import fig2str
import matplotlib.pyplot as plt

# Create plot
fig, ax = plt.subplots()
ax.plot(data_x, data_y)

# Embed in question
exercise_text = f'<img src="{fig2str(fig)}" alt="Graph" />'
```

## Contributing

When adding new examples:

1. Follow the established directory structure
2. Include comprehensive docstrings and comments
3. Demonstrate specific MoodPy features
4. Provide both simple and advanced usage
5. Test thoroughly with Moodle import
6. Update this README with new examples

## Migration from v2.0.0

If you have existing MoodPy v2.0.0 generators:

1. Update imports: `from moodpy import Generator, Cloze`
2. Use new package structure: `src/moodpy/`
3. Check for deprecated functions
4. Test with new validation methods
5. Update XML export calls

## Further Reading

- **Main Documentation**: See `docs/` directory (Phase 7)
- **API Reference**: Complete function documentation
- **Migration Guide**: Detailed v2→v3 upgrade instructions
- **Contributing Guide**: Development and contribution guidelines
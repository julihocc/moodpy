# MoodPy v3.0.0 - Developer Documentation

**Production-ready parametric exercise generator for Moodle LMS with 750+ lines of core code, 60+ domain examples, and comprehensive test coverage.**

---

## Table of Contents

1. [Quick Navigation](#quick-navigation)
2. [Project Status](#project-status)
3. [Architecture Overview](#architecture-overview)
4. [Package Structure](#package-structure)
5. [Core Classes & APIs](#core-classes--apis)
6. [Development Guide](#development-guide)
7. [Testing & Quality](#testing--quality)
8. [Deployment & Publishing](#deployment--publishing)
9. [Common Patterns](#common-patterns)
10. [Troubleshooting](#troubleshooting)

---

## Quick Navigation

| Need | Location |
|------|----------|
| Getting started | `examples/demo.py` or README.md |
| Add new example | `examples/{domain}/` folder |
| Run tests | `pytest` or `python -m pytest` |
| Build package | `pip install -e .` or `python -m build` |
| Publish to PyPI | GitHub Release or `twine upload` |
| Core code | `src/moodpy/*.py` (752 lines total) |
| Package metadata | `pyproject.toml` (119 lines) |

---

## Project Status

| Aspect | Status |
|--------|--------|
| **Version** | 3.0.0 (stable) |
| **Python Support** | 3.8, 3.9, 3.10, 3.11, 3.12 |
| **License** | MIT |
| **Test Coverage** | Full suite with pytest + coverage reports |
| **PyPI Status** | Published as `moodpy` |
| **Documentation** | Comprehensive examples + inline docs |
| **Maintenance** | Active |

### Recent Milestones

- ✅ v3.0.0: Production release with derived parameters
- ✅ GitHub Actions: Automated PyPI publishing
- ✅ 60+ Examples: All major domains covered
- ✅ Test Suite: 6 test modules, integration tests
- ✅ Package Structure: Proper src/moodpy layout

---

## Architecture Overview

### Core Concept

MoodPy implements a **parametric exercise framework** where:

1. **Parameters** are randomly generated values
2. **Derived** parameters are calculated from base parameters
3. **Exercises** use both to create unique questions
4. **XML** is generated for Moodle import
5. **Batches** create sets of variations

```
┌─────────────────────────────────────────────────┐
│           Generator Instance                     │
│  - lambdas: Functions to generate random values │
│  - derived: Calculated dependent values          │
│  - requirements: Validation conditions           │
└──────────────────┬──────────────────────────────┘
                   ↓
         ┌─────────────────────┐
         │ reload_parameters() │ → Generate random values
         └─────────────────────┘
                   ↓
         ┌──────────────────────┐
         │ calculate_derived()  │ → Compute derived values
         └──────────────────────┘
                   ↓
         ┌─────────────────────┐
         │ test_parameters()   │ → Validate constraints
         └─────────────────────┘
                   ↓
         ┌──────────────────────┐
         │ set_exercise()       │ → Format with parameters
         └──────────────────────┘
                   ↓
         ┌────────────────────┐
         │ Cloze wrapper      │ → Batch processing
         └────────────────────┘
                   ↓
         ┌────────────────────┐
         │ get_exercises()    │ → XML export
         └────────────────────┘
                   ↓
         ┌────────────────────┐
         │ Moodle import file │
         └────────────────────┘
```

### Key Design Principles

1. **Parametric Randomization**: Every exercise is unique via lambda functions
2. **Separation of Concerns**: Generator (logic) vs Cloze (export)
3. **Derived Values**: Complex calculations from base parameters
4. **Validation**: Constraint checking up to 10,000 iterations
5. **XML Compliance**: Automatic Moodle-compatible formatting
6. **Extensibility**: Domain-specific modules (matfin, graphics)

---

## Package Structure

```
moodpy/
├── pyproject.toml                    # Package metadata (v3.0.0, dependencies)
├── setup.py                          # Legacy setup (if needed)
├── README.md                         # User guide & quick start
├── CLAUDE.md                         # This file (developer docs)
│
├── src/moodpy/                       # Main package (752 lines)
│   ├── __init__.py                   # Package exports, version info (117 lines)
│   ├── generator.py                  # Generator class (114 lines)
│   ├── cloze.py                      # Cloze export class (145 lines)
│   ├── tools.py                      # Utilities & formatting (159 lines)
│   ├── matfin.py                     # Financial math module (123 lines)
│   └── graphics.py                   # Image handling (94 lines)
│
├── examples/                         # 60+ working examples
│   ├── README.md                     # Examples guide
│   ├── demo.py                       # Quick demo
│   ├── basic/                        # Beginner examples
│   ├── mathematics/                  # 20+ math examples
│   ├── finance/                      # 8+ finance examples
│   ├── economics/                    # 5+ economics examples
│   ├── engineering/                  # 6+ engineering examples
│   ├── statistics/                   # Statistical analysis
│   ├── data_science/                 # Data science applications
│   ├── business/                     # Business mathematics
│   └── physics/                      # Physics problems (future)
│
├── tests/                            # Full test coverage
│   ├── conftest.py                   # pytest configuration
│   ├── test_generator.py             # Generator tests
│   ├── test_cloze.py                 # Cloze tests
│   ├── test_tools.py                 # Tools/utilities tests
│   ├── test_matfin.py                # Financial math tests
│   ├── test_graphics.py              # Graphics module tests
│   └── test_integration.py           # End-to-end tests
│
├── .github/
│   ├── workflows/
│   │   └── publish.yml               # PyPI publishing workflow
│   ├── ai-manifest.json              # AI assistant config
│   ├── copilot-instructions.md       # Copilot setup guide
│   └── prompts/                      # Automation prompts
│
├── generators/                       # Submodule: Generator library
└── library/                          # Submodule: Question bank archive

Key files: 752 lines core + 60+ examples + comprehensive tests
```

---

## Core Classes & APIs

### 1. Generator Class (114 lines, `src/moodpy/generator.py`)

**Purpose**: Create parametric exercises with random parameters and validation.

#### Key Attributes

```python
gen = Generator()
gen.counter           # Exercise number (int)
gen.header            # HTML header: "<h1>Subject</h1><h2>Topic</h2>"
gen.lambdas           # {key: lambda function} - parameter generators
gen.derived           # {key: lambda function} - dependent calculations
gen.parameters        # {key: value} - current random values (read-only)
gen.data              # Copy of parameters for backward compatibility
gen.exercise_text     # HTML/LaTeX exercise statement
gen.feedback_text     # Optional solution/explanation text
gen.requirements      # [bool, bool, ...] - validation conditions
```

#### Core Methods

```python
# Generation
gen.reload_parameters()           # Execute all lambdas
gen.calculate_derived()           # Compute derived parameters
gen.test_parameters(max_steps=10000, debug=False)  # Find valid combination

# Exercise setup
gen.set_exercise(text)            # Set with format string {d[key]}
gen.set_feedback(text)            # Set feedback with format string
gen.set_counter(counter)          # Update exercise number

# Output
gen.statement()                   # Return XML-formatted question + feedback
gen.get_exercise()                # Return HTML-formatted exercise + feedback
gen.print_args()                  # Debug: print all parameters
```

#### New in v3.0.0: Derived Parameters

```python
gen = Generator()
gen.lambdas = {
    "principal": lambda k: np.random.randint(1000, 10000),
    "rate": lambda k: np.random.uniform(0.05, 0.15),
    "years": lambda k: np.random.randint(1, 30)
}

gen.derived = {
    "amount": lambda d: d["principal"] * (1 + d["rate"]) ** d["years"],
    "interest": lambda d: d["amount"] - d["principal"]
}

gen.reload_parameters()
gen.calculate_derived()
# Now gen.parameters contains: principal, rate, years, amount, interest
```

#### Validation Pattern

```python
gen.requirements = [
    lambda: gen.parameters["principal"] > 1000,
    lambda: gen.parameters["rate"] < 0.20,
    lambda: (gen.parameters["principal"] * gen.parameters["rate"]) % 100 != 0
]

gen.reload_parameters()
gen.calculate_derived()
gen.test_parameters(max_steps=5000, debug=True)

if gen.parameters is None:
    print("Failed to find valid parameters")
```

---

### 2. Cloze Class (145 lines, `src/moodpy/cloze.py`)

**Purpose**: Batch generation and Moodle XML export.

#### Key Attributes

```python
cloze = Cloze()
cloze.counter          # Current exercise number
cloze.num_question     # Question numbering
cloze.penalty          # Penalty for wrong answers (default 0.5)
cloze.generator        # Associated Generator instance
cloze.foldername       # Output directory: {MATERIA}_{CLAVE}_{TEMA}
cloze.filename         # Output file: {foldername}_{timestamp}.xml
cloze.label            # Question label/header
cloze.header           # HTML header for all exercises
cloze.xml              # List of XML statements
cloze.path             # Full path to output file
```

#### Core Methods

```python
# Setup
cloze.set_info(materia, clave, tema)
cloze.set_generator(generator)

# Generation
cloze.get_exercises(cuantos=10)   # Generate N questions + export XML
cloze.testing(n=5)                # Test mode: generate TESTING-*.txt

# Output
cloze.to_moodle_xml()             # Write XML file
cloze.get_info()                  # Print folder/file info
```

#### File Organization

```
{MATERIA}_{CLAVE}_{TEMA}/
├── {MATERIA}_{CLAVE}_{TEMA}_{timestamp}.xml
├── {MATERIA}_{CLAVE}_{TEMA}_{timestamp}.xml
└── TESTING-{MATERIA}_{CLAVE}_{TEMA}_{timestamp}.txt
```

Example: `MATHEMATICS_CALC_DERIVATIVES_20260630122345.xml`

---

### 3. Tools Module (159 lines, `src/moodpy/tools.py`)

**Utility functions** for random number generation and Moodle formatting.

#### Key Functions

```python
# Random number generation
round_normal(m=0, s=1, size=1, a=-np.inf, b=np.inf, d=0)
  # Bounded normal distribution with rounding

int_normal(m=0, s=1, size=1, a=-np.inf, b=np.inf)
  # Integer version of bounded normal

# Moodle formatting
NM(x, entero=False, percent=False, error=0.001, round_zero=False)
  # Format numerical answer: {1:NM:=value:tolerance}
  # Example: NM(42.5, error=0.001) → "{1:NM:=42.5:0.0425}"

STxt(text)
  # Short text formatting (legacy)

# Array conversion
txt2arr(temp, array=True)
  # Convert space-separated string to numpy array
```

#### Numerical Answer Format

The `NM()` function creates Moodle-compatible numerical questions:

```python
NM(42.5, error=0.001)              # {1:NM:=42.5:0.0425}
NM(100, entero=True)               # {1:NM:=100:0}
NM(0.85, error=0.05, percent=True) # Percentage with tolerance
```

---

### 4. MatFin Module (123 lines, `src/moodpy/matfin.py`)

**Financial mathematics** domain-specific generators.

#### Key Functions

```python
# Frequency management
frec = {1: "anualmente", 2: "semestralmente", 4: "trimestralmente", ...}
per = {1: "año", 2: "semestre", 4: "trimestre", ...}
tempo = {1: "anual", 2: "semestral", 4: "trimestral", ...}
get_frec()  # Random frequency with all labels

# Interest rate generation
gen_rates(r_mean, f)  # Generate interest rate with frequency validation

# Cash flow generation
gen_flux(f, N_mean, j, scale=0.5, lower=-np.inf, upper=np.inf, sim="normal")
  # Generate cash flow sequence with normal or Poisson distribution
gen_T(f, _N, min_N=5)  # Number of periods

# Financial calculations
VPN(F, j)  # Net Present Value
TIR(F)     # Internal Rate of Return (root-finding)
alpha(j, N)  # Annuity factor

# Table generation
tab_flux(F, f=None)                    # Horizontal HTML table
tab_flux_vertical(F, f=None, fmt="html")  # Vertical HTML table
```

#### Example: Financial Exercise

```python
from moodpy.matfin import get_frec, gen_rates, gen_flux, VPN, tab_flux_vertical

frec_data = get_frec()
rates = gen_rates(r_mean=8, f=frec_data['f'])
flux = gen_flux(f=frec_data['f'], N_mean=5, j=rates['j'])
vpn = VPN(flux['F'], rates['j'])
table = tab_flux_vertical(flux['F'], f=frec_data['f'])

exercise = f"Cash flows:\n{table['tab']}\nCalculate NPV at {rates['r_pct']}%"
```

---

### 5. Graphics Module (94 lines, `src/moodpy/graphics.py`)

**Image integration** with matplotlib and base64 encoding.

**Note**: Requires matplotlib and optional dependencies.

#### Key Functions

```python
tagImg(nom_graf, alt="imagen", width="600", height="400")
  # Generate HTML <img> tag with PLUGINFILE reference

fileImg(nom_graf, cod_graf)
  # Generate XML <file> element for base64-encoded image

encodePlot(*args)           # Encode matplotlib plot
encodeGraf(graf)            # Encode Sage/graphics
```

---

## Development Guide

### Setup Development Environment

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/julihocc/moodpy.git
cd moodpy

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install optional dependencies
pip install -e ".[docs,examples]"
```

### Project Dependencies

**Core** (always required):
- `numpy>=1.21.0` - Numerical operations
- `matplotlib>=3.5.0` - Plotting
- `tabulate>=0.8.0` - Table formatting
- `scipy>=1.7.0` - Scientific computing

**Development** (dev):
- `pytest>=7.0` - Testing
- `pytest-cov>=4.0` - Coverage reporting
- `black>=22.0` - Code formatting
- `flake8>=5.0` - Linting
- `pre-commit>=2.20` - Git hooks

**Documentation** (docs):
- `sphinx>=5.0`
- `sphinx-rtd-theme>=1.0`
- `jupyter>=1.0`
- `nbsphinx>=0.8`

### Creating a New Example

1. **Choose domain** under `examples/{domain}/`
2. **Follow the pattern**:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example Description

Domain: ...
Topic: ...
Level: Beginner/Intermediate/Advanced
Formula/Concept: ...
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import numpy as np
from moodpy import Generator, Cloze
from moodpy.tools import NM

def create_generator():
    """Create the generator."""
    gen = Generator()
    gen.lambdas = {...}
    gen.derived = {...}
    gen.requirements = [...]
    return gen

def set_exercise_text(gen):
    """Set exercise with formatting."""
    # Use gen.parameters to format
    pass

if __name__ == "__main__":
    gen = create_generator()
    # Test it
```

3. **Test locally** with `python examples/{domain}/your_example.py`
4. **Update** `examples/README.md` with description

### Coding Standards

**Tools installed**: black (formatting), flake8 (linting), pre-commit (hooks)

```bash
# Format code
black src/moodpy/ examples/ tests/

# Check linting
flake8 src/moodpy/ examples/ tests/

# Run pre-commit hooks
pre-commit run --all-files
```

**Style guide**:
- Line length: 88 characters (black default)
- Python 3.8+ syntax (no walrus operators required for compatibility)
- Docstrings for all public functions
- Type hints where practical

---

## Testing & Quality

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_generator.py -v

# Run with coverage report
pytest --cov=moodpy --cov-report=html

# Run tests without stopping at first failure
pytest --tb=short --maxfail=5
```

### Test Structure

```
tests/
├── conftest.py              # pytest fixtures and configuration
├── test_generator.py        # Generator class tests
├── test_cloze.py            # Cloze class tests
├── test_tools.py            # Tools/utilities tests
├── test_matfin.py           # Financial module tests
├── test_graphics.py         # Graphics module tests
└── test_integration.py      # End-to-end tests
```

### Coverage Requirements

- Target: >80% coverage
- Reports: Terminal, HTML, XML (for CI/CD)
- Command: `pytest --cov=moodpy --cov-report=term-missing`

---

## Deployment & Publishing

### PyPI Publishing

**Automated via GitHub Actions** (`.github/workflows/publish.yml`):

1. Create GitHub Release
2. Workflow triggers automatically
3. Package is built and tested
4. Uploaded to PyPI

**Manual publishing**:

```bash
# Build
python -m build

# Check
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### Versioning

Follow Semantic Versioning (MAJOR.MINOR.PATCH):
- Update `pyproject.toml` version
- Update `src/moodpy/__init__.py` version
- Create git tag: `git tag v3.0.0`
- Push and create GitHub Release

---

## Common Patterns

### Basic Exercise Generator

```python
from moodpy import Generator, Cloze, tools
import numpy as np

# Create generator
gen = Generator()
gen.lambdas = {
    "a": lambda k: np.random.randint(1, 20),
    "b": lambda k: np.random.randint(1, 20),
}
gen.requirements = [
    lambda: gen.parameters["a"] + gen.parameters["b"] < 50
]

# Generate
gen.reload_parameters()
gen.test_parameters()

# Set exercise
a, b = gen.parameters["a"], gen.parameters["b"]
answer = a + b
gen.set_exercise(f"Calculate: {a} + {b} = {tools.NM(answer)}")

# Export
cloze = Cloze()
cloze.set_info("MATH", "101", "addition")
cloze.set_generator(gen)
cloze.get_exercises(cuantos=20)
```

### Advanced: Derived Parameters

```python
gen.lambdas = {
    "principal": lambda k: np.random.randint(1000, 100000),
    "rate": lambda k: np.random.uniform(0.05, 0.20),
    "years": lambda k: np.random.randint(1, 40)
}

gen.derived = {
    "amount": lambda d: d["principal"] * (1 + d["rate"]) ** d["years"],
    "interest": lambda d: d["amount"] - d["principal"]
}

gen.reload_parameters()
gen.calculate_derived()

# Now all 5 values available: principal, rate, years, amount, interest
```

### Conditional Logic

```python
def set_exercise(gen):
    operation_type = gen.parameters.get("type", "add")
    
    if operation_type == "add":
        answer = gen.parameters["a"] + gen.parameters["b"]
        op_symbol = "+"
    else:
        answer = gen.parameters["a"] - gen.parameters["b"]
        op_symbol = "-"
    
    exercise = f"{gen.parameters['a']} {op_symbol} {gen.parameters['b']} = ?"
    feedback = f"Answer: {tools.NM(answer)}"
    
    gen.set_exercise(exercise)
    gen.set_feedback(feedback)
```

---

## Troubleshooting

### Parameter Validation Failures

**Problem**: `parameters is None` after `test_parameters()`

**Solution**:
1. Reduce constraints: try with fewer requirements
2. Increase max_steps: `test_parameters(max_steps=50000)`
3. Check constraint logic: use `debug=True`
4. Log parameters: `print(gen.parameters)` before testing

### XML Export Issues

**Problem**: Moodle won't import XML file

**Solution**:
1. Check encoding: must be UTF-8
2. Validate XML: Use online validator or `twine check`
3. Check CDATA wrapping: all text in `<![CDATA[...]]>`
4. Check Moodle version: some features v3.9+ only

### Import Errors

**Problem**: `from moodpy import ...` fails

**Solution**:
1. Install package: `pip install -e .`
2. Check Python version: 3.8+ required
3. Reinstall: `pip install --force-reinstall --no-cache-dir .`

### Graphics Not Working

**Problem**: `AttributeError` in graphics module

**Solution**:
1. Install matplotlib: `pip install matplotlib`
2. Check imports in graphics.py
3. Use try/except: `if moodpy.has_graphics(): ...`

---

## API Quick Reference

| Task | Code |
|------|------|
| Create generator | `gen = Generator()` |
| Add parameters | `gen.lambdas = {...}` |
| Add derived | `gen.derived = {...}` |
| Generate values | `gen.reload_parameters()` |
| Compute derived | `gen.calculate_derived()` |
| Validate | `gen.test_parameters()` |
| Set exercise | `gen.set_exercise(text)` |
| Set feedback | `gen.set_feedback(text)` |
| Get XML | `gen.statement()` |
| Create cloze | `cloze = Cloze()` |
| Configure cloze | `cloze.set_info(...); cloze.set_generator(...)` |
| Export batch | `cloze.get_exercises(cuantos=20)` |
| Format answer | `NM(value, error=0.001)` |

---

## Resources

- **User Guide**: README.md
- **Examples**: `examples/` directory (60+)
- **Tests**: `tests/` directory (full coverage)
- **PyPI**: https://pypi.org/project/moodpy/
- **GitHub**: https://github.com/julihocc/moodpy
- **Issues**: https://github.com/julihocc/moodpy/issues

---

**Last Updated**: June 2026 | **Version**: 3.0.0 | **License**: MIT

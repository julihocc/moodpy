# MoodPy v2.0.0

> Python library for generating randomized Moodle cloze-type questions with mathematical and financial content

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-beta-orange.svg)](https://github.com/julihocc/moodpy)

## Overview

MoodPy is a powerful Python library designed for educators and instructional designers who need to create dynamic, parametric exercises for Moodle learning management systems. The library specializes in generating randomized cloze-type questions with mathematical and financial content that can be directly exported to Moodle XML format.

## Features

### ✨ Core Capabilities
- **Parametric Exercise Generation**: Create exercises with randomized values using lambda functions
- **Moodle XML Export**: Direct export to Moodle-compatible XML format
- **Mathematical Content**: Built-in support for mathematical notation and calculations
- **Financial Mathematics**: Specialized generators for financial calculations (NPV, IRR, cash flows)
- **Batch Processing**: Generate multiple question variations automatically
- **Image Integration**: Support for matplotlib plots with base64 encoding

### 🎯 Key Components
- **`Generator`**: Core class for parametric exercise creation with validation
- **`Cloze`**: Moodle XML export and file management system
- **`tools`**: Utility functions for random generation and formatting
- **`matfin`**: Financial mathematics domain-specific generators
- **`graphics`**: Image handling for matplotlib integration

## Installation

```bash
# Install from source
git clone https://github.com/julihocc/moodpy.git
cd moodpy
pip install -e .

# Or install dependencies manually
pip install numpy matplotlib tabulate
```

## Quick Start

```python
import moodpy
from moodpy import Generator, Cloze, tools

# Create a parametric exercise generator
gen = Generator()

# Define random parameters using lambda functions
gen.lambdas = {
    "a": lambda k: np.random.randint(1, 10),
    "b": lambda k: np.random.randint(1, 10)
}

# Generate random values and validate
gen.reload_parameters()
gen.test_parameters()

# Create the exercise text with placeholders
gen.set_exercise("Calculate: {d[a]} + {d[b]} = {1:NM:=" + 
                str(gen.parameters['a'] + gen.parameters['b']) + ":0.1}")

# Export to Moodle XML
cloze = Cloze()
cloze.generator = gen
cloze.set_info("MATH_101", "addition")
cloze.get_exercises(cuantos=10)  # Generate 10 variations
```

## Architecture

### Parameter Generation Workflow
1. **Define Parameters**: Use `generator.lambdas` with lambda functions
2. **Generate Values**: Call `reload_parameters()` to create random values
3. **Validate**: Use `test_parameters()` to ensure requirements are met
4. **Create Exercise**: Set exercise text with `{d[key]}` placeholders
5. **Export**: Generate Moodle XML with `cloze.get_exercises()`

### File Organization
- **Folders**: `{SUBJECT}_{CODE}_{TOPIC}` format
- **Files**: `{foldername}_{timestamp}.xml` with automatic timestamping
- **Encoding**: UTF-8 support for international mathematical content

## Advanced Usage

### Financial Mathematics
```python
from moodpy import matfin

# Generate cash flow exercises
gen = matfin.create_npv_generator()
gen.reload_parameters()

# Create compound interest problems
gen = matfin.create_interest_generator()
```

### Custom Validation
```python
# Add parameter requirements
gen.requirements = [
    "d['a'] > d['b']",
    "d['a'] * d['b'] < 100"
]
gen.test_parameters()  # Validates up to 10,000 iterations
```

### Numerical Answers with Tolerance
```python
import moodpy.tools as tools

# Create numerical answer with automatic tolerance
answer = tools.NM(42.5, error=0.001)  # Creates {1:NM:=42.5:0.001}

# Integer answers
integer_answer = tools.NM(42, entero=True)  # Creates {1:NM:=42}
```

## Project Structure

```
moodpy/
├── __init__.py          # Package initialization and exports
├── generator.py         # Core Generator class for parametric exercises
├── cloze.py            # Moodle XML export and batch processing
├── tools.py            # Utility functions and random generation
├── matfin.py           # Financial mathematics generators
├── graphics.py         # Image handling and matplotlib integration
├── generators/         # Submodule: Collection of exercise generators
├── library/           # Submodule: Question banks and course materials
└── pyproject.toml     # Project configuration and dependencies
```

## Submodules

This repository includes two important submodules:

- **`generators/`**: Contains 80+ Jupyter notebooks with ready-to-use exercise generators
- **`library/`**: Organized collection of question banks and course materials from different semesters

To initialize submodules after cloning:
```bash
git submodule update --init --recursive
```

## Dependencies

### Required
- **Python 3.8+**
- **numpy**: Numerical computations and random generation
- **matplotlib**: Plot generation and image handling
- **tabulate**: HTML table formatting for financial calculations

### Optional
- **Jupyter**: For working with generator notebooks
- **pandas**: Advanced data manipulation (used in some generators)

## Development Status

MoodPy v2.0.0 represents a major milestone in the project's evolution:

- ✅ **Stable Core**: Generator and Cloze classes are production-ready
- ✅ **Rich Content**: 80+ exercise generators in multiple mathematical domains
- ✅ **Proven**: Used in real educational environments with multiple semesters of content
- 🔄 **Active Development**: Continuous improvements and new features
- 📚 **Well Documented**: Comprehensive AI-assisted development with detailed instructions

## Contributing

We welcome contributions! The project uses AI-assisted development with detailed instructions in `.github/copilot-instructions.md`.

### Development Setup
```bash
git clone --recurse-submodules https://github.com/julihocc/moodpy.git
cd moodpy
pip install -e .
```

### Key Development Patterns
- Use `Generator` class for all parametric exercises
- Follow the lambda → reload → validate → generate workflow
- Maintain UTF-8 encoding for international content
- Use `tools.NM()` for numerical Moodle answers
- Test with `cloze.testing()` before XML export

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Julio Cesar Hernandez Ochoa**
- Email: julihocc@gmail.com
- GitHub: [@julihocc](https://github.com/julihocc)

## Acknowledgments

- Built for educators creating dynamic mathematical content
- Designed with Moodle LMS integration in mind
- Supports international educational standards
- Community-driven development with AI assistance

---

*MoodPy v2.0.0 - Empowering educators with dynamic, parametric question generation*

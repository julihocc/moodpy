# MoodPy Copilot Instructions

MoodPy is a Python library for generating randomized Moodle cloze-type questions with mathematical and financial content. The system generates parametric exercises that can be exported to Moodle XML format.

## Architecture Overview

### Core Components
- **`generator.py`**: Base `Generator` class that handles parametric exercise generation with lambda functions, parameter validation, and XML formatting
- **`cloze.py`**: `Cloze` class that manages Moodle XML export, file organization, and batch processing
- **`tools.py`**: Utility functions for random number generation, array manipulation, and Moodle numerical question formatting
- **`matfin.py`**: Financial mathematics domain-specific generators (rates, cash flows, NPV, IRR calculations)
- **`graphics.py`**: Image handling utilities for matplotlib plots and base64 encoding (missing imports: `matplotlib.pyplot as plt`, `time`, `base64`, `os`)

### Data Flow
1. `Generator` → parametric exercise creation with randomized values
2. `Cloze` → batch generation and Moodle XML formatting
3. Output → timestamped XML files in organized folders per subject/topic

## Key Patterns & Conventions

### Generator Pattern
```python
# Core workflow: Create generator, set parameters, validate requirements
gen = Generator()
gen.lambdas = {"x": lambda k: np.random.randint(1, 10)}
gen.reload_parameters()  # Generate random values
gen.test_parameters()    # Validate against requirements
gen.set_exercise("Problem with {d[x]}")  # Use format strings
```

### Moodle Numerical Questions
Use `tools.NM()` function for numerical answers with tolerance:
```python
# Creates {1:NM:=42.5:0.1} format for Moodle
answer = tools.NM(42.5, error=0.001)  # Automatic tolerance
integer_answer = tools.NM(42, entero=True)  # Integer format
```

### File Organization Convention
- Folders: `{MATERIA}_{CLAVE}_{TEMA}` (uppercase subject, lowercase topic)
- Files: `{foldername}_{timestamp}.xml` (lowercase, underscores)
- Timestamps: `datetime.now()` with colons/dots removed

### XML Structure
- Questions wrapped in `<![CDATA[]]>` sections via `cdata()` function
- Headers auto-injected with subject/topic formatting: `<h1>Subject</h1><h2>Topic</h2>`
- Feedback sections optional, controlled by `generator.feedback_text`

## Domain-Specific Patterns

### Financial Mathematics (`matfin.py`)
- Frequency mappings: `frec`, `per`, `tempo` dictionaries for period translations
- Cash flow generation with `gen_flux()` using normal/poisson distributions  
- Interest rate calculations with validation loops
- Table generation using `tabulate` library for HTML output

### Random Number Generation (`tools.py`)
- `round_normal()`: bounded normal distribution with decimal rounding
- `int_normal()`: integer version of bounded normal
- `txt2arr()`: string to numpy array conversion using `exec()`

## Development Workflows

### Testing & Validation
```python
# Generate test output without XML export
cloze.testing(n=5)  # Creates TESTING-*.txt file with parameters and exercises

# Batch XML generation
cloze.get_exercises(cuantos=10)  # Generates 10 randomized questions
```

### Missing Dependencies
- `graphics.py` needs imports: `import matplotlib.pyplot as plt`, `import time`, `import base64`, `import os`
- External dependencies: `numpy`, `matplotlib`, `tabulate`

### Parameter Validation
- Use `generator.requirements` list for validation conditions
- `test_parameters()` runs up to 10,000 iterations to find valid combinations
- Set `debug=True` for parameter inspection during validation

## Critical Implementation Notes

- **Never modify** `generator.parameters` directly - use `generator.lambdas` and `reload_parameters()`
- **Always validate** parameters with `test_parameters()` before exercise generation
- **Format strings** use `{d[key]}` syntax for parameter substitution
- **File encoding** must be UTF-8 for Spanish mathematical content
- **XML escaping** handled automatically by `cdata()` wrapper function

## Code Patterns to Follow

1. **Parametric Generation**: Define lambdas → reload → validate → generate
2. **Error Handling**: Check `parameters is None` after validation failure  
3. **File Management**: Use `cloze.set_info()` for proper folder/file structure
4. **XML Export**: Call `get_exercises()` for complete workflow automation
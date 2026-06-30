# MoodPy - Parametric Exercise Generator for Moodle

Generate randomized mathematical and financial exercises for Moodle LMS with parametric variables and automatic XML export.

## What is MoodPy?

MoodPy is a Python library that helps educators create **personalized, randomized quizzes** for Moodle. Instead of manually writing hundreds of similar questions, you define a question template with variable parameters, and MoodPy generates unlimited unique versions automatically.

### Example Use Case

**Without MoodPy:** Write 20 different compound interest problems manually
**With MoodPy:** Define one template with variables (principal, rate, time), generate 20 unique problems in seconds

## Features

✅ **Parametric Exercise Generation** - Define variables with random number generators  
✅ **Parameter Validation** - Set mathematical constraints (e.g., "interest rate > 5%")  
✅ **Moodle XML Export** - Direct import into Moodle cloze questions  
✅ **Financial Math Support** - Pre-built generators for NPV, IRR, cash flows  
✅ **Batch Processing** - Generate hundreds of questions in one operation  
✅ **Spanish Language Support** - Full UTF-8 support for Spanish mathematical content  

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/julihocc/moodpy.git
cd moodpy

# Install dependencies
pip install numpy matplotlib tabulate
```

### Basic Example — Pattern A (string template)

```python
from moodpy import Generator, Cloze
import numpy as np

gen = Generator()
gen.lambdas = {
    "a": lambda k: np.random.randint(1, 10),
    "b": lambda k: np.random.randint(2, 8),
}
gen.derived = {
    "answer": lambda d: int(d["a"] + d["b"]),
}
# Requirements must be lambda functions (not strings)
gen.requirements = [
    lambda: gen.parameters["a"] != gen.parameters["b"],
]

# Initial reload so set_exercise() can render a preview
gen.reload_parameters()
gen.calculate_derived()

# Template is re-substituted fresh for each question in get_exercises()
gen.set_exercise("<p>Calculate: {d[a]} + {d[b]} = ?</p><p>Answer: {d[answer]}</p>")

cloze = Cloze()
cloze.set_info("MATHEMATICS", "ALG101", "addition")
cloze.set_generator(gen)
cloze.get_exercises(cuantos=10)  # 10 unique questions → XML file
```

This creates `MATHEMATICS_ALG101_addition/` with an XML file ready to import into Moodle.

### When answers need formatting — Pattern B (exercise_fn)

Use `exercise_fn` when the answer must be formatted with `NM()` (Moodle numerical
answer syntax). The function is called each iteration with freshly generated parameters.

```python
from moodpy import Generator, Cloze
from moodpy.tools import NM
import numpy as np

gen = Generator()
gen.lambdas = {
    "a": lambda k: np.random.randint(2, 13),
    "b": lambda k: np.random.randint(2, 13),
}
gen.requirements = [lambda: gen.parameters["a"] != gen.parameters["b"]]

def build_exercise(gen):
    a, b = gen.parameters["a"], gen.parameters["b"]
    gen.set_exercise(f"<p>Calculate: {a} × {b} = {NM(a * b, entero=True)}</p>")
    gen.set_feedback(f"<p>{a} × {b} = {a * b}</p>")

cloze = Cloze()
cloze.set_info("MATH", "102", "multiplication")
cloze.set_generator(gen)
cloze.get_exercises(cuantos=10, exercise_fn=build_exercise)
```

## Core Concepts

### 1. Generators

A **Generator** defines how to create a single exercise with randomized parameters.

```python
gen = Generator()
gen.lambdas = {
    "x": lambda k: np.random.randint(1, 100),      # Random integer 1-99
    "y": lambda k: np.random.choice([2, 3, 5, 7]), # Pick from list
    "z": lambda k: np.random.normal(50, 10),       # Normal distribution
}
```

### 2. Parameter Validation

Use the `requirements` list to ensure generated parameters meet mathematical constraints:

```python
gen.requirements = [
    lambda: gen.parameters["x"] < gen.parameters["y"],  # x must be less than y
    lambda: (gen.parameters["x"] + gen.parameters["y"]) % 10 != 0,  # sum not divisible by 10
]
gen.reload_parameters()
gen.test_parameters()  # Validates up to 10,000 times
```

### 3. Cloze Wrapper

The **Cloze** class handles batch generation and Moodle XML export:

```python
cloze = Cloze()
cloze.set_info(materia="Math", clave="CALC", tema="Derivatives")
cloze.set_generator(gen)
cloze.get_exercises(cuantos=50)  # Generate 50 questions
```

Output structure:
```
MATH_CALC_DERIVATIVES/
├── MATH_CALC_DERIVATIVES_20260630122345.xml  (Moodle-ready XML)
└── [more XML files as you generate batches]
```

### 4. Numerical Answers

Use `tools.NM()` to format numerical answers with tolerance for Moodle:

```python
from moodpy.tools import NM

answer = NM(42.5, error=0.001)      # Value ±0.1% tolerance → {1:NM:=42.5:0.0425}
answer = NM(100, entero=True)       # Integer answer        → {1:NM:=100}
```

> Use `NM()` inside an `exercise_fn`, not directly in a template string —
> Moodle's `{1:NM:=...}` syntax conflicts with Python's `.format()` placeholders.

## Financial Mathematics

MoodPy includes specialized generators for financial math problems:

```python
from moodpy.matfin import get_frec, gen_rates, gen_flux, VPN, tab_flux_vertical, TIR

# Generate frequency (annual, semi-annual, quarterly, etc.)
frec = get_frec()  # Returns: {'f': 2, 'frecuencia': 'semestralmente', ...}

# Generate interest rate
rates = gen_rates(r_mean=8, f=frec['f'])  # 8% mean annual rate

# Generate cash flow
flux = gen_flux(f=frec['f'], N_mean=5, j=rates['j'])

# Calculate financial metrics
npv = VPN(flux['F'], rates['j'])
irr = TIR(flux['F'])

# Generate HTML table for exercise
table = tab_flux_vertical(flux['F'], f=frec['f'], fmt="html")
```

## File Organization

MoodPy automatically organizes output by subject and topic:

```
PROJECT_CODE_TOPIC/
├── PROJECT_CODE_TOPIC_YYYYMMDDHHMMSS.xml      (XML for Moodle)
├── PROJECT_CODE_TOPIC_YYYYMMDDHHMMSS.xml
└── TESTING-PROJECT_CODE_TOPIC_YYYYMMDDHHMMSS.txt  (Debug output)
```

Naming convention:
- **Folder**: `{SUBJECT}_{CODE}_{TOPIC}` (uppercase/lowercase)
- **Files**: Include timestamp to avoid overwrites
- **Encoding**: UTF-8 for Spanish characters (ñ, á, é, etc.)

## Module Reference

| Module | Purpose |
|--------|---------|
| `generator.py` | `Generator` class - core parametric exercise engine |
| `cloze.py` | `Cloze` class - batch generation and Moodle XML export |
| `tools.py` | Utility functions (random numbers, Moodle formatting) |
| `matfin.py` | Financial mathematics generators (rates, cash flows, NPV, IRR) |
| `graphics.py` | Image handling utilities (matplotlib integration) |

### Submodules

- **moodpy-generators**: Domain-specific exercise generators
- **moodpy-library**: Shared reusable components

## Advanced Usage

### Testing Without XML Export

Generate and inspect exercises without creating XML files:

```python
cloze.testing(n=5)  # Creates TESTING-*.txt with parameters
```

### Custom Random Distributions

Define complex parameter distributions:

```python
from moodpy.tools import round_normal, int_normal

gen.lambdas = {
    # Integer from bounded normal distribution
    "amount": lambda k: int_normal(m=50000, s=10000, size=1, a=10000, b=100000)[0],
    
    # Rounded decimal from bounded normal distribution
    "rate": lambda k: round_normal(m=0.08, s=0.02, size=1, a=0.05, b=0.12, d=4)[0],
}
```

### Formatted Output with Feedback

Add explanations and solutions:

```python
gen.set_feedback("""
Solution: Using the compound interest formula...
Answer: ${d[answer]:.2f}
""")

xml = gen.statement()  # Includes feedback section
```

## Limitations & Known Issues

- Parameter validation timeout: 10,000 iterations max (increase with `max_steps=`)
- `exercise_fn` is required when `NM()` answers appear in exercise text (see Pattern B above)

## Importing into Moodle

1. Generate questions with MoodPy
2. In Moodle:
   - Course → Import content → Import course
   - Select the XML file from `{SUBJECT}_{CODE}_{TOPIC}/`
   - Questions appear as Cloze-type (fill-in-the-blank)

## Dependencies

- `numpy` - Numerical operations and random number generation
- `matplotlib` - Plotting utilities
- `tabulate` - HTML/text table generation

```bash
pip install numpy matplotlib tabulate
```

## Project Structure

```
moodpy/
├── pyproject.toml             # Package metadata
├── src/moodpy/                # Core package
│   ├── generator.py           # Generator class
│   ├── cloze.py               # Moodle XML export
│   ├── tools.py               # Utilities (NM, round_normal, txt2arr, …)
│   ├── matfin.py              # Financial math
│   └── graphics.py            # fig2str, tagImg, encodePlot
├── examples/                  # 60+ working examples by domain
├── tests/                     # pytest suite (78 tests)
├── generators/                # Submodule: exercise generator library
├── library/                   # Submodule: question bank archive
└── .github/workflows/         # Automated PyPI publishing
```

## Contributing

This project is organized with Git submodules for modularity:
- Core exercises: Add to `generators/` submodule
- Shared code: Add to `library/` submodule
- Core framework: Modify main files

## License

*See repository for license information.*

## Getting Help

- **Architecture Guide**: See `.github/copilot-instructions.md`
- **Code Examples**: Check the examples above
- **Domain Patterns**: Review `matfin.py` for financial math patterns

---

**Made for Spanish educational institutions. Full UTF-8 support for mathematical notation and Spanish language content.**

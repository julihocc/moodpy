# MoodPy - Moodle Parametric Exercise Generator

## Project Overview

**MoodPy** is a Python library for generating randomized, parametric educational exercises for Moodle LMS. It specializes in creating mathematical and financial mathematics questions in the Moodle cloze (fill-in-the-blank) format.

The system allows educators to:
- Define parametric exercises with random variable generation
- Create mathematically complex problems with variable parameters
- Export questions to Moodle XML format for direct import
- Generate batches of randomized exercises with consistent templates

**Language & Domain**: Spanish-language mathematical and financial education content
**Target Platform**: Moodle LMS
**Status**: Active development with recent additions of modular substructure

---

## Repository Structure

### Root Files

| File | Purpose |
|------|---------|
| **`generator.py`** | Core `Generator` class for parametric exercise creation |
| **`cloze.py`** | `Cloze` class managing Moodle XML export and batch processing |
| **`tools.py`** | Utility functions for RNG, array manipulation, Moodle question formatting |
| **`matfin.py`** | Financial mathematics domain-specific generators (rates, cash flows, NPV, IRR) |
| **`graphics.py`** | Image handling utilities (matplotlib integration, base64 encoding) |

### Submodules

```
generators/    → moodpy-generators repo (contains specific exercise generators)
library/       → moodpy-library repo (shared reusable components)
```

The project uses Git submodules to separate domain-specific generators and shared library code. Both are tracked in `.gitmodules`.

### Configuration & Documentation

```
.github/copilot-instructions.md    → Architecture & pattern guide
.github/prompts/                   → Automated workflow prompts
  - commit.prompt.md               → Commit message generation
  - release-new-version.prompt.md  → Version release workflow
  - publish-to-pipy.prompt.md      → PyPI publishing workflow
  - tag-new-version.prompt.md      → Git tagging automation
  - update-documentation.prompt.md → Doc update automation
  - summarize-changes.prompt.md    → Change summarization
```

---

## Core Architecture

### Data Flow

```
1. Generator Instance
   ↓
2. Define parametric inputs (lambdas)
   ↓
3. Reload & validate parameters
   ↓
4. Generate exercise text with random values
   ↓
5. Cloze wrapper for batch processing
   ↓
6. Export to Moodle XML
```

### Key Classes

#### `Generator` (generator.py)
Base class for creating randomized exercises with parameter validation.

**Key Attributes:**
- `counter`: Exercise counter for tracking
- `header`: HTML header content (subject/topic formatting)
- `lambdas`: Dictionary of lambda functions for parameter generation
- `parameters`: Generated parameter values (read-only, use reload)
- `data`: Dictionary for exercise-specific data
- `exercise_text`: The main exercise statement
- `feedback_text`: Optional feedback for the exercise
- `requirements`: List of boolean conditions for parameter validation

**Key Methods:**
- `reload_parameters()`: Execute lambdas to generate new parameter values
- `test_parameters(max_steps=10000, debug=False)`: Validate parameters against requirements
- `set_exercise(text)`: Set exercise template with format strings
- `set_feedback(text)`: Set optional feedback text
- `statement()`: Generate complete XML-formatted question with optional feedback
- `print_args()`: Debug output showing parameters and values

**Usage Pattern:**
```python
gen = Generator()
gen.header = "<h1>Subject</h1><h2>Topic</h2>"
gen.lambdas = {
    "x": lambda k: np.random.randint(1, 10),
    "y": lambda k: np.random.randint(5, 20)
}
gen.requirements = [lambda: gen.parameters["x"] < gen.parameters["y"]]
gen.reload_parameters()
gen.test_parameters()
gen.set_exercise("Calculate {d[x]} + {d[y]}")
xml_output = gen.statement()
```

#### `Cloze` (cloze.py)
Wrapper class managing batch generation and Moodle XML export.

**Key Attributes:**
- `counter`: Current exercise counter
- `num_question`: Question numbering in output
- `penalty`: Penalty for incorrect answers (default 0.5)
- `foldername`: Output directory name
- `filename`: Output XML filename
- `label`: Question label/header
- `header`: HTML header for exercises
- `generator`: Associated `Generator` instance
- `xml`: List of generated XML statements

**Key Methods:**
- `set_info(materia, clave, tema)`: Configure output folder and filename structure
- `set_generator(gen)`: Assign a Generator instance
- `get_exercises(cuantos)`: Generate `n` randomized exercises and export to XML
- `to_moodle_xml()`: Write XML file with proper Moodle format
- `testing(n)`: Generate testing output (debugging, not XML)

**Folder/File Convention:**
- Folder: `{MATERIA}_{CLAVE}_{TEMA}` (uppercase subject, topic lowercase)
- File: `{foldername}_{timestamp}.xml` (lowercase, underscores)
- Timestamp: `YYYYMMDDHHmmss` format (colons/dots removed)

---

## Key Components

### 1. Generator Framework (generator.py)

The `Generator` class implements a **parametric exercise system** using lambda functions:

**Workflow:**
1. Define lambda functions in `gen.lambdas` dict
2. Call `reload_parameters()` to generate random values
3. Define validation rules in `gen.requirements` list
4. Call `test_parameters()` to validate combinations (retry up to 10,000 times)
5. Use `{d[key]}` format strings in exercise text for parameter substitution

**XML Generation:**
- Questions wrapped in `<![CDATA[]]>` sections via `cdata()` function
- Automatic HTML headers with subject/topic formatting
- Optional feedback sections

**Format Functions:**
- `cdata(text)`: Wraps text in XML CDATA tags
- `questiontext(cdata_text)`: Creates question element
- `feedback(cdata_text)`: Creates feedback element

### 2. Moodle Export (cloze.py)

The `Cloze` class handles:
- Batch question generation
- Moodle XML format compliance
- File organization by subject/topic
- Metadata and naming conventions

**XML Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
  <!-- question: 001 -->
  <question type="cloze">
    <name>
      <text>Pregunta 001 SUBJECT_CODE_TOPIC timestamp</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[
        <h1>Subject</h1>
        <h2>Topic</h2>
        Exercise text with blanks {1:QTYPE:choices}
      ]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text><![CDATA[Feedback text]]></text>
    </generalfeedback>
    <penalty>0.5</penalty>
    <hidden>0</hidden>
  </question>
</quiz>
```

### 3. Utilities (tools.py)

**Random Number Generation:**
- `round_normal(m, s, size, a, b, d)`: Bounded normal distribution with decimal rounding
- `int_normal(m, s, size, a, b)`: Integer version of bounded normal
- Validation loops ensure values stay within bounds [a, b]

**Array/String Utilities:**
- `txt2arr(temp, array=True)`: Convert space-separated strings to numpy arrays using `exec()`

**Moodle Question Formatting:**
- `NM(x, entero=False, percent=False, error=0.001, round_zero=False)`: Format numerical answers
  - Returns `{1:NM:=value:tolerance}` format for Moodle
  - Example: `NM(42.5, error=0.001)` → `"{1:NM:=42.5:0.0425}"`
  - Integer mode: `NM(42, entero=True)` → `"{1:NM:=42:0}"`

### 4. Financial Mathematics (matfin.py)

Domain-specific generators for financial math exercises:

**Frequency/Period Handling:**
- `frec`: Frequency mappings (1=annual, 2=biannual, 3=quarterly, etc.)
- `per`: Period labels in Spanish
- `tempo`: Temporal adjectives for use in text
- `get_frec()`: Randomly select a frequency with associated labels

**Cash Flow Generation:**
- `gen_T(f, _N, min_N=5)`: Generate number of periods
- `gen_rates(r_mean, f)`: Generate interest rates with validation
- `gen_flux(f, N_mean, j, scale, lower, upper, sim)`: Generate cash flows (normal/poisson)
- `alpha(j, N)`: Annuity factor calculation
- `tab_flux(F, f)`: Generate horizontal HTML table of cash flows
- `tab_flux_vertical(F, f, fmt)`: Generate vertical HTML table

**Financial Metrics:**
- `VPN(F, j)`: Net Present Value calculation
- `TIR(F)`: Internal Rate of Return (IRR) calculation with root-finding

### 5. Graphics/Images (graphics.py)

*Note: This file has missing imports and unfinished implementation.*

**Available Functions:**
- `tagImg(nom_graf, alt, width, height)`: Generate HTML img tag with PLUGINFILE reference
- `fileImg(nom_graf, cod_graf)`: Generate XML file element for base64-encoded image
- `encodePlot(*args)`: Encode matplotlib plot as base64 (incomplete - missing self context)
- `encodeGraf(graf)`: Encode Sage/other graphics as base64 (incomplete)

**Status**: Requires import fixes and context refactoring for full functionality.

---

## Conventions & Patterns

### Parameter Definition Pattern

```python
gen = Generator()
gen.lambdas = {
    "principal": lambda k: np.random.randint(1000, 10000),
    "rate": lambda k: np.random.choice([0.05, 0.06, 0.07, 0.08]),
    "periods": lambda k: np.random.randint(5, 20)
}
gen.requirements = [
    lambda: gen.parameters["principal"] > 0,
    lambda: gen.parameters["rate"] > 0.04,
    lambda: gen.parameters["periods"] >= 5
]
gen.reload_parameters()
gen.test_parameters(debug=False)
```

### File Organization Convention

```
MATHEMATICS_CALC_DERIVATIVES/
├── MATHEMATICS_CALC_DERIVATIVES_20260630122345.xml
├── MATHEMATICS_CALC_DERIVATIVES_20260630123456.xml
└── TESTING-MATHEMATICS_CALC_DERIVATIVES_20260630122345.txt
```

### Spanish Content Support

- Full UTF-8 encoding for Spanish characters (ñ, á, é, í, ó, ú, ü)
- Frequency labels: "anualmente", "semestralmente", "cuatrimestral", "trimestralmente", "bimestralmente", "mensualmente"
- Question format uses "Pregunta" (Question) with zero-padded numbers

### Numerical Answer Formatting

Moodle cloze questions use special format for numerical answers:
- `{1:NM:=42.5:0.1}` - Value 42.5 with ±0.1 tolerance
- `{1:NM:=42:0}` - Integer answer (no tolerance)
- Auto-tolerance: `error=0.001` means ±0.1% of value

---

## Development Workflows

### Creating a Simple Exercise Generator

```python
from cloze import Cloze
from generator import Generator
import numpy as np

# Create cloze instance
cz = Cloze()
cz.set_info(materia="Mathematics", clave="CALC", tema="Derivatives")

# Create generator
gen = Generator()
gen.lambdas = {
    "x": lambda k: np.random.randint(1, 10),
    "n": lambda k: np.random.randint(2, 6)
}
gen.set_exercise("Find the derivative of f(x) = {d[x]}x^{d[n]}")

# Generate batch
cz.set_generator(gen)
cz.get_exercises(cuantos=10)  # Outputs 10 questions to MATHEMATICS_CALC_DERIVATIVES_*.xml
```

### Testing Without XML Export

```python
cz.testing(n=5)  # Creates TESTING-*.txt with parameters and exercises
```

### Parameter Validation Example

```python
gen.requirements = [
    lambda: gen.parameters["x"] % 2 == 0,  # x must be even
    lambda: gen.parameters["y"] > gen.parameters["x"],  # y > x
    lambda: (gen.parameters["x"] + gen.parameters["y"]) % 10 != 0  # sum not multiple of 10
]
gen.test_parameters(max_steps=10000, debug=True)
if gen.parameters is None:
    print("Could not find valid parameters within 10000 iterations")
```

### Financial Math Exercise

```python
from matfin import get_frec, gen_T, gen_rates, gen_flux, VPN, tab_flux_vertical, TIR
from cloze import Cloze

frec_data = get_frec()  # Get random frequency
rates_data = gen_rates(r_mean=8, f=frec_data['f'])
flux_data = gen_flux(f=frec_data['f'], N_mean=5, j=rates_data['j'])

vpn_result = VPN(flux_data['F'], rates_data['j'])
tir_result = TIR(flux_data['F'])
table = tab_flux_vertical(flux_data['F'], f=frec_data['f'])

exercise_text = f"""
Frequency: {frec_data['frecuencia']}
Rate: {rates_data['r_pct']}%
{table['tab']}
Calculate NPV: {vpn_result['VPN']:.2f}
"""
```

---

## Known Issues & Limitations

### graphics.py Issues
- Missing imports: `matplotlib.pyplot as plt`, `time`, `base64`, `os`
- Functions use undefined `self` context (should be refactored)
- `encodePlot()` and `encodeGraf()` incomplete/non-functional

### Current State
- No setup.py or pyproject.toml (not packaged for PyPI yet)
- Submodules added recently (a154712, e449b8c) but may be empty
- Workflows defined in prompts but not automated via GitHub Actions

### Technical Debt
- XML escaping relies on CDATA wrapper (robust but manual)
- Parameter validation timeout of 10,000 iterations may fail for constrained problems
- No logging or error reporting in batch generation
- File paths hardcoded relative to current directory

---

## Dependencies

### External Libraries Required
- `numpy`: Numerical operations, random number generation
- `matplotlib`: Plotting (for graphics.py)
- `tabulate`: HTML/text table generation (used in matfin.py)

### Python Version
- Python 3.6+ (uses f-strings in some areas, but not consistently)

### Installation Notes
- Currently no `requirements.txt` or `setup.py`
- Manual pip install needed: `pip install numpy matplotlib tabulate`

---

## Recent Changes

| Commit | Description |
|--------|-------------|
| a5523b9 | Adds prompts for automated release workflows |
| a154712 | Add moodpy-library as submodule |
| e449b8c | Add moodpy-generators as submodule |
| 643e29f | Expands .gitignore with comprehensive Python ignore patterns |
| 23f450a | Adds Copilot instructions for MoodPy library |

The project is moving toward modular structure with submodules for generators and library code, with automation workflows being added.

---

## Next Steps for Consideration

1. **Packaging**: Create `setup.py` or `pyproject.toml` for PyPI distribution
2. **Documentation**: Add docstrings to all classes/functions
3. **Testing**: Add unit tests for parameter validation and XML generation
4. **Fix graphics.py**: Complete imports and refactor image handling
5. **CI/CD**: Implement GitHub Actions workflows matching `.github/prompts` definitions
6. **Submodule Integration**: Document and test moodpy-generators and moodpy-library integration
7. **Type Hints**: Add Python type hints for IDE support and clarity

---

## Quick Reference

### Common Tasks

**Generate 5 random math questions:**
```python
cz = Cloze()
cz.set_info("Math", "ALG", "Factoring")
cz.set_generator(your_generator)
cz.get_exercises(5)
```

**Create a generator with validation:**
```python
gen = Generator()
gen.lambdas = {...}
gen.requirements = [...]
gen.reload_parameters()
gen.test_parameters()
```

**Format numerical answer for Moodle:**
```python
from tools import NM
answer = NM(42.5, error=0.001)  # Returns "{1:NM:=42.5:0.0425}"
```

**Generate cash flow table:**
```python
from matfin import gen_flux, tab_flux_vertical
flux = gen_flux(f=2, N_mean=5, j=0.06)
table = tab_flux_vertical(flux['F'], f=2, fmt="html")
```

---

## File Size Reference

| File | Lines | Purpose |
|------|-------|---------|
| generator.py | 93 | Core Generator class |
| cloze.py | 146 | Moodle XML export wrapper |
| tools.py | 96 | Utility functions |
| matfin.py | 110 | Financial math generators |
| graphics.py | 39 | Image handling (incomplete) |

**Total Core Code**: ~480 lines (excludes .github config files)

---

## Contact & Ownership

- **Repository**: moodpy (moodpy.worktrees/explore-codebase-2 branch)
- **Submodules**: 
  - moodpy-library: https://github.com/julihocc/moodpy-library.git
  - moodpy-generators: https://github.com/julihocc/moodpy-generators.git
- **Git User**: Juliho (jcc30986@gmail.com)

---

## License & Usage

*License information not specified in repository. Check LICENSE file or repository settings.*

This documentation was generated from repository analysis. For the latest updates, refer to `.github/copilot-instructions.md` and git history.

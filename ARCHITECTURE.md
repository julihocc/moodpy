# MoodPy Architecture & Design

Comprehensive technical documentation for MoodPy's design, implementation patterns, and extension points.

---

## Design Philosophy

### Core Principles

1. **Parametric Randomization**: Every exercise variation is unique
2. **Separation of Concerns**: Generation logic separate from export logic
3. **Composability**: Combine simple generators into complex workflows
4. **Extensibility**: Domain-specific modules without modifying core
5. **XML Compliance**: Automatic Moodle-compatible output
6. **Validation First**: Ensure mathematical constraints before generation

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| Lambdas for parameters | Allows complex, arbitrary RNG strategies |
| Derived parameters | Support calculations without modifying lambdas |
| Validation loops | Ensure mathematical validity of problems |
| XML auto-formatting | Reduce user errors, ensure compatibility |
| Batch processing | Scale to thousands of questions efficiently |
| Submodule architecture | Separate content from platform |

---

## Parametric Exercise Generation Pipeline

### Step-by-Step Process

```
┌─────────────────────────────────────────────────────────────┐
│ 1. LAMBDA GENERATION (reload_parameters)                    │
│    Execute all user-defined lambda functions               │
│    → Random values generated (primary parameters)           │
│    → Store in gen.parameters dict                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. DERIVED CALCULATION (calculate_derived)                  │
│    Execute derived parameter lambdas using primary params   │
│    → Complex calculations from random values               │
│    → Add to gen.parameters (secondary parameters)           │
│    → Available for exercise formatting                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. VALIDATION (test_parameters)                             │
│    Check all requirements (boolean conditions)              │
│    If valid:  Proceed to exercise generation              │
│    If invalid: Retry up to max_steps times                │
│                ├─ Regenerate lambda parameters             │
│                ├─ Recalculate derived parameters           │
│                └─ Check requirements again                 │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. EXERCISE FORMATTING (set_exercise / set_feedback)        │
│    Format text using {d[key]} placeholders                  │
│    → Replace with actual parameter values                   │
│    → Support HTML/LaTeX mathematical notation               │
│    → Include header (subject/topic)                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. XML GENERATION (statement)                               │
│    Wrap in Moodle cloze XML format                          │
│    ├─ <questiontext> with CDATA wrapping                    │
│    ├─ <generalfeedback> if feedback_text set               │
│    └─ <penalty> score deduction                            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. BATCH PROCESSING (get_exercises)                         │
│    Repeat steps 1-5 for N questions                         │
│    → Collect all XML statements                            │
│    → Add metadata (timestamps, numbering)                   │
│    → Write to file with timestamps                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
          ┌──────────────────────────┐
          │  MOODLE IMPORT XML FILE  │
          │ READY FOR IMPORT/USE     │
          └──────────────────────────┘
```

### Data Flow Example

```python
# 1. Initial Setup
gen.lambdas = {
    "principal": lambda k: np.random.randint(1000, 10000),
    "rate": lambda k: np.random.uniform(0.05, 0.15)
}

gen.derived = {
    "interest": lambda d: d["principal"] * d["rate"]
}

# 2. Generation runs through pipeline:
gen.reload_parameters()
# After: gen.parameters = {"principal": 5423, "rate": 0.0892}

gen.calculate_derived()
# After: gen.parameters = {"principal": 5423, "rate": 0.0892, "interest": 483.48}

# 3. Validation
gen.requirements = [
    lambda: gen.parameters["interest"] < gen.parameters["principal"]
]
gen.test_parameters()
# Validates: 483.48 < 5423 ✓ (Valid, proceeds)

# 4. Formatting
gen.set_exercise(
    "Principal: ${d[principal]}, Rate: {d[rate]:.2%}\n"
    "Interest: {d[interest]:.2f}"
)
# After: exercise_text includes actual values

# 5. XML Output
xml = gen.statement()
# Returns Moodle-compatible XML with exercise and optional feedback

# 6. Batch Export (via Cloze)
for i in range(10):
    gen.reload_parameters()
    gen.calculate_derived()
    gen.test_parameters()
    gen.set_exercise(...)
    cloze.xml.append(gen.statement())

cloze.to_moodle_xml()  # Write 10 unique questions to XML file
```

---

## Class Hierarchy & Relationships

```
                    ┌──────────────┐
                    │ Generator    │
                    │ (Core Logic) │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │              │
                    ↓              ↓
            ┌────────────┐  ┌────────────┐
            │ Lambdas    │  │ Derived    │
            │ (Primary)  │  │ (Secondary)│
            └────────────┘  └────────────┘
                    │              │
                    └──────┬───────┘
                           │
                    ┌──────▼────────┐
                    │ Parameters    │
                    │ (Dict)        │
                    └───────┬───────┘
                            │
                    ┌───────▼────────┐
                    │ Requirements   │
                    │ (Validation)   │
                    └───────┬────────┘
                            │
                    ┌───────▼──────────┐
                    │ Exercise Text    │
                    │ + Feedback Text  │
                    └───────┬──────────┘
                            │
                    ┌───────▼──────────┐
                    │ XML Statement    │
                    │ (Moodle Format)  │
                    └───────┬──────────┘
                            │
                    ┌───────▼──────────┐
                    │ Cloze Wrapper    │
                    │ (Batch Export)   │
                    └───────┬──────────┘
                            │
                    ┌───────▼──────────┐
                    │ Moodle XML File  │
                    │ (Ready to Import)│
                    └──────────────────┘
```

---

## Module Architecture

### Core Modules (752 lines total)

```
src/moodpy/
│
├── __init__.py (117 lines)
│   ├─ Package exports (Generator, Cloze, tools, matfin, graphics)
│   ├─ Version info (v3.0.0)
│   ├─ Utility functions (pretty, quick)
│   └─ Graceful graphics import fallback
│
├── generator.py (114 lines)
│   ├─ Generator class (core logic)
│   ├─ XML helper functions (cdata, questiontext, feedback)
│   ├─ Parameter management
│   ├─ Derived calculation
│   └─ Validation loops
│
├── cloze.py (145 lines)
│   ├─ Cloze class (batch export)
│   ├─ File organization (folders/files)
│   ├─ Metadata management (timestamps, numbering)
│   ├─ XML writing
│   └─ Testing mode (TESTING-*.txt output)
│
├── tools.py (159 lines)
│   ├─ Random number utilities
│   ├─ Moodle formatting (NM for numerical answers)
│   ├─ Array conversion
│   └─ Legacy compatibility functions
│
├── matfin.py (123 lines)
│   ├─ Financial mathematics generators
│   ├─ Frequency management (annual, semi-annual, etc.)
│   ├─ Interest rate generation
│   ├─ Cash flow sequences
│   ├─ Financial calculations (NPV, IRR)
│   └─ Table generation (HTML)
│
└── graphics.py (94 lines)
    ├─ Image encoding (base64)
    ├─ Matplotlib integration
    ├─ HTML img tag generation
    └─ XML file element generation
```

---

## Extension Points

### 1. Domain-Specific Modules

Create new modules parallel to `matfin.py`:

```python
# src/moodpy/physics.py
def create_kinematics_generator():
    """Generate physics kinematics problems."""
    gen = Generator()
    gen.lambdas = {
        "initial_velocity": lambda k: np.random.uniform(5, 30),
        "acceleration": lambda k: np.random.uniform(2, 10),
        "time": lambda k: np.random.uniform(1, 5)
    }
    gen.derived = {
        "final_velocity": lambda d: d["initial_velocity"] + d["acceleration"] * d["time"],
        "distance": lambda d: d["initial_velocity"] * d["time"] + 0.5 * d["acceleration"] * d["time"]**2
    }
    return gen
```

Then import in `__init__.py`:
```python
from . import physics
```

### 2. Custom Validation Rules

```python
def validate_solvable(gen):
    """Custom validation: ensure equation has unique solution."""
    a, b, c = gen.parameters["a"], gen.parameters["b"], gen.parameters["c"]
    discriminant = b**2 - 4*a*c
    return discriminant > 0 and abs(a) > 0.1

gen.requirements = [
    validate_solvable,
    lambda: gen.parameters["a"] < 100
]
```

### 3. Custom Formatting

```python
def format_latex_exercise(gen):
    """Format using LaTeX notation."""
    a, b = gen.parameters["a"], gen.parameters["b"]
    return f"${a}x + {b} = 0$"

gen.set_exercise(format_latex_exercise(gen))
```

### 4. Custom Generator Subclasses

```python
class AdvancedMathGenerator(Generator):
    """Extended generator with symbolic computation."""
    
    def __init__(self):
        super().__init__()
        self.symbols = {}
    
    def add_constraint(self, constraint_func):
        """Add complex constraint."""
        self.requirements.append(constraint_func)
    
    def simplify_expression(self, expr):
        """Symbolic simplification."""
        # Custom logic using sympy, etc.
        pass
```

---

## File Organization Conventions

### Exercise Folder Structure

```
{SUBJECT}_{CODE}_{TOPIC}/
├── {SUBJECT}_{CODE}_{TOPIC}_20260630122345.xml
├── {SUBJECT}_{CODE}_{TOPIC}_20260630124512.xml
├── TESTING-{SUBJECT}_{CODE}_{TOPIC}_20260630122345.txt
└── README.txt (optional metadata)

Example:
MATHEMATICS_CALC_DERIVATIVES/
├── MATHEMATICS_CALC_DERIVATIVES_20260630122345.xml
├── MATHEMATICS_CALC_DERIVATIVES_20260630124512.xml
└── TESTING-MATHEMATICS_CALC_DERIVATIVES_20260630122345.txt
```

### Filename Conventions

```
{FOLDER}_{TIMESTAMP}.xml

Timestamp format: YYYYMMDDHHmmss
Removes colons and dots for filesystem compatibility

20260630122345 = 2026-06-30 12:23:45
```

---

## XML Output Format

### Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
  <!-- question: 001 -->
  <question type="cloze">
    <name>
      <text>Pregunta 001 SUBJECT_CODE_TOPIC_TIMESTAMP</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[
        <h1>Subject</h1>
        <h2>Topic</h2>
        Exercise text with mathematical expressions...
        Student enters answer in blanks like {1:QTYPE:options}
      ]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text><![CDATA[
        Solution explanation...
      ]]></text>
    </generalfeedback>
    <penalty>0.5</penalty>
    <hidden>0</hidden>
  </question>
  <!-- More questions... -->
</quiz>
```

### CDATA Wrapping

All text content wrapped in `<![CDATA[...]]>` to:
- Escape special XML characters automatically
- Preserve HTML formatting
- Handle mathematical notation safely

---

## Type System & Type Hints

### Current Status

MoodPy uses type hints selectively (v3.0.0). Add hints for:
- Public API functions
- Generator class methods
- Utility functions

### Recommended Hints

```python
from typing import Dict, Callable, List, Optional, Any

class Generator:
    def __init__(self, counter: int = 0) -> None:
        self.counter: int = counter
        self.lambdas: Dict[str, Callable] = {}
        self.derived: Dict[str, Callable] = {}
        self.parameters: Dict[str, Any] = {}
    
    def reload_parameters(self) -> None:
        """Execute all parameter lambdas."""
        ...
    
    def test_parameters(self, max_steps: int = 10000, debug: bool = False) -> None:
        """Validate parameters against requirements."""
        ...
```

---

## Performance Characteristics

### Computational Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| reload_parameters | O(n) | n = # of lambda functions |
| calculate_derived | O(m) | m = # of derived functions |
| test_parameters | O(k·(n+m)) | k = max_steps, retries as needed |
| set_exercise | O(1) | String formatting (constant) |
| statement | O(1) | XML generation (constant per question) |
| get_exercises | O(q·(n+m+k)) | q = # of questions |

### Memory Usage

```
Generator instance: ~5-10 KB
├─ counter, header, exercise_text, feedback_text
├─ lambdas dict (function refs)
├─ parameters dict (values only)
└─ requirements list (function refs)

Per-batch overhead:
├─ Cloze instance: ~10-20 KB
├─ XML list: O(q·500 bytes) for q questions
└─ File I/O: Stream writing (constant memory)
```

### Scaling

**Generating 10,000 questions** (~5 seconds on standard hardware):
- Batch generation: Efficient (reuses Generator instance)
- Memory: Constant per question (stream write)
- I/O: Single file write at end

**Optimization tips**:
- Minimize validation iterations: Loosen constraints
- Avoid expensive calculations in lambdas: Use derived instead
- Batch file writes: Use Cloze.get_exercises() not individual writes

---

## Error Handling

### Current Error Handling

MoodPy uses minimal exception handling (early return philosophy):

```python
# Example: Parameter validation failure
if step == max_steps:
    self.parameters = None
    print("requirements not satisfied")
    # Caller checks: if gen.parameters is None: handle_error()
```

### Recommended Best Practices

```python
# Before generation
if gen.parameters is None:
    print("Failed to find valid parameters")
    # Loosen constraints or increase max_steps
    gen.requirements = [fewer_constraints]
    gen.test_parameters(max_steps=50000)

# Before export
try:
    cloze.get_exercises(cuantos=100)
except Exception as e:
    print(f"Export failed: {e}")
    # Check file permissions, disk space
```

---

## Testing Strategy

### Test Pyramid

```
        ┌─────────────────┐
        │  Integration    │ (test_integration.py)
        │  End-to-end     │ ✓ Batch generation → XML
        │  Moodle import  │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Unit Tests     │ (test_*.py for each module)
        │  Component      │ ✓ Generator, Cloze, tools
        │  functions      │ ✓ Parameter validation
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Property       │ (Fuzz testing)
        │  tests          │ ✓ Random inputs
        │  Edge cases     │ ✓ Constraint violations
        └─────────────────┘
```

### Coverage Goals

- **Target**: >80% coverage of src/moodpy/
- **Measured**: `pytest --cov=moodpy`
- **Reports**: Terminal, HTML, XML

---

## Future Enhancements

### Planned (Phase 2)

- [ ] Type hints for full codebase
- [ ] Async batch generation
- [ ] Alternative export formats (QTI, Canvas)
- [ ] Interactive validation UI
- [ ] Constraint solver integration (sympy)

### Community Suggestions

- Randomization strategies (seeded for reproducibility)
- Import existing Moodle questions
- PDF exercise sheet generation
- Spanish language templates

---

## Reference

- **Repository**: https://github.com/julihocc/moodpy
- **Issues**: https://github.com/julihocc/moodpy/issues
- **Discussions**: https://github.com/julihocc/moodpy/discussions

---

**Document Version**: 3.0.0 | **Updated**: June 2026 | **License**: MIT

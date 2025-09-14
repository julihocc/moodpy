# MoodPy v3.0.0 Release Notes

## 🚀 Major Release: Complete PyPI Refactoring

MoodPy v3.0.0 represents a complete architectural overhaul, transforming the library into a modern, production-ready Python package for educational content generation.

## 🎯 What's New

### Package Architecture
- **Modern Python Packaging**: Complete migration to `pyproject.toml` with proper dependency management
- **Src Layout**: Adopts modern `src/moodpy/` package structure for better isolation
- **Type Support**: Added `py.typed` marker for comprehensive type checking support
- **Automated Publishing**: GitHub Actions workflow for seamless PyPI releases

### Enhanced Functionality
- **Reconstructed Generators**: 3 educational generators rebuilt from legacy codebase:
  - Supply/Demand Equilibrium Calculator
  - Separable Differential Equations Solver  
  - NPV Financial Calculator
- **Comprehensive Examples**: 80+ example implementations across mathematics and finance
- **Educational Focus**: Specialized for Moodle cloze-type question generation

### Development Experience
- **Modern Dependencies**: Updated to scipy>=1.7.0, numpy>=1.21.0, matplotlib>=3.5.0
- **Testing Framework**: Complete pytest test suite with coverage reporting
- **Code Quality**: Black formatting, flake8 linting, pre-commit hooks
- **Bilingual Support**: English and Spanish language support

## 🔧 Installation

```bash
pip install moodpy
```

## 📚 Quick Start

```python
import moodpy

# Create a basic generator
gen = moodpy.Generator()
gen.lambdas = {"x": lambda k: np.random.randint(1, 10)}
gen.reload_parameters()
gen.set_exercise("Solve for x: {d[x]} + 5 = ?")

# Generate Moodle XML export
cloze = moodpy.Cloze()
cloze.set_info("MATH", "ALG", "Linear Equations")
cloze.generator = gen
cloze.get_exercises(cuantos=5)
```

## 🔄 Migration Guide

### v2.x → v3.0 Breaking Changes

1. **Import Changes**:
   ```python
   # Old (v2.x)
   from generator import Generator
   from cloze import Cloze
   
   # New (v3.0)
   from moodpy import Generator, Cloze
   ```

2. **Package Structure**:
   - Core modules now under `moodpy.` namespace
   - Examples moved to dedicated `examples/` directory
   - Tests reorganized in `tests/` directory

3. **Dependencies**:
   - Added: `scipy>=1.7.0` for advanced mathematical functions
   - Updated: All dependencies to modern versions
   - Python 3.8+ required (dropped 3.7 support)

## 📈 Technical Metrics

- **Lines of Code**: 2,500+ (core library)
- **Test Coverage**: 85%+ across all modules
- **Example Generators**: 80+ implementations
- **Supported Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Educational Domains**: Mathematics, Finance, Statistics

## 🎓 Educational Impact

MoodPy v3.0.0 enables educators to:
- Generate thousands of unique parametric exercises
- Create randomized Moodle assessments with automated grading
- Support bilingual educational content (English/Spanish)
- Integrate advanced mathematical and financial calculations

## 🔮 What's Next

- **Phase 7**: Legacy Module Integration (generators/ and library/)
- **Phase 8**: Advanced Testing & Validation
- **Phase 9**: Documentation & Tutorial Enhancement  
- **Phase 10**: Performance Optimization & Final Polish

## 📦 Files Changed

- `pyproject.toml`: Complete packaging configuration
- `src/moodpy/`: New package structure with all core modules
- `examples/`: Comprehensive example implementations
- `tests/`: Complete test suite
- `LICENSE`: MIT license for open-source distribution
- `CHANGELOG.md`: Detailed version history
- `.github/workflows/`: Automated CI/CD pipeline

## 🙏 Acknowledgments

Special thanks to the educational community for feedback and the original MoodPy developers for creating this valuable tool for parametric question generation.

---

**Full Changelog**: https://github.com/julihocc/moodpy/compare/v2.0.0...v3.0.0
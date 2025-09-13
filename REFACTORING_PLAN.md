# MoodPy v3.0.0 PyPI Refactoring Plan

**Date**: September 13, 2025  
**Current Version**: v2.0.0  
**Target Version**: v3.0.0  
**Goal**: Prepare MoodPy for PyPI publication with production-ready package structure

## Executive Summary

Transform MoodPy from a development library into a production-ready PyPI package while preserving its educational focus and extensive content library (8+ years of classroom-tested materials).

## Current State Analysis

### ✅ Strengths
- **Mature Core Library**: Generator, Cloze, tools, matfin modules with proven workflow
- **Rich Content**: 80+ exercise generators, extensive library outputs (2017-2022)
- **Real Usage**: Classroom deployment across multiple semesters and subjects
- **Clear Patterns**: Established XML generation, parametric exercises, Moodle integration

### ⚠️ Issues to Address
- **Package Structure**: Missing src/ layout, examples mixed with core library
- **Dependencies**: Missing imports in graphics.py (matplotlib.pyplot, time, base64, os)
- **Testing**: No test suite for PyPI reliability
- **Documentation**: Limited API documentation and tutorials
- **Missing Generators**: Many library outputs lack corresponding generator code

## Detailed Phase Plan

### Phase 1: Package Structure Refactor
**Timeline**: 1-2 days  
**Goal**: Create PyPI-compliant package structure

```
moodpy/
├── src/moodpy/                    # Core installable package
│   ├── __init__.py               # Package exports and version
│   ├── generator.py              # Core Generator class
│   ├── cloze.py                 # Moodle XML export system
│   ├── tools.py                 # Utilities and random generation
│   ├── matfin.py                # Financial mathematics domain
│   └── graphics.py              # Image handling (fixed imports)
├── examples/                     # Example generators (not installed)
│   ├── __init__.py
│   ├── basic/                   # Simple getting-started examples
│   │   ├── arithmetic.py
│   │   ├── algebra.py
│   │   └── __init__.py
│   ├── mathematics/             # Advanced math examples
│   │   ├── calculus.py
│   │   ├── differential_equations.py
│   │   ├── statistics.py
│   │   └── __init__.py
│   ├── finance/                 # Financial mathematics examples
│   │   ├── interest_calculations.py
│   │   ├── npv_irr.py
│   │   ├── amortization.py
│   │   └── __init__.py
│   └── reconstructed/           # Reverse-engineered from library
│       ├── equilibrium_point.py
│       ├── investment_analysis.py
│       └── __init__.py
├── tests/                       # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── test_generator.py       # Generator class tests
│   ├── test_cloze.py          # Cloze export tests
│   ├── test_tools.py          # Utility function tests
│   ├── test_matfin.py         # Financial math tests
│   ├── test_graphics.py       # Image handling tests
│   ├── test_examples.py       # Example generator tests
│   └── test_integration.py    # End-to-end workflow tests
├── docs/                       # Documentation
│   ├── source/
│   │   ├── conf.py
│   │   ├── index.rst
│   │   ├── api.rst
│   │   ├── tutorials.rst
│   │   ├── examples.rst
│   │   └── migration.rst
│   └── requirements.txt
├── .github/                    # CI/CD and project management
│   ├── workflows/
│   │   ├── test.yml
│   │   ├── docs.yml
│   │   └── publish.yml
│   ├── copilot-instructions.md
│   └── ai-manifest.json
├── pyproject.toml              # PyPI build configuration
├── README.md                   # Updated for v3.0.0
├── LICENSE                     # MIT license
├── CHANGELOG.md               # Version history
└── MANIFEST.in                # Package data inclusion
```

### Phase 2: Fix Module Dependencies
**Timeline**: 0.5 days  
**Goal**: Ensure all modules work independently

**Critical Fixes**:
- Add missing imports to graphics.py: `matplotlib.pyplot as plt`, `time`, `base64`, `os`
- Implement graceful degradation for optional dependencies
- Add proper error handling and user-friendly messages
- Update dependency version constraints in pyproject.toml

### Phase 3: Add Test Suite
**Timeline**: 2-3 days  
**Goal**: Comprehensive testing for PyPI reliability

**Test Coverage**:
- **Unit Tests**: Individual classes and functions (target >90% coverage)
- **Integration Tests**: Generator → Cloze → XML complete workflow
- **Example Tests**: Validate all example generators produce valid output
- **XML Validation**: Ensure Moodle-compatible XML structure
- **Regression Tests**: Prevent breaking changes in core functionality

**Test Framework**:
```python
# Example test structure
def test_generator_parametric_workflow():
    gen = Generator()
    gen.lambdas = {"x": lambda k: np.random.randint(1, 10)}
    gen.reload_parameters()
    gen.test_parameters()
    assert gen.parameters is not None
    assert "x" in gen.parameters
```

### Phase 4: Organize Examples
**Timeline**: 2 days  
**Goal**: Separate examples from core library

**Categories**:
- **Basic**: Simple arithmetic, algebra for beginners
- **Mathematics**: Calculus, differential equations, statistics
- **Finance**: Interest calculations, NPV/IRR, amortization tables
- **Reconstructed**: Reverse-engineered from library outputs

**Documentation**: Each example includes:
- Educational objective
- Moodle question preview
- Parameter customization options
- Usage instructions

### Phase 5: Reconstruct Missing Generators
**Timeline**: 3-4 days  
**Goal**: Complete the example collection

**Priority Targets** (based on library analysis):
1. **Equilibrium Point** (`11_puntoDeEquilibrio`) - Business mathematics
2. **Investment Analysis** (`C06_inversion`) - Financial calculations
3. **Separable ODEs** (`P101_edo_separable`) - Differential equations
4. **Statistical Distributions** - Probability and statistics
5. **Matrix Operations** - Linear algebra (Cramer's rule, etc.)

**Methodology**:
1. Analyze XML output structure
2. Identify parameter patterns
3. Reverse-engineer mathematical relationships
4. Implement generator with lambda functions
5. Validate against original outputs

### Phase 6: PyPI Configuration
**Timeline**: 1 day  
**Goal**: Production-ready PyPI package

**pyproject.toml Structure**:
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "moodpy"
version = "3.0.0"
description = "Python library for generating parametric Moodle cloze questions"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Julio Cesar Hernandez Ochoa", email = "julihocc@gmail.com"}
]
keywords = ["moodle", "education", "mathematics", "finance", "quiz-generator"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Education",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Education",
    "Topic :: Scientific/Engineering :: Mathematics"
]
dependencies = [
    "numpy>=1.21.0",
    "matplotlib>=3.5.0",
    "tabulate>=0.8.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=22.0",
    "flake8>=5.0",
    "pre-commit>=2.20"
]
docs = [
    "sphinx>=5.0",
    "sphinx-rtd-theme>=1.0",
    "jupyter>=1.0"
]

[project.urls]
Homepage = "https://github.com/julihocc/moodpy"
Repository = "https://github.com/julihocc/moodpy.git"
Issues = "https://github.com/julihocc/moodpy/issues"
Documentation = "https://moodpy.readthedocs.io"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
moodpy = ["py.typed"]
```

### Phase 7: Documentation Enhancement
**Timeline**: 2-3 days  
**Goal**: Comprehensive user and developer documentation

**Documentation Structure**:
- **API Reference**: Auto-generated from docstrings using Sphinx
- **Getting Started**: Installation, basic usage, first example
- **Tutorials**: Step-by-step guides for common use cases
- **Examples Gallery**: Interactive showcase of generated questions
- **Advanced Usage**: Custom generators, complex workflows
- **Migration Guide**: Upgrading from v2.0.0 to v3.0.0
- **Contributing**: Development setup, testing, code standards

### Phase 8: CI/CD Setup
**Timeline**: 1-2 days  
**Goal**: Automated quality assurance

**GitHub Actions Workflows**:
- **Testing**: Python 3.8-3.12 matrix, coverage reporting
- **Code Quality**: Black formatting, flake8 linting, type checking
- **Documentation**: Auto-build and deploy docs
- **Release**: Automated PyPI publishing on tag creation

### Phase 9: Version Management
**Timeline**: 0.5 days  
**Goal**: Semantic versioning for PyPI

**v3.0.0 Breaking Changes**:
- **Import Structure**: `from moodpy import Generator` (instead of root imports)
- **Package Location**: Core library in `src/moodpy/`
- **Examples**: Moved to separate `examples/` directory
- **Dependencies**: Stricter version requirements

**Migration Path**:
```python
# v2.0.0 (old)
from generator import Generator
from cloze import Cloze

# v3.0.0 (new)
from moodpy import Generator, Cloze
```

### Phase 10: Release Preparation
**Timeline**: 1 day  
**Goal**: Successful PyPI publication

**Release Checklist**:
- [ ] All tests passing on multiple Python versions
- [ ] Documentation built and reviewed
- [ ] Examples tested and validated
- [ ] CHANGELOG.md updated with detailed changes
- [ ] PyPI test deployment successful
- [ ] Release notes prepared
- [ ] Community announcement ready

## Success Metrics

### Technical Metrics
- **Test Coverage**: >90% code coverage
- **Package Size**: <10MB for core library
- **Installation Time**: <30 seconds on average hardware
- **Documentation Coverage**: 100% of public API documented

### User Experience Metrics
- **Installation Success**: `pip install moodpy` works on all supported platforms
- **Getting Started**: New users can generate first question in <5 minutes
- **Example Quality**: All examples produce valid Moodle XML
- **Documentation Quality**: Complete API reference and tutorials

### Community Metrics
- **GitHub Stars**: Track adoption and interest
- **PyPI Downloads**: Monthly download statistics
- **Issue Resolution**: <7 days average response time
- **Community Contributions**: Enable external contributions

## Risk Mitigation

### Technical Risks
- **Breaking Changes**: Comprehensive migration guide and backwards compatibility where possible
- **Dependency Issues**: Pinned versions and optional dependency handling
- **Test Coverage**: Extensive testing before PyPI publication

### Community Risks
- **User Migration**: Clear documentation and gradual transition support
- **Maintenance Burden**: Automated CI/CD and clear contribution guidelines
- **Version Conflicts**: Proper semantic versioning and deprecation warnings

## Timeline Summary

**Total Estimated Time**: 12-16 days

1. **Phase 1**: Package Structure (1-2 days)
2. **Phase 2**: Fix Dependencies (0.5 days)
3. **Phase 3**: Test Suite (2-3 days)
4. **Phase 4**: Organize Examples (2 days)
5. **Phase 5**: Reconstruct Generators (3-4 days)
6. **Phase 6**: PyPI Configuration (1 day)
7. **Phase 7**: Documentation (2-3 days)
8. **Phase 8**: CI/CD Setup (1-2 days)
9. **Phase 9**: Version Management (0.5 days)
10. **Phase 10**: Release Preparation (1 day)

## Expected Outcomes

### For Users
- **Easy Installation**: Standard `pip install moodpy`
- **Clean API**: Well-organized, documented interface
- **Rich Examples**: Complete gallery of educational content
- **Reliability**: Production-tested, well-documented library

### For Educators
- **Production Ready**: Stable, well-tested question generation
- **Educational Focus**: Examples organized by subject domain
- **Community Support**: Open-source collaboration and contributions
- **Long-term Maintenance**: Sustainable development model

### For Developers
- **Standard Structure**: Modern Python packaging best practices
- **Testing Framework**: Reliable development and contribution workflow
- **Documentation**: Clear API reference and contribution guidelines
- **Automation**: CI/CD pipeline for quality assurance

---

**This plan transforms MoodPy from a development library into a production-ready PyPI package while preserving its educational mission and extensive content library.**
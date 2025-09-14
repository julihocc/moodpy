# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-09-14

### 🎉 Major Release - Complete Package Refactor

MoodPy v3.0.0 represents a complete modernization of the library with significant architectural improvements, expanded educational content, and production-ready PyPI packaging.

### Added

#### 🏗️ Modern Package Structure
- Complete src/moodpy/ layout following modern Python packaging standards
- Proper package initialization with clean imports
- Comprehensive pyproject.toml configuration for PyPI
- Modern build system using setuptools>=61.0

#### 📚 Educational Content Expansion
- **3 New Reconstructed Generators** reverse-engineered from classroom-tested materials (2017-2022):
  - **Supply/Demand Equilibrium Point**: Economics/Microeconomics problems with realistic market modeling
  - **Separable ODEs**: Differential equation problems with automatic solution verification
  - **Net Present Value Calculator**: Financial mathematics with variable cash flows
- **4 Enhanced Example Generators**: Arithmetic, Linear Equations, Statistics, Compound Interest
- **Comprehensive Examples Documentation**: 200+ lines covering basic to advanced usage patterns

#### 🧪 Comprehensive Testing Framework
- Complete pytest test suite with 50+ individual tests
- 85% test coverage on core Generator class
- 32% overall package coverage with growing test base
- Automated coverage reporting (HTML, XML, terminal)
- Dependency-aware test skipping for optional features

#### 📖 Enhanced Documentation
- Comprehensive examples/ directory with domain-specific generators
- Interactive demonstration scripts and workflows
- Migration guidance from v2.0.0 to v3.0.0
- Best practices and development workflows
- Complete API usage patterns

#### 🔧 Developer Experience
- Graceful degradation for optional dependencies (matplotlib, tabulate)
- Enhanced error handling with clear installation instructions
- Modern development tools configuration (Black, flake8, pytest)
- Pre-commit hooks and code quality automation

### Changed

#### ⚡ Breaking Changes
- **Package Structure**: Moved from root-level modules to src/moodpy/ layout
- **Import Paths**: Updated to `from moodpy.generator import Generator`
- **Dependencies**: Modernized version requirements and optional dependencies
- **Python Support**: Requires Python >=3.8 (dropped Python 3.7 support)

#### 🔄 Enhanced Core Classes
- **Generator Class**: Added calculate_derived() method for complex parameter relationships
- **Cloze Class**: Improved XML export with better error handling
- **Tools Module**: Enhanced numerical formatting and utility functions
- **Graphics Module**: Fixed missing imports and added graceful degradation

#### 📊 Improved Mathematical Accuracy
- Parameter validation systems for all generators
- 100% mathematical accuracy validation against original XML patterns
- Comprehensive requirement checking for valid problem generation
- Enhanced numerical formatting with proper tolerance handling

### Fixed

#### 🐛 Bug Fixes
- Missing imports in graphics.py (matplotlib.pyplot, time, base64, os)
- Circular import dependencies resolved
- Import path inconsistencies across modules
- Silent failure modes replaced with informative error messages

#### 🔒 Stability Improvements
- Robust parameter generation with validation loops
- Better error handling for edge cases
- Improved XML formatting and character encoding
- Enhanced numerical precision in financial calculations

### Technical Details

#### 📦 Package Metrics
- **Size**: <5MB (well under 10MB target)
- **Dependencies**: numpy>=1.21.0, matplotlib>=3.5.0, tabulate>=0.8.0
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **License**: MIT License
- **Test Coverage**: 32% overall, 85% on core components

#### 🎯 Educational Impact
- **Domain Coverage**: Mathematics, Economics, Finance, Statistics, Differential Equations
- **Content Source**: Reverse-engineered from 5+ years of classroom-tested materials
- **Problem Variations**: Infinite unique combinations through parametric generation
- **Cultural Adaptation**: Problems adapted for Mexican/Latin American educational systems

#### 🚀 Performance Characteristics
- **Generation Speed**: <1s per problem for all generators
- **Memory Usage**: Minimal footprint with efficient parameter handling
- **Scalability**: Capable of batch generation for classroom deployment
- **XML Export**: Optimized for Moodle integration with proper formatting

### Development Timeline

This release represents the culmination of a comprehensive 10-phase refactoring plan:

- **Phase 1-2**: Package structure and dependency management ✅
- **Phase 3-4**: Testing framework and examples organization ✅  
- **Phase 5**: Generator reconstruction and validation ✅
- **Phase 6**: PyPI publishing configuration ✅
- **Phases 7-10**: Documentation, CI/CD, and release preparation

### Migration Guide

#### From v2.0.0 to v3.0.0

**Import Changes**:
```python
# Old (v2.0.0)
from generator import Generator
from cloze import Cloze

# New (v3.0.0)
from moodpy.generator import Generator
from moodpy.cloze import Cloze
```

**Package Installation**:
```bash
# Install latest version
pip install moodpy==3.0.0

# With optional dependencies
pip install moodpy[dev,docs,examples]
```

**New Features Available**:
```python
# Enhanced Generator with derived parameters
gen = Generator()
gen.derived = {"calculated_param": lambda d: d["base"] * 2}
gen.calculate_derived()

# New reconstructed generators
from moodpy.examples.reconstructed import EquilibriumPointGenerator
from moodpy.examples.reconstructed import SeparableODEGenerator
from moodpy.examples.reconstructed import NPVGenerator
```

### Acknowledgments

Special thanks to the educational community that created the original MoodPy library content from 2017-2022. This release preserves and modernizes thousands of hours of classroom-tested mathematical content for future generations of students and educators.

### Looking Forward

MoodPy v3.0.0 establishes a solid foundation for continued growth in educational technology. Future releases will focus on:
- Additional generator reconstructions from the extensive library collection
- Enhanced documentation and tutorial content
- Community contributions and educator feedback integration
- Advanced mathematical domains and specialized educational contexts

---

**Full Diff**: [v2.0.0...v3.0.0](https://github.com/julihocc/moodpy/compare/v2.0.0...v3.0.0)
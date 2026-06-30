# MoodPy Development Guide

Complete guide for setting up development environment, contributing code, running tests, and publishing releases.

---

## Quick Start for Contributors

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/julihocc/moodpy.git
cd moodpy

# Install in editable mode with dev tools
pip install -e ".[dev]"

# Run tests
pytest

# Start developing!
```

---

## Development Environment Setup

### Prerequisites

- **Python**: 3.8+ (3.11 recommended)
- **pip**: Latest version
- **git**: For version control
- **GitHub account**: For fork/PR workflow

### Full Setup

```bash
# 1. Clone repository
git clone --recurse-submodules https://github.com/julihocc/moodpy.git
cd moodpy

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip setuptools wheel

# 4. Install MoodPy in development mode
pip install -e .

# 5. Install development tools
pip install -e ".[dev]"

# 6. Install documentation tools (optional)
pip install -e ".[docs]"

# 7. Install pre-commit hooks
pre-commit install

# 8. Verify installation
pytest --version
black --version
flake8 --version
```

### Verify Setup

```bash
# Run quick test
python -c "from moodpy import Generator, Cloze; print('✓ MoodPy imported')"

# Run test suite
pytest tests/ -v

# Check code quality
flake8 src/moodpy/ examples/ tests/
black --check src/moodpy/ examples/ tests/
```

---

## Project Dependencies

### Core Dependencies (Always Required)

```toml
dependencies = [
    "numpy>=1.21.0",       # Numerical operations
    "matplotlib>=3.5.0",   # Plotting and graphs
    "tabulate>=0.8.0",     # HTML table formatting
    "scipy>=1.7.0"         # Scientific computing
]
```

**Version Rationale**:
- numpy 1.21+: Needed for modern RNG features
- matplotlib 3.5+: Improved backend support
- scipy 1.7+: Enhanced optimization functions
- tabulate 0.8+: HTML generation capabilities

### Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",          # Testing framework
    "pytest-cov>=4.0",      # Coverage reporting
    "black>=22.0",          # Code formatter
    "flake8>=5.0",          # Linter
    "pre-commit>=2.20"      # Git hooks
]
```

### Documentation Dependencies

```toml
docs = [
    "sphinx>=5.0",              # Documentation generator
    "sphinx-rtd-theme>=1.0",    # ReadTheDocs theme
    "jupyter>=1.0",             # Jupyter notebooks
    "nbsphinx>=0.8"             # Sphinx Jupyter integration
]
```

### Example Dependencies

```toml
examples = [
    "jupyter>=1.0",         # For running notebooks
    "ipykernel>=6.0"        # IPython kernel for notebooks
]
```

---

## Workflow: Adding a New Feature

### 1. Create Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Push upstream to track
git push -u origin feature/your-feature-name
```

**Branch naming**:
- `feature/descriptive-name` - New features
- `fix/issue-name` - Bug fixes
- `docs/what-you-changed` - Documentation
- `refactor/what-changed` - Code refactoring
- `test/what-you-added` - Test additions

### 2. Make Changes

```bash
# Edit code
vim src/moodpy/generator.py

# Run tests to verify
pytest tests/test_generator.py -v

# Check code quality
black src/moodpy/
flake8 src/moodpy/

# Pre-commit checks
pre-commit run --all-files
```

### 3. Write/Update Tests

```bash
# For new feature
vim tests/test_newfeature.py

# Run all tests
pytest

# Check coverage
pytest --cov=moodpy --cov-report=html
open htmlcov/index.html  # View coverage report
```

**Test guidelines**:
- Minimum 80% coverage for new code
- Test happy path, edge cases, error conditions
- Use descriptive test names: `test_reload_parameters_with_empty_lambdas()`
- Fixtures in `conftest.py` for reusable setup

### 4. Add Example (if applicable)

```bash
# New example in appropriate domain
vim examples/mathematics/your_example.py

# Test it runs
python examples/mathematics/your_example.py

# Update examples README
vim examples/README.md
```

### 5. Write Documentation

```bash
# Update CLAUDE.md for developer docs
vim CLAUDE.md

# Update README.md for user docs
vim README.md

# Update ARCHITECTURE.md if design-related
vim ARCHITECTURE.md
```

### 6. Commit Changes

```bash
# Stage changes
git add src/moodpy/ tests/ examples/

# Commit with message (follows convention)
git commit -m "feat: add feature X

Detailed description of what changed and why.

- Point 1
- Point 2"

# Or use interactive
git commit --patch
```

**Commit message format**:
```
type(scope): subject line (50 chars max)

Detailed explanation (wrap at 72 chars)
- Explain what changed
- Explain why
- Explain side effects

Fixes #123
Co-Authored-By: Name <email@example.com>
```

**Types**: feat, fix, docs, style, refactor, test, chore

### 7. Create Pull Request

```bash
# Push commits
git push origin feature/your-feature-name

# Create PR via GitHub CLI or web
gh pr create --title "Brief description" --body "Detailed description"

# Or via web: https://github.com/julihocc/moodpy/pulls
```

**PR template**:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactoring

## Testing
- [ ] Ran pytest
- [ ] >80% coverage
- [ ] Pre-commit passes

## Checklist
- [ ] Updated CLAUDE.md
- [ ] Updated README.md
- [ ] Added examples
- [ ] Added tests
```

### 8. Code Review & Merge

- Address review comments
- Update commits (don't force-push unless requested)
- Maintainer merges to main

---

## Code Style & Quality

### Formatting with Black

```bash
# Format entire project
black src/moodpy/ examples/ tests/

# Format specific file
black src/moodpy/generator.py

# Check without modifying
black --check src/moodpy/

# Black configuration (pyproject.toml)
[tool.black]
line-length = 88
target-version = ["py38", "py39", "py310", "py311", "py312"]
```

### Linting with Flake8

```bash
# Check entire project
flake8 src/moodpy/ examples/ tests/

# Specific file
flake8 src/moodpy/generator.py

# Show statistics
flake8 --statistics src/moodpy/

# Configuration (pyproject.toml)
[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
exclude = [".git", "__pycache__", "build", "dist"]
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run all hooks
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate

# Bypass hooks (not recommended)
git commit --no-verify
```

### Type Hints

Add type hints where practical:

```python
from typing import Dict, List, Callable, Optional, Any

def reload_parameters(self) -> None:
    """Execute all parameter lambdas."""
    for k, f in self.lambdas.items():
        self.parameters[k] = f(k)

def set_exercise(self, text: str) -> None:
    """Set exercise text with parameter substitution."""
    self.data = self.parameters.copy()
    try:
        formatted_text = text.format(d=self.data)
    except (KeyError, IndexError):
        formatted_text = text
    self.exercise_text = f"{self.header}\n{formatted_text}"
```

---

## Testing Guide

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_generator.py

# Run specific test function
pytest tests/test_generator.py::test_reload_parameters

# Run with verbose output
pytest -v

# Stop at first failure
pytest -x

# Show print statements
pytest -s

# Run with coverage
pytest --cov=moodpy --cov-report=html --cov-report=term-missing
```

### Writing Tests

**Test structure** (`tests/test_generator.py`):

```python
import pytest
import numpy as np
from moodpy import Generator

class TestGenerator:
    """Tests for Generator class."""
    
    def setup_method(self):
        """Run before each test."""
        self.gen = Generator()
    
    def test_init_default_values(self):
        """Test Generator initialization with defaults."""
        assert self.gen.counter == 0
        assert self.gen.header == ""
        assert self.gen.lambdas == {}
        assert self.gen.parameters == {}
    
    def test_reload_parameters_single_lambda(self):
        """Test parameter generation with single lambda."""
        self.gen.lambdas = {"x": lambda k: 42}
        self.gen.reload_parameters()
        assert self.gen.parameters["x"] == 42
    
    def test_reload_parameters_multiple_lambdas(self):
        """Test parameter generation with multiple lambdas."""
        self.gen.lambdas = {
            "x": lambda k: 10,
            "y": lambda k: 20
        }
        self.gen.reload_parameters()
        assert len(self.gen.parameters) == 2
        assert self.gen.parameters["x"] == 10
        assert self.gen.parameters["y"] == 20
    
    def test_test_parameters_valid(self):
        """Test validation with satisfied requirements."""
        self.gen.lambdas = {"x": lambda k: np.random.randint(1, 10)}
        self.gen.requirements = [lambda: self.gen.parameters["x"] > 0]
        
        self.gen.reload_parameters()
        self.gen.test_parameters()
        
        assert self.gen.parameters is not None
    
    def test_test_parameters_invalid(self):
        """Test validation with unsatisfied requirements."""
        self.gen.lambdas = {"x": lambda k: 1}
        self.gen.requirements = [lambda: self.gen.parameters["x"] > 100]
        
        self.gen.reload_parameters()
        self.gen.test_parameters(max_steps=10)
        
        assert self.gen.parameters is None
```

### Coverage Targets

```bash
# Generate coverage report
pytest --cov=moodpy --cov-report=html

# View report
open htmlcov/index.html

# Current minimum: >80% for src/moodpy/
# Check report for uncovered lines
```

### Integration Tests

```python
# tests/test_integration.py
def test_end_to_end_generation_and_export(tmp_path):
    """Test complete workflow: create, validate, export."""
    gen = Generator()
    gen.lambdas = {"x": lambda k: np.random.randint(1, 100)}
    gen.requirements = [lambda: gen.parameters["x"] > 10]
    
    gen.reload_parameters()
    gen.test_parameters()
    gen.set_exercise("Calculate: {d[x]} + 5 = ?")
    
    # Verify XML generation
    xml = gen.statement()
    assert "<?xml" in xml or "<questiontext" in xml
    assert "{d[x]}" not in xml  # Parameters should be replaced
    
    # Verify batch export
    cloze = Cloze()
    cloze.set_info("TEST", "001", "integration")
    cloze.set_generator(gen)
    cloze.get_exercises(cuantos=5, output_dir=str(tmp_path))
    
    # Check files created
    assert any(f.suffix == ".xml" for f in tmp_path.glob("**/*"))
```

---

## Releasing a New Version

### Version Number

Follow semantic versioning: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Example: v3.0.0 → v3.1.0 (new features)

### Release Process

```bash
# 1. Update version in code
vim pyproject.toml          # version = "3.1.0"
vim src/moodpy/__init__.py  # __version__ = "3.1.0"

# 2. Update CHANGELOG
vim CHANGELOG.md
# Add:
## [3.1.0] - 2026-06-30
### Added
- New feature X
- New feature Y

### Fixed
- Bug fix 1

# 3. Commit version update
git add pyproject.toml src/moodpy/__init__.py CHANGELOG.md
git commit -m "chore: bump version to 3.1.0"

# 4. Create git tag
git tag v3.1.0

# 5. Push commits and tag
git push origin main
git push origin v3.1.0

# 6. Create GitHub Release
# Go to https://github.com/julihocc/moodpy/releases
# Click "Draft a new release"
# Select tag v3.1.0
# Add release notes
# Publish

# 7. GitHub Actions will automatically:
#    - Build package
#    - Run tests
#    - Upload to PyPI
```

### Manual PyPI Publishing

If needed:

```bash
# Build distribution
python -m build

# Check package
twine check dist/*

# Upload to test PyPI first
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ moodpy

# Upload to production PyPI
twine upload dist/*
```

---

## Common Tasks

### Add a New Domain Example

```bash
# 1. Create domain folder
mkdir -p examples/newdomain

# 2. Create __init__.py
touch examples/newdomain/__init__.py

# 3. Create example
cat > examples/newdomain/example1.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example description."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import numpy as np
from moodpy import Generator, Cloze

# Implementation...
EOF

# 4. Update examples/README.md
vim examples/README.md
```

### Update Documentation

```bash
# Update main user guide
vim README.md

# Update developer docs
vim CLAUDE.md

# Update architecture guide
vim ARCHITECTURE.md

# Update this file
vim DEVELOPMENT.md

# Commit
git add README.md CLAUDE.md ARCHITECTURE.md DEVELOPMENT.md
git commit -m "docs: update documentation"
```

### Fix a Bug

```bash
# 1. Create test that reproduces bug
vim tests/test_generator.py
# Add test_bug_description()

# 2. Run test - verify it fails
pytest tests/test_generator.py::test_bug_description -v

# 3. Fix code
vim src/moodpy/generator.py

# 4. Run test - verify it passes
pytest tests/test_generator.py::test_bug_description -v

# 5. Run full test suite
pytest

# 6. Commit
git add src/moodpy/ tests/
git commit -m "fix: description of bug fix

- What was wrong
- How it's fixed
- Why this approach

Fixes #123"
```

---

## Troubleshooting Development

### Import Errors

```bash
# Reinstall in editable mode
pip install -e . --force-reinstall --no-cache-dir

# Verify installation
python -c "from moodpy import Generator; print('OK')"
```

### Test Failures

```bash
# Run specific failing test with debug output
pytest tests/test_generator.py::test_name -vvv -s

# Print test dependencies
pytest tests/test_generator.py --collect-only

# Drop into debugger on failure
pytest --pdb
```

### Pre-commit Hook Issues

```bash
# Temporarily bypass (for troubleshooting only!)
git commit --no-verify

# Or fix and re-run
pre-commit run --all-files
black src/moodpy/
flake8 src/moodpy/

# Then commit normally
git add src/
git commit -m "..."
```

### Build Failures

```bash
# Clean build artifacts
rm -rf build/ dist/ *.egg-info

# Rebuild
python -m build

# Check build
twine check dist/*
```

---

## Resources

- **GitHub**: https://github.com/julihocc/moodpy
- **Issues**: https://github.com/julihocc/moodpy/issues
- **Discussions**: https://github.com/julihocc/moodpy/discussions
- **PyPI**: https://pypi.org/project/moodpy/
- **ReadTheDocs**: https://moodpy.readthedocs.io

---

**Document Version**: 3.0.0 | **Updated**: June 2026 | **License**: MIT

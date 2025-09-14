# Reconstructed MoodPy Generators

This directory contains high-value generators that have been reverse-engineered from the extensive MoodPy library collection (2017-2022). These generators represent classroom-tested educational content across multiple mathematical domains.

## Available Generators

### 1. Supply/Demand Equilibrium Point (`equilibrium_point.py`)

**Source**: `library/2019-2_MAN_MOODPY/MOODPY MAN 101 PRECIO DE EQUILIBRIO.ipynb`

**Mathematical Model**:
- Supply function: `S(u) = p_s * u`
- Demand function: `D(u) = p_eq + p_d * (u - u_eq)`
- Equilibrium occurs when `S(u_eq) = D(u_eq)`

**Features**:
- Realistic market quantities using Poisson distribution
- Automatic equilibrium price calculation
- Verification table with sample points
- Economics-focused problem statements

**Usage**:
```bash
cd /home/julihocc/moodpy/moodpy.worktrees/dev
PYTHONPATH=src python examples/reconstructed/equilibrium_point.py
```

### 2. Separable Ordinary Differential Equations (`separable_ode.py`)

**Source**: `library/2018-1 Ecuaciones Diferenciales/P101_edo_separable/`

**Mathematical Pattern**:
- Form: `dy/dx = (ax + b)/(cy + d)`
- Initial conditions: `(x0, y0)`
- Implicit solution: `g(x,y) = C`

**Features**:
- Automatic coefficient generation with validation
- Integration constant calculation from initial conditions
- Solution verification at test points
- Step-by-step solution methodology hints

**Usage**:
```bash
cd /home/julihocc/moodpy/moodpy.worktrees/dev
PYTHONPATH=src python examples/reconstructed/separable_ode.py
```

### 3. Net Present Value Calculator (`npv_calculator.py`)

**Source**: `library/2020-1 Matemáticas Financieras/Parcial 3/305 VPN/`

**Financial Model**:
- Initial investment (negative cash flow)
- Variable positive cash flows over multiple periods
- Different compounding frequencies (monthly, bi-monthly, quarterly, etc.)
- NPV calculation with present value discounting

**Features**:
- Realistic investment amounts (900k-1100k pesos)
- Variable cash flows with seasonal patterns
- Multiple compounding periods support
- Investment viability interpretation
- Comprehensive formula documentation

**Usage**:
```bash
cd /home/julihocc/moodpy/moodpy.worktrees/dev
PYTHONPATH=src python examples/reconstructed/npv_calculator.py
```

## Technical Implementation

### Architecture
All generators inherit from the `moodpy.generator.Generator` base class and follow the established MoodPy v3.0.0 patterns:

1. **Parameter Generation**: Lambda functions for randomized inputs
2. **Validation**: Requirements lists to ensure mathematical validity
3. **Derived Calculations**: Automatic computation of dependent values
4. **Exercise Generation**: Formatted HTML with LaTeX mathematics
5. **Moodle Integration**: XML export via `moodpy.cloze.Cloze`

### Dependencies
- **numpy**: Numerical computations and random number generation
- **scipy**: Statistical distributions (Poisson for realistic quantities)
- **tabulate**: HTML table generation for financial data
- **MoodPy Core**: Generator and Cloze classes from `src/moodpy/`

### Quality Assurance
Each generator has been validated against the original XML outputs to ensure:
- ✅ Mathematical accuracy
- ✅ Parameter range consistency
- ✅ Output format compatibility
- ✅ Educational value preservation

## Reconstruction Methodology

The reverse-engineering process involved:

1. **XML Pattern Analysis**: Studying generated questions to identify mathematical patterns
2. **Parameter Extraction**: Determining coefficient ranges and distributions
3. **Formula Reconstruction**: Rebuilding mathematical relationships
4. **Validation Logic**: Ensuring parameter combinations produce valid problems
5. **Educational Context**: Preserving pedagogical structure and problem presentation

## Integration with MoodPy v3.0.0

These generators are fully compatible with the modern MoodPy package structure:
- Use proper package imports (`from moodpy.generator import Generator`)
- Follow PEP 8 coding standards
- Include comprehensive documentation
- Support batch XML generation
- Integrate with the testing framework

## Future Expansion

Additional high-value generators identified for future reconstruction:
- Bond valuation problems (304 Bonos)
- Annuity calculations (203 Valor de Anualidades)  
- Complex differential equations
- Advanced financial derivatives
- Statistical hypothesis testing

## Educational Impact

These reconstructed generators represent thousands of hours of classroom testing and refinement, providing:
- **Proven Educational Value**: Used in actual university courses
- **Mathematical Rigor**: Validated formulas and realistic parameters
- **Cultural Context**: Problems adapted for Mexican/Latin American educational systems
- **Scalability**: Capable of generating unlimited unique problem variations

---

*Generated as part of MoodPy v3.0.0 Phase 5: Reconstruct Missing Generators*
*Reverse-engineered from MoodPy library collection (2017-2022)*
# Phase 7: Legacy Module Integration Plan

## Overview
Convert 136 legacy Python generators (converted from Jupyter notebooks) into the MoodPy v3.0.0 package structure while maintaining educational value and functionality.

## Migration Strategy

### Step 1: Content Analysis & Cataloging
- Analyze all 136 generators by subject, complexity, and educational value
- Identify patterns and common structures
- Group by subject areas (Mathematics, Finance, Statistics, etc.)
- Detect duplicates and variations

### Step 2: Migration Framework Setup
- Create subject-specific subpackages under `src/moodpy/subjects/`
- Establish conversion utilities for percent-format to module format
- Set up validation and testing framework for converted generators
- Create documentation templates

### Step 3: Systematic Conversion Process
- Convert highest-value generators first
- Modernize code to use MoodPy v3.0.0 APIs
- Add proper error handling and validation
- Create comprehensive tests for each converted generator

### Step 4: Integration & Organization
- Integrate converted generators into package structure
- Update imports and dependencies
- Add to examples and documentation
- Validate against original XML outputs where available

## Subject Categories Identified

Based on filenames, we can see several subject areas:
- **MAN**: Management/Economics (Precio de equilibrio)
- **MB**: Mathematics/Business
- **P103-P303**: Progressive difficulty levels (100s, 200s, 300s)
- **ED**: Differential Equations
- **PEP**: Statistics/Probability
- **Mate Financiera**: Financial Mathematics
- **TEST**: Assessment generators

## Conversion Priorities

1. **High Value**: Unique mathematical content with clear educational purpose
2. **Medium Value**: Variations of core concepts with different parameters
3. **Low Priority**: Test files, checkpoints, and duplicates

## Technical Requirements

- Maintain compatibility with MoodPy v3.0.0 API
- Preserve mathematical accuracy and educational intent
- Add proper documentation and examples
- Ensure all dependencies are handled
- Create migration validation tests
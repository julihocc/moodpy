#!/bin/bash

# GitHub Issues Creation Script for MoodPy v3.0.0
# Run this script to create all the organized issues for project management

echo "🚀 Creating GitHub Issues for MoodPy v3.0.0 Project Management"
echo "================================================="
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "Please install it first: https://cli.github.com/"
    echo "Then run: gh auth login"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI is not authenticated."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready!"
echo ""

# Define repository (adjust if needed)
REPO="julihocc/moodpy"

# Create milestones first
echo "📋 Creating Milestones..."
gh milestone create "Phase 7 - 75% Completion" --description "Complete Phase 7 legacy module integration to reach 75% of generators migrated" --due-date "2025-10-01" --repo $REPO
gh milestone create "Phase 8 - Documentation Complete" --description "Complete comprehensive documentation with Sphinx setup and migration guides" --due-date "2025-10-15" --repo $REPO  
gh milestone create "Phase 9 - Infrastructure Complete" --description "Complete CI/CD pipeline and testing infrastructure" --due-date "2025-10-20" --repo $REPO
gh milestone create "Phase 10 - Version 3.0.0 Ready" --description "Finalize v3.0.0 breaking changes and version management" --due-date "2025-10-25" --repo $REPO
gh milestone create "Phase 11 - v3.0.0 Released" --description "Execute final release preparation and PyPI deployment" --due-date "2025-11-01" --repo $REPO
gh milestone create "Project Organization" --description "Project management and community setup" --due-date "2025-09-20" --repo $REPO

echo "✅ Milestones created!"
echo ""

# Phase 7 Issues - Legacy Module Integration
echo "📊 Creating Phase 7 Issues (Legacy Module Integration)..."

gh issue create \
  --title "Migrate Advanced Mathematics Generators (15+ generators)" \
  --body "Migrate 15+ advanced mathematics generators from legacy collection focusing on:
- Optimization problems and linear programming
- Linear algebra (matrix operations, eigenvalues, vector spaces)  
- Advanced calculus applications (multivariable, optimization)
- Numerical methods and computational mathematics

**Acceptance Criteria**:
- [ ] Identify and catalog 15+ mathematics generators from legacy collection
- [ ] Migrate generators to examples/mathematics/ with proper v3.0.0 structure
- [ ] Ensure all generators produce valid Moodle XML output
- [ ] Add comprehensive docstrings and educational context
- [ ] Test generators with at least 10 different parameter sets each
- [ ] Update PROGRESS_TRACKER.md with completion status

**Priority**: High (next immediate batch after Data Science completion)" \
  --label "generator-migration,phase-7,high-priority,mathematics" \
  --milestone "Phase 7 - 75% Completion" \
  --repo $REPO

gh issue create \
  --title "Migrate Computer Science/Algorithms Generators (8+ generators)" \
  --body "Migrate 8+ computer science and algorithms generators from legacy collection:
- Sorting algorithms analysis (complexity, performance)
- Graph algorithms (shortest path, minimum spanning tree)
- Data structures problems (stacks, queues, trees)
- Computational complexity and Big-O analysis

**Acceptance Criteria**:
- [ ] Create examples/computer_science/ directory structure
- [ ] Identify and catalog 8+ CS/algorithms generators
- [ ] Migrate with proper educational scaffolding for algorithm analysis
- [ ] Include complexity analysis and performance comparisons
- [ ] Validate against computer science curriculum standards
- [ ] Update subject area count and progress tracking" \
  --label "generator-migration,phase-7,high-priority,computer-science" \
  --milestone "Phase 7 - 75% Completion" \
  --repo $REPO

gh issue create \
  --title "Migrate Physics Applications Generators (12+ generators)" \
  --body "Migrate 12+ physics applications generators covering:
- Classical mechanics (kinematics, dynamics, energy)
- Electromagnetics (fields, circuits, waves)
- Thermodynamics (heat transfer, gas laws, entropy)
- Modern physics applications

**Acceptance Criteria**:
- [ ] Create examples/physics/ directory with proper structure
- [ ] Migrate generators with accurate physical constants and units
- [ ] Include proper scientific notation and unit conversion
- [ ] Add physics problem-solving methodology
- [ ] Validate against physics education standards
- [ ] Test with realistic physical parameter ranges" \
  --label "generator-migration,phase-7,medium-priority,physics" \
  --milestone "Phase 7 - 75% Completion" \
  --repo $REPO

gh issue create \
  --title "Migrate Chemistry Applications Generators (8+ generators)" \
  --body "Migrate 8+ chemistry applications generators including:
- Stoichiometry and molar calculations
- Thermochemistry and reaction energetics
- Chemical kinetics and equilibrium
- Acid-base and redox reactions

**Acceptance Criteria**:
- [ ] Create examples/chemistry/ directory structure
- [ ] Implement proper chemical notation and formulas
- [ ] Include periodic table data and chemical constants
- [ ] Add reaction balancing and stoichiometric calculations
- [ ] Validate against chemistry curriculum standards
- [ ] Test with realistic chemical parameter ranges" \
  --label "generator-migration,phase-7,medium-priority,chemistry" \
  --milestone "Phase 7 - 75% Completion" \
  --repo $REPO

echo "✅ Phase 7 issues created!"
echo ""

# Phase 8 Issues - Documentation
echo "📚 Creating Phase 8 Issues (Documentation Enhancement)..."

gh issue create \
  --title "Setup Comprehensive Documentation with Sphinx" \
  --body "Create professional documentation system using Sphinx:
- Setup docs/ directory with proper Sphinx configuration
- Generate API reference from docstrings
- Create getting started guide and tutorials
- Build examples gallery with educational content

**Acceptance Criteria**:
- [ ] Install and configure Sphinx with modern theme
- [ ] Create docs/source/ structure with proper index
- [ ] Auto-generate API documentation from docstrings
- [ ] Write comprehensive getting started guide
- [ ] Create examples gallery with categorized generators
- [ ] Setup automated documentation building
- [ ] Deploy documentation to GitHub Pages or similar" \
  --label "documentation,phase-8,medium-priority" \
  --milestone "Phase 8 - Documentation Complete" \
  --repo $REPO

gh issue create \
  --title "Create Comprehensive Migration Guide v2→v3" \
  --body "Create detailed migration guide for users upgrading from MoodPy v2.0.0 to v3.0.0:
- Document breaking changes and new import structure
- Provide code examples for common migration patterns
- Include troubleshooting section for common issues

**Acceptance Criteria**:
- [ ] Document all breaking changes with examples
- [ ] Create side-by-side code comparisons (v2 vs v3)
- [ ] Include automated migration scripts where possible
- [ ] Add troubleshooting section for common problems
- [ ] Test migration guide with real v2.0.0 projects
- [ ] Include performance improvements and new features" \
  --label "documentation,phase-8,high-priority" \
  --milestone "Phase 8 - Documentation Complete" \
  --repo $REPO

echo "✅ Phase 8 issues created!"
echo ""

# Phase 9 Issues - CI/CD
echo "⚙️ Creating Phase 9 Issues (CI/CD Setup)..."

gh issue create \
  --title "Implement Complete CI/CD Pipeline" \
  --body "Setup comprehensive GitHub Actions workflows for:
- Multi-version Python testing (3.8, 3.9, 3.10, 3.11, 3.12)
- Automated documentation building and deployment
- Code quality checks (Black, flake8, coverage)
- Automated PyPI releases on version tags

**Acceptance Criteria**:
- [ ] Create .github/workflows/test.yml for testing
- [ ] Create .github/workflows/docs.yml for documentation
- [ ] Create .github/workflows/publish.yml for PyPI releases
- [ ] Setup code quality checks and coverage reporting
- [ ] Configure automated dependency updates
- [ ] Test workflows with sample releases" \
  --label "ci-cd,phase-9,medium-priority,automation" \
  --milestone "Phase 9 - Infrastructure Complete" \
  --repo $REPO

gh issue create \
  --title "Enhance Code Quality and Test Coverage" \
  --body "Improve code quality and increase test coverage:
- Increase test coverage from 32% to >90%
- Add comprehensive integration tests
- Setup automated code formatting and linting
- Add performance benchmarking for generators

**Acceptance Criteria**:
- [ ] Achieve >90% test coverage across all modules
- [ ] Add integration tests for complete workflows
- [ ] Setup Black, flake8, and isort configurations
- [ ] Add performance benchmarks for generator speed
- [ ] Create test data fixtures for consistent testing
- [ ] Add property-based testing for edge cases" \
  --label "testing,phase-9,high-priority,quality" \
  --milestone "Phase 9 - Infrastructure Complete" \
  --repo $REPO

echo "✅ Phase 9 issues created!"
echo ""

# Phase 10-11 Issues - Release Preparation
echo "🚀 Creating Phase 10-11 Issues (Release Preparation)..."

gh issue create \
  --title "Finalize v3.0.0 Breaking Changes and Version Management" \
  --body "Implement final breaking changes for v3.0.0 release:
- Update import structure to \`from moodpy import Generator\`
- Implement backwards compatibility layers where possible
- Update all examples and documentation
- Prepare comprehensive changelog

**Acceptance Criteria**:
- [ ] Implement new import structure throughout codebase
- [ ] Add backwards compatibility warnings for deprecated patterns
- [ ] Update all examples to use new import structure
- [ ] Create detailed CHANGELOG.md with migration info
- [ ] Test backwards compatibility with v2.0.0 patterns
- [ ] Update version numbers across all files" \
  --label "breaking-changes,phase-10,high-priority,version-management" \
  --milestone "Phase 10 - Version 3.0.0 Ready" \
  --repo $REPO

gh issue create \
  --title "Prepare and Execute v3.0.0 Release" \
  --body "Final preparation and execution of MoodPy v3.0.0 release:
- Complete final testing across all Python versions
- Prepare release notes and community announcements
- Execute PyPI deployment
- Setup post-release monitoring and support

**Acceptance Criteria**:
- [ ] All tests passing on Python 3.8-3.12
- [ ] Documentation complete and deployed
- [ ] All examples validated and working
- [ ] Release notes prepared with feature highlights
- [ ] PyPI deployment successful with proper metadata
- [ ] Community announcement ready (social media, forums)
- [ ] Post-release monitoring setup (issues, discussions)" \
  --label "release,phase-11,high-priority,pypi" \
  --milestone "Phase 11 - v3.0.0 Released" \
  --repo $REPO

echo "✅ Release preparation issues created!"
echo ""

# Project Management Issues
echo "📋 Creating Project Management Issues..."

gh issue create \
  --title "Create GitHub Project Board for Task Management" \
  --body "Setup GitHub project board to track all development tasks:
- Create project with proper columns (Backlog, In Progress, Review, Done)
- Organize all issues by phases and priorities
- Setup automation for issue status updates
- Create milestone tracking and progress visualization

**Acceptance Criteria**:
- [ ] Create GitHub project with proper structure
- [ ] Add all issues to project with appropriate status
- [ ] Setup automation for status updates
- [ ] Create milestone progress tracking
- [ ] Configure notifications and team access
- [ ] Add project description and documentation" \
  --label "project-management,organization" \
  --milestone "Project Organization" \
  --repo $REPO

gh issue create \
  --title "Establish Community Guidelines and Contribution Process" \
  --body "Create comprehensive community guidelines and contribution process:
- Setup CONTRIBUTING.md with development workflow
- Create issue and pull request templates
- Establish code of conduct and community standards
- Setup community support channels

**Acceptance Criteria**:
- [ ] Create CONTRIBUTING.md with clear development setup
- [ ] Add issue templates for bugs, features, and questions
- [ ] Create pull request template with checklist
- [ ] Establish CODE_OF_CONDUCT.md
- [ ] Setup GitHub Discussions for community support
- [ ] Create contributor recognition system" \
  --label "community,documentation,guidelines" \
  --milestone "Project Organization" \
  --repo $REPO

echo "✅ Project management issues created!"
echo ""

echo "🎉 All GitHub Issues Created Successfully!"
echo ""
echo "📊 Summary:"
echo "- 4 Phase 7 issues (Legacy Module Integration)"
echo "- 2 Phase 8 issues (Documentation Enhancement)"
echo "- 2 Phase 9 issues (CI/CD Setup)"
echo "- 2 Phase 10-11 issues (Release Preparation)"
echo "- 2 Project Management issues"
echo "- 6 Milestones created"
echo ""
echo "🔗 Next Steps:"
echo "1. Visit https://github.com/$REPO/issues to review all issues"
echo "2. Create a GitHub project board to organize the issues"
echo "3. Start with Phase 7: Advanced Mathematics batch migration"
echo ""
echo "✅ Project management setup complete!"
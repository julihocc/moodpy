#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package Structure Verification

This script verifies that the new package structure is working correctly.
It tests importing from the new src/moodpy package structure.
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing MoodPy v3.0.0 package structure...")
    
    try:
        # Test main package import
        import moodpy
        print(f"✓ Main package imported successfully - version {moodpy.__version__}")
        
        # Test individual module imports
        from moodpy import Generator
        print("✓ Generator class imported successfully")
        
        from moodpy import Cloze
        print("✓ Cloze class imported successfully")
        
        from moodpy import tools
        print("✓ Tools module imported successfully")
        
        from moodpy import matfin
        print("✓ Matfin module imported successfully")
        
        # Test optional graphics import
        from moodpy import graphics
        if graphics is None:
            print("⚠ Graphics module not available (missing dependencies)")
        else:
            print("✓ Graphics module imported successfully")
        
        # Test utility functions
        print(f"✓ Version info: {moodpy.get_version()}")
        print(f"✓ Graphics available: {moodpy.has_graphics()}")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality with the new package structure."""
    print("\nTesting basic functionality...")
    
    try:
        from moodpy import Generator
        
        # Create a simple generator
        gen = Generator()
        gen.lambdas = {"x": lambda k: 42}
        gen.reload_parameters()
        
        if gen.parameters["x"] == 42:
            print("✓ Basic parameter generation works")
        else:
            print("✗ Parameter generation failed")
            return False
        
        # Test exercise creation
        gen.set_exercise("Test exercise with value {d[x]}")
        if "42" in gen.exercise_text:
            print("✓ Exercise text generation works")
        else:
            print("✗ Exercise text generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False


def verify_package_structure():
    """Verify the package directory structure."""
    print("\nVerifying package structure...")
    
    base_dir = os.path.dirname(__file__)
    expected_dirs = [
        "src/moodpy",
        "examples",
        "examples/basic", 
        "examples/mathematics",
        "examples/finance",
        "examples/reconstructed",
        "tests"
    ]
    
    expected_files = [
        "src/moodpy/__init__.py",
        "src/moodpy/generator.py",
        "src/moodpy/cloze.py",
        "src/moodpy/tools.py",
        "src/moodpy/matfin.py",
        "src/moodpy/graphics.py",
        "pyproject.toml",
        "MANIFEST.in",
        "REFACTORING_PLAN.md"
    ]
    
    all_good = True
    
    # Check directories
    for dir_path in expected_dirs:
        full_path = os.path.join(base_dir, dir_path)
        if os.path.isdir(full_path):
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"✗ Missing directory: {dir_path}")
            all_good = False
    
    # Check files
    for file_path in expected_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.isfile(full_path):
            print(f"✓ File exists: {file_path}")
        else:
            print(f"✗ Missing file: {file_path}")
            all_good = False
    
    return all_good


def main():
    """Main verification function."""
    print("=" * 60)
    print("MoodPy v3.0.0 Package Structure Verification")
    print("=" * 60)
    
    # Run all tests
    structure_ok = verify_package_structure()
    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if structure_ok and imports_ok and functionality_ok:
        print("🎉 ALL TESTS PASSED - Package structure is ready!")
        print("\nNext steps:")
        print("1. Fix module dependencies (Phase 2)")
        print("2. Add comprehensive test suite (Phase 3)")
        print("3. Organize examples (Phase 4)")
        return 0
    else:
        print("❌ SOME TESTS FAILED - Package structure needs fixes")
        if not structure_ok:
            print("- Fix missing directories/files")
        if not imports_ok:
            print("- Fix import issues")
        if not functionality_ok:
            print("- Fix basic functionality")
        return 1


if __name__ == "__main__":
    exit(main())
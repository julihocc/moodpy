#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dependency Checker for MoodPy

This script checks if all required and optional dependencies are available
and provides installation instructions for missing packages.
"""

import sys
import importlib.util


def check_dependency(package_name, import_name=None, required=True):
    """
    Check if a dependency is available.
    
    Args:
        package_name (str): Name of the package for installation
        import_name (str): Name to use for import (if different from package_name)
        required (bool): Whether this is a required dependency
        
    Returns:
        bool: True if available, False otherwise
    """
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    available = spec is not None
    
    status = "✓" if available else ("✗" if required else "⚠")
    req_type = "Required" if required else "Optional"
    
    if available:
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"{status} {package_name} ({version}) - {req_type}")
        except ImportError:
            print(f"{status} {package_name} (available) - {req_type}")
    else:
        print(f"{status} {package_name} (missing) - {req_type}")
        if required:
            print(f"    Install with: pip install {package_name}")
        else:
            print(f"    Optional: pip install {package_name}")
    
    return available


def main():
    """Main dependency checking function."""
    print("=" * 60)
    print("MoodPy Dependency Checker")
    print("=" * 60)
    
    # Required dependencies
    required_ok = True
    print("\nRequired Dependencies:")
    required_ok &= check_dependency("numpy")
    required_ok &= check_dependency("matplotlib")
    required_ok &= check_dependency("tabulate")
    
    # Optional dependencies  
    print("\nOptional Dependencies:")
    check_dependency("pytest", required=False)
    check_dependency("jupyter", required=False)
    check_dependency("sphinx", required=False)
    
    print("\n" + "=" * 60)
    if required_ok:
        print("🎉 All required dependencies are available!")
        print("MoodPy should work correctly.")
    else:
        print("❌ Some required dependencies are missing.")
        print("Install missing packages before using MoodPy.")
    
    print("\nTo install all dependencies:")
    print("pip install numpy matplotlib tabulate")
    print("\nFor development:")
    print("pip install numpy matplotlib tabulate pytest jupyter sphinx")
    
    return 0 if required_ok else 1


if __name__ == "__main__":
    exit(main())
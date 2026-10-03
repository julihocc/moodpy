#!/bin/bash
# MoodPy v3.0.0 Test PyPI Upload Script
# 
# This script will upload MoodPy v3.0.0 to Test PyPI once you have your API token
# 
# Prerequisites:
# 1. Test PyPI account created at https://test.pypi.org/
# 2. API token generated at https://test.pypi.org/manage/account/
# 3. Token copied and ready to paste

set -e  # Exit on any error

echo "🚀 MoodPy v3.0.0 Test PyPI Upload"
echo "=================================="
echo

# Check if packages exist
if [ ! -f "dist/moodpy-3.0.0.tar.gz" ] || [ ! -f "dist/moodpy-3.0.0-py3-none-any.whl" ]; then
    echo "❌ Error: Package files not found in dist/"
    echo "   Run: python -m build"
    exit 1
fi

echo "✅ Package files found:"
ls -la dist/moodpy-3.0.0*

echo
echo "📋 Pre-upload validation:"
echo "Running twine check..."
uv run twine check dist/*

if [ $? -ne 0 ]; then
    echo "❌ Package validation failed!"
    exit 1
fi

echo "✅ Package validation passed!"
echo

# Prompt for API token
echo "🔑 Test PyPI API Token Required"
echo "--------------------------------"
echo "1. Go to: https://test.pypi.org/manage/account/"
echo "2. Scroll to 'API tokens' section"
echo "3. Click 'Add API token'"
echo "4. Name: 'MoodPy v3.0.0 Upload'"
echo "5. Scope: 'Entire account' (or project-specific if you prefer)"
echo "6. Copy the token (starts with 'pypi-')"
echo

read -p "Do you have your Test PyPI API token ready? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please get your API token first, then run this script again."
    exit 1
fi

echo
read -s -p "Paste your Test PyPI API token: " PYPI_TOKEN
echo

if [ -z "$PYPI_TOKEN" ]; then
    echo "❌ No token provided"
    exit 1
fi

if [[ ! $PYPI_TOKEN == pypi-* ]]; then
    echo "❌ Token should start with 'pypi-'"
    echo "   Make sure you copied the complete token"
    exit 1
fi

echo "✅ Token format looks correct"
echo

# Set environment variables
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=$PYPI_TOKEN

echo "🚀 Uploading to Test PyPI..."
echo "Repository: https://test.pypi.org/"
echo

# Upload to Test PyPI
uv run twine upload --repository testpypi dist/*

if [ $? -eq 0 ]; then
    echo
    echo "🎉 SUCCESS! MoodPy v3.0.0 uploaded to Test PyPI!"
    echo
    echo "📦 View your package at:"
    echo "   https://test.pypi.org/project/moodpy/3.0.0/"
    echo
    echo "🧪 Test installation:"
    echo "   pip install -i https://test.pypi.org/simple/ moodpy==3.0.0"
    echo
    echo "✅ Next steps:"
    echo "   1. Visit the package page to verify metadata"
    echo "   2. Test installation in a clean environment"
    echo "   3. Validate basic functionality works"
    echo "   4. Ready for production PyPI when satisfied!"
else
    echo
    echo "❌ Upload failed!"
    echo "Check the error messages above for details."
    exit 1
fi
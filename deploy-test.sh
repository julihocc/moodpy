#!/bin/bash
# Simple Test PyPI deployment script
# Requires .pypirc configuration or environment variables

set -e

echo "MoodPy Test PyPI Deployment"
echo "=========================="

# Check if packages exist, build if needed
if [ ! -f "dist/moodpy-3.0.0.tar.gz" ] || [ ! -f "dist/moodpy-3.0.0-py3-none-any.whl" ]; then
    echo "Building package..."
    uv run python -m build
fi

echo "Validating packages..."
uv run twine check dist/*

if [ $? -ne 0 ]; then
    echo "Package validation failed"
    exit 1
fi

echo "Uploading to Test PyPI..."
uv run twine upload --repository testpypi dist/*

if [ $? -eq 0 ]; then
    echo "Upload successful"
    echo "View at: https://test.pypi.org/project/moodpy/"
    echo "Install with: pip install -i https://test.pypi.org/simple/ moodpy"
else
    echo "Upload failed"
    exit 1
fi
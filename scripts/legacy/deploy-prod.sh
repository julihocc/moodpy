#!/bin/bash
# Simple Production PyPI deployment script
# Requires .pypirc configuration or environment variables

set -e

echo "MoodPy Production PyPI Deployment"
echo "================================"

# Safety check - confirm this is intentional
read -p "Deploy to PRODUCTION PyPI? This cannot be undone. (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Deployment cancelled"
    exit 1
fi

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

echo "Uploading to Production PyPI..."
uv run twine upload dist/*

if [ $? -eq 0 ]; then
    echo "Upload successful"
    echo "View at: https://pypi.org/project/moodpy/"
    echo "Install with: pip install moodpy"
else
    echo "Upload failed"
    exit 1
fi
#!/bin/bash
# Setup .pypirc configuration for PyPI deployments

echo "PyPI Configuration Setup"
echo "======================="

# Check if .pypirc already exists
if [ -f ~/.pypirc ]; then
    echo "Warning: ~/.pypirc already exists"
    read -p "Overwrite existing configuration? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled"
        exit 1
    fi
fi

echo
echo "You need API tokens from:"
echo "- Test PyPI: https://test.pypi.org/manage/account/"
echo "- Production PyPI: https://pypi.org/manage/account/"
echo

read -p "Enter your Test PyPI API token (starts with pypi-): " TEST_TOKEN
read -p "Enter your Production PyPI API token (starts with pypi-): " PROD_TOKEN

if [ -z "$TEST_TOKEN" ] || [ -z "$PROD_TOKEN" ]; then
    echo "Error: Both tokens are required"
    exit 1
fi

# Create .pypirc file
cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = $PROD_TOKEN

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = $TEST_TOKEN
EOF

# Secure the file
chmod 600 ~/.pypirc

echo "Configuration saved to ~/.pypirc"
echo
echo "Test your setup:"
echo "  ./deploy-test.sh    # Upload to Test PyPI"
echo "  ./deploy-prod.sh    # Upload to Production PyPI"
echo
echo "Direct commands:"
echo "  twine upload --repository testpypi dist/*"
echo "  twine upload dist/*"
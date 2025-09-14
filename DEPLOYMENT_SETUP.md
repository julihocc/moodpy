# MoodPy PyPI Configuration and Deployment Setup

This document explains how to set up one-time configuration for easy PyPI deployments.

## Option 1: .pypirc Configuration File (Recommended)

Create a `.pypirc` file in your home directory for persistent configuration:

```bash
# Create .pypirc file
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = your-production-pypi-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your-test-pypi-token-here
EOF

# Secure the file
chmod 600 ~/.pypirc
```

After setup, deployment becomes simple:

```bash
# Test PyPI upload
twine upload --repository testpypi dist/*

# Production PyPI upload  
twine upload dist/*
```

## Option 2: Environment Variables

Set persistent environment variables in your shell profile:

```bash
# Add to ~/.zshrc or ~/.bashrc
export TWINE_USERNAME=__token__
export TWINE_TEST_PASSWORD=your-test-pypi-token
export TWINE_PASSWORD=your-production-pypi-token

# For test uploads
TWINE_PASSWORD=$TWINE_TEST_PASSWORD twine upload --repository testpypi dist/*

# For production uploads
twine upload dist/*
```

## Streamlined Deployment Scripts

### deploy-test.sh
```bash
#!/bin/bash
set -e
echo "Building and uploading to Test PyPI..."
python -m build
twine check dist/*
twine upload --repository testpypi dist/*
echo "Uploaded to: https://test.pypi.org/project/moodpy/"
```

### deploy-prod.sh  
```bash
#!/bin/bash
set -e
echo "Building and uploading to Production PyPI..."
python -m build
twine check dist/*
twine upload dist/*
echo "Uploaded to: https://pypi.org/project/moodpy/"
```

## Setup Instructions

1. Get your API tokens:
   - Test PyPI: https://test.pypi.org/manage/account/
   - Production PyPI: https://pypi.org/manage/account/

2. Choose configuration method (.pypirc recommended)

3. Replace token placeholders with actual tokens

4. Test with: `twine upload --repository testpypi dist/*`

5. Deploy to production: `twine upload dist/*`

## Security Notes

- .pypirc file should have 600 permissions (readable only by you)
- Never commit .pypirc or tokens to version control
- Consider using project-scoped tokens instead of account-wide tokens
- Rotate tokens periodically for security
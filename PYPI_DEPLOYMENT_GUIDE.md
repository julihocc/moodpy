# PyPI Test Deployment Instructions

## Prerequisites

Before deploying to Test PyPI, you need to:

1. **Create Test PyPI Account**:
   - Go to https://test.pypi.org/
   - Register for an account
   - Verify your email address

2. **Generate API Token**:
   - Go to https://test.pypi.org/manage/account/
   - Scroll to "API tokens" section
   - Click "Add API token"
   - Name: "MoodPy v3.0.0 Deployment"
   - Scope: "Entire account" (or create project-specific)
   - Copy the token (starts with `pypi-`)

3. **Configure GitHub Secrets** (for automated deployment):
   - Go to your GitHub repository settings
   - Navigate to Secrets → Actions
   - Add new secret: `TEST_PYPI_API_TOKEN`
   - Paste the API token value

## Manual Test Deployment

Once you have the API token, run:

```bash
# Set your token as environment variable
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-token-here

# Upload to Test PyPI
uv run twine upload --repository testpypi dist/*
```

## Expected Output

After successful upload, you should see:
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading moodpy-3.0.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 13.3/13.3 kB • 00:01 • ?
Uploading moodpy-3.0.0.tar.gz  
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 47.7/47.7 kB • 00:01 • ?

View at:
https://test.pypi.org/project/moodpy/3.0.0/
```

## Test Installation

After upload, test the installation:

```bash
# Install from Test PyPI
pip install -i https://test.pypi.org/simple/ moodpy==3.0.0

# Test import
python -c "import moodpy; print(f'MoodPy {moodpy.__version__} installed successfully!')"
```

## GitHub Actions Workflow Test

You can also test the automated workflow:

1. Go to your GitHub repository
2. Navigate to Actions tab
3. Click "Publish to PyPI" workflow
4. Click "Run workflow" button
5. Select branch and run manually

This will trigger the Test PyPI deployment automatically.

## Next Steps After Successful Test

1. ✅ Verify package appears on https://test.pypi.org/project/moodpy/
2. ✅ Test installation in clean environment
3. ✅ Validate all dependencies resolve correctly
4. ✅ Test basic functionality works
5. ✅ Ready for production PyPI deployment!

## Package Information

- **Name**: moodpy
- **Version**: 3.0.0
- **Wheel**: moodpy-3.0.0-py3-none-any.whl (13.3 KB)
- **Source**: moodpy-3.0.0.tar.gz (47.7 KB)
- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **License**: MIT
- **Dependencies**: numpy, matplotlib, tabulate, scipy
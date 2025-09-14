#!/bin/bash

# GitHub Project Creation Script for MoodPy v3.0.0
# Run this script after creating issues to organize them in a project board

echo "📋 Creating GitHub Project Board for MoodPy v3.0.0"
echo "==============================================="
echo ""

# Check if GitHub CLI is installed and authenticated
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "Please install it first: https://cli.github.com/"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI is not authenticated."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready!"
echo ""

# Define repository
REPO="julihocc/moodpy"

# Create project
echo "📊 Creating GitHub Project..."
PROJECT_URL=$(gh project create \
  --title "MoodPy v3.0.0 Development" \
  --body "Complete project management for MoodPy v3.0.0 refactoring and release.

## Project Overview
- **Current Status**: Phase 7 at 51.5% completion (70/136 generators migrated)
- **Last Achievement**: Data Science batch completed
- **Next Priority**: Advanced Mathematics batch (15+ generators)

## Phases
- **Phase 7**: Legacy Module Integration (Continued) - 66 generators remaining
- **Phase 8**: Documentation Enhancement - Sphinx setup, API reference, tutorials
- **Phase 9**: CI/CD Setup - GitHub Actions, testing infrastructure, automation
- **Phase 10**: Version Management - v3.0.0 breaking changes, migration guide
- **Phase 11**: Release Preparation - Final testing, PyPI deployment

## Success Metrics
- Target: 100% generator migration (136 total)
- Target: >90% test coverage
- Target: Complete documentation with API reference
- Target: Automated CI/CD pipeline
- Target: Successful PyPI v3.0.0 release" \
  --format json | jq -r '.url')

echo "✅ Project created: $PROJECT_URL"
echo ""

# Get project ID for adding issues (this might need manual adjustment)
PROJECT_ID=$(gh project list --format json --owner julihocc | jq -r '.[] | select(.title=="MoodPy v3.0.0 Development") | .id')

if [ -z "$PROJECT_ID" ]; then
    echo "⚠️  Could not automatically get project ID."
    echo "Please manually add issues to the project at: $PROJECT_URL"
    echo ""
    echo "📋 Manual Steps:"
    echo "1. Visit the project URL above"
    echo "2. Click 'Add items'"
    echo "3. Add all issues related to MoodPy v3.0.0"
    echo "4. Organize issues into columns (Backlog, In Progress, Review, Done)"
    echo "5. Set up automation rules for status updates"
else
    echo "📊 Project ID: $PROJECT_ID"
    echo "Adding issues to project..."
    
    # Get all issues and add them to project
    gh issue list --repo $REPO --limit 50 --format json | jq -r '.[].number' | while read issue_number; do
        echo "Adding issue #$issue_number to project..."
        gh project item-add $PROJECT_ID --id $issue_number 2>/dev/null || echo "Could not add issue #$issue_number"
    done
    
    echo "✅ Issues added to project!"
fi

echo ""
echo "🎉 GitHub Project Setup Complete!"
echo ""
echo "📊 Project Details:"
echo "- Title: MoodPy v3.0.0 Development" 
echo "- URL: $PROJECT_URL"
echo "- Status: Ready for task management"
echo ""
echo "🔗 Next Steps:"
echo "1. Visit the project URL to organize issues into columns"
echo "2. Set up automation rules for issue status updates"
echo "3. Configure project settings and permissions"
echo "4. Start working on Phase 7: Advanced Mathematics batch"
echo ""
echo "✅ Project management infrastructure complete!"
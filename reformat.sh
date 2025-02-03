#!/bin/bash
# Format with Black
black .

# Reorder imports with isort
isort .

# Commit changes in git
git add .
git commit -m "code formatings"
# Run Pylint to catch remaining issues
pylint .


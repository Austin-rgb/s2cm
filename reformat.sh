#!/bin/bash
# Format with Black
black .

# Reorder imports with isort
isort .

# Run Pylint to catch remaining issues
pylint .


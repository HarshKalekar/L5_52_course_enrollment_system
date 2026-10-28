#!/bin/bash
set -u

echo "Setting up static analysis tools..."

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install pylint bandit flake8

echo ""
echo "Files in the repository:"
find . -maxdepth 2 -name "*.py" -not -path "./.venv/*"

echo ""
echo "Setup complete."
echo "Next, run the analysis commands against your assigned Python file."

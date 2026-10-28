#!/bin/bash
set -e

echo "Setting up static analysis tools..."

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pylint bandit flake8

TARGET="course_enrollment_system.py"

if [ ! -f "$TARGET" ]; then
    echo "Error: $TARGET not found."
    exit 1
fi

echo "Running Pylint..."
pylint "$TARGET" > pylint_after.txt 2>&1 || true

echo "Running Bandit..."
bandit -r "$TARGET" > bandit_after.txt 2>&1 || true

echo "Running Flake8..."
flake8 "$TARGET" > flake8_after.txt 2>&1 || true

echo "Analysis reports generated:"
echo "  pylint_after.txt"
echo "  bandit_after.txt"
echo "  flake8_after.txt"

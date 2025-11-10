#!/bin/bash

# Setup script for Wikipedia project
VENV_DIR="wikienv"
PIP="$VENV_DIR/bin/pip"
PYTHON="python3"

echo "Creating virtual environment..."
$PYTHON -m venv $VENV_DIR
echo "Virtual environment created at $VENV_DIR"

echo "Installing dependencies..."
$PIP install -q --upgrade pip setuptools wheel
$PIP install -q -r requirements.txt
echo "Dependencies installed"

echo ""
echo "Development environment ready!"
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate
exec bash

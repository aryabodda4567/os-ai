#!/bin/bash

# Set the name of the virtual environment directory
VENV_DIR="venv"

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo " Python3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment in ./$VENV_DIR ..."
python3 -m venv "$VENV_DIR"

# Check if the virtual environment was created successfully
if [ ! -d "$VENV_DIR" ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Activate the virtual environment
echo " Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Show Python and pip version in the venv
echo " Python version: $(python --version)"
echo " Pip version: $(pip --version)"

# Optionally upgrade pip
echo "⬆  Upgrading pip..."
pip install --upgrade pip

pip install -r requirements.txt
echo "Virtual environment is ready and activated!"
echo " To activate it again later, run: source $VENV_DIR/bin/activate"

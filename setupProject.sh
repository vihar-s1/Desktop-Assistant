#!/usr/bin/env bash

# This script is used to setup the project for the first time.

echo "Starting project setup..."

# Check if the system is macOS and install portaudio using brew
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "MacOS detected, installing portaudio using brew..."
    brew install portaudio
fi

VENV_DIR=""
if [ -x ".venv" ]; then
    VENV_DIR=".venv"
    echo "Found existing virtual environment directory: .venv"
elif [ -x "venv" ]; then
    VENV_DIR="venv"
    echo "Found existing virtual environment directory: venv"
fi

# Create a virtual environment
if [ -z "${VENV_DIR}" ]; then
    if [ -x "*.iml" ]; then
        # intelliJ system so use "venv"
        VENV_DIR="venv"
        echo "IntelliJ system detected, setting virtual environment directory to: venv"
    else
        VENV_DIR=".venv"
        echo "Setting virtual environment directory to: .venv"
    fi
    echo "Creating virtual environment in directory: ${VENV_DIR}"
    python3 -m venv "${VENV_DIR}"
fi

# Activate the virtual environment if inactive
# VIRTUAL_ENV will be set if virtual env is active
if [ -z "${VIRTUAL_ENV}" ]; then
    echo "Activating virtual environment..."
    source "${VENV_DIR}/bin/activate"
else
    echo "Active virtual environment found: ${VIRTUAL_ENV}"
fi

# attempt to upgrade pip in case it is not latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install the required packages
echo "Installing required packages from requirements.txt..."
pip3 install -r requirements.txt

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Project setup complete."
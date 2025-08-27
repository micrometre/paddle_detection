#!/bin/bash
# Setup script for PaddleDetection Vehicle License Plate Recognition
# This script creates a virtual environment and installs dependencies

set -e

echo "Setting up PaddleDetection Vehicle License Plate Recognition environment..."

# Create virtual environment
python3 -m venv .venv
echo "Virtual environment created in .venv/"

# Activate virtual environment
source .venv/bin/activate
echo "Virtual environment activated"

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup completed successfully!"
echo ""
echo "To use the environment:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Run license plate detection:"
echo "   python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_file test_data/1.jpg"
echo ""
echo "Example commands:"
echo "# Single image"
echo "python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_file test_data/1.jpg"
echo ""
echo "# Multiple images"
echo "python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_dir test_data/"
echo ""
echo "# Deactivate environment when done: deactivate"

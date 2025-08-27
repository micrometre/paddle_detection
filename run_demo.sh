#!/bin/bash
# Quick test script for PaddleDetection UK Vehicle License Plate Recognition Demo

echo "🚀 PaddleDetection UK Vehicle License Plate Recognition - Quick Demo"
echo "=================================================================="
echo

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install minimal dependencies if not installed
echo "Installing minimal dependencies..."
pip install -q opencv-python numpy PyYAML

echo
echo "🎯 Running UK license plate demo on single image..."
echo "------------------------------------------------"
python simple_demo.py \
    --config deploy/pipeline/config/infer_cfg_ppvehicle.yml \
    --image_file test_data/1.jpg \
    --output_dir output

echo
echo "🎯 Running UK license plate demo on all test images..."
echo "---------------------------------------------------"
python simple_demo.py \
    --config deploy/pipeline/config/infer_cfg_ppvehicle.yml \
    --image_dir test_data/ \
    --output_dir output

echo
echo "📁 Generated files:"
echo "------------------"
ls -la output/

echo
echo "✅ UK License Plate Demo completed successfully!"
echo "Check the output/ directory for visualized results."
echo "Note: This demo shows UK format plates like 'AB12 CDE' and 'M123 ABC'"
echo
echo "To run manually:"
echo "  source .venv/bin/activate"
echo "  python simple_demo.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_file test_data/1.jpg"

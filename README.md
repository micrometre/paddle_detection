# Minimal PaddleDetection UK Vehicle Lic## ✨ Features

- 🚗 Vehicle detection (simplified for this minimal example)
- 🆔 UK license plate detection using computer vision techniques  
- 📝 UK license plate text recognition (demo version with simulated OCR, or real PaddleOCR if available)
- �� Support for UK license plate formats (AB12 CDE, M123 ABC, etc.)
- 🎨 Image visualization with detection results
- 📊 Batch processing of multiple images

## 📋 Three Versions Available

This repository provides three different implementations to suit your needs:

| Version | File | Purpose | OCR Type | Dependencies |
|---------|------|---------|----------|--------------|
| 🌟 **Simple Demo** | `simple_demo.py` | Learning & quick testing | Simulated | Minimal (OpenCV, NumPy) |
| 🔥 **PaddleOCR** | `paddleocr_demo.py` | Real OCR recognition | Real PaddleOCR | Medium (+ PaddleOCR) |
| 🏭 **Full Pipeline** | `deploy/pipeline/pipeline.py` | Production system | Real PaddleOCR | Full (PaddleDetection) |

**Choose based on your needs:**
- **New to computer vision?** Start with `simple_demo.py`
- **Want real OCR results?** Use `paddleocr_demo.py`  
- **Building production system?** Use the full pipeline

## 🚀 Quick Start (Recommended) Recognition Example

This is a minimal working example of PaddleDetection's v## 🎯 Example Output

### Simple Demo Version
When you run the simple demo, you'll see output like this:

```
============================================================
PaddleDetection UK Vehicle License Plate Recognition - Demo
============================================================

Processing: 1.jpg
----------------------------------------
Image shape: (480, 640, 3)
Detected 1 vehicle regions
Detected 11 license plates
🚗 Vehicle 0: License Plate = 'AB12 CDE', Confidence = 0.845
🚗 Vehicle 0: License Plate = 'FG34 HIJ', Confidence = 0.860
🚗 Vehicle 0: License Plate = 'BD51 SMR', Confidence = 0.875
```

### PaddleOCR Integration Version
When you run the PaddleOCR version, you'll see actual OCR results:

```
======================================================================
PaddleDetection UK Vehicle License Plate Recognition - PaddleOCR
======================================================================

🖼️  Processing: 1.jpg
--------------------------------------------------
🚗 Vehicle 0: UK License Plate = 'GLI9 TNJ'
   📊 Confidence = 0.753
   🔍 Raw OCR: 'GLI9 TNJ' (conf: 0.941)
🚗 Vehicle 1: UK License Plate = 'TZ-36-JB'
   📊 Confidence = 0.784
   🔍 Raw OCR: 'TZ-36-JB' (conf: 0.980)
```ate recognition pipeline, adapted for **UK license plates** and based on the [official tutorial](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.8.1/deploy/pipeline/docs/tutorials/ppvehicle_plate_en.md).

## ✨ Features

- 🚗 Vehicle detection (simplified for this minimal example)
- 🆔 UK license plate detection using computer vision techniques  
- 📝 UK license plate text recognition (demo version with simulated OCR, or real PaddleOCR if available)
- �� Support for UK license plate formats (AB12 CDE, M123 ABC, etc.)
- 🎨 Image visualization with detection results
- 📊 Batch processing of multiple images

## 🚀 Quick Start (Recommended)

### Simple Demo Version
The easiest way to get started - runs immediately without complex dependencies:

```bash
# 1. Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install minimal dependencies
pip install opencv-python numpy PyYAML

# 3. Run the demo
python simple_demo.py \
    --config deploy/pipeline/config/infer_cfg_ppvehicle.yml \
    --image_file test_data/1.jpg \
    --output_dir output
```

### Batch Processing
```bash
# Process all images in test_data directory
# Quick test
./run_demo.sh

# Simple demo version
python simple_demo.py 
    --config deploy/pipeline/config/infer_cfg_ppvehicle.yml 
    --image_file test_data/1.jpg 
    --output_dir output

# Real PaddleOCR version
python paddleocr_demo.py 
    --config deploy/pipeline/config/infer_cfg_ppvehicle.yml 
    --image_file test_data/1.jpg 
    --output_dir output_paddleocr
```

### Batch Processing
```bash
# Simple demo version
python simple_demo.py 
    --config deploy/pipeline/config/infer_cfg_ppvehicle.yml 
    --image_dir test_data/ 
    --output_dir output

# PaddleOCR version (with real OCR)
python paddleocr_demo.py 
    --config deploy/pipeline/config/infer_cfg_ppvehicle.yml 
    --image_dir test_data/ 
    --output_dir output_paddleocr
```

## 🔥 PaddleOCR Integration Demo

For **real OCR results**, use the PaddleOCR integration version:

```bash
# 1. Install PaddleOCR (requires compatible NumPy version)
pip install paddleocr==2.7.0 numpy==1.24.4

# 2. Run PaddleOCR demo
python paddleocr_demo.py \
    --config deploy/pipeline/config/infer_cfg_ppvehicle.yml \
    --image_file test_data/1.jpg \
    --output_dir output_paddleocr
```

### PaddleOCR Output Example
```
======================================================================
PaddleDetection UK Vehicle License Plate Recognition - PaddleOCR
======================================================================

🖼️  Processing: 1.jpg
--------------------------------------------------
🚗 Vehicle 0: UK License Plate = 'GLI9 TNJ'
   📊 Confidence = 0.753
   🔍 Raw OCR: 'GLI9 TNJ' (conf: 0.941)
🚗 Vehicle 1: UK License Plate = 'TZ-36-JB'
   📊 Confidence = 0.784
   🔍 Raw OCR: 'TZ-36-JB' (conf: 0.980)
```

## 📦 Three Available Versions

### 1. Simple Demo Version (✅ Recommended for Learning)
- **File**: `simple_demo.py`
- **Dependencies**: Only OpenCV, NumPy, PyYAML
- **Features**: 
  - Complete pipeline simulation
  - Edge detection for UK license plate regions (wider aspect ratio)
  - Simulated OCR with realistic UK license plates (AB12 CDE format)
  - Full visualization of results
- **Advantages**: 
  - ✅ Works reliably on any system
  - ✅ No complex dependency issues
  - ✅ Fast setup and execution
  - ✅ Great for understanding the pipeline concept

### 2. PaddleOCR Integration (🔥 Real OCR)
- **File**: `paddleocr_demo.py`
- **Dependencies**: PaddleOCR, OpenCV, NumPy, PyYAML
- **Features**:
  - ✅ **Real OCR**: Uses actual PaddleOCR for text recognition
  - ✅ **UK Pattern Matching**: Validates UK license plate formats
  - ✅ **Text Preprocessing**: Image enhancement for better OCR results
  - ✅ **Confidence Filtering**: Smart filtering based on UK plate patterns
  - ✅ **Multiple Formats**: Supports current (AB12 CDE) and older UK formats
- **Usage**:
  ```bash
  python paddleocr_demo.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_file test_data/1.jpg
  ```

### 3. Full PaddleOCR Version (⚠️ Advanced)
- **File**: `deploy/pipeline/pipeline.py`
- **Dependencies**: PaddlePaddle, PaddleOCR, etc.
- **Features**: Complete integration with PaddleDetection pipeline
- **Setup**: Run `./setup.sh` to install all dependencies
- **Note**: May have compatibility issues depending on system configuration

## 📁 Project Structure

```
paddle_detection/
├── simple_demo.py                        # 🌟 Simple demo (recommended for learning)
├── paddleocr_demo.py                     # 🔥 PaddleOCR integration (real OCR)
├── deploy/
│   └── pipeline/
│       ├── config/
│       │   └── infer_cfg_ppvehicle.yml   # Configuration file (UK settings)
│       ├── ppvehicle/
│       │   ├── rec_word_dict.txt         # Chinese OCR dictionary (legacy)
│       │   └── uk_license_dict.txt       # UK license plate dictionary
│       └── pipeline.py                   # Full PaddleOCR version
├── test_data/
│   ├── 1.jpg                            # Test image 1
│   └── 2.jpg                            # Test image 2
├── output/                              # Simple demo results
│   ├── result_1.jpg                     # Processed results
│   └── result_2.jpg
├── output_paddleocr/                    # PaddleOCR results
│   ├── paddleocr_result_1.jpg           # Real OCR results
│   └── paddleocr_result_2.jpg
├── requirements.txt                     # Python dependencies
├── setup.sh                           # Automated setup script
├── test_setup.py                      # Validation script
└── README.md                          # This file
```

## 🎯 Example Output

When you run the demo, you'll see output like this:

```
============================================================
PaddleDetection Vehicle License Plate Recognition - Demo
============================================================

Processing: 1.jpg
----------------------------------------
Image shape: (480, 640, 3)
Detected 1 vehicle regions
Detected 11 license plates
🚗 Vehicle 0: License Plate = 'AB12 CDE', Confidence = 0.845
🚗 Vehicle 0: License Plate = 'FG34 HIJ', Confidence = 0.860
🚗 Vehicle 0: License Plate = 'BD51 SMR', Confidence = 0.875

============================================================
PROCESSING SUMMARY
============================================================
📊 Total images processed: 1
📊 Total license plates detected: 11
📊 Results saved in: output/

🏆 Detected License Plates:
    1. AB12 CDE (confidence: 0.845)
    2. FG34 HIJ (confidence: 0.860)
    3. BD51 SMR (confidence: 0.875)

============================================================
Demo completed successfully! 🎉
```

## 🛠️ Configuration

The main configuration is in `deploy/pipeline/config/infer_cfg_ppvehicle.yml`:

```yaml
VEHICLE_PLATE:
  enable: True
  det_db_thresh: 0.25       # Detection confidence threshold (lower for UK)
  det_db_box_thresh: 0.45   # Bounding box threshold
  rec_thresh: 0.45          # Recognition threshold
  ocr_language: "en"        # English for UK plates

OUTPUT:
  output_dir: "./output"
  save_images: True
  save_results: True
```

## 🧪 How the Demo Works

1. **Vehicle Detection**: Simulates vehicle detection by creating regions of interest in the image
2. **UK License Plate Detection**: Uses OpenCV edge detection and contour analysis to find rectangular regions with UK license plate aspect ratios (4.5:1 to 5.5:1)
3. **Text Recognition**: Simulates OCR by returning sample UK license plate numbers (AB12 CDE format) with realistic confidence scores
4. **Visualization**: Draws bounding boxes around detected vehicles (green) and license plates (red) with confidence scores

## 🔧 Dependencies

### Minimal (Simple Demo)
- OpenCV (computer vision)
- NumPy (numerical computing) 
- PyYAML (configuration files)

### Full Version (Advanced)
- PaddlePaddle (deep learning framework)
- PaddleOCR (OCR toolkit)
- All minimal dependencies above

## 🚨 Troubleshooting

### 1. Import Errors
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Install missing packages
pip install opencv-python numpy PyYAML
```

### 2. Image Not Found
Make sure your image paths are correct:
```bash
ls test_data/  # Should show 1.jpg, 2.jpg
```

### 3. No Output Generated
Check that output directory exists and has write permissions:
```bash
mkdir -p output
chmod 755 output
```

## 🎓 Educational Value

This example demonstrates:
- **Pipeline Architecture**: How vehicle detection → license plate detection → OCR recognition flows work
- **Computer Vision Basics**: Edge detection, contour analysis, and region filtering optimized for UK license plates
- **Configuration Management**: YAML-based configuration systems
- **Batch Processing**: Handling multiple images efficiently
- **Result Visualization**: Drawing detection results on images
- **UK License Plate Formats**: Understanding current (AB12 CDE) and older (M123 ABC) UK plate formats

## 🚀 Next Steps for Production

To convert this demo into a production system:

1. **Vehicle Detection**: Replace simulated vehicle detection with PP-YOLOE model
2. **OCR Integration**: Integrate real PaddleOCR for accurate UK text recognition (lang='en')
3. **UK-Specific Tuning**: Fine-tune detection parameters for UK license plate fonts and formats
4. **Video Processing**: Add support for video file processing with frame skipping
5. **Tracking**: Implement vehicle tracking across video frames
6. **Result Stabilization**: Add logic to stabilize license plate recognition across multiple frames
7. **DVLA Compliance**: Ensure compliance with UK DVLA license plate standards and formats
8. **Performance Optimization**: GPU acceleration, model optimization, and batch processing

## 📚 Further Reading

- [PaddleDetection Official Documentation](https://github.com/PaddlePaddle/PaddleDetection)
- [PP-Vehicle Tutorial](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.8.1/deploy/pipeline/docs/tutorials/ppvehicle_plate_en.md)
- [PaddleOCR Documentation](https://github.com/PaddlePaddle/PaddleOCR)
- [OpenCV Documentation](https://docs.opencv.org/)

---

## 📄 License

This example is provided for educational purposes. Please refer to the original PaddleDetection license for usage terms.

## 🇬🇧 UK License Plate Information

This demo supports UK license plate formats:

### Current Format (2001-present)
- **Format**: `AB12 CDE`
- **Structure**: 2 letters + 2 numbers + space + 3 letters
- **Examples**: BD51 SMR, LK03 ABC, AB12 CDE

### Older Formats
- **Format**: `M123 ABC` (1983-2001)
- **Format**: `H456 DEF` 
- **Structure**: 1 letter + 3 numbers + space + 3 letters

The demo randomly generates these formats to simulate realistic UK license plate recognition.

**Happy coding! 🎉**

## Project Structure

```
paddle_detection/
├── deploy/
│   └── pipeline/
│       ├── config/
│       │   └── infer_cfg_ppvehicle.yml    # Configuration file
│       ├── ppvehicle/
│       │   └── rec_word_dict.txt          # OCR dictionary
│       └── pipeline.py                    # Main pipeline script
├── test_data/
│   ├── 1.jpg                             # Test image 1
│   └── 2.jpg                             # Test image 2
├── output/                               # Generated results
├── requirements.txt                      # Python dependencies
├── setup.sh                            # Setup script
└── README.md                           # This file
```

## Configuration

The main configuration is in `deploy/pipeline/config/infer_cfg_ppvehicle.yml`:

- **VEHICLE_PLATE.enable**: Enable/disable license plate recognition
- **VEHICLE_PLATE.det_db_thresh**: Detection confidence threshold
- **VEHICLE_PLATE.rec_thresh**: Recognition confidence threshold

## Dependencies

- PaddlePaddle (>=2.4.0) - Deep learning framework
- PaddleOCR (>=2.6.0) - OCR toolkit for text detection and recognition
- OpenCV - Computer vision library
- NumPy - Numerical computing
- PyYAML - YAML file parsing

## How It Works

1. **Vehicle Detection**: For this minimal example, we assume the entire image contains a vehicle. In the full PaddleDetection pipeline, PP-YOLOE is used for accurate vehicle detection.

2. **License Plate Detection**: Uses PaddleOCR's detection model to find license plate regions within vehicle areas.

3. **Text Recognition**: Uses PaddleOCR's recognition model to extract text from detected license plates.

4. **Post-processing**: Applies confidence thresholds and generates visualization results.

## Example Output

The script will:
- Print detected license plate text and confidence scores to console
- Save visualization images with bounding boxes to the output directory
- Display processing statistics

## Limitations of This Minimal Example

- Simplified vehicle detection (assumes whole image is vehicle)
- No vehicle tracking across video frames
- No frame skipping optimization for videos
- Basic result stabilization

For production use, refer to the full PaddleDetection implementation which includes:
- PP-YOLOE vehicle detection model
- Multi-object tracking
- Video processing optimization
- Advanced result stabilization strategies

## Troubleshooting

1. **GPU Issues**: If you don't have a GPU, change `paddlepaddle-gpu` to `paddlepaddle` in `requirements.txt`

2. **Memory Issues**: Reduce batch size in the config file:
   ```yaml
   VEHICLE_PLATE:
     rec_batch_num: 1  # Reduce from 6 to 1
   ```

3. **Import Errors**: Make sure virtual environment is activated:
   ```bash
   source .venv/bin/activate
   ```

## Further Reading

- [PaddleDetection Official Documentation](https://github.com/PaddlePaddle/PaddleDetection)
- [PP-Vehicle Tutorial](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.8.1/deploy/pipeline/docs/tutorials/ppvehicle_plate_en.md)
- [PaddleOCR Documentation](https://github.com/PaddlePaddle/PaddleOCR)

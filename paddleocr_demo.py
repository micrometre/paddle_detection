#!/usr/bin/env python
"""
PaddleDetection UK Vehicle License Plate Recognition with PaddleOCR Integration
Real OCR-based UK license plate recognition
"""
import os
import sys
import argparse
import cv2
import yaml
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import dependencies with error handling
try:
    import paddle
    PADDLE_AVAILABLE = True
    logger.info(f"PaddlePaddle version: {paddle.__version__}")
except ImportError:
    PADDLE_AVAILABLE = False
    logger.warning("PaddlePaddle not available")

try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
    logger.info("PaddleOCR is available")
except ImportError:
    PADDLEOCR_AVAILABLE = False
    logger.warning("PaddleOCR not available")

class UKLicensePlateDetector:
    def __init__(self, config_path):
        """Initialize the UK license plate detector with PaddleOCR"""
        self.config = self.load_config(config_path)
        self.setup_models()
        
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
        
    def setup_models(self):
        """Setup PaddleOCR models for UK license plate detection and recognition"""
        if not PADDLEOCR_AVAILABLE:
            logger.error("PaddleOCR is not available. Please install it with: pip install paddleocr")
            raise ImportError("PaddleOCR is required for this integration")
            
        try:
            # Initialize PaddleOCR for UK license plates
            # Use English language and disable GPU to avoid compatibility issues
            logger.info("Initializing PaddleOCR for UK license plates...")
            self.ocr = PaddleOCR(
                use_angle_cls=False,  # Disable angle classification for stability
                lang='en',           # English for UK plates
                use_gpu=False,       # Use CPU for better compatibility
                show_log=False       # Reduce log verbosity
            )
            logger.info("PaddleOCR initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize PaddleOCR: {e}")
            # Fallback initialization
            try:
                self.ocr = PaddleOCR(lang='en', use_gpu=False)
                logger.info("PaddleOCR initialized with fallback settings")
            except Exception as e2:
                logger.error(f"Fallback initialization also failed: {e2}")
                raise
        
    def detect_vehicles(self, image):
        """Mock vehicle detection - returns regions where vehicles might be"""
        h, w = image.shape[:2]
        
        # For demo purposes, we'll create regions that might contain vehicles
        regions = [
            (int(w*0.1), int(h*0.2), int(w*0.9), int(h*0.8)),  # Main central region
            (int(w*0.05), int(h*0.1), int(w*0.95), int(h*0.6)),  # Upper region
            (int(w*0.05), int(h*0.4), int(w*0.95), int(h*0.9))   # Lower region
        ]
        
        return regions[:2]  # Return two regions for better coverage
        
    def preprocess_for_ocr(self, image_region):
        """Preprocess image region for better OCR results"""
        # Convert to grayscale
        if len(image_region.shape) == 3:
            gray = cv2.cvtColor(image_region, cv2.COLOR_BGR2GRAY)
        else:
            gray = image_region
            
        # Apply histogram equalization to improve contrast
        equalized = cv2.equalizeHist(gray)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(equalized, (3, 3), 0)
        
        # Convert back to BGR for PaddleOCR
        processed = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
        
        return processed
        
    def filter_uk_license_plate_text(self, text, confidence):
        """Filter and validate UK license plate text patterns"""
        if not text or confidence < 0.3:  # Low confidence threshold
            return None, 0
            
        # Clean the text
        text = text.upper().strip()
        
        # Remove common OCR artifacts and clean up
        text = text.replace('|', 'I').replace('0', 'O')  # Common OCR mistakes
        text = ''.join(c for c in text if c.isalnum() or c in [' ', '-'])  # Keep only valid chars
        
        # UK license plate patterns (more flexible)
        uk_patterns = [
            # Current format: AB12 CDE (2001-present)
            r'^[A-Z]{2}[0-9]{2}\s*[A-Z]{3}$',
            # Older format: M123 ABC (1983-2001) 
            r'^[A-Z][0-9]{3}\s*[A-Z]{3}$',
            # Very old format: ABC 123D (1963-1983)
            r'^[A-Z]{3}\s*[0-9]{3}[A-Z]$',
            # Older format: 123 ABC (before 1963)
            r'^[0-9]{3}\s*[A-Z]{3}$',
            # European format (some UK territories): AB-12-CD
            r'^[A-Z]{2}[-\s]*[0-9]{2}[-\s]*[A-Z]{2,3}$',
            # Flexible format for partial matches
            r'^[A-Z0-9]{4,7}[-\s]*[A-Z0-9]{0,4}$'
        ]
        
        import re
        
        # First try exact UK patterns
        for pattern in uk_patterns[:-1]:  # Exclude the flexible pattern first
            if re.match(pattern, text.replace(' ', '').replace('-', '')):
                # Format with proper spacing for standard UK format
                clean_text = text.replace(' ', '').replace('-', '')
                if len(clean_text) >= 6:
                    if clean_text[2:4].isdigit() and len(clean_text) == 7:  # Current format
                        formatted = f"{clean_text[:2]}{clean_text[2:4]} {clean_text[4:]}"
                    elif clean_text[1:4].isdigit():  # Older format M123ABC
                        formatted = f"{clean_text[0]}{clean_text[1:4]} {clean_text[4:]}"
                    else:  # Other formats
                        formatted = text.replace('-', ' ') if '-' in text else text
                    return formatted.strip(), confidence
                    
        # Try the flexible pattern for unusual formats
        if re.match(uk_patterns[-1], text):
            # Check if it has reasonable mix of letters and numbers
            has_letters = any(c.isalpha() for c in text)
            has_numbers = any(c.isdigit() for c in text)
            
            if has_letters and has_numbers and len(text.replace(' ', '').replace('-', '')) >= 4:
                # Return as-is but reduce confidence
                return text.strip(), confidence * 0.7
                    
        return None, 0
        
    def detect_license_plates(self, image, vehicle_boxes):
        """Detect and recognize UK license plates using PaddleOCR"""
        results = []
        
        for i, (x1, y1, x2, y2) in enumerate(vehicle_boxes):
            # Crop vehicle region
            vehicle_crop = image[y1:y2, x1:x2]
            
            if vehicle_crop.size == 0:
                continue
                
            logger.info(f"Processing vehicle region {i+1}: {vehicle_crop.shape}")
            
            # Preprocess the region for better OCR
            processed_crop = self.preprocess_for_ocr(vehicle_crop)
            
            try:
                # Use PaddleOCR to detect and recognize text
                ocr_results = self.ocr.ocr(processed_crop, cls=False)
                
                if ocr_results and ocr_results[0]:
                    for line in ocr_results[0]:
                        if line:
                            # Extract text and confidence
                            bbox, (text, confidence) = line
                            
                            logger.info(f"Raw OCR result: '{text}' (confidence: {confidence:.3f})")
                            
                            # Filter and validate UK license plate text
                            filtered_text, filtered_confidence = self.filter_uk_license_plate_text(text, confidence)
                            
                            if filtered_text:
                                # Convert relative coordinates to absolute
                                abs_bbox = []
                                for point in bbox:
                                    abs_x = int(point[0] + x1)
                                    abs_y = int(point[1] + y1)
                                    abs_bbox.append([abs_x, abs_y])
                                
                                results.append({
                                    'vehicle_id': i,
                                    'license_plate': filtered_text,
                                    'confidence': filtered_confidence,
                                    'bbox': abs_bbox,
                                    'vehicle_bbox': [x1, y1, x2, y2],
                                    'raw_ocr_text': text,
                                    'raw_confidence': confidence
                                })
                                
                                logger.info(f"✓ Valid UK plate detected: '{filtered_text}' (confidence: {filtered_confidence:.3f})")
                            else:
                                logger.info(f"✗ Text filtered out: '{text}' (not UK plate format)")
                                
            except Exception as e:
                logger.error(f"OCR error for vehicle {i}: {e}")
                continue
                
        return results
        
    def process_image(self, image_path):
        """Process a single image"""
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Could not load image {image_path}")
            return []
            
        logger.info(f"Processing image: {image_path}")
        logger.info(f"Image shape: {image.shape}")
        
        # Step 1: Detect vehicles
        vehicle_boxes = self.detect_vehicles(image)
        logger.info(f"Detected {len(vehicle_boxes)} vehicle regions")
        
        # Step 2: Detect license plates
        plate_results = self.detect_license_plates(image, vehicle_boxes)
        logger.info(f"Detected {len(plate_results)} UK license plates")
        
        return plate_results
        
    def draw_results(self, image_path, results, output_path):
        """Draw detection results on image"""
        image = cv2.imread(image_path)
        
        for result in results:
            # Draw vehicle bounding box in green
            x1, y1, x2, y2 = result['vehicle_bbox']
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Add vehicle label
            cv2.putText(image, f"Vehicle {result['vehicle_id']}", (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Draw license plate bounding box in red
            bbox = result['bbox']
            pts = np.array(bbox, np.int32).reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, (0, 0, 255), 2)
            
            # Add license plate text with confidence
            text = f"{result['license_plate']} ({result['confidence']:.2f})"
            text_x = bbox[0][0]
            text_y = bbox[0][1] - 5
            
            # Add background rectangle for better text visibility
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(image, (text_x, text_y - text_size[1] - 5), 
                         (text_x + text_size[0], text_y), (255, 255, 255), -1)
            cv2.putText(image, text, (text_x, text_y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
        cv2.imwrite(output_path, image)
        logger.info(f"Results saved to: {output_path}")

def parse_args():
    parser = argparse.ArgumentParser(description='UK License Plate Recognition with PaddleOCR')
    parser.add_argument('--config', type=str, required=True,
                        help='Path to config file')
    parser.add_argument('--image_file', type=str, default=None,
                        help='Path to single image file')
    parser.add_argument('--image_dir', type=str, default=None,
                        help='Path to image directory')
    parser.add_argument('--output_dir', type=str, default='output_paddleocr',
                        help='Output directory for results')
    parser.add_argument('--device', type=str, default='cpu',
                        help='Device to use: cpu or gpu')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose logging')
    
    return parser.parse_args()

def main():
    print("=" * 70)
    print("PaddleDetection UK Vehicle License Plate Recognition - PaddleOCR")
    print("=" * 70)
    print()
    
    args = parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not PADDLEOCR_AVAILABLE:
        print("❌ PaddleOCR is not available!")
        print("Please install it with: pip install paddleocr")
        print("Or run the simple demo version: python simple_demo.py")
        return
    
    print("✅ Using real PaddleOCR for UK license plate recognition")
    print()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize detector
    try:
        detector = UKLicensePlateDetector(args.config)
        print("🔧 UK License Plate Detector with PaddleOCR initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize detector: {e}")
        return
    
    # Process images
    image_files = []
    if args.image_file:
        image_files = [args.image_file]
    elif args.image_dir:
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            image_files.extend(Path(args.image_dir).glob(ext))
        image_files = [str(p) for p in image_files]
    
    if not image_files:
        print("❌ No images found to process!")
        return
        
    print(f"📊 Processing {len(image_files)} images...")
    print()
    
    all_results = []
    for image_file in image_files:
        print(f"🖼️  Processing: {os.path.basename(image_file)}")
        print("-" * 50)
        
        # Process image
        results = detector.process_image(image_file)
        all_results.extend(results)
        
        # Print results
        if results:
            for result in results:
                print(f"🚗 Vehicle {result['vehicle_id']}: UK License Plate = '{result['license_plate']}'")
                print(f"   📊 Confidence = {result['confidence']:.3f}")
                print(f"   🔍 Raw OCR: '{result['raw_ocr_text']}' (conf: {result['raw_confidence']:.3f})")
        else:
            print("   ❌ No UK license plates detected in this image")
        
        # Save visualization
        output_path = os.path.join(args.output_dir, f"paddleocr_result_{os.path.basename(image_file)}")
        detector.draw_results(image_file, results, output_path)
        print()
    
    # Summary
    print("=" * 70)
    print("🎯 PROCESSING SUMMARY")
    print("=" * 70)
    print(f"📊 Total images processed: {len(image_files)}")
    print(f"📊 Total UK license plates detected: {len(all_results)}")
    print(f"📊 Results saved in: {args.output_dir}/")
    
    if all_results:
        print("\n🏆 Detected UK License Plates:")
        for i, result in enumerate(all_results, 1):
            print(f"   {i:2d}. {result['license_plate']:10s} (confidence: {result['confidence']:.3f}) "
                  f"[raw: '{result['raw_ocr_text']}']")
    
    print("\n" + "=" * 70)
    print("🎉 Real PaddleOCR processing completed successfully!")
    print()
    print("💡 Tips for better results:")
    print("   • Use high-resolution images with clear license plates")
    print("   • Ensure good lighting and minimal blur")
    print("   • License plates should be relatively straight (not too angled)")
    print("   • Try different preprocessing if results are poor")

if __name__ == '__main__':
    main()

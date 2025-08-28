#!/usr/bin/env python
"""
Minimal PaddleDetection UK Vehicle License Plate Recognition Pipeline
Based on PaddleDetection/deploy/pipeline/pipeline.py
"""
import os
import sys
import argparse
import cv2
import yaml
import numpy as np
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import paddle
    print(f"PaddlePaddle version: {paddle.__version__}")
except ImportError:
    print("PaddlePaddle not installed. Installing...")
    import paddle

try:
    from paddleocr import PaddleOCR
    print("PaddleOCR is available")
except ImportError:
    print("PaddleOCR not installed. Installing...")
    from paddleocr import PaddleOCR

class VehiclePlateDetector:
    def __init__(self, config_path):
        """Initialize the vehicle plate detector"""
        self.config = self.load_config(config_path)
        self.setup_models()
        
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
        
    def setup_models(self):
        """Setup OCR models for UK license plate detection and recognition"""
        try:
            # Initialize PaddleOCR for UK license plate detection and recognition
            # Use English language for UK plates
            self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
            print("PaddleOCR initialized successfully for UK license plates")
        except Exception as e:
            print(f"Error initializing PaddleOCR: {e}")
            # Simple fallback
            self.ocr = PaddleOCR(lang='en')
            print("PaddleOCR initialized with fallback settings for UK plates")
        
    def detect_vehicles(self, image):
        """Mock vehicle detection - in real implementation, use PP-YOLOE"""
        # For this minimal example, we'll assume the entire image contains a vehicle
        h, w = image.shape[:2]
        # Return a bounding box covering most of the image
        return [(int(w*0.1), int(h*0.1), int(w*0.9), int(h*0.9))]
        
    def detect_license_plates(self, image, vehicle_boxes):
        """Detect and recognize license plates in vehicle regions"""
        results = []
        
        for i, (x1, y1, x2, y2) in enumerate(vehicle_boxes):
            # Crop vehicle region
            vehicle_crop = image[y1:y2, x1:x2]
            
            # Use PaddleOCR to detect and recognize text (license plates)
            ocr_results = self.ocr.ocr(vehicle_crop, cls=True)
            
            if ocr_results and ocr_results[0]:
                for line in ocr_results[0]:
                    if line:
                        # Extract text and confidence
                        text = line[1][0]
                        confidence = line[1][1]
                        bbox = line[0]
                        
                        # Convert relative coordinates to absolute
                        abs_bbox = []
                        for point in bbox:
                            abs_x = int(point[0] + x1)
                            abs_y = int(point[1] + y1)
                            abs_bbox.append([abs_x, abs_y])
                        
                        results.append({
                            'vehicle_id': i,
                            'license_plate': text,
                            'confidence': confidence,
                            'bbox': abs_bbox,
                            'vehicle_bbox': [x1, y1, x2, y2]
                        })
                        
        return results
        
    def process_image(self, image_path):
        """Process a single image"""
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image {image_path}")
            return []
            
        # Step 1: Detect vehicles
        vehicle_boxes = self.detect_vehicles(image)
        print(f"Detected {len(vehicle_boxes)} vehicles")
        
        # Step 2: Detect license plates
        plate_results = self.detect_license_plates(image, vehicle_boxes)
        
        return plate_results
        
    def draw_results(self, image_path, results, output_path):
        """Draw detection results on image"""
        image = cv2.imread(image_path)
        
        for result in results:
            # Draw vehicle bounding box
            x1, y1, x2, y2 = result['vehicle_bbox']
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw license plate bounding box
            bbox = result['bbox']
            pts = np.array(bbox, np.int32).reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, (0, 0, 255), 2)
            
            # Add text
            text = f"{result['license_plate']} ({result['confidence']:.2f})"
            cv2.putText(image, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        cv2.imwrite(output_path, image)
        print(f"Results saved to: {output_path}")

def parse_args():
    parser = argparse.ArgumentParser(description='PP-Vehicle License Plate Recognition')
    parser.add_argument('--config', type=str, required=True,
                        help='Path to config file')
    parser.add_argument('--image_file', type=str, default=None,
                        help='Path to single image file')
    parser.add_argument('--image_dir', type=str, default=None,
                        help='Path to image directory')
    parser.add_argument('--output_dir', type=str, default='output',
                        help='Output directory for results')
    parser.add_argument('--device', type=str, default='cpu',
                        help='Device to use: cpu or gpu')
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize detector
    detector = VehiclePlateDetector(args.config)
    
    # Process images
    image_files = []
    if args.image_file:
        image_files = [args.image_file]
    elif args.image_dir:
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            image_files.extend(Path(args.image_dir).glob(ext))
        image_files = [str(p) for p in image_files]
    
    if not image_files:
        print("No images found to process!")
        return
        
    print(f"Processing {len(image_files)} images...")
    
    for image_file in image_files:
        print(f"\nProcessing: {image_file}")
        
        # Process image
        results = detector.process_image(image_file)
        
        # Print results
        for result in results:
            print(f"Vehicle {result['vehicle_id']}: License Plate = '{result['license_plate']}', "
                  f"Confidence = {result['confidence']:.3f}")
        
        # Save visualization
        output_path = os.path.join(args.output_dir, f"result_{os.path.basename(image_file)}")
        detector.draw_results(image_file, results, output_path)

if __name__ == '__main__':
    main()

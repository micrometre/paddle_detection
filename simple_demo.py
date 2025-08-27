#!/usr/bin/env python
"""
Simple PaddleDetection Vehicle License Plate Recognition Demo
A minimal working example that demonstrates the pipeline concept
"""
import os
import sys
import argparse
import cv2
import yaml
import numpy as np
from pathlib import Path
import re

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try importing paddle - if it fails, we'll show a demo without actual OCR
try:
    import paddle
    PADDLE_AVAILABLE = True
    print(f"PaddlePaddle version: {paddle.__version__}")
except ImportError:
    PADDLE_AVAILABLE = False
    print("PaddlePaddle not available - running in demo mode")

class SimpleLicensePlateDetector:
    def __init__(self, config_path):
        """Initialize the simple license plate detector"""
        self.config = self.load_config(config_path)
        print("Simple UK License Plate Detector initialized")
        
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
        
    def detect_vehicles(self, image):
        """Mock vehicle detection - returns regions where vehicles might be"""
        h, w = image.shape[:2]
        
        # For demo purposes, we'll divide the image into regions
        # In real implementation, this would use PP-YOLOE
        regions = [
            (int(w*0.1), int(h*0.1), int(w*0.9), int(h*0.9)),  # Full image as vehicle
            (int(w*0.2), int(h*0.2), int(w*0.8), int(h*0.6)),  # Upper region
            (int(w*0.1), int(h*0.4), int(w*0.9), int(h*0.9))   # Lower region
        ]
        
        return regions[:1]  # Return just one region for simplicity
        
    def simple_plate_detection(self, image_region):
        """Simple license plate detection using OpenCV"""
        # Convert to grayscale
        gray = cv2.cvtColor(image_region, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours that could be license plates
        plate_regions = []
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # UK license plate aspect ratio is typically around 4.5:1 to 5.5:1
            aspect_ratio = w / h if h > 0 else 0
            area = w * h
            
            # Filter based on size and aspect ratio for UK plates
            if (4.0 <= aspect_ratio <= 6.0 and 
                area > 800 and  # Minimum area (UK plates are wider)
                w > 80 and h > 15):  # Minimum dimensions for UK plates
                
                plate_regions.append((x, y, x+w, y+h))
        
        return plate_regions
        
    def simulate_ocr(self, plate_region):
        """Simulate OCR recognition - returns demo UK license plate numbers"""
        # Demo UK license plates with different formats
        # Current format (2001-present): 2 letters + 2 numbers + 3 letters
        # Old format examples also included for variety
        demo_plates = [
            "AB12 CDE",  # Current format
            "FG34 HIJ",  # Current format
            "KL56 MNO",  # Current format
            "PQ78 RST",  # Current format
            "UV90 WXY",  # Current format
            "BD51 SMR",  # Real-style current format
            "LK03 ABC",  # Real-style current format
            "M123 ABC",  # Older format (1983-2001)
            "H456 DEF",  # Older format
            "R789 GHI"   # Older format
        ]
        
        # Return a demo plate based on region characteristics
        h, w = plate_region.shape[:2]
        index = (w + h) % len(demo_plates)
        confidence = 0.82 + (index * 0.015)  # UK OCR typically has slightly lower confidence
        
        return demo_plates[index], confidence
        
    def detect_license_plates(self, image, vehicle_boxes):
        """Detect and recognize license plates in vehicle regions"""
        results = []
        
        for i, (x1, y1, x2, y2) in enumerate(vehicle_boxes):
            # Crop vehicle region
            vehicle_crop = image[y1:y2, x1:x2]
            
            if vehicle_crop.size == 0:
                continue
                
            # Detect potential license plate regions
            plate_regions = self.simple_plate_detection(vehicle_crop)
            
            for px1, py1, px2, py2 in plate_regions:
                # Extract plate region
                plate_crop = vehicle_crop[py1:py2, px1:px2]
                
                if plate_crop.size == 0:
                    continue
                
                # Simulate OCR
                license_text, confidence = self.simulate_ocr(plate_crop)
                
                # Convert to absolute coordinates
                abs_x1 = x1 + px1
                abs_y1 = y1 + py1
                abs_x2 = x1 + px2
                abs_y2 = y1 + py2
                
                results.append({
                    'vehicle_id': i,
                    'license_plate': license_text,
                    'confidence': confidence,
                    'bbox': [[abs_x1, abs_y1], [abs_x2, abs_y1], 
                            [abs_x2, abs_y2], [abs_x1, abs_y2]],
                    'vehicle_bbox': [x1, y1, x2, y2]
                })
                
        return results
        
    def process_image(self, image_path):
        """Process a single image"""
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image {image_path}")
            return []
            
        print(f"Image shape: {image.shape}")
        
        # Step 1: Detect vehicles
        vehicle_boxes = self.detect_vehicles(image)
        print(f"Detected {len(vehicle_boxes)} vehicle regions")
        
        # Step 2: Detect license plates
        plate_results = self.detect_license_plates(image, vehicle_boxes)
        print(f"Detected {len(plate_results)} license plates")
        
        return plate_results
        
    def draw_results(self, image_path, results, output_path):
        """Draw detection results on image"""
        image = cv2.imread(image_path)
        
        for result in results:
            # Draw vehicle bounding box in green
            x1, y1, x2, y2 = result['vehicle_bbox']
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, "Vehicle", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw license plate bounding box in red
            bbox = result['bbox']
            pts = np.array(bbox, np.int32).reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, (0, 0, 255), 2)
            
            # Add license plate text
            text = f"{result['license_plate']} ({result['confidence']:.2f})"
            text_x = bbox[0][0]
            text_y = bbox[0][1] - 5
            cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
        cv2.imwrite(output_path, image)
        print(f"Results saved to: {output_path}")

def parse_args():
    parser = argparse.ArgumentParser(description='Simple UK License Plate Recognition Demo')
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
    print("=" * 60)
    print("PaddleDetection UK Vehicle License Plate Recognition - Demo")
    print("=" * 60)
    print()
    
    if not PADDLE_AVAILABLE:
        print("⚠️  Note: This is a DEMO version without actual PaddlePaddle OCR")
        print("   For full functionality, ensure PaddlePaddle and PaddleOCR are properly installed")
        print("   This demo simulates UK license plate recognition")
        print()
    
    args = parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize detector
    detector = SimpleLicensePlateDetector(args.config)
    
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
    print()
    
    all_results = []
    for image_file in image_files:
        print(f"Processing: {os.path.basename(image_file)}")
        print("-" * 40)
        
        # Process image
        results = detector.process_image(image_file)
        all_results.extend(results)
        
        # Print results
        if results:
            for result in results:
                print(f"🚗 Vehicle {result['vehicle_id']}: License Plate = '{result['license_plate']}', "
                      f"Confidence = {result['confidence']:.3f}")
        else:
            print("   No license plates detected in this image")
        
        # Save visualization
        output_path = os.path.join(args.output_dir, f"result_{os.path.basename(image_file)}")
        detector.draw_results(image_file, results, output_path)
        print()
    
    # Summary
    print("=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)
    print(f"📊 Total images processed: {len(image_files)}")
    print(f"📊 Total license plates detected: {len(all_results)}")
    print(f"📊 Results saved in: {args.output_dir}/")
    
    if all_results:
        print("\n🏆 Detected License Plates:")
        for i, result in enumerate(all_results, 1):
            print(f"   {i:2d}. {result['license_plate']} (confidence: {result['confidence']:.3f})")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully! 🎉")
    
    if not PADDLE_AVAILABLE:
        print("\nFor real UK license plate recognition:")
        print("1. Install PaddlePaddle: pip install paddlepaddle")
        print("2. Install PaddleOCR: pip install paddleocr")
        print("3. Configure PaddleOCR for English/Latin characters: lang='en'")
        print("4. Replace the demo OCR with actual PaddleOCR integration")
        print("5. Train or use models specifically tuned for UK license plate fonts")

if __name__ == '__main__':
    main()

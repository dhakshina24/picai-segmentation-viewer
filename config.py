"""Configuration file for input/output paths."""
import os 

PROJECT_DIR = "./picai-segmentation-viewer"
INPUT_DIR = os.path.join(PROJECT_DIR, "test")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output_debug")
SEG_PATH = os.path.join(OUTPUT_DIR, "images", "cspca-detection-map", "cspca_detection_map.mha")
SCORE_PATH = os.path.join(OUTPUT_DIR, "cspca-case-level-likelihood.json")
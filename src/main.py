"""
Main Execution Script
UIDAI Hackathon 2026 - Aadhaar Lifecycle Analysis

Author: Siddhi Rohan
Date: 11th January 2026
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loading import load_all_datasets
from analysis import calculate_lifecycle_metrics, print_key_findings
from visualizations import create_all_figures


def main(data_path: str = 'data/', output_path: str = 'figures/'):
    """
    Run the complete Aadhaar Lifecycle Analysis.
    
    Args:
        data_path: Path to data directory
        output_path: Path for output figures
    """
    print("="*70)
    print("UIDAI HACKATHON 2026 - AADHAAR LIFECYCLE ANALYSIS")
    print("="*70)
    print()
    
    # Create output directory if needed
    os.makedirs(output_path, exist_ok=True)
    
    # Step 1: Load and preprocess data
    print("[Step 1/3] Loading and preprocessing data...")
    enrol, demo, bio = load_all_datasets(data_path)
    print()
    
    # Step 2: Run analysis
    print("[Step 2/3] Running analysis...")
    metrics = calculate_lifecycle_metrics(enrol, demo, bio)
    print()
    
    # Step 3: Generate visualizations
    print("[Step 3/3] Generating visualizations...")
    create_all_figures(enrol, demo, bio, output_path)
    print()
    
    # Print key findings
    print_key_findings(metrics)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nFigures saved to: {output_path}")
    
    return metrics


if __name__ == "__main__":
    # Default paths - modify as needed
    DATA_PATH = 'data/'
    OUTPUT_PATH = 'figures/'
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        DATA_PATH = sys.argv[1]
    if len(sys.argv) > 2:
        OUTPUT_PATH = sys.argv[2]
    
    metrics = main(DATA_PATH, OUTPUT_PATH)

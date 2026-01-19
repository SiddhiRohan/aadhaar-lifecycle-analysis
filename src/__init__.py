"""
Aadhaar Lifecycle Analysis Package
UIDAI Hackathon 2026
"""

from .data_loading import load_all_datasets
from .analysis import calculate_lifecycle_metrics, print_key_findings
from .visualizations import create_all_figures

__version__ = '1.0.0'
__author__ = 'Siddhi Rohan'

"""
Data Loading and Preprocessing Module
UIDAI Hackathon 2026 - Aadhaar Lifecycle Analysis
"""

import pandas as pd
import numpy as np
from typing import Tuple, List

# File configurations
ENROL_FILES = [
    'api_data_aadhar_enrolment_0_500000.csv',
    'api_data_aadhar_enrolment_500000_1000000.csv',
    'api_data_aadhar_enrolment_1000000_1006029.csv'
]

DEMO_FILES = [
    'api_data_aadhar_demographic_0_500000.csv',
    'api_data_aadhar_demographic_500000_1000000.csv',
    'api_data_aadhar_demographic_1000000_1500000.csv',
    'api_data_aadhar_demographic_1500000_2000000.csv',
    'api_data_aadhar_demographic_2000000_2071700.csv'
]

BIO_FILES = [
    'api_data_aadhar_biometric_0_500000.csv',
    'api_data_aadhar_biometric_500000_1000000.csv',
    'api_data_aadhar_biometric_1000000_1500000.csv',
    'api_data_aadhar_biometric_1500000_1861108.csv'
]

# State name normalization mapping
STATE_MAPPING = {
    'West Bengal': 'West Bengal', 'west Bengal': 'West Bengal',
    'WEST BENGAL': 'West Bengal', 'West bengal': 'West Bengal',
    'Westbengal': 'West Bengal', 'West  Bengal': 'West Bengal',
    'WESTBENGAL': 'West Bengal', 'West Bangal': 'West Bengal',
    'Odisha': 'Odisha', 'odisha': 'Odisha', 'ODISHA': 'Odisha', 'Orissa': 'Odisha',
    'Chhattisgarh': 'Chhattisgarh', 'Chhatisgarh': 'Chhattisgarh',
    'Andhra Pradesh': 'Andhra Pradesh', 'andhra pradesh': 'Andhra Pradesh',
    'Tamil Nadu': 'Tamil Nadu', 'Tamilnadu': 'Tamil Nadu',
    'Uttarakhand': 'Uttarakhand', 'Uttaranchal': 'Uttarakhand',
    'Jammu and Kashmir': 'Jammu and Kashmir', 'Jammu & Kashmir': 'Jammu and Kashmir',
    'Jammu And Kashmir': 'Jammu and Kashmir',
    'Andaman and Nicobar Islands': 'Andaman and Nicobar Islands',
    'Andaman & Nicobar Islands': 'Andaman and Nicobar Islands',
    'Puducherry': 'Puducherry', 'Pondicherry': 'Puducherry',
    'Dadra and Nagar Haveli': 'Dadra and Nagar Haveli',
    'Dadra & Nagar Haveli': 'Dadra and Nagar Haveli',
    'Daman and Diu': 'Daman and Diu', 'Daman & Diu': 'Daman and Diu',
}

VALID_STATES = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
    'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Puducherry', 'Chandigarh',
    'Andaman and Nicobar Islands', 'Dadra and Nagar Haveli', 'Daman and Diu',
    'Lakshadweep'
]


def normalize_state(state: str) -> str:
    """Normalize state name to standard format."""
    return STATE_MAPPING.get(state, state)


def load_dataset(data_path: str, files: List[str], dataset_type: str) -> pd.DataFrame:
    """
    Load and concatenate multiple CSV files into a single DataFrame.
    
    Args:
        data_path: Path to data directory
        files: List of CSV filenames
        dataset_type: Type of dataset ('enrolment', 'demographic', 'biometric')
    
    Returns:
        Concatenated and preprocessed DataFrame
    """
    dfs = []
    for f in files:
        filepath = f"{data_path}/{f}"
        try:
            df = pd.read_csv(filepath)
            dfs.append(df)
        except FileNotFoundError:
            print(f"Warning: File not found - {filepath}")
    
    if not dfs:
        raise FileNotFoundError(f"No {dataset_type} files found in {data_path}")
    
    combined = pd.concat(dfs, ignore_index=True)
    
    # Parse dates
    combined['date'] = pd.to_datetime(combined['date'], format='%d-%m-%Y')
    
    # Rename columns for demographic and biometric datasets
    if dataset_type == 'demographic':
        combined.columns = ['date', 'state', 'district', 'pincode', 'demo_age_5_17', 'demo_age_17_plus']
        combined['total_demo_update'] = combined['demo_age_5_17'] + combined['demo_age_17_plus']
    elif dataset_type == 'biometric':
        combined.columns = ['date', 'state', 'district', 'pincode', 'bio_age_5_17', 'bio_age_17_plus']
        combined['total_bio_update'] = combined['bio_age_5_17'] + combined['bio_age_17_plus']
    elif dataset_type == 'enrolment':
        combined['total_enrolment'] = combined['age_0_5'] + combined['age_5_17'] + combined['age_18_greater']
    
    return combined


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataset by normalizing state names and filtering invalid entries.
    
    Args:
        df: Raw DataFrame
    
    Returns:
        Cleaned DataFrame
    """
    # Normalize state names
    df['state'] = df['state'].apply(normalize_state)
    
    # Filter to valid states only
    df_clean = df[df['state'].isin(VALID_STATES)].copy()
    
    return df_clean


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add temporal features for analysis.
    
    Args:
        df: DataFrame with date column
    
    Returns:
        DataFrame with added temporal features
    """
    df['month'] = df['date'].dt.to_period('M')
    df['day_of_week'] = df['date'].dt.day_name()
    df['is_weekend'] = df['date'].dt.dayofweek >= 5
    df['day'] = df['date'].dt.day
    
    return df


def load_all_datasets(data_path: str = 'data/') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load, clean, and preprocess all three datasets.
    
    Args:
        data_path: Path to data directory
    
    Returns:
        Tuple of (enrolment, demographic, biometric) DataFrames
    """
    print("Loading datasets...")
    
    # Load raw data
    enrol = load_dataset(data_path, ENROL_FILES, 'enrolment')
    demo = load_dataset(data_path, DEMO_FILES, 'demographic')
    bio = load_dataset(data_path, BIO_FILES, 'biometric')
    
    print(f"  Raw enrolment records: {len(enrol):,}")
    print(f"  Raw demographic records: {len(demo):,}")
    print(f"  Raw biometric records: {len(bio):,}")
    
    # Clean data
    print("Cleaning datasets...")
    enrol_clean = clean_dataset(enrol)
    demo_clean = clean_dataset(demo)
    bio_clean = clean_dataset(bio)
    
    print(f"  Cleaned enrolment records: {len(enrol_clean):,}")
    print(f"  Cleaned demographic records: {len(demo_clean):,}")
    print(f"  Cleaned biometric records: {len(bio_clean):,}")
    
    # Add temporal features
    print("Adding temporal features...")
    enrol_clean = add_temporal_features(enrol_clean)
    demo_clean = add_temporal_features(demo_clean)
    bio_clean = add_temporal_features(bio_clean)
    
    print("Data loading complete!")
    
    return enrol_clean, demo_clean, bio_clean


if __name__ == "__main__":
    # Test loading
    enrol, demo, bio = load_all_datasets("../data/")
    print(f"\nEnrolment shape: {enrol.shape}")
    print(f"Demographic shape: {demo.shape}")
    print(f"Biometric shape: {bio.shape}")

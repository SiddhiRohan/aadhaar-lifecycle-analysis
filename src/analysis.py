"""
Analysis Module
UIDAI Hackathon 2026 - Aadhaar Lifecycle Analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def calculate_volume_statistics(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate total volume statistics.
    
    Returns:
        Dictionary with volume metrics
    """
    return {
        'total_enrolment': enrol['total_enrolment'].sum(),
        'total_demo_update': demo['total_demo_update'].sum(),
        'total_bio_update': bio['total_bio_update'].sum(),
        'total_transactions': (
            enrol['total_enrolment'].sum() + 
            demo['total_demo_update'].sum() + 
            bio['total_bio_update'].sum()
        )
    }


def calculate_age_distribution(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate age group distributions for each dataset.
    
    Returns:
        Dictionary with age distribution metrics
    """
    total_enrol = enrol['total_enrolment'].sum()
    total_demo = demo['total_demo_update'].sum()
    total_bio = bio['total_bio_update'].sum()
    
    return {
        'enrolment': {
            'age_0_5': enrol['age_0_5'].sum(),
            'age_0_5_pct': 100 * enrol['age_0_5'].sum() / total_enrol,
            'age_5_17': enrol['age_5_17'].sum(),
            'age_5_17_pct': 100 * enrol['age_5_17'].sum() / total_enrol,
            'age_18_plus': enrol['age_18_greater'].sum(),
            'age_18_plus_pct': 100 * enrol['age_18_greater'].sum() / total_enrol,
        },
        'demographic': {
            'age_5_17': demo['demo_age_5_17'].sum(),
            'age_5_17_pct': 100 * demo['demo_age_5_17'].sum() / total_demo,
            'age_17_plus': demo['demo_age_17_plus'].sum(),
            'age_17_plus_pct': 100 * demo['demo_age_17_plus'].sum() / total_demo,
        },
        'biometric': {
            'age_5_17': bio['bio_age_5_17'].sum(),
            'age_5_17_pct': 100 * bio['bio_age_5_17'].sum() / total_bio,
            'age_17_plus': bio['bio_age_17_plus'].sum(),
            'age_17_plus_pct': 100 * bio['bio_age_17_plus'].sum() / total_bio,
        }
    }


def calculate_weekly_patterns(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze day-of-week patterns.
    
    Returns:
        Dictionary with weekly pattern metrics
    """
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    dow_enrol = enrol.groupby('day_of_week')['total_enrolment'].sum().reindex(day_order)
    dow_demo = demo.groupby('day_of_week')['total_demo_update'].sum().reindex(day_order)
    dow_bio = bio.groupby('day_of_week')['total_bio_update'].sum().reindex(day_order)
    
    # Weekend vs weekday analysis
    weekend_demo = demo[demo['is_weekend']].groupby('date')['total_demo_update'].sum().mean()
    weekday_demo = demo[~demo['is_weekend']].groupby('date')['total_demo_update'].sum().mean()
    
    return {
        'enrolment_by_dow': dow_enrol.to_dict(),
        'demographic_by_dow': dow_demo.to_dict(),
        'biometric_by_dow': dow_bio.to_dict(),
        'weekend_demo_avg': weekend_demo,
        'weekday_demo_avg': weekday_demo,
        'weekend_ratio': weekend_demo / weekday_demo
    }


def calculate_state_statistics(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate state-level statistics.
    
    Returns:
        Dictionary with state-level metrics
    """
    state_enrol = enrol.groupby('state')['total_enrolment'].sum().sort_values(ascending=False)
    state_demo = demo.groupby('state')['total_demo_update'].sum().sort_values(ascending=False)
    state_bio = bio.groupby('state')['total_bio_update'].sum().sort_values(ascending=False)
    
    # Child enrolment percentage by state
    child_pct = enrol.groupby('state').apply(
        lambda x: 100 * x['age_0_5'].sum() / x['total_enrolment'].sum()
    ).sort_values(ascending=False)
    
    return {
        'enrolment_by_state': state_enrol.to_dict(),
        'demographic_by_state': state_demo.to_dict(),
        'biometric_by_state': state_bio.to_dict(),
        'child_enrolment_pct_by_state': child_pct.to_dict(),
        'top_5_states_enrolment': state_enrol.head(5).to_dict(),
        'unique_states': enrol['state'].nunique(),
        'unique_districts': enrol['district'].nunique(),
        'unique_pincodes': enrol['pincode'].nunique()
    }


def calculate_update_ratios(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate update-to-enrolment ratios by state.
    
    Returns:
        DataFrame with ratios
    """
    state_enrol = enrol.groupby('state')['total_enrolment'].sum()
    state_demo = demo.groupby('state')['total_demo_update'].sum()
    state_bio = bio.groupby('state')['total_bio_update'].sum()
    
    ratios = pd.DataFrame({
        'enrolment': state_enrol,
        'demo': state_demo,
        'bio': state_bio
    }).fillna(0)
    
    # Filter to states with meaningful volumes
    ratios = ratios[ratios['enrolment'] > 10000]
    ratios['demo_ratio'] = ratios['demo'] / ratios['enrolment']
    ratios['bio_ratio'] = ratios['bio'] / ratios['enrolment']
    
    return ratios


def calculate_monthly_trends(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze monthly trends.
    
    Returns:
        Dictionary with monthly trend data
    """
    monthly_enrol = enrol.groupby('month')['total_enrolment'].sum()
    monthly_demo = demo.groupby('month')['total_demo_update'].sum()
    monthly_bio = bio.groupby('month')['total_bio_update'].sum()
    
    return {
        'enrolment': {str(k): v for k, v in monthly_enrol.to_dict().items()},
        'demographic': {str(k): v for k, v in monthly_demo.to_dict().items()},
        'biometric': {str(k): v for k, v in monthly_bio.to_dict().items()}
    }


def calculate_district_statistics(enrol: pd.DataFrame, demo: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate district-level statistics.
    
    Returns:
        Dictionary with top districts
    """
    district_enrol = enrol.groupby(['state', 'district'])['total_enrolment'].sum().sort_values(ascending=False)
    district_demo = demo.groupby(['state', 'district'])['total_demo_update'].sum().sort_values(ascending=False)
    
    return {
        'top_15_districts_enrolment': district_enrol.head(15).to_dict(),
        'top_15_districts_demographic': district_demo.head(15).to_dict()
    }


def calculate_lifecycle_metrics(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate all lifecycle analysis metrics.
    
    Returns:
        Comprehensive dictionary with all metrics
    """
    print("Calculating lifecycle metrics...")
    
    metrics = {
        'volumes': calculate_volume_statistics(enrol, demo, bio),
        'age_distribution': calculate_age_distribution(enrol, demo, bio),
        'weekly_patterns': calculate_weekly_patterns(enrol, demo, bio),
        'state_statistics': calculate_state_statistics(enrol, demo, bio),
        'monthly_trends': calculate_monthly_trends(enrol, demo, bio),
        'district_statistics': calculate_district_statistics(enrol, demo)
    }
    
    # Add update ratios as separate DataFrame
    metrics['update_ratios'] = calculate_update_ratios(enrol, demo, bio)
    
    print("Metrics calculation complete!")
    
    return metrics


def print_key_findings(metrics: Dict[str, Any]) -> None:
    """Print key findings from the analysis."""
    
    print("\n" + "="*70)
    print("KEY FINDINGS - THE AADHAAR LIFECYCLE")
    print("="*70)
    
    age_dist = metrics['age_distribution']
    weekly = metrics['weekly_patterns']
    
    print(f"""
1. BAAL AADHAAR DOMINANCE
   - {age_dist['enrolment']['age_0_5_pct']:.1f}% of new enrolments are children aged 0-5
   - Birth registration linkage with Aadhaar is highly effective

2. SCHOOL-AGE BIOMETRIC UPDATES
   - {age_dist['biometric']['age_5_17_pct']:.1f}% of biometric updates are for ages 5-17
   - Likely driven by scholarship and mid-day meal scheme requirements

3. ADULT DEMOGRAPHIC UPDATES
   - {age_dist['demographic']['age_17_plus_pct']:.1f}% of demographic updates are by adults
   - Life events (address change, marriage) drive update patterns

4. WEEKEND SURGE
   - Saturday shows {100*weekly['weekend_ratio']:.0f}% of weekday demographic update volume
   - Working adults prefer updating on their day off

5. TOTAL VOLUMES
   - Enrolments: {metrics['volumes']['total_enrolment']:,}
   - Demographic Updates: {metrics['volumes']['total_demo_update']:,}
   - Biometric Updates: {metrics['volumes']['total_bio_update']:,}
   - Total Transactions: {metrics['volumes']['total_transactions']:,}
    """)


if __name__ == "__main__":
    from data_loading import load_all_datasets
    
    enrol, demo, bio = load_all_datasets("../data/")
    metrics = calculate_lifecycle_metrics(enrol, demo, bio)
    print_key_findings(metrics)

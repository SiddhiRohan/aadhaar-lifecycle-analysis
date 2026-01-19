"""
Visualization Module
UIDAI Hackathon 2026 - Aadhaar Lifecycle Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
from typing import Optional

warnings.filterwarnings('ignore')

# Style configuration
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Color palette
COLORS = {
    'primary': '#1a5276',
    'secondary': '#3498db',
    'accent1': '#27ae60',
    'accent2': '#e74c3c',
    'accent3': '#f39c12',
    'accent4': '#9b59b6',
    'dark': '#2c3e50'
}


def create_volume_overview(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame, 
                          output_path: str = 'figures/') -> None:
    """Create volume overview figure with pie charts."""
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # Total volumes bar chart
    volumes = {
        'New\nEnrolments': enrol['total_enrolment'].sum() / 1e6,
        'Demographic\nUpdates': demo['total_demo_update'].sum() / 1e6,
        'Biometric\nUpdates': bio['total_bio_update'].sum() / 1e6
    }
    colors_vol = [COLORS['accent1'], COLORS['secondary'], COLORS['accent4']]
    bars = axes[0].bar(volumes.keys(), volumes.values(), color=colors_vol, edgecolor='white', linewidth=2)
    axes[0].set_ylabel('Transactions (Millions)', fontweight='bold')
    axes[0].set_title('Total Activity Volume\n(March - December 2025)', fontweight='bold', pad=15)
    for bar, val in zip(bars, volumes.values()):
        axes[0].annotate(f'{val:.1f}M', xy=(bar.get_x() + bar.get_width()/2, bar.get_height() + 1),
                        ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Enrolment age distribution pie
    enrol_age = {
        'Age 0-5': enrol['age_0_5'].sum(),
        'Age 5-17': enrol['age_5_17'].sum(),
        'Age 18+': enrol['age_18_greater'].sum()
    }
    colors_age = [COLORS['accent2'], COLORS['accent3'], COLORS['accent1']]
    axes[1].pie(enrol_age.values(), labels=enrol_age.keys(), autopct='%1.1f%%', 
                colors=colors_age, explode=(0.05, 0, 0), startangle=90,
                wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    axes[1].set_title('New Enrolments\nby Age Group', fontweight='bold', pad=15)
    
    # Biometric age distribution pie
    bio_age = {
        'Age 5-17': bio['bio_age_5_17'].sum(),
        'Age 17+': bio['bio_age_17_plus'].sum()
    }
    colors_bio = [COLORS['accent3'], COLORS['accent1']]
    axes[2].pie(bio_age.values(), labels=bio_age.keys(), autopct='%1.1f%%',
                colors=colors_bio, explode=(0.05, 0), startangle=90,
                wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    axes[2].set_title('Biometric Updates\nby Age Group', fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(f'{output_path}fig1_volume_overview.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  Created: fig1_volume_overview.png")


def create_lifecycle_chart(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame,
                          output_path: str = 'figures/') -> None:
    """Create the main Aadhaar Lifecycle visualization."""
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    total_enrol = enrol['total_enrolment'].sum()
    total_demo = demo['total_demo_update'].sum()
    total_bio = bio['total_bio_update'].sum()
    
    x = np.arange(3)
    width = 0.25
    
    enrol_pct = [
        100 * enrol['age_0_5'].sum() / total_enrol,
        100 * enrol['age_5_17'].sum() / total_enrol,
        100 * enrol['age_18_greater'].sum() / total_enrol
    ]
    demo_pct = [0, 100 * demo['demo_age_5_17'].sum() / total_demo, 
                100 * demo['demo_age_17_plus'].sum() / total_demo]
    bio_pct = [0, 100 * bio['bio_age_5_17'].sum() / total_bio,
               100 * bio['bio_age_17_plus'].sum() / total_bio]
    
    bars1 = ax.bar(x - width, enrol_pct, width, label='New Enrolments', 
                   color=COLORS['accent1'], edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x, demo_pct, width, label='Demographic Updates',
                   color=COLORS['secondary'], edgecolor='white', linewidth=1.5)
    bars3 = ax.bar(x + width, bio_pct, width, label='Biometric Updates',
                   color=COLORS['accent4'], edgecolor='white', linewidth=1.5)
    
    ax.set_ylabel('Percentage of Total (%)', fontweight='bold', fontsize=13)
    ax.set_xlabel('Life Stage', fontweight='bold', fontsize=13)
    ax.set_title('The Aadhaar Lifecycle: Activity Distribution Across Age Groups', 
                fontweight='bold', fontsize=16, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(['Birth & Infancy\n(Age 0-5)', 'School Age\n(Age 5-17)', 
                        'Adulthood\n(Age 18+)'], fontsize=12)
    ax.legend(loc='upper right', fontsize=11, frameon=True)
    ax.set_ylim(0, 105)
    ax.grid(axis='y', alpha=0.3)
    
    # Value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.annotate(f'{height:.1f}%',
                           xy=(bar.get_x() + bar.get_width()/2, height + 1),
                           ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_path}fig2_aadhaar_lifecycle.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  Created: fig2_aadhaar_lifecycle.png")


def create_weekly_patterns(enrol: pd.DataFrame, demo: pd.DataFrame,
                          output_path: str = 'figures/') -> None:
    """Create weekly patterns visualization."""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_short = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    dow_enrol = enrol.groupby('day_of_week')['total_enrolment'].sum().reindex(day_order)
    dow_demo = demo.groupby('day_of_week')['total_demo_update'].sum().reindex(day_order)
    
    colors_dow = [COLORS['secondary']]*5 + [COLORS['accent2'], COLORS['accent2']]
    
    # Enrolments
    axes[0].bar(range(7), dow_enrol.values/1e6, color=colors_dow, edgecolor='white', linewidth=1.5)
    axes[0].set_xticks(range(7))
    axes[0].set_xticklabels(day_short)
    axes[0].set_ylabel('Enrolments (Millions)', fontweight='bold')
    axes[0].set_title('New Enrolments by Day of Week', fontweight='bold', pad=15)
    axes[0].axhline(y=dow_enrol.mean()/1e6, color=COLORS['dark'], linestyle='--', linewidth=2)
    axes[0].grid(axis='y', alpha=0.3)
    
    # Demographic updates
    axes[1].bar(range(7), dow_demo.values/1e6, color=colors_dow, edgecolor='white', linewidth=1.5)
    axes[1].set_xticks(range(7))
    axes[1].set_xticklabels(day_short)
    axes[1].set_ylabel('Demographic Updates (Millions)', fontweight='bold')
    axes[1].set_title('Demographic Updates by Day of Week', fontweight='bold', pad=15)
    axes[1].grid(axis='y', alpha=0.3)
    
    # Saturday spike annotation
    axes[1].annotate('Saturday spike!\n172% of weekday avg', 
                    xy=(5, dow_demo.values[5]/1e6), xytext=(3, dow_demo.values[5]/1e6 + 2),
                    fontsize=10, ha='center', fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=COLORS['dark'], lw=2),
                    bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['accent3'], alpha=0.3))
    
    plt.tight_layout()
    plt.savefig(f'{output_path}fig3_weekly_patterns.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  Created: fig3_weekly_patterns.png")


def create_geographic_chart(enrol: pd.DataFrame, output_path: str = 'figures/') -> None:
    """Create geographic distribution visualization."""
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # Top states by enrolment
    state_enrol = enrol.groupby('state')['total_enrolment'].sum().sort_values(ascending=True).tail(15)
    colors_gradient = plt.cm.Blues(np.linspace(0.3, 0.9, 15))
    axes[0].barh(range(15), state_enrol.values/1e3, color=colors_gradient, edgecolor='white')
    axes[0].set_yticks(range(15))
    axes[0].set_yticklabels(state_enrol.index, fontsize=10)
    axes[0].set_xlabel('Enrolments (Thousands)', fontweight='bold')
    axes[0].set_title('Top 15 States by New Enrolments', fontweight='bold', pad=15)
    axes[0].grid(axis='x', alpha=0.3)
    
    # Child enrolment percentage
    child_pct = enrol.groupby('state').apply(
        lambda x: x['age_0_5'].sum() / x['total_enrolment'].sum() * 100
    ).sort_values(ascending=True)
    major_states = enrol.groupby('state')['total_enrolment'].sum()
    major_states = major_states[major_states > 5000].index
    child_pct_major = child_pct[child_pct.index.isin(major_states)].tail(20)
    
    colors_child = plt.cm.RdYlGn(child_pct_major.values/100)
    axes[1].barh(range(len(child_pct_major)), child_pct_major.values, color=colors_child, edgecolor='white')
    axes[1].set_yticks(range(len(child_pct_major)))
    axes[1].set_yticklabels(child_pct_major.index, fontsize=10)
    axes[1].set_xlabel('Child (0-5) Enrolment %', fontweight='bold')
    axes[1].set_title('Child Enrolment Percentage by State', fontweight='bold', pad=15)
    axes[1].axvline(x=65, color=COLORS['accent2'], linestyle='--', linewidth=2, label='National Avg (65%)')
    axes[1].legend(loc='lower right')
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_path}fig4_geographic.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  Created: fig4_geographic.png")


def create_monthly_trends(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame,
                         output_path: str = 'figures/') -> None:
    """Create monthly trends visualization."""
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    monthly_enrol = enrol.groupby('month')['total_enrolment'].sum()
    monthly_demo = demo.groupby('month')['total_demo_update'].sum()
    monthly_bio = bio.groupby('month')['total_bio_update'].sum()
    
    months = [str(m) for m in monthly_enrol.index]
    x = np.arange(len(months))
    
    ax.plot(x, monthly_enrol.values/1e6, 'o-', linewidth=3, markersize=10, 
            label='Enrolments', color=COLORS['accent1'], markeredgecolor='white', markeredgewidth=2)
    ax.plot(x, monthly_demo.values/1e6, 's-', linewidth=3, markersize=10,
            label='Demographic Updates', color=COLORS['secondary'], markeredgecolor='white', markeredgewidth=2)
    ax.plot(x, monthly_bio.values/1e6, '^-', linewidth=3, markersize=10,
            label='Biometric Updates', color=COLORS['accent4'], markeredgecolor='white', markeredgewidth=2)
    
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha='right')
    ax.set_ylabel('Volume (Millions)', fontweight='bold')
    ax.set_xlabel('Month', fontweight='bold')
    ax.set_title('Monthly Activity Trends (2025)', fontweight='bold', pad=15)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_path}fig5_monthly_trends.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  Created: fig5_monthly_trends.png")


def create_all_figures(enrol: pd.DataFrame, demo: pd.DataFrame, bio: pd.DataFrame,
                      output_path: str = 'figures/') -> None:
    """Create all visualization figures."""
    
    print("Creating visualizations...")
    
    create_volume_overview(enrol, demo, bio, output_path)
    create_lifecycle_chart(enrol, demo, bio, output_path)
    create_weekly_patterns(enrol, demo, output_path)
    create_geographic_chart(enrol, output_path)
    create_monthly_trends(enrol, demo, bio, output_path)
    
    print("All visualizations created!")


if __name__ == "__main__":
    from data_loading import load_all_datasets
    
    enrol, demo, bio = load_all_datasets("../data/")
    create_all_figures(enrol, demo, bio, "../figures/")

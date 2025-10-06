"""
Integration Dashboard - Mock Data Generator
Generates sample data for testing and development
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_mock_integration_data(num_records: int = 100) -> pd.DataFrame:
    """
    Generate mock integration data for testing
    
    Args:
        num_records: Number of records to generate
        
    Returns:
        DataFrame with mock integration data
    """
    
    np.random.seed(42)
    random.seed(42)
    
    # Sample data
    dealer_names = [
        'AutoMax', 'Premier Motors', 'Elite Auto', 'DriveTime', 'CarHub',
        'Velocity Motors', 'Apex Auto', 'Summit Cars', 'Horizon Motors', 'Peak Auto',
        'Metro Motors', 'City Auto', 'Urban Cars', 'Downtown Motors', 'Central Auto',
        'Coastal Motors', 'Riverside Auto', 'Lakeside Cars', 'Bayview Motors', 'Seaside Auto'
    ]
    
    regions = ['NAM', 'EMEA', 'APAC', 'LATAM']
    implementation_types = ['Conquest', 'Buy/Sell', 'New Point']
    vendor_list_updated = ['Yes', 'No', '']
    
    pems = ['John Smith', 'Sarah Johnson', 'Mike Williams', 'Emily Brown', 'David Jones',
            'Lisa Garcia', 'Robert Miller', 'Jennifer Davis', 'Michael Rodriguez', 'Jessica Martinez']
    
    directors = ['Tom Anderson', 'Mary Taylor', 'James Thomas', 'Patricia Jackson', 'Christopher White',
                 'Linda Harris', 'Daniel Martin', 'Barbara Thompson', 'Matthew Garcia', 'Susan Martinez']
    
    assignees = ['Alex Chen', 'Maria Lopez', 'Kevin Park', 'Rachel Kim', 'Brian Lee',
                 'Amanda Wang', 'Justin Nguyen', 'Nicole Patel', 'Ryan Singh', 'Lauren Kumar']
    
    # Generate data
    data = []
    today = datetime.now()
    
    for i in range(num_records):
        # Generate go live date (spread across past, current, and future months)
        days_offset = random.randint(-60, 120)  # -60 to +120 days from today
        go_live_date = today + timedelta(days=days_offset)
        
        # Select implementation type
        impl_type = random.choice(implementation_types)
        
        # Vendor list updated (bias towards 'No' for more interesting data)
        vendor_updated = random.choices(
            vendor_list_updated,
            weights=[0.3, 0.6, 0.1],  # 30% Yes, 60% No, 10% blank
            k=1
        )[0]
        
        # Randomly make some fields blank for Data Incomplete testing
        is_incomplete = random.random() < 0.1  # 10% chance of incomplete data
        
        record = {
            'Dealer Name': random.choice(dealer_names),
            'Dealer ID': f'DLR{1000 + i}',
            'Go Live Date': go_live_date.strftime('%Y-%m-%d'),
            'Implementation Type': impl_type if not is_incomplete else '',
            'Vendor List Updated': vendor_updated,
            'PEM': random.choice(pems) if not is_incomplete else '',
            'Director': random.choice(directors),
            'Assigned to': random.choice(assignees) if not is_incomplete else '',
            'Region': random.choice(regions)
        }
        
        data.append(record)
    
    df = pd.DataFrame(data)
    
    print(f"[DEBUG Integration] Generated {len(df)} mock records")
    print(f"[DEBUG Integration] Columns: {df.columns.tolist()}")
    print(f"[DEBUG Integration] Date range: {df['Go Live Date'].min()} to {df['Go Live Date'].max()}")
    
    return df


def load_integration_data() -> pd.DataFrame:
    """
    Load integration data from source (mock or SharePoint)
    
    Returns:
        DataFrame with integration data
    """
    
    from integration_dashboard.config.settings import USE_MOCK_DATA
    
    if USE_MOCK_DATA:
        print("[DEBUG Integration] Loading mock data...")
        return generate_mock_integration_data()
    else:
        # TODO: Implement SharePoint data loading
        print("[DEBUG Integration] SharePoint loading not yet implemented, using mock data")
        return generate_mock_integration_data()


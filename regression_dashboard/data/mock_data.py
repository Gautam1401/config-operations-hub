"""
Regression Testing Dashboard - Mock Data Generator
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_mock_data(num_rows: int = 50) -> pd.DataFrame:
    """
    Generate mock data for Regression Testing dashboard
    
    Args:
        num_rows: Number of rows to generate
        
    Returns:
        pd.DataFrame: Mock data
    """
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Sample data
    dealership_names = [
        "ABC Motors", "XYZ Auto", "Premium Cars", "Elite Dealership",
        "Metro Motors", "City Auto", "Highway Cars", "Downtown Motors",
        "Suburban Auto", "Coastal Cars", "Mountain Motors", "Valley Auto",
        "Riverside Dealership", "Lakeside Motors", "Parkway Cars",
        "Central Auto", "North Motors", "South Dealership", "East Cars",
        "West Auto", "Platinum Motors", "Gold Dealership", "Silver Cars"
    ]
    
    regions = ['NAM', 'EMEA', 'APAC', 'LATAM']
    
    implementation_types = ['Conquest', 'Buy/Sell', 'Enterprise', 'New Point']
    
    testing_statuses = ['Completed', 'WIP', 'Unable to Complete', None, '']
    
    assignees = [
        'John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams',
        'Charlie Brown', 'Diana Prince', 'Eve Davis', 'Frank Miller',
        'Grace Lee', 'Henry Wilson', 'Ivy Chen', 'Jack Taylor'
    ]
    
    # Generate data
    data = []
    today = datetime.now()
    
    for i in range(num_rows):
        # Generate Go Live Date (spread across past, current, and future months)
        days_offset = random.randint(-90, 90)  # -90 to +90 days from today
        go_live_date = today + timedelta(days=days_offset)
        
        # Generate SIM Start Date (usually before Go Live Date)
        sim_days_before = random.randint(7, 30)  # 7-30 days before Go Live
        sim_start_date = go_live_date - timedelta(days=sim_days_before)
        
        # Determine status based on SIM Start Date
        if sim_start_date < today:
            # Past SIM Start Date
            if random.random() < 0.7:  # 70% have status
                status = random.choice(['Completed', 'WIP', 'Unable to Complete'])
            else:  # 30% are blank (Data Incomplete)
                status = random.choice([None, ''])
        else:
            # Future SIM Start Date
            if random.random() < 0.3:  # 30% have status
                status = random.choice(['Completed', 'WIP'])
            else:  # 70% are blank
                status = random.choice([None, ''])
        
        # Generate dealer ID
        dealer_id = f"{10000 + i}"
        
        row = {
            'Dealership Name': f"{random.choice(dealership_names)} - {dealer_id}",
            'Go-Live Date': go_live_date,
            'SIM Start Date': sim_start_date,
            'Assignee': random.choice(assignees),
            'Region': random.choice(regions),
            'Testing Status': status,
            'Type of Implementation': random.choice(implementation_types)
        }
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Convert date columns to datetime
    df['Go-Live Date'] = pd.to_datetime(df['Go-Live Date'])
    df['SIM Start Date'] = pd.to_datetime(df['SIM Start Date'])
    
    print(f"[DEBUG Mock Data] Generated {len(df)} rows")
    print(f"[DEBUG Mock Data] Columns: {df.columns.tolist()}")
    print(f"[DEBUG Mock Data] Date range: {df['Go-Live Date'].min()} to {df['Go-Live Date'].max()}")
    print(f"[DEBUG Mock Data] Status distribution:\n{df['Testing Status'].value_counts(dropna=False)}")
    
    return df


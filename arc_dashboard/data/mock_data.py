"""
Mock Data Generator for ARC Dashboard
Generates realistic sample data for testing without SharePoint connection
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_mock_data(num_rows=100):
    """
    Generate mock ARC configuration data
    
    Args:
        num_rows (int): Number of records to generate
        
    Returns:
        pd.DataFrame: Mock data with all required columns
    """
    
    # Sample data pools
    dealerships = [
        'Downtown Toyota', 'Westside Honda', 'Eastside Ford', 'Northgate Chevrolet',
        'Southside Nissan', 'Central BMW', 'Riverside Mercedes', 'Lakeside Audi',
        'Hillside Lexus', 'Valley Hyundai', 'Metro Kia', 'Coastal Mazda',
        'Mountain Subaru', 'Desert Volkswagen', 'Prairie Jeep', 'Summit Dodge',
        'Harbor Chrysler', 'Garden Buick', 'Forest GMC', 'Ocean Cadillac',
        'Sunset Acura', 'Sunrise Infiniti', 'Midtown Volvo', 'Uptown Porsche',
        'Parkway Land Rover', 'Boulevard Jaguar', 'Avenue Tesla', 'Street Alfa Romeo',
        'Plaza Maserati', 'Square Bentley', 'Circle Rolls-Royce', 'Triangle Ferrari',
        'Diamond Lamborghini', 'Pearl McLaren', 'Ruby Aston Martin', 'Emerald Lotus',
        'Sapphire Bugatti', 'Topaz Pagani', 'Amber Koenigsegg', 'Jade Genesis',
    ]
    
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    
    lobs = ['Service', 'Parts', 'Accounting']
    
    statuses = ['Completed', 'WIP', 'Not Configured']
    
    implementation_types = ['New Implementation', 'Migration', 'Upgrade', 'Expansion']
    
    team_members = [
        'John Smith', 'Sarah Johnson', 'Michael Brown', 'Emily Davis',
        'David Wilson', 'Jessica Martinez', 'James Anderson', 'Jennifer Taylor',
        'Robert Thomas', 'Linda Jackson', 'William White', 'Mary Harris',
        'Richard Martin', 'Patricia Thompson', 'Charles Garcia', 'Barbara Rodriguez',
    ]
    
    # Generate data
    data = []
    
    # Get current date
    today = datetime.now()
    
    for i in range(num_rows):
        # Generate go-live date (mix of past, current month, next month, and future)
        days_offset = random.randint(-60, 90)
        go_live_date = today + timedelta(days=days_offset)
        
        # Select random values
        dealership = random.choice(dealerships)
        region = random.choice(regions)
        lob = random.choice(lobs)
        implementation_type = random.choice(implementation_types)
        assigned_to = random.choice(team_members)
        
        # Status distribution (weighted towards Completed and WIP)
        status = random.choices(
            statuses,
            weights=[0.5, 0.35, 0.15],  # 50% Completed, 35% WIP, 15% Not Configured
            k=1
        )[0]
        
        # Create record
        record = {
            'Dealership Name': f"{dealership} - {lob}",
            'Go Live Date': go_live_date.strftime('%Y-%m-%d'),
            'Type of Implementation': implementation_type,
            'Assigned To': assigned_to,
            'Region': region,
            'Line of Business': lob,
            'Status': status,
        }
        
        data.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Sort by Go Live Date
    df = df.sort_values('Go Live Date').reset_index(drop=True)
    
    return df


def get_sample_data():
    """
    Quick function to get sample data
    
    Returns:
        pd.DataFrame: Sample data
    """
    return generate_mock_data(100)


if __name__ == '__main__':
    # Test the mock data generator
    df = generate_mock_data(20)
    print("Mock Data Sample:")
    print(df.head(10))
    print(f"\nTotal Records: {len(df)}")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nStatus Distribution:\n{df['Status'].value_counts()}")
    print(f"\nLOB Distribution:\n{df['Line of Business'].value_counts()}")
    print(f"\nRegion Distribution:\n{df['Region'].value_counts()}")


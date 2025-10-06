"""
CRM Configuration Dashboard - Mock Data Generator
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, Any

from crm_dashboard.config.settings import (
    REGIONS,
    IMPLEMENTATION_TYPES,
    CONFIGURATION_STATUS,
    PRE_GO_LIVE_STATUS,
    GO_LIVE_TESTING_STATUS,
    MOCK_DATA_ROWS
)


def generate_mock_crm_data(num_rows: int = MOCK_DATA_ROWS) -> pd.DataFrame:
    """
    Generate mock CRM configuration data
    
    Args:
        num_rows: Number of rows to generate
        
    Returns:
        pd.DataFrame: Mock CRM data
    """
    
    data = []
    
    # Sample dealer names
    dealer_prefixes = ['AutoNation', 'Lithia', 'Penske', 'Group 1', 'Sonic', 
                       'Asbury', 'Hendrick', 'CarMax', 'Carvana', 'Vroom']
    dealer_suffixes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 
                       'Mercedes', 'Nissan', 'Hyundai', 'Kia', 'Mazda']
    
    # Sample assignees
    assignees = ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Emily Brown', 
                 'David Wilson', 'Lisa Anderson', 'Tom Martinez', 'Jennifer Lee',
                 'Robert Taylor', 'Maria Garcia']
    
    # Generate data
    for i in range(num_rows):
        dealer_name = f"{random.choice(dealer_prefixes)} {random.choice(dealer_suffixes)}"
        dealer_id = f"D{1000 + i}"
        
        # Random go-live date (past, current, future)
        days_offset = random.randint(-60, 90)
        go_live_date = datetime.now() + timedelta(days=days_offset)
        
        region = random.choice(REGIONS)
        impl_type = random.choice(IMPLEMENTATION_TYPES)
        
        # Go Live Status (for Data Incorrect logic)
        go_live_status = random.choice(['Pending', 'In Progress', 'Rolled out'])
        
        # Configuration data
        config_type = random.choice(['Standard', 'Copy', 'Implementation', None])
        config_assignee = random.choice(assignees) if config_type else None
        
        # Pre Go Live data
        domain_updated = random.choice(['Yes', 'No', None])
        setup_check = random.choice(['Yes', 'No', None])
        pre_go_live_assignee = random.choice(assignees) if domain_updated or setup_check else None
        
        # Go Live Testing data
        sample_adf = random.choice(['Yes', 'No Issues', 'Issues Found', None])
        inbound_email = random.choice(['Yes', 'No Issues', 'Issues Found', None])
        outbound_email = random.choice(['Yes', 'No Issues', 'Issues Found', None])
        data_migration = random.choice(['Yes', 'No Issues', 'Issues Found', None])
        go_live_testing_assignee = random.choice(assignees) if any([sample_adf, inbound_email, outbound_email, data_migration]) else None
        
        row = {
            'Dealer Name': dealer_name,
            'Dealer ID': dealer_id,
            'Go Live Date': go_live_date,
            'Implementation Type': impl_type,
            'Region': region,
            'Go Live Status': go_live_status,
            
            # Configuration
            'Configuration Type': config_type,
            'Configuration Assignee': config_assignee,
            
            # Pre Go Live
            'Domain Updated': domain_updated,
            'Set Up Check': setup_check,
            'Pre Go Live Assignee': pre_go_live_assignee,
            
            # Go Live Testing
            'Sample ADF': sample_adf,
            'Inbound Email': inbound_email,
            'Outbound Email': outbound_email,
            'Data Migration': data_migration,
            'Go Live Testing Assignee': go_live_testing_assignee,
        }
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    print(f"[DEBUG] Generated {len(df)} mock CRM records")
    print(f"[DEBUG] Columns: {df.columns.tolist()}")
    
    return df


def load_crm_data() -> pd.DataFrame:
    """
    Load CRM data from Excel file or mock data

    Returns:
        pd.DataFrame: CRM configuration data
    """
    from crm_dashboard.config.settings import USE_MOCK_DATA
    from crm_dashboard.data.excel_loader import load_crm_data_from_excel

    if USE_MOCK_DATA:
        print("[DEBUG] Loading mock CRM data...")
        return generate_mock_crm_data()
    else:
        # Load from Excel file
        try:
            print("[INFO] Loading CRM data from Excel file...")
            return load_crm_data_from_excel()
        except Exception as e:
            print(f"[ERROR] Failed to load Excel file: {e}")
            print("[INFO] Using mock data instead.")
            return generate_mock_crm_data()


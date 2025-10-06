"""
Excel Data Loader for ARC Dashboard
Loads data from local Excel file and transforms to long format
"""

import pandas as pd
import os
from pathlib import Path


def load_arc_data_from_excel():
    """
    Load ARC Configuration data from Excel file
    ONE ROW PER DEALERSHIP (wide format)

    Returns:
        pd.DataFrame: ARC configuration data with columns:
                     - Dealership Name
                     - Go Live Date
                     - Days to Go Live
                     - Type of Implementation
                     - Assigned To
                     - Region
                     - Parts Status
                     - Service Status
                     - Accounting Status
    """
    from datetime import datetime

    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    excel_path = project_root / "data" / "ARC Configuration.xlsx"

    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Read all sheets and combine them
    xl = pd.ExcelFile(excel_path)
    all_data = []

    for sheet_name in xl.sheet_names:
        df_sheet = pd.read_excel(excel_path, sheet_name=sheet_name)
        all_data.append(df_sheet)

    # Combine all sheets
    df = pd.concat(all_data, ignore_index=True)

    # Standardize column names
    df.columns = df.columns.str.strip()

    # Column mapping
    column_mapping = {
        'Dealership': 'Dealership Name',
        'Assignee': 'Assigned To',
        'Go Live Date': 'Go Live Date',
        'Type of Implementation': 'Type of Implementation',
        'Region': 'Region',
        'Parts': 'Parts Status',
        'Service': 'Service Status',
        'Accounting': 'Accounting Status'
    }

    # Rename columns
    df.rename(columns=column_mapping, inplace=True)

    # Convert Go Live Date to datetime
    df['Go Live Date'] = pd.to_datetime(df['Go Live Date'], errors='coerce')

    # Calculate Days to Go Live
    today = pd.Timestamp(datetime.now().date())
    df['Days to Go Live'] = (df['Go Live Date'] - today).dt.days

    # Determine if Rolled Out (Days to Go Live < 0)
    df['Is Rolled Out'] = df['Days to Go Live'] < 0

    # ========================================================================
    # MODULE STATUS LOGIC
    # ========================================================================
    # For each module (Parts, Service, Accounting):
    # - If blank AND Rolled Out → "Not Configured"
    # - If blank AND NOT Rolled Out → Keep blank (None - don't count)
    # - If not blank → Standardize value (Completed/WIP/Not Configured)

    def process_module_status(status, is_rolled_out):
        """Process module status based on blank and rolled out logic"""
        # Convert to string and clean
        status_str = str(status).strip() if pd.notna(status) else ''

        # If blank
        if status_str == '' or status_str.lower() in ['nan', 'none', 'n/a', 'na']:
            if is_rolled_out:
                return 'Not Configured'
            else:
                return None  # Don't count

        # Standardize status values (case-insensitive)
        status_lower = status_str.lower()
        if status_lower in ['completed', 'complete', 'done']:
            return 'Completed'
        elif status_lower in ['wip', 'in progress', 'work in progress']:
            return 'WIP'
        elif status_lower in ['not configured', 'not started', 'pending']:
            return 'Not Configured'
        else:
            return status_str  # Keep original if unknown

    # Apply module status logic to each module column
    df['Parts Status'] = df.apply(lambda row: process_module_status(row['Parts Status'], row['Is Rolled Out']), axis=1)
    df['Service Status'] = df.apply(lambda row: process_module_status(row['Service Status'], row['Is Rolled Out']), axis=1)
    df['Accounting Status'] = df.apply(lambda row: process_module_status(row['Accounting Status'], row['Is Rolled Out']), axis=1)

    # ========================================================================
    # DATA STANDARDIZATION - Clean up other fields
    # ========================================================================

    # Clean up Region values
    df['Region'] = df['Region'].fillna('Unknown')
    df['Region'] = df['Region'].astype(str).str.strip()

    # Standardize region values (case-insensitive)
    region_mapping = {
        'canada': 'Canada',
        'canda': 'Canada',  # Fix typo
        'can': 'Canada',
        'usa east': 'USA East',
        'east': 'USA East',
        'usa west': 'USA West',
        'west': 'USA West',
        'usa west and central': 'USA West and Central',
        'west and central': 'USA West and Central',
        'mid market': 'Mid Market',
        'midmarket': 'Mid Market',
        'enterprise': 'Enterprise',
        'ent': 'Enterprise',
        'united kingdom': 'United Kingdom',
        'uk': 'United Kingdom',
        'unknown': 'Unknown',
        'nan': 'Unknown',
        'none': 'Unknown',
        '': 'Unknown'
    }

    df['Region'] = df['Region'].str.lower().replace(region_mapping)

    # Clean up Type of Implementation
    df['Type of Implementation'] = df['Type of Implementation'].fillna('Unknown')
    df['Type of Implementation'] = df['Type of Implementation'].astype(str).str.strip()

    impl_type_mapping = {
        'new point': 'New Point',
        'conquest': 'Conquest',
        'buy/sell': 'Buy/Sell',
        'buy-sell': 'Buy/Sell',
        'buysell': 'Buy/Sell',
        'enterprise': 'Enterprise',
        'migration': 'Migration',
        'upgrade': 'Upgrade'
    }

    df['Type of Implementation'] = df['Type of Implementation'].str.lower().replace(impl_type_mapping)

    # Clean up Dealership Name and Assigned To
    df['Dealership Name'] = df['Dealership Name'].fillna('Unknown')
    df['Dealership Name'] = df['Dealership Name'].astype(str).str.strip()
    df['Assigned To'] = df['Assigned To'].fillna('Unassigned')
    df['Assigned To'] = df['Assigned To'].astype(str).str.strip()

    # Keep only necessary columns
    final_columns = [
        'Dealership Name',
        'Go Live Date',
        'Days to Go Live',
        'Type of Implementation',
        'Assigned To',
        'Region',
        'Parts Status',
        'Service Status',
        'Accounting Status',
        'Is Rolled Out'
    ]

    df = df[final_columns]

    print(f"[DEBUG ARC Loader] Loaded {len(df)} dealerships from {len(xl.sheet_names)} sheets")
    print(f"[DEBUG ARC Loader] ONE ROW PER DEALERSHIP (wide format)")
    print(f"[DEBUG ARC Loader] Columns: {df.columns.tolist()}")
    print(f"[DEBUG ARC Loader] Unique Regions: {df['Region'].unique().tolist()}")
    print(f"[DEBUG ARC Loader] Sample data:")
    print(df[['Dealership Name', 'Parts Status', 'Service Status', 'Accounting Status', 'Is Rolled Out']].head(5))

    return df


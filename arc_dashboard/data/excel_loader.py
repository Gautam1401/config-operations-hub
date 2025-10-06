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
    Combines all month sheets and transforms to long format (one row per module)

    Returns:
        pd.DataFrame: ARC configuration data in long format with columns:
                     - Dealership Name
                     - Go Live Date
                     - Type of Implementation
                     - Assigned To
                     - Region
                     - Module (Parts/Service/Accounting)
                     - Status (Completed/WIP/Not Configured)
    """
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

    # Keep only necessary columns
    base_columns = ['Dealership', 'Go Live Date', 'Type of Implementation', 'Assignee', 'Region']
    module_columns = ['Parts', 'Service', 'Accounting']

    # Create long format - one row per module
    long_format_data = []

    for _, row in df.iterrows():
        # Base information for this dealership
        base_info = {
            'Dealership Name': row.get('Dealership', ''),
            'Go Live Date': row.get('Go Live Date', ''),
            'Type of Implementation': row.get('Type of Implementation', ''),
            'Assigned To': row.get('Assignee', ''),
            'Region': row.get('Region', '')
        }

        # Create 3 rows - one for each module
        for module in module_columns:
            module_row = base_info.copy()
            module_row['Module'] = module
            module_row['Status'] = row.get(module, 'Not Configured')
            long_format_data.append(module_row)

    # Create final dataframe
    df_long = pd.DataFrame(long_format_data)

    # Clean up Status values
    df_long['Status'] = df_long['Status'].fillna('Not Configured')
    df_long['Status'] = df_long['Status'].astype(str).str.strip()

    # Standardize status values
    status_mapping = {
        'Completed': 'Completed',
        'Complete': 'Completed',
        'Done': 'Completed',
        'WIP': 'WIP',
        'In Progress': 'WIP',
        'Not Configured': 'Not Configured',
        'Not Started': 'Not Configured',
        'NA': 'Not Configured',
        'N/A': 'Not Configured',
        '': 'Not Configured'
    }

    df_long['Status'] = df_long['Status'].replace(status_mapping)

    print(f"[DEBUG ARC Loader] Loaded {len(df)} dealerships from {len(xl.sheet_names)} sheets")
    print(f"[DEBUG ARC Loader] Transformed to {len(df_long)} rows (long format)")
    print(f"[DEBUG ARC Loader] Columns: {df_long.columns.tolist()}")

    return df_long


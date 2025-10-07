"""
Excel Data Loader for Integration Dashboard
Loads data from local Excel file
"""

import pandas as pd
import os
from pathlib import Path


def load_integration_data_from_excel():
    """
    Load Integration data from Excel file

    Returns:
        pd.DataFrame: Integration access board data with standardized columns
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    excel_path = project_root / "data" / "Integration Access Board.xlsx"

    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Read the Excel file - try first sheet
    df = pd.read_excel(excel_path, sheet_name=0)

    # Standardize column names - strip trailing/leading spaces
    df.columns = df.columns.str.strip()

    print(f"[DEBUG Integration Loader] Loaded {len(df)} rows")
    print(f"[DEBUG Integration Loader] Columns after strip: {df.columns.tolist()}")

    # Map to expected column names
    column_mapping = {
        'Assigned to': 'Assigned To',
        'OEM Tasks Completed': 'OEM Tasks Completed',
        'Integration to Be Launched': 'Integration to Be Launched',
        'Comments': 'Comments'
    }

    df.rename(columns=column_mapping, inplace=True)

    print(f"[DEBUG Integration Loader] Columns after mapping: {df.columns.tolist()}")

    # Keep 'Dealer Name' and 'Dealer ID' for the data processor to combine later

    # Standardize text values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
            # Replace 'nan' string with actual NaN
            df[col] = df[col].replace(['nan', 'NaN', 'None', ''], pd.NA)

    # Standardize Region - Capitalize first letter
    if 'Region' in df.columns:
        # Capitalize first letter of each word
        df['Region'] = df['Region'].str.title()

        # Handle specific region mappings
        region_mapping = {
            'Usa East': 'USA East',
            'Usa West': 'USA West',
            'Usa West And Central': 'USA West and Central',
            'Mid Market': 'Mid Market',
            'Enterprise': 'Enterprise',
            'Canada': 'Canada',
        }
        df['Region'] = df['Region'].replace(region_mapping)

    return df


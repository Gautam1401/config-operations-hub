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

    # Standardize column names
    df.columns = df.columns.str.strip()

    print(f"[DEBUG Integration Loader] Loaded {len(df)} rows")
    print(f"[DEBUG Integration Loader] Columns: {df.columns.tolist()}")

    # Map to expected column names
    column_mapping = {
        'Dealer Name': 'Dealership Name',
        'Dealer ID': 'Dealer ID',
        'Go Live Date': 'Go Live Date',
        'Days to Go Live': 'Days to Go Live',
        'PEM': 'PEM',
        'Director': 'Director',
        'Type of Implementation': 'Type of Implementation',
        'Region': 'Region',
        'Assigned to': 'Assigned To',
        'Vendor List Updated': 'Vendor List Updated'
    }

    df.rename(columns=column_mapping, inplace=True)

    # Standardize text values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()

    # Standardize Region
    region_mapping = {
        'nam': 'NAM',
        'north america': 'NAM',
        'emea': 'EMEA',
        'europe': 'EMEA',
        'apac': 'APAC',
        'asia pacific': 'APAC',
        'latam': 'LATAM',
        'latin america': 'LATAM'
    }

    if 'Region' in df.columns:
        df['Region'] = df['Region'].str.lower().replace(region_mapping)

    return df


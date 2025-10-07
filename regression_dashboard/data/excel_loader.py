"""
Excel Data Loader for Regression Testing Dashboard
Loads data from local Excel file
"""

import pandas as pd
import os
from pathlib import Path
from shared.data_paths import get_excel_file_path, REGRESSION_FILE


def load_regression_data_from_excel():
    """
    Load Regression Testing data from Excel file

    Returns:
        pd.DataFrame: Regression testing data with standardized columns
    """
    # Get path from centralized config
    excel_path = get_excel_file_path(REGRESSION_FILE)

    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Read the Excel file - use "Stores Checklist" sheet
    df = pd.read_excel(excel_path, sheet_name="Stores Checklist")

    # Standardize column names
    df.columns = df.columns.str.strip()

    print(f"[DEBUG Regression Loader] Loaded {len(df)} rows")
    print(f"[DEBUG Regression Loader] Columns: {df.columns.tolist()}")

    # Don't rename columns - data processor handles column mapping
    # Just keep original column names from Excel

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


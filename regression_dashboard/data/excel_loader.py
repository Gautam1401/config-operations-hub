"""
Excel Data Loader for Regression Testing Dashboard
Loads data from local Excel file
"""

import pandas as pd
import os
from pathlib import Path


def load_regression_data_from_excel():
    """
    Load Regression Testing data from Excel file

    Returns:
        pd.DataFrame: Regression testing data with standardized columns
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    excel_path = project_root / "data" / "E2E Testing Check.xlsx"

    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Read the Excel file - use "Stores Checklist" sheet
    df = pd.read_excel(excel_path, sheet_name="Stores Checklist")

    # Standardize column names
    df.columns = df.columns.str.strip()

    print(f"[DEBUG Regression Loader] Loaded {len(df)} rows")
    print(f"[DEBUG Regression Loader] Columns: {df.columns.tolist()}")

    # Map to expected column names
    column_mapping = {
        'Dealership Name': 'Dealership Name',
        'Go-Live Date': 'Go Live Date',
        'Region': 'Region',
        'Type of Implementation': 'Type of Implementation',
        'SIM Start Date': 'SIM Start Date',
        'Assignee': 'Assigned To',
        'Testing Status': 'Status'
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


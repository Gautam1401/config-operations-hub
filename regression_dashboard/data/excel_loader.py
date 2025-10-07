"""
Excel Data Loader for Regression Testing Dashboard
Loads data from local Excel file - ONLY "Stores Checklist" sheet
"""

import pandas as pd
from datetime import datetime
from shared.data_paths import get_excel_file_path, REGRESSION_FILE


def load_regression_data_from_excel():
    """
    Load Regression Testing data from Excel file
    Uses ONLY the "Stores Checklist" sheet

    Column Mapping:
    - Dealership Name → Dealership Name
    - Go Live Date → Go Live Date
    - Days to Go Live → Calculated (Go Live Date - Today, if <0 then "Rolled Out")
    - Region → Region (with "ALL" option)
    - Implementation Type → Implementation Type
    - Assignee → Assignee
    - Testing Status → Status

    Returns:
        pd.DataFrame: Regression testing data with standardized column names
    """
    # Get path from centralized config
    excel_path = get_excel_file_path(REGRESSION_FILE)

    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Read ONLY the "Stores Checklist" sheet
    sheet_name = 'Stores Checklist'
    
    xl = pd.ExcelFile(excel_path)
    
    if sheet_name not in xl.sheet_names:
        raise ValueError(f"Sheet '{sheet_name}' not found in {excel_path}. Available sheets: {xl.sheet_names}")

    print(f"[INFO Regression Loader] Reading sheet: '{sheet_name}'")
    
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    print(f"[INFO Regression Loader] Loaded {len(df)} rows")

    # Standardize column names - strip whitespace
    df.columns = df.columns.str.strip()

    # Column mapping as per requirements
    column_mapping = {
        'Testing Status': 'Status'
    }

    # Columns to keep (including those that don't need renaming)
    columns_to_keep = [
        'Dealership Name',
        'Go Live Date',
        'Region',
        'Implementation Type',
        'Assignee',
        'Testing Status'
    ]

    # Only keep columns that exist
    existing_cols = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_cols]
    
    # Rename columns
    df.rename(columns=column_mapping, inplace=True)

    print(f"[INFO Regression Loader] Columns after mapping: {df.columns.tolist()}")

    # Standardize values (trim spaces)
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()

    # Convert Go Live Date to datetime
    if 'Go Live Date' in df.columns:
        df['Go Live Date'] = pd.to_datetime(df['Go Live Date'], errors='coerce')

    # Calculate Days to Go Live
    today = datetime.now()
    if 'Go Live Date' in df.columns:
        df['Days to Go Live'] = (df['Go Live Date'] - today).dt.days
        # If Days to Go Live < 0, mark as "Rolled Out"
        df['Days to Go Live Display'] = df['Days to Go Live'].apply(
            lambda x: 'Rolled Out' if pd.notna(x) and x < 0 else (str(int(x)) if pd.notna(x) else '')
        )

    # Handle NA/blank values - replace with pd.NA
    na_values = ['nan', 'NA', 'N/A', 'na', 'n/a', '', 'None']
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].replace(na_values, pd.NA)

    print(f"[INFO Regression Loader] Final data shape: {df.shape}")

    return df

"""
Excel Data Loader for ARC Dashboard
Loads data from local Excel file and combines all month sheets
"""

import pandas as pd
from datetime import datetime
from shared.data_paths import get_excel_file_path, ARC_FILE


def load_arc_data_from_excel():
    """
    Load ARC Configuration data from Excel file
    Combines all month sheets into one dataset

    Column Mapping:
    - Assignee → Assigned To
    - Go Live Date → Go Live Date
    - Implementation Type → Implementation Type
    - Dealership Name → Dealership Name
    - Region → Region (with "ALL" option)
    - Parts - Status → Parts Status
    - Service - Status → Service Status
    - Accounting - Status → Accounting Status

    Returns:
        pd.DataFrame: ARC configuration data with standardized column names
    """
    # Get path from centralized config
    excel_path = get_excel_file_path(ARC_FILE)

    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Read all sheets and combine them
    xl = pd.ExcelFile(excel_path)
    all_data = []

    print(f"[INFO ARC Loader] Found sheets: {xl.sheet_names}")

    for sheet_name in xl.sheet_names:
        df_sheet = pd.read_excel(excel_path, sheet_name=sheet_name)
        print(f"[INFO ARC Loader] Sheet '{sheet_name}': {len(df_sheet)} rows")
        all_data.append(df_sheet)

    # Combine all sheets
    df = pd.concat(all_data, ignore_index=True)

    # Standardize column names - strip whitespace
    df.columns = df.columns.str.strip()

    print(f"[INFO ARC Loader] Combined data: {len(df)} rows")

    # Column mapping as per requirements
    column_mapping = {
        'Assignee': 'Assigned To',
        'Parts - Status': 'Parts Status',
        'Service - Status': 'Service Status',
        'Accounting - Status': 'Accounting Status'
    }

    # Columns to keep (including those that don't need renaming)
    columns_to_keep = [
        'Assignee',
        'Go Live Date',
        'Implementation Type',
        'Dealership Name',
        'Region',
        'Parts - Status',
        'Service - Status',
        'Accounting - Status'
    ]

    # Only keep columns that exist
    existing_cols = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_cols]
    
    # Rename columns
    df.rename(columns=column_mapping, inplace=True)

    print(f"[INFO ARC Loader] Columns after mapping: {df.columns.tolist()}")

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

    print(f"[INFO ARC Loader] Final data shape: {df.shape}")

    return df

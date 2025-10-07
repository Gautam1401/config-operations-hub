"""
Excel Data Loader for CRM Dashboard
Loads data from local Excel file and combines all month sheets
"""

import pandas as pd
from datetime import datetime
from shared.data_paths import get_excel_file_path, CRM_FILE


def load_crm_data_from_excel():
    """
    Load CRM Configuration data from Excel file
    Combines all month sheets into one dataset

    Column Mapping:
    - Dealership Name → Dealership Name
    - Implementation Type → Implementation Type
    - Region → Region (with "ALL" option)
    - Go Live Date → Go Live Date
    - Days to Go Live → Calculated (Go Live Date - Today, if <0 then "Rolled Out")
    - Configuration - Assigned → Configuration Assignee
    - Configuration - Status → Configuration Status
    - Pre Go Live - Assigned to → Pre Go Live Assignee
    - Pre Go Live - Domain Updated → Pre Go Live Domain Updated
    - Pre Go Live - Set Up Check → Pre Go Live Set Up Check
    - Go Live Testing - Assigned To → Go Live Testing Assignee
    - Go Live Testing - Sample ADF → Sample ADF
    - Go Live Testing - Inbound Email Test → Inbound Email
    - Go Live Testing - Outbound Mail Test → Outbound Email
    - Go Live Testing - Data Migration Test → Data Migration

    Returns:
        pd.DataFrame: CRM configuration data with standardized column names
    """
    # Get path from centralized config
    excel_path = get_excel_file_path(CRM_FILE)

    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Read all sheets and combine them
    xl = pd.ExcelFile(excel_path)
    all_data = []

    print(f"[INFO CRM Loader] Found sheets: {xl.sheet_names}")

    for sheet_name in xl.sheet_names:
        df_sheet = pd.read_excel(excel_path, sheet_name=sheet_name)
        print(f"[INFO CRM Loader] Sheet '{sheet_name}': {len(df_sheet)} rows")
        all_data.append(df_sheet)

    # Combine all sheets
    df = pd.concat(all_data, ignore_index=True)

    # Standardize column names - strip whitespace
    df.columns = df.columns.str.strip()

    print(f"[INFO CRM Loader] Combined data: {len(df)} rows")

    # Column mapping as per requirements - keep original names that don't need mapping
    column_mapping = {
        'Configuration - Assigned': 'Configuration Assignee',
        'Configuration - Status': 'Configuration Status',
        'Pre Go Live - Assigned to': 'Pre Go Live Assignee',
        'Pre Go Live - Domain Updated': 'Pre Go Live Domain Updated',
        'Pre Go Live - Set Up Check': 'Pre Go Live Set Up Check',
        'Go Live Testing - Assigned To': 'Go Live Testing Assignee',
        'Go Live Testing - Sample ADF': 'Sample ADF',
        'Go Live Testing - Inbound Email Test': 'Inbound Email',
        'Go Live Testing - Outbound Mail Test': 'Outbound Email',
        'Go Live Testing - Data Migration Test': 'Data Migration'
    }

    # Columns to keep (including those that don't need renaming)
    columns_to_keep = [
        'Dealership Name',
        'Implementation Type',
        'Region',
        'Go Live Date',
        'Configuration - Assigned',
        'Configuration - Status',
        'Pre Go Live - Assigned to',
        'Pre Go Live - Domain Updated',
        'Pre Go Live - Set Up Check',
        'Go Live Testing - Assigned To',
        'Go Live Testing - Sample ADF',
        'Go Live Testing - Inbound Email Test',
        'Go Live Testing - Outbound Mail Test',
        'Go Live Testing - Data Migration Test'
    ]

    # Only keep columns that exist
    existing_cols = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_cols]
    
    # Rename columns
    df.rename(columns=column_mapping, inplace=True)

    print(f"[INFO CRM Loader] Columns after mapping: {df.columns.tolist()}")

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

    print(f"[INFO CRM Loader] Final data shape: {df.shape}")

    return df

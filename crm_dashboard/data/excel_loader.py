"""
Excel Data Loader for CRM Dashboard
Loads data from local Excel file and combines all month sheets
"""

import pandas as pd
import os
from pathlib import Path
from shared.data_paths import get_excel_file_path, CRM_FILE


def load_crm_data_from_excel():
    """
    Load CRM Configuration data from Excel file
    Combines all month sheets into one dataset

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

    print(f"[DEBUG CRM Loader] Found sheets: {xl.sheet_names}")

    for sheet_name in xl.sheet_names:
        df_sheet = pd.read_excel(excel_path, sheet_name=sheet_name)
        print(f"[DEBUG CRM Loader] Sheet '{sheet_name}': {len(df_sheet)} rows")
        all_data.append(df_sheet)

    # Combine all sheets
    df = pd.concat(all_data, ignore_index=True)

    # Standardize column names - strip whitespace
    df.columns = df.columns.str.strip()

    print(f"[DEBUG CRM Loader] Combined data: {len(df)} rows")
    print(f"[DEBUG CRM Loader] Columns in Excel: {df.columns.tolist()}")

    # Map to expected column names
    # Note: 'Dealership Name', 'Go Live Date', and 'Implementation Type' are already correct in updated Excel
    column_mapping = {
        'Configuration - Status': 'Configuration Status',
        'Configuration - Assigned': 'Configuration Assigned',
        'Pre Go Live - Assigned to': 'Pre Go Live Assigned',
        'Pre Go Live - Domain Updated': 'Domain Updated',
        'Pre Go Live - Set Up Check': 'Set Up Check',
        'Go Live Testing - Assigned To': 'Go Live Testing Assigned',
        'Go Live Testing - Sample ADF': 'Sample ADF',
        'Go Live Testing - Inbound Email Test': 'Inbound Email',
        'Go Live Testing - Outbound Mail Test': 'Outbound Email',
        'Go Live Testing - Data Migration Test': 'Data Migration'
    }

    df.rename(columns=column_mapping, inplace=True)

    print(f"[DEBUG CRM Loader] Columns after mapping: {df.columns.tolist()}")

    # 'Dealership Name' is already combined in Excel (e.g., "Lewiston Auto Co., Inc. - 1067")
    # 'Go Live Date' is already correct in Excel

    # Standardize values (case-insensitive, trim spaces)
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
            # Replace 'nan' string with actual NaN
            df[col] = df[col].replace(['nan', 'NaN', 'None', ''], pd.NA)

    # Standardize Configuration Status
    if 'Configuration Status' in df.columns:
        # Map variations to standard values (case-insensitive)
        config_mapping = {
            'standard configuration': 'Standard',
            'stnadard configuration': 'Standard',  # Fix typo in data
            'standard': 'Standard',
            'copy store': 'Copy',
            'copy': 'Copy',
            'implementation': 'Implementation',
            'custom': 'Implementation',
            'not configured': 'Not Configured',
        }
        # Convert to lowercase for mapping, handle NaN
        df['Configuration Status'] = df['Configuration Status'].fillna('').astype(str).str.lower().str.strip()
        df['Configuration Status'] = df['Configuration Status'].replace(config_mapping)
        # Replace empty strings with 'Not Configured'
        df.loc[df['Configuration Status'] == '', 'Configuration Status'] = 'Not Configured'

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
            'United Kingdom': 'United Kingdom',
            'Canada': 'Canada',
        }
        df['Region'] = df['Region'].replace(region_mapping)

    print(f"[DEBUG CRM Loader] Final columns: {df.columns.tolist()}")

    return df


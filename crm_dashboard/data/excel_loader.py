"""
Excel Data Loader for CRM Dashboard
Loads data from local Excel file and combines all month sheets
"""

import pandas as pd
import os
from pathlib import Path


def load_crm_data_from_excel():
    """
    Load CRM Configuration data from Excel file
    Combines all month sheets into one dataset

    Returns:
        pd.DataFrame: CRM configuration data with standardized column names
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    excel_path = project_root / "data" / "CRM Data.xlsx"

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

    # Standardize column names
    df.columns = df.columns.str.strip()

    print(f"[DEBUG CRM Loader] Combined data: {len(df)} rows")
    print(f"[DEBUG CRM Loader] Columns: {df.columns.tolist()}")

    # Map to expected column names (keep Dealer Name for data processor)
    column_mapping = {
        'Go Live': 'Go Live Date',
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

    # Keep both 'Dealer Name' and 'Dealer ID' for the data processor to combine later

    # Standardize values (case-insensitive, trim spaces)
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

    print(f"[DEBUG CRM Loader] Final columns: {df.columns.tolist()}")

    return df


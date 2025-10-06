"""
Excel Data Loader for CRM Dashboard
Loads data from local Excel file
"""

import pandas as pd
import os
from pathlib import Path


def load_crm_data_from_excel():
    """
    Load CRM Configuration data from Excel file
    
    Returns:
        pd.DataFrame: CRM configuration data from "Stores Checklist" sheet
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    excel_path = project_root / "data" / "CRM Data.xlsx"
    
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    # Read the Excel file - use "Stores Checklist" sheet
    try:
        df = pd.read_excel(excel_path, sheet_name="Stores Checklist")
    except:
        # If "Stores Checklist" doesn't exist, try first sheet
        df = pd.read_excel(excel_path, sheet_name=0)
    
    return df


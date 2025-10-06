"""
Excel Data Loader for ARC Dashboard
Loads data from local Excel file
"""

import pandas as pd
import os
from pathlib import Path


def load_arc_data_from_excel():
    """
    Load ARC Configuration data from Excel file
    
    Returns:
        pd.DataFrame: ARC configuration data
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    excel_path = project_root / "data" / "ARC Configuration.xlsx"
    
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    # Read the Excel file
    # Assuming the data is in the first sheet or a sheet named "Surge List"
    try:
        df = pd.read_excel(excel_path, sheet_name="Surge List")
    except:
        # If "Surge List" sheet doesn't exist, try the first sheet
        df = pd.read_excel(excel_path, sheet_name=0)
    
    return df


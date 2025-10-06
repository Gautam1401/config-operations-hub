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
        pd.DataFrame: Integration access board data
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    excel_path = project_root / "data" / "Integration Access Board.xlsx"
    
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    # Read the Excel file - try first sheet
    df = pd.read_excel(excel_path, sheet_name=0)
    
    return df


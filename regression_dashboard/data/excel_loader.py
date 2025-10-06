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
        pd.DataFrame: Regression testing data from "Stores Checklist" sheet
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    excel_path = project_root / "data" / "E2E Testing Check.xlsx"
    
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    # Read the Excel file - use "Stores Checklist" sheet
    df = pd.read_excel(excel_path, sheet_name="Stores Checklist")
    
    return df


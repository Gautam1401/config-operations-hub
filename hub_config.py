"""
Hub Configuration - Central path configuration for all dashboards
"""

from pathlib import Path
from shared.data_paths import get_excel_file_path, CRM_FILE, ARC_FILE, INTEGRATION_FILE, REGRESSION_FILE


def get_excel_path(filename: str) -> str:
    """
    Get the full path to an Excel file in the Data Source folder
    
    Args:
        filename: Name of the Excel file
        
    Returns:
        str: Full path to the Excel file
    """
    return str(get_excel_file_path(filename))


# Excel file paths for each dashboard
CRM_EXCEL_PATH = get_excel_path(CRM_FILE)
ARC_EXCEL_PATH = get_excel_path(ARC_FILE)
INTEGRATION_EXCEL_PATH = get_excel_path(INTEGRATION_FILE)
REGRESSION_EXCEL_PATH = get_excel_path(REGRESSION_FILE)

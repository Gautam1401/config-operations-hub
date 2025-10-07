"""
Centralized Data Path Configuration
Stores the path to the Data Source folder for all dashboards
"""

from pathlib import Path
import os


def get_data_source_folder() -> Path:
    """
    Get the Data Source folder path

    Returns the "Data Source" folder in the project root.
    This folder is committed to GitHub and deployed to Streamlit Cloud.

    Returns:
        Path: Path to the Data Source folder
    """
    # Option 1: Try environment variable first (for future multi-user support)
    env_path = os.getenv('DATA_SOURCE_PATH')
    if env_path:
        return Path(env_path)

    # Option 2: Use "Data Source" folder in project root
    # This folder is committed to GitHub and works on both local and Streamlit Cloud
    project_root = Path(__file__).parent.parent
    return project_root / "Data Source"


def get_excel_file_path(filename: str) -> Path:
    """
    Get the full path to an Excel file in the Data Source folder
    
    Args:
        filename: Name of the Excel file (e.g., "CRM Data.xlsx")
        
    Returns:
        Path: Full path to the Excel file
    """
    data_source = get_data_source_folder()
    return data_source / filename


# File name constants
CRM_FILE = "CRM Data.xlsx"
ARC_FILE = "ARC Configurations.xlsx"
INTEGRATION_FILE = "Integration Access Board.xlsx"
REGRESSION_FILE = "E2E Testing Check .xlsx"


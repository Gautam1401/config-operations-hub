"""
Regression Testing Dashboard - Configuration Settings
"""

# Dashboard metadata
DASHBOARD_TITLE = "Regression Testing Dashboard"
DASHBOARD_ICON = "🧪"

# Data source settings
USE_MOCK_DATA = False  # Set to True for mock data, False for real Excel data
EXCEL_FILE_PATH = "data/E2E Testing Check.xlsx"
SHEET_NAME = "Stores Checklist"

# Date filter options (sub-tabs)
DATE_FILTERS = {
    'current_month': 'Current Month',
    'next_month': 'Next Month',
    'ytd': 'YTD (Year to Date)'
}

# KPI definitions
KPI_DEFINITIONS = {
    'Total Go Live': 'Total number of go-lives in the selected period',
    'Completed': 'Testing Status = Completed',
    'WIP': 'Testing Status = WIP',
    'Unable to Complete': 'Testing Status = Unable to Complete',
    'Upcoming Next Week': 'SIM Start Date within next 7 days from today',
    'Data Incomplete': 'SIM Start Date before today but Status is blank'
}

# Implementation types
IMPLEMENTATION_TYPES = ['Conquest', 'Buy/Sell', 'Enterprise', 'New Point', 'All']

# KPI color mapping
KPI_COLORS = {
    'Total Go Live': 'kpi-accent',
    'Completed': 'kpi-success',
    'WIP': 'kpi-warning',
    'Unable to Complete': 'kpi-error',
    'Upcoming Next Week': 'kpi-info',
    'Data Incomplete': 'kpi-grey'
}

# Column mappings from source data to standard names
COLUMN_MAPPINGS = {
    # Source column name: Standard column name
    'Dealership Name': 'Dealership Name',
    'Go-Live Date': 'Go Live Date',
    'SIM Start Date': 'SIM Start Date',
    'Assignee': 'Assignee',
    'Region': 'Region',
    'Testing Status': 'Status',
    'Type of Implementation': 'Type of Implementation'
}

# Required fields for data completeness check
REQUIRED_FIELDS = [
    'Dealership Name',
    'Go Live Date',
    'SIM Start Date',
    'Assignee',
    'Region',
    'Status'
]

# Display columns for data table
DISPLAY_COLUMNS = [
    'Dealership Name',
    'Go Live Date',
    'SIM Start Date',
    'Assignee',
    'Region',
    'Status'
]

# Date format
DATE_FORMAT = '%Y-%m-%d'
DISPLAY_DATE_FORMAT = '%d-%b-%Y'

# Mock data settings
MOCK_DATA_ROWS = 50


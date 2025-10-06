"""
Integration Dashboard - Configuration Settings
"""

# Dashboard metadata
DASHBOARD_TITLE = "Integration Dashboard"
DASHBOARD_ICON = "🔗"

# Data source settings
USE_MOCK_DATA = True  # Set to False when connecting to SharePoint
SHAREPOINT_SITE_URL = ""  # To be configured
SHAREPOINT_LIST_NAME = "Integration Access Board"

# Date filter options (sub-tabs)
DATE_FILTERS = {
    'current_month': 'Current Month',
    'next_month': 'Next Month',
    'two_months': '2 Months From Now',
    'ytd': 'YTD (Year to Date)'
}

# KPI definitions
KPI_DEFINITIONS = {
    'Total Go Lives': 'Total number of go-lives in the selected period',
    'GTG': 'Vendor List Updated = Yes',
    'On Track': 'Vendor List Updated = No and within safe timeframe',
    'Critical': 'Vendor List Updated = No and approaching deadline',
    'Escalated': 'Vendor List Updated = No and past safe deadline',
    'Data Incomplete': 'Missing key data fields'
}

# Implementation types
IMPLEMENTATION_TYPES = ['Conquest', 'Buy/Sell', 'New Point']

# Regions (will be dynamically loaded from data)
REGIONS = ['NAM', 'EMEA', 'APAC', 'LATAM']

# Status color mapping
STATUS_COLORS = {
    'GTG': '#29C46F',           # Green
    'On Track': '#3874F2',      # Blue
    'Critical': '#FF9800',      # Orange
    'Escalated': '#F44336',     # Red
    'Data Incomplete': '#23272F' # Grey
}

# KPI color mapping
KPI_COLORS = {
    'Total Go Lives': 'kpi-accent',
    'GTG': 'kpi-success',
    'On Track': 'kpi-accent',
    'Critical': 'kpi-warning',
    'Escalated': 'kpi-error',
    'Upcoming Week': 'kpi-info',
    'Data Incomplete': 'kpi-grey'
}

# Column mappings from source data to standard names
COLUMN_MAPPINGS = {
    # Source column name: Standard column name
    'Dealer Name': 'Dealer Name',
    'Dealer ID': 'Dealer ID',
    'Go Live Date': 'Go Live Date',
    'Implementation Type': 'Implementation Type',
    'Vendor List Updated': 'Vendor List Updated',
    'PEM': 'PEM',
    'Director': 'Director',
    'Assigned to': 'Assignee',
    'Region': 'Region'
}

# Required fields for data completeness check
REQUIRED_FIELDS = [
    'Dealer Name',
    'Dealer ID',
    'Go Live Date',
    'Implementation Type',
    'PEM',
    'Director',
    'Assignee'
]

# Days to Go Live thresholds by Implementation Type
THRESHOLDS = {
    'Conquest': {
        'on_track': 60,      # > 60 days
        'critical_min': 30,  # 30-60 days
        'critical_max': 60,
        'escalated': 30      # < 30 days
    },
    'Buy/Sell': {
        'on_track': 15,      # > 15 days
        'critical_min': 3,   # 3-15 days
        'critical_max': 15,
        'escalated': 3       # < 3 days
    },
    'New Point': {
        'on_track': 15,      # > 15 days
        'critical_min': 3,   # 3-15 days
        'critical_max': 15,
        'escalated': 3       # < 3 days
    }
}

# Display columns for data table
DISPLAY_COLUMNS = [
    'Dealership Name',
    'Go Live Date',
    'Days to Go Live',
    'Implementation Type',
    'PEM',
    'Director',
    'Assignee',
    'Status'
]

# Date format
DATE_FORMAT = '%Y-%m-%d'
DISPLAY_DATE_FORMAT = '%d-%b-%Y'


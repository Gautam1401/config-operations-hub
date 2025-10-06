"""
CRM Configuration Dashboard - Settings and Constants
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

# ============================================================================
# DASHBOARD INFO
# ============================================================================

DASHBOARD_TITLE = "CRM Configuration Dashboard"
PAGE_ICON = "📊"
COMPANY_NAME = "Tekion"

# ============================================================================
# DATA SOURCE
# ============================================================================

USE_MOCK_DATA = True  # Set to False for SharePoint

SHAREPOINT_CONFIG = {
    'site_url': 'https://your-tenant.sharepoint.com/sites/your-site',
    'list_name': 'CRM Configuration',
    'credentials': {
        'username': 'user@domain.com',
        'password': 'password'
    }
}

# ============================================================================
# MOCK DATA SETTINGS
# ============================================================================

MOCK_DATA_ROWS = 100

# ============================================================================
# REGIONS
# ============================================================================

REGIONS = ['NAM', 'EMEA', 'APAC', 'LATAM']

# ============================================================================
# SUB-TABS
# ============================================================================

SUB_TABS = {
    'configuration': 'Configuration',
    'pre_go_live': 'Pre Go Live Checks',
    'go_live_testing': 'Go Live Testing'
}

# ============================================================================
# STATUS OPTIONS
# ============================================================================

# Configuration statuses
CONFIGURATION_STATUS = ['Standard', 'Copy', 'Not Configured', 'Data Incorrect']

# Pre Go Live statuses
PRE_GO_LIVE_STATUS = ['GTG', 'Partial', 'Fail', 'Data Incorrect']

# Go Live Testing statuses
GO_LIVE_TESTING_STATUS = ['GTG', 'Go Live Blocker', 'Non-Blocker', 'Fail', 'Data Incorrect']

# Implementation types
IMPLEMENTATION_TYPES = ['Conquest', 'Buy-Sell', 'New Point']

# ============================================================================
# DATE FILTERS
# ============================================================================

_current_month = datetime.now().strftime('%B %Y')
_next_month = (datetime.now() + relativedelta(months=1)).strftime('%B %Y')

DATE_FILTERS = {
    'current_month': _current_month,
    'next_month': _next_month,
    'ytd': 'YTD (Year to Date)',
}

# ============================================================================
# COLORS
# ============================================================================

PRIMARY_COLOR = "#008080"  # Teal
SECONDARY_COLOR = "#FFFFFF"  # White
SUCCESS_COLOR = "#28a745"  # Green
WARNING_COLOR = "#ffc107"  # Yellow
DANGER_COLOR = "#dc3545"  # Red
INFO_COLOR = "#17a2b8"  # Blue

# KPI Colors for each sub-tab
KPI_COLORS = {
    # Configuration KPIs
    'Go Lives': PRIMARY_COLOR,
    'Standard': SUCCESS_COLOR,
    'Copy': INFO_COLOR,
    'Not Configured': WARNING_COLOR,
    'Data Incorrect': DANGER_COLOR,
    
    # Pre Go Live KPIs
    'Checks Completed': PRIMARY_COLOR,
    'GTG': SUCCESS_COLOR,
    'Partial': WARNING_COLOR,
    'Fail': DANGER_COLOR,
    
    # Go Live Testing KPIs
    'Tests Completed': PRIMARY_COLOR,
    'Go Live Blocker': DANGER_COLOR,
    'Non-Blocker': WARNING_COLOR,
}

# Status color mapping
STATUS_COLORS = {
    'Standard': SUCCESS_COLOR,
    'Copy': INFO_COLOR,
    'Not Configured': WARNING_COLOR,
    'GTG': SUCCESS_COLOR,
    'Partial': WARNING_COLOR,
    'Fail': DANGER_COLOR,
    'Go Live Blocker': DANGER_COLOR,
    'Non-Blocker': WARNING_COLOR,
    'Data Incorrect': DANGER_COLOR,
}

# ============================================================================
# UPCOMING WEEK THRESHOLD
# ============================================================================

UPCOMING_WEEK_DAYS = 7  # Highlight go-lives in next 7 days

# ============================================================================
# TABLE COLUMNS
# ============================================================================

DISPLAY_COLUMNS = [
    'Dealership Name',
    'Go Live Date',
    'Days to Go Live',
    'Implementation Type',
    'Region',
    'Assignee',
    'Status',
]

# ============================================================================
# FIELD MAPPINGS
# ============================================================================

# Map source columns to standard names
COLUMN_MAPPINGS = {
    'Dealer Name': 'Dealer Name',
    'Dealer ID': 'Dealer ID',
    'Go Live Date': 'Go Live Date',
    'Implementation Type': 'Implementation Type',
    'Region': 'Region',
    
    # Configuration fields
    'Configuration Type': 'Configuration Type',
    'Configuration Assigned To': 'Configuration Assignee',
    
    # Pre Go Live fields
    'Domain Updated': 'Domain Updated',
    'Set Up Check': 'Set Up Check',
    'Pre Go Live Assigned To': 'Pre Go Live Assignee',
    
    # Go Live Testing fields
    'Sample ADF': 'Sample ADF',
    'Inbound Email': 'Inbound Email',
    'Outbound Email': 'Outbound Email',
    'Data Migration': 'Data Migration',
    'Go Live Testing Assigned To': 'Go Live Testing Assignee',
    
    # Status field
    'Go Live Status': 'Go Live Status',
}


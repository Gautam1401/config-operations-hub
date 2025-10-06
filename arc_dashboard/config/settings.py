"""
Configuration settings for ARC Dashboard
Contains all constants, color schemes, and configuration parameters
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

# ============================================================================
# DASHBOARD SETTINGS
# ============================================================================

DASHBOARD_TITLE = "ARC Configuration Dashboard"
COMPANY_NAME = "Tekion"
PAGE_ICON = "📊"

# ============================================================================
# COLOR SCHEME - Tekion Branding
# ============================================================================

COLORS = {
    # Primary Colors
    'primary': '#008080',      # Teal
    'secondary': '#005F5F',    # Dark Teal
    'accent': '#00A0A0',       # Light Teal
    
    # Status Colors
    'success': '#28a745',      # Green
    'warning': '#ffc107',      # Yellow
    'danger': '#dc3545',       # Red
    'info': '#17a2b8',         # Blue
    
    # Background Colors
    'bg_primary': '#FFFFFF',   # White
    'bg_secondary': '#F8F9FA', # Light Gray
    'bg_dark': '#343A40',      # Dark Gray
    
    # Text Colors
    'text_primary': '#212529',
    'text_secondary': '#6C757D',
    'text_light': '#FFFFFF',
}

# ============================================================================
# KPI CARD COLORS
# ============================================================================

KPI_COLORS = {
    'Total Go Live': '#008080',
    'Completed': '#28a745',
    'WIP': '#ffc107',
    'Not Configured': '#dc3545',
    
    # Breakdown Colors
    'Service': '#17a2b8',
    'Parts': '#6610f2',
    'Accounting': '#fd7e14',
    'Any': '#6c757d',
}

# ============================================================================
# DATA CONFIGURATION
# ============================================================================

# Column mappings for Excel file
COLUMN_MAPPING = {
    'dealership_name': 'Dealership Name',
    'go_live_date': 'Go Live Date',
    'implementation_type': 'Type of Implementation',
    'assigned_to': 'Assigned To',
    'region': 'Region',
    'lob': 'Line of Business',  # Service, Parts, Accounting
    'status': 'Status',  # Completed, WIP, Not Configured
}

# Expected LOBs
LOBS = ['Service', 'Parts', 'Accounting']

# Status values
STATUS_VALUES = ['Completed', 'WIP', 'Not Configured']

# ============================================================================
# SHAREPOINT CONFIGURATION
# ============================================================================

# SharePoint settings (to be configured by user)
SHAREPOINT_CONFIG = {
    'site_url': '',  # e.g., 'https://yourtenant.sharepoint.com/sites/yoursite'
    'file_path': '',  # e.g., '/Shared Documents/ARC Configuration/data.xlsx'
    'client_id': '',  # Azure AD App Client ID
    'client_secret': '',  # Azure AD App Client Secret
    'tenant_id': '',  # Azure AD Tenant ID
}

# ============================================================================
# DATE FILTER OPTIONS
# ============================================================================

# Calculate current and next month dynamically
_current_month = datetime.now().strftime('%B %Y')
_next_month = (datetime.now() + relativedelta(months=1)).strftime('%B %Y')

DATE_FILTERS = {
    'current_month': _current_month,
    'next_month': _next_month,
    'ytd': 'YTD (Year to Date)',
}

# ============================================================================
# MOCK DATA SETTINGS
# ============================================================================

USE_MOCK_DATA = False  # Set to True for mock data, False for real Excel data
MOCK_DATA_ROWS = 100  # Number of mock records to generate

# ============================================================================
# UI SETTINGS
# ============================================================================

# Card dimensions
CARD_HEIGHT = 120
CARD_PADDING = 20

# Table settings
TABLE_PAGE_SIZE = 25
TABLE_HEIGHT = 400

# Export settings
EXPORT_FILENAME_PREFIX = 'ARC_Configuration_Export'


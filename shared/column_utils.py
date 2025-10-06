"""
Column Alias/Fuzzy Matching Utilities
Handles different column name variations across Excel files
"""

# --- COLUMN ALIAS/FUZZY MATCHING ---
COLUMN_ALIASES = {
    'Dealer Name': ['Dealer Name', 'Dealership Name', 'Name', 'Store Name'],
    'Dealer ID': ['Dealer ID', 'Dealership ID', 'ID', 'Store ID'],
    'Dealership Name': ['Dealership Name', 'Dealer Name', 'Name', 'Store Name'],
    'Status': ['Status', 'Testing Status', 'Go Live Status', 'Configuration Status'],
    'Module': ['Module', 'Line of Business', 'LOB'],
    'Go Live Date': ['Go Live Date', 'Go-Live Date', 'Go Live', 'GoLive Date'],
    'Assigned To': ['Assigned To', 'Assignee', 'Assigned', 'Owner'],
    'Region': ['Region', 'Area', 'Territory'],
    'Type of Implementation': ['Type of Implementation', 'Implementation Type', 'Type'],
    'Days to Go Live': ['Days to Go Live', 'Days To Go Live', 'Days'],
    'PEM': ['PEM', 'Project Manager', 'PM'],
    'Director': ['Director', 'Dir'],
    'SIM Start Date': ['SIM Start Date', 'SIM Start', 'Start Date'],
    'Configuration Status': ['Configuration Status', 'Config Status', 'Configuration - Status'],
    'Configuration Assigned': ['Configuration Assigned', 'Config Assigned', 'Configuration - Assigned'],
    'Pre Go Live Assigned': ['Pre Go Live Assigned', 'Pre Go Live - Assigned to', 'Pre-Go Live Assigned'],
    'Domain Updated': ['Domain Updated', 'Pre Go Live - Domain Updated', 'Domain'],
    'Set Up Check': ['Set Up Check', 'Pre Go Live - Set Up Check', 'Setup Check'],
    'Go Live Testing Assigned': ['Go Live Testing Assigned', 'Go Live Testing - Assigned To', 'Testing Assigned'],
    'Sample ADF': ['Sample ADF', 'Go Live Testing - Sample ADF', 'ADF'],
    'Inbound Email': ['Inbound Email', 'Go Live Testing - Inbound Email Test', 'Inbound'],
    'Outbound Email': ['Outbound Email', 'Go Live Testing - Outbound Mail Test', 'Outbound'],
    'Data Migration': ['Data Migration', 'Go Live Testing - Data Migration Test', 'Migration'],
    'Vendor List Updated': ['Vendor List Updated', 'Vendor Updated', 'Vendor List'],
}


def find_column(df, expected):
    """
    Find a column in DataFrame using fuzzy matching with aliases
    
    Args:
        df: pandas DataFrame
        expected: Expected column name (key in COLUMN_ALIASES)
        
    Returns:
        str: Actual column name in the DataFrame
        
    Raises:
        KeyError: If column not found
    """
    aliases = COLUMN_ALIASES.get(expected, [expected])
    df_cols_lower = {c.lower().strip(): c for c in df.columns}
    
    for alias in aliases:
        key = alias.strip().lower()
        if key in df_cols_lower:
            return df_cols_lower[key]
    
    raise KeyError(
        f"Could not find the expected column '{expected}'. "
        f"Tried: {aliases}. "
        f"Columns present: {list(df.columns)}"
    )


def safe_get_column(df, expected, default=None):
    """
    Safely get a column from DataFrame, return default if not found
    
    Args:
        df: pandas DataFrame
        expected: Expected column name
        default: Default value if column not found (default: None)
        
    Returns:
        pandas Series or default value
    """
    try:
        col_name = find_column(df, expected)
        return df[col_name]
    except KeyError:
        return default


def has_column(df, expected):
    """
    Check if DataFrame has a column (using fuzzy matching)
    
    Args:
        df: pandas DataFrame
        expected: Expected column name
        
    Returns:
        bool: True if column exists, False otherwise
    """
    try:
        find_column(df, expected)
        return True
    except KeyError:
        return False


def rename_columns_to_standard(df):
    """
    Rename all columns in DataFrame to standard names
    
    Args:
        df: pandas DataFrame
        
    Returns:
        pandas DataFrame with standardized column names
    """
    df = df.copy()
    df.columns = df.columns.str.strip()
    
    # Create reverse mapping: actual column -> standard name
    rename_map = {}
    df_cols_lower = {c.lower().strip(): c for c in df.columns}
    
    for standard_name, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            key = alias.strip().lower()
            if key in df_cols_lower:
                actual_col = df_cols_lower[key]
                if actual_col != standard_name:  # Only rename if different
                    rename_map[actual_col] = standard_name
                break  # Found match, move to next standard name
    
    if rename_map:
        df.rename(columns=rename_map, inplace=True)
        print(f"[DEBUG] Renamed columns: {rename_map}")
    
    return df


"""
Column Alias/Fuzzy Matching Utilities
Handles different column name variations across Excel files
"""

import pandas as pd


def standardize_columns(df):
    """
    Standardize all column names to lowercase, remove dashes/underscores

    Args:
        df: pandas DataFrame

    Returns:
        pandas DataFrame with standardized column names
    """
    df = df.copy()
    # Make all column names lower-case, remove extra spaces, normalize dashes/underscores
    df.columns = [col.strip().lower().replace('-', ' ').replace('_', ' ') for col in df.columns]
    return df


# --- COLUMN ALIAS/FUZZY MATCHING (all lowercase, normalized) ---
COLUMN_ALIASES = {
    'dealer name': ['dealer name', 'dealership name', 'name', 'store name'],
    'dealer id': ['dealer id', 'dealership id', 'id', 'store id'],
    'dealership name': ['dealership name', 'dealer name', 'name', 'store name'],
    'status': ['status', 'testing status', 'go live status', 'configuration status'],
    'module': ['module', 'line of business', 'lob'],
    'go live date': ['go live date', 'go live', 'golive date'],
    'assigned to': ['assigned to', 'assignee', 'assigned', 'owner'],
    'region': ['region', 'area', 'territory'],
    'type of implementation': ['type of implementation', 'implementation type', 'type'],
    'days to go live': ['days to go live', 'days to go live', 'days'],
    'pem': ['pem', 'project manager', 'pm'],
    'director': ['director', 'dir'],
    'sim start date': ['sim start date', 'sim start', 'start date'],
    'configuration status': ['configuration status', 'config status', 'configuration   status'],
    'configuration assigned': ['configuration assigned', 'config assigned', 'configuration   assigned'],
    'pre go live assigned': ['pre go live assigned', 'pre go live   assigned to', 'pre go live assigned'],
    'domain updated': ['domain updated', 'pre go live   domain updated', 'domain'],
    'set up check': ['set up check', 'pre go live   set up check', 'setup check'],
    'go live testing assigned': ['go live testing assigned', 'go live testing   assigned to', 'testing assigned'],
    'sample adf': ['sample adf', 'go live testing   sample adf', 'adf'],
    'inbound email': ['inbound email', 'go live testing   inbound email test', 'inbound'],
    'outbound email': ['outbound email', 'go live testing   outbound mail test', 'outbound'],
    'data migration': ['data migration', 'go live testing   data migration test', 'migration'],
    'vendor list updated': ['vendor list updated', 'vendor updated', 'vendor list'],
}


def find_column(df, expected):
    """
    Find a column in DataFrame using fuzzy matching with aliases
    Assumes df columns are already standardized (lowercase, no dashes/underscores)

    Args:
        df: pandas DataFrame (should be standardized first)
        expected: Expected column name (will be normalized)

    Returns:
        str: Actual column name in the DataFrame

    Raises:
        KeyError: If column not found
    """
    # Normalize the expected column name
    expected_normalized = expected.strip().lower().replace('-', ' ').replace('_', ' ')

    # Get aliases for this column
    aliases = COLUMN_ALIASES.get(expected_normalized, [expected_normalized])

    # Try to find a match
    for alias in aliases:
        if alias in df.columns:
            return alias

    raise KeyError(
        f"Column '{expected}' not found in your file. "
        f"Tried: {aliases}. "
        f"Got columns: {list(df.columns)}"
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


def validate_and_debug_dataframe(df, dashboard_name="Dashboard"):
    """
    Validate and debug DataFrame - print useful information
    Does NOT modify the DataFrame, just prints debug info

    Args:
        df: pandas DataFrame
        dashboard_name: Name of the dashboard for logging

    Returns:
        pandas DataFrame (same as input, unmodified)
    """
    print(f"\n{'='*60}")
    print(f"[DEBUG {dashboard_name}] Data Validation")
    print(f"{'='*60}")

    print(f"✅ Loaded {len(df)} rows")
    print(f"📋 Columns: {df.columns.tolist()}")
    print(f"\n📊 First 2 rows:")
    print(df.head(2))

    # Check for Status column (case-insensitive)
    status_cols = [c for c in df.columns if 'status' in c.lower()]
    if status_cols:
        status_col = status_cols[0]
        print(f"\n✅ Status column found: '{status_col}'")
        print(f"   Unique values: {df[status_col].unique().tolist()}")
        print(f"   Value counts:\n{df[status_col].value_counts()}")
    else:
        print(f"\n⚠️  Status column not found")

    # Check for Go Live Date column (case-insensitive)
    date_cols = [c for c in df.columns if 'go live' in c.lower() and 'date' in c.lower()]
    if date_cols:
        date_col = date_cols[0]
        print(f"\n✅ Go Live Date column found: '{date_col}'")
        print(f"   Earliest date: {pd.to_datetime(df[date_col], errors='coerce').min()}")
        print(f"   Latest date: {pd.to_datetime(df[date_col], errors='coerce').max()}")
        print(f"   Null dates: {pd.to_datetime(df[date_col], errors='coerce').isna().sum()}")
    else:
        print(f"\n⚠️  Go Live Date column not found")

    # Check for Region column (case-insensitive)
    region_cols = [c for c in df.columns if 'region' in c.lower()]
    if region_cols:
        region_col = region_cols[0]
        print(f"\n✅ Region column found: '{region_col}'")
        print(f"   Unique regions: {df[region_col].unique().tolist()}")
        print(f"   Region counts:\n{df[region_col].value_counts()}")
    else:
        print(f"\n⚠️  Region column not found")

    print(f"\n{'='*60}\n")

    return df


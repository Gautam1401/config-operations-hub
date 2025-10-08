"""
Data Processing Utilities for ARC Dashboard
Handles data transformations, calculations, and filtering
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from shared.column_utils import find_column, has_column


class ARCDataProcessor:
    """
    Processes ARC configuration data for dashboard display
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize processor with data
        
        Args:
            df: DataFrame with ARC configuration data
        """
        # Defensive coding: ensure df is a DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"ARCDataProcessor expects a pandas DataFrame, "
                f"but got {type(df).__name__}. "
                f"If you're passing an ARCDataProcessor object, "
                f"use processor.df to get the underlying DataFrame."
            )
        
        self.df = df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """
        Prepare data: convert dates, calculate days to go live, etc.
        """
        # Debug: Print columns at start
        print(f"[DEBUG ARCDataProcessor] Columns received: {self.df.columns.tolist()}")
        print(f"[DEBUG ARCDataProcessor] Data shape: {self.df.shape}")

        # Convert Go Live Date to datetime
        self.df['Go Live Date'] = pd.to_datetime(self.df['Go Live Date'], errors='coerce')

        # Calculate Days to Go Live
        today = pd.Timestamp(datetime.now().date())
        self.df['Days to Go Live'] = (self.df['Go Live Date'] - today).dt.days

        # Add Month and Year columns for filtering
        self.df['Month'] = self.df['Go Live Date'].dt.month
        self.df['Year'] = self.df['Go Live Date'].dt.year
        self.df['Month Name'] = self.df['Go Live Date'].dt.strftime('%B %Y')

        print(f"[DEBUG ARCDataProcessor] Data prepared successfully")
    
        
        # DEBUG: Print columns after preparation
        print(f"[DEBUG DataProcessor] _prepare_data - Columns AFTER prep: {self.df.columns.tolist()}")

    def filter_by_date_range(self, filter_type: str) -> pd.DataFrame:
        """
        Filter data by month name

        Args:
            filter_type: 'september', 'october', 'november', or 'ytd'

        Returns:
            pd.DataFrame: Filtered data
        """
        if filter_type == 'september':
            # September 2025
            mask = (self.df['Go Live Date'].dt.month == 9) & \
                   (self.df['Go Live Date'].dt.year == 2025)
            return self.df[mask].copy()

        elif filter_type == 'october':
            # October 2025
            mask = (self.df['Go Live Date'].dt.month == 10) & \
                   (self.df['Go Live Date'].dt.year == 2025)
            return self.df[mask].copy()

        elif filter_type == 'november':
            # November 2025
            mask = (self.df['Go Live Date'].dt.month == 11) & \
                   (self.df['Go Live Date'].dt.year == 2025)
            return self.df[mask].copy()

        elif filter_type == 'ytd':
            # YTD: All data (entire dataset)
            return self.df.copy()

        else:
            return self.df.copy()
    
    def get_kpi_counts(self, df: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """
        Calculate KPI counts - COUNT BY MODULE (wide format)

        Counts each module (Parts, Service, Accounting) separately
        Total = sum of all module counts

        Args:
            df: DataFrame to calculate from (uses self.df if None)

        Returns:
            dict: KPI counts
        """
        if df is None:
            df = self.df

        # Count by MODULE (not by dealership)
        # Each dealership has 3 modules: Parts, Service, Accounting

        # Count Completed modules
        parts_completed = (df['Parts Status'] == 'Completed').sum()
        service_completed = (df['Service Status'] == 'Completed').sum()
        accounting_completed = (df['Accounting Status'] == 'Completed').sum()
        total_completed = parts_completed + service_completed + accounting_completed

        # Count WIP modules
        parts_wip = (df['Parts Status'] == 'WIP').sum()
        service_wip = (df['Service Status'] == 'WIP').sum()
        accounting_wip = (df['Accounting Status'] == 'WIP').sum()
        total_wip = parts_wip + service_wip + accounting_wip

        # Count Not Configured modules
        parts_not_configured = (df['Parts Status'] == 'Not Configured').sum()
        service_not_configured = (df['Service Status'] == 'Not Configured').sum()
        accounting_not_configured = (df['Accounting Status'] == 'Not Configured').sum()
        total_not_configured = parts_not_configured + service_not_configured + accounting_not_configured

        # Total Go Live = number of dealerships (not modules)
        total_go_live = len(df)

        kpis = {
            'Total Go Live': total_go_live,
            'Completed': total_completed,
            'WIP': total_wip,
            'Not Configured': total_not_configured,
        }

        print(f"[DEBUG] KPI Counts (by module): {kpis}")
        print(f"[DEBUG]   Parts: Completed={parts_completed}, WIP={parts_wip}, Not Configured={parts_not_configured}")
        print(f"[DEBUG]   Service: Completed={service_completed}, WIP={service_wip}, Not Configured={service_not_configured}")
        print(f"[DEBUG]   Accounting: Completed={accounting_completed}, WIP={accounting_wip}, Not Configured={accounting_not_configured}")

        return kpis
    
    def get_lob_breakdown(self, status: str, df: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """
        Get breakdown by Module for a specific status (wide format)

        Args:
            status: Status to filter by ('Completed', 'WIP', or 'Not Configured')
            df: DataFrame to calculate from (uses self.df if None)

        Returns:
            dict: Module breakdown counts
        """
        if df is None:
            df = self.df

        # Count each module separately (wide format)
        parts_count = (df['Parts Status'] == status).sum()
        service_count = (df['Service Status'] == status).sum()
        accounting_count = (df['Accounting Status'] == status).sum()

        breakdown = {
            'Parts': parts_count,
            'Service': service_count,
            'Accounting': accounting_count,
            'Any': parts_count + service_count + accounting_count,  # Total for this status
        }

        # DEBUG: Print breakdown
        print(f"[DEBUG DataProcessor] LOB Breakdown for {status}: {breakdown}")

        return breakdown
    def get_regions(self, df: Optional[pd.DataFrame] = None) -> List[str]:
        """Get unique regions from data"""
        if df is None:
            df = self.df

        # Safety check: ensure Region column exists
        if 'Region' not in df.columns:
            print("[DEBUG ARC] 'Region' column missing in DataFrame!")
            return ['All']

        # Normalize regions: strip whitespace, title case
        df['Region'] = df['Region'].astype(str).str.strip().str.title()
        
        # Get unique regions, excluding NaN and empty values
        regions = [r for r in df['Region'].unique() if r and r != 'Nan']
        
        # If no regions found, return default
        if not regions:
            print("[DEBUG ARC] No regions found, returning default")
            return ['All']

        # Sort regions alphabetically, then add 'All' at the beginning
        sorted_regions = sorted(regions)
        region_options = ['All'] + sorted_regions
        
        print(f"[DEBUG ARC] Regions extracted: {region_options}")
        return region_options

    def filter_by_status(self, status: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Filter data by status (wide format)
        Returns dealerships where AT LEAST ONE module has the given status

        Args:
            status: Status to filter by
            df: DataFrame to filter (uses self.df if None)

        Returns:
            pd.DataFrame: Filtered data (dealerships with at least one module matching status)
        """
        if df is None:
            df = self.df

        # Filter dealerships where at least one module has this status
        mask = ((df['Parts Status'] == status) |
                (df['Service Status'] == status) |
                (df['Accounting Status'] == status))

        return df[mask].copy()

    def filter_by_lob(self, lob: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Filter data by Line of Business (Module) - wide format
        Returns dealerships with the specified module column

        Args:
            lob: LOB to filter by ('Parts', 'Service', or 'Accounting')
            df: DataFrame to filter (uses self.df if None)

        Returns:
            pd.DataFrame: Filtered data with only the specified module status
        """
        if df is None:
            df = self.df

        # For wide format, we can't really "filter" by LOB
        # Instead, we return the full dataframe but could add a column indicating which module
        # For now, just return the full dataframe
        # The UI will need to handle showing specific module columns
        return df.copy()
    
    def filter_by_region(self, region: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Filter data by region
        
        Args:
            region: Region to filter by ('All' returns all data)
            df: DataFrame to filter (uses self.df if None)
            
        Returns:
            pd.DataFrame: Filtered data
        """
        if df is None:
            df = self.df
        
        if region == 'All':
            return df.copy()
        
        return df[df['Region'] == region].copy()
    
    def get_display_dataframe(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Get DataFrame formatted for display in table
        
        Args:
            df: DataFrame to format (uses self.df if None)
            
        Returns:
            pd.DataFrame: Formatted data for display
        """
        if df is None:
            df = self.df
        
        # DEBUG: Print current columns before display
        print(f"[DEBUG DataProcessor] get_display_dataframe - Current columns: {df.columns.tolist()}")
        
        # DEFENSIVE: Check which column exists for Module/LOB
        module_col = None
        if 'Module' in df.columns:
            module_col = 'Module'
            print("[DEBUG DataProcessor] Using 'Module' column")
        elif 'Line of Business' in df.columns:
            module_col = 'Line of Business'
            print("[WARNING DataProcessor] Using 'Line of Business' column - should be 'Module'")
        else:
            print(f"[ERROR DataProcessor] Neither 'Module' nor 'Line of Business' found!")
            print(f"[ERROR DataProcessor] Available columns: {df.columns.tolist()}")
            # Use a placeholder
            module_col = 'Module'
        
        # Select and order columns for display
        display_cols = [
            'Dealership Name',
            'Go Live Date',
            'Type of Implementation',
            'Days to Go Live',
            'Assigned To',
            'Region',
            module_col,  # Use the detected column
            'Status',
        ]
        
        # DEFENSIVE: Check if all columns exist
        missing_cols = [col for col in display_cols if col not in df.columns]
        if missing_cols:
            print(f"[ERROR DataProcessor] Missing columns: {missing_cols}")
            print(f"[ERROR DataProcessor] Available columns: {df.columns.tolist()}")
            # Filter to only existing columns
            display_cols = [col for col in display_cols if col in df.columns]
        
        display_df = df[display_cols].copy()
        
        # Rename to Module if needed (standardize to 'Module')
        if module_col == 'Line of Business':
            display_df = display_df.rename(columns={'Line of Business': 'Module'})
        
        # Format Go Live Date
        display_df['Go Live Date'] = display_df['Go Live Date'].dt.strftime('%d-%b-%Y')

        # Format Days to Go Live: Show "Rolled Out" for negative values
        display_df['Days to Go Live'] = display_df['Days to Go Live'].apply(
            lambda x: "Rolled Out" if x < 0 else str(int(x))
        )
        
        print(f"[DEBUG DataProcessor] Display DataFrame ready: {len(display_df)} records, columns: {display_df.columns.tolist()}")
        
        return display_df
def calculate_days_to_go_live(go_live_date: datetime) -> int:
    """
    Calculate days remaining until go-live date
    
    Args:
        go_live_date: Go live date
        
    Returns:
        int: Days to go live (negative if past)
    """
    today = datetime.now().date()
    delta = (go_live_date.date() - today).days
    return delta


if __name__ == '__main__':
    # Test data processor
    from arc_dashboard.data.mock_data import generate_mock_data
    
    df = generate_mock_data(50)
    processor = ARCDataProcessor(df)
    
    print("Data Processor Test")
    print("=" * 50)
    
    # Test KPI counts
    kpis = processor.get_kpi_counts()
    print("\nKPI Counts:")
    for key, value in kpis.items():
        print(f"  {key}: {value}")
    
    # Test LOB breakdown
    print("\nCompleted LOB Breakdown:")
    completed_lob = processor.get_lob_breakdown('Completed')
    for key, value in completed_lob.items():
        print(f"  {key}: {value}")
    
    # Test regions
    print("\nRegions:")
    regions = processor.get_regions()
    print(f"  {regions}")
    
    # Test current month filter
    current_month_df = processor.filter_by_date_range('current_month')
    print(f"\nCurrent Month Records: {len(current_month_df)}")


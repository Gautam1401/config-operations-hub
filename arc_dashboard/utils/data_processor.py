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
        Filter data by date range
        
        Args:
            filter_type: 'current_month', 'next_month', or 'ytd'
            
        Returns:
            pd.DataFrame: Filtered data
        """
        today = datetime.now()
        
        if filter_type == 'current_month':
            # Current month
            mask = (self.df['Month'] == today.month) & (self.df['Year'] == today.year)
            return self.df[mask].copy()
            
        elif filter_type == 'next_month':
            # Next month
            next_month = today.month + 1 if today.month < 12 else 1
            next_year = today.year if today.month < 12 else today.year + 1
            mask = (self.df['Month'] == next_month) & (self.df['Year'] == next_year)
            return self.df[mask].copy()
            
        elif filter_type == 'ytd':
            # Year to date (from Jan 1 to today)
            start_of_year = datetime(today.year, 1, 1)
            mask = (self.df['Go Live Date'] >= pd.Timestamp(start_of_year)) & \
                   (self.df['Go Live Date'] <= pd.Timestamp(today))
            return self.df[mask].copy()
        
        else:
            return self.df.copy()
    
    def get_kpi_counts(self, df: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """
        Calculate KPI counts

        Args:
            df: DataFrame to calculate from (uses self.df if None)

        Returns:
            dict: KPI counts
        """
        if df is None:
            df = self.df

        # Debug: Check if Status column exists
        if 'Status' not in df.columns:
            print(f"[ERROR] 'Status' column not found! Available columns: {df.columns.tolist()}")
            return {
                'Total Go Live': len(df),
                'Completed': 0,
                'WIP': 0,
                'Not Configured': 0,
            }

        kpis = {
            'Total Go Live': len(df),
            'Completed': len(df[df['Status'] == 'Completed']),
            'WIP': len(df[df['Status'] == 'WIP']),
            'Not Configured': len(df[df['Status'] == 'Not Configured']),
        }

        print(f"[DEBUG] KPI Counts: {kpis}")

        return kpis
    
    def get_lob_breakdown(self, status: str, df: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """
        Get breakdown by Module for a specific status
        
        Args:
            status: Status to filter by ('Completed', 'WIP', or 'Not Configured')
            df: DataFrame to calculate from (uses self.df if None)
            
        Returns:
            dict: Module breakdown counts
        """
        if df is None:
            df = self.df
        
        # IMPROVEMENT #4: Check for Module column
        module_col = None
        if 'Module' in df.columns:
            module_col = 'Module'
        elif 'Line of Business' in df.columns:
            module_col = 'Line of Business'
            print("[WARNING] Using 'Line of Business' column - should be renamed to 'Module'")
        else:
            print(f"[ERROR] Neither 'Module' nor 'Line of Business' column found in DataFrame!")
            print(f"[ERROR] Available columns: {df.columns.tolist()}")
            # Return empty breakdown
            return {
                'Service': 0,
                'Parts': 0,
                'Accounting': 0,
                'Any': 0,
            }
        
        filtered = df[df['Status'] == status]
        
        breakdown = {
            'Service': len(filtered[filtered[module_col] == 'Service']),
            'Parts': len(filtered[filtered[module_col] == 'Parts']),
            'Accounting': len(filtered[filtered[module_col] == 'Accounting']),
            'Any': len(filtered),  # Total for this status
        }
        
        # DEBUG: Print breakdown
        print(f"[DEBUG DataProcessor] LOB Breakdown for {status}: {breakdown}")
        
        return breakdown
    def get_regions(self, df: Optional[pd.DataFrame] = None) -> List[str]:
        """
        Get unique regions from data
        
        Args:
            df: DataFrame to get regions from (uses self.df if None)
            
        Returns:
            list: Sorted list of unique regions
        """
        if df is None:
            df = self.df
        
        regions = sorted(df['Region'].unique().tolist())
        return ['All'] + regions
    
    def filter_by_status(self, status: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Filter data by status
        
        Args:
            status: Status to filter by
            df: DataFrame to filter (uses self.df if None)
            
        Returns:
            pd.DataFrame: Filtered data
        """
        if df is None:
            df = self.df
        
        return df[df['Status'] == status].copy()
    
    def filter_by_lob(self, lob: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Filter data by Line of Business
        
        Args:
            lob: LOB to filter by
            df: DataFrame to filter (uses self.df if None)
            
        Returns:
            pd.DataFrame: Filtered data
        """
        if df is None:
            df = self.df
        
        return df[df['Module'] == lob].copy()
    
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


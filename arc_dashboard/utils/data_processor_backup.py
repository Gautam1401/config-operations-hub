"""
Data Processing Utilities for ARC Dashboard
Handles data transformations, calculations, and filtering
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional


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
        # Convert Go Live Date to datetime
        self.df['Go Live Date'] = pd.to_datetime(self.df['Go Live Date'])
        
        # Calculate Days to Go Live
        today = pd.Timestamp(datetime.now().date())
        self.df['Days to Go Live'] = (self.df['Go Live Date'] - today).dt.days
        
        # Add Month and Year columns for filtering
        self.df['Month'] = self.df['Go Live Date'].dt.month
        self.df['Year'] = self.df['Go Live Date'].dt.year
        self.df['Month Name'] = self.df['Go Live Date'].dt.strftime('%B %Y')
    
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
        
        kpis = {
            'Total Go Live': len(df),
            'Completed': len(df[df['Status'] == 'Completed']),
            'WIP': len(df[df['Status'] == 'WIP']),
            'Not Configured': len(df[df['Status'] == 'Not Configured']),
        }
        
        return kpis
    
    def get_lob_breakdown(self, status: str, df: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """
        Get breakdown by Line of Business for a specific status
        
        Args:
            status: Status to filter by ('Completed' or 'WIP')
            df: DataFrame to calculate from (uses self.df if None)
            
        Returns:
            dict: LOB breakdown counts
        """
        if df is None:
            df = self.df
        
        filtered = df[df['Status'] == status]
        
        breakdown = {
            'Service': len(filtered[filtered['Line of Business'] == 'Service']),
            'Parts': len(filtered[filtered['Line of Business'] == 'Parts']),
            'Accounting': len(filtered[filtered['Line of Business'] == 'Accounting']),
            'Any': len(filtered),  # Total for this status
        }
        
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
        
        # Select and order columns for display
        display_cols = [
            'Dealership Name',
            'Go Live Date',
            'Type of Implementation',
            'Days to Go Live',
            'Assigned To',
            'Region',
            'Line of Business',
            'Status',
        ]
        
        display_df = df[display_cols].copy()
        
        # Rename Line of Business to Module
        display_df = display_df.rename(columns={'Line of Business': 'Module'})
        
        # Format Go Live Date
        display_df['Go Live Date'] = display_df['Go Live Date'].dt.strftime('%d-%b-%Y')
        
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


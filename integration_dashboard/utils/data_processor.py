"""
Integration Dashboard - Data Processor
Handles all data processing, filtering, and KPI calculations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from integration_dashboard.config.settings import (
    THRESHOLDS,
    REQUIRED_FIELDS,
    DISPLAY_COLUMNS,
    DATE_FORMAT,
    DISPLAY_DATE_FORMAT
)
from shared.column_utils import find_column, has_column


class IntegrationDataProcessor:
    """Process and analyze Integration data"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize processor with data
        
        Args:
            df: Raw integration data
        """
        self.df = self._prepare_data(df)
        print(f"[DEBUG Integration Processor] Initialized with {len(self.df)} records")
    
    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare and clean data
        
        Args:
            df: Raw data
            
        Returns:
            Cleaned and processed DataFrame
        """
        df = df.copy()
        
        # Convert Go Live Date to datetime
        df['Go Live Date'] = pd.to_datetime(df['Go Live Date'], errors='coerce')
        
        # Extract month and year for filtering
        df['Go Live Month'] = df['Go Live Date'].dt.month
        df['Go Live Year'] = df['Go Live Date'].dt.year
        
        # Calculate Days to Go Live
        today = pd.Timestamp.now().normalize()
        df['Days to Go Live'] = (df['Go Live Date'] - today).dt.days
        
        # Create Dealership Name (Dealer Name - Dealer ID)
        df['Dealership Name'] = df.apply(
            lambda row: f"{row['Dealer Name']} - {row['Dealer ID']}" 
            if pd.notna(row['Dealer Name']) and pd.notna(row['Dealer ID'])
            else '',
            axis=1
        )
        
        # Calculate Status
        df['Status'] = df.apply(self._calculate_status, axis=1)
        
        # Check for Data Incomplete
        df['Is Data Incomplete'] = df.apply(self._is_data_incomplete, axis=1)
        
        print(f"[DEBUG Integration Processor] Data prepared: {len(df)} records")
        print(f"[DEBUG Integration Processor] Columns: {df.columns.tolist()}")
        
        return df
    
    def _calculate_status(self, row) -> str:
        """
        Calculate status based on business rules
        
        Args:
            row: DataFrame row
            
        Returns:
            Status string
        """
        # Check for Data Incomplete first
        if self._is_data_incomplete(row):
            return 'Data Incomplete'
        
        # GTG: Vendor List Updated = 'Yes'
        if pd.notna(row['Vendor List Updated']) and row['Vendor List Updated'] == 'Yes':
            return 'GTG'
        
        # For other statuses, Vendor List Updated must be 'No'
        if pd.isna(row['Vendor List Updated']) or row['Vendor List Updated'] != 'No':
            return 'Data Incomplete'
        
        # Get implementation type and days to go live
        impl_type = row['Implementation Type']
        days = row['Days to Go Live']
        
        # Handle missing implementation type
        if pd.isna(impl_type) or impl_type == '':
            return 'Data Incomplete'
        
        # Handle rolled out (negative days)
        if days < 0:
            return 'GTG'  # Already rolled out
        
        # Get thresholds for this implementation type
        thresholds = THRESHOLDS.get(impl_type)
        if not thresholds:
            # Default to Buy/Sell thresholds if type not found
            thresholds = THRESHOLDS['Buy/Sell']
        
        # Escalated
        if days < thresholds['escalated']:
            return 'Escalated'
        
        # Critical
        if thresholds['critical_min'] <= days <= thresholds['critical_max']:
            return 'Critical'
        
        # On Track
        if days > thresholds['on_track']:
            return 'On Track'
        
        # Default to Critical if between escalated and on_track
        return 'Critical'
    
    def _is_data_incomplete(self, row) -> bool:
        """
        Check if row has incomplete data
        
        Args:
            row: DataFrame row
            
        Returns:
            True if data is incomplete
        """
        for field in REQUIRED_FIELDS:
            if field in row.index:
                if pd.isna(row[field]) or row[field] == '':
                    return True
        return False
    
    def get_upcoming_week_data(self) -> pd.DataFrame:
        """
        Get dealerships with Go Live in next 7 days from today (real-time)
        
        Returns:
            DataFrame with upcoming week go lives
        """
        today = pd.Timestamp.now().normalize()
        next_week = today + pd.Timedelta(days=7)
        
        # Filter: Go Live Date between today and 7 days from now
        upcoming = self.df[
            (self.df['Go Live Date'] >= today) &
            (self.df['Go Live Date'] <= next_week)
        ].copy()
        
        print(f"[DEBUG Integration Processor] Upcoming Week Go Lives: {len(upcoming)} records")
        print(f"[DEBUG Integration Processor] Date range: {today.date()} to {next_week.date()}")
        
        return upcoming
    
    def filter_by_date_range(self, date_filter: str) -> pd.DataFrame:
        """
        Filter data by date range using exact calendar month logic
        
        Args:
            date_filter: One of 'current_month', 'next_month', 'two_months', 'ytd'
            
        Returns:
            Filtered DataFrame
        """
        today = pd.Timestamp.today()
        
        if date_filter == 'current_month':
            # Current Month: Exact month and year match
            m, y = today.month, today.year
            filtered = self.df[(self.df['Go Live Month'] == m) & (self.df['Go Live Year'] == y)].copy()
            print(f"[DEBUG Integration Processor] Current Month: {m}/{y}")
        
        elif date_filter == 'next_month':
            # Next Month: Exact next month and year match
            next_date = today + pd.DateOffset(months=1)
            m, y = next_date.month, next_date.year
            filtered = self.df[(self.df['Go Live Month'] == m) & (self.df['Go Live Year'] == y)].copy()
            print(f"[DEBUG Integration Processor] Next Month: {m}/{y}")
        
        elif date_filter == 'two_months':
            # 2 Months From Now: Exact 2-months-ahead month and year match
            two_months_date = today + pd.DateOffset(months=2)
            m, y = two_months_date.month, two_months_date.year
            filtered = self.df[(self.df['Go Live Month'] == m) & (self.df['Go Live Year'] == y)].copy()
            print(f"[DEBUG Integration Processor] 2 Months From Now: {m}/{y}")
        
        elif date_filter == 'ytd':
            # YTD: All rows in the current year
            y = today.year
            filtered = self.df[self.df['Go Live Year'] == y].copy()
            print(f"[DEBUG Integration Processor] YTD: Year {y}")
        
        else:
            filtered = self.df.copy()
        
        print(f"[DEBUG Integration Processor] Filtered by {date_filter}: {len(filtered)} records")
        print(f"[DEBUG Integration Processor] Current date: {today.date()}")
        if len(filtered) > 0:
            print(f"[DEBUG Integration Processor] Sample dates in filtered data: {filtered['Go Live Date'].head().tolist()}")
        
        return filtered
    
    def get_kpis(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Calculate KPIs from filtered data
        
        Args:
            df: Filtered DataFrame
            
        Returns:
            Dictionary of KPI name to count
        """
        # Calculate Upcoming Week count (next 7 days from today)
        today = pd.Timestamp.now().normalize()
        next_week = today + pd.Timedelta(days=7)
        upcoming_week_count = len(self.df[
            (self.df['Go Live Date'] >= today) &
            (self.df['Go Live Date'] <= next_week)
        ])
        
        kpis = {
            'Total Go Lives': len(df),
            'GTG': len(df[df['Status'] == 'GTG']),
            'On Track': len(df[df['Status'] == 'On Track']),
            'Critical': len(df[df['Status'] == 'Critical']),
            'Escalated': len(df[df['Status'] == 'Escalated']),
            'Upcoming Week': upcoming_week_count,
            'Data Incomplete': len(df[df['Status'] == 'Data Incomplete'])
        }
        
        print(f"[DEBUG Integration Processor] KPIs: {kpis}")
        
        return kpis
    
    def get_regions(self, df: pd.DataFrame) -> List[str]:
        """
        Get unique regions from data

        Args:
            df: DataFrame

        Returns:
            List of unique regions
        """
        # Safety check: ensure Region column exists and has data
        if 'Region' not in df.columns or df['Region'].dropna().empty:
            print("[WARNING] No 'Region' column or all values missing!")
            return ['Unknown']  # Return default region

        regions = sorted(df['Region'].dropna().unique().tolist())

        # If no regions found, return default
        if not regions:
            return ['Unknown']

        print(f"[DEBUG Integration Processor] Regions: {regions}")
        return regions
    
    def get_region_counts(self, status: str, df: pd.DataFrame) -> Dict[str, int]:
        """
        Get counts by region for a specific status
        
        Args:
            status: Status to filter by
            df: DataFrame
            
        Returns:
            Dictionary of region to count
        """
        if status == 'Total Go Lives':
            status_df = df
        else:
            status_df = df[df['Status'] == status]
        
        region_counts = {}
        for region in self.get_regions(df):
            count = len(status_df[status_df['Region'] == region])
            region_counts[region] = count
        
        print(f"[DEBUG Integration Processor] Region counts for {status}: {region_counts}")
        
        return region_counts
    
    def filter_by_region(self, region: str, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter data by region
        
        Args:
            region: Region to filter by
            df: DataFrame
            
        Returns:
            Filtered DataFrame
        """
        filtered = df[df['Region'] == region].copy()
        print(f"[DEBUG Integration Processor] Filtered by region {region}: {len(filtered)} records")
        return filtered
    
    def get_display_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare DataFrame for display in table
        
        Args:
            df: Filtered DataFrame
            
        Returns:
            Display-ready DataFrame
        """
        display_df = df.copy()
        
        # Format Go Live Date
        display_df['Go Live Date'] = display_df['Go Live Date'].dt.strftime(DISPLAY_DATE_FORMAT)
        
        # Format Days to Go Live (show "Rolled Out" for negative values)
        display_df['Days to Go Live'] = display_df['Days to Go Live'].apply(
            lambda x: "Rolled Out" if x < 0 else str(int(x))
        )
        
        # Select and order display columns
        available_cols = [col for col in DISPLAY_COLUMNS if col in display_df.columns]
        display_df = display_df[available_cols].copy()
        
        print(f"[DEBUG Integration Processor] Display DataFrame ready: {len(display_df)} records")
        
        return display_df

"""
Regression Testing Dashboard - Data Processor
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from shared.column_utils import find_column, has_column


class RegressionDataProcessor:
    """Process and analyze Regression Testing data"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize data processor
        
        Args:
            df: Raw DataFrame from data source
        """
        self.df = df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare and clean data"""

        # Print available columns for debugging
        print(f"[DEBUG Regression Processor] Available columns: {self.df.columns.tolist()}")

        # Rename columns to standard names
        column_mapping = {
            'Go-Live Date': 'Go Live Date',
            'Testing Status': 'Status'
        }
        self.df.rename(columns=column_mapping, inplace=True)

        # Add missing columns with defaults if they don't exist
        required_cols = {
            'Go Live Date': None,
            'SIM Start Date': None,
            'Status': '',
            'Dealership Name': '',
            'Assignee': '',
            'Region': ''
        }

        for col, default_val in required_cols.items():
            if col not in self.df.columns:
                print(f"[WARNING] Column '{col}' not found, adding with default value")
                self.df[col] = default_val

        # Ensure date columns are datetime
        self.df['Go Live Date'] = pd.to_datetime(self.df['Go Live Date'], errors='coerce')
        self.df['SIM Start Date'] = pd.to_datetime(self.df['SIM Start Date'], errors='coerce')

        # Add Month and Year columns for filtering
        self.df['Go Live Month'] = self.df['Go Live Date'].dt.month
        self.df['Go Live Year'] = self.df['Go Live Date'].dt.year

        # Clean Status column (handle None, NaN, empty strings)
        self.df['Status'] = self.df['Status'].fillna('').astype(str).str.strip()
        self.df.loc[self.df['Status'] == '', 'Status'] = None

        print(f"[DEBUG Regression Processor] Data prepared: {len(self.df)} records")
        print(f"[DEBUG Regression Processor] Final columns: {self.df.columns.tolist()}")
        print(f"[DEBUG Regression Processor] Status distribution:\n{self.df['Status'].value_counts(dropna=False)}")
    
    def filter_by_date_range(self, filter_type: str) -> pd.DataFrame:
        """
        Filter data by month name (dynamically handles all 12 months)

        Args:
            filter_type: lowercase month name ('january', 'february', etc.) or 'ytd'

        Returns:
            Filtered DataFrame
        """
        if filter_type == 'ytd':
            # YTD: All data (entire dataset)
            filtered = self.df.copy()
        else:
            # Map month names to numbers
            month_map = {
                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                'september': 9, 'october': 10, 'november': 11, 'december': 12
            }

            if filter_type.lower() in month_map:
                month_num = month_map[filter_type.lower()]
                # Filter by month (any year in the data)
                mask = self.df['Go Live Month'] == month_num
                filtered = self.df[mask].copy()
            else:
                # Unknown filter, return all data
                filtered = self.df.copy()

        print(f"[DEBUG Regression Processor] Filtered by {filter_type}: {len(filtered)} records")
        return filtered
    
    def get_kpis(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Calculate KPIs from filtered data
        
        Args:
            df: Filtered DataFrame
            
        Returns:
            Dictionary of KPI name to count
        """
        today = pd.Timestamp.now().normalize()
        next_week = today + pd.Timedelta(days=7)
        
        # Calculate Upcoming Next Week (SIM Start Date within next 7 days)
        upcoming_next_week_count = len(self.df[
            (self.df['SIM Start Date'] >= today) &
            (self.df['SIM Start Date'] <= next_week)
        ])
        
        # Calculate Data Incomplete (SIM Start Date before today but Status is blank)
        data_incomplete_count = len(self.df[
            (self.df['SIM Start Date'] < today) &
            (self.df['Status'].isna() | (self.df['Status'] == ''))
        ])
        
        kpis = {
            'Total Go Live': len(df),
            'Completed': len(df[df['Status'] == 'Completed']),
            'WIP': len(df[df['Status'] == 'WIP']),
            'Unable to Complete': len(df[df['Status'] == 'Unable to Complete']),
            'Upcoming Next Week': upcoming_next_week_count,
            'Data Incomplete': data_incomplete_count
        }
        
        print(f"[DEBUG Regression Processor] KPIs: {kpis}")
        
        return kpis
    
    def filter_by_implementation_type(self, impl_type: str, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter data by implementation type
        
        Args:
            impl_type: Implementation type ('Conquest', 'Buy/Sell', 'Enterprise', 'New Point', 'All')
            df: DataFrame to filter
            
        Returns:
            Filtered DataFrame
        """
        if impl_type == 'All':
            return df.copy()
        else:
            filtered = df[df['Type of Implementation'] == impl_type].copy()
            print(f"[DEBUG Regression Processor] Filtered by {impl_type}: {len(filtered)} records")
            return filtered
    
    def get_regions(self, df: Optional[pd.DataFrame] = None) -> List[str]:
        """Get unique regions from data"""
        if df is None:
            df = self.df

        # Safety check: ensure Region column exists
        if 'Region' not in df.columns:
            print("[DEBUG Regression] 'Region' column missing in DataFrame!")
            return ['All']

        # Normalize regions: strip whitespace, title case
        df['Region'] = df['Region'].astype(str).str.strip().str.title()
        
        # Get unique regions, excluding NaN and empty values
        regions = [r for r in df['Region'].unique() if r and r != 'Nan']
        
        # If no regions found, return default
        if not regions:
            print("[DEBUG Regression] No regions found, returning default")
            return ['All']

        # Sort regions alphabetically, then add 'All' at the beginning
        sorted_regions = sorted(regions)
        region_options = ['All'] + sorted_regions
        
        print(f"[DEBUG Regression] Regions extracted: {region_options}")
        return region_options

    def get_region_counts(self, kpi_name: str, df: pd.DataFrame) -> Dict[str, int]:
        """
        Get counts by region for a specific KPI
        
        Args:
            kpi_name: KPI name
            df: Filtered DataFrame
            
        Returns:
            Dictionary of region to count
        """
        regions = self.get_regions(df)
        region_counts = {}
        
        today = pd.Timestamp.now().normalize()
        next_week = today + pd.Timedelta(days=7)
        
        for region in regions:
            region_df = df[df['Region'] == region]
            
            if kpi_name == 'Total Go Live':
                count = len(region_df)
            elif kpi_name == 'Upcoming Next Week':
                count = len(self.df[
                    (self.df['Region'] == region) &
                    (self.df['SIM Start Date'] >= today) &
                    (self.df['SIM Start Date'] <= next_week)
                ])
            elif kpi_name == 'Data Incomplete':
                count = len(self.df[
                    (self.df['Region'] == region) &
                    (self.df['SIM Start Date'] < today) &
                    (self.df['Status'].isna() | (self.df['Status'] == ''))
                ])
            else:
                count = len(region_df[region_df['Status'] == kpi_name])
            
            region_counts[region] = count
        
        return region_counts
    
    def filter_by_region(self, region: str, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter data by region
        
        Args:
            region: Region name or 'All'
            df: DataFrame to filter
            
        Returns:
            Filtered DataFrame
        """
        if region == 'All' or region == 'All Regions':
            return df.copy()
        else:
            filtered = df[df['Region'] == region].copy()
            print(f"[DEBUG Regression Processor] Filtered by region {region}: {len(filtered)} records")
            return filtered
    
    def get_display_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare DataFrame for display
        
        Args:
            df: Filtered DataFrame
            
        Returns:
            Display-ready DataFrame
        """
        display_df = df[[
            'Dealership Name',
            'Go Live Date',
            'SIM Start Date',
            'Assignee',
            'Region',
            'Status'
        ]].copy()
        
        # Format dates
        display_df['Go Live Date'] = pd.to_datetime(display_df['Go Live Date']).dt.strftime('%d-%b-%Y')
        display_df['SIM Start Date'] = pd.to_datetime(display_df['SIM Start Date']).dt.strftime('%d-%b-%Y')
        
        # Replace None/NaN in Status with empty string
        display_df['Status'] = display_df['Status'].fillna('')
        
        print(f"[DEBUG Regression Processor] Display DataFrame ready: {len(display_df)} records")
        
        return display_df


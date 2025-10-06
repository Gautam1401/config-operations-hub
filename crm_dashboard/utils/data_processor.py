"""
CRM Configuration Dashboard - Data Processor
Handles all data transformations, filtering, and KPI calculations
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from crm_dashboard.config.settings import UPCOMING_WEEK_DAYS
from shared.column_utils import find_column, has_column


class CRMDataProcessor:
    """Process and analyze CRM configuration data"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize processor with CRM data
        
        Args:
            df: Raw CRM DataFrame
        """
        self.df = df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare data: convert dates, calculate days to go live, create combined fields"""

        print(f"[DEBUG CRMDataProcessor] _prepare_data - Columns BEFORE prep: {self.df.columns.tolist()}")

        # Clean column names
        self.df.columns = self.df.columns.str.strip()

        # Use fuzzy column matching
        go_live_col = find_column(self.df, 'Go Live Date')
        dealer_name_col = find_column(self.df, 'Dealer Name')
        dealer_id_col = find_column(self.df, 'Dealer ID')

        # Convert Go Live Date to datetime
        self.df[go_live_col] = pd.to_datetime(self.df[go_live_col], errors='coerce')

        # Standardize to 'Go Live Date' column name
        if go_live_col != 'Go Live Date':
            self.df.rename(columns={go_live_col: 'Go Live Date'}, inplace=True)

        # Calculate Days to Go Live
        today = pd.Timestamp(datetime.now().date())
        self.df['Days to Go Live'] = (self.df['Go Live Date'] - today).dt.days

        # Create Dealership Name (Dealer Name + Dealer ID)
        if has_column(self.df, 'Dealership Name'):
            # Already exists, don't overwrite
            pass
        else:
            # Create from Dealer Name + Dealer ID
            self.df['Dealership Name'] = self.df[dealer_name_col].astype(str) + ' (' + self.df[dealer_id_col].astype(str) + ')'
        
        # Add Month and Year columns for filtering
        self.df['Month'] = self.df['Go Live Date'].dt.month
        self.df['Year'] = self.df['Go Live Date'].dt.year
        self.df['Month Name'] = self.df['Go Live Date'].dt.strftime('%B %Y')

        # Mark upcoming week
        self.df['Is Upcoming Week'] = self.df['Days to Go Live'].apply(
            lambda x: 0 <= x <= UPCOMING_WEEK_DAYS
        )

        # Add 'Go Live Status' column if it doesn't exist (needed for Data Incorrect logic)
        if 'Go Live Status' not in self.df.columns:
            # Default to None - can be populated from Excel if column exists
            self.df['Go Live Status'] = None

        # Add 'Configuration Type' column if it doesn't exist
        if 'Configuration Type' not in self.df.columns:
            # Map from 'Configuration Status' if it exists
            if 'Configuration Status' in self.df.columns:
                self.df['Configuration Type'] = self.df['Configuration Status']
            else:
                self.df['Configuration Type'] = None

        # Calculate derived statuses for each sub-tab
        self._calculate_configuration_status()
        self._calculate_pre_go_live_status()
        self._calculate_go_live_testing_status()
        
        print(f"[DEBUG CRMDataProcessor] _prepare_data - Columns AFTER prep: {self.df.columns.tolist()}")
        print(f"[DEBUG CRMDataProcessor] Total records: {len(self.df)}")
    
    def _calculate_configuration_status(self):
        """Calculate Configuration status based on Configuration Type"""
        
        def get_config_status(row):
            # Data Incorrect: Go Live Status is 'Rolled out' but Configuration Type is blank/None
            if pd.notna(row['Go Live Status']) and row['Go Live Status'] == 'Rolled out':
                if pd.isna(row['Configuration Type']) or row['Configuration Type'] == '':
                    return 'Data Incorrect'
            
            # Not Configured
            if pd.isna(row['Configuration Type']) or row['Configuration Type'] == '':
                return 'Not Configured'
            
            # Standard or Copy
            if row['Configuration Type'] in ['Standard', 'Copy']:
                return row['Configuration Type']
            
            # Implementation -> treat as Copy
            if row['Configuration Type'] == 'Implementation':
                return 'Copy'
            
            return 'Not Configured'
        
        self.df['Configuration Status'] = self.df.apply(get_config_status, axis=1)
        print(f"[DEBUG CRMDataProcessor] Configuration Status calculated")
    
    def _calculate_pre_go_live_status(self):
        """Calculate Pre Go Live status based on Domain Updated and Set Up Check"""
        
        def get_pre_go_live_status(row):
            # Data Incorrect: Go Live Status is 'Rolled out' but both checks are blank/None
            if pd.notna(row['Go Live Status']) and row['Go Live Status'] == 'Rolled out':
                if (pd.isna(row['Domain Updated']) or row['Domain Updated'] == '') and \
                   (pd.isna(row['Set Up Check']) or row['Set Up Check'] == ''):
                    return 'Data Incorrect'
            
            domain = row['Domain Updated']
            setup = row['Set Up Check']
            
            # Both blank/NA -> Not started
            if (pd.isna(domain) or domain == '') and (pd.isna(setup) or setup == ''):
                return None
            
            # Both Yes -> GTG
            if domain == 'Yes' and setup == 'Yes':
                return 'GTG'
            
            # Both No -> Fail
            if domain == 'No' and setup == 'No':
                return 'Fail'
            
            # One Yes, one No -> Partial
            if (domain == 'Yes' and setup == 'No') or (domain == 'No' and setup == 'Yes'):
                return 'Partial'
            
            # One Yes, one blank -> Partial
            if (domain == 'Yes' and (pd.isna(setup) or setup == '')) or \
               ((pd.isna(domain) or domain == '') and setup == 'Yes'):
                return 'Partial'
            
            # One No, one blank -> Partial
            if (domain == 'No' and (pd.isna(setup) or setup == '')) or \
               ((pd.isna(domain) or domain == '') and setup == 'No'):
                return 'Partial'
            
            return None
        
        self.df['Pre Go Live Status'] = self.df.apply(get_pre_go_live_status, axis=1)
        print(f"[DEBUG CRMDataProcessor] Pre Go Live Status calculated")
    
    def _calculate_go_live_testing_status(self):
        """Calculate Go Live Testing status based on test results with weighted scoring"""
        
        def get_go_live_testing_status(row):
            # Skip if go-live date is in the future
            if row['Days to Go Live'] > 0:
                return None
            
            # Data Incorrect: Go Live Status is 'Rolled out' but all tests are blank/None
            if pd.notna(row['Go Live Status']) and row['Go Live Status'] == 'Rolled out':
                if all(pd.isna(row[field]) or row[field] == '' 
                       for field in ['Sample ADF', 'Inbound Email', 'Outbound Email', 'Data Migration']):
                    return 'Data Incorrect'
            
            sample_adf = row['Sample ADF']
            inbound = row['Inbound Email']
            outbound = row['Outbound Email']
            data_mig = row['Data Migration']
            
            # All blank/NA -> Not tested
            if all(pd.isna(val) or val == '' for val in [sample_adf, inbound, outbound, data_mig]):
                return None
            
            # All Yes or No Issues -> GTG
            if all(val in ['Yes', 'No Issues'] for val in [sample_adf, inbound, outbound, data_mig] if pd.notna(val) and val != ''):
                return 'GTG'
            
            # Check for blockers (Sample ADF or Data Migration have issues)
            has_blocker = False
            has_non_blocker = False
            
            if sample_adf == 'Issues Found':
                has_blocker = True
            if data_mig == 'Issues Found':
                has_blocker = True
            if inbound == 'Issues Found':
                has_non_blocker = True
            if outbound == 'Issues Found':
                has_non_blocker = True
            
            # Determine status
            if has_blocker and has_non_blocker:
                return 'Go Live Blocker & Non-Blocker'
            elif has_blocker:
                return 'Go Live Blocker'
            elif has_non_blocker:
                return 'Non-Blocker'
            
            # All failed
            if all(val == 'Issues Found' for val in [sample_adf, inbound, outbound, data_mig] if pd.notna(val) and val != ''):
                return 'Fail'
            
            return None
        
        self.df['Go Live Testing Status'] = self.df.apply(get_go_live_testing_status, axis=1)
        print(f"[DEBUG CRMDataProcessor] Go Live Testing Status calculated")
    
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
            filtered = self.df[
                (self.df['Month'] == today.month) & 
                (self.df['Year'] == today.year)
            ].copy()
        elif filter_type == 'next_month':
            next_month = today.month + 1 if today.month < 12 else 1
            next_year = today.year if today.month < 12 else today.year + 1
            filtered = self.df[
                (self.df['Month'] == next_month) & 
                (self.df['Year'] == next_year)
            ].copy()
        elif filter_type == 'ytd':
            filtered = self.df[self.df['Year'] == today.year].copy()
        else:
            filtered = self.df.copy()
        
        print(f"[DEBUG CRMDataProcessor] Filtered by {filter_type}: {len(filtered)} records")
        return filtered
    
    def filter_by_region(self, region: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Filter data by region"""
        if df is None:
            df = self.df
        
        filtered = df[df['Region'] == region].copy()
        print(f"[DEBUG CRMDataProcessor] Filtered by region '{region}': {len(filtered)} records")
        return filtered
    
    def get_regions(self, df: Optional[pd.DataFrame] = None) -> List[str]:
        """Get unique regions from data"""
        if df is None:
            df = self.df
        return sorted(df['Region'].unique().tolist())

    
    def get_configuration_kpis(self, df: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """Get Configuration KPI counts"""
        if df is None:
            df = self.df
        
        kpis = {
            'Go Lives': len(df),  # Total go-lives
            'Standard': len(df[df['Configuration Status'] == 'Standard']),
            'Copy': len(df[df['Configuration Status'] == 'Copy']),
            'Not Configured': len(df[df['Configuration Status'] == 'Not Configured']),
            'Data Incorrect': len(df[df['Configuration Status'] == 'Data Incorrect']),
        }
        
        print(f"[DEBUG CRMDataProcessor] Configuration KPIs: {kpis}")
        return kpis
    
    def get_pre_go_live_kpis(self, df: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """Get Pre Go Live KPI counts"""
        if df is None:
            df = self.df
        
        # Checks Completed = records where Pre Go Live Assignee is not blank
        checks_completed = len(df[df['Pre Go Live Assignee'].notna() & (df['Pre Go Live Assignee'] != '')])
        
        kpis = {
            'Checks Completed': checks_completed,
            'GTG': len(df[df['Pre Go Live Status'] == 'GTG']),
            'Partial': len(df[df['Pre Go Live Status'] == 'Partial']),
            'Fail': len(df[df['Pre Go Live Status'] == 'Fail']),
            'Data Incorrect': len(df[df['Pre Go Live Status'] == 'Data Incorrect']),
        }
        
        print(f"[DEBUG CRMDataProcessor] Pre Go Live KPIs: {kpis}")
        return kpis
    
    def get_go_live_testing_kpis(self, df: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """Get Go Live Testing KPI counts"""
        if df is None:
            df = self.df
        
        # Tests Completed = records where Go Live Testing Assignee is not blank AND not future go-live
        tests_completed = len(df[
            (df['Go Live Testing Assignee'].notna()) & 
            (df['Go Live Testing Assignee'] != '') &
            (df['Days to Go Live'] <= 0)
        ])
        
        kpis = {
            'Tests Completed': tests_completed,
            'GTG': len(df[df['Go Live Testing Status'] == 'GTG']),
            'Go Live Blocker': len(df[df['Go Live Testing Status'].str.contains('Go Live Blocker', na=False)]),
            'Non-Blocker': len(df[df['Go Live Testing Status'].str.contains('Non-Blocker', na=False)]),
            'Fail': len(df[df['Go Live Testing Status'] == 'Fail']),
            'Data Incorrect': len(df[df['Go Live Testing Status'] == 'Data Incorrect']),
        }
        
        print(f"[DEBUG CRMDataProcessor] Go Live Testing KPIs: {kpis}")
        return kpis
    
    def get_region_counts(self, status_field: str, status_value: str, df: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """
        Get counts by region for a specific status
        
        Args:
            status_field: Field name (e.g., 'Configuration Status')
            status_value: Status value to filter by
            df: DataFrame to use
            
        Returns:
            Dict mapping region to count
        """
        if df is None:
            df = self.df
        
        # Handle special cases for Go Live Testing
        if 'Blocker' in status_value or 'Non-Blocker' in status_value:
            filtered = df[df[status_field].str.contains(status_value, na=False)]
        else:
            filtered = df[df[status_field] == status_value]
        
        region_counts = {}
        for region in self.get_regions(df):
            count = len(filtered[filtered['Region'] == region])
            region_counts[region] = count
        
        print(f"[DEBUG CRMDataProcessor] Region counts for {status_field}={status_value}: {region_counts}")
        return region_counts
    
    def get_display_dataframe(self, sub_tab: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Get DataFrame formatted for display in table
        
        Args:
            sub_tab: 'configuration', 'pre_go_live', or 'go_live_testing'
            df: DataFrame to format (uses self.df if None)
            
        Returns:
            pd.DataFrame: Formatted data for display
        """
        if df is None:
            df = self.df
        
        print(f"[DEBUG CRMDataProcessor] get_display_dataframe - Current columns: {df.columns.tolist()}")
        
        # Determine assignee column based on sub-tab
        assignee_col_map = {
            'configuration': 'Configuration Assignee',
            'pre_go_live': 'Pre Go Live Assignee',
            'go_live_testing': 'Go Live Testing Assignee',
        }
        
        status_col_map = {
            'configuration': 'Configuration Status',
            'pre_go_live': 'Pre Go Live Status',
            'go_live_testing': 'Go Live Testing Status',
        }
        
        assignee_col = assignee_col_map.get(sub_tab, 'Configuration Assignee')
        status_col = status_col_map.get(sub_tab, 'Configuration Status')
        
        # Select columns
        display_cols = [
            'Dealership Name',
            'Go Live Date',
            'Days to Go Live',
            'Implementation Type',
            'Region',
            assignee_col,
            status_col,
        ]
        
        # Check if all columns exist
        missing_cols = [col for col in display_cols if col not in df.columns]
        if missing_cols:
            print(f"[ERROR CRMDataProcessor] Missing columns: {missing_cols}")
            display_cols = [col for col in display_cols if col in df.columns]
        
        display_df = df[display_cols].copy()
        
        # Rename assignee and status columns to standard names
        display_df = display_df.rename(columns={
            assignee_col: 'Assignee',
            status_col: 'Status',
        })
        
        # Format Go Live Date
        display_df['Go Live Date'] = display_df['Go Live Date'].dt.strftime('%d-%b-%Y')
        
        # Format Days to Go Live: Show "Rolled Out" for negative values
        display_df['Days to Go Live'] = display_df['Days to Go Live'].apply(
            lambda x: "Rolled Out" if x < 0 else str(int(x))
        )
        
        print(f"[DEBUG CRMDataProcessor] Display DataFrame ready: {len(display_df)} records")
        
        return display_df

"""
CRM Analytics Calculator
Calculates all analytics metrics for CRM dashboard
"""

import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime


class CRMAnalyticsCalculator:
    """Calculate analytics metrics for CRM dashboard"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize calculator with CRM data
        
        Args:
            df: CRM DataFrame with all columns
        """
        self.df = df
        
    def get_configuration_analytics(self, filtered_df: pd.DataFrame) -> Dict:
        """
        Calculate Configuration analytics
        
        Returns:
            Dictionary with all configuration metrics
        """
        # Total records
        total = len(filtered_df)
        
        # Configuration Status breakdown
        config_status = filtered_df['Configuration Status'].value_counts(dropna=False)
        
        # In Scope (Standard + Copy)
        in_scope = config_status.get('Standard', 0) + config_status.get('Copy', 0)
        
        # Out of Scope (Not Configured)
        out_of_scope = config_status.get('Not Configured', 0)
        
        # Data Incorrect
        data_incorrect = config_status.get('Data Incorrect', 0)
        
        # None (not started)
        not_started = config_status.get(None, 0)
        
        # Completion rate (In Scope / Total excluding None)
        total_excluding_none = total - not_started
        completion_rate = (in_scope / total_excluding_none * 100) if total_excluding_none > 0 else 0
        
        # Configuration Type Distribution
        standard = config_status.get('Standard', 0)
        copy = config_status.get('Copy', 0)
        standard_pct = (standard / in_scope * 100) if in_scope > 0 else 0
        copy_pct = (copy / in_scope * 100) if in_scope > 0 else 0
        
        # Regional breakdown
        regional_data = self._get_regional_breakdown(filtered_df, 'Configuration Status')
        
        # Out of Scope by Region
        out_of_scope_by_region = {}
        for region in filtered_df['Region'].unique():
            if pd.notna(region):
                region_df = filtered_df[filtered_df['Region'] == region]
                not_configured = len(region_df[region_df['Configuration Status'] == 'Not Configured'])
                total_region = len(region_df[region_df['Configuration Status'].notna()])
                out_of_scope_by_region[region] = {
                    'count': not_configured,
                    'total': total_region,
                    'percentage': (not_configured / total_region * 100) if total_region > 0 else 0
                }
        
        return {
            'total': total,
            'in_scope': in_scope,
            'out_of_scope': out_of_scope,
            'data_incorrect': data_incorrect,
            'not_started': not_started,
            'completion_rate': completion_rate,
            'standard': standard,
            'copy': copy,
            'standard_pct': standard_pct,
            'copy_pct': copy_pct,
            'regional_data': regional_data,
            'out_of_scope_by_region': out_of_scope_by_region
        }
    
    def get_pre_go_live_analytics(self, filtered_df: pd.DataFrame) -> Dict:
        """
        Calculate Pre Go Live analytics
        
        Returns:
            Dictionary with all pre go live metrics
        """
        # Filter out None and Data Incorrect
        valid_df = filtered_df[
            (filtered_df['Pre Go Live Status'].notna()) &
            (filtered_df['Pre Go Live Status'] != 'Data Incorrect')
        ]
        
        total = len(valid_df)
        
        # Status breakdown
        status_counts = valid_df['Pre Go Live Status'].value_counts()
        gtg = status_counts.get('GTG', 0)
        partial = status_counts.get('Partial', 0)
        fail = status_counts.get('Fail', 0)
        
        # GTG rate
        gtg_rate = (gtg / total * 100) if total > 0 else 0
        
        # Domain Updated vs Set Up Check breakdown
        domain_setup_breakdown = self._get_domain_setup_breakdown(valid_df)
        
        # Regional readiness
        regional_data = self._get_regional_breakdown(valid_df, 'Pre Go Live Status')
        
        # Timeline analysis - stores with <7 days to Go Live and not GTG
        at_risk = valid_df[
            (valid_df['Days to Go Live'] < 7) &
            (valid_df['Days to Go Live'] >= 0) &
            (valid_df['Pre Go Live Status'] != 'GTG')
        ]
        
        return {
            'total': total,
            'gtg': gtg,
            'partial': partial,
            'fail': fail,
            'gtg_rate': gtg_rate,
            'domain_setup_breakdown': domain_setup_breakdown,
            'regional_data': regional_data,
            'at_risk_count': len(at_risk),
            'at_risk_stores': at_risk[['Dealership Name', 'Days to Go Live', 'Pre Go Live Status']].to_dict('records')
        }
    
    def get_go_live_testing_analytics(self, filtered_df: pd.DataFrame) -> Dict:
        """
        Calculate Go Live Testing analytics

        Returns:
            Dictionary with all go live testing metrics
        """
        # Filter out None and Data Incorrect
        valid_df = filtered_df[
            (filtered_df['Go Live Testing Status'].notna()) &
            (filtered_df['Go Live Testing Status'] != 'Data Incorrect')
        ]

        total = len(valid_df)

        # Status breakdown
        status_counts = valid_df['Go Live Testing Status'].value_counts()
        gtg = status_counts.get('GTG', 0)

        # Count blockers and non-blockers (including combined)
        go_live_blocker = status_counts.get('Go Live Blocker', 0)
        non_blocker = status_counts.get('Non-Blocker', 0)
        both = status_counts.get('Go Live Blocker & Non-Blocker', 0)

        total_blockers = go_live_blocker + both
        total_non_blockers = non_blocker + both

        # GTG rate
        gtg_rate = (gtg / total * 100) if total > 0 else 0

        # Test-specific pass rates
        test_pass_rates = self._get_test_pass_rates(valid_df)

        # Weighted score analysis
        score_distribution = self._get_score_distribution(valid_df)

        # Regional data
        regional_data = self._get_regional_breakdown(valid_df, 'Go Live Testing Status')

        # Unable to test (Data Incorrect)
        unable_to_test = len(filtered_df[filtered_df['Go Live Testing Status'] == 'Data Incorrect'])
        unable_by_region = {}
        for region in filtered_df['Region'].unique():
            if pd.notna(region):
                region_df = filtered_df[filtered_df['Region'] == region]
                unable = len(region_df[region_df['Go Live Testing Status'] == 'Data Incorrect'])
                if unable > 0:
                    unable_by_region[region] = unable

        return {
            'total': total,
            'gtg': gtg,
            'blockers': total_blockers,
            'non_blockers': total_non_blockers,
            'go_live_blocker_only': go_live_blocker,
            'non_blocker_only': non_blocker,
            'both_blocker_and_non_blocker': both,
            'gtg_rate': gtg_rate,
            'test_pass_rates': test_pass_rates,
            'score_distribution': score_distribution,
            'regional_data': regional_data,
            'unable_to_test': unable_to_test,
            'unable_by_region': unable_by_region
        }

    def get_assignee_analytics(self, filtered_df: pd.DataFrame) -> Dict:
        """
        Calculate Assignee-level analytics

        Returns:
            Dictionary with assignee performance metrics
        """
        assignee_data = {}

        # Configuration Assignee Analysis
        config_assignees = {}
        for assignee in filtered_df['Configuration Assignee'].unique():
            if pd.notna(assignee) and assignee not in ['Not Under Ready For Configuration', 'Not configured', 'Yet to start', 'Not Configured', 'Handled by EM']:
                assignee_df = filtered_df[filtered_df['Configuration Assignee'] == assignee]

                total = len(assignee_df)
                in_scope = len(assignee_df[assignee_df['Configuration Status'].isin(['Standard', 'Copy'])])
                out_of_scope = len(assignee_df[assignee_df['Configuration Status'] == 'Not Configured'])
                completion_rate = (in_scope / total * 100) if total > 0 else 0

                config_assignees[assignee] = {
                    'total': total,
                    'in_scope': in_scope,
                    'out_of_scope': out_of_scope,
                    'completion_rate': completion_rate
                }

        # Pre Go Live Assignee Analysis
        pregl_assignees = {}
        for assignee in filtered_df['Pre Go Live Assignee'].unique():
            if pd.notna(assignee):
                assignee_df = filtered_df[filtered_df['Pre Go Live Assignee'] == assignee]

                total = len(assignee_df)
                gtg = len(assignee_df[assignee_df['Pre Go Live Status'] == 'GTG'])
                gtg_rate = (gtg / total * 100) if total > 0 else 0

                pregl_assignees[assignee] = {
                    'total': total,
                    'gtg': gtg,
                    'gtg_rate': gtg_rate
                }

        # Go Live Testing Assignee Analysis
        glt_assignees = {}
        for assignee in filtered_df['Go Live Testing Assignee'].unique():
            if pd.notna(assignee) and assignee not in ['Unable to Test', 'Umable to Test']:
                assignee_df = filtered_df[filtered_df['Go Live Testing Assignee'] == assignee]

                # Filter valid testing data
                valid_df = assignee_df[
                    (assignee_df['Go Live Testing Status'].notna()) &
                    (assignee_df['Go Live Testing Status'] != 'Data Incorrect')
                ]

                total = len(valid_df)
                gtg = len(valid_df[valid_df['Go Live Testing Status'] == 'GTG'])
                blockers = len(valid_df[valid_df['Go Live Testing Status'].str.contains('Blocker', na=False)])
                gtg_rate = (gtg / total * 100) if total > 0 else 0

                glt_assignees[assignee] = {
                    'total': total,
                    'gtg': gtg,
                    'blockers': blockers,
                    'gtg_rate': gtg_rate
                }

        return {
            'configuration': config_assignees,
            'pre_go_live': pregl_assignees,
            'go_live_testing': glt_assignees
        }
    
    def _get_regional_breakdown(self, df: pd.DataFrame, status_field: str) -> Dict:
        """Get regional breakdown for a status field"""
        regional_data = {}
        
        for region in df['Region'].unique():
            if pd.notna(region):
                region_df = df[df['Region'] == region]
                total = len(region_df)
                
                status_counts = region_df[status_field].value_counts()
                
                regional_data[region] = {
                    'total': total,
                    'status_counts': status_counts.to_dict()
                }
        
        return regional_data
    
    def _get_domain_setup_breakdown(self, df: pd.DataFrame) -> Dict:
        """Get Domain Updated vs Set Up Check breakdown"""
        both_yes = len(df[
            (df['Pre Go Live Domain Updated'] == 'Yes') &
            (df['Pre Go Live Set Up Check'] == 'Yes')
        ])
        
        domain_only = len(df[
            (df['Pre Go Live Domain Updated'] == 'Yes') &
            (df['Pre Go Live Set Up Check'] != 'Yes')
        ])
        
        setup_only = len(df[
            (df['Pre Go Live Domain Updated'] != 'Yes') &
            (df['Pre Go Live Set Up Check'] == 'Yes')
        ])
        
        neither = len(df[
            (df['Pre Go Live Domain Updated'] != 'Yes') &
            (df['Pre Go Live Set Up Check'] != 'Yes')
        ])
        
        return {
            'both_complete': both_yes,
            'domain_only': domain_only,
            'setup_only': setup_only,
            'neither': neither
        }
    
    def _get_test_pass_rates(self, df: pd.DataFrame) -> Dict:
        """Get pass rates for each test"""
        tests = ['Sample ADF', 'Inbound Email', 'Outbound Email', 'Data Migration']
        pass_rates = {}

        for test in tests:
            if test in df.columns:
                total = len(df[df[test].notna()])
                # Pass = "No Issues" or "Yes"
                passed = len(df[(df[test] == 'No Issues') | (df[test] == 'Yes')])
                pass_rate = (passed / total * 100) if total > 0 else 0
                pass_rates[test] = {
                    'passed': passed,
                    'total': total,
                    'pass_rate': pass_rate
                }

        return pass_rates
    
    def _get_score_distribution(self, df: pd.DataFrame) -> Dict:
        """Get distribution of weighted scores"""
        # Calculate weighted scores for each store
        scores = []

        for _, row in df.iterrows():
            score = 100.0

            # Sample ADF: 40%
            if row.get('Sample ADF') not in ['Yes', 'No Issues']:
                score -= 40

            # Inbound Email: 12.5%
            if row.get('Inbound Email') not in ['Yes', 'No Issues']:
                score -= 12.5

            # Outbound Email: 12.5%
            if row.get('Outbound Email') not in ['Yes', 'No Issues']:
                score -= 12.5

            # Data Migration: 35%
            if row.get('Data Migration') not in ['Yes', 'No Issues']:
                score -= 35

            scores.append(score)

        # Categorize scores
        excellent = sum(1 for s in scores if s >= 90)
        good = sum(1 for s in scores if 75 <= s < 90)
        needs_improvement = sum(1 for s in scores if 60 <= s < 75)
        critical = sum(1 for s in scores if s < 60)

        avg_score = sum(scores) / len(scores) if scores else 0

        return {
            'excellent': excellent,
            'good': good,
            'needs_improvement': needs_improvement,
            'critical': critical,
            'average_score': avg_score
        }

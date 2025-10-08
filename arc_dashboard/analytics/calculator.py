"""
ARC Analytics Calculator
Calculates all analytics metrics for ARC Configuration dashboard
"""

import pandas as pd
from typing import Dict, List
from datetime import datetime


class ARCAnalyticsCalculator:
    """Calculate analytics metrics for ARC Configuration dashboard"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize calculator with ARC data
        
        Args:
            df: ARC DataFrame with all columns
        """
        self.df = df
        
    def get_configuration_analytics(self, filtered_df: pd.DataFrame) -> Dict:
        """
        Calculate Configuration Status analytics
        
        Returns:
            Dictionary with all configuration metrics
        """
        total = len(filtered_df)
        
        # Service Status
        service_completed = len(filtered_df[filtered_df['Service Status'] == 'Completed'])
        service_wip = len(filtered_df[filtered_df['Service Status'] == 'WIP'])
        service_not_configured = len(filtered_df[filtered_df['Service Status'] == 'Not Configured'])

        # Parts Status
        parts_completed = len(filtered_df[filtered_df['Parts Status'] == 'Completed'])
        parts_wip = len(filtered_df[filtered_df['Parts Status'] == 'WIP'])
        parts_not_configured = len(filtered_df[filtered_df['Parts Status'] == 'Not Configured'])

        # Accounting Status
        accounting_completed = len(filtered_df[filtered_df['Accounting Status'] == 'Completed'])
        accounting_wip = len(filtered_df[filtered_df['Accounting Status'] == 'WIP'])
        accounting_not_configured = len(filtered_df[filtered_df['Accounting Status'] == 'Not Configured'])
        
        # Overall completion rates
        service_completion_rate = (service_completed / total * 100) if total > 0 else 0
        parts_completion_rate = (parts_completed / total * 100) if total > 0 else 0
        accounting_completion_rate = (accounting_completed / total * 100) if total > 0 else 0
        
        # Fully configured (all 3 completed)
        fully_configured = len(filtered_df[
            (filtered_df['Service Status'] == 'Completed') &
            (filtered_df['Parts Status'] == 'Completed') &
            (filtered_df['Accounting Status'] == 'Completed')
        ])

        # Not configured at all (all 3 not configured)
        not_configured_all = len(filtered_df[
            (filtered_df['Service Status'] == 'Not Configured') &
            (filtered_df['Parts Status'] == 'Not Configured') &
            (filtered_df['Accounting Status'] == 'Not Configured')
        ])
        
        # Regional breakdown
        regional_data = self._get_regional_breakdown(filtered_df)
        
        return {
            'total': total,
            'service': {
                'completed': service_completed,
                'wip': service_wip,
                'not_configured': service_not_configured,
                'completion_rate': service_completion_rate
            },
            'parts': {
                'completed': parts_completed,
                'wip': parts_wip,
                'not_configured': parts_not_configured,
                'completion_rate': parts_completion_rate
            },
            'accounting': {
                'completed': accounting_completed,
                'wip': accounting_wip,
                'not_configured': accounting_not_configured,
                'completion_rate': accounting_completion_rate
            },
            'fully_configured': fully_configured,
            'not_configured_all': not_configured_all,
            'regional_data': regional_data
        }
    
    def get_timeline_analytics(self, filtered_df: pd.DataFrame) -> Dict:
        """
        Calculate Timeline analytics (Days to Go Live)
        
        Returns:
            Dictionary with timeline metrics
        """
        # Calculate days to go live
        today = pd.Timestamp.now().normalize()
        filtered_df['Days to Go Live'] = (filtered_df['Go Live Date'] - today).dt.days
        
        # Categorize by implementation type
        conquest_df = filtered_df[filtered_df['Type of Implementation'] == 'Conquest']
        buysell_df = filtered_df[filtered_df['Type of Implementation'].isin(['Buy/Sell', 'Buy-Sell'])]
        newpoint_df = filtered_df[filtered_df['Type of Implementation'] == 'New Point']
        
        # On Track / Critical / Escalated logic
        def categorize_status(row):
            days = row['Days to Go Live']
            impl_type = row['Type of Implementation']

            # Handle NA values
            if pd.isna(impl_type) or pd.isna(days):
                return 'Unknown'

            if impl_type == 'Conquest':
                if days > 60:
                    return 'On Track'
                elif days > 30:
                    return 'Critical'
                else:
                    return 'Escalated'
            elif impl_type in ['Buy/Sell', 'Buy-Sell', 'New Point']:
                if days > 15:
                    return 'On Track'
                elif days > 3:
                    return 'Critical'
                else:
                    return 'Escalated'
            return 'Unknown'
        
        filtered_df['Status Category'] = filtered_df.apply(categorize_status, axis=1)
        
        on_track = len(filtered_df[filtered_df['Status Category'] == 'On Track'])
        critical = len(filtered_df[filtered_df['Status Category'] == 'Critical'])
        escalated = len(filtered_df[filtered_df['Status Category'] == 'Escalated'])
        
        # Average days to go live
        avg_days = filtered_df['Days to Go Live'].mean() if len(filtered_df) > 0 else 0
        
        return {
            'on_track': on_track,
            'critical': critical,
            'escalated': escalated,
            'avg_days_to_go_live': avg_days,
            'conquest_count': len(conquest_df),
            'buysell_count': len(buysell_df),
            'newpoint_count': len(newpoint_df)
        }
    
    def get_assignee_analytics(self, filtered_df: pd.DataFrame) -> Dict:
        """
        Calculate Assignee performance analytics
        
        Returns:
            Dictionary with assignee metrics
        """
        assignee_stats = []

        for assignee in filtered_df['Assigned To'].dropna().unique():
            assignee_df = filtered_df[filtered_df['Assigned To'] == assignee]
            
            total = len(assignee_df)
            completed = len(assignee_df[
                (assignee_df['Service Status'] == 'Completed') &
                (assignee_df['Parts Status'] == 'Completed') &
                (assignee_df['Accounting Status'] == 'Completed')
            ])
            wip = len(assignee_df[
                (assignee_df['Service Status'] == 'WIP') |
                (assignee_df['Parts Status'] == 'WIP') |
                (assignee_df['Accounting Status'] == 'WIP')
            ])
            
            completion_rate = (completed / total * 100) if total > 0 else 0
            
            assignee_stats.append({
                'assignee': assignee,
                'total': total,
                'completed': completed,
                'wip': wip,
                'completion_rate': completion_rate
            })
        
        # Sort by completion rate
        assignee_stats = sorted(assignee_stats, key=lambda x: x['completion_rate'], reverse=True)
        
        return {
            'assignee_stats': assignee_stats,
            'total_assignees': len(assignee_stats)
        }
    
    def _get_regional_breakdown(self, filtered_df: pd.DataFrame) -> Dict:
        """Get regional breakdown of configuration status"""
        regional_data = {}
        
        for region in filtered_df['Region'].dropna().unique():
            region_df = filtered_df[filtered_df['Region'] == region]
            
            total = len(region_df)
            completed = len(region_df[
                (region_df['Service Status'] == 'Completed') &
                (region_df['Parts Status'] == 'Completed') &
                (region_df['Accounting Status'] == 'Completed')
            ])
            wip = len(region_df[
                (region_df['Service Status'] == 'WIP') |
                (region_df['Parts Status'] == 'WIP') |
                (region_df['Accounting Status'] == 'WIP')
            ])
            not_configured = len(region_df[
                (region_df['Service Status'] == 'Not Configured') &
                (region_df['Parts Status'] == 'Not Configured') &
                (region_df['Accounting Status'] == 'Not Configured')
            ])
            
            completion_rate = (completed / total * 100) if total > 0 else 0
            
            regional_data[region] = {
                'total': total,
                'completed': completed,
                'wip': wip,
                'not_configured': not_configured,
                'completion_rate': completion_rate
            }
        
        return regional_data

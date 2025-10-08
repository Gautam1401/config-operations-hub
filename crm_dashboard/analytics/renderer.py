"""
CRM Analytics Renderer
Main renderer for analytics tab
"""

import streamlit as st
import pandas as pd
from typing import Dict

from crm_dashboard.analytics.calculator import CRMAnalyticsCalculator
from crm_dashboard.analytics.visualizations import (
    render_metric_cards,
    render_completion_rate_chart,
    render_regional_heatmap,
    render_pie_chart,
    render_out_of_scope_analysis,
    render_test_pass_rates,
    render_score_distribution,
    render_at_risk_stores,
    render_assignee_performance
)


def render_configuration_analytics(calculator: CRMAnalyticsCalculator, filtered_df: pd.DataFrame):
    """Render Configuration Analytics"""
    st.markdown("### 📊 Configuration Analytics")
    
    # Calculate metrics
    metrics = calculator.get_configuration_analytics(filtered_df)
    
    # Key Metrics Cards
    metric_data = {
        "Total Stores": f"{metrics['total']}",
        "In Scope": f"{metrics['in_scope']}",
        "Out of Scope": f"{metrics['out_of_scope']}",
        "Completion Rate": f"{metrics['completion_rate']:.1f}%"
    }
    render_metric_cards(metric_data, "📈 Key Metrics")
    
    st.markdown("---")
    
    # Two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Completion rate chart
        render_completion_rate_chart(metrics)
    
    with col2:
        # Configuration type distribution
        render_pie_chart(
            metrics,
            "📋 Configuration Type Distribution",
            ["Standard", "Copy"],
            ["standard", "copy"],
            ["#3874F2", "#29C46F"]
        )
    
    st.markdown("---")
    
    # Regional performance heatmap
    render_regional_heatmap(metrics['regional_data'], "Configuration Status")
    
    st.markdown("---")
    
    # Out of Scope Analysis
    render_out_of_scope_analysis(metrics['out_of_scope_by_region'])


def render_pre_go_live_analytics(calculator: CRMAnalyticsCalculator, filtered_df: pd.DataFrame):
    """Render Pre Go Live Analytics"""
    st.markdown("### 📊 Pre Go Live Analytics")
    
    # Calculate metrics
    metrics = calculator.get_pre_go_live_analytics(filtered_df)
    
    # Key Metrics Cards
    metric_data = {
        "Total Stores": f"{metrics['total']}",
        "GTG": f"{metrics['gtg']}",
        "Partial": f"{metrics['partial']}",
        "GTG Rate": f"{metrics['gtg_rate']:.1f}%"
    }
    render_metric_cards(metric_data, "📈 Key Metrics")
    
    st.markdown("---")
    
    # Two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        render_pie_chart(
            metrics,
            "📋 Pre Go Live Status Distribution",
            ["GTG", "Partial", "Fail"],
            ["gtg", "partial", "fail"],
            ["#29C46F", "#FFC107", "#F44336"]
        )
    
    with col2:
        # Domain vs Setup breakdown
        domain_setup = metrics['domain_setup_breakdown']
        render_pie_chart(
            domain_setup,
            "🔍 Domain Updated vs Set Up Check",
            ["Both Complete", "Domain Only", "Setup Only", "Neither"],
            ["both_complete", "domain_only", "setup_only", "neither"],
            ["#29C46F", "#3874F2", "#FFC107", "#F44336"]
        )
    
    st.markdown("---")
    
    # Regional performance heatmap
    render_regional_heatmap(metrics['regional_data'], "Pre Go Live Status")
    
    st.markdown("---")
    
    # At-risk stores
    if metrics['at_risk_count'] > 0:
        render_at_risk_stores(metrics['at_risk_stores'])


def render_go_live_testing_analytics(calculator: CRMAnalyticsCalculator, filtered_df: pd.DataFrame):
    """Render Go Live Testing Analytics"""
    st.markdown("### 📊 Go Live Testing Analytics")
    
    # Calculate metrics
    metrics = calculator.get_go_live_testing_analytics(filtered_df)
    
    # Key Metrics Cards
    metric_data = {
        "Total Tested": f"{metrics['total']}",
        "GTG": f"{metrics['gtg']}",
        "Blockers": f"{metrics['blockers']}",
        "GTG Rate": f"{metrics['gtg_rate']:.1f}%"
    }
    render_metric_cards(metric_data, "📈 Key Metrics")
    
    st.markdown("---")
    
    # Two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Test pass rates
        render_test_pass_rates(metrics['test_pass_rates'])
    
    with col2:
        # Score distribution
        render_score_distribution(metrics['score_distribution'])
    
    st.markdown("---")
    
    # Regional performance heatmap
    render_regional_heatmap(metrics['regional_data'], "Go Live Testing Status")
    
    st.markdown("---")
    
    # Unable to Test Analysis
    if metrics['unable_to_test'] > 0:
        st.markdown("#### 🔴 Unable to Test Analysis")
        
        st.warning(f"⚠️ {metrics['unable_to_test']} stores unable to test (Data Incorrect)")
        
        if metrics['unable_by_region']:
            st.markdown("**By Region:**")
            for region, count in sorted(metrics['unable_by_region'].items(), key=lambda x: x[1], reverse=True):
                st.markdown(f"- **{region}**: {count} stores")
            
            st.info("💡 Action: Investigate why these stores have data issues and resolve to enable testing")


def render_assignee_analytics(calculator: CRMAnalyticsCalculator, filtered_df: pd.DataFrame):
    """Render Assignee Analytics"""
    st.markdown("### 👤 Assignee Analytics")

    # Calculate metrics
    metrics = calculator.get_assignee_analytics(filtered_df)

    # Sub-tabs for different assignee categories
    tab1, tab2, tab3 = st.tabs([
        "📋 Configuration",
        "✅ Pre Go Live",
        "🧪 Go Live Testing"
    ])

    with tab1:
        render_assignee_performance(metrics['configuration'], "Configuration")

    with tab2:
        render_assignee_performance(metrics['pre_go_live'], "Pre Go Live")

    with tab3:
        render_assignee_performance(metrics['go_live_testing'], "Go Live Testing")


def render_month_analytics(calculator: CRMAnalyticsCalculator, month_name: str, full_df: pd.DataFrame):
    """Render analytics for a specific month"""
    # Filter data for this month
    month_df = full_df[full_df['Month Name'] == month_name]

    st.markdown(f"### 📅 {month_name}")
    st.info(f"Total stores in {month_name}: **{len(month_df)}**")

    # Sub-tabs for different analytics
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Configuration",
        "✅ Pre Go Live",
        "🧪 Go Live Testing",
        "👤 Assignee"
    ])

    with tab1:
        render_configuration_analytics(calculator, month_df)

    with tab2:
        render_pre_go_live_analytics(calculator, month_df)

    with tab3:
        render_go_live_testing_analytics(calculator, month_df)

    with tab4:
        render_assignee_analytics(calculator, month_df)


def render_ytd_analytics(calculator: CRMAnalyticsCalculator, full_df: pd.DataFrame):
    """Render YTD analytics"""
    st.markdown(f"### 📅 Year to Date (YTD)")
    st.info(f"Total stores YTD: **{len(full_df)}**")

    # Sub-tabs for different analytics
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Configuration",
        "✅ Pre Go Live",
        "🧪 Go Live Testing",
        "👤 Assignee"
    ])

    with tab1:
        render_configuration_analytics(calculator, full_df)

    with tab2:
        render_pre_go_live_analytics(calculator, full_df)

    with tab3:
        render_go_live_testing_analytics(calculator, full_df)

    with tab4:
        render_assignee_analytics(calculator, full_df)


def render_analytics_tab(calculator: CRMAnalyticsCalculator, full_df: pd.DataFrame):
    """
    Main function to render Analytics tab with month-by-month breakdown

    Args:
        calculator: CRMAnalyticsCalculator instance
        full_df: Full DataFrame (not filtered by date)
    """
    st.markdown("## 📈 Analytics Dashboard")

    # Get unique months sorted
    months = sorted(full_df['Month Name'].unique())

    # Create tabs for each month + YTD
    tab_labels = months + ['YTD (Year to Date)']
    tabs = st.tabs(tab_labels)

    # Render each month
    for idx, month in enumerate(months):
        with tabs[idx]:
            render_month_analytics(calculator, month, full_df)

    # Render YTD
    with tabs[-1]:
        render_ytd_analytics(calculator, full_df)

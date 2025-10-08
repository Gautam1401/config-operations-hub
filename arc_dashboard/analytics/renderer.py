"""
ARC Analytics Renderer
Renders the Analytics tab with visualizations and insights
"""

import streamlit as st
import pandas as pd
from .calculator import ARCAnalyticsCalculator


def render_month_analytics(calculator: ARCAnalyticsCalculator, month_name: str, month_df: pd.DataFrame):
    """Render analytics for a specific month"""

    st.markdown(f"### 📅 {month_name}")
    st.info(f"Total dealerships in {month_name}: **{len(month_df)}**")

    # Sub-tabs for different analytics views
    analytics_tabs = st.tabs([
        "📊 Configuration Status",
        "👥 Assignee Performance",
        "🌍 Regional Insights"
    ])

    # Tab 1: Configuration Status
    with analytics_tabs[0]:
        render_configuration_analytics(calculator, month_df, month_name)

    # Tab 2: Assignee Performance
    with analytics_tabs[1]:
        render_assignee_analytics(calculator, month_df, month_name)

    # Tab 3: Regional Insights
    with analytics_tabs[2]:
        render_regional_analytics(calculator, month_df, month_name)


def render_ytd_analytics(calculator: ARCAnalyticsCalculator, full_df: pd.DataFrame):
    """Render YTD analytics"""

    st.markdown(f"### 📅 Year to Date (YTD)")
    st.info(f"Total dealerships YTD: **{len(full_df)}**")

    # Sub-tabs for different analytics views
    analytics_tabs = st.tabs([
        "📊 Configuration Status",
        "👥 Assignee Performance",
        "🌍 Regional Insights"
    ])

    # Tab 1: Configuration Status
    with analytics_tabs[0]:
        render_configuration_analytics(calculator, full_df, "YTD")

    # Tab 2: Assignee Performance
    with analytics_tabs[1]:
        render_assignee_analytics(calculator, full_df, "YTD")

    # Tab 3: Regional Insights
    with analytics_tabs[2]:
        render_regional_analytics(calculator, full_df, "YTD")


def render_analytics_tab(full_df: pd.DataFrame, period_name: str):
    """
    Main function to render Analytics tab with month-by-month breakdown

    Args:
        full_df: Full DataFrame (all months)
        period_name: Not used (kept for compatibility)
    """

    if full_df.empty:
        st.warning("No data available for analytics")
        return

    st.markdown("## 📈 Analytics Dashboard")

    # Initialize calculator
    calculator = ARCAnalyticsCalculator(full_df)

    # Get unique months from data
    full_df['Month Name'] = pd.to_datetime(full_df['Go Live Date']).dt.strftime('%B')
    months = ['September', 'October', 'November']  # Fixed order

    # Create tabs for each month + YTD
    tab_labels = months + ['YTD (All Months)']
    tabs = st.tabs(tab_labels)

    # Render each month
    for idx, month in enumerate(months):
        with tabs[idx]:
            month_df = full_df[full_df['Month Name'] == month]
            render_month_analytics(calculator, month, month_df)

    # Render YTD
    with tabs[-1]:
        render_ytd_analytics(calculator, full_df)


def render_configuration_analytics(calculator, filtered_df, period_name):
    """Render Configuration Status analytics"""
    
    st.subheader(f"📊 Configuration Status Analytics - {period_name}")
    
    metrics = calculator.get_configuration_analytics(filtered_df)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Dealerships", metrics['total'])
    
    with col2:
        st.metric("Fully Configured", metrics['fully_configured'])
    
    with col3:
        st.metric("Not Configured", metrics['not_configured_all'])
    
    with col4:
        overall_rate = (metrics['fully_configured'] / metrics['total'] * 100) if metrics['total'] > 0 else 0
        st.metric("Overall Completion", f"{overall_rate:.1f}%")
    
    st.markdown("---")
    
    # Service, Parts, Accounting breakdown
    st.subheader("Configuration by Module")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔧 Service")
        st.metric("Completed", metrics['service']['completed'])
        st.metric("WIP", metrics['service']['wip'])
        st.metric("Not Configured", metrics['service']['not_configured'])
        st.progress(metrics['service']['completion_rate'] / 100)
        st.caption(f"Completion Rate: {metrics['service']['completion_rate']:.1f}%")
    
    with col2:
        st.markdown("### 🔩 Parts")
        st.metric("Completed", metrics['parts']['completed'])
        st.metric("WIP", metrics['parts']['wip'])
        st.metric("Not Configured", metrics['parts']['not_configured'])
        st.progress(metrics['parts']['completion_rate'] / 100)
        st.caption(f"Completion Rate: {metrics['parts']['completion_rate']:.1f}%")
    
    with col3:
        st.markdown("### 💰 Accounting")
        st.metric("Completed", metrics['accounting']['completed'])
        st.metric("WIP", metrics['accounting']['wip'])
        st.metric("Not Configured", metrics['accounting']['not_configured'])
        st.progress(metrics['accounting']['completion_rate'] / 100)
        st.caption(f"Completion Rate: {metrics['accounting']['completion_rate']:.1f}%")
    
    # Key Insights
    st.markdown("---")
    st.subheader("💡 Key Insights")
    
    insights = []
    
    # Insight 1: Best performing module
    completion_rates = {
        'Service': metrics['service']['completion_rate'],
        'Parts': metrics['parts']['completion_rate'],
        'Accounting': metrics['accounting']['completion_rate']
    }
    best_module = max(completion_rates, key=completion_rates.get)
    insights.append(f"✅ **{best_module}** has the highest completion rate at {completion_rates[best_module]:.1f}%")
    
    # Insight 2: WIP count
    total_wip = metrics['service']['wip'] + metrics['parts']['wip'] + metrics['accounting']['wip']
    if total_wip > 0:
        insights.append(f"⚠️ **{total_wip}** configurations are currently in progress (WIP)")
    
    # Insight 3: Not configured
    if metrics['not_configured_all'] > 0:
        pct = (metrics['not_configured_all'] / metrics['total'] * 100)
        insights.append(f"🔴 **{metrics['not_configured_all']}** dealerships ({pct:.1f}%) are completely not configured")
    
    for insight in insights:
        st.markdown(insight)


def render_assignee_analytics(calculator, filtered_df, period_name):
    """Render Assignee Performance analytics"""
    
    st.subheader(f"👥 Assignee Performance - {period_name}")
    
    metrics = calculator.get_assignee_analytics(filtered_df)
    
    st.metric("Total Assignees", metrics['total_assignees'])
    
    st.markdown("---")
    
    # Assignee performance table
    if metrics['assignee_stats']:
        df_assignees = pd.DataFrame(metrics['assignee_stats'])
        
        # Format the dataframe
        df_display = df_assignees.copy()
        df_display['completion_rate'] = df_display['completion_rate'].apply(lambda x: f"{x:.1f}%")
        df_display.columns = ['Assignee', 'Total', 'Completed', 'WIP', 'Completion Rate']
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
        
        # Top performer
        st.markdown("---")
        st.subheader("🏆 Top Performer")
        
        top_assignee = metrics['assignee_stats'][0]
        st.success(f"**{top_assignee['assignee']}** with {top_assignee['completion_rate']:.1f}% completion rate ({top_assignee['completed']}/{top_assignee['total']} dealerships)")


def render_regional_analytics(calculator, filtered_df, period_name):
    """Render Regional Insights"""
    
    st.subheader(f"🌍 Regional Insights - {period_name}")
    
    metrics = calculator.get_configuration_analytics(filtered_df)
    regional_data = metrics['regional_data']
    
    if not regional_data:
        st.info("No regional data available")
        return
    
    # Convert to DataFrame for display
    df_regional = pd.DataFrame.from_dict(regional_data, orient='index')
    df_regional = df_regional.sort_values('completion_rate', ascending=False)
    df_regional.reset_index(inplace=True)
    df_regional.columns = ['Region', 'Total', 'Completed', 'WIP', 'Not Configured', 'Completion Rate']
    
    # Format completion rate
    df_display = df_regional.copy()
    df_display['Completion Rate'] = df_display['Completion Rate'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Best and worst regions
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Best Performing Region")
        best_region = df_regional.iloc[0]
        st.success(f"**{best_region['Region']}** - {best_region['Completion Rate']:.1f}% completion rate")
    
    with col2:
        st.subheader("⚠️ Needs Attention")
        worst_region = df_regional.iloc[-1]
        st.warning(f"**{worst_region['Region']}** - {worst_region['Completion Rate']:.1f}% completion rate")

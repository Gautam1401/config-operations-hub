"""
Integration Dashboard - Data Table Component
Renders data tables with color-coded status and export functionality
"""

import streamlit as st
import pandas as pd
from typing import Optional

from integration_dashboard.config.settings import STATUS_COLORS


def render_data_table(
    df: pd.DataFrame,
    title: str = "Data Table",
    key_suffix: str = "table"
):
    """
    Render data table with color-coded status and export
    
    Args:
        df: DataFrame to display
        title: Table title
        key_suffix: Unique key suffix for widgets
    """
    
    if df.empty:
        st.info("No data available for the selected filters.")
        return
    
    # Title
    st.markdown(f"### 📋 {title}")
    
    # Summary stats
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**Total Records:** {len(df)}")
    
    with col2:
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"integration_{title.lower().replace(' ', '_')}.csv",
            mime="text/csv",
            key=f"download_{key_suffix}"
        )
    
    # Status breakdown if Status column exists
    if 'Status' in df.columns:
        st.markdown("---")
        render_status_breakdown(df)
        st.markdown("---")
    
    # Display table with color-coded status
    if 'Status' in df.columns:
        # Apply color styling to Status column
        def color_status(val):
            color = STATUS_COLORS.get(val, '#23272F')
            return f'background-color: {color}; color: white; font-weight: bold;'
        
        styled_df = df.style.applymap(
            color_status,
            subset=['Status']
        )
        
        st.dataframe(styled_df, use_container_width=True, height=400)
    else:
        st.dataframe(df, use_container_width=True, height=400)
    
    # Record count
    st.caption(f"Showing {len(df)} records")


def render_status_breakdown(df: pd.DataFrame):
    """
    Render status breakdown summary
    
    Args:
        df: DataFrame with Status column
    """
    
    if 'Status' not in df.columns:
        return
    
    st.markdown("**Status Breakdown:**")
    
    status_counts = df['Status'].value_counts()
    
    # Create columns for status cards
    statuses = ['GTG', 'On Track', 'Critical', 'Escalated']
    available_statuses = [s for s in statuses if s in status_counts.index]
    
    if not available_statuses:
        st.info("No status data available")
        return
    
    cols = st.columns(len(available_statuses))
    
    for idx, status in enumerate(available_statuses):
        count = status_counts[status]
        color = STATUS_COLORS.get(status, '#23272F')
        
        with cols[idx]:
            st.markdown(
                f"""
                <div style="
                    background: {color};
                    color: white;
                    padding: 12px;
                    border-radius: 8px;
                    text-align: center;
                    font-weight: bold;
                ">
                    <div style="font-size: 1.5em;">{count}</div>
                    <div style="font-size: 0.9em;">{status}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


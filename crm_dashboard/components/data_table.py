"""
CRM Configuration Dashboard - Data Table Component
"""

import streamlit as st
import pandas as pd
from crm_dashboard.config.settings import STATUS_COLORS


def render_data_table(df: pd.DataFrame, title: str = "Data Table", key_suffix: str = "", month_key: str = ""):
    """
    Render data table with styling and export

    Args:
        df: DataFrame to display
        title: Table title
        key_suffix: Unique suffix for widget keys
        month_key: Month identifier for unique keys
    """

    if df.empty:
        st.info("No data available for the selected filters")
        return

    st.markdown(f"### 📊 {title}")
    st.markdown(f"**Total Records:** {len(df)}")

    # Export button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"crm_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        key=f"download_btn_{key_suffix}_{month_key}"
    )
    
    # Style the dataframe
    def style_status(val):
        """Apply color to status column"""
        color = STATUS_COLORS.get(val, '#6c757d')
        return f'background-color: {color}; color: white; font-weight: bold;'
    
    # Apply styling if Status column exists
    if 'Status' in df.columns:
        styled_df = df.style.applymap(style_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True, height=400)
    else:
        st.dataframe(df, use_container_width=True, height=400)
    
    # Show summary stats
    render_summary_stats(df)


def render_summary_stats(df: pd.DataFrame):
    """
    Render summary statistics for the data
    
    Args:
        df: DataFrame to summarize
    """
    
    st.markdown("---")
    st.markdown("### 📈 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(df))
    
    with col2:
        if 'Region' in df.columns:
            unique_regions = df['Region'].nunique()
            st.metric("Regions", unique_regions)
        else:
            st.metric("Regions", "N/A")
    
    with col3:
        if 'Status' in df.columns:
            unique_statuses = df['Status'].nunique()
            st.metric("Unique Statuses", unique_statuses)
        else:
            st.metric("Statuses", "N/A")
    
    with col4:
        if 'Assignee' in df.columns:
            unique_assignees = df['Assignee'].nunique()
            st.metric("Assignees", unique_assignees)
        else:
            st.metric("Assignees", "N/A")
    
    # Status breakdown
    if 'Status' in df.columns:
        st.markdown("#### Status Breakdown")
        status_counts = df['Status'].value_counts()
        
        # Create columns for status breakdown
        num_statuses = len(status_counts)
        if num_statuses > 0:
            cols = st.columns(min(num_statuses, 5))
            for idx, (status, count) in enumerate(status_counts.items()):
                col_idx = idx % 5
                with cols[col_idx]:
                    color = STATUS_COLORS.get(status, '#6c757d')
                    st.markdown(
                        f"""
                        <div style="
                            background-color: {color};
                            color: white;
                            padding: 10px;
                            border-radius: 5px;
                            text-align: center;
                            margin-bottom: 10px;
                        ">
                            <h4 style="margin: 0;">{count}</h4>
                            <p style="margin: 0; font-size: 0.9em;">{status}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


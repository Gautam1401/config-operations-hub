"""
Data Table Component for ARC Dashboard
Displays filtered data in an interactive table with export functionality
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional


def render_data_table(
    df: pd.DataFrame,
    title: str = "Data Table",
    show_export: bool = True,
    export_filename: Optional[str] = None,
    height: int = 400,
    month_key: str = ""
):
    """
    Render an interactive data table with export functionality

    Args:
        df: DataFrame to display
        title: Table title
        show_export: Whether to show export button
        export_filename: Custom filename for export (auto-generated if None)
        height: Table height in pixels
        month_key: Month identifier for unique keys
    """
    
    # Display title and record count
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(title)
    with col2:
        st.metric("Records", len(df))
    
    # Show export button if enabled
    if show_export and len(df) > 0:
        # Generate filename if not provided
        if export_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_filename = f"ARC_Export_{timestamp}.csv"
        
        # Convert to CSV
        csv = df.to_csv(index=False)
        
        # Download button
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=export_filename,
            mime="text/csv",
            key=f"download_{title.replace(' ', '_')}_{month_key}"
        )
    
    # Display table
    if len(df) > 0:
        # Use Streamlit's dataframe with configuration
        st.dataframe(
            df,
            use_container_width=True,
            height=height,
            hide_index=True
        )
    else:
        st.info("No data to display")


def render_filtered_table(
    df: pd.DataFrame,
    filters: dict,
    title: str = "Filtered Data"
):
    """
    Render a table with applied filters displayed
    
    Args:
        df: DataFrame to display
        filters: Dictionary of applied filters
        title: Table title
    """
    
    # Display active filters
    if filters:
        st.markdown("**Active Filters:**")
        filter_cols = st.columns(len(filters))
        for idx, (filter_name, filter_value) in enumerate(filters.items()):
            with filter_cols[idx]:
                st.info(f"{filter_name}: {filter_value}")
    
    # Render table
    render_data_table(df, title=title)


def render_summary_stats(df: pd.DataFrame):
    """
    Render summary statistics for the data
    
    Args:
        df: DataFrame to summarize
    """
    
    st.subheader("Summary Statistics")
    
    # Create metrics
    cols = st.columns(4)
    
    with cols[0]:
        st.metric("Total Records", len(df))
    
    with cols[1]:
        if 'Status' in df.columns:
            completed = len(df[df['Status'] == 'Completed'])
            st.metric("Completed", completed)
    
    with cols[2]:
        if 'Status' in df.columns:
            wip = len(df[df['Status'] == 'WIP'])
            st.metric("WIP", wip)
    
    with cols[3]:
        if 'Region' in df.columns:
            regions = df['Region'].nunique()
            st.metric("Regions", regions)


def render_interactive_table(
    df: pd.DataFrame,
    searchable_columns: Optional[list] = None,
    title: str = "Data"
):
    """
    Render an interactive table with search functionality
    
    Args:
        df: DataFrame to display
        searchable_columns: Columns to enable search on
        title: Table title
    """
    
    st.subheader(title)
    
    # Add search box if searchable columns specified
    if searchable_columns:
        search_term = st.text_input(
            "🔍 Search",
            placeholder="Enter search term...",
            key=f"search_{title}"
        )
        
        if search_term:
            # Filter dataframe based on search
            mask = pd.Series([False] * len(df))
            for col in searchable_columns:
                if col in df.columns:
                    mask |= df[col].astype(str).str.contains(search_term, case=False, na=False)
            
            df = df[mask]
            st.info(f"Found {len(df)} matching records")
    
    # Render table
    render_data_table(df, title="", show_export=True)


if __name__ == '__main__':
    # Test data table component
    print("Data Table Component Module")
    print("Run the main dashboard to see these components in action")


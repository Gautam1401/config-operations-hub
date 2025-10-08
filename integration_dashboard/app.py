"""
Integration Dashboard - Main Application
"""

import streamlit as st
import pandas as pd
from typing import Optional
import datetime
import os
import time
from pathlib import Path

from integration_dashboard.data.mock_data import load_integration_data
from integration_dashboard.utils.data_processor import IntegrationDataProcessor
from integration_dashboard.components.data_table import render_data_table
from integration_dashboard.config.settings import (
    DASHBOARD_TITLE,
    DATE_FILTERS,
    USE_MOCK_DATA,
    KPI_COLORS
)
from shared.styles import (
    apply_modern_styles,
    render_modern_header
)



# Dashboard Version
__version__ = "1.1.3"
__last_updated__ = "2025-10-08 15:22:44 IST"

def initialize_session_state():
    """Initialize session state variables for Integration dashboard"""

    if 'integration_date_filter' not in st.session_state:
        st.session_state.integration_date_filter = 'current_month'

    if 'integration_selected_kpi' not in st.session_state:
        st.session_state.integration_selected_kpi = None

    if 'integration_selected_region' not in st.session_state:
        st.session_state.integration_selected_region = None

    if 'integration_data_processor' not in st.session_state:
        st.session_state.integration_data_processor = None

    print(f"[DEBUG Integration] Session State: date_filter={st.session_state.integration_date_filter}, "
          f"KPI={st.session_state.integration_selected_kpi}, "
          f"Region={st.session_state.integration_selected_region}")


def get_excel_last_modified() -> str:
    """Get the last modified time of the Excel file"""
    try:
        from shared.data_paths import get_excel_file_path, INTEGRATION_FILE
        excel_path = get_excel_file_path(INTEGRATION_FILE)

        if excel_path.exists():
            mod_time = os.path.getmtime(excel_path)
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time))
        else:
            return "File not found"
    except Exception as e:
        return f"Error: {str(e)}"


def load_data(force_reload: bool = False) -> IntegrationDataProcessor:
    """Load and process Integration data"""

    # Check if we should use cached data
    if not force_reload and st.session_state.integration_data_processor is not None:
        print("[DEBUG Integration] Using cached data processor")
        return st.session_state.integration_data_processor

    print("[DEBUG Integration] Loading fresh data from Excel")
    df = load_integration_data()
    df.columns = df.columns.str.strip()

    if USE_MOCK_DATA:
        print(f"[DEBUG Integration] Loaded data columns: {df.columns.tolist()}")
        print(f"[DEBUG Integration] Data shape: {df.shape}")

    processor = IntegrationDataProcessor(df)

    # Cache the processor
    st.session_state.integration_data_processor = processor

    return processor


def render_date_filter():
    """Render date filter radio buttons (sub-tabs)"""
    
    st.write("#### 📅 Select Time Period")
    
    filter_options = list(DATE_FILTERS.values())
    filter_keys = list(DATE_FILTERS.keys())
    
    current_idx = filter_keys.index(st.session_state.integration_date_filter) if st.session_state.integration_date_filter in filter_keys else 0
    
    selected_label = st.radio(
        "",
        options=filter_options,
        index=current_idx,
        horizontal=True,
        key="integration_date_filter_radio",
        label_visibility="collapsed"
    )
    
    selected_key = filter_keys[filter_options.index(selected_label)]
    
    if st.session_state.integration_date_filter != selected_key:
        st.session_state.integration_date_filter = selected_key
        st.session_state.integration_selected_kpi = None
        st.session_state.integration_selected_region = None
        print(f"[DEBUG Integration] Date filter changed to: {selected_key}")
        st.rerun()


def render_kpi_cards(kpis: dict):
    """
    Render KPI cards using HTML - NO CODE LEAKS
    Build complete HTML string, then display ONLY with unsafe_allow_html=True
    
    Args:
        kpis: Dictionary of KPI name to count
    """
    
    # Build complete HTML string
    cards_html = '<div class="kpi-row">'
    
    for kpi_name, kpi_value in kpis.items():
        # Get color class for this KPI
        color_class = KPI_COLORS.get(kpi_name, 'kpi-grey')
        
        # Add 'selected' class ONLY if this KPI is selected
        selected_class = 'selected' if kpi_name == st.session_state.integration_selected_kpi else ''
        
        # Build card HTML (compact, no extra whitespace)
        cards_html += f'<div class="kpi-card {color_class} {selected_class}">{kpi_value}<br /><span style="font-size:0.55em;">{kpi_name}</span></div>'
    
    cards_html += '</div>'
    
    # Display ONLY the final HTML - NO CODE LEAKS
    st.markdown(cards_html, unsafe_allow_html=True)


def render_region_buttons(region_counts: dict):
    """
    Render region buttons using HTML with aligned clickable buttons
    
    Args:
        region_counts: Dictionary of region to count
    """
    
    # Filter out regions with 0 count
    active_regions = {region: count for region, count in region_counts.items() if count > 0}
    
    if not active_regions:
        return
    
    # Build region cards HTML
    regions_html = '<div class="region-row">'
    
    for region, count in active_regions.items():
        selected_class = 'selected' if region == st.session_state.integration_selected_region else ''
        regions_html += f'<div class="region-btn {selected_class}">{region} ({count})</div>'
    
    regions_html += '</div>'
    st.markdown(regions_html, unsafe_allow_html=True)
    
    # Handle button clicks using Streamlit columns
    cols = st.columns(len(active_regions))
    for idx, region in enumerate(active_regions.keys()):
        with cols[idx]:
            if st.button(f"{region}", key=f"integration_region_btn_{region}"):
                st.session_state.integration_selected_region = region
                st.rerun()


def handle_kpi_click(kpis: dict):
    """Handle KPI card clicks using buttons"""
    
    cols = st.columns(len(kpis))
    
    for idx, (kpi_name, count) in enumerate(kpis.items()):
        with cols[idx]:
            if st.button(f"{kpi_name}", key=f"integration_kpi_btn_{kpi_name}", help=f"Click to view {kpi_name} details"):
                if st.session_state.integration_selected_kpi != kpi_name:
                    st.session_state.integration_selected_kpi = kpi_name
                    st.session_state.integration_selected_region = None
                    print(f"[DEBUG Integration] KPI clicked: {kpi_name}")
                    st.rerun()


def handle_region_click(region_counts: dict):
    """Handle region card clicks using buttons"""
    
    active_regions = {region: count for region, count in region_counts.items() if count > 0}
    
    if not active_regions:
        return
    
    cols = st.columns(len(active_regions))
    
    for idx, (region, count) in enumerate(active_regions.items()):
        with cols[idx]:
            if st.button(f"{region}", key=f"integration_region_btn_{region}", help=f"Click to view {region} details"):
                st.session_state.integration_selected_region = region
                print(f"[DEBUG Integration] Region clicked: {region}")
                st.rerun()


def render_data_tab(processor: IntegrationDataProcessor):
    """Render Data tab with sub-tabs"""

    # Show Excel last modified time and reload button
    col1, col2 = st.columns([3, 1])
    with col1:
        last_modified = get_excel_last_modified()
        st.caption(f"📄 Excel last modified: **{last_modified}**")
    with col2:
        if st.button("🔄 Reload Latest Data", help="Reload data from Excel file"):
            st.session_state.integration_data_processor = None
            st.session_state.integration_selected_kpi = None
            st.session_state.integration_selected_region = None
            st.success("✅ Data reloaded successfully!")
            st.rerun()

    st.markdown("---")

    render_date_filter()

    # Filter by date range using exact calendar month logic
    filtered_df = processor.filter_by_date_range(st.session_state.integration_date_filter)
    
    st.markdown("---")
    
    # Get KPIs
    kpis = processor.get_kpis(filtered_df)
    
    # Render KPI cards - NO CODE LEAKS, only final HTML
    render_kpi_cards(kpis)
    
    # Handle KPI clicks
    handle_kpi_click(kpis)
    
    # Show region banners if KPI is selected
    if st.session_state.integration_selected_kpi:
        st.markdown("---")
        st.write("### 📍 Select Region")
        
        # Get region counts
        if st.session_state.integration_selected_kpi == 'Total Go Lives':
            region_counts = {region: len(filtered_df[filtered_df['Region'] == region]) 
                           for region in processor.get_regions(filtered_df)}
        elif st.session_state.integration_selected_kpi == 'Upcoming Week':
            # Get upcoming week data and count by region
            upcoming_df = processor.get_upcoming_week_data()
            region_counts = {region: len(upcoming_df[upcoming_df['Region'] == region]) 
                           for region in processor.get_regions(processor.df)}
        else:
            region_counts = processor.get_region_counts(
                st.session_state.integration_selected_kpi,
                filtered_df
            )
        
        # Render region buttons - NO CODE LEAKS, only final HTML
        render_region_buttons(region_counts)
        
        # Show table if region is selected
        if st.session_state.integration_selected_region:
            st.markdown("---")
            
            # Filter by region
            if st.session_state.integration_selected_kpi == 'Upcoming Week':
                # Use upcoming week data
                upcoming_df = processor.get_upcoming_week_data()
                region_filtered_df = processor.filter_by_region(st.session_state.integration_selected_region, upcoming_df)
            else:
                region_filtered_df = processor.filter_by_region(st.session_state.integration_selected_region, filtered_df)
                
                if st.session_state.integration_selected_kpi != 'Total Go Lives':
                    region_filtered_df = region_filtered_df[
                        region_filtered_df['Status'] == st.session_state.integration_selected_kpi
                    ]
            
            display_df = processor.get_display_dataframe(region_filtered_df)
            
            render_data_table(
                display_df,
                title=f"{st.session_state.integration_selected_kpi} - {st.session_state.integration_selected_region}",
                key_suffix="integration"
            )
        else:
            st.info("👆 Click a region banner above to view detailed data")
    else:
        st.info("👆 Click a KPI card above to view regional breakdown")


def render_analytics_tab():
    """Render Analytics tab (placeholder)"""
    
    st.markdown("### 📈 Analytics")
    st.info("👷 Analytics tab coming soon!")
    
    st.markdown("""
    **Planned Analytics Features:**
    - Integration trends over time
    - Vendor list update completion rates
    - Implementation type distribution
    - Regional performance comparison
    - PEM/Director workload distribution
    - Days to Go Live analysis
    """)


def render_integration_dashboard():
    """Main function to render Integration dashboard"""
    
    # Apply modern styles
    apply_modern_styles()
    
    # Initialize session state
    initialize_session_state()
    
    # Load data
    with st.spinner("Loading Integration data..."):
        processor = load_data()
    
    # Render modern header
    render_modern_header("Integration Dashboard", "https://img.icons8.com/?size=512&id=7819&format=png")
    
    # Main tabs
    tab1, tab2 = st.tabs(["📊 Data", "📈 Analytics"])
    
    with tab1:
        render_data_tab(processor)
    
    with tab2:
        render_analytics_tab()


# For standalone testing
if __name__ == "__main__":
    st.set_page_config(
        page_title="Integration Dashboard",
        page_icon="🔗",
        layout="wide"
    )
    
    render_integration_dashboard()

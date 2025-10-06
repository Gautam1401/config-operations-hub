"""
ARC Configuration Dashboard - Main Application
Interactive dashboard for visualizing and managing ARC Configuration KPIs
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from arc_dashboard.config.settings import *
from arc_dashboard.data.mock_data import generate_mock_data
from arc_dashboard.data.sharepoint_loader import load_data_from_sharepoint
from arc_dashboard.utils.data_processor import ARCDataProcessor
from arc_dashboard.components.kpi_cards import (
    render_kpi_grid,
    render_breakdown_cards,
    render_region_banners
)
from arc_dashboard.components.data_table import render_data_table, render_summary_stats


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

# Page config moved to main hub - only set when running standalone
# Page config - only set when running standalone
try:
    st.set_page_config(
        page_title=DASHBOARD_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except:
    pass  # Already configured by parent app

    # ============================================================================
    # SESSION STATE INITIALIZATION
    # ============================================================================
    
def initialize_session_state():
    """Initialize session state variables"""
    if 'selected_kpi' not in st.session_state:
        st.session_state.selected_kpi = None
    if 'selected_region' not in st.session_state:
        st.session_state.selected_region = None
    if 'selected_lob' not in st.session_state:
        st.session_state.selected_lob = None
    if 'date_filter' not in st.session_state:
        st.session_state.date_filter = 'current_month'
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False


# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(use_mock: bool = True):
    """
    Load data from SharePoint or mock data
    
    Args:
        use_mock: Whether to use mock data
        
    Returns:
        ARCDataProcessor: Data processor instance with loaded data
    """
    if use_mock:
        df = generate_mock_data(MOCK_DATA_ROWS)
    else:
        # Load from SharePoint
        df = load_data_from_sharepoint(SHAREPOINT_CONFIG)
        if df is None:
            st.warning("Failed to load from SharePoint, using mock data")
            df = generate_mock_data(MOCK_DATA_ROWS)
    
    # Return ARCDataProcessor instance
    return ARCDataProcessor(df)


# ============================================================================
# CALLBACK FUNCTIONS
# ============================================================================

def on_kpi_click(kpi_name: str):
    """Handle KPI card click"""
    st.session_state.selected_kpi = kpi_name
    st.session_state.selected_region = None  # Reset region selection


def on_region_click(region: str):
    """Handle region banner click"""
    st.session_state.selected_region = region


def on_breakdown_click(category: str):
    """Handle breakdown card click"""
    st.session_state.selected_lob = category
    st.session_state.selected_region = None  # Reset region selection


def reset_filters():
    """Reset all filters"""
    st.session_state.selected_kpi = None
    st.session_state.selected_region = None
    st.session_state.selected_lob = None


# ============================================================================
# UI RENDERING FUNCTIONS
# ============================================================================

def render_header():
    """Render dashboard header"""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.title(f"📊 {DASHBOARD_TITLE}")
        st.markdown(f"*{COMPANY_NAME} - Internal Use*")
    
    with col2:
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()


def render_sidebar(processor: ARCDataProcessor):
    """Render sidebar with filters and controls"""
    
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # Date filter
        st.subheader("Date Range")
        date_filter = st.radio(
            "Select Period",
            options=['current_month', 'next_month', 'ytd'],
            format_func=lambda x: DATE_FILTERS[x],
            key='date_filter_radio'
        )
        st.session_state.date_filter = date_filter
        
        st.divider()
        
        # Data source info
        st.subheader("📁 Data Source")
        if USE_MOCK_DATA:
            st.info("Using Mock Data")
        else:
            st.success("Connected to SharePoint")
        
        st.divider()
        
        # Active filters
        st.subheader("🔍 Active Filters")
        if st.session_state.selected_kpi:
            st.write(f"**KPI:** {st.session_state.selected_kpi}")
        if st.session_state.selected_lob:
            st.write(f"**LOB:** {st.session_state.selected_lob}")
        if st.session_state.selected_region:
            st.write(f"**Region:** {st.session_state.selected_region}")
        
        if st.session_state.selected_kpi or st.session_state.selected_lob:
            if st.button("🔄 Reset Filters", use_container_width=True):
                reset_filters()
                st.rerun()
        
        st.divider()
        
        # Statistics
        st.subheader("📊 Quick Stats")
        kpis = processor.get_kpi_counts()
        for kpi_name, kpi_value in kpis.items():
            st.metric(kpi_name, kpi_value)


def render_data_tab(processor: ARCDataProcessor):
    """Render the Data tab with interactive drill-down"""
    
    # Apply date filter
    filtered_df = processor.filter_by_date_range(st.session_state.date_filter)
    
    # Get KPIs for filtered data
    kpis = processor.get_kpi_counts(filtered_df)
    
    # Render top-level KPI cards
    st.subheader("📈 Key Performance Indicators")
    render_kpi_grid(kpis, KPI_COLORS, on_click=on_kpi_click)
    
    st.divider()
    
    # Show selected KPI
    if st.session_state.selected_kpi:
        st.info(f"📌 Selected: **{st.session_state.selected_kpi}**")
    
    # Determine which data to use for regions
    if st.session_state.selected_kpi:
        st.subheader(f"🔍 Drill-down: {st.session_state.selected_kpi}")
        
        # Filter data based on selected KPI
        if st.session_state.selected_kpi == 'Total Go Live':
            kpi_filtered_df = filtered_df
        elif st.session_state.selected_kpi in ['Completed', 'WIP', 'Not Configured']:
            kpi_filtered_df = processor.filter_by_status(
                st.session_state.selected_kpi,
                filtered_df
            )
        
        # Show breakdown cards for Completed and WIP
        if st.session_state.selected_kpi in ['Completed', 'WIP', 'Not Configured']:
            breakdown = processor.get_lob_breakdown(
                st.session_state.selected_kpi,
                filtered_df
            )
            render_breakdown_cards(
                breakdown,
                KPI_COLORS,
                f"{st.session_state.selected_kpi} by Module",
                on_click=on_breakdown_click
            )
            
            st.divider()
        
        # Apply LOB filter if selected
        if st.session_state.selected_lob and st.session_state.selected_lob != 'Any':
            kpi_filtered_df = processor.filter_by_lob(
                st.session_state.selected_lob,
                kpi_filtered_df
            )
    else:
        # No KPI selected, use all filtered data
        kpi_filtered_df = filtered_df
    
    # Show region cards (always visible)
    regions = processor.get_regions(kpi_filtered_df)
    
    # Calculate region counts
    region_counts = {}
    for region in regions:
        if region == "All":
            region_counts[region] = len(kpi_filtered_df)
        else:
            region_counts[region] = len(kpi_filtered_df[kpi_filtered_df["Region"] == region])
    
    render_region_banners(
        regions,
        st.session_state.selected_region,
        on_click=on_region_click,
        counts=region_counts
    )
    
    st.divider()
    
    # If region is selected, show data table
    if st.session_state.selected_region:
        region_filtered_df = processor.filter_by_region(
            st.session_state.selected_region,
            kpi_filtered_df
        )
        
        # Get display dataframe
        display_df = processor.get_display_dataframe(region_filtered_df)
        
        # Render table
        render_data_table(
            display_df,
            title=f"Data: {st.session_state.selected_region}",
            show_export=True
        )


def render_analytics_tab():
    """Render the Analytics tab (placeholder for future)"""
    
    st.subheader("📊 Analytics")
    st.info("Analytics visualizations will be added here in future updates.")
    
    # Placeholder for future charts
    st.markdown("""
    ### Planned Analytics:
    - 📈 Trend analysis over time
    - 🗺️ Geographic distribution
    - 📊 LOB performance comparison
    - ⏱️ Time-to-completion metrics
    - 👥 Team performance analytics
    """)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def render_arc_dashboard():
    """Render the ARC Configuration dashboard (for embedding in main hub)"""
    # Initialize session state
    initialize_session_state()
    
    # Load data
    processor = load_data()
    
    # Sidebar
    render_sidebar(processor)
    
    # Main content area
    tab1, tab2 = st.tabs(["📊 Data", "📈 Analytics"])
    
    with tab1:
        render_data_tab(processor)
    
    with tab2:
        render_analytics_tab()
    
    

    """Main application entry point"""
    
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Load data
    with st.spinner("Loading data..."):
        processor = load_data(use_mock=USE_MOCK_DATA)
        st.session_state.data_loaded = True
    
    # Render sidebar
    render_sidebar(processor)
    
    # Main content tabs
    tab1, tab2 = st.tabs(["📋 Data", "📊 Analytics"])
    
    with tab1:
        render_data_tab(processor)
    
    with tab2:
        render_analytics_tab()
    
    # Footer
    st.divider()
    st.markdown(
        f"<div style='text-align: center; color: gray;'>"
        f"ARC Configuration Dashboard | {COMPANY_NAME} | "
        f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        f"</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()


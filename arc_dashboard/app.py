"""
ARC Configuration Dashboard - Main Application (IMPROVED VERSION)
Interactive dashboard for visualizing and managing ARC Configuration KPIs

IMPROVEMENTS:
1. Unique keys for all widgets
2. Column cleaning immediately after data load
3. Improved drilldown flow (table only shows when both KPI and region selected)
4. Reset region/lob when clicking new KPI
5. Debug print statements
6. Module breakdown only after region selected
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
from shared.styles import (
    apply_modern_styles,
    render_modern_header
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

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
    
    # DEBUG: Print session state during development
    if USE_MOCK_DATA:
        print(f"[DEBUG] Session State: KPI={st.session_state.selected_kpi}, "
              f"Region={st.session_state.selected_region}, "
              f"LOB={st.session_state.selected_lob}")


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
    
    # IMPROVEMENT #2: Clean column names immediately after loading
    df.columns = df.columns.str.strip()
    df.rename(columns={'Line of Business': 'Module'}, inplace=True)
    
    # DEBUG: Print columns during development
    if USE_MOCK_DATA:
        print(f"[DEBUG] Loaded data columns: {df.columns.tolist()}")
        print(f"[DEBUG] Data shape: {df.shape}")
    
    # Return ARCDataProcessor instance
    return ARCDataProcessor(df)


# ============================================================================
# CALLBACK FUNCTIONS
# ============================================================================

def on_kpi_click(kpi_name: str):
    """
    Handle KPI card click
    IMPROVEMENT #3 & #4: Reset region and LOB when clicking new KPI
    """
    if st.session_state.selected_kpi != kpi_name:
        st.session_state.selected_kpi = kpi_name
        st.session_state.selected_region = None  # Reset region
        st.session_state.selected_lob = None  # Reset LOB
        print(f"[DEBUG] KPI clicked: {kpi_name}, reset region and LOB")


def on_region_click(region: str):
    """Handle region banner click"""
    st.session_state.selected_region = region
    print(f"[DEBUG] Region clicked: {region}")


def on_breakdown_click(category: str):
    """Handle breakdown card click"""
    st.session_state.selected_lob = category
    print(f"[DEBUG] LOB clicked: {category}")


def reset_filters():
    """Reset all filters"""
    st.session_state.selected_kpi = None
    st.session_state.selected_region = None
    st.session_state.selected_lob = None
    print("[DEBUG] All filters reset")


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
        # IMPROVEMENT #1: Unique key for refresh button
        if st.button("🔄 Refresh Data", key="btn_refresh_header", use_container_width=True):
            st.cache_data.clear()
            st.rerun()


def render_sidebar(processor: ARCDataProcessor):
    """Render sidebar with filters and controls"""
    
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # Date filter - IMPROVEMENT #1: Unique key
        st.subheader("Date Range")
        date_filter = st.radio(
            "Select Period",
            options=['current_month', 'next_month', 'ytd'],
            format_func=lambda x: DATE_FILTERS[x],
            key='sidebar_date_filter_radio'  # Unique key
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
            st.write(f"**Module:** {st.session_state.selected_lob}")
        if st.session_state.selected_region:
            st.write(f"**Region:** {st.session_state.selected_region}")
        
        if st.session_state.selected_kpi or st.session_state.selected_lob or st.session_state.selected_region:
            # IMPROVEMENT #1: Unique key for reset button
            if st.button("🔄 Reset Filters", key="btn_reset_sidebar", use_container_width=True):
                reset_filters()
                st.rerun()
        
        st.divider()
        
        # Statistics
        st.subheader("📊 Quick Stats")
        kpis = processor.get_kpi_counts()
        for kpi_name, kpi_value in kpis.items():
            st.metric(kpi_name, kpi_value)




# ============================================================================
# UI RENDERING FUNCTIONS
# ============================================================================

def render_kpi_cards_arc(kpis: dict):
    """Render KPI cards with aligned buttons"""
    # Build KPI cards HTML
    cards_html = '<div class="kpi-row">'
    
    kpi_colors = {
        'Total Go Live': 'kpi-accent',
        'Completed': 'kpi-success',
        'WIP': 'kpi-warning',
        'Not Configured': 'kpi-grey'
    }
    
    for kpi_name, kpi_value in kpis.items():
        color_class = kpi_colors.get(kpi_name, 'kpi-grey')
        selected_class = 'selected' if kpi_name == st.session_state.selected_kpi else ''
        cards_html += f'<div class="kpi-card {color_class} {selected_class}">{kpi_value}<br /><span style="font-size:0.55em;">{kpi_name}</span></div>'
    
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
    
    # Handle button clicks
    cols = st.columns(len(kpis))
    for idx, kpi_name in enumerate(kpis.keys()):
        with cols[idx]:
            if st.button(f"{kpi_name}", key=f"arc_kpi_btn_{kpi_name}"):
                on_kpi_click(kpi_name)
                st.rerun()


def render_region_cards_arc(region_counts: dict):
    """Render region cards with aligned buttons"""
    active_regions = {region: count for region, count in region_counts.items() if count > 0}
    
    if not active_regions:
        return
    
    st.markdown("#### 🌍 Regions")
    
    # Build regions HTML
    regions_html = '<div class="region-row">'
    
    for region, count in active_regions.items():
        selected_class = 'selected' if region == st.session_state.selected_region else ''
        regions_html += f'<div class="region-btn {selected_class}">{region} ({count})</div>'
    
    regions_html += '</div>'
    st.markdown(regions_html, unsafe_allow_html=True)
    
    # Handle button clicks
    cols = st.columns(len(active_regions))
    for idx, region in enumerate(active_regions.keys()):
        with cols[idx]:
            if st.button(f"{region}", key=f"arc_region_btn_{region}"):
                on_region_click(region)
                st.rerun()


def render_lob_cards_arc(lob_counts: dict):
    """Render LOB breakdown cards with aligned buttons"""
    active_lobs = {lob: count for lob, count in lob_counts.items() if count > 0}
    
    if not active_lobs:
        return
    
    st.markdown("#### 📊 Line of Business")
    
    # Build LOB HTML
    lob_html = '<div class="region-row">'
    
    for lob, count in active_lobs.items():
        selected_class = 'selected' if lob == st.session_state.selected_lob else ''
        lob_html += f'<div class="region-btn {selected_class}">{lob} ({count})</div>'
    
    lob_html += '</div>'
    st.markdown(lob_html, unsafe_allow_html=True)
    
    # Handle button clicks
    cols = st.columns(len(active_lobs))
    for idx, lob in enumerate(active_lobs.keys()):
        with cols[idx]:
            if st.button(f"{lob}", key=f"arc_lob_btn_{lob}"):
                on_breakdown_click(lob)
                st.rerun()


def render_data_tab(processor: ARCDataProcessor):
    """
    Render the Data tab with interactive drill-down
    IMPROVEMENT #3: Table only shows when both KPI and region selected
    IMPROVEMENT #6: Module breakdown only after region selected
    """
    
    # Month Filter at the top
    st.markdown("### 📅 Select Month")
    
    today = pd.Timestamp.today().normalize()
    current_month_str = today.strftime("%B %Y")
    next_month_dt = today + pd.DateOffset(months=1)
    next_month_str = next_month_dt.strftime("%B %Y")
    ytd_str = "YTD (Year to Date)"
    
    month_option = st.radio(
        "Select Month",
        [current_month_str, next_month_str, ytd_str],
        index=0,
        horizontal=True,
        key="arc_month_filter",
        label_visibility="collapsed"
    )
    
    # Map selection to filter type
    if month_option == current_month_str:
        st.session_state.date_filter = 'current_month'
    elif month_option == next_month_str:
        st.session_state.date_filter = 'next_month'
    else:  # YTD
        st.session_state.date_filter = 'ytd'
    
    st.markdown("---")
    
    # Apply date filter
    filtered_df = processor.filter_by_date_range(st.session_state.date_filter)
    
    # Get KPIs for filtered data
    kpis = processor.get_kpi_counts(filtered_df)
    
    # Render top-level KPI cards
    st.subheader("📈 Key Performance Indicators")
    render_kpi_cards_arc(kpis)
    
    st.divider()
    
    # Show selected KPI
    if st.session_state.selected_kpi:
        st.info(f"📌 Selected: **{st.session_state.selected_kpi}**")
        
        # Filter data based on selected KPI
        if st.session_state.selected_kpi == 'Total Go Live':
            kpi_filtered_df = filtered_df
        elif st.session_state.selected_kpi in ['Completed', 'WIP', 'Not Configured']:
            kpi_filtered_df = processor.filter_by_status(
                st.session_state.selected_kpi,
                filtered_df
            )
        else:
            kpi_filtered_df = filtered_df
    else:
        # No KPI selected, use all filtered data
        kpi_filtered_df = filtered_df
    
    # Show region cards (always visible after KPI selection or for all data)
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
    
    # IMPROVEMENT #3 & #6: Show table and module breakdown ONLY when region is selected
    if st.session_state.selected_region:
        region_filtered_df = processor.filter_by_region(
            st.session_state.selected_region,
            kpi_filtered_df
        )
        
        # IMPROVEMENT #6: Show module breakdown ONLY after region is selected
        if st.session_state.selected_kpi and st.session_state.selected_kpi in ['Completed', 'WIP', 'Not Configured']:
            st.subheader(f"🔍 {st.session_state.selected_kpi} by Module - {st.session_state.selected_region}")
            breakdown = processor.get_lob_breakdown(
                st.session_state.selected_kpi,
                region_filtered_df
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
            region_filtered_df = processor.filter_by_lob(
                st.session_state.selected_lob,
                region_filtered_df
            )
        
        # Get display dataframe
        display_df = processor.get_display_dataframe(region_filtered_df)
        
        # Render table
        render_data_table(
            display_df,
            title=f"Data: {st.session_state.selected_region}",
            show_export=True
        )
    else:
        # No region selected - show instruction
        if st.session_state.selected_kpi:
            st.info("👆 Click a region banner above to view detailed data")


def render_analytics_tab():
    """Render the Analytics tab (placeholder for future)"""
    
    st.subheader("📊 Analytics")
    st.info("Analytics visualizations will be added here in future updates.")


    # Placeholder for future charts
    st.markdown("""
    ### Planned Analytics:
    - 📈 Trend analysis over time
    - 🗺️ Geographic distribution
    - 📊 Module performance comparison
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
    processor = load_data(use_mock=USE_MOCK_DATA)
    
    # Sidebar
    render_sidebar(processor)
    
    # Main content area
    tab1, tab2 = st.tabs(["📊 Data", "📈 Analytics"])
    
    with tab1:
        render_data_tab(processor)
    
    with tab2:
        render_analytics_tab()


def main():
    """Main application entry point (for standalone mode)"""
    
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

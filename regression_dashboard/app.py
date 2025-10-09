"""
Regression Testing Dashboard - Main Application
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import calendar

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from regression_dashboard.config.settings import *
from regression_dashboard.data.mock_data import generate_mock_data
from regression_dashboard.data.excel_loader import load_regression_data_from_excel
from regression_dashboard.utils.data_processor import RegressionDataProcessor
from shared.styles import apply_modern_styles


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================


# Dashboard Version
__version__ = "1.1.8"
__last_updated__ = "2025-10-08 17:59:23 IST"

def initialize_session_state():
    """Initialize session state variables"""
    if 'regression_selected_kpi' not in st.session_state:
        st.session_state.regression_selected_kpi = None
    if 'regression_selected_impl_type' not in st.session_state:
        st.session_state.regression_selected_impl_type = 'All'
    if 'regression_selected_region' not in st.session_state:
        st.session_state.regression_selected_region = None
    if 'regression_date_filter' not in st.session_state:
        st.session_state.regression_date_filter = 'current_month'


# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data(ttl=300, show_spinner=False)  # Cache for 5 minutes - auto-refresh
def load_data(use_mock: bool = False):
    """
    Load data from Excel file (Stores Checklist sheet) or mock data

    Args:
        use_mock: Whether to use mock data (default: False - use real Excel data)

    Returns:
        RegressionDataProcessor: Data processor instance with loaded data
    """
    if use_mock:
        df = generate_mock_data(MOCK_DATA_ROWS)
    else:
        # Load from Excel file - "Stores Checklist" sheet
        try:
            df = load_regression_data_from_excel()
        except Exception as e:
            st.error(f"Failed to load Excel file: {e}")
            st.warning("Using mock data instead")
            df = generate_mock_data(MOCK_DATA_ROWS)

    # Clean column names
    df.columns = df.columns.str.strip()

    # DEBUG: Print columns
    print(f"[DEBUG Regression] Loaded data columns: {df.columns.tolist()}")
    print(f"[DEBUG Regression] Data shape: {df.shape}")

    processor = RegressionDataProcessor(df)
    return processor


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_kpi_cards(kpis: dict, month_key: str = ""):
    """Render KPI cards with aligned buttons"""
    # Build KPI cards HTML
    cards_html = '<div class="kpi-row">'

    for kpi_name, kpi_value in kpis.items():
        color_class = KPI_COLORS.get(kpi_name, 'kpi-grey')
        selected_class = 'selected' if kpi_name == st.session_state.regression_selected_kpi else ''
        cards_html += f'<div class="kpi-card {color_class} {selected_class}">{kpi_value}<br /><span style="font-size:0.55em;">{kpi_name}</span></div>'

    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # Handle button clicks
    cols = st.columns(len(kpis))
    for idx, kpi_name in enumerate(kpis.keys()):
        with cols[idx]:
            if st.button(f"{kpi_name}", key=f"regression_kpi_btn_{kpi_name}_{month_key}"):
                st.session_state.regression_selected_kpi = kpi_name
                st.session_state.regression_selected_region = None
                st.rerun()


def render_implementation_type_pills(impl_types: list, current_selection: str, month_key: str = ""):
    """Render implementation type pill selectors"""
    st.markdown("#### 🏷️ Type of Implementation")

    # Build pills HTML
    pills_html = '<div class="impl-type-row">'

    for impl_type in impl_types:
        selected_class = 'selected' if impl_type == current_selection else ''
        pills_html += f'<div class="impl-type-btn {selected_class}">{impl_type}</div>'

    pills_html += '</div>'
    st.markdown(pills_html, unsafe_allow_html=True)

    # Handle button clicks
    cols = st.columns(len(impl_types))
    for idx, impl_type in enumerate(impl_types):
        with cols[idx]:
            if st.button(f"{impl_type}", key=f"regression_impl_btn_{impl_type}_{month_key}"):
                st.session_state.regression_selected_impl_type = impl_type
                st.session_state.regression_selected_region = None
                st.rerun()


def render_region_buttons(region_counts: dict, month_key: str = ""):
    """Render region buttons"""
    active_regions = {region: count for region, count in region_counts.items() if count > 0}

    if not active_regions:
        st.info("No data available for the selected filters.")
        return

    st.markdown("#### 🌍 Regions")

    # Build regions HTML
    regions_html = '<div class="region-row">'

    # Add "All Regions" option
    all_count = sum(active_regions.values())
    selected_class = 'selected' if st.session_state.regression_selected_region == 'All Regions' else ''
    regions_html += f'<div class="region-btn {selected_class}">All Regions ({all_count})</div>'

    for region, count in active_regions.items():
        selected_class = 'selected' if region == st.session_state.regression_selected_region else ''
        regions_html += f'<div class="region-btn {selected_class}">{region} ({count})</div>'

    regions_html += '</div>'
    st.markdown(regions_html, unsafe_allow_html=True)

    # Handle button clicks
    all_regions = ['All Regions'] + list(active_regions.keys())
    cols = st.columns(len(all_regions))
    for idx, region in enumerate(all_regions):
        with cols[idx]:
            if st.button(f"{region}", key=f"regression_region_btn_{region}_{month_key}"):
                st.session_state.regression_selected_region = region
                st.rerun()


def render_data_table(df: pd.DataFrame, month_key: str = ""):
    """Render data table"""
    st.markdown("#### 📋 Data Table")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Export button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"regression_testing_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        key=f"download_regression_{month_key}"
    )


# ============================================================================
# MAIN TABS
# ============================================================================

def get_dynamic_months_regression(df: pd.DataFrame):
    """
    Dynamically detect all months from data and return tab labels, keys, and full names

    Returns:
        tuple: (tab_labels, month_keys, month_names)
    """
    # Get unique year-month combinations from data (use copy to avoid modifying original)
    temp_df = df.copy()

    # Filter out rows with NaN/null dates
    temp_df = temp_df[temp_df['Go Live Date'].notna()]

    if len(temp_df) == 0:
        # No valid dates, return empty lists with just YTD
        return ['YTD'], ['ytd'], ['YTD (All Months)']

    temp_df['YearMonth'] = temp_df['Go Live Date'].dt.to_period('M')
    unique_months = sorted(temp_df['YearMonth'].dropna().unique())

    tab_labels = []
    month_keys = []
    month_names = []

    for ym in unique_months:
        month_num = int(ym.month)  # Convert to int for calendar lookup
        month_full = calendar.month_name[month_num]  # January, February, etc.
        month_abbr = calendar.month_abbr[month_num]  # Jan, Feb, etc.

        tab_labels.append(month_abbr)
        month_keys.append(month_full.lower())
        month_names.append(month_full)

    # Add YTD at the end
    tab_labels.append('YTD')
    month_keys.append('ytd')
    month_names.append('YTD (All Months)')

    return tab_labels, month_keys, month_names


def render_month_data_regression(processor: RegressionDataProcessor, month_key: str, month_name: str):
    """Render data for a specific month"""

    # Apply date filter
    filtered_df = processor.filter_by_date_range(month_key)

    st.info(f"Total dealerships in {month_name}: **{len(filtered_df)}**")

    st.markdown("---")
    
    # Get KPIs for filtered data
    kpis = processor.get_kpis(filtered_df)
    
    # Render KPI cards
    st.markdown("### 📊 Key Performance Indicators")
    render_kpi_cards(kpis, month_key)

    st.markdown("---")

    # Render Implementation Type pills
    render_implementation_type_pills(IMPLEMENTATION_TYPES, st.session_state.regression_selected_impl_type, month_key)
    
    st.markdown("---")
    
    # Filter by implementation type
    impl_filtered_df = processor.filter_by_implementation_type(
        st.session_state.regression_selected_impl_type,
        filtered_df
    )
    
    # Show selected KPI and Type
    if st.session_state.regression_selected_kpi:
        st.info(f"📌 Selected: **{st.session_state.regression_selected_kpi}** | Type: **{st.session_state.regression_selected_impl_type}**")
        
        # Get region counts
        if st.session_state.regression_selected_kpi == 'Total Go Live':
            region_counts = {region: len(impl_filtered_df[impl_filtered_df['Region'] == region]) 
                           for region in processor.get_regions(impl_filtered_df)}
        elif st.session_state.regression_selected_kpi == 'Upcoming Next Week':
            # Use upcoming week data
            today = pd.Timestamp.now().normalize()
            next_week = today + pd.Timedelta(days=7)
            upcoming_df = processor.df[
                (processor.df['SIM Start Date'] >= today) &
                (processor.df['SIM Start Date'] <= next_week)
            ]
            upcoming_filtered = processor.filter_by_implementation_type(
                st.session_state.regression_selected_impl_type,
                upcoming_df
            )
            region_counts = {region: len(upcoming_filtered[upcoming_filtered['Region'] == region]) 
                           for region in processor.get_regions(processor.df)}
        elif st.session_state.regression_selected_kpi == 'Data Incomplete':
            # Use data incomplete logic
            today = pd.Timestamp.now().normalize()
            incomplete_df = processor.df[
                (processor.df['SIM Start Date'] < today) &
                (processor.df['Status'].isna() | (processor.df['Status'] == ''))
            ]
            incomplete_filtered = processor.filter_by_implementation_type(
                st.session_state.regression_selected_impl_type,
                incomplete_df
            )
            region_counts = {region: len(incomplete_filtered[incomplete_filtered['Region'] == region]) 
                           for region in processor.get_regions(processor.df)}
        else:
            region_counts = processor.get_region_counts(
                st.session_state.regression_selected_kpi,
                impl_filtered_df
            )
        
        # Render region buttons
        render_region_buttons(region_counts, month_key)
        
        # Show table when region is selected
        if st.session_state.regression_selected_region:
            st.markdown("---")
            
            # Filter by region
            if st.session_state.regression_selected_kpi == 'Upcoming Next Week':
                region_filtered_df = processor.filter_by_region(st.session_state.regression_selected_region, upcoming_filtered)
            elif st.session_state.regression_selected_kpi == 'Data Incomplete':
                region_filtered_df = processor.filter_by_region(st.session_state.regression_selected_region, incomplete_filtered)
            else:
                region_filtered_df = processor.filter_by_region(st.session_state.regression_selected_region, impl_filtered_df)
                
                if st.session_state.regression_selected_kpi != 'Total Go Live':
                    region_filtered_df = region_filtered_df[
                        region_filtered_df['Status'] == st.session_state.regression_selected_kpi
                    ]
            
            # Prepare display dataframe
            display_df = processor.get_display_dataframe(region_filtered_df)

            # Render table
            render_data_table(display_df, month_key)


def render_data_tab(processor: RegressionDataProcessor):
    """Render Data tab with dynamic month tabs"""

    # Get dynamic months from data
    tab_labels, month_keys, month_names = get_dynamic_months_regression(processor.df)

    # Create month tabs
    month_tabs = st.tabs(tab_labels)

    for idx, (tab, month_key, month_name) in enumerate(zip(month_tabs, month_keys, month_names)):
        with tab:
            render_month_data_regression(processor, month_key, month_name)


def render_analytics_tab():
    """Render the Analytics tab (stub)"""
    st.markdown("### 📈 Analytics")
    st.info("👷 Analytics tab coming soon!")
    
    st.markdown("""
    **Planned Features:**
    - Trend analysis
    - Performance metrics
    - Regional comparisons
    - Status distribution charts
    """)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def render_regression_dashboard():
    """Render the Regression Testing dashboard (for embedding in main hub)"""
    # Initialize session state
    initialize_session_state()
    
    # Load data
    processor = load_data(USE_MOCK_DATA)
    
    # Create sub-tabs
    tab1, tab2 = st.tabs(["📊 Data", "📈 Analytics"])
    
    with tab1:
        render_data_tab(processor)
    
    with tab2:
        render_analytics_tab()


if __name__ == "__main__":
    st.set_page_config(
        page_title=DASHBOARD_TITLE,
        page_icon=DASHBOARD_ICON,
        layout="wide"
    )
    
    apply_modern_styles()
    render_regression_dashboard()


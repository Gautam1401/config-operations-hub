"""
CRM Configuration Dashboard - Main Application (Modern Design)
"""

import streamlit as st
import pandas as pd
from typing import Optional
import datetime

from crm_dashboard.data.mock_data import load_crm_data
from crm_dashboard.utils.data_processor import CRMDataProcessor
from crm_dashboard.components.data_table import render_data_table
from crm_dashboard.config.settings import (
    DASHBOARD_TITLE,
    DATE_FILTERS,
    SUB_TABS,
    USE_MOCK_DATA
)
from shared.styles import (
    apply_modern_styles,
    render_modern_header,
    render_upcoming_week_alert
)


def initialize_session_state():
    """Initialize session state variables for CRM dashboard"""
    
    if 'crm_date_filter' not in st.session_state:
        st.session_state.crm_date_filter = 'current_month'
    
    if 'crm_sub_tab' not in st.session_state:
        st.session_state.crm_sub_tab = 'configuration'
    
    if 'crm_selected_kpi' not in st.session_state:
        st.session_state.crm_selected_kpi = None
    
    if 'crm_selected_region' not in st.session_state:
        st.session_state.crm_selected_region = None
    
    print(f"[DEBUG CRM] Session State: date_filter={st.session_state.crm_date_filter}, "
          f"sub_tab={st.session_state.crm_sub_tab}, "
          f"KPI={st.session_state.crm_selected_kpi}, "
          f"Region={st.session_state.crm_selected_region}")


@st.cache_data(ttl=300, show_spinner=False)
def load_data() -> CRMDataProcessor:
    """Load and process CRM data"""

    try:
        df = load_crm_data()
        df.columns = df.columns.str.strip()

        print(f"[DEBUG CRM] Loaded data columns: {df.columns.tolist()}")
        print(f"[DEBUG CRM] Data shape: {df.shape}")

        processor = CRMDataProcessor(df)
        return processor
    except Exception as e:
        st.error(f"❌ Error loading CRM data: {str(e)}")
        print(f"[ERROR CRM] Failed to load data: {e}")
        import traceback
        traceback.print_exc()
        raise


def render_date_filter():
    """Render date filter radio buttons"""
    
    st.write("#### 📅 Select Time Period")
    
    filter_options = list(DATE_FILTERS.values())
    filter_keys = list(DATE_FILTERS.keys())
    
    current_idx = filter_keys.index(st.session_state.crm_date_filter) if st.session_state.crm_date_filter in filter_keys else 0
    
    selected_label = st.radio(
        "",
        options=filter_options,
        index=current_idx,
        horizontal=True,
        key="crm_date_filter_radio",
        label_visibility="collapsed"
    )
    
    selected_key = filter_keys[filter_options.index(selected_label)]
    
    if st.session_state.crm_date_filter != selected_key:
        st.session_state.crm_date_filter = selected_key
        st.session_state.crm_selected_kpi = None
        st.session_state.crm_selected_region = None
        print(f"[DEBUG CRM] Date filter changed to: {selected_key}")
        st.rerun()


def render_sub_tab_selector():
    """Render sub-tab selector"""
    
    st.write("#### 🗂️ Select Category")
    
    tab_options = list(SUB_TABS.values())
    tab_keys = list(SUB_TABS.keys())
    
    current_idx = tab_keys.index(st.session_state.crm_sub_tab) if st.session_state.crm_sub_tab in tab_keys else 0
    
    selected_label = st.radio(
        "",
        options=tab_options,
        index=current_idx,
        horizontal=True,
        key="crm_sub_tab_radio",
        label_visibility="collapsed"
    )
    
    selected_key = tab_keys[tab_options.index(selected_label)]
    
    if st.session_state.crm_sub_tab != selected_key:
        st.session_state.crm_sub_tab = selected_key
        st.session_state.crm_selected_kpi = None
        st.session_state.crm_selected_region = None
        print(f"[DEBUG CRM] Sub-tab changed to: {selected_key}")
        st.rerun()


def handle_kpi_click(kpis: dict):
    """Handle KPI card clicks using buttons"""
    
    cols = st.columns(len(kpis))
    
    for idx, (kpi_name, count) in enumerate(kpis.items()):
        with cols[idx]:
            if st.button(f"Select {kpi_name}", key=f"crm_kpi_btn_{kpi_name}", help=f"Click to view {kpi_name} details"):
                if st.session_state.crm_selected_kpi != kpi_name:
                    st.session_state.crm_selected_kpi = kpi_name
                    st.session_state.crm_selected_region = None
                    print(f"[DEBUG CRM] KPI clicked: {kpi_name}")
                    st.rerun()


def handle_region_click(region_counts: dict):
    """Handle region card clicks using buttons"""
    
    active_regions = {region: count for region, count in region_counts.items() if count > 0}
    
    if not active_regions:
        return
    
    cols = st.columns(len(active_regions))
    
    for idx, (region, count) in enumerate(active_regions.items()):
        with cols[idx]:
            if st.button(f"Select {region}", key=f"crm_region_btn_{region}", help=f"Click to view {region} details"):
                st.session_state.crm_selected_region = region
                print(f"[DEBUG CRM] Region clicked: {region}")
                st.rerun()




# ============================================================================
# UI RENDERING FUNCTIONS
# ============================================================================

def render_kpi_cards_crm(kpis: dict, kpi_type: str):
    """Render KPI cards with aligned buttons"""
    # Build KPI cards HTML
    cards_html = '<div class="kpi-row">'
    
    kpi_colors = {
        # Configuration
        'Go Lives': 'kpi-accent',
        'Standard': 'kpi-success',
        'Copy': 'kpi-info',
        'Data Incorrect': 'kpi-error',
        # Pre Go Live
        'Checks Completed': 'kpi-accent',
        'GTG': 'kpi-success',
        'Partial': 'kpi-warning',
        'Fail': 'kpi-error',
        # Go Live Testing
        'Tests Completed': 'kpi-accent',
        'Go Live Blocker': 'kpi-error',
        'Non-Blocker': 'kpi-warning',
    }
    
    for kpi_name, kpi_value in kpis.items():
        color_class = kpi_colors.get(kpi_name, 'kpi-grey')
        selected_class = 'selected' if kpi_name == st.session_state.crm_selected_kpi else ''
        cards_html += f'<div class="kpi-card {color_class} {selected_class}">{kpi_value}<br /><span style="font-size:0.55em;">{kpi_name}</span></div>'
    
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
    
    # Handle button clicks
    cols = st.columns(len(kpis))
    for idx, kpi_name in enumerate(kpis.keys()):
        with cols[idx]:
            if st.button(f"{kpi_name}", key=f"crm_{kpi_type}_kpi_btn_{kpi_name}"):
                if st.session_state.crm_selected_kpi != kpi_name:
                    st.session_state.crm_selected_kpi = kpi_name
                    st.session_state.crm_selected_region = None
                    st.rerun()


def render_region_cards_crm(region_counts: dict):
    """Render region cards with aligned buttons - includes 'All' option"""
    active_regions = {region: count for region, count in region_counts.items() if count > 0}

    if not active_regions:
        return

    # Add "All" option with total count
    total_count = sum(active_regions.values())
    all_regions = {'All': total_count}
    all_regions.update(active_regions)

    # Build regions HTML
    regions_html = '<div class="region-row">'

    for region, count in all_regions.items():
        selected_class = 'selected' if region == st.session_state.crm_selected_region else ''
        regions_html += f'<div class="region-btn {selected_class}">{region} ({count})</div>'

    regions_html += '</div>'
    st.markdown(regions_html, unsafe_allow_html=True)

    # Handle button clicks
    cols = st.columns(len(all_regions))
    for idx, region in enumerate(all_regions.keys()):
        with cols[idx]:
            if st.button(f"{region}", key=f"crm_region_btn_{region}"):
                st.session_state.crm_selected_region = region
                st.rerun()


def render_configuration_tab(processor: CRMDataProcessor, filtered_df: pd.DataFrame):
    """Render Configuration sub-tab"""
    
    kpis = processor.get_configuration_kpis(filtered_df)
    
    # Render KPI cards with modern styling
    render_kpi_cards_crm(kpis, "config")
    
    # Handle KPI clicks
    
    
    # Show region banners if KPI is selected
    if st.session_state.crm_selected_kpi:
        st.markdown("---")
        st.write("### 📍 Select Region")
        
        # Get region counts
        if st.session_state.crm_selected_kpi == 'Go Lives':
            region_counts = {region: len(filtered_df[filtered_df['Region'] == region]) 
                           for region in processor.get_regions(filtered_df)}
        else:
            region_counts = processor.get_region_counts(
                'Configuration Status',
                st.session_state.crm_selected_kpi,
                filtered_df
            )
        
        # Render region cards
        render_region_cards_crm(region_counts)
        
        # Handle region clicks
        
        
        # Show table if region is selected
        if st.session_state.crm_selected_region:
            st.markdown("---")

            # Handle "All" region - show all data, otherwise filter by region
            if st.session_state.crm_selected_region == 'All':
                region_filtered_df = filtered_df.copy()
            else:
                region_filtered_df = processor.filter_by_region(st.session_state.crm_selected_region, filtered_df)

            if st.session_state.crm_selected_kpi != 'Go Lives':
                region_filtered_df = region_filtered_df[
                    region_filtered_df['Configuration Status'] == st.session_state.crm_selected_kpi
                ]

            display_df = processor.get_display_dataframe('configuration', region_filtered_df)

            render_data_table(
                display_df,
                title=f"{st.session_state.crm_selected_kpi} - {st.session_state.crm_selected_region}",
                key_suffix="config"
            )
        else:
            st.info("👆 Click a region banner above to view detailed data")
    else:
        st.info("👆 Click a KPI card above to view regional breakdown")


def render_pre_go_live_tab(processor: CRMDataProcessor, filtered_df: pd.DataFrame):
    """Render Pre Go Live Checks sub-tab"""
    
    kpis = processor.get_pre_go_live_kpis(filtered_df)
    
    # Render KPI cards
    render_kpi_cards_crm(kpis, 'pregl')
    
    if st.session_state.crm_selected_kpi:
        st.markdown("---")
        st.write("### 📍 Select Region")
        
        if st.session_state.crm_selected_kpi == 'Checks Completed':
            checks_df = filtered_df[
                (filtered_df['Pre Go Live Assigned'].notna()) &
                (filtered_df['Pre Go Live Assigned'] != '')
            ]
            region_counts = {region: len(checks_df[checks_df['Region'] == region]) 
                           for region in processor.get_regions(filtered_df)}
        else:
            region_counts = processor.get_region_counts(
                'Pre Go Live Status',
                st.session_state.crm_selected_kpi,
                filtered_df
            )
        
        render_region_cards_crm(region_counts)
        
        
        if st.session_state.crm_selected_region:
            st.markdown("---")

            # Handle "All" region - show all data, otherwise filter by region
            if st.session_state.crm_selected_region == 'All':
                region_filtered_df = filtered_df.copy()
            else:
                region_filtered_df = processor.filter_by_region(st.session_state.crm_selected_region, filtered_df)

            if st.session_state.crm_selected_kpi == 'Checks Completed':
                region_filtered_df = region_filtered_df[
                    (region_filtered_df['Pre Go Live Assigned'].notna()) &
                    (region_filtered_df['Pre Go Live Assigned'] != '')
                ]
            else:
                region_filtered_df = region_filtered_df[
                    region_filtered_df['Pre Go Live Status'] == st.session_state.crm_selected_kpi
                ]

            display_df = processor.get_display_dataframe('pre_go_live', region_filtered_df)

            render_data_table(
                display_df,
                title=f"{st.session_state.crm_selected_kpi} - {st.session_state.crm_selected_region}",
                key_suffix="pre_go_live"
            )
        else:
            st.info("👆 Click a region banner above to view detailed data")
    else:
        st.info("👆 Click a KPI card above to view regional breakdown")



def render_go_live_testing_tab(processor: CRMDataProcessor, filtered_df: pd.DataFrame):
    """Render Go Live Testing sub-tab"""
    
    kpis = processor.get_go_live_testing_kpis(filtered_df)
    
    # Show upcoming week banner (ONLY in Go Live Testing)
    upcoming_count = len(filtered_df[filtered_df['Is Upcoming Week'] == True])
    render_upcoming_week_alert(upcoming_count)
    
    # Render KPI cards
    render_kpi_cards_crm(kpis, 'pregl')
    
    if st.session_state.crm_selected_kpi:
        st.markdown("---")
        st.write("### 📍 Select Region")
        
        if st.session_state.crm_selected_kpi == 'Tests Completed':
            tests_df = filtered_df[
                (filtered_df['Go Live Testing Assignee'].notna()) & 
                (filtered_df['Go Live Testing Assignee'] != '') &
                (filtered_df['Days to Go Live'] <= 0)
            ]
            region_counts = {region: len(tests_df[tests_df['Region'] == region]) 
                           for region in processor.get_regions(filtered_df)}
        else:
            region_counts = processor.get_region_counts(
                'Go Live Testing Status',
                st.session_state.crm_selected_kpi,
                filtered_df
            )
        
        render_region_cards_crm(region_counts)
        
        
        if st.session_state.crm_selected_region:
            st.markdown("---")

            # Handle "All" region - show all data, otherwise filter by region
            if st.session_state.crm_selected_region == 'All':
                region_filtered_df = filtered_df.copy()
            else:
                region_filtered_df = processor.filter_by_region(st.session_state.crm_selected_region, filtered_df)

            if st.session_state.crm_selected_kpi == 'Tests Completed':
                region_filtered_df = region_filtered_df[
                    (region_filtered_df['Go Live Testing Assignee'].notna()) &
                    (region_filtered_df['Go Live Testing Assignee'] != '') &
                    (region_filtered_df['Days to Go Live'] <= 0)
                ]
            else:
                if 'Blocker' in st.session_state.crm_selected_kpi or 'Non-Blocker' in st.session_state.crm_selected_kpi:
                    region_filtered_df = region_filtered_df[
                        region_filtered_df['Go Live Testing Status'].str.contains(st.session_state.crm_selected_kpi, na=False)
                    ]
                else:
                    region_filtered_df = region_filtered_df[
                        region_filtered_df['Go Live Testing Status'] == st.session_state.crm_selected_kpi
                    ]

            display_df = processor.get_display_dataframe('go_live_testing', region_filtered_df)
            
            render_data_table(
                display_df,
                title=f"{st.session_state.crm_selected_kpi} - {st.session_state.crm_selected_region}",
                key_suffix="go_live_testing"
            )
        else:
            st.info("👆 Click a region banner above to view detailed data")
    else:
        st.info("👆 Click a KPI card above to view regional breakdown")


def render_data_tab(processor: CRMDataProcessor):
    """Render Data tab with sub-tabs"""
    
    render_date_filter()
    
    filtered_df = processor.filter_by_date_range(st.session_state.crm_date_filter)
    
    st.markdown("---")
    
    render_sub_tab_selector()
    
    st.markdown("---")
    
    if st.session_state.crm_sub_tab == 'configuration':
        render_configuration_tab(processor, filtered_df)
    elif st.session_state.crm_sub_tab == 'pre_go_live':
        render_pre_go_live_tab(processor, filtered_df)
    elif st.session_state.crm_sub_tab == 'go_live_testing':
        render_go_live_testing_tab(processor, filtered_df)


def render_analytics_tab():
    """Render Analytics tab (placeholder)"""
    
    st.markdown("### 📈 Analytics")
    st.info("👷 Analytics tab coming soon!")
    
    st.markdown("""
    **Planned Analytics Features:**
    - Configuration trends over time
    - Pre Go Live completion rates
    - Go Live Testing success metrics
    - Regional performance comparison
    - Assignee workload distribution
    """)


def render_crm_dashboard():
    """Main function to render CRM Configuration dashboard"""
    
    # Apply modern styles
    apply_modern_styles()
    
    # Initialize session state
    initialize_session_state()
    
    # Load data
    with st.spinner("Loading CRM data..."):
        processor = load_data()
    
    # Render modern header
    render_modern_header("CRM Configuration Dashboard")
    
    # Main tabs
    tab1, tab2 = st.tabs(["📊 Data", "📈 Analytics"])
    
    with tab1:
        render_data_tab(processor)
    
    with tab2:
        render_analytics_tab()


# For standalone testing
if __name__ == "__main__":
    st.set_page_config(
        page_title="CRM Configuration Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    render_crm_dashboard()

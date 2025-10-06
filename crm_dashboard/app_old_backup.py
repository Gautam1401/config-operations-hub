"""
CRM Configuration Dashboard - Main Application
"""

import streamlit as st
import pandas as pd
from typing import Optional

from crm_dashboard.data.mock_data import load_crm_data
from crm_dashboard.utils.data_processor import CRMDataProcessor
from crm_dashboard.components.kpi_cards import render_kpi_grid, render_region_banners, render_upcoming_week_banner
from crm_dashboard.components.data_table import render_data_table
from crm_dashboard.config.settings import (
    DASHBOARD_TITLE,
    DATE_FILTERS,
    SUB_TABS,
    USE_MOCK_DATA
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


def load_data() -> CRMDataProcessor:
    """
    Load and process CRM data
    
    Returns:
        CRMDataProcessor: Processed data
    """
    
    # Load raw data
    df = load_crm_data()
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    if USE_MOCK_DATA:
        print(f"[DEBUG CRM] Loaded data columns: {df.columns.tolist()}")
        print(f"[DEBUG CRM] Data shape: {df.shape}")
    
    # Wrap in processor
    processor = CRMDataProcessor(df)
    
    return processor


def on_kpi_click(kpi_name: str):
    """Callback when KPI card is clicked"""
    
    if st.session_state.crm_selected_kpi != kpi_name:
        st.session_state.crm_selected_kpi = kpi_name
        st.session_state.crm_selected_region = None  # Reset region
        print(f"[DEBUG CRM] KPI clicked: {kpi_name}, reset region")


def on_region_click(region: str):
    """Callback when region banner is clicked"""
    
    st.session_state.crm_selected_region = region
    print(f"[DEBUG CRM] Region clicked: {region}")


def render_header(processor: CRMDataProcessor):
    """Render dashboard header with title and controls"""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f"📊 {DASHBOARD_TITLE}")
    
    with col2:
        if st.button("🔄 Refresh", key="crm_btn_refresh_header"):
            st.rerun()


def render_date_filter():
    """Render date filter radio buttons"""
    
    st.markdown("### 📅 Select Time Period")
    
    filter_options = list(DATE_FILTERS.values())
    filter_keys = list(DATE_FILTERS.keys())
    
    # Find current selection index
    current_idx = filter_keys.index(st.session_state.crm_date_filter) if st.session_state.crm_date_filter in filter_keys else 0
    
    selected_label = st.radio(
        "Time Period",
        options=filter_options,
        index=current_idx,
        horizontal=True,
        key="crm_date_filter_radio",
        label_visibility="collapsed"
    )
    
    # Map back to key
    selected_key = filter_keys[filter_options.index(selected_label)]
    
    if st.session_state.crm_date_filter != selected_key:
        st.session_state.crm_date_filter = selected_key
        st.session_state.crm_selected_kpi = None
        st.session_state.crm_selected_region = None
        print(f"[DEBUG CRM] Date filter changed to: {selected_key}")
        st.rerun()


def render_sub_tab_selector():
    """Render sub-tab selector"""
    
    st.markdown("### 📑 Select Category")
    
    tab_options = list(SUB_TABS.values())
    tab_keys = list(SUB_TABS.keys())
    
    # Find current selection index
    current_idx = tab_keys.index(st.session_state.crm_sub_tab) if st.session_state.crm_sub_tab in tab_keys else 0
    
    selected_label = st.radio(
        "Category",
        options=tab_options,
        index=current_idx,
        horizontal=True,
        key="crm_sub_tab_radio",
        label_visibility="collapsed"
    )
    
    # Map back to key
    selected_key = tab_keys[tab_options.index(selected_label)]
    
    if st.session_state.crm_sub_tab != selected_key:
        st.session_state.crm_sub_tab = selected_key
        st.session_state.crm_selected_kpi = None
        st.session_state.crm_selected_region = None
        print(f"[DEBUG CRM] Sub-tab changed to: {selected_key}")
        st.rerun()


def render_configuration_tab(processor: CRMDataProcessor, filtered_df: pd.DataFrame):
    """Render Configuration sub-tab"""
    
    # Get KPIs
    kpis = processor.get_configuration_kpis(filtered_df)
    
    
    # Render KPI cards
    render_kpi_grid(kpis, on_kpi_click, st.session_state.crm_selected_kpi)
    
    # Show region banners if KPI is selected
    if st.session_state.crm_selected_kpi:
        st.markdown("---")
        
        # Get region counts for selected KPI
        if st.session_state.crm_selected_kpi == 'Go Lives':
            # For "Go Lives", show all regions
            region_counts = {region: len(filtered_df[filtered_df['Region'] == region]) 
                           for region in processor.get_regions(filtered_df)}
        else:
            region_counts = processor.get_region_counts(
                'Configuration Status',
                st.session_state.crm_selected_kpi,
                filtered_df
            )
        
        render_region_banners(region_counts, on_region_click, st.session_state.crm_selected_region)
        
        # Show table if region is selected
        if st.session_state.crm_selected_region:
            st.markdown("---")
            
            # Filter by region
            region_filtered_df = processor.filter_by_region(st.session_state.crm_selected_region, filtered_df)
            
            # Further filter by KPI if not "Go Lives"
            if st.session_state.crm_selected_kpi != 'Go Lives':
                region_filtered_df = region_filtered_df[
                    region_filtered_df['Configuration Status'] == st.session_state.crm_selected_kpi
                ]
            
            # Get display dataframe
            display_df = processor.get_display_dataframe('configuration', region_filtered_df)
            
            # Render table
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
    
    # Get KPIs
    kpis = processor.get_pre_go_live_kpis(filtered_df)
    
    
    # Render KPI cards
    render_kpi_grid(kpis, on_kpi_click, st.session_state.crm_selected_kpi)
    
    # Show region banners if KPI is selected
    if st.session_state.crm_selected_kpi:
        st.markdown("---")
        
        # Get region counts for selected KPI
        if st.session_state.crm_selected_kpi == 'Checks Completed':
            # For "Checks Completed", filter by assignee not blank
            checks_df = filtered_df[
                (filtered_df['Pre Go Live Assignee'].notna()) & 
                (filtered_df['Pre Go Live Assignee'] != '')
            ]
            region_counts = {region: len(checks_df[checks_df['Region'] == region]) 
                           for region in processor.get_regions(filtered_df)}
        else:
            region_counts = processor.get_region_counts(
                'Pre Go Live Status',
                st.session_state.crm_selected_kpi,
                filtered_df
            )
        
        render_region_banners(region_counts, on_region_click, st.session_state.crm_selected_region)
        
        # Show table if region is selected
        if st.session_state.crm_selected_region:
            st.markdown("---")
            
            # Filter by region
            region_filtered_df = processor.filter_by_region(st.session_state.crm_selected_region, filtered_df)
            
            # Further filter by KPI
            if st.session_state.crm_selected_kpi == 'Checks Completed':
                region_filtered_df = region_filtered_df[
                    (region_filtered_df['Pre Go Live Assignee'].notna()) & 
                    (region_filtered_df['Pre Go Live Assignee'] != '')
                ]
            else:
                region_filtered_df = region_filtered_df[
                    region_filtered_df['Pre Go Live Status'] == st.session_state.crm_selected_kpi
                ]
            
            # Get display dataframe
            display_df = processor.get_display_dataframe('pre_go_live', region_filtered_df)
            
            # Render table
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
    
    # Get KPIs
    kpis = processor.get_go_live_testing_kpis(filtered_df)
    
    # Show upcoming week banner
    upcoming_count = len(filtered_df[filtered_df['Is Upcoming Week'] == True])
    render_upcoming_week_banner(upcoming_count)
    
    # Render KPI cards
    render_kpi_grid(kpis, on_kpi_click, st.session_state.crm_selected_kpi)
    
    # Show region banners if KPI is selected
    if st.session_state.crm_selected_kpi:
        st.markdown("---")
        
        # Get region counts for selected KPI
        if st.session_state.crm_selected_kpi == 'Tests Completed':
            # For "Tests Completed", filter by assignee not blank AND not future go-live
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
        
        render_region_banners(region_counts, on_region_click, st.session_state.crm_selected_region)
        
        # Show table if region is selected
        if st.session_state.crm_selected_region:
            st.markdown("---")
            
            # Filter by region
            region_filtered_df = processor.filter_by_region(st.session_state.crm_selected_region, filtered_df)
            
            # Further filter by KPI
            if st.session_state.crm_selected_kpi == 'Tests Completed':
                region_filtered_df = region_filtered_df[
                    (region_filtered_df['Go Live Testing Assignee'].notna()) & 
                    (region_filtered_df['Go Live Testing Assignee'] != '') &
                    (region_filtered_df['Days to Go Live'] <= 0)
                ]
            else:
                # Handle special cases for Blocker/Non-Blocker
                if 'Blocker' in st.session_state.crm_selected_kpi or 'Non-Blocker' in st.session_state.crm_selected_kpi:
                    region_filtered_df = region_filtered_df[
                        region_filtered_df['Go Live Testing Status'].str.contains(st.session_state.crm_selected_kpi, na=False)
                    ]
                else:
                    region_filtered_df = region_filtered_df[
                        region_filtered_df['Go Live Testing Status'] == st.session_state.crm_selected_kpi
                    ]
            
            # Get display dataframe
            display_df = processor.get_display_dataframe('go_live_testing', region_filtered_df)
            
            # Render table
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
    
    # Render date filter
    render_date_filter()
    
    # Filter data by date
    filtered_df = processor.filter_by_date_range(st.session_state.crm_date_filter)
    
    st.markdown("---")
    
    # Render sub-tab selector
    render_sub_tab_selector()
    
    st.markdown("---")
    
    # Render appropriate sub-tab
    if st.session_state.crm_sub_tab == 'configuration':
        render_configuration_tab(processor, filtered_df)
    elif st.session_state.crm_sub_tab == 'pre_go_live':
        render_pre_go_live_tab(processor, filtered_df)
    elif st.session_state.crm_sub_tab == 'go_live_testing':
        render_go_live_testing_tab(processor, filtered_df)


def render_analytics_tab():
    """Render Analytics tab (placeholder)"""
    
    st.markdown("### 📈 Analytics")
    st.info("Analytics features coming soon!")
    
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
    
    # Initialize session state
    initialize_session_state()
    
    # Load data
    with st.spinner("Loading CRM data..."):
        processor = load_data()
    
    # Render header
    render_header(processor)
    
    st.markdown("---")
    
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

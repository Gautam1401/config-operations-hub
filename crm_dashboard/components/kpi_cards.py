"""
CRM Configuration Dashboard - KPI Cards Component
"""

import streamlit as st
from typing import Dict, Callable
from crm_dashboard.config.settings import KPI_COLORS


def render_kpi_grid(kpis: Dict[str, int], on_kpi_click: Callable, selected_kpi: str = None):
    """
    Render KPI cards in a grid
    
    Args:
        kpis: Dictionary of KPI name to count
        on_kpi_click: Callback function when KPI is clicked
        selected_kpi: Currently selected KPI name
    """
    
    num_kpis = len(kpis)
    cols = st.columns(num_kpis)
    
    for idx, (kpi_name, count) in enumerate(kpis.items()):
        with cols[idx]:
            # Determine if this KPI is selected
            is_selected = (selected_kpi == kpi_name)
            
            # Get color
            color = KPI_COLORS.get(kpi_name, "#008080")
            
            # Create card with button
            card_style = f"""
                background-color: {color};
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                cursor: pointer;
                border: {'3px solid #FFD700' if is_selected else 'none'};
                box-shadow: {'0 0 10px rgba(255, 215, 0, 0.5)' if is_selected else '0 4px 6px rgba(0,0,0,0.1)'};
            """
            
            st.markdown(
                f"""
                <div style="{card_style}">
                    <h2 style="margin: 0; font-size: 2.5em;">{count}</h2>
                    <p style="margin: 5px 0 0 0; font-size: 1.1em;">{kpi_name}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Invisible button for click detection
            if st.button(f"Select {kpi_name}", key=f"kpi_btn_{kpi_name}", help=f"Click to view {kpi_name} details"):
                on_kpi_click(kpi_name)


def render_region_banners(region_counts: Dict[str, int], on_region_click: Callable, selected_region: str = None):
    """
    Render region banners/cards
    
    Args:
        region_counts: Dictionary of region to count
        on_region_click: Callback function when region is clicked
        selected_region: Currently selected region
    """
    
    st.markdown("### 📍 Select Region")
    
    # Filter out regions with 0 count
    active_regions = {region: count for region, count in region_counts.items() if count > 0}
    
    if not active_regions:
        st.info("No data available for the selected KPI")
        return
    
    num_regions = len(active_regions)
    cols = st.columns(num_regions)
    
    for idx, (region, count) in enumerate(active_regions.items()):
        with cols[idx]:
            is_selected = (selected_region == region)
            
            # Region card style
            card_style = f"""
                background-color: {'#17a2b8' if is_selected else '#6c757d'};
                color: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                cursor: pointer;
                border: {'3px solid #FFD700' if is_selected else 'none'};
                box-shadow: {'0 0 10px rgba(255, 215, 0, 0.5)' if is_selected else '0 4px 6px rgba(0,0,0,0.1)'};
            """
            
            st.markdown(
                f"""
                <div style="{card_style}">
                    <h3 style="margin: 0; font-size: 2em;">{count}</h3>
                    <p style="margin: 5px 0 0 0; font-size: 1em;">{region}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Invisible button for click detection
            if st.button(f"Select {region}", key=f"region_btn_{region}", help=f"Click to view {region} details"):
                on_region_click(region)


def render_upcoming_week_banner(count: int):
    """
    Render banner for upcoming week go-lives
    
    Args:
        count: Number of go-lives in upcoming week
    """
    
    if count > 0:
        st.markdown(
            f"""
            <div style="
                background-color: #ffc107;
                color: #000;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 20px;
                border-left: 5px solid #ff9800;
            ">
                <h3 style="margin: 0;">⚠️ Upcoming Week Alert</h3>
                <p style="margin: 5px 0 0 0; font-size: 1.2em;">
                    <strong>{count}</strong> Go-Live(s) scheduled in the next 7 days
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


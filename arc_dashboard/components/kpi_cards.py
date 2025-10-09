"""
KPI Card Components for ARC Dashboard
Reusable UI components for displaying KPI cards
"""

import streamlit as st
from typing import Dict, Optional, Callable


def render_kpi_grid(kpis: Dict[str, int], colors: Dict[str, str], on_click: Optional[Callable] = None):
    """
    Render a grid of KPI cards as buttons
    
    Args:
        kpis: Dictionary of KPI names and values
        colors: Dictionary of KPI names and colors
        on_click: Callback function when a card is clicked
    """
    
    # Create columns for grid layout
    num_kpis = len(kpis)
    cols = st.columns(num_kpis)
    
    for idx, (kpi_name, kpi_value) in enumerate(kpis.items()):
        with cols[idx]:
            # Create clickable button
            if st.button(
                f"{kpi_name}\n\n{kpi_value}",
                key=f"kpi_{kpi_name.replace(' ', '_')}",
                use_container_width=True,
                type="primary"
            ):
                if on_click:
                    on_click(kpi_name)


def render_breakdown_cards(
    breakdown: Dict[str, int],
    colors: Dict[str, str],
    title: str,
    on_click: Optional[Callable] = None
):
    """
    Render breakdown cards (e.g., Service, Parts, Accounting)
    
    Args:
        breakdown: Dictionary of breakdown categories and values
        colors: Dictionary of category colors
        title: Section title
        on_click: Callback function when a card is clicked
    """
    
    st.subheader(title)
    
    # Create columns
    cols = st.columns(len(breakdown))
    
    for idx, (category, value) in enumerate(breakdown.items()):
        with cols[idx]:
            if st.button(
                f"{category}\n\n{value}",
                key=f"breakdown_{title.replace(' ', '_')}_{category}",
                use_container_width=True,
                type="secondary"
            ):
                if on_click:
                    on_click(category)


def render_region_cards(
    regions: list,
    selected_region: Optional[str],
    on_click: Callable,
    counts: Optional[Dict[str, int]] = None,
    month_key: str = ""
):
    """
    Render region selection as clickable cards

    Args:
        regions: List of region names
        selected_region: Currently selected region
        on_click: Callback function when a region is clicked
        counts: Optional dictionary of region counts
        month_key: Optional month key for unique button IDs
    """

    st.subheader("Select Region")

    # Create columns for regions (max 4 per row)
    regions_per_row = 4
    num_rows = (len(regions) + regions_per_row - 1) // regions_per_row

    region_idx = 0
    for row in range(num_rows):
        cols = st.columns(regions_per_row)
        for col_idx in range(regions_per_row):
            if region_idx < len(regions):
                region = regions[region_idx]
                with cols[col_idx]:
                    # Determine if this region is selected
                    is_selected = (region == selected_region)

                    # Get count if available
                    count = counts.get(region, 0) if counts else 0

                    # Display as clickable button
                    if st.button(
                        f"{region}\n\n{count} records",
                        key=f"region_card_{region}_{month_key}",
                        use_container_width=True,
                        type="primary" if is_selected else "secondary"
                    ):
                        on_click(region)

                region_idx += 1


# Keep old function name for backward compatibility
def render_region_banners(
    regions: list,
    selected_region: Optional[str],
    on_click: Callable,
    counts: Optional[Dict[str, int]] = None,
    month_key: str = ""
):
    """Backward compatibility wrapper"""
    render_region_cards(regions, selected_region, on_click, counts, month_key)


def render_metric_card(label: str, value: str, delta: Optional[str] = None):
    """
    Render a simple metric card using Streamlit's metric component
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta/change value
    """
    st.metric(label=label, value=value, delta=delta)


if __name__ == '__main__':
    # Test KPI cards
    print("KPI Cards Component Module")
    print("Run the main dashboard to see these components in action")

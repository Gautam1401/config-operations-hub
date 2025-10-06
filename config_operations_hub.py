"""
Config Operations Hub - Main Dashboard (Modern Design)
Integrates all LOB dashboards: ARC Configuration, CRM Configuration, Integration, Regression Testing
"""

import streamlit as st

# Import LOB dashboard modules
import arc_dashboard.app as arc_app
import crm_dashboard.app as crm_app
import integration_dashboard.app as integration_app
import regression_dashboard.app as regression_app

# Import modern styles
from shared.styles import apply_modern_styles, render_modern_header

# Import authentication
from shared.auth import require_auth, render_user_info, is_current_user_super_admin
from shared.admin_manager import render_admin_management_page


def render_placeholder_tab(tab_name: str):
    """Render placeholder for tabs not yet implemented"""
    
    st.markdown(f"### {tab_name}")
    st.info(f"👷 {tab_name} dashboard coming soon!")
    
    st.markdown("""
    **Planned Features:**
    - Data visualization and KPIs
    - Regional breakdown
    - Status tracking
    - Export capabilities
    """)


def main():
    """Main function to render Config Operations Hub"""
    
    # Page config
    st.set_page_config(
        page_title="Config Operations Hub",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply modern styles
    apply_modern_styles()
    
    # Require authentication
    if not require_auth():
        return
    
    # Render modern header
    render_modern_header(
        "Config Operations Hub",
        "https://img.icons8.com/?size=512&id=82751&format=png"
    )
    
    # Main LOB tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔧 ARC Configuration",
        "📞 CRM Configuration",
        "🔗 Integration",
        "🧪 Regression Testing"
    ])
    
    with tab1:
        # Render ARC Configuration dashboard
        arc_app.render_arc_dashboard()
    
    with tab2:
        # Render CRM Configuration dashboard
        crm_app.render_crm_dashboard()
    
    with tab3:
        # Render Integration dashboard
        integration_app.render_integration_dashboard()
    
    with tab4:
        # Render Regression Testing dashboard
        regression_app.render_regression_dashboard()


if __name__ == "__main__":
    main()

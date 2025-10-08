"""
Config Operations Hub - Main Dashboard (Modern Design)
Integrates all LOB dashboards: ARC Configuration, CRM Configuration, Integration, Regression Testing
"""

# Version and Last Updated (IST)
__version__ = "1.1.3"
__last_updated__ = "2025-10-08 15:22:44 IST"

import streamlit as st

# Import LOB dashboard modules
import arc_dashboard.app as arc_app
import crm_dashboard.app as crm_app
import integration_dashboard.app as integration_app
import regression_dashboard.app as regression_app

# Import modern styles
from shared.styles import apply_modern_styles, render_modern_header

# Import authentication
from shared.auth import require_auth, is_current_user_super_admin
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
    
    # === SIDEBAR: User Management ===
    with st.sidebar:
        st.markdown("### 👤 User Management")
        st.markdown("---")
        
        # Display current user info
        if 'user_email' in st.session_state:
            st.markdown(f"**Email:** {st.session_state.user_email}")
            
            # Show role
            if st.session_state.get('is_super_admin', False):
                st.markdown("**Role:** ⭐ Super Admin")
            elif st.session_state.get('is_admin', False):
                st.markdown("**Role:** 🔧 Admin")
            else:
                st.markdown("**Role:** 👁️ Viewer")
        
        st.markdown("---")
        
        # Admin Management (only for super admins)
        if is_current_user_super_admin():
            st.markdown("#### ⭐ Admin Panel")
            if st.button("🔧 Manage Admins", use_container_width=True, key="manage_admins_btn"):
                st.session_state['show_admin_panel'] = True
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="secondary", key="logout_btn_main"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Display version at bottom of sidebar
    st.markdown("---")
    st.caption(f"🔄 Version: {__version__} | Updated: {__last_updated__}")
    
    # === MAIN CONTENT ===
    
    # Check if admin panel should be shown
    if st.session_state.get('show_admin_panel', False):
        render_admin_management_page()
        
        # Back button
        if st.button("← Back to Dashboard", key="back_to_dashboard_btn"):
            st.session_state['show_admin_panel'] = False
            st.rerun()
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
        try:
            arc_app.render_arc_dashboard()
        except Exception as e:
            st.warning("⚠️ Dashboard is loading... Please wait or refresh the page.")
            print(f"[ERROR ARC Dashboard] {str(e)}")

    with tab2:
        # Render CRM Configuration dashboard
        try:
            crm_app.render_crm_dashboard()
        except Exception as e:
            st.warning("⚠️ Dashboard is loading... Please wait or refresh the page.")
            print(f"[ERROR CRM Dashboard] {str(e)}")

    with tab3:
        # Render Integration dashboard
        try:
            integration_app.render_integration_dashboard()
        except Exception as e:
            st.warning("⚠️ Dashboard is loading... Please wait or refresh the page.")
            print(f"[ERROR Integration Dashboard] {str(e)}")

    with tab4:
        # Render Regression Testing dashboard
        try:
            regression_app.render_regression_dashboard()
        except Exception as e:
            st.warning("⚠️ Dashboard is loading... Please wait or refresh the page.")
            print(f"[ERROR Regression Dashboard] {str(e)}")


if __name__ == "__main__":
    main()

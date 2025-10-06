"""
Admin Management Module
Allows Super Admins to add/remove regular admins
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import List, Tuple
from shared.auth import (
    validate_email, 
    is_current_user_super_admin,
    REQUIRED_DOMAIN,
    SUPER_ADMIN_EMAILS
)

# File to store admin list
ADMIN_LIST_FILE = "data/admin_list.json"

# ============================================================================
# ADMIN LIST MANAGEMENT
# ============================================================================

def load_admin_list() -> List[str]:
    """
    Load admin list from file
    
    Returns:
        List of admin email addresses
    """
    if not os.path.exists(ADMIN_LIST_FILE):
        # Create default file
        os.makedirs(os.path.dirname(ADMIN_LIST_FILE), exist_ok=True)
        save_admin_list([])
        return []
    
    try:
        with open(ADMIN_LIST_FILE, 'r') as f:
            data = json.load(f)
            return data.get('admins', [])
    except Exception as e:
        st.error(f"Error loading admin list: {str(e)}")
        return []


def save_admin_list(admins: List[str]) -> bool:
    """
    Save admin list to file
    
    Args:
        admins: List of admin email addresses
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(ADMIN_LIST_FILE), exist_ok=True)
        
        data = {
            'admins': admins,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_by': st.session_state.get('user_email', 'unknown')
        }
        
        with open(ADMIN_LIST_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving admin list: {str(e)}")
        return False


def get_all_admins() -> List[str]:
    """
    Get all admins (regular + super admins)
    
    Returns:
        List of all admin emails
    """
    regular_admins = load_admin_list()
    all_admins = list(set(regular_admins + SUPER_ADMIN_EMAILS))
    return sorted(all_admins)


def add_admin(email: str) -> Tuple[bool, str]:
    """
    Add a new admin
    
    Args:
        email: Email to add as admin
        
    Returns:
        Tuple of (success, message)
    """
    # Validate email
    is_valid, error_msg = validate_email(email)
    if not is_valid:
        return False, error_msg
    
    email_lower = email.lower()
    
    # Check if already super admin
    if email_lower in [sa.lower() for sa in SUPER_ADMIN_EMAILS]:
        return False, "This email is already a Super Admin"
    
    # Load current admin list
    admins = load_admin_list()
    
    # Check if already admin
    if email_lower in [a.lower() for a in admins]:
        return False, "This email is already an Admin"
    
    # Add to list
    admins.append(email_lower)
    
    # Save
    if save_admin_list(admins):
        return True, f"✅ Successfully added {email} as Admin"
    else:
        return False, "Failed to save admin list"


def remove_admin(email: str) -> Tuple[bool, str]:
    """
    Remove an admin
    
    Args:
        email: Email to remove from admins
        
    Returns:
        Tuple of (success, message)
    """
    email_lower = email.lower()
    
    # Cannot remove super admins
    if email_lower in [sa.lower() for sa in SUPER_ADMIN_EMAILS]:
        return False, "Cannot remove Super Admins"
    
    # Load current admin list
    admins = load_admin_list()
    
    # Check if admin exists
    if email_lower not in [a.lower() for a in admins]:
        return False, "This email is not in the admin list"
    
    # Remove from list
    admins = [a for a in admins if a.lower() != email_lower]
    
    # Save
    if save_admin_list(admins):
        return True, f"✅ Successfully removed {email} from Admins"
    else:
        return False, "Failed to save admin list"


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_super_admin_panel():
    """
    Render Super Admin panel for managing admins
    Only visible to Super Admins
    """
    if not is_current_user_super_admin():
        return
    
    st.markdown("---")
    st.markdown("## ⭐ Super Admin Panel")
    st.markdown("### Manage Admin Users")
    
    # Get current admin list
    all_admins = get_all_admins()
    regular_admins = load_admin_list()
    
    # Display current admins
    st.markdown("#### Current Admins")
    
    if all_admins:
        # Create a nice table
        admin_data = []
        for admin_email in all_admins:
            if admin_email.lower() in [sa.lower() for sa in SUPER_ADMIN_EMAILS]:
                role = "⭐ Super Admin"
                can_remove = False
            else:
                role = "🔧 Admin"
                can_remove = True
            
            admin_data.append({
                "Email": admin_email,
                "Role": role,
                "Can Remove": "✅" if can_remove else "❌"
            })
        
        # Display as table
        import pandas as pd
        df = pd.DataFrame(admin_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.info(f"📊 Total: {len(all_admins)} admins ({len(SUPER_ADMIN_EMAILS)} Super Admins, {len(regular_admins)} Regular Admins)")
    else:
        st.warning("No admins found")
    
    st.markdown("---")
    
    # Add new admin
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Add New Admin")
        new_admin_email = st.text_input(
            "Email Address",
            placeholder=f"newadmin{REQUIRED_DOMAIN}",
            key="new_admin_email",
            help=f"Enter a {REQUIRED_DOMAIN} email address"
        )
    
    with col2:
        st.markdown("####  ")  # Spacing
        if st.button("➕ Add Admin", use_container_width=True, type="primary"):
            if new_admin_email:
                success, message = add_admin(new_admin_email)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
            else:
                st.warning("Please enter an email address")
    
    st.markdown("---")
    
    # Remove admin
    if regular_admins:
        st.markdown("#### Remove Admin")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            admin_to_remove = st.selectbox(
                "Select Admin to Remove",
                options=regular_admins,
                key="admin_to_remove"
            )
        
        with col2:
            st.markdown("####  ")  # Spacing
            if st.button("🗑️ Remove", use_container_width=True, type="secondary"):
                if admin_to_remove:
                    success, message = remove_admin(admin_to_remove)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    st.markdown("---")
    
    # Instructions
    with st.expander("ℹ️ How to Add Another Super Admin"):
        st.markdown("""
        **To add another Super Admin:**
        
        1. Open the file: `shared/auth.py`
        2. Find the `SUPER_ADMIN_EMAILS` list
        3. Add the new email address:
        
        ```python
        SUPER_ADMIN_EMAILS = [
            "gautam@tekion.com",
            "newsuperadmin@tekion.com",  # Add here
        ]
        ```
        
        4. Save the file
        5. Restart the dashboard
        
        **Note:** Super Admins can:
        - ✅ Upload and refresh data
        - ✅ Add/remove regular admins
        - ✅ Access all dashboard features
        
        **Regular Admins can:**
        - ✅ Upload and refresh data
        - ✅ Access all dashboard features
        - ❌ Cannot manage other admins
        """)


def render_admin_management_page():
    """
    Render full admin management page
    Only accessible to Super Admins
    """
    if not is_current_user_super_admin():
        st.error("❌ Access Denied")
        st.warning("Only Super Admins can access this page")
        st.stop()
        return
    
    st.title("⭐ Admin Management")
    st.markdown("Manage admin users for the Config Operations Hub")
    
    render_super_admin_panel()


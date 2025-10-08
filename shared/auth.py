"""
Authentication and Authorization Module
Handles user authentication and admin access control
"""

import streamlit as st
from typing import Optional, Tuple
import re
import json
import os

# Email verification (optional - can be enabled/disabled)
EMAIL_VERIFICATION_ENABLED = False  # Set to True to enable email verification

try:
    from shared.email_verification import render_email_verification_ui
except ImportError:
    EMAIL_VERIFICATION_ENABLED = False

# ============================================================================
# ADMIN CONFIGURATION
# ============================================================================

# Super Admin emails (can add/remove admins and have all admin privileges)
SUPER_ADMIN_EMAILS = [
    "gdnaresh@tekion.com",
    # Add additional super admins here if needed in future:
    # "superadmin2@tekion.com",
]

# Regular Admin emails (can upload/refresh data but cannot manage other admins)
# This list will be stored in a file and managed by Super Admins
ADMIN_EMAILS = [
    # Regular admins will be added by Super Admins through the UI
    # Or you can manually add them here:
    # "admin1@tekion.com",
    # "admin2@tekion.com",
]

# Required email domain for all users
REQUIRED_DOMAIN = "@tekion.com"

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format and domain
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email cannot be empty"
    
    # Basic email format validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    
    # Check domain
    if not email.lower().endswith(REQUIRED_DOMAIN.lower()):
        return False, f"Only {REQUIRED_DOMAIN} emails are allowed"
    
    return True, ""


def is_super_admin(email: str) -> bool:
    """
    Check if user is a super admin
    
    Args:
        email: User's email address
        
    Returns:
        bool: True if user is super admin, False otherwise
    """
    return email.lower() in [admin.lower() for admin in SUPER_ADMIN_EMAILS]


def _load_admin_list_from_file() -> list:
    """Load admin list from file"""
    admin_file = "data/admin_list.json"
    if not os.path.exists(admin_file):
        return ADMIN_EMAILS  # Return hardcoded list if file doesn't exist
    
    try:
        with open(admin_file, 'r') as f:
            data = json.load(f)
            return data.get('admins', ADMIN_EMAILS)
    except:
        return ADMIN_EMAILS


def is_admin(email: str) -> bool:
    """
    Check if user is an admin (regular or super)
    
    Args:
        email: User's email address
        
    Returns:
        bool: True if user is admin or super admin, False otherwise
    """
    email_lower = email.lower()
    
    # Load dynamic admin list from file
    dynamic_admins = _load_admin_list_from_file()
    
    return (email_lower in [admin.lower() for admin in dynamic_admins] or 
            email_lower in [admin.lower() for admin in SUPER_ADMIN_EMAILS])


def authenticate_user() -> Optional[str]:
    """
    Authenticate user and return their email if valid
    
    Returns:
        str: User's email if authenticated, None otherwise
    """
    # Check if user is already authenticated
    if 'user_email' in st.session_state and st.session_state.user_email:
        return st.session_state.user_email
    
    # Show login form
    st.markdown("### 🔐 Tekion Config Operations Hub")
    st.markdown("---")
    st.caption("🔄 Version: 1.1.5 | Updated: 2025-10-08 15:47:43 IST")
    st.markdown("---")
    
    with st.form("login_form"):
        st.markdown("#### Please enter your Tekion email to continue")
        email = st.text_input(
            "Email Address",
            placeholder="yourname@tekion.com",
            help=f"Only {REQUIRED_DOMAIN} emails are allowed"
        )
        
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            # Validate email
            is_valid, error_msg = validate_email(email)
            
            if is_valid:
                # Check if email verification is required
                if EMAIL_VERIFICATION_ENABLED:
                    # Store email temporarily for verification
                    st.session_state.pending_email = email.lower()
                    st.session_state.needs_verification = True
                    st.rerun()
                else:
                    # No verification needed - login directly
                    st.session_state.user_email = email.lower()
                    st.session_state.is_admin = is_admin(email)
                    st.session_state.is_super_admin = is_super_admin(email)
                    
                    if is_super_admin(email):
                        st.success(f"✅ Welcome, Super Admin {email}!")
                    elif is_admin(email):
                        st.success(f"✅ Welcome, Admin {email}!")
                    else:
                        st.success(f"✅ Welcome, {email}!")
                    st.rerun()
            else:
                st.error(f"❌ {error_msg}")
                return None
    
    # Email verification step (if enabled)
    if EMAIL_VERIFICATION_ENABLED and st.session_state.get('needs_verification', False):
        pending_email = st.session_state.get('pending_email', '')
        
        if render_email_verification_ui(pending_email):
            # Email verified - complete login
            st.session_state.user_email = pending_email
            st.session_state.is_admin = is_admin(pending_email)
            st.session_state.is_super_admin = is_super_admin(pending_email)
            st.session_state.needs_verification = False
            
            if is_super_admin(pending_email):
                st.success(f"✅ Welcome, Super Admin {pending_email}!")
            elif is_admin(pending_email):
                st.success(f"✅ Welcome, Admin {pending_email}!")
            else:
                st.success(f"✅ Welcome, {pending_email}!")
            st.rerun()
        
        return None
    
    return None


def logout():
    """Logout current user"""
    if 'user_email' in st.session_state:
        del st.session_state.user_email
    if 'is_admin' in st.session_state:
        del st.session_state.is_admin
    st.rerun()


def render_user_info():
    """Render user info in sidebar"""
    if 'user_email' not in st.session_state:
        return
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👤 User Info")
    
    # Show email
    st.sidebar.markdown(f"**Email:** {st.session_state.user_email}")
    
    # Show role
    if st.session_state.get('is_super_admin', False):
        st.sidebar.markdown("**Role:** ⭐ Super Admin")
    elif st.session_state.get('is_admin', False):
        st.sidebar.markdown("**Role:** 🔧 Admin")
    else:
        st.sidebar.markdown("**Role:** 👁️ Viewer")
    
    # Logout button
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()


def require_auth():
    """
    Require authentication before showing dashboard
    Returns True if authenticated, False otherwise
    """
    user_email = authenticate_user()
    
    if not user_email:
        st.stop()
        return False
    
    return True


def require_admin():
    """
    Require admin access
    Shows error if user is not admin
    """
    if not st.session_state.get('is_admin', False):
        st.error("❌ Admin access required for this action")
        st.info("Please contact an administrator if you need access to this feature.")
        st.stop()
        return False
    
    return True


# ============================================================================
# ADMIN PANEL COMPONENTS
# ============================================================================

def render_admin_panel():
    """Render admin panel in sidebar"""
    if not st.session_state.get('is_admin', False):
        return
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Admin Panel")
    
    # Data refresh info
    if 'last_data_refresh' in st.session_state:
        st.sidebar.markdown(f"**Last Refresh:** {st.session_state.last_data_refresh}")
    else:
        st.sidebar.markdown("**Last Refresh:** Never")
    
    st.sidebar.markdown("**Data Source:** Local Upload")


def show_admin_badge():
    """Show admin badge in main area"""
    if st.session_state.get('is_super_admin', False):
        st.markdown(
            """
            <div style="background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%); 
                        padding: 8px 16px; border-radius: 8px; margin-bottom: 16px;
                        text-align: center; color: #000; font-weight: 600;">
                ⭐ SUPER ADMIN MODE - You can upload data and manage admins
            </div>
            """,
            unsafe_allow_html=True
        )
    elif st.session_state.get('is_admin', False):
        st.markdown(
            """
            <div style="background: linear-gradient(90deg, #3874F2 0%, #1abc9c 100%); 
                        padding: 8px 16px; border-radius: 8px; margin-bottom: 16px;
                        text-align: center; color: #fff; font-weight: 600;">
                🔧 ADMIN MODE - You can upload and refresh data
            </div>
            """,
            unsafe_allow_html=True
        )


def get_current_user() -> Optional[str]:
    """Get current logged-in user email"""
    return st.session_state.get('user_email', None)


def is_current_user_admin() -> bool:
    """Check if current user is admin"""
    return st.session_state.get('is_admin', False)


def is_current_user_super_admin() -> bool:
    """Check if current user is super admin"""
    return st.session_state.get('is_super_admin', False)


# ============================================================================
# ADMIN MANAGEMENT FUNCTIONS
# ============================================================================

def add_admin(email: str) -> Tuple[bool, str]:
    """
    Add a new admin (for future use)
    
    Args:
        email: Email to add as admin
        
    Returns:
        Tuple of (success, message)
    """
    is_valid, error_msg = validate_email(email)
    
    if not is_valid:
        return False, error_msg
    
    if email.lower() in [admin.lower() for admin in ADMIN_EMAILS]:
        return False, "Email is already an admin"
    
    # Note: In production, this would update a database
    # For now, admins must be added manually to ADMIN_EMAILS list
    return False, "Please add admin emails directly to shared/auth.py ADMIN_EMAILS list"


def remove_admin(email: str) -> Tuple[bool, str]:
    """
    Remove an admin (for future use)
    
    Args:
        email: Email to remove from admins
        
    Returns:
        Tuple of (success, message)
    """
    # Note: In production, this would update a database
    # For now, admins must be removed manually from ADMIN_EMAILS list
    return False, "Please remove admin emails directly from shared/auth.py ADMIN_EMAILS list"


def get_admin_list() -> list:
    """Get list of all admin emails (regular + super)"""
    dynamic_admins = _load_admin_list_from_file()
    all_admins = list(set(dynamic_admins + SUPER_ADMIN_EMAILS))
    return sorted(all_admins)


"""
Email Verification Module
Sends verification codes to email addresses to ensure they are valid
"""

import streamlit as st
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional, Tuple

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

# SMTP Configuration for sending emails
# You'll need to configure this with your email service

# Option 1: Gmail (requires App Password)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Option 2: Outlook/Office365
# SMTP_SERVER = "smtp.office365.com"
# SMTP_PORT = 587

# Option 3: Tekion's SMTP (if available)
# SMTP_SERVER = "smtp.tekion.com"
# SMTP_PORT = 587

# Sender email credentials
# NOTE: For production, use environment variables or secrets management
SENDER_EMAIL = "your-email@gmail.com"  # Update this
SENDER_PASSWORD = "your-app-password"  # Update this (use App Password, not regular password)

# Verification code settings
CODE_LENGTH = 6
CODE_EXPIRY_MINUTES = 10

# ============================================================================
# VERIFICATION CODE GENERATION
# ============================================================================

def generate_verification_code() -> str:
    """
    Generate a random 6-digit verification code
    
    Returns:
        str: 6-digit verification code
    """
    return ''.join(random.choices(string.digits, k=CODE_LENGTH))


def store_verification_code(email: str, code: str):
    """
    Store verification code in session state with expiry time
    
    Args:
        email: Email address
        code: Verification code
    """
    if 'verification_codes' not in st.session_state:
        st.session_state.verification_codes = {}
    
    st.session_state.verification_codes[email.lower()] = {
        'code': code,
        'expiry': datetime.now() + timedelta(minutes=CODE_EXPIRY_MINUTES),
        'attempts': 0
    }


def verify_code(email: str, entered_code: str) -> Tuple[bool, str]:
    """
    Verify the entered code against stored code
    
    Args:
        email: Email address
        entered_code: Code entered by user
        
    Returns:
        Tuple of (is_valid, message)
    """
    if 'verification_codes' not in st.session_state:
        return False, "No verification code found. Please request a new code."
    
    email_lower = email.lower()
    
    if email_lower not in st.session_state.verification_codes:
        return False, "No verification code found for this email. Please request a new code."
    
    code_data = st.session_state.verification_codes[email_lower]
    
    # Check expiry
    if datetime.now() > code_data['expiry']:
        del st.session_state.verification_codes[email_lower]
        return False, "Verification code has expired. Please request a new code."
    
    # Check attempts
    if code_data['attempts'] >= 3:
        del st.session_state.verification_codes[email_lower]
        return False, "Too many failed attempts. Please request a new code."
    
    # Verify code
    if entered_code == code_data['code']:
        # Code is valid - clean up
        del st.session_state.verification_codes[email_lower]
        return True, "Email verified successfully!"
    else:
        # Increment attempts
        code_data['attempts'] += 1
        remaining = 3 - code_data['attempts']
        return False, f"Invalid code. {remaining} attempts remaining."


# ============================================================================
# EMAIL SENDING
# ============================================================================

def send_verification_email(email: str, code: str) -> Tuple[bool, str]:
    """
    Send verification code via email
    
    Args:
        email: Recipient email address
        code: Verification code to send
        
    Returns:
        Tuple of (success, message)
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Config Operations Hub - Email Verification'
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        
        # Email body
        text = f"""
        Welcome to Tekion Config Operations Hub!
        
        Your verification code is: {code}
        
        This code will expire in {CODE_EXPIRY_MINUTES} minutes.
        
        If you didn't request this code, please ignore this email.
        
        Best regards,
        Config Operations Hub Team
        """
        
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
              <h2 style="color: #008080; margin-bottom: 20px;">Welcome to Tekion Config Operations Hub!</h2>
              
              <p style="font-size: 16px; color: #333; margin-bottom: 20px;">
                Your verification code is:
              </p>
              
              <div style="background-color: #f0f0f0; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 20px;">
                <h1 style="color: #008080; font-size: 36px; letter-spacing: 8px; margin: 0;">
                  {code}
                </h1>
              </div>
              
              <p style="font-size: 14px; color: #666; margin-bottom: 10px;">
                This code will expire in <strong>{CODE_EXPIRY_MINUTES} minutes</strong>.
              </p>
              
              <p style="font-size: 14px; color: #666;">
                If you didn't request this code, please ignore this email.
              </p>
              
              <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
              
              <p style="font-size: 12px; color: #999; text-align: center;">
                Config Operations Hub Team<br>
                Tekion
              </p>
            </div>
          </body>
        </html>
        """
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True, f"Verification code sent to {email}"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_email_verification_ui(email: str) -> bool:
    """
    Render email verification UI
    
    Args:
        email: Email address to verify
        
    Returns:
        bool: True if email is verified, False otherwise
    """
    st.markdown("### 📧 Email Verification Required")
    st.info(f"We need to verify that **{email}** is a valid email address.")
    
    # Check if code already sent
    if 'verification_code_sent' not in st.session_state:
        st.session_state.verification_code_sent = False
    
    # Send code button
    if not st.session_state.verification_code_sent:
        if st.button("📨 Send Verification Code", type="primary", use_container_width=True):
            # Generate code
            code = generate_verification_code()
            
            # Store code
            store_verification_code(email, code)
            
            # Send email
            success, message = send_verification_email(email, code)
            
            if success:
                st.success(f"✅ {message}")
                st.session_state.verification_code_sent = True
                st.rerun()
            else:
                st.error(f"❌ {message}")
                st.warning("Please check your email configuration in shared/email_verification.py")
        
        return False
    
    # Verify code form
    st.markdown("---")
    st.markdown("#### Enter Verification Code")
    st.markdown(f"A 6-digit code has been sent to **{email}**")
    
    with st.form("verify_code_form"):
        entered_code = st.text_input(
            "Verification Code",
            max_chars=6,
            placeholder="000000",
            help="Enter the 6-digit code sent to your email"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            verify_button = st.form_submit_button("✅ Verify", use_container_width=True, type="primary")
        
        with col2:
            resend_button = st.form_submit_button("🔄 Resend Code", use_container_width=True)
        
        if verify_button:
            if entered_code:
                is_valid, message = verify_code(email, entered_code)
                
                if is_valid:
                    st.success(f"✅ {message}")
                    st.session_state.verification_code_sent = False
                    return True
                else:
                    st.error(f"❌ {message}")
            else:
                st.warning("Please enter the verification code")
        
        if resend_button:
            # Generate new code
            code = generate_verification_code()
            store_verification_code(email, code)
            
            # Send email
            success, message = send_verification_email(email, code)
            
            if success:
                st.success(f"✅ New code sent to {email}")
            else:
                st.error(f"❌ {message}")
    
    return False


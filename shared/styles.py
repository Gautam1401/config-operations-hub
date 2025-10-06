"""
Shared Styles for Config Operations Hub
Sleek Black Theme - Modern, professional design with perfect alignment
"""

import streamlit as st


def apply_modern_styles():
    """Apply modern CSS styling to the dashboard - Sleek Black Theme with Perfect Alignment"""
    
    st.markdown("""
        <style>
            /* Base Styles */
            .stApp {
                background: #18191A !important;
                color: #F5F5F7 !important;
            }
            .block-container, .css-18e3th9, .element-container {
                background: #18191A !important;
                border-radius: 12px;
            }
            h1, h2, h3, h4, h5, h6, .st-bq, .st-bv, .st-e0, .st-eb {
                color: #F5F5F7 !important;
            }
            p, span, div, label {
                color: #F5F5F7 !important;
            }
            
            /* KPI Cards Row - CSS Grid for Perfect Alignment */
            .kpi-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 16px;
                margin: 1.5em 0;
                max-width: 100%;
            }
            .kpi-card {
                border-radius: 12px;
                padding: 24px 16px;
                min-height: 120px;
                font-size: 2em;
                font-weight: 700;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #fff;
                text-align: center;
                flex-direction: column;
                box-shadow: 0 2px 8px 0 rgba(0,0,0,0.19);
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                position: relative;
                box-sizing: border-box;
            }
            .kpi-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }
            .kpi-card.selected {
                box-shadow: 0 0 0 3px #FFD700, 0 4px 12px rgba(255, 215, 0, 0.4);
            }
            
            /* KPI Color Classes */
            .kpi-success { background: #29C46F; }
            .kpi-warning { background: #FF9800; }
            .kpi-error { background: #F44336; }
            .kpi-accent { background: #3874F2; }
            .kpi-info { background: #17a2b8; }
            .kpi-primary { background: #008080; }
            .kpi-grey { background: #23272F; color: #B0B8C8; }
            
            /* Button Row - Matches KPI Grid Exactly */
            .button-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 16px;
                margin: 0 0 2em 0;
                max-width: 100%;
            }
            .kpi-button {
                background: transparent;
                color: #F5F5F7;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                font-weight: 600;
                font-size: 0.95em;
                cursor: pointer;
                transition: all 0.2s;
                text-align: center;
                box-sizing: border-box;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .kpi-button:hover {
                background: #2b2f38;
                color: #3874F2;
            }
            
            /* Region Cards/Buttons - Grid Layout */
            .region-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 12px;
                margin: 1.5em 0;
                max-width: 100%;
            }
            .region-btn {
                background: #23272F;
                color: #fff !important;
                border-radius: 9px;
                padding: 18px 16px;
                font-weight: 600;
                font-size: 1.05em;
                border: 2px solid #2b2b30;
                transition: all 0.2s;
                cursor: pointer;
                text-align: center;
                box-sizing: border-box;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .region-btn:hover {
                background: #2b2f38;
                border-color: #3874F2;
            }
            .region-btn.selected {
                background: #3874F2;
                color: #fff !important;
                border-color: #3874F2;
                box-shadow: 0 0 0 2px rgba(56, 116, 242, 0.3);
            }
            
            /* Implementation Type Pills - Grid Layout */
            .impl-type-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 12px;
                margin: 1.5em 0;
                max-width: 100%;
            }
            .impl-type-btn {
                background: #23272F;
                color: #fff !important;
                border-radius: 9px;
                padding: 16px 12px;
                font-weight: 600;
                font-size: 1em;
                border: 2px solid #2b2b30;
                transition: all 0.2s;
                cursor: pointer;
                text-align: center;
                box-sizing: border-box;
            }
            .impl-type-btn:hover {
                background: #2b2f38;
                border-color: #3874F2;
            }
            .impl-type-btn.selected {
                background: #3874F2;
                color: #fff !important;
                border-color: #3874F2;
                box-shadow: 0 0 0 2px rgba(56, 116, 242, 0.3);
            }
            
            /* Alert Banner */
            .alert {
                background: #FFD600;
                color: #18191A;
                border-radius: 8px;
                padding: 18px 24px;
                margin-bottom: 18px;
                font-weight: 700;
                font-size: 1.1em;
            }
            
            /* Download Button */
            .stDownloadButton > button {
                background: #3874f2;
                color: #fff;
                border-radius: 9px;
                font-weight: 600;
                border: none;
                transition: all 0.2s;
            }
            .stDownloadButton > button:hover {
                background: #2d5fd1;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(56, 116, 242, 0.3);
            }
            
            /* Radio Buttons */
            .stRadio > div {
                flex-direction: row;
                gap: 12px;
            }
            .stRadio > div > label {
                background: #23272F;
                color: #F5F5F7 !important;
                padding: 10px 18px;
                border-radius: 8px;
                border: 2px solid #2b2b30;
                cursor: pointer;
                transition: all 0.2s;
            }
            .stRadio > div > label:hover {
                border-color: #3874f2;
                background: #2b2f38;
            }
            
            /* Selectbox */
            .stSelectbox > div > div {
                background: #23272F;
                color: #F5F5F7;
                border: 2px solid #2b2b30;
                border-radius: 8px;
            }
            
            /* Tables */
            .dataframe {
                border-radius: 8px;
                overflow: hidden;
                background: #23272F !important;
                color: #F5F5F7 !important;
            }
            .dataframe th {
                background: #2b2f38 !important;
                color: #F5F5F7 !important;
                font-weight: 600;
            }
            .dataframe td {
                background: #23272F !important;
                color: #F5F5F7 !important;
            }
            
            /* Info/Warning boxes */
            .stInfo, .stWarning, .stSuccess, .stError {
                border-radius: 8px;
                padding: 16px;
                background: #23272F !important;
                color: #F5F5F7 !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background: #18191A;
            }
            .stTabs [data-baseweb="tab"] {
                background: #23272F;
                color: #F5F5F7;
                border-radius: 8px 8px 0 0;
                padding: 10px 20px;
                border: 2px solid #2b2b30;
            }
            .stTabs [aria-selected="true"] {
                background: #3874F2;
                color: #fff;
                border-color: #3874F2;
            }
            
            /* Buttons - Visible and styled */
            .stButton > button {
                background: #23272F;
                color: #F5F5F7;
                border: 2px solid #2b2b30;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: 600;
                transition: all 0.2s;
                width: 100%;
                box-sizing: border-box;
                cursor: pointer;
                font-size: 0.9em;
            }
            .stButton > button:hover {
                background: #3874F2;
                border-color: #3874F2;
                color: #fff;
                transform: translateY(-2px);
            }
            
            /* Dividers */
            hr {
                border-color: #2b2b30 !important;
            }
            
            /* Hide Streamlit button focus outline */
            .stButton > button:focus {
                outline: none;
                box-shadow: 0 0 0 2px rgba(56, 116, 242, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)


def render_modern_header(title: str, icon_url: str = "https://img.icons8.com/?size=512&id=w12qCfGNQTGx&format=png"):
    """
    Render modern header with icon and last refresh timestamp - Black Theme
    
    Args:
        title: Dashboard title
        icon_url: URL to icon image
    """
    from datetime import datetime
    
    # Get current timestamp
    current_time = datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
            <h1 style='display: flex; align-items: center; gap: 14px; margin-bottom:2px; color: #F5F5F7 !important;'>
                <img src="{icon_url}" height="38" alt="">
                {title}
            </h1>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='text-align: right; padding-top: 8px;'>
                <span style='color: #86868B; font-size: 13px;'>🔄 Last Refreshed</span><br>
                <span style='color: #F5F5F7; font-size: 14px; font-weight: 500;'>{current_time}</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("---")


def render_upcoming_week_alert(count: int):
    """
    Render upcoming week alert banner
    
    Args:
        count: Number of upcoming go-lives
    """
    
    if count > 0:
        st.markdown(
            f'<div class="alert">⚠️ <b>Upcoming Week Alert</b><br>'
            f'{count} Go-Live(s) scheduled in the next 7 days</div>',
            unsafe_allow_html=True
        )

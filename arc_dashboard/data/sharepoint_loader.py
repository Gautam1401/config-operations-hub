"""
SharePoint Data Loader for ARC Dashboard
Handles connection to SharePoint and loading Excel files via Microsoft Graph API
"""

import pandas as pd
import requests
from io import BytesIO
import msal
from typing import Optional
import streamlit as st


class SharePointLoader:
    """
    Handles authentication and data loading from SharePoint via Microsoft Graph API
    """
    
    def __init__(self, client_id: str, client_secret: str, tenant_id: str, site_url: str):
        """
        Initialize SharePoint loader
        
        Args:
            client_id: Azure AD App Client ID
            client_secret: Azure AD App Client Secret
            tenant_id: Azure AD Tenant ID
            site_url: SharePoint site URL
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.site_url = site_url
        self.access_token = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with Microsoft Graph API using client credentials
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Create MSAL confidential client
            authority = f"https://login.microsoftonline.com/{self.tenant_id}"
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=authority,
                client_credential=self.client_secret,
            )
            
            # Acquire token
            scopes = ["https://graph.microsoft.com/.default"]
            result = app.acquire_token_for_client(scopes=scopes)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                return True
            else:
                error_msg = result.get("error_description", "Unknown error")
                st.error(f"Authentication failed: {error_msg}")
                return False
                
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return False
    
    def get_file_content(self, file_path: str) -> Optional[bytes]:
        """
        Download file content from SharePoint
        
        Args:
            file_path: Path to file in SharePoint (e.g., '/Shared Documents/file.xlsx')
            
        Returns:
            bytes: File content or None if error
        """
        if not self.access_token:
            if not self.authenticate():
                return None
        
        try:
            # Extract site name from URL
            # Example: https://tenant.sharepoint.com/sites/sitename
            site_parts = self.site_url.split('/sites/')
            if len(site_parts) != 2:
                st.error("Invalid SharePoint site URL format")
                return None
            
            tenant_url = site_parts[0]
            site_name = site_parts[1].rstrip('/')
            
            # Get site ID
            site_endpoint = f"https://graph.microsoft.com/v1.0/sites/{tenant_url.split('//')[1]}:/sites/{site_name}"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            site_response = requests.get(site_endpoint, headers=headers)
            if site_response.status_code != 200:
                st.error(f"Failed to get site info: {site_response.text}")
                return None
            
            site_id = site_response.json()['id']
            
            # Get file content
            # Encode the file path
            encoded_path = requests.utils.quote(file_path)
            file_endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:{encoded_path}:/content"
            
            file_response = requests.get(file_endpoint, headers=headers)
            if file_response.status_code == 200:
                return file_response.content
            else:
                st.error(f"Failed to download file: {file_response.text}")
                return None
                
        except Exception as e:
            st.error(f"Error downloading file: {str(e)}")
            return None
    
    def load_excel(self, file_path: str, sheet_name: str = 0) -> Optional[pd.DataFrame]:
        """
        Load Excel file from SharePoint into DataFrame
        
        Args:
            file_path: Path to Excel file in SharePoint
            sheet_name: Sheet name or index to load
            
        Returns:
            pd.DataFrame: Loaded data or None if error
        """
        try:
            # Get file content
            file_content = self.get_file_content(file_path)
            if file_content is None:
                return None
            
            # Read Excel from bytes
            df = pd.read_excel(BytesIO(file_content), sheet_name=sheet_name)
            
            return df
            
        except Exception as e:
            st.error(f"Error loading Excel file: {str(e)}")
            return None


def load_data_from_sharepoint(config: dict) -> Optional[pd.DataFrame]:
    """
    Convenience function to load data from SharePoint
    
    Args:
        config: Dictionary with SharePoint configuration
            - client_id
            - client_secret
            - tenant_id
            - site_url
            - file_path
            
    Returns:
        pd.DataFrame: Loaded data or None if error
    """
    try:
        loader = SharePointLoader(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            tenant_id=config['tenant_id'],
            site_url=config['site_url']
        )
        
        df = loader.load_excel(config['file_path'])
        return df
        
    except Exception as e:
        st.error(f"Failed to load data from SharePoint: {str(e)}")
        return None


if __name__ == '__main__':
    # Test SharePoint loader (requires valid credentials)
    print("SharePoint Loader Module")
    print("This module requires valid Azure AD credentials to test.")
    print("Use the main dashboard to test with mock data first.")


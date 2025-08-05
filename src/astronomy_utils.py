"""Utilities file for proper namespace hygiene"""
import os
import base64
from typing import Dict

DATA_FILEPATH = '../data/'

def construct_astronomy_api_auth() -> str:
    """
    WARN!!! Assumes the .env is loaded and has values for:
        - APPLICATION_ID
        - APPLICATION_SECRET
    Constructs & returns an authorisation string for the Astronomy API
    """
    user_pass = f"{os.getenv('APPLICATION_ID')}:{os.getenv('APPLICATION_SECRET')}"
    auth_string = base64.b64encode(user_pass.encode()).decode()
    return auth_string

def make_request_headers() -> Dict[str, str]:
    """
    WARN!!! Assumes the .env is loaded and has values for:
        - APPLICATION_ID
        - APPLICATION_SECRET
    Makes and returns the headers for the Astronomy API request
    """
    headers = {
        'Authorization': f'Basic {construct_astronomy_api_auth()}',
        'Content-Type': 'application/json'
    }
    return headers

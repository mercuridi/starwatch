"""Utilities file for proper namespace hygiene"""
import os
import base64

DATA_FILEPATH = '../data/'

def construct_astronomy_api_auth():
    """
    WARN!!! Assumes the .env is loaded and has values for:
        - applicationId
        - applicationSecret
    Constructs & returns an authorisation string for the Astronomy API
    """
    user_pass = f"{os.environ.get('applicationId')}:{os.environ.get('applicationSecret')}"
    auth_string = base64.b64encode(user_pass.encode()).decode()
    return auth_string

def make_request_headers():
    """
    WARN!!! Assumes the .env is loaded and has values for:
        - applicationId
        - applicationSecret
    Makes and returns the headers for the Astronomy API request
    """
    headers = {
        'Authorization': f'Basic {construct_astronomy_api_auth()}',
        'Content-Type': 'application/json'
    }
    return headers

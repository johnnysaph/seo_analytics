from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
import sys
import os

# path to json creds
GOOGLE_KEY_PATH = os.getenv("GOOGLE_API_KEY_FILE_PATH")

def get_credentials(google_api_key_path):
    if not google_api_key_path:
        raise ValueError("GOOGLE_API_KEY_FILE_PATH is not set")
    credentials = service_account.Credentials.from_service_account_file(
        google_api_key_path)
    return credentials

def get_service(api_name, api_version, scopes):
    """
    Get a service that communicates to a Google API.
    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
    Returns:
        A service that is connected to the specified API.
    """
    
    try:
        credentials = get_credentials(GOOGLE_KEY_PATH)
        service = build(api_name, api_version, credentials=credentials, cache_discovery=False)
        return service
    except Exception as ex:
        logging.error('Google Authentication Error occurred.')
        logging.error(ex)
        sys.exit(1)
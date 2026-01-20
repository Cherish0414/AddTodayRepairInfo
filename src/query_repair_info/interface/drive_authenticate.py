import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging
import sys
from pathlib import Path

def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(os.path.dirname(sys.executable))
    else:
        return Path(__file__).resolve().parents[3]

BASE_DIR = get_base_dir()
CREDENTIALS_PATH = BASE_DIR / "config" / "credentials.json"
TOKEN_PATH = BASE_DIR / "config" / "token.pickle"
SCOPES = ['https://www.googleapis.com/auth/drive.file']
logger = logging.getLogger(__name__)

def authenticate():
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
        
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    logger.info("Google Drive authentication successful.")
    return build('drive', 'v3', credentials=creds)
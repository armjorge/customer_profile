import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth.exceptions import MalformedError

def youtube_load(working_folder):
    # Define the service account JSON key file path
    SERVICE_ACCOUNT_FILE = os.path.join(working_folder, 'armjorge.json')

    # Authenticate and build the YouTube API client
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        youtube = build("youtube", "v3", credentials=credentials)
        return youtube
    except FileNotFoundError:
        print(f"Service account file not found at {SERVICE_ACCOUNT_FILE}")
    except MalformedError as e:
        print(f"Malformed service account file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None
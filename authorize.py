import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


from config import CONFIGURATIONS


def gmail_authorisation():
    """
    Returns the gmail credentials after authorisation
    """
    creds = None
    print(os.environ.get('GMAIL_TOKEN_PATH'))
    print(CONFIGURATIONS["TOKEN_FILE_PATH"])
    if os.path.exists(CONFIGURATIONS["TOKEN_FILE_PATH"]):
        creds = Credentials.from_authorized_user_file(CONFIGURATIONS["TOKEN_FILE_PATH"], CONFIGURATIONS["SCOPES"])

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CONFIGURATIONS["CLIENT_SECRET_FILE_PATH"], CONFIGURATIONS["SCOPES"])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(CONFIGURATIONS["TOKEN_FILE_PATH"],'w') as token:
            token.write(creds.to_json())
    return creds
import pickle
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive']


def get_fresh_auth_token(auth_folder_path: Path) -> Credentials:
    creds_file_path = auth_folder_path / "credentials.json"

    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=str(creds_file_path), scopes=SCOPES)
    return flow.run_local_server(port=0)


def get_valid_auth_token(auth_folder_path: Path, creds: Credentials) -> Credentials:
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(request=Request())
        else:
            creds = get_fresh_auth_token(auth_folder_path=auth_folder_path)

    return creds


def get_and_save_auth_token(auth_folder_path: Path):
    token_file_path = auth_folder_path / "token.pickle"

    try:
        with token_file_path.open(mode="rb") as token:
            creds: Credentials = pickle.load(file=token)
    except FileNotFoundError:
        creds = get_fresh_auth_token(auth_folder_path=auth_folder_path)
    else:
        creds = get_valid_auth_token(auth_folder_path=auth_folder_path, creds=creds)

    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(obj=creds, file=token)

    return creds

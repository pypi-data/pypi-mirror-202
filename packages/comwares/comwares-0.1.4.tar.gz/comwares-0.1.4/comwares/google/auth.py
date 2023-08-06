from __future__ import print_function
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os


def update_token(scopes=None, path='creds/'):
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:1087'
    SCOPES = scopes or ['https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists(path + 'token.pickle'):
        with open(path + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(path + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


if __name__ == '__main__':
    creds = update_token()
    print(creds)

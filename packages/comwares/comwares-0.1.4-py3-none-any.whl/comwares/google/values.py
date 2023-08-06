from comwares.google.auth import *
from googleapiclient.discovery import build
import os


def get_sheet_values(sheet_id, range, path='comwares/google/creds/'):
    if os.path.exists(path + 'token.pickle'):
        with open(path + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
        if not creds.valid:
            creds = update_token(path=path)
    else:
        creds = update_token(path=path)

    if creds is not None:
        # Call the Sheets API
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
        values = result.get('values')
        return values


if __name__ == '__main__':
    sheet_id = '1Uymx_ETfkZBi5DiFYCMvwMt3oLf_rg17mUXCDCsd5Ks'
    print(get_sheet_values(sheet_id=sheet_id))

from __future__ import print_function
import pickle
import os.path
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import io
from comwares.google.auth import update_token


def build_service(service_type, version, path='comwares/google/creds/'):
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:1087'
    creds = None
    if os.path.exists(path + 'token.pickle'):
        with open(path + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        print('No creds found or creds is not valid, update oauth token first.')
        creds = update_token(path=path)
        print('Token has been updated.')
    service = build(service_type, version, credentials=creds)
    print('Service has been built.')
    return service


def test_service(service):
    # Call the Drive v3 API
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def download_gdrive_file(drive_service, file_id, to_filename):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download {progress}%.".format(progress=int(status.progress() * 100)))
    with open(to_filename, 'wb') as f:
        f.write(fh.read())


def search_file(drive_service, first_keyword: str, extra_keywords: list = None):
    page_token = None
    query = "name contains '{kw}'".format(kw=first_keyword)
    if extra_keywords is not None:
        for kw in extra_keywords:
            query += " and name contains '{kw}'".format(kw=kw)
    print('Query: ', query)
    files_found = []
    while True:
        response = drive_service.files().list(q=query,
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            files_found.append(file)
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files_found


def main(path):
    build_service(path=path)


if __name__ == '__main__':
    drive_service = build_service(service_type='drive', version='v3', path='creds/')
    # test_service(drive_service)
    # files_found = search_file(drive_service, first_keyword='橙联', extra_keywords=['.xlsx'])
    # print(files_found)

    download_gdrive_file(drive_service=drive_service,
                         file_id='1DatB08pH4pN3Ntyc2jS9DjXaJ7bDApeY',
                         to_filename='橙联_2020-05-16.xlsx')







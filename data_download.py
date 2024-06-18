import csv
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError


CREDENTIALS_FILE = 'google_account.json'  # имя файла с закрытым ключом

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, CREDENTIALS_FILE)

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials).spreadsheets() #.values()

SAMPLE_RANGE_NAME = 'Кураторы'
STAT_RANGE_NAME = 'Статистика (ПБ)'
#------------------------------------------------------------

def downloader(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, filename):
    #print('-------------Загрузка-------------данных-------------')
    try:
        result = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        data_from_sheet = result.get('values', [])
        #print('---------------Запись--данных--в--файл---------------')
        with open(filename, 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data_from_sheet)
            file.close()
        return 0
    except HttpError:
        print('HttpError: ', SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
        return 1
